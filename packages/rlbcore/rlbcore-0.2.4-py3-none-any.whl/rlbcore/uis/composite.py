"""The CompositeUI enables one to log to multiple UIs at the same time."""
import typing as t

import attrs

from rlbcore import api


@attrs.define()
class CompositeUI(api.UI):
    """Enables one to log to multiple UIs at the same time.

    Args:
        uis (Sequence[api.UI]): The UIs to log to.

    EXAMPLE: Using the CompositeUI to log to both the CLI and W&B.
        ```python
        import torch
        from gymnasium import make as vector_make
        from rlbcore.uis import CliUI, CompositeUI, WandBUI
        env = vector_make("Pendulum-v1", 2)
        model = torch.nn.Linear(1, 1)
        ui = CompositeUI(
                 uis=[CliUI(exp_name="my_exp", config=pdt.BaseModel()), WandBUI()]
             )
        ui.setup()
        ui.watch_model("model", model)
        ep_return = 0
        obs, _ = env.reset()
        for _ in range(1000):
            obs, rewards, dones, _ = env.step(env.action_space.sample())
            ep_return += rewards
            if dones.any():
                # This will diplay the rewards both in the CLI and W&B.
                ui.log_ep_return(step, np.extract(dones, ep_return))
        ui.cleanup()
        ```
    """

    uis: t.Sequence[api.UI]

    def setup(self, **kwargs: t.Any) -> None:
        """Setup each ui in `self.uis`.

        IMPORTANT:
            You must call this method before logging anything to the UI.

        Args:
            kwargs: Additional keyword arguments specific to the UI.
        """
        for ui in self.uis:
            ui.setup(**kwargs)

    def cleanup(self, **kwargs: t.Any) -> None:
        """Cleanup each ui in `self.uis`.

        IMPORTANT:
            Don't forget to call this method when you're done with the UI to release
            resources.

        Args:
            kwargs: Additional keyword arguments specific to the UI.
        """
        for ui in self.uis:
            ui.cleanup(**kwargs)

    def log_ep_return(
        self,
        step: int,
        avg_return: float,
        mode: t.Literal["train", "eval"] = "train",
    ) -> None:
        """Log the episode return to each ui in `self.uis`.

        Args:
            step: The current step.
            avg_return: The episode return.
            mode: The mode (train or eval) in which the evaluation episodes were run.

        See [the CliUI](../uis/cli.md#CliUI) for an example of a UI that logs the
        episode returns to the command line.

        See [the WandBUI](../uis/wandb_.md#WandBUI) for an example of a UI that logs the
        metrics to W&B.

        """
        for ui in self.uis:
            ui.log_ep_return(step, avg_return, mode)

    def log(
        self,
        step: int,
        metrics: dict[str, t.Any],
        **kwargs: t.Any,
    ) -> None:
        """Log the metrics to each ui in `self.uis`.

        Args:
            step: The current step.
            metrics: The metrics to log.
            kwargs: Additional keyword arguments specific to the UI.
        """
        for ui in self.uis:
            ui.log(step, metrics, **kwargs)
