import typing as t
from datetime import datetime

import pydantic as pdt


class WandBConfig(pdt.BaseModel):
    """WandB configuration

    Args:
        project_name (str): The name of the project to track in WandB.
            Defaults to "RLBTorch".
        entity (str): The entity (team) name.
            Defaults to "RLBTorch".
        save_code (bool): Whether to save code.
        capture_video (bool): If True, capture videos of the agent performance.
            Defaults to False.
        tags (list[str]): WandB tags to organize your experiments.
        notes (str | None): WandB notes.
        mode (str): WandB mode. One of "disabled", "online", "offline".
            Defaults to "online".
        reinit (bool): Whether to reinitialize wandb.
            Defaults to False.
        group (str | None): WandB group.
        watch_model_log (str): What to log about the model. One of "gradients", "all",
            "parameters". Defaults to "all".
        watch_model_log_graph (bool): Whether to log the model graph.
            Defaults to True.
        watch_model_log_freq (int): The frequency of model logging.
            Defaults to 5000.

    Attributes:
        init_config (dict[str, t.Any]): The config to pass to wandb.init.

    TODO:
        - Implement video capture support.
    """

    project_name: str = pdt.Field(default="RLBTorch", description="WandB project name.")
    entity: str | None = pdt.Field(default=None, description="The entity (team) name.")
    save_code: bool = pdt.Field(default=True, description="Whether to save code.")
    capture_video: bool = pdt.Field(
        default=False, description="If True, capture videos of the agent performance."
    )
    tags: list[str] = pdt.Field(default_factory=list, description="WandB tags.")
    notes: str | None = pdt.Field(default=None, description="WandB notes.")
    mode: t.Literal["disabled", "online", "offline"] = pdt.Field(
        default="online", description="WandB mode."
    )
    reinit: bool = pdt.Field(
        default=False, description="Whether to reinitialize wandb."
    )
    group: str | None = pdt.Field(default=None, description="WandB group.")
    watch_model_log: t.Literal["gradients", "all", "parameters"] = pdt.Field(
        default="all", description="What to log about the model."
    )
    watch_model_log_graph: bool = pdt.Field(
        default=True, description="Whether to log the model graph."
    )
    watch_model_log_freq: int = pdt.Field(
        default=5000, description="How often to log the model."
    )

    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True

    @pdt.validator("capture_video")
    def check_capture_video(cls, value: bool):
        if value:
            raise NotImplementedError(
                "Video capture support has not yet been implemented in RLBTorch"
            )

    @property
    def init_config(self) -> dict[str, t.Any]:
        return dict(
            project=self.project_name,
            entity=self.entity,
            save_code=True,
        )


class ExperimentConfig(pdt.BaseModel):
    """The base class for experiment configuration in rlbtorch.

    The rlbtorch cli knows how to load experiment configuration in a given file.

    Args:
        exp_name (str | None): Name of experiment.
        seed (int): Seed for reproducibility. Defaults to 0.
        cuda_deterministic (bool): If toggled, sets `torch.cuda.manual_seed_all(seed)`.
            Defaults to True.
        cudnn_deterministic (bool): If toggled, sets
            `torch.backends.cudnn.deterministic=False`. Defaults to True.
        cuda (bool): Whether to use CUDA.
            Defaults to False.
        wandb (bool): Whether to track the experiment in WandB.
            Defaults to False.
        wandb_config (WandBConfig): The wandb configuration.
            Defaults to WandBConfig().

    Attributes:
        exp_name (str | None): Name of experiment. Can be None.
        seed (int): Seed for reproducibility.
        cuda_deterministic (bool): If toggled, sets `torch.cuda.manual_seed_all(seed)`.
        cudnn_deterministic (bool): If toggled, sets
            `torch.backends.cudnn.deterministic=False`.
        cuda (bool): Whether to use CUDA.
        cli_ui (bool): If True, shows pretty training progress in CLI.
            See `rlbtorch.uis.cli` for example output.
        safe_exp_name (str): Name of experiment. If exp_name is None, then this is
            set to the format "{agent_name}__{env_id}__{timestamp}".
        wandb (bool): Whether to track the experiment in WandB.
        wandb_config (WandBConfig): The wandb configuration.
        torch_device (torch.device): The torch device to use for the experiment.
        wandb_init_config (dict[str, t.Any]): The config to pass to wandb.init.

    NOTE:
        Enabling CliUI may show noticeable sampling throughput reduction on fast
        algorithms like SAC.
    """

    exp_name: str | None = pdt.Field(default=None, description="Name of experiment.")
    seed: int = pdt.Field(default=0, description="Seed for reproducibility.")
    log_interval: int = pdt.Field(
        default=100,
        description="The number of episodes between logging.",
    )
    cli_ui: bool = pdt.Field(
        default=False, description="Show pretty training progress in the CLI."
    )
    wandb: bool = pdt.Field(
        default=False, description="Whether to track the experiment in WandB."
    )
    wandb_config: WandBConfig = pdt.Field(
        default_factory=WandBConfig,
        description="Config for WandB tracking.",
    )
    start_timestamp: datetime = pdt.Field(
        const=True,
        default_factory=datetime.now,
        description="The start time of the experiment.",
        exclude=True,
    )

    def __init__(self, **data: t.Any):
        super().__init__(**data)

    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True

    @property
    def safe_exp_name(self) -> str:
        if self.exp_name:
            return self.exp_name
        # Assumes that the config class name ends with "Config"
        agent_name = self.__class__.__name__[: -len("Config")]
        env_id = getattr(self, "env_id", "UnknownEnv")
        # Timestamp is in format Mon_Jan_01_22__22_15_32
        timestamp = datetime.strftime(self.start_timestamp, "%a_%b_%d_%y__%H_%M_%S")
        return f"{agent_name}__{env_id}__{timestamp}"

    @property
    def wandb_init_config(self) -> dict[str, t.Any]:
        result = self.wandb_config.init_config
        result["name"] = self.safe_exp_name
        result["config"] = self.copy(deep=True)
        return result
