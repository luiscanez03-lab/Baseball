"""Data models used throughout the pitching report pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


@dataclass(slots=True)
class StartConfig:
    """Configuration metadata for a single pitching start."""

    label: str
    filepath: Path
    opponent: Optional[str] = None
    color: Optional[str] = None


@dataclass(slots=True)
class AthleteInfo:
    """Information about the athlete used in the report header."""

    name: str
    throwing_hand: Optional[str] = None
    organization: Optional[str] = None
    additional_details: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class SummaryMetric:
    """Defines how to aggregate a metric for each start."""

    label: str
    column: str
    reducer: str = "max"
    precision: int = 2


@dataclass(slots=True)
class PlotVariable:
    """Metadata describing a variable that will be plotted."""

    column: str
    label: str
    color: Optional[str] = None


@dataclass(slots=True)
class ReportVisualSettings:
    """Styling information shared by all report pages."""

    figsize: Tuple[float, float] = (11.0, 8.5)
    dpi: int = 150
    background_color: str = "white"
    grid: bool = True


@dataclass(slots=True)
class ReportConfig:
    """Container for all configuration that drives the report."""

    title: str
    athlete: AthleteInfo
    starts: Sequence[StartConfig]
    time_column: str
    kinematic_variables: Sequence[PlotVariable]
    velocity_variable: Optional[PlotVariable]
    points_of_interest: Dict[str, str]
    summary_metrics: Sequence[SummaryMetric]
    output_path: Path
    visuals: ReportVisualSettings = ReportVisualSettings()


def reducer_from_string(name: str):
    """Return a reducer callable based on a string identifier."""

    name = name.lower()
    if name == "max":
        return lambda series: series.max()
    if name == "min":
        return lambda series: series.min()
    if name in {"mean", "avg", "average"}:
        return lambda series: series.mean()
    if name == "median":
        return lambda series: series.median()
    raise ValueError(f"Unsupported reducer: {name}")
