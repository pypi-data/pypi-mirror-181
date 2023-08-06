"""Various InputTransform and OutputTransform implementations."""

import typing as t

import attrs
import numpy.typing as npt

from rlbcore.api import InputTransform, OutputTransform
from rlbcore.experience import VanillaExperience


class IdentityInputTransform(InputTransform):
    """Identity input transform.

    This is the default input transform for ExperienceReplay. It returns the input data
    unchanged.
    """

    def __call__(self, **kwargs: npt.NDArray[t.Any]) -> dict[str, npt.NDArray[t.Any]]:
        """Return the input data unchanged.

        Args:
            kwargs: The input data.
        """
        return kwargs


@attrs.define()
class ToVanillaExperience(OutputTransform[VanillaExperience]):
    """Transforms a dict of arrays to an Experience.

    This is the default output transform for ExperienceReplay. It transforms a dict of
    arrays to a VanillaExperience. The dict must have the same keys as those in
    VanillaExperience.

    Args:
        n_envs (int): The number of environments. Used to create a buffer of appropriate
            shape.
    """

    n_envs: int

    def __call__(self, **kwargs: npt.NDArray[t.Any]) -> VanillaExperience:
        """Transform a dict of arrays to a VanillaExperience.

        Args:
            kwargs: The input data.

        Returns:
            The transformed data.

        NOTE:
            This expects the input data to have the following shape:
            `(batch_size, n_envs, ...)`. It will reshape the data to
            `(batch_size * n_envs, ...)`.
        """

        def as_batch_shape(key: str, value: npt.NDArray[t.Any]) -> npt.NDArray[t.Any]:
            """Change shape from (batch_size, n_envs, ...) to (batch_size * n_envs, ...)."""  # noqa: E501
            if key in {"rewards", "terminals", "truncateds"}:
                return value.reshape(-1, 1)
            return value.reshape(value.shape[0] * value.shape[1], *value.shape[2:])

        return VanillaExperience(
            **{
                k: as_batch_shape(k, v)
                for k, v in kwargs.items()
                if k in VanillaExperience.keys()
            }
        )
