import typing as t

import attrs
import numpy.typing as npt

from rlbcore.api import Experience


@attrs.define()
class VanillaExperience(Experience):
    """VanillaExperience with numpy arrays.

    Attributes:
        observations: Observations from a batch sampled from the replay buffer.
        actions: Actions from a batch sampled from the replay buffer.
        next_observations: Next observations from a batch sampled from the replay
            buffer.
        rewards: Rewards from a batch sampled from the replay buffer.
        terminals: Terminals from a batch sampled from the replay buffer.
        truncateds: Truncateds from a batch sampled from the replay buffer.
    """

    observations: npt.NDArray[t.Any]
    actions: npt.NDArray[t.Any]
    next_observations: npt.NDArray[t.Any]
    rewards: npt.NDArray[t.Any]
    terminals: npt.NDArray[t.Any]
    truncateds: npt.NDArray[t.Any]

    @classmethod
    def keys(cls) -> set[str]:
        """Returns the keys of the experience."""
        return {
            "observations",
            "actions",
            "next_observations",
            "rewards",
            "terminals",
            "truncateds",
        }

    @property
    def dones(self) -> npt.NDArray[t.Any]:
        """Returns a boolean array indicating whether the episode is done.

        NOTE:
            This returns True irrespective of whether the episode is done due to a
            successful terminal or a time-limit truncation.
        """
        return self.terminals | self.truncateds

    def __len__(self) -> int:
        """Returns the number of experiences in the batch.

        NOTE:
            Assumes that all the arrays have the same length. This should be the case
            since the arrays are all sampled from the same replay buffer.
        """
        return len(self.observations)

    def __getitem__(self, key: str) -> npt.NDArray[t.Any]:
        """Access attributes as keys."""
        if key == "observations":
            return self.observations
        if key == "actions":
            return self.actions
        if key == "next_observations":
            return self.next_observations
        if key == "rewards":
            return self.rewards
        if key == "terminals":
            return self.terminals
        if key == "truncateds":
            return self.truncateds
        raise KeyError(f"Invalid key {key}")
