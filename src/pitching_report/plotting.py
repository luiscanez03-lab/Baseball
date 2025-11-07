"""Plotting utilities for the pitching report."""
from __future__ import annotations

from itertools import cycle
from typing import Iterable, List, Sequence, Tuple

import matplotlib.pyplot as plt
import pandas as pd

from .data_models import PlotVariable, StartConfig

LINESTYLES = ["-", "--", "-.", ":"]
DEFAULT_COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]


def _resolve_linestyle(index: int) -> str:
    return LINESTYLES[index % len(LINESTYLES)]


def plot_kinematic_sequence(
    ax: plt.Axes,
    data_by_start: Sequence[Tuple[StartConfig, pd.DataFrame]],
    time_column: str,
    variables: Sequence[PlotVariable],
    show_grid: bool = True,
) -> None:
    """Plot kinematic sequence lines for each variable across starts."""

    color_cycle = cycle(DEFAULT_COLORS)
    for var_idx, variable in enumerate(variables):
        color = variable.color or next(color_cycle)
        for start_idx, (start, frame) in enumerate(data_by_start):
            linestyle = _resolve_linestyle(start_idx)
            label = f"{variable.label} ({start.label})"
            ax.plot(
                frame[time_column],
                frame[variable.column],
                label=label,
                color=color,
                linestyle=linestyle,
                linewidth=2,
            )

    ax.set_xlabel("Pitch Phase (%)")
    ax.set_ylabel("Angle / Position")
    ax.set_title("Kinematic Sequence")
    if show_grid:
        ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.7)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0.0)


def plot_velocity_overlay(
    ax: plt.Axes,
    data_by_start: Sequence[Tuple[StartConfig, pd.DataFrame]],
    time_column: str,
    variable: PlotVariable,
    show_grid: bool = True,
) -> None:
    """Plot a hand (or ball) velocity overlay for each start."""

    for start_idx, (start, frame) in enumerate(data_by_start):
        linestyle = _resolve_linestyle(start_idx)
        color = start.color or DEFAULT_COLORS[start_idx % len(DEFAULT_COLORS)]
        ax.plot(
            frame[time_column],
            frame[variable.column],
            label=start.label,
            color=color,
            linestyle=linestyle,
            linewidth=2,
        )

    ax.set_xlabel("Pitch Phase (%)")
    ax.set_ylabel(variable.label)
    ax.set_title(variable.label)
    if show_grid:
        ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.7)
    ax.legend(loc="upper left")


def annotate_points_of_interest(
    ax: plt.Axes,
    data_by_start: Sequence[Tuple[StartConfig, pd.DataFrame]],
    time_column: str,
    event_column: str,
    events: dict,
) -> None:
    """Annotate vertical lines for key pitching events."""

    ymin, ymax = ax.get_ylim()
    for code, label in events.items():
        for start_idx, (start, frame) in enumerate(data_by_start):
            matches = frame.loc[frame[event_column] == code, time_column]
            if matches.empty:
                continue
            xpos = matches.iloc[0]
            linestyle = _resolve_linestyle(start_idx)
            ax.axvline(
                xpos,
                color="black",
                linestyle=linestyle,
                linewidth=1,
                alpha=0.6,
            )
            ax.text(
                xpos,
                ymax,
                f" {label}\n({start.label})",
                rotation=90,
                verticalalignment="bottom",
                fontsize=8,
                color="black",
            )


def render_summary_table(
    ax: plt.Axes,
    summary_rows: List[List[str]],
    column_labels: Iterable[str],
) -> None:
    """Render a summary table on the provided axes."""

    ax.axis("off")
    table = ax.table(
        cellText=summary_rows,
        colLabels=list(column_labels),
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.2)
