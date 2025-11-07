"""Input/output helpers for the pitching report pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Tuple

import pandas as pd
import yaml

from .data_models import (
    AthleteInfo,
    PlotVariable,
    ReportConfig,
    ReportVisualSettings,
    StartConfig,
    SummaryMetric,
)


def _coerce_plot_variable(item: Dict) -> PlotVariable:
    column = item.get("column") or item.get("variable")
    if not column:
        raise ValueError("Each plot variable must define a 'column' or 'variable' field.")
    label = item.get("label", column.replace("_", " ").title())
    color = item.get("color")
    return PlotVariable(column=column, label=label, color=color)


def _coerce_summary_metric(item: Dict) -> SummaryMetric:
    column = item.get("column")
    label = item.get("label", column.replace("_", " ").title())
    reducer = item.get("reducer", "max")
    precision = int(item.get("precision", 2))
    return SummaryMetric(label=label, column=column, reducer=reducer, precision=precision)


def _coerce_start(item: Dict) -> StartConfig:
    filepath = Path(item["filepath"])
    label = item.get("label", filepath.stem)
    opponent = item.get("opponent")
    color = item.get("color")
    return StartConfig(label=label, filepath=filepath, opponent=opponent, color=color)


def load_report_config(config_path: Path) -> ReportConfig:
    """Load a :class:`ReportConfig` instance from a YAML file."""

    with open(config_path, "r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    athlete_raw = raw.get("athlete", {})
    athlete = AthleteInfo(
        name=athlete_raw.get("name", "Unknown Pitcher"),
        throwing_hand=athlete_raw.get("throwing_hand"),
        organization=athlete_raw.get("organization"),
        additional_details={k: v for k, v in athlete_raw.get("extra", {}).items()},
    )

    starts = tuple(_coerce_start(item) for item in raw.get("starts", []))
    if not starts:
        raise ValueError("At least one start must be defined in the configuration.")

    plot_section = raw.get("plots", {})
    time_column = plot_section.get("time_column", "phase_pct")

    kinematic_section = plot_section.get("kinematic_sequence", {})
    kinematic_variables = tuple(
        _coerce_plot_variable(item) for item in kinematic_section.get("variables", [])
    )
    if not kinematic_variables:
        raise ValueError("The configuration must define at least one kinematic sequence variable.")

    velocity_section = plot_section.get("velocity_overlay", {})
    velocity_variable = None
    if velocity_section:
        velocity_variable = _coerce_plot_variable(velocity_section)

    poi = raw.get("points_of_interest", {}).get("events", {})
    summary_metrics = tuple(_coerce_summary_metric(item) for item in raw.get("summary_metrics", []))

    output_section = raw.get("output", {})
    output_path = Path(output_section.get("path", "reports/pitching_report.pdf"))
    dpi = int(output_section.get("dpi", 150))
    figsize_data = output_section.get("figsize", [11, 8.5])
    if not isinstance(figsize_data, (list, tuple)) or len(figsize_data) != 2:
        raise ValueError("Output figsize must be a list or tuple of two floats.")
    figsize = (float(figsize_data[0]), float(figsize_data[1]))
    background_color = output_section.get("background_color", "white")
    grid = bool(output_section.get("grid", True))
    visuals = ReportVisualSettings(
        figsize=figsize,
        dpi=dpi,
        background_color=background_color,
        grid=grid,
    )

    return ReportConfig(
        title=raw.get("title", "Kansas City Royals - Baseball Pitching Report"),
        athlete=athlete,
        starts=starts,
        time_column=time_column,
        kinematic_variables=kinematic_variables,
        velocity_variable=velocity_variable,
        points_of_interest=poi,
        summary_metrics=summary_metrics,
        output_path=output_path,
        visuals=visuals,
    )


def load_start_frame(start: StartConfig) -> pd.DataFrame:
    """Load the CSV data for a pitching start into a DataFrame."""

    frame = pd.read_csv(start.filepath)
    frame["start_label"] = start.label
    if start.opponent:
        frame["opponent"] = start.opponent
    return frame


def validate_required_columns(frame: pd.DataFrame, columns: Iterable[str], start_label: str) -> None:
    missing = [col for col in columns if col not in frame.columns]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Missing columns for {start_label}: {joined}")


def ensure_output_directory(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
