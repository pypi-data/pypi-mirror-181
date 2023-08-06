import abc
import typing as t


class UI(abc.ABC):
    """A UI is used to display the training progress and results.

    EXAMPLE: Create a UI and log episode returns.
        ```python
        from gymnasium.vector import make as vector_make
        ui = WandBUI()  # or any other UI subclass
        env = vector_make("Pendulum-v1", 2)
        ui.setup()
        actions = ...
        obs, _ = env.reset()
        ep_return = 0
        for step in range(1000):
            obs, rewards, dones, _ = env.step(actions)
            ep_return += rewards
            if dones.any():
                ui.log_ep_return(step, np.extract(dones, ep_return))
        ```

    See [the CliUI](../uis/cli.md#CliUI) for an example of a UI that logs the episode
    returns to the command line.

    See [the WandBUI](../uis/wandb_.md#WandBUI) for an example of a UI that logs the
    metrics to W&B.

    """

    def setup(self, **kwargs: t.Any) -> None:
        """Setup the UI.

        IMPORTANT:
            You must call this method before logging anything to the UI.

        Args:
            kwargs: Additional keyword arguments specific to the UI.
        """
        pass

    def cleanup(self, **kwargs: t.Any) -> None:
        """Cleanup the UI.

        IMPORTANT:
            Don't forget to call this method when you're done with the UI to release
            resources.

        Args:
            kwargs: Additional keyword arguments specific to the UI.
        """
        pass

    @abc.abstractmethod
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

        See [the CliUI](../uis/cli.md#CliUI) for an example of a UI that logs the
        episode returns to the console.

        See [the WandBUI](../uis/wandb_.md#WandBUI) for an example of a UI that logs the
        episode returns to [Weights & Biases](https://wandb.ai/site).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def log(self, step: int, metrics: dict[str, t.Any], **kwargs: t.Any) -> None:
        """Log the given values to the UI.

        Args:
            step: The step at which the values were logged.
            metrics: The values to log.
            kwargs: Additional keyword arguments specific to the UI.

        See [the WandBUI](../uis/wandb_.md#WandBUI) for an example of a UI that logs
        values to [Weights & Biases](https://wandb.ai/site).

        EXAMPLE: Logging multiple values to the UI.
            ```python
            from rlbcore.uis import WandBUI
            ui = WandBUI(...)
            qf1_loss = ...
            qf2_loss = ...
            qf_loss = qf1_loss + qf2_loss
            ui.log(
                step,
                {
                    "losses/qf1_loss": qf1_loss,
                    "losses/qf2_loss": qf2_loss,
                    "losses/qf_loss": qf_loss
                }
            )
            ```
        """
        raise NotImplementedError
