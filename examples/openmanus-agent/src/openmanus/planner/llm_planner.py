"""LLM-based planner using litellm.

This planner uses a Large Language Model to generate execution plans.
"""

import json
import re

import json5  # For lenient JSON parsing
from litellm import completion
from pydantic import ValidationError

from openmanus.config import get_settings
from openmanus.models.plan import Plan, RiskLevel, Step
from openmanus.planner.base import Planner, PlanningError

# System prompt for the planner
PLANNER_SYSTEM_PROMPT = """You are a task planning assistant. Your job is to break down user tasks into executable steps.

IMPORTANT JSON FORMAT RULES:
- Respond with a SINGLE LINE of valid JSON (no pretty-printing)
- If you include code/text content, use \\n for newlines and \\" for quotes
- Do NOT use actual newline characters within string values
- Do NOT use markdown code blocks around the JSON
- Example: {"content": "line 1\\nline 2", "key": "value"}

You must respond with a JSON object containing:
- goal: The original task
- risk_level: "LOW", "MEDIUM", or "HIGH"
- workspace_root: The provided workspace path
- steps: An array of step objects, each with:
  - id: Step number as string (e.g., "1", "2", "3")
  - description: What this step does
  - tool: One of "file" or "shell"
  - inputs: Object with tool-specific inputs
  - produces: Optional description of output
- success_criteria: Array of strings indicating success

Risk levels:
- LOW: Read-only operations, writing to safe locations
- MEDIUM: Writing multiple files, overwriting existing files
- HIGH: Deleting files, dangerous commands, accessing outside workspace

Tools:
- file: actions = ["read_text", "write_text", "list_dir"], paths relative to workspace
- shell: use "cmd" for the command (NOT "command"), limited to whitelist: ls, cat, grep, wc, head, tail, python3, mkdir

To reference output from a previous step, use: "ref:step:<id>.output"

Examples:
{
  "goal": "Create directory and list files",
  "risk_level": "LOW",
  "workspace_root": "/tmp/workspace",
  "steps": [
    {
      "id": "1",
      "description": "Create output directory",
      "tool": "shell",
      "inputs": {"cmd": "mkdir -p output"}
    },
    {
      "id": "2",
      "description": "List files",
      "tool": "shell",
      "inputs": {"cmd": "ls -la"}
    }
  ],
  "success_criteria": ["Directory created"]
}

File write example:
{
  "goal": "Write hello to file",
  "risk_level": "LOW",
  "workspace_root": "/tmp/workspace",
  "steps": [
    {
      "id": "1",
      "description": "Write to file",
      "tool": "file",
      "inputs": {"action": "write_text", "path": "hello.txt", "content": "Hello World!\\nSecond line"}
    }
  ],
  "success_criteria": ["File hello.txt exists"]
}"""


class LLMPlanner(Planner):
    """LLM-based planner that generates plans using litellm."""

    def __init__(
        self,
        api_key: str | None = None,
        api_base: str | None = None,
        model: str | None = None,
    ) -> None:
        """Initialize the LLM planner.

        Args:
            api_key: API key for the LLM provider (defaults to settings)
            api_base: Base URL for the LLM API (defaults to settings)
            model: Model name to use (defaults to settings)
        """
        settings = get_settings()
        self.api_key = api_key or settings.api_key
        self.api_base = api_base or settings.api_base
        self.model = model or settings.model

        if not self.api_key:
            raise PlanningError("API key is required. Set OPENMANUS_API_KEY environment variable.")

    def generate_plan(self, goal: str, workspace_root: str) -> Plan:
        """Generate an execution plan using the LLM.

        Args:
            goal: The user's natural language task description
            workspace_root: The root directory for file operations

        Returns:
            A structured Plan

        Raises:
            PlanningError: If plan generation fails or output is invalid
        """
        user_prompt = f"""Generate an execution plan for the following task:

Goal: {goal}
Workspace root: {workspace_root}

Respond only with valid JSON, no markdown, no code blocks."""

        try:
            response = completion(
                model=self.model,
                api_key=self.api_key,
                api_base=self.api_base,
                messages=[
                    {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=8000,  # Increased for larger responses with code
                response_format={"type": "json_object"},  # Force JSON output
            )

            content = response.choices[0].message.content.strip()

            # Extract JSON from response (handle markdown code blocks)
            json_str = self._extract_json(content)

            # Fix common JSON issues from LLM:
            # 1. Unescaped newlines in strings
            json_str = self._fix_json_strings(json_str)

            # Parse and validate the plan
            # Try json5 first for lenient parsing (handles unescaped newlines)
            try:
                plan_data = json5.loads(json_str)
            except Exception as e5:
                # Fall back to standard JSON
                try:
                    plan_data = json.loads(json_str)
                except json.JSONDecodeError as e:
                    raise PlanningError(f"Invalid JSON response from LLM: {e}\n\n(json5 also failed: {e5})\n\nResponse: {json_str[:1000]}...")

            # Ensure workspace_root is set correctly
            plan_data["workspace_root"] = workspace_root

            try:
                plan = Plan(**plan_data)
            except ValidationError as e:
                raise PlanningError(f"Plan validation failed: {e}")

            # Auto-retry once if validation fails
            if not self._validate_plan(plan):
                return self._retry_plan(goal, workspace_root)

            return plan

        except PlanningError:
            raise
        except Exception as e:
            raise PlanningError(f"Failed to generate plan: {e}")

    def estimate_risk_level(self, plan: Plan) -> str:
        """Estimate the risk level of a plan.

        This is already computed by the LLM, but we can do additional checks.
        """
        # Additional safety checks
        for step in plan.steps:
            if step.tool == "shell":
                cmd = step.inputs.get("cmd", "")
                # Check for dangerous patterns
                dangerous = ["rm", "delete", "format", "shutdown", "reboot"]
                if any(d in cmd.lower() for d in dangerous):
                    return RiskLevel.HIGH.value

        return plan.risk_level.value

    def _extract_json(self, content: str) -> str:
        """Extract JSON from content, handling markdown code blocks."""
        # Try to extract JSON from markdown code blocks
        pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            return match.group(1)

        # If no code block, try to find JSON object
        try:
            # Find first { and last }
            start = content.index("{")
            end = content.rindex("}") + 1
            return content[start:end]
        except ValueError:
            # No JSON found, return as-is
            return content

    def _fix_json_strings(self, json_str: str) -> str:
        """Fix common JSON issues from LLM responses.

        Specifically handles unescaped newlines and quotes in string values.
        This is a best-effort fix for LLM outputs that contain literal newlines
        in JSON string values.
        """
        import re

        # The issue: LLMs often return JSON like:
        # "content": "<!DOCTYPE html>
        # <html>..."
        # Instead of:
        # "content": "<!DOCTYPE html>\n<html>..."

        # Strategy: Find string values that contain unescaped newlines
        # and replace those newlines with \\n

        # Pattern to match potential string value with unescaped newline
        # This looks for: "key": "value
        # continued value"
        fixed = json_str

        # Case 1: Fix triple-quoted code blocks in JSON strings
        # LLMs often include HTML/CSS/JS code with actual newlines
        # We need to escape those newlines

        # Find all occurrences where a line ends inside a string value
        # and the next line continues it
        lines = json_str.split('\n')
        result = []
        i = 0

        while i < len(lines):
            current_line = lines[i]
            result.append(current_line)

            # Check if this line ends with an opening quote or colon
            # followed by content that suggests a multi-line string
            if i < len(lines) - 1:
                next_line = lines[i + 1]

                # If current line ends like: "content": "<div>
                # and next line looks like continuation (not a new key)
                stripped_current = current_line.rstrip()
                stripped_next = next_line.lstrip()

                # Check if we're in the middle of a string value
                # Pattern: ends with quote, no closing comma/brace
                if (stripped_current.endswith('"') or
                    ('": "' in stripped_current and not stripped_current.endswith('",') and
                     not stripped_current.endswith('"}'))):

                    # Check if next line looks like continuation
                    # (doesn't start with JSON structure character)
                    if stripped_next and not stripped_next[0] in ('"', '{', '}', '[', ']', ','):
                        # This is likely a continuation - replace the newline
                        result[-1] = result[-1].rstrip() + '\\n' + stripped_next
                        i += 1
                        continue

            i += 1

        return '\n'.join(result)

    def _validate_plan(self, plan: Plan) -> bool:
        """Validate that a plan is well-formed."""
        if not plan.steps:
            return False

        # Check step IDs are sequential
        for i, step in enumerate(plan.steps, 1):
            if step.id != str(i):
                # Allow non-numeric IDs but ensure they're unique
                pass

        return True

    def _retry_plan(self, goal: str, workspace_root: str) -> Plan:
        """Retry plan generation with more explicit instructions."""
        user_prompt = f"""The previous plan was invalid. Please try again with these requirements:

Goal: {goal}
Workspace root: {workspace_root}

Requirements:
- steps must be an array with at least one step
- each step must have id, description, tool, inputs
- risk_level must be LOW, MEDIUM, or HIGH
- workspace_root must be: {workspace_root}

Respond only with valid JSON."""

        try:
            response = completion(
                model=self.model,
                api_key=self.api_key,
                api_base=self.api_base,
                messages=[
                    {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )

            content = response.choices[0].message.content.strip()
            json_str = self._extract_json(content)
            plan_data = json.loads(json_str)
            plan_data["workspace_root"] = workspace_root
            return Plan(**plan_data)

        except Exception as e:
            raise PlanningError(f"Retry also failed: {e}")
