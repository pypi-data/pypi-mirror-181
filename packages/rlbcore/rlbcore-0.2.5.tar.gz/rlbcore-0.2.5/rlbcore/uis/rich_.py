"""Utilities for working with rich."""
import collections
import time
import typing as t

import attrs
import numpy as np
import pydantic as pdt
import yaml
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TaskID, TextColumn
from rich.syntax import Syntax
from rich.table import Table


@attrs.define()
class Header:
    """Display a header with the experiment name and time elapsed.

    Args:
        exp_name: The name of the experiment.
        start_time: The time at which the experiment started.

    How it looks:
    ![Header](../../resources/images/cli_ui_header.png)
    """

    title: str
    exp_name: str
    start_time: int = attrs.field(init=False, factory=time.time)

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            f"[b]{self.title}:[/b] {self.exp_name}",
            f"Train time: {self._time_elapsed()}",
        )
        return Panel(grid, style="white on blue")

    def _time_elapsed(self) -> str:
        """Return time elapsed since start of training in a human readable format."""
        elapsed = time.time() - self.start_time
        if elapsed < 60:
            return f"{elapsed:.2f}s"
        return f"{elapsed / 60:.2f}m" if elapsed < 3600 else f"{elapsed / 3600:.2f}h"


@attrs.define()
class ConfigPanel:
    """Display the experiment config in a panel.

    Args:
        config (pydantic.BaseModel): The experiment config.

    How it looks:
    -------------
    ![Config Panel](../../resources/images/config_panel.png)
    """

    config: pdt.BaseModel

    def __rich__(self) -> Panel:
        return Panel(
            Syntax(yaml.dump(self.config.dict()), "yaml", line_numbers=True),
            title="Config",
            style="white on blue",
        )


@attrs.define()
class TrainingPanel:
    """Display a progress bar for training.

    Args:
        progress_bar (rich.progress.Progress): The progress bar to display.

    How it looks:
    -------------
    ![Training Panel](../../resources/images/training_panel.png)
    """

    progress_bar: Progress = attrs.field(factory=lambda: Progress(auto_refresh=False))

    def __rich__(self) -> Panel:
        return Panel(self.progress_bar, title="Training")


@attrs.define()
class ObserverPanel:
    """Display a progress bar for showing episode returns.

    Args:
        history (collections.deque[float]): The history of episode returns.
        progress (rich.progres.Progress): Used to display live episode returns.

    How it looks:
    -------------
    ![Observer Panel](../../resources/images/observer_panel.png)
    """

    history: collections.deque[float] = attrs.field(
        factory=lambda: collections.deque(maxlen=50)
    )
    progress: Progress = attrs.field(init=False)
    _task_id: TaskID = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[yellow]{task.fields[step]}"),
            "-->",
            TextColumn("[green]{task.fields[avg_return]:.2f}"),
        )
        self._task_id = self.progress.add_task(
            "Observer", step=0, avg_return=-float("inf")
        )

    def update(self, step: int, avg_return: float) -> None:
        """Update the progress bar with the latest episode return.

        Args:
            step: The current step (mostly indicates number of transitions observed).
            avg_return: The average return of all episodes that finished on this step.
        """
        self.history.append(avg_return)
        self.progress.update(
            self._task_id,
            step=step,
            # Numpy can handle deques quite well, but pyright doesn't know that, so we
            # lie to it.
            avg_return=np.mean(t.cast(list[float], self.history)),
        )

    def __rich__(self) -> Panel:
        return Panel(self.progress, title="Observer")


@attrs.define()
class EpReturnHistory:
    """Display a table of episode returns, one per epoch.

    Args:
        epoch_len: The number of steps per epoch.
        table: The table to display.
        prev_step: The prev step at which a row was added to the table.

    How it looks:
    -------------
    ![Episode Return History](../../resources/images/ep_return_history.png)
    """

    data: collections.deque[tuple[int, float]] = attrs.field(
        factory=lambda: collections.deque(maxlen=25)
    )
    prev_step: int = attrs.field(init=False, default=-1)
    epoch_len: int = attrs.field(init=False, default=10_000)

    def __rich__(self) -> Panel:
        table = Table.grid(expand=True)
        table.add_column("Step", justify="left")
        table.add_column("Avg Return", justify="right")
        table.add_row("Step", "Avg Return")
        table.add_section()
        for step, avg_return in self.data:
            table.add_row(str(step), f"{avg_return:.2f}")
        return Panel(table, title="Episode Return History")

    def update(self, step: int, avg_return: float) -> None:
        """Update the episode return history with the latest episode return.

        Args:
            step: The current step (mostly indicates number of transitions observed).
            avg_return: The average return of all episodes that finished on this step.
        """
        if self.prev_step == -1 or step - self.prev_step >= self.epoch_len:
            self.data.append((step, avg_return))
            self.prev_step = step
