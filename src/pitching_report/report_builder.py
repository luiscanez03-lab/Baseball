"""High-level orchestration for building the pitching report."""
from __future__ import annotations

from typing import List, Sequence, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from .data_models import ReportConfig, StartConfig, SummaryMetric, reducer_from_string
from .io import ensure_output_directory, load_report_config, load_start_frame, validate_required_columns
from .plotting import (
    annotate_points_of_interest,
    plot_kinematic_sequence,
    plot_velocity_overlay,
    render_summary_table,
)

EVENT_COLUMN = "event"


def _collect_data(report_config: ReportConfig) -> List[Tuple[StartConfig, pd.DataFrame]]:
    """Load and validate each start specified in the configuration."""

    required_columns = {report_config.time_column, EVENT_COLUMN}
    required_columns.update(var.column for var in report_config.kinematic_variables)
    if report_config.velocity_variable:
        required_columns.add(report_config.velocity_variable.column)

    collected: List[Tuple[StartConfig, pd.DataFrame]] = []
    for start in report_config.starts:
        frame = load_start_frame(start)
        validate_required_columns(frame, required_columns, start.label)
        collected.append((start, frame))
    return collected


def _build_summary_rows(
    summary_metrics: Sequence[SummaryMetric],
    data_by_start: Sequence[Tuple[StartConfig, pd.DataFrame]],
) -> List[List[str]]:
    rows: List[List[str]] = []
    for metric in summary_metrics:
        reducer = reducer_from_string(metric.reducer)
        row = [metric.label]
        for _, frame in data_by_start:
            value = reducer(frame[metric.column])
            if value is None:
                row.append("-")
            else:
                row.append(f"{value:.{metric.precision}f}")
        rows.append(row)
    return rows


def _add_header(fig: plt.Figure, config: ReportConfig) -> None:
    """Add title, athlete metadata, and start details to the figure."""

    fig.suptitle(config.title, fontsize=18, fontweight="bold", y=0.97)
    athlete = config.athlete
    header_lines = [f"Athlete: {athlete.name}"]
    if athlete.throwing_hand:
        header_lines.append(f"Throws: {athlete.throwing_hand}")
    if athlete.organization:
        header_lines.append(f"Org: {athlete.organization}")
    for key, value in athlete.additional_details.items():
        header_lines.append(f"{key}: {value}")

    start_lines = []
    for start in config.starts:
        line = start.label
        if start.opponent:
            line += f" vs {start.opponent}"
        start_lines.append(line)

    fig.text(0.02, 0.91, " \n".join(header_lines), fontsize=10, va="top")
    fig.text(0.72, 0.91, "Starts:\n" + "\n".join(start_lines), fontsize=10, va="top")


def build_report(config: ReportConfig) -> None:
    """Generate the full pitching report and export it as a PDF."""

    data_by_start = _collect_data(config)
    ensure_output_directory(config.output_path)

    with PdfPages(config.output_path) as pdf:
        fig = plt.figure(figsize=config.visuals.figsize, dpi=config.visuals.dpi)
        fig.patch.set_facecolor(config.visuals.background_color)

        if config.velocity_variable:
            grid = fig.add_gridspec(
                2,
                2,
                height_ratios=[3.2, 1.5],
                width_ratios=[2.2, 1.0],
                hspace=0.35,
                wspace=0.35,
            )
            ax_seq = fig.add_subplot(grid[0, :])
            ax_velocity = fig.add_subplot(grid[1, 0])
            ax_table = fig.add_subplot(grid[1, 1])
        else:
            grid = fig.add_gridspec(2, 1, height_ratios=[3.2, 1.5], hspace=0.35)
            ax_seq = fig.add_subplot(grid[0, 0])
            ax_velocity = None
            ax_table = fig.add_subplot(grid[1, 0])

        _add_header(fig, config)

        plot_kinematic_sequence(
            ax_seq,
            data_by_start,
            config.time_column,
            config.kinematic_variables,
            show_grid=config.visuals.grid,
        )
        if config.points_of_interest:
            annotate_points_of_interest(
                ax_seq,
                data_by_start,
                config.time_column,
                EVENT_COLUMN,
                config.points_of_interest,
            )

        if config.velocity_variable and ax_velocity is not None:
            plot_velocity_overlay(
                ax_velocity,
                data_by_start,
                config.time_column,
                config.velocity_variable,
                show_grid=config.visuals.grid,
            )

        if config.summary_metrics:
            summary_rows = _build_summary_rows(config.summary_metrics, data_by_start)
            headers = ["Metric"] + [start.label for start, _ in data_by_start]
            render_summary_table(ax_table, summary_rows, headers)
        else:
            ax_table.axis("off")
            ax_table.text(0.5, 0.5, "No summary metrics configured.", ha="center", va="center", fontsize=10)

        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)


def build_report_from_file(config_path) -> None:
    """Convenience wrapper to load config from disk and build the report."""

    config = load_report_config(config_path)
    build_report(config)
