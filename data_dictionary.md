## 📘 Data Dictionary

This document describes the structure of the dataset used for the **Baseball Pitching Analysis** project.  
Each file in the `data/` folder represents motion capture data for a single pitching session.  
The dataset includes time-normalized kinematic variables and event markers used to analyze mechanical efficiency, timing, and sequencing throughout the delivery.

---

### 🧾 Column Definitions

| Column Name | Data Type | Description |
|--------------|------------|-------------|
| **pitch_id** | `int64` | Unique identifier assigned to each pitch. Used to distinguish between multiple pitches in a session. |
| **event** | `string` | Describes the key event occurring at that frame (e.g., “foot_contact”, “max_external_rotation”, “ball_release”). Useful for aligning kinematic phases. |
| **time_from_max_hand** | `float64` | Time in seconds relative to the moment of maximum hand velocity (`0`). Negative values represent frames before that moment; positive values represent frames after. |
| **index** | `int64` | Frame number or sequential index from motion capture export. Useful for verifying temporal order and plotting data chronologically. |
| **pitch_type** | `string` | Label for the pitch type (e.g., “fastball”, “slider”, “changeup”). Used for comparing different pitch styles. |

---

### 🧠 Mapping to Report Sections

| Report Section | Related Columns | Notes |
|----------------|-----------------|-------|
| **Kinematic Sequence** | `time_from_max_hand`, `event` | Serves as a time base for angular velocity or joint rotation plots to evaluate mechanical sequencing. |
| **Points of Interest (POI)** | `event` | Used to identify stride foot contact (SFC), max external rotation (MER), and ball release (BR). |
| **Pitch Comparison** | `pitch_id`, `pitch_type` | Enables comparison of timing and mechanics between different pitch types or trials. |
