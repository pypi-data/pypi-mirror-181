"""Protocol to define a new agent in an RLBaselines project.

See [Adding new agents](../../sections/adding_new_agents.md) for details on how to add
new agents to any RLBaselines project.

API:
"""
import typing as t

import pydantic as pdt

ConfigT_contra = t.TypeVar("ConfigT_contra", bound=pdt.BaseModel, contravariant=True)
ConfigT_co = t.TypeVar("ConfigT_co", bound=pdt.BaseModel, covariant=True)
ConfigT = t.TypeVar("ConfigT", bound=pdt.BaseModel)


class TrainFunc(t.Protocol[ConfigT_contra]):
    """Protocol for a function that trains an agent.

    IMPORTANT:
        If you want `rlbcore` CLI to be able to detect your agent, then you must expose
        a `train` function from your agent's module that follows this protocol.

        See [Adding new agents](../../sections/adding_new_agents.md) for details on how
        to add new agents to any RLBaselines project.

    Example:
        - See the module docstring for an example.
        - [TODO]: Add link to `rlbtorch`, `rlbtf`, `rlbjax` and `rlbft` examples.
    """

    def __call__(self, config: ConfigT_contra) -> None:
        raise NotImplementedError


class LoadConfigFunc(t.Protocol[ConfigT_co]):
    """Protocol for a function that loads a config.

    IMPORTANT:
        If you want your agent to be detected by the `rlbcore` CLI, then you must expose
        a `load_config` function from your agent's module that follows this protocol.

    Example:
        - See the module docstring for an example.
        - [TODO] Add links to `rlbtorch`, `rlbtf`, `rlbjax` and `rlbft` examples.
    """

    def __call__(self, data: dict[str, t.Any]) -> ConfigT_co:
        raise NotImplementedError
