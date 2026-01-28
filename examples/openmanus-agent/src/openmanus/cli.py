"""CLI interface for OpenManus."""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from openmanus import __version__
from openmanus.config import get_settings
from openmanus.executor import create_default_executor
from openmanus.models.plan import RiskLevel
from openmanus.planner.llm_planner import LLMPlanner
from openmanus.planner.mock_planner import MockPlanner

app = typer.Typer(
    name="openmanus",
    help="OpenManus - A local CLI assistant for macOS",
    add_completion=False,
)

console = Console()


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        console.print(f"[bold green]OpenManus[/bold green] version [bold]{__version__}[/bold]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
    workspace: str = typer.Option(
        None,
        "--workspace",
        "-w",
        help="Workspace root directory",
    ),
    mock: bool = typer.Option(
        False,
        "--mock",
        help="Use mock planner (for testing)",
    ),
) -> None:
    """OpenManus - A local CLI assistant for macOS.

    Plan, confirm, execute, and trace tasks with safety and accountability.
    """
    pass


@app.command()
def run(
    plan_file: Path = typer.Argument(
        ...,
        help="Path to plan.json file to execute",
        exists=True,
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation (only for LOW risk plans)",
    ),
) -> None:
    """Execute a previously saved plan.

    Example: openmanus run runs/20250125-120000/plan.json
    """
    try:
        # Load plan
        executor = create_default_executor()
        plan = executor.load_plan(plan_file)

        # Show plan summary
        _show_plan_summary(plan)

        # Check if confirmation needed
        if not yes and plan.risk_level != RiskLevel.LOW:
            if not _confirm_execution(plan):
                console.print("[yellow]Execution cancelled.[/yellow]")
                raise typer.Exit(code=0)

        # Execute
        console.print("\n[bold cyan]Executing plan...[/bold cyan]\n")
        result = executor.execute_plan(plan)

        # Show result
        _show_execution_result(result)

        # Exit with appropriate code
        if result.overall_status == "success":
            raise typer.Exit(code=0)
        else:
            raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def replay(
    trace_dir: Path = typer.Argument(
        ...,
        help="Path to trace directory to replay",
        exists=True,
    ),
) -> None:
    """View/Replay execution trace.

    Example: openmanus replay runs/20250125-120000
    """
    try:
        executor = create_default_executor()
        result = executor.load_trace(trace_dir)

        _show_trace_result(result)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


def _main_command(
    goal: str,
    yes: bool = False,
    dry_run: bool = False,
    workspace: str | None = None,
    mock: bool = False,
) -> None:
    """Main command implementation (called by both default and explicit forms)."""
    try:
        settings = get_settings()
        workspace_root = workspace or str(settings.workspace_root)

        # Create planner
        if mock:
            planner = MockPlanner()
        else:
            try:
                planner = LLMPlanner()
            except Exception as e:
                console.print(
                    f"[bold red]Error initializing LLM planner:[/bold red] {e}\n"
                    "[yellow]Hint:[/yellow] Set OPENMANUS_API_KEY environment variable\n"
                    "        Or use --mock flag for testing"
                )
                raise typer.Exit(code=1)

        # Generate plan
        console.print(f"[bold cyan]Generating plan for:[/bold cyan] {goal}\n")
        plan = planner.generate_plan(goal, workspace_root)

        # Show plan
        _show_plan_summary(plan)

        # Check if dry run
        if dry_run:
            console.print("\n[yellow]Dry run mode - plan not executed[/yellow]")
            # Still save the plan
            executor = create_default_executor(workspace_root=workspace_root)
            executor._save_plan(plan)
            console.print(f"[green]Plan saved to:[/green] {executor.runs_dir}")
            raise typer.Exit(code=0)

        # Check confirmation
        if not yes:
            if not _confirm_execution(plan):
                console.print("[yellow]Execution cancelled.[/yellow]")
                raise typer.Exit(code=0)
        elif plan.risk_level == RiskLevel.HIGH:
            console.print("[bold red]Refusing to execute HIGH risk plan with --yes flag[/bold red]")
            console.print("[yellow]Remove --yes flag to manually confirm high-risk operations[/yellow]")
            raise typer.Exit(code=1)

        # Execute plan
        console.print("\n[bold cyan]Executing plan...[/bold cyan]\n")
        executor = create_default_executor(workspace_root=workspace_root)
        result = executor.execute_plan(plan)

        # Show result
        _show_execution_result(result)

        # Exit with appropriate code
        if result.overall_status == "success":
            raise typer.Exit(code=0)
        else:
            raise typer.Exit(code=1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


# Handle the case where goal is passed as a standalone argument
@app.command()
def execute(
    goal: str = typer.Argument(..., help="Task description"),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation (only for LOW risk plans)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Only generate plan without executing",
    ),
    workspace: str = typer.Option(
        None,
        "--workspace",
        "-w",
        help="Workspace root directory",
    ),
    mock: bool = typer.Option(
        False,
        "--mock",
        help="Use mock planner (for testing)",
    ),
) -> None:
    """Execute a task by generating and running a plan.

    Examples:
        openmanus execute "Summarize data/notes.txt into 3 bullet points"
        openmanus execute "Summarize data.txt" --yes
        openmanus execute "Process files" --dry-run
    """
    _main_command(goal, yes, dry_run, workspace, mock)


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Handle case where goal is passed directly without 'execute' subcommand."""
    # If no subcommand was given and there are remaining arguments, treat as goal
    if ctx.invoked_subcommand is None and ctx.args:
        # Parse arguments manually for the default case
        goal = ctx.args[0]
        yes = "--yes" in ctx.args or "-y" in ctx.args
        dry_run = "--dry-run" in ctx.args
        workspace = next(
            (
                ctx.args[i + 1]
                for i, arg in enumerate(ctx.args)
                if arg in ["--workspace", "-w"] and i + 1 < len(ctx.args)
            ),
            None,
        )
        mock = "--mock" in ctx.args

        _main_command(goal, yes, dry_run, workspace, mock)
        raise typer.Exit()


@app.command()
def hello(
    name: str = typer.Option("World", help="Name to greet"),
) -> None:
    """Hello world command for testing."""
    console.print(Panel(f"[bold green]Hello, {name}![/bold green]", title="Greeting"))


def _show_plan_summary(plan) -> None:
    """Display a summary of the plan."""
    # Risk level color
    risk_colors = {
        RiskLevel.LOW: "green",
        RiskLevel.MEDIUM: "yellow",
        RiskLevel.HIGH: "red",
    }
    risk_color = risk_colors.get(plan.risk_level, "white")

    console.print(Panel(f"[bold]{plan.goal}[/bold]", title="Plan", border_style=risk_color))
    console.print(f"[bold]Risk Level:[/bold] [{risk_color}]{plan.risk_level.value}[/{risk_color}]")
    console.print(f"[bold]Workspace:[/bold] {plan.workspace_root}")
    console.print(f"[bold]Steps:[/bold] {len(plan.steps)}")

    # Show steps
    console.print("\n[bold]Steps:[/bold]")
    for step in plan.steps:
        console.print(f"  {step.id}. {step.description} [{step.tool}]")

    # Show success criteria
    console.print(f"\n[bold]Success Criteria:[/bold]")
    for criteria in plan.success_criteria:
        console.print(f"  • {criteria}")


def _confirm_execution(plan) -> bool:
    """Ask user to confirm execution."""
    if plan.risk_level == RiskLevel.HIGH:
        console.print("\n[bold red]⚠️  HIGH RISK OPERATION ⚠️[/bold red]")
        console.print("[red]This operation may be dangerous![/red]")

    console.print("\n[yellow]Do you want to proceed?[/yellow] [bold](y/N)[/bold] ", end="")
    response = input().strip().lower()
    return response in ["y", "yes"]


def _show_execution_result(result) -> None:
    """Display execution result."""
    if result.overall_status == "success":
        console.print("\n[bold green]✓ Execution successful![/bold green]")
    else:
        console.print("\n[bold red]✗ Execution failed[/bold red]")

    # Summary stats
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Total steps: {result.total_steps}")
    console.print(f"  Successful: [green]{result.successful_steps}[/green]")
    console.print(f"  Failed: [red]{result.failed_steps}[/red]")
    console.print(f"  Duration: {result.duration_ms}ms" if result.duration_ms else "  Duration: N/A")

    # Produced files
    if result.produced_files:
        console.print(f"\n[bold]Produced files:[/bold]")
        for file_path in result.produced_files:
            console.print(f"  • {file_path}")

    # Trace location
    console.print(f"\n[dim]Trace saved to runs/ directory[/dim]")


def _show_trace_result(result) -> None:
    """Display trace result."""
    console.print(Panel(f"[bold]{result.plan_goal}[/bold]", title="Execution Trace"))

    console.print(f"\n[bold]Status:[/bold] {result.overall_status}")
    console.print(f"[bold]Duration:[/bold] {result.duration_ms}ms" if result.duration_ms else "")
    console.print(f"[bold]Steps:[/bold] {result.successful_steps}/{result.total_steps} successful")

    # Show trace table
    table = Table(title="Step Details")
    table.add_column("Step", style="cyan")
    table.add_column("Tool", style="magenta")
    table.add_column("Status", style="bold")
    table.add_column("Duration", style="dim")

    for trace in result.traces:
        status_color = "green" if trace.status == "success" else "red"
        duration = f"{trace.duration_ms}ms" if trace.duration_ms else "N/A"

        table.add_row(trace.step_id, trace.tool, f"[{status_color}]{trace.status}[/{status_color}]", duration)

    console.print("\n", table)


if __name__ == "__main__":
    app()
