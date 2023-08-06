"""Commands for the `rlbcore` CLI command group `rlbcore list`."""
from pathlib import Path

import rich
import typer
from rich.panel import Panel
from rich.table import Table

app = typer.Typer()


@app.command()
def agents(
    rlb_repo_root: Path = typer.Argument(
        ...,
        help="The path to the root of the RLBaselines project using `rlbcore`.",
    ),
    rlb_project_name: str = typer.Argument(
        ...,
        help="The name of the RLBaselines project using `rlbcore`.",
    ),
):
    """List available agents.

    Args:
        rlb_repo_root (Path): The path to the root of the RLBaselines project using
            `rlbcore`.
        rlb_project_name (str): The name of the RLBaselines project using `rlbcore`.
            Valid values are:
                - "rlbtorch"
                - "rlbtf"
                - "rlbjax"
                - "rlbft"

    IMPORTANT:
        This command assumes that the RLBaselines project using `rlbcore` follows the
        standard directory structure. If it does not, this command will not work.

        See [Adding new agents](../../docs/adding-new-agents.md) for more details.
    """
    if not rlb_repo_root:
        raise ValueError("rlb_repo_root must be provided")
    if not rlb_project_name:
        raise ValueError("rlb_project_name must be provided")
    elif rlb_project_name not in ("rlbtorch", "rlbtf", "rlbjax", "rlbft"):
        raise ValueError(
            "rlb_project_name must be one of: rlbtorch, rlbtf, rlbjax, rlbft"
        )
    rlb_repo_root_path = Path(rlb_repo_root)
    agents = Table(show_header=False, header_style="bold magenta", expand=True)
    agents.add_column("Agent", justify="left", style="cyan", no_wrap=True)
    for train_module in (rlb_repo_root_path / rlb_project_name / "agents").glob(
        "*/train.py"
    ):
        agent_module = train_module.parent
        if not agent_module.name.startswith("_"):
            agents.add_row(agent_module.name)
    rich.print(Panel(agents, title="Available Agents", title_align="center"))
    typer.Exit()
