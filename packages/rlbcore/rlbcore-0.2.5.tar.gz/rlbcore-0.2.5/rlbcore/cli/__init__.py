"""The command line interface for rlbcore."""

import rich
import typer
from rich.panel import Panel

from rlbcore import __version__
from rlbcore.cli import docs, run

app = typer.Typer()
app.add_typer(docs.app, name="docs")
app.add_typer(run.app, name="run")


@app.command()
def version():
    """Print the version number.

    IMPORTANT:
        NOT meant to be used by other RLBaselines projects.
    """
    panel = Panel(
        __version__, title="RLB Core", title_align="center", border_style="blue"
    )
    rich.print(panel)
    typer.Exit()
