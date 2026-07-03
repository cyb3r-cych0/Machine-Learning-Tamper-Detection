# Plots

The `plots` package generates publication-oriented figures from the attack and
detection outputs produced by the research pipeline. It reads detector metrics,
attack recall summaries, confidence intervals, statistical comparisons, and
attack campaign summaries, then exports each figure in multiple formats.

## Pipeline

```text
outputs/detection/
outputs/attacks/
    -> load_metrics and load_statistics
    -> generate detector, recall, confidence interval, significance, campaign,
       confusion matrix, and workflow figures
    -> save figures to plots/output/
```

The main entry point from the repository root is:

```powershell
python run_plots.py
```

Programmatic use:

```python
from plots.manager import run

run()
```

At present, `manager.py` only calls `workflow_diagram()` by default. The other
figure calls are present but commented out, so enable them in `manager.py` when
the required detection and attack artifacts are available.

## Inputs

Configured in `config.py`:

```text
outputs/detection/
outputs/attacks/
```

The plotting modules currently expect JSON-formatted artifacts, including:

```text
outputs/detection/detector_comparison.json
outputs/detection/pairwise_statistics.json
outputs/detection/isolation_forest/metrics_isolation_forest.json
outputs/detection/isolation_forest/confidence_intervals_isolation_forest.json
outputs/detection/isolation_forest/attack_recall_isolation_forest.json
outputs/detection/isolation_forest/country_recall_isolation_forest.json
outputs/detection/rolling_z-score/metrics_rolling_zscore.json
outputs/detection/rolling_z-score/confidence_intervals_rolling_zscore.json
outputs/detection/rolling_z-score/attack_recall_rolling_zscore.json
outputs/detection/rolling_z-score/country_recall_rolling_zscore.json
outputs/detection/lstm_autoencoder/metrics_lstm_autoencoder.json
outputs/detection/lstm_autoencoder/confidence_intervals_lstm_autoencoder.json
outputs/detection/lstm_autoencoder/attack_recall_lstm_autoencoder.json
outputs/detection/lstm_autoencoder/country_recall_lstm_autoencoder.json
outputs/attacks/attack_report.json
outputs/attacks/attack_manifest.json
outputs/attacks/campaign.json
```

The `workflow_diagram` figure does not require pipeline output artifacts, but it
does require Graphviz to be installed and available to Python.

## Outputs

Figures are written under:

```text
plots/output/
```

Most matplotlib-based figures are exported as:

```text
png
pdf
svg
```

Generated figure names:

```text
Figure_3_DetectorComparison
Figure_4_AttackRecall
Figure_5_CountryHeatmap
Figure_6_ConfidenceIntervals
Figure_7_ConfusionMatrices
Figure_8_Significance
Figure_9_CampaignSummary
Figure_10_Framework
```

Run logs are written to:

```text
plots/output/logs/plots.log
```

## Modules

### `config.py`

Defines input directories, output directories, export formats, figure DPI,
default figure size, and font sizes.

### `loader.py`

Loads detector comparison metrics, pairwise statistics, attack reports, and
attack manifests from the configured output directories.

### `export.py`

Provides the shared `save_figure()` helper used by matplotlib-based plots. It
exports PNG, PDF, and SVG variants according to the flags in `config.py`.

### `detector_metrics.py`

Builds a grouped bar chart comparing detector accuracy, precision, recall, F1,
ROC AUC, PR AUC, and false-positive rate.

Output base name:

```text
Figure_3_DetectorComparison
```

### `attack_recall.py`

Builds a grouped bar chart of detector recall by attack type.

Output base name:

```text
Figure_4_AttackRecall
```

### `country_heatmap.py`

Builds a heatmap of country-wise recall across the supported detectors.

Output base name:

```text
Figure_5_CountryHeatmap
```

### `confidence_intervals.py`

Builds bootstrap confidence interval panels for F1, recall, and ROC AUC.

Output base name:

```text
Figure_6_ConfidenceIntervals
```

### `confusion_matrix.py`

Builds normalized confusion matrix panels for Isolation Forest, Rolling
Z-Score, and LSTM Autoencoder.

Output base name:

```text
Figure_7_ConfusionMatrices
```

### `significance.py`

Builds pairwise statistical significance heatmaps for McNemar and Wilcoxon
p-values.

Output base name:

```text
Figure_8_Significance
```

### `campaign_summary.py`

Builds a three-panel attack campaign summary showing attack type distribution,
attack coverage, and campaign distribution by country.

Output base name:

```text
Figure_9_CampaignSummary
```

### `workflow_diagram.py`

Builds the research framework diagram using Graphviz.

Output base name:

```text
Figure_10_Framework
```

### `logger.py`

Configures console and file logging for plot generation.

### `manager.py`

Sets up logging and dispatches figure generation.

## Package Layout

```text
plots/
    __init__.py
    attack_recall.py
    campaign_summary.py
    confidence_intervals.py
    config.py
    confusion_matrix.py
    country_heatmap.py
    detector_metrics.py
    export.py
    loader.py
    logger.py
    manager.py
    significance.py
    workflow_diagram.py
```
