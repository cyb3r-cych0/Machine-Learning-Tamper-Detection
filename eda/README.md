## EDA v1.0
```aiignore
EDA
├── Data Discovery
├── Validation
├── Feature Engineering
├── Statistics
├── Country Reports
├── Country Plots
├── Continental Reports
├── Continental Plots
└── Combined Dataset
```

### Architecture
```aiignore
eda/

    __init__.py

    config.py

    loader.py

    validator.py

    features.py

    statistics.py

    report.py

    manager.py

    pipeline.py

    plotting/

        __init__.py

        utils.py

        country.py

        continental.py
```

### Idea
```aiignore
run_eda.py

↓

manager.run()
```