# Environmental Cybersecurity PM2.5 Pipeline

This repository contains a reproducible Python research pipeline for collecting
OpenAQ PM2.5 observations, running exploratory analysis, producing a cleaned
baseline dataset, simulating adversarial sensor-data attacks, and evaluating
anomaly detectors against attack ground truth.

The project is organized as stage-specific packages so each part of the
workflow can be run, tested, and documented independently.

## Workflow

```text
OpenAQ API
    -> fetch_country_pm25.py
    -> data/preprocessed/*.csv
    -> eda
    -> outputs/continental/combined_dataset.parquet or .csv
    -> preprocessing
    -> outputs/preprocessing/baseline_dataset.parquet or .csv
    -> attacks
    -> outputs/attacks/attacked_dataset.parquet or .csv
    -> outputs/attacks/ground_truth.csv
    -> detection
    -> outputs/detection/
```

## Repository Layout

| Path | Purpose |
| --- | --- |
| `fetch_country_pm25.py` | Collects country-level PM2.5 measurements from the OpenAQ v3 API with checkpointing and raw JSON preservation. |
| `run_eda.py` | Entry point for exploratory data analysis. |
| `run_attacks.py` | Entry point for attack simulation. |
| `run_detection.py` | Entry point for anomaly detection and detector comparison. |
| `eda/` | Country-level and continental exploratory analysis package. |
| `preprocessing/` | Dataset validation, cleaning, integrity checks, temporal features, quality scoring, and baseline export. |
| `attacks/` | Attack campaign generation, attack injection, ground-truth labels, attack analytics, and manifests. |
| `detection/` | Rolling z-score, Isolation Forest, and LSTM autoencoder anomaly detection with evaluation and comparison. |
| `tests/` | Root test package placeholder. Stage-specific tests live under each package. |
| `requirements.txt` | Pinned environment used for the research pipeline. |
| `pyproject.toml` | Package metadata and pytest configuration. |

Stage-level documentation:

- `eda/README.md`
- `preprocessing/README.md`
- `attacks/README.md`
- `detection/README.md`

## Requirements

- Python 3.10 or newer
- OpenAQ API key for data collection
- Python packages listed in `requirements.txt`

The detection stage includes TensorFlow/Keras for the LSTM autoencoder, plus
scikit-learn, scipy, and statsmodels for detector training and statistical
evaluation.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the repository root for OpenAQ collection:

```env
OPENAQ_API_KEY=your_api_key_here
```

## Running the Pipeline

### 1. Collect OpenAQ PM2.5 Data

```powershell
python fetch_country_pm25.py --country ET --start-date 2025-01-01 --end-date 2025-12-31
```

Generated collection artifacts:

```text
data/raw/openaq/
data/processed/
logs/country_pm25_fetch.log
```

Before running EDA, place or convert the country CSV files expected by
`eda/config.py` under:

```text
data/preprocessed/
```

### 2. Run EDA

```powershell
python run_eda.py
```

Main outputs:

```text
outputs/country_reports/
outputs/continental/combined_dataset.csv
outputs/continental/combined_dataset.parquet
outputs/continental/eda_execution_summary.json
```

### 3. Run Preprocessing

```powershell
python -m preprocessing.run_preprocessing
```

or:

```powershell
python preprocessing/run_preprocessing.py
```

Main outputs:

```text
outputs/preprocessing/baseline_dataset.csv
outputs/preprocessing/baseline_dataset.parquet
outputs/preprocessing/preprocessing_report.json
outputs/preprocessing/dataset_manifest.json
```

### 4. Simulate Attacks

```powershell
python run_attacks.py
```

Main outputs:

```text
outputs/attacks/attacked_dataset.csv
outputs/attacks/attacked_dataset.parquet
outputs/attacks/ground_truth.csv
outputs/attacks/campaign.csv
outputs/attacks/attack_report.json
outputs/attacks/attack_manifest.json
outputs/attacks/analytics/
```

Implemented attack types:

- Constant Bias
- Gradual Drift
- Spike Suppression
- Random Stealth

### 5. Run Detection

```powershell
python run_detection.py
```

Main outputs:

```text
outputs/detection/detector_comparison.csv
outputs/detection/pairwise_statistics.csv
outputs/detection/detection_manifest.json
outputs/detection/isolation_forest/
outputs/detection/rolling_z-score/
outputs/detection/lstm_autoencoder/
```

Implemented detectors:

- Rolling Z-Score
- Isolation Forest
- LSTM Autoencoder

## Generated and Ignored Files

The repository intentionally ignores local environments, private configuration,
large/generated data, plots, logs, research drafts, reference papers, and legacy
scripts. The ignored paths are configured in `.gitignore`.

Ignored project artifacts include:

```text
.env
.venv/
.tf_env/
.idea/
reference papers
draft papers
plots/
logs/
data/
data_results/
outputs/
env_cysec.egg-info/
legacy/
```

This keeps Git focused on source code, tests, and documentation. Data and
results should be regenerated from the pipeline or stored separately with the
research artifacts that require them.

## Tests

Run package-specific tests from the repository root:

```powershell
python -m pytest preprocessing/tests
python -m pytest attacks/tests
python -m pytest detection/tests
```

Run all configured tests:

```powershell
python -m pytest
```

## Reproducibility Notes

- Keep the exact input CSVs, date ranges, country codes, and OpenAQ query
  parameters with any paper or experiment output.
- Preserve generated manifests from `preprocessing`, `attacks`, and `detection`
  when comparing experimental runs.
- The `outputs/` directory is ignored because it contains regenerated research
  artifacts rather than source files.
- The `legacy/` directory is ignored and should be treated as archival code, not
  the active workflow.
