### Proposed Pipeline
```
EnvironmentalCybersecurity/

│
├── data/
│   ├── raw/
│   │   ├── kenya.csv
│   │   ├── uganda.csv
│   │   ├── zambia.csv
│   │   ├── ...
│   │
│   └── processed/
│
├── outputs/
│
│   ├── country_reports/
│   │
│   │   ├── Kenya/
│   │   │      summary.csv
│   │   │      metadata.json
│   │   │      plots/
│   │   │
│   │   ├── Uganda/
│   │   │
│   │   └── ...
│   │
│   └── continental/
│        country_summary.csv
│        combined_dataset.csv
│        comparison_plots/
│
├── preprocessing/
│
├── attacks/
│
├── models/
│
└── evaluation/
```

## EDA Workflow
```aiignore
Raw CSVs

      │
      ▼

Locate every CSV

      │
      ▼

For each country

      │
      ├── Load
      ├── Validate
      ├── Clean
      ├── Feature Engineering
      ├── Country Statistics
      ├── Country Plots
      └── Save Report

      │
      ▼

Merge country summaries

      │
      ▼

Cross-country Analysis

      │
      ▼

Generate Combined Dataset

      │
      ▼

Attack Simulation
```

### Project Structure
```aiignore
project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── outputs/
│   ├── country_reports/
│   └── continental/
│
├── eda/
│   ├── __init__.py
│   ├── config.py
│   ├── loader.py
│   ├── validator.py
│   ├── features.py
│   ├── statistics.py
│   ├── plotting.py
│   ├── report.py
│   └── pipeline.py
│
└── run_eda.py
```
