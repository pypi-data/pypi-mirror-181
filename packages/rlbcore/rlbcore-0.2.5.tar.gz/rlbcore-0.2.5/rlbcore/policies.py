"""Common utilities for policies / policy classes."""
import typing as t

import attrs
import numpy as np
import numpy.typing as npt
from gymnasium import spaces as gym_spaces
from gymnasium.vector import VectorEnv

from rlbcore import external_utils as extu

DTypeT = t.TypeVar("DTypeT", np.float32, np.int32)


@attrs.define()
class ContinuousRandomPolicy(t.Generic[DTypeT]):
    """A policy that generates random actions for continuous action space envs.

    Args:
        action_space_low (float | np.ndarray): The lower bound of the action space.
        action_space_high (float | np.ndarray): The upper bound of the action space.
        action_dtype (np.dtype): The dtype of the action space.
        shape (tuple[int, ...]): The shape of the action space. If None, it is
            inferred from action_space_high.
        rng (np.random.Generator): The random number generator for reproducibility.

    NOTE: action_space_high and action_space_low must be the spaces of a single env in
    the vectorized env.

    Example: Use a random policy to generate actions for a vectorized env.
        ```python
        >>> import numpy as np
        ... from gymnasium.vector import make as vector_make
        ... from rlbcore.policies import ContinuousRandomPolicy
        ... env = vector_make("Pendulum-v1", 2)
        ... policy = ContinuousRandomPolicy.from_env(env)
        ... observations, _ = env.reset(seed=0)
        ... rng = np.random.default_rng(0)
        ... actions = policy(observations.shape[0], rng=rng)
        ... assert np.allclose(
        ...     actions, np.array([[1.4024], [0.5478]]), atol=1e-4, rtol=0
        ... ), actions
        ... result = env.step(actions)
        ... assert isinstance(result, tuple)

        ```
    """

    action_space_high: float | npt.NDArray[t.Any]
    action_space_low: float | npt.NDArray[t.Any]

    action_dtype: DTypeT = attrs.field(default=np.float32)  # type: ignore
    shape: tuple[int, ...] = attrs.field(default=None)
    rng: np.random.Generator = attrs.field(factory=np.random.default_rng)

    @classmethod
    def from_env(
        cls,
        env: VectorEnv,
        action_dtype: DTypeT = np.float32,  # type: ignore
        rng: np.random.Generator | None = None,
    ) -> "ContinuousRandomPolicy[DTypeT]":
        """Create a policy from an environment."""
        rng = rng or np.random.default_rng()
        action_space: gym_spaces.Space[t.Any] = env.single_action_space
        assert isinstance(action_space, gym_spaces.Box)
        return cls(
            action_space.high,
            action_space.low,
            action_dtype=action_dtype,
            shape=action_space.shape,
            rng=rng,
        )

    def __attrs_post_init__(self) -> None:
        if not self.shape:
            if isinstance(self.action_space_high, float):
                self.shape = ()
            else:
                self.shape = self.action_space_high.shape

    def __call__(
        self,
        batch_size: int,
        rng: np.random.Generator | None = None,
    ) -> np.ndarray[t.Any, np.dtype[DTypeT]]:
        """Generate random actions.

        Args:
            batch_size: The number of actions to generate.
            rng: The random number generator to use. If None, will use the default
                generator of this class.

        Returns:
            The random actions with shape (batch_size, *self.size).
        """
        rng = rng or self.rng
        random_unscaled_action: npt.NDArray[DTypeT] = rng.random(
            (batch_size, *self.shape),
            dtype=self.action_dtype,  # type: ignore
        )
        return extu.rescale(
            random_unscaled_action,
            old_min=0.0,
            old_max=1.0,
            new_min=self.action_space_low,
            new_max=self.action_space_high,
        )
