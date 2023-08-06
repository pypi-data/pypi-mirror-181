"""Custom api.UI classes exist in this directory.

A UI enables one to visualize training progress, and optionally log metrics to the UI.

EXAMPLE: CliUI
    The CliUI visualizes training progress in the CLI.

EXAMPLE: WandBUI
    The WandBUI visualizes training progress in W&B and logs metrics to W&B.

EXAMPLE: CompositeUI
    Enables one to log to multiple UIs at the same time.

TODO: MLFlowUI
    The MLFlowUI visualizes training progress in MLFlow and logs metrics to MLFlow.
"""

from rlbcore.uis.cli import CliUI as CliUI
from rlbcore.uis.composite import CompositeUI as CompositeUI
from rlbcore.uis.wandb_ import WandBUI as WandBUI
