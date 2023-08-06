"""The WandBUI visualizes training progress in W&B and logs metrics to W&B."""
import typing as t
from pathlib import Path

import attrs
import pydantic as pdt
import wandb
from wandb.wandb_run import Run

from rlbcore import api


@attrs.define()
class WandBUI(api.UI):
    """Visualizes training progress in W&B and logs metrics to W&B.

    Args:
        name (str): The name of the experiment.
        config (pydantic.BaseModel): The exp config to store in W&B.
        project (str | None): The W&B project to log to.
        entity (str | None): The W&B entity (team) to log to.
        tags (List[str]): The tags to log to W&B.
        notes (str | None): The notes to log to W&B.
        mode (str): The mode to log to W&B. One of "online", "offline", "disabled".
        reinit (bool): Whether to reinitialize the W&B run.
        group (str | None): The group to log to W&B.
        save_code (bool): Whether to save the code to W&B.
        watch_model_log (str): The type of model logging to do. One of "gradients",
            "parameters", "all". Defaults to "all".
        watch_model_log_graph (bool): Whether to log the model graph. Defaults to True.
        watch_model_log_freq (int): The frequency of model logging. Defaults to 5000.

    Attributes:
        EP_RETURN_STEP (str): The key for the custom metric against which episode
            returns will be logged.
        EP_RETURN_KEY (str): The key used to log episode returns.
        TRAIN_KEY (str): The key used to group episode returns logged during training.
        EVAL_KEY (str): The key used to group episode returns logged during evaluation.
        wandb_run (wandb.wandb_run.Run | None): The underlying wandb Run object.
        custom_metrics (set[str]): Custom metrics being logged to W&B.
        tables (dict[str, wandb.Table]): Any tables being logged to W&B.
        watched_models (set[str]): The names of the models being watched.
    """

    EP_RETURN_STEP: t.ClassVar[str] = "ep_return_step"
    EP_RETURN_KEY: t.ClassVar[str] = "ep_return"
    TRAIN_KEY: t.ClassVar[str] = "train"
    EVAL_KEY: t.ClassVar[str] = "eval"

    name: str
    config: pdt.BaseModel
    repo_root: Path
    project: str | None = "RLBaselines"
    entity: str | None = None
    tags: t.List[str] = attrs.field(factory=list)
    notes: str | None = None
    mode: t.Literal["online", "offline", "disabled"] = "online"
    reinit: bool = False
    group: str | None = None
    save_code: bool = True

    _wandb_run: Run | None = attrs.field(init=False, default=None)
    custom_metrics: set[str] = attrs.field(init=False, factory=set)
    tables: dict[str, wandb.Table] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self) -> None:
        """Initialize the W&B run."""
        self._wandb_run = t.cast(
            Run,
            wandb.init(
                name=self.name,
                project=self.project,
                entity=self.entity,
                tags=self.tags,
                notes=self.notes,
                mode=self.mode,
                reinit=self.reinit,
                group=self.group,
                config=self.config.dict(),
            ),
        )
        if self.save_code:
            self._wandb_run.log_code(root=self.repo_root)
        self._wandb_run.define_metric(self.EP_RETURN_STEP)
        for key in (self.TRAIN_KEY, self.EVAL_KEY):
            self._wandb_run.define_metric(
                f"{key}/{self.EP_RETURN_KEY}", step_metric=self.EP_RETURN_STEP
            )
        self.custom_metrics.update(
            (
                self.EP_RETURN_STEP,
                f"{self.TRAIN_KEY}/{self.EP_RETURN_KEY}",
                f"{self.EVAL_KEY}/{self.EP_RETURN_KEY}",
            )
        )

    @property
    def wandb_run(self) -> Run:
        """Get the underlying wandb Run object."""
        if self._wandb_run is None:
            raise RuntimeError("The W&B run is not initialized.")
        return self._wandb_run

    def log_ep_return(
        self, step: int, avg_return: float, mode: t.Literal["train", "eval"] = "train"
    ) -> None:
        """Log the episode returns averaged over all episodes finishing at this step.

        Args:
            step: The step at which the episode finished.
            avg_return: The average return over all episodes finishing at this step.
            mode: Whether or not the episode was generated during training.
                Supported modes are:
                - "train": The episode was generated during training.
                - "eval": The episode was generated during evaluation.

        EFFECT:
            Logs the episode return to W&B.

        NOTE:
            Depending on the mode, the episode return is logged to a different W&B
            chart. The train ep returns are under the `train` section, where as the
            eval ep returns are under the `eval` section.

        NOTE:
            The avg_return is logged against a custom metric called `ep_return_step`.
            This is done so that you can log losses and returns against the same
            step, but by using two different log calls.

        TODO: Add images showing the UI showing train / eval episode returns.
        """
        self.wandb_run.log({f"{mode}/ep_return": avg_return, self.EP_RETURN_STEP: step})

    def log(self, step: int, metrics: dict[str, t.Any], **kwargs: t.Any) -> None:
        """Log the metrics to W&B.

        Args:
            step: The step at which the metrics were logged.
            metrics: The metrics to log.
            kwargs: Ignored.

        EFFECT:
            Logs the metrics to W&B.

        TODO: Add images showing the UI showing the logged metrics.
        """
        wandb_log_kwargs = {k: v for k, v in kwargs.items() if k == "commit"}
        self.wandb_run.log(metrics, step=step, **wandb_log_kwargs)
