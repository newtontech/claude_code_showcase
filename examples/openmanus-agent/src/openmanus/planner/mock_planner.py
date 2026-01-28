"""Mock planner for testing.

This planner returns fixed responses for testing purposes.
"""

from openmanus.models.plan import Plan, RiskLevel, Step
from openmanus.planner.base import Planner, PlanningError


class MockPlanner(Planner):
    """Mock planner that returns predefined plans for testing.

    This is useful for E2E tests where we want deterministic behavior
    without calling an actual LLM.
    """

    def __init__(self) -> None:
        """Initialize the mock planner."""
        self._call_count = 0

    def generate_plan(self, goal: str, workspace_root: str) -> Plan:
        """Generate a mock plan based on the goal.

        This method has built-in responses for common test scenarios.
        """
        self._call_count += 1

        # Scenario 1: File summarization task
        if "总结" in goal or "summarize" in goal.lower():
            # Determine the input path based on the goal
            if "data/notes.txt" in goal:
                input_path = "data/notes.txt"
            else:
                input_path = "data/notes.txt"  # default

            return Plan(
                goal=goal,
                risk_level=RiskLevel.LOW,
                workspace_root=workspace_root,
                steps=[
                    Step(
                        id="1",
                        description="Read the source file",
                        tool="file",
                        inputs={"action": "read_text", "path": input_path},
                        produces="content:source_content",
                    ),
                    Step(
                        id="2",
                        description="Write summary to output file",
                        tool="file",
                        inputs={
                            "action": "write_text",
                            "path": "out/summary.md",
                            "content": "- Summary point 1\n- Summary point 2\n- Summary point 3",
                        },
                        produces="file:out/summary.md",
                    ),
                ],
                success_criteria=[
                    "File out/summary.md exists",
                    "File contains 3 bullet points starting with '-'",
                    "All steps completed successfully",
                ],
            )

        # Scenario 2: Dangerous command (should be rejected)
        if "删除" in goal or "delete" in goal.lower() or "rm -rf" in goal:
            return Plan(
                goal=goal,
                risk_level=RiskLevel.HIGH,
                workspace_root=workspace_root,
                steps=[
                    Step(
                        id="1",
                        description="Attempt to delete files",
                        tool="shell",
                        inputs={"cmd": "rm -rf *"},
                        produces="file_deletion",
                    ),
                ],
                success_criteria=["Files deleted"],
            )

        # Default: simple file read
        return Plan(
            goal=goal,
            risk_level=RiskLevel.LOW,
            workspace_root=workspace_root,
            steps=[
                Step(
                    id="1",
                    description="Read a file",
                    tool="file",
                    inputs={"action": "read_text", "path": "test.txt"},
                    produces="content:file_content",
                ),
            ],
            success_criteria=["File read successfully"],
        )

    def estimate_risk_level(self, plan: Plan) -> str:
        """Estimate risk level from the plan."""
        return plan.risk_level.value

    @property
    def call_count(self) -> int:
        """Get the number of times generate_plan was called."""
        return self._call_count

    def reset(self) -> None:
        """Reset the call counter."""
        self._call_count = 0
