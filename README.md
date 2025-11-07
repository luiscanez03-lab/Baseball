# Kansas City Royals - Baseball Pitching Report

This repository bundles everything you need to generate a **multi-start pitching report** for the Kansas City Royals organization. It includes:

- A reusable Python package (`src/pitching_report`) for assembling the report
- A command-line script for triggering report generation
- Sample configuration and example data for two starts
- Documentation describing the data schema (`data_dictionary.md`)

The final deliverable is a PDF report that overlays kinematic trends from two outings, annotates key delivery events, and summarizes peak metrics.

## 📁 Repository Structure

```
Baseball/
├── config/
│   └── report_config.yaml         # YAML configuration that drives the report
├── data/
│   ├── pitcher001_start1.csv      # Sample start #1 data (time-normalized)
│   └── pitcher001_start2.csv      # Sample start #2 data (time-normalized)
├── data_dictionary.md             # Column-level documentation for the datasets
├── reports/
│   └── .gitkeep                   # Placeholder so the output folder is tracked
├── requirements.txt               # Python dependencies required to run the pipeline
├── scripts/
│   └── generate_pitching_report.py# CLI entry point for report generation
├── src/
│   └── pitching_report/           # Core package housing plotting + orchestration code
│       ├── __init__.py
│       ├── data_models.py
│       ├── io.py
│       ├── plotting.py
│       └── report_builder.py
└── README.md
```

## 🚀 Quick Start

1. **Create & activate a virtual environment (optional but recommended).**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

2. **Install dependencies.**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the report.**
   ```bash
   PYTHONPATH=src python scripts/generate_pitching_report.py --config config/report_config.yaml
   ```
   The command above will export `reports/pitcher001_pitching_report.pdf` using the sample data provided. Override `--config` if you create additional configuration files.

## 🧩 Customizing the Report

- **Data inputs:** Drop your CSV exports (one per start) into the `data/` folder. Make sure they share the same schema as defined in `data_dictionary.md`.
- **Configuration:** Duplicate `config/report_config.yaml` and adjust the paths, labels, and metrics. You can add or remove kinematic variables, point-of-interest markers, and summary metrics as needed.
- **Styling:** Edit `output` and plot sections within the YAML configuration to control figure size, colors, and which variables are visualized.

## 🧪 Testing the Pipeline

The `scripts/generate_pitching_report.py` CLI doubles as a smoke test. Running it with the default configuration should create a PDF without errors.

```bash
PYTHONPATH=src python scripts/generate_pitching_report.py
```

## 🛠️ Adding New Functionality

- To create additional pages, extend `pitching_report/report_builder.py` with new plotting layouts and append them to the `PdfPages` context.
- Encapsulate reusable matplotlib logic inside `pitching_report/plotting.py` to keep figures consistent across pages.
- When introducing new summary metrics, add them to the `summary_metrics` array in the YAML file.

## 📄 License

This project is provided for internal analytical use by the Kansas City Royals organization. Adapt and extend as required for your workflows.
