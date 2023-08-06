import typing as t

import attrs
import numpy as np
import numpy.typing as npt
from gymnasium.vector import VectorEnv


@attrs.define()
class NumpyCircularBuffer:
    """Circular buffer for numpy arrays.

    Args:
        data (dict[str, np.ndarray]): dict of numpy arrays.

    Attributes:
        data (dict[str, np.ndarray]): dict of numpy arrays.
        capacity (int): capacity of the buffer.
        head (int): point of insertion of the next sample
        total_num_samples_seen (int): total number of samples seen by the buffer

    Example:  Create a buffer with given shapes and dtypes and store data.

        ```python
        >>> import numpy as np
        ... from gymnasium.vector import make as vector_make
        ... from rlbcore.memories.experience_replay.buffers import NumpyCircularBuffer
        ... envs = vector_make("Pendulum-v1", num_envs=2)
        ... buffer = NumpyCircularBuffer.create(
        ...     capacity=3,
        ...     shapes={
        ...         "observations": envs.observation_space.shape,
        ...         "actions": envs.action_space.shape,
        ...         "rewards": (2,),
        ...         "terminals": (2,),
        ...     },
        ...     dtypes={
        ...         "observations": np.float32,
        ...         "actions": np.float32,
        ...         "rewards": np.float32,
        ...         "terminals": bool,
        ...     },
        ... )
        ... assert len(buffer) == 0
        ... envs.reset()
        ... actions = envs.action_space.sample()
        ... observations, rewards, terminals, *_ = envs.step(actions)
        ... buffer.add(
        ...     {
        ...         "observations": observations,
        ...         "actions": actions,
        ...         "rewards": rewards,
        ...         "terminals": terminals,
        ...     }
        ... )
        ... assert len(buffer) == 1

        ```
    """

    data: dict[str, npt.NDArray[t.Any]] = attrs.field(repr=False)

    capacity: int = attrs.field(init=False)
    _head: int = attrs.field(init=False, default=0)
    _filled_once: bool = attrs.field(init=False, default=False)
    _total_n_samples_seen: int = attrs.field(init=False, default=0)

    def __attrs_post_init__(self) -> None:
        self.capacity = next(iter(self.data.values())).shape[0]

    @classmethod
    def create(
        cls,
        capacity: int,
        shapes: dict[str, tuple[int, ...]],
        dtypes: dict[str, npt.DTypeLike],
    ) -> "NumpyCircularBuffer":
        return cls(
            data={
                k: np.empty(shape=(capacity, *v), dtype=dtypes[k])
                for k, v in shapes.items()
            },
        )

    @classmethod
    def from_env(cls, env: VectorEnv, capacity: int) -> "NumpyCircularBuffer":
        """Construct a NumpyCircularBuffer from a VectorEnv.

        Args:
            env (gymnasium.vector.VectorEnv): A VectorEnv to get the shapes and dtypes
            capacity (int): capacity of the buffer.

        Returns:
            NumpyCircularBuffer.

        Example:  Create a buffer from an environment with 2 envs and store data.
            ```python
            >>> import numpy as np
            ... from gymnasium.vector import make as vector_make
            ... from rlbcore.memories import NumpyCircularBuffer
            ... envs = vector_make("Pendulum-v1", num_envs=2)
            ... buffer = NumpyCircularBuffer.from_env(envs, capacity=3)
            ... assert len(buffer) == 0
            ... for _ in range(4):
            ...     observations, _ = envs.reset(seed=0)
            ...     actions = envs.action_space.sample()
            ...     next_observations, rewards, terminals, truncateds, _ = envs.step(
            ...         actions
            ...     )
            ...     buffer.add(
            ...         {
            ...             "observations": observations,
            ...             "actions": actions,
            ...             "next_observations": next_observations,
            ...             "rewards": rewards,
            ...             "terminals": terminals,
            ...             "truncateds": truncateds,
            ...         }
            ...     )
            ... assert len(buffer) == 3
            ... samples = buffer[0]
            ... assert samples["observations"].shape == (2, 3), (
            ...     samples["observations"].shape
            ... )
            ... assert samples["actions"].shape == (2, 1), samples["actions"].shape
            ... assert samples["next_observations"].shape == (2, 3), (
            ...     samples["next_observations"].shape
            ... )
            ... assert samples["rewards"].shape == (2,), samples["rewards"].shape
            ... assert samples["terminals"].shape == (2,), samples["terminals"].shape
            ... assert samples["truncateds"].shape == (2,), samples["truncateds"].shape

            ```
        """
        state_space = env.observation_space  # type: ignore
        action_space = env.action_space  # type: ignore
        state_space_shape = state_space.shape
        action_space_shape = action_space.shape
        n_envs = env.num_envs
        assert isinstance(state_space_shape, tuple)
        assert isinstance(action_space_shape, tuple)
        return cls.create(
            capacity=capacity,
            shapes={
                "observations": state_space_shape,
                "actions": action_space_shape,
                "next_observations": state_space_shape,
                "rewards": (n_envs,),
                "terminals": (n_envs,),
                "truncateds": (n_envs,),
            },
            dtypes={
                "observations": state_space.dtype,
                "actions": action_space.dtype,
                "next_observations": state_space.dtype,
                "rewards": np.float32,
                "terminals": bool,
                "truncateds": bool,
            },
        )

    @property
    def head(self) -> int:
        return self._head

    @property
    def total_n_samples_seen(self) -> int:
        return self._total_n_samples_seen

    def add(self, data: dict[str, npt.NDArray[t.Any]]) -> None:
        """Add experience.

        NOTE:
            data keys must be a subset of self.shapes.keys().

        Args:
            data (dict[str, np.ndarray]): A dictionary of numpy arrays.
        """
        for k, v in data.items():
            self.data[k][self._head] = v
        self._head += 1
        self._total_n_samples_seen += 1
        if self._head == self.capacity:
            self._filled_once = True
            self._head = 0

    def flush(self) -> None:
        """Clear the data in the buffer.

        NOTE:
            Do not count on the underlying data being cleared. The buffer will act as if
            it is empty, but the underlying data will not be cleared.
        """
        self._head = 0
        self._filled_once = False

    def __getitem__(
        self,
        item: int | slice | list[int] | npt.NDArray[np.intp],
    ) -> dict[str, npt.NDArray[t.Any]]:
        """Get a sample or samples from the buffer.

        Args:
            item (int | slice | list[int] | np.ndarray[np.intp]): The index or indices
                of the samples to get.

        Returns:
            dict[str, np.ndarray]: A dictionary of numpy arrays.
        """
        if not len(self):
            raise IndexError("Empty buffer.")
        return {k: v[: len(self)][item] for k, v in self.data.items()}

    def __len__(self) -> int:
        """Get the number of samples in the buffer.

        Returns:
            The number of samples in the buffer.
        """
        return self.capacity if self._filled_once else self._head
