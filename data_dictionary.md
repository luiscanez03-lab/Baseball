## 📘 Data Dictionary

This document describes the structure of the dataset used for the **Baseball Pitching Analysis** project. Each file in the `data/` folder represents time-normalized kinematic data for a single pitching start.

### 🧾 Column Definitions

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `pitch_id` | `int64` | Identifier for the pitch attempt associated with each row. |
| `phase_pct` | `float64` | Normalized delivery phase expressed as a percentage (0 = start of motion, 100 = follow-through). |
| `pelvis_rotation_deg` | `float64` | Pelvis rotation angle in degrees. |
| `torso_rotation_deg` | `float64` | Upper trunk rotation angle in degrees. |
| `lead_knee_extension_deg` | `float64` | Lead knee extension angle in degrees. |
| `shoulder_external_rotation_deg` | `float64` | Throwing shoulder external rotation angle in degrees. |
| `hand_velocity_mph` | `float64` | Hand velocity relative to the mound in miles per hour. |
| `event` | `string` | Event marker describing the delivery milestone (e.g., `SFC`, `MER`, `BR`). Empty strings denote frames without a tagged event. |
| `start_label` | `string` | (Added during processing) Indicates which start the row originated from. |
| `opponent` | `string` | (Optional) Opponent label passed through from the configuration. |

### 🧠 Mapping to Report Sections

| Report Section | Related Columns | Notes |
|----------------|-----------------|-------|
| Kinematic Sequence | `phase_pct`, each `*_deg` column | Plots overlay angular data for both starts. |
| Velocity Overlay | `phase_pct`, `hand_velocity_mph` | Shows hand-speed trends through the delivery. |
| Points of Interest | `event` | Used to draw vertical markers for `SFC`, `MER`, and `BR`. |
| Summary Metrics | `hand_velocity_mph`, `shoulder_external_rotation_deg`, `lead_knee_extension_deg` | Aggregated via reducers defined in `config/report_config.yaml`. |
