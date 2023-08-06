"""API followed by all replay buffers."""
import abc
import typing as t

import numpy as np
import numpy.typing as npt


class Experience(abc.ABC):
    """The interface for data sampled from a Memory.

    This class is used to define the interface for data sampled from a Memory. Each
    Experience subclass is defined by a set of keys that can be accessed either as
    attributes or as dictionary keys. The keys are defined by the `keys` classmethod.

    See also:
        - The [experience](../experience.md) module contains examples of how to define
        custom Experience subclasses.
        - The [memory](#memory) class contains an example usage of this class and links
        to subclasses that use Experience subclassese.

    Example: Create a custom experience class for openai gym < 0.25 environments.
        ```python
        >>> from rlbcore.api.memory import Experience
        ... class MyExperience(Experience):
        ...     def __init__(self, observations, actions, next_observations, dones, rewards) -> None:  # noqa: E501
        ...         self.observations = observations
        ...         self.actions = actions
        ...         self.next_observations = next_observations
        ...         self.dones = dones
        ...         self.rewards = rewards
        ...     def __len__(self) -> int:
        ...         return len(self.rewards)
        ...     @classmethod
        ...     def keys(cls) -> set[str]:
        ...         return {"observations", "actions", "next_observations", "dones", "rewards"}
        ...     def __getitem__(self, key: str) -> npt.NDArray[t.Any]:
        ...         try:
        ...             return getattr(self, key)
        ...         except AttributeError:
        ...             raise KeyError(f"{self.__class__} has no key {key}")
        ... experience = MyExperience(
        ...     np.zeros((2, 3)),
        ...     np.zeros((2, 1)),
        ...     np.zeros((2, 3)),
        ...     np.zeros((2,)),
        ...     np.zeros((2,))
        ... )
        ... assert isinstance(experience["observations"], np.ndarray)
        ... assert isinstance(experience.observations, np.ndarray)

        ```
    """

    @abc.abstractmethod
    def __len__(self) -> int:
        """Return the number of samples in the experience.

        Must be defined in subclasses.
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def keys(cls) -> set[str]:
        """Return the set of keys in the experience.

        Must be defined in subclasses.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key: str) -> npt.NDArray[t.Any]:
        raise NotImplementedError

    def __getattr__(self, name: str) -> npt.NDArray[t.Any]:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"{self.__class__} has no attribute {name}") from None


ExperienceT = t.TypeVar("ExperienceT", bound=Experience)
ExperienceT_co = t.TypeVar("ExperienceT_co", bound=Experience, covariant=True)
OutputTransformT = t.TypeVar("OutputTransformT", covariant=True)


class InputTransform(t.Protocol):
    """A protocol for transforming the input to a replay buffer.

    This protocol is used to transform the input to a replay buffer. Typically, the
    input is obtained from calling the environment step function. See the Memory
    subclasses for examples of how this protocol is used.
    """

    def __call__(self, **kwargs: npt.NDArray[t.Any]) -> dict[str, npt.NDArray[t.Any]]:
        raise NotImplementedError


class OutputTransform(t.Protocol[ExperienceT_co]):
    """A protocol for transforming the output of a replay buffer.

    The input is the data (or a subset of it) stored in the replay buffer. The output
    is an instance of Experience.  The transform is used to convert the data stored in
    the replay buffer to an instance of Experience.

    """

    def __call__(self, **kwargs: npt.NDArray[t.Any]) -> ExperienceT_co:
        raise NotImplementedError


class Memory(abc.ABC, t.Generic[ExperienceT]):
    """The interface for replay buffers.

    Attributes:
        input_transform: The input transform.
        output_transform: The output transform.

    # noqa: E501
    See also:
        - The [ExperienceReplay](../memories/experience_replay/vanilla.md#ExperienceReplay)
         class for an
        example implementation of this class.
    """

    input_transform: InputTransform
    output_transform: OutputTransform[ExperienceT]

    @property
    @abc.abstractmethod
    def total_n_samples_seen(self) -> int:
        """Return the total number of samples seen by the replay buffer.

        Returns:
            The total number of samples seen by the replay buffer.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, **kwargs: npt.NDArray[t.Any]) -> None:
        """Add an experience to the replay buffer.

        Args:
            **kwargs: The experience to add to the replay buffer.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, rng: np.random.Generator | None = None) -> ExperienceT:
        """Get a batch of experiences from the replay buffer.

        Args:
            rng: The random number generator to use.

        Returns:
            A batch of experiences.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def flush(self) -> None:
        """Clear the data in the replay buffer."""
        raise NotImplementedError
