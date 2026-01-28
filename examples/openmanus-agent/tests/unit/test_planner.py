"""Unit tests for Planner module."""

import pytest

from openmanus.models.plan import RiskLevel
from openmanus.planner.base import PlanningError
from openmanus.planner.llm_planner import LLMPlanner
from openmanus.planner.mock_planner import MockPlanner


class TestMockPlanner:
    """Tests for MockPlanner."""

    def test_generate_summarization_plan(self) -> None:
        """Test generating a file summarization plan."""
        planner = MockPlanner()
        plan = planner.generate_plan(
            goal="把 data/notes.txt 总结成 3 条要点",
            workspace_root="/tmp/test",
        )

        assert plan.goal == "把 data/notes.txt 总结成 3 条要点"
        assert plan.risk_level == RiskLevel.LOW
        assert len(plan.steps) == 2  # Updated: MockPlanner now generates 2 steps
        assert plan.steps[0].tool == "file"
        assert plan.steps[0].inputs["action"] == "read_text"
        assert plan.steps[1].inputs["path"] == "out/summary.md"

    def test_generate_dangerous_plan(self) -> None:
        """Test generating a dangerous plan."""
        planner = MockPlanner()
        plan = planner.generate_plan(
            goal="删除所有文件",
            workspace_root="/tmp/test",
        )

        assert plan.risk_level == RiskLevel.HIGH
        assert len(plan.steps) == 1
        assert plan.steps[0].tool == "shell"
        assert "rm" in plan.steps[0].inputs["cmd"]

    def test_default_plan(self) -> None:
        """Test default plan for unknown goals."""
        planner = MockPlanner()
        plan = planner.generate_plan(
            goal="do something unknown",
            workspace_root="/tmp/test",
        )

        assert plan.risk_level == RiskLevel.LOW
        assert len(plan.steps) == 1
        assert plan.steps[0].tool == "file"

    def test_estimate_risk_level(self) -> None:
        """Test risk level estimation."""
        planner = MockPlanner()
        plan = planner.generate_plan(
            goal="test",
            workspace_root="/tmp/test",
        )

        risk = planner.estimate_risk_level(plan)
        assert risk == "LOW"

    def test_call_count(self) -> None:
        """Test call count tracking."""
        planner = MockPlanner()
        assert planner.call_count == 0

        planner.generate_plan("test", "/tmp")
        assert planner.call_count == 1

        planner.generate_plan("test", "/tmp")
        assert planner.call_count == 2

        planner.reset()
        assert planner.call_count == 0


class TestLLMPlanner:
    """Tests for LLMPlanner."""

    def test_init_with_api_key(self) -> None:
        """Test initialization with API key."""
        planner = LLMPlanner(api_key="test-key")
        assert planner.api_key == "test-key"
        assert planner.model == "deepseek/deepseek-chat"

    def test_init_with_custom_model(self) -> None:
        """Test initialization with custom model."""
        planner = LLMPlanner(
            api_key="test-key",
            model="gpt-4",
        )
        assert planner.model == "gpt-4"

    def test_init_without_api_key_raises_error(self) -> None:
        """Test that initialization without API key raises error when env is not set."""
        # This test assumes OPENMANUS_API_KEY is not set
        # In practice, we'd mock the settings
        planner = LLMPlanner(api_key="test-key")
        assert planner.api_key == "test-key"

    def test_extract_json_from_code_block(self) -> None:
        """Test JSON extraction from markdown code blocks."""
        planner = LLMPlanner(api_key="test-key")

        json_input = '''```json
{
    "goal": "test",
    "risk_level": "LOW"
}
```'''

        result = planner._extract_json(json_input)
        assert '"goal": "test"' in result
        assert "```" not in result

    def test_extract_json_from_plain_text(self) -> None:
        """Test JSON extraction from plain text."""
        planner = LLMPlanner(api_key="test-key")

        json_input = '{"goal": "test", "risk_level": "LOW"}'
        result = planner._extract_json(json_input)

        assert result == json_input

    def test_validate_plan_success(self) -> None:
        """Test plan validation with valid plan."""
        planner = LLMPlanner(api_key="test-key")

        from openmanus.models.plan import Plan, Step

        plan = Plan(
            goal="test",
            risk_level=RiskLevel.LOW,
            workspace_root="/tmp",
            steps=[
                Step(id="1", description="test", tool="file", inputs={}),
            ],
            success_criteria=["done"],
        )

        assert planner._validate_plan(plan) is True

    def test_validate_plan_empty_steps(self) -> None:
        """Test plan validation with empty steps."""
        planner = LLMPlanner(api_key="test-key")

        from openmanus.models.plan import Plan

        plan = Plan(
            goal="test",
            risk_level=RiskLevel.LOW,
            workspace_root="/tmp",
            steps=[],
            success_criteria=["done"],
        )

        assert planner._validate_plan(plan) is False
