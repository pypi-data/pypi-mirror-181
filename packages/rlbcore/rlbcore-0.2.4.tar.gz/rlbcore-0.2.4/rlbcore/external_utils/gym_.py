import attrs
import numpy as np
import numpy.typing as npt

from rlbcore import api, uis
from rlbcore.external_utils.other import null_object


@attrs.define()
class EpisodeReturnRecorder:
    """Records episode returns during training and prints them to console.

    Args:
        ui (CliUI): The UI to use for printing the episode returns.

    Example:
        ```python
        >>> from pydantic import BaseModel
        ... from rlbcore.uis import CliUI
        ... recorder = EpisodeReturnRecorder(CliUI("rlb", "foo", BaseModel()))
        ... recorder.track(np.array([1, 2, 3]), np.array([False, False, False]))
        ... recorder.track(np.array([1, 2, 3]), np.array([False, False, True]))
        ... # Prints Step 2: -> Avg Return: 6.00
        ... assert (recorder._episode_returns == np.array([2, 4, 0])).all()
        ... recorder.track(np.array([1, 2, 3]), np.array([False, True, False]))
        ... # Prints Step 3: -> Avg Return: 6.00
        ... assert (recorder._episode_returns == np.array([3, 0, 3])).all()
        ... recorder.track(np.array([1, 2, 3]), np.array([True, False, False]))
        ... # Prints Step 4: -> Avg Return: 4.00
        ... assert (recorder._episode_returns == np.array([0, 2, 6])).all()

        ```
    """

    ui: api.UI = attrs.field(factory=lambda: null_object(uis.CliUI))

    _step: int = attrs.field(init=False, default=0)
    _episode_returns: npt.NDArray[np.float32] = attrs.field(init=False, default=None)

    def track(
        self, rewards: npt.NDArray[np.float32], dones: npt.NDArray[np.bool_]
    ) -> None:
        """Track the episode returns.

        Args:
            rewards: The rewards received in the current step.
            dones: The dones received in the current step.

        Effects:
            Updates the internal state of the recorder.
            On each episode completion, prints the episode return to console.
        """
        self._step += 1
        if self._episode_returns is None:
            self._episode_returns = np.zeros_like(rewards)
        self._episode_returns += rewards
        if not dones.any():
            return
        episode_returns = np.extract(dones, self._episode_returns)
        np.putmask(self._episode_returns, dones, 0)
        avg_return = episode_returns.mean()
        self.ui.log_ep_return(step=self._step, avg_return=avg_return)
