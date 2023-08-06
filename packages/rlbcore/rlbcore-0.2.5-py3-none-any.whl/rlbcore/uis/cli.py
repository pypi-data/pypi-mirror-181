"""The CliUI visualizes training progress in the CLI.

NOTE:
    The CliUI does NOT log metrics to the CLI. For that, use the WandBUI or MLFlowUI.
"""
import typing as t

import attrs
import pydantic as pdt
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.progress import TaskID

from rlbcore import api
from rlbcore.uis.rich_ import (
    ConfigPanel,
    EpReturnHistory,
    Header,
    ObserverPanel,
    TrainingPanel,
)


@attrs.define()
class CliUI(api.UI):
    """Visualizes training progress in the CLI.

    NOTE:
        The CliUI does NOT log metrics to the CLI. For that, use the WandBUI or
        MLFlowUI.
    Args:
        exp_name (str): The name of the experiment.
        config (pydantic.BaseModel): The config to display.
        layout (Layout): The layout of the UI.
        config_panel (ConfigPanel): The panel to display the config.
        training_panel (TrainingPanel): The panel to display the training progress.
        observer_panel (ObserverPanel): The panel to display the observer progress.
        ep_return_history (EpReturnHistory): The panel to display the episode return
            history.

    How it looks:
    -------------
    ![CLI UI](../../resources/images/cli_ui.png)

    USAGE:
        ```python
        >>> import pydantic as pdt
        ... from rlbcore.uis import CliUI
        ... ui = CliUI("RLBCore", exp_name="my_exp", config=pdt.BaseModel())
        ... # No point in adding tasks to the UI if you don't start the ui to display
        ... # them
        ... ui.start()
        ... # There's a task with 3 steps
        ... progress_task_one = ui.add_training_task("[red]SomeName", total=3)
        ... # There's another task with 2 steps
        ... progress_task_two = ui.add_training_task("[blue]SomeOtherName", total=2)
        ... # Track the episode return
        ... ui.log_ep_return(step=1, avg_return=1.0)
        ... # Update the progress bar for the first task
        ... ui.update_training_progress_bar(progress_task_one, advance=1)
        ... ui.log_ep_return(step=2, avg_return=2.0)
        ... ui.update_training_progress_bar(progress_task_one, advance=1)
        ... # Update the progress bar for the second task
        ... ui.update_training_progress_bar(progress_task_two, advance=1)
        ... ui.log_ep_return(step=3, avg_return=3.0)
        ... ui.update_training_progress_bar(progress_task_one, advance=1)
        ... ui.update_training_progress_bar(progress_task_two, advance=1)
        ... # Don't forget to stop the UI to release resources.
        ... ui.stop()

        ```

    """

    title: str
    exp_name: str
    config: pdt.BaseModel
    layout: Layout = attrs.field(factory=lambda: Layout(name="root"))
    config_panel: ConfigPanel = attrs.field(default=None)
    training_panel: TrainingPanel = attrs.field(factory=TrainingPanel)
    observer_panel: ObserverPanel = attrs.field(factory=ObserverPanel)
    ep_return_history: EpReturnHistory = attrs.field(factory=EpReturnHistory)
    live: Live = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        if self.config_panel is None:
            self.config_panel = ConfigPanel(self.config)
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="config", ratio=1),
            Layout(name="training", size=5),
            Layout(name="observer", size=3),
            Layout(name="history", ratio=1),
        )
        self.layout["header"].update(Header(title=self.title, exp_name=self.exp_name))
        self.layout["config"].update(self.config_panel)
        self.layout["training"].update(self.training_panel)
        self.layout["observer"].update(self.observer_panel)
        self.layout["history"].update(self.ep_return_history)
        self.live = Live(self.layout, refresh_per_second=1, screen=True)

    def add_training_task(self, task_name: str, total: int) -> TaskID:
        """Add a task to the training progress bar.

        Args:
            task_name (str): The name of the task. Will be displayed beside the progress
                bar.
            total (int): The total number of steps to complete the task.

        Returns:
            TaskID: The ID of the task. Required to update the progress bar.

        Example:
            ```python
            >>> ui = CliUI("RLBCore", "my_exp", pdt.BaseModel())
            ... ui.start()
            ... # There's a task that will finish in 3 steps
            ... pbar = ui.add_training_task("SomeName", total=3)
            ... for _ in range(3):
            ...     # Do something for the task
            ...     ui.update_training_progress_bar(pbar, advance=1)
            ... # Finally, stop the UI
            ... ui.stop()

            ```
        """
        return self.training_panel.progress_bar.add_task(task_name, total=total)

    def update_training_progress_bar(self, task_id: TaskID, advance: int) -> None:
        """Update the training progress bar.

        Args:
            task_id (TaskID): The ID of the task to update.
            advance (int): The number of steps to advance the progress bar.

        See `CliUI.add_training_task` for an example.
        """
        self.training_panel.progress_bar.update(task_id, advance=advance)

    def log_ep_return(
        self, step: int, avg_return: float, mode: t.Literal["train", "eval"] = "train"
    ) -> None:
        """Update the CLI to show training progress and performance.

        Args:
            step: The current step (mostly indicates number of transitions observed).
            avg_return: The average return of all episodes that finished on this step.
            mode: The mode of the experiment. Either "train" or "eval".
                Currently, CliUI only supports "train" mode.

        TODO:
            - Add support for "eval" mode.

        Example:
            ```python
            >>> from gymnasium import make
            ... ui = CliUI("RLBCore", "my_exp", pdt.BaseModel())
            ... env = make("CartPole-v1")
            ... ui.start()
            ... obs, _ = env.reset()
            ... episode_return = 0
            ... for step in range(10):
            ...     # Step the env
            ...     obs, reward, term, trunc, _ = env.step(env.action_space.sample())
            ...     done = term or trunc
            ...     episode_return += reward
            ...     if done:
            ...         # Track the episode return
            ...         # NOTE: If there are multiple envs that finish on the same step,
            ...         # you must average them before passing them to this function.
            ...         ui.log_ep_return(step=step, avg_return=episode_return)
            ...         # Reset the episode return
            ...         episode_return = 0

            ```
        """
        self.observer_panel.update(step=step, avg_return=avg_return)
        self.ep_return_history.update(step=step, avg_return=avg_return)

    def log(self, step: int, metrics: dict[str, t.Any], **kwargs: t.Any) -> None:
        """The CliUI does not log any values other than the episode return.

        REASON:
            It's very difficult to display charts in the terminal.

        IMPORTANT:
            This function is only here to satisfy the interface. It does nothing.

        Args:
            step: The current step (mostly indicates number of transitions observed).
            metrics: The values to log. This function ignores all values.
            kwargs: Additional arguments specific to the UI. This function ignores all
                values.
        """

    def start(self) -> None:
        """Start the UI.

        IMPORTANT:
            You must call this function if you want to see the UI.
        """
        self.live.start()

    def stop(self) -> None:
        """Stop the UI.

        Call this function when you're done with the UI to release resources.
        """
        self.live.stop()
        console = Console()
        console.rule("Training complete")
        console.print(self.ep_return_history)
