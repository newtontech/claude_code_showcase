"""Base planner interface."""

from abc import ABC, abstractmethod

from openmanus.models.plan import Plan


class Planner(ABC):
    """Abstract base class for planners.

    A planner is responsible for converting a user's natural language
    task description into a structured execution plan.
    """

    @abstractmethod
    def generate_plan(self, goal: str, workspace_root: str) -> Plan:
        """Generate an execution plan for the given goal.

        Args:
            goal: The user's natural language task description
            workspace_root: The root directory for file operations

        Returns:
            A structured Plan that can be executed

        Raises:
            PlanningError: If plan generation fails
        """
        raise NotImplementedError

    @abstractmethod
    def estimate_risk_level(self, plan: Plan) -> str:
        """Estimate the risk level of a plan.

        Args:
            plan: The plan to evaluate

        Returns:
            Risk level: "LOW", "MEDIUM", or "HIGH"
        """
        raise NotImplementedError


class PlanningError(Exception):
    """Exception raised when planning fails."""

    pass
