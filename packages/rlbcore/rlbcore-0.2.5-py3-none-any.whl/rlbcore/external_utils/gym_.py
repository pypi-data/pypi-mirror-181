import typing as t

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


def get_final_episode_observations(
    next_observations: np.ndarray[t.Any, np.dtype[t.Any]],
    dones: np.ndarray[t.Any, np.dtype[np.bool_]],
    infos: dict[str, t.Any],
) -> np.ndarray[t.Any, np.dtype[t.Any]]:
    """Get the final observations of the episodes.

    VectorEnv returns the first observation of the new episode as part of
    next_observations when an episode ends and the final observation of the previous
    episode as part of the infos dict. This function returns the final observation of
    the episode as part of next_observations.

    Args:
        next_observations: The next observations returned by the environment.
        dones: The dones returned by the environment.
        infos: The infos returned by the environment. Must contain key named
            `final_observation`.

    Returns:
        next_observations with the first observation of new episode replaced with
        final observation of previous episode.

    Example: When there is no episode completion, next_observations is returned as is.
        ```python
        >>> from rlbcore.external_utils import get_final_episode_observations
        ... next_observations = np.array([1, 2, 3])
        ... dones = np.array([False, False, False])
        ... infos = {}
        ... assert np.equal(
        ...     get_final_episode_observations(next_observations, dones, infos),
        ...     np.array([1, 2, 3])
        ... ).all()

        ```

    Example: When there is an episode completion.
        ```python
        >>> from rlbcore.external_utils import get_final_episode_observations
        ... next_observations = np.array([1, 2, 3])
        ... dones = np.array([False, False, True])
        ... infos = {"final_observation": np.array([None, None, np.array(6)])}
        ... assert np.equal(
        ...     get_final_episode_observations(next_observations, dones, infos),
        ...     np.array([1, 2, 6])
        ... ).all()

        ```

    See also:
        [gymnasium.vector.VectorEnv.step](https://gymnasium.farama.org/api/vector/
            #gymnasium.vector.VectorEnv.step) for more details on this behavior.
    """
    if not dones.any():
        return next_observations
    result: np.ndarray[t.Any, np.dtype[t.Any]] = next_observations.copy()
    for done_idxs in np.argwhere(dones):
        done_idx = done_idxs[0]
        result[done_idx] = infos["final_observation"][done_idx]
    return result
