# Data Directory

This directory stores datasets, models, logs, and calibration data.

**Note:** Large files are NOT stored in Git. Use DVC or Git LFS.

## Structure

```
data/
├── demonstrations/     # Raw demonstration recordings
│   ├── phase1_lerobot/
│   ├── phase5_training/
│   └── online_learning/
├── datasets/           # Processed datasets
│   ├── train/
│   ├── val/
│   └── test/
├── models/             # Trained models
│   ├── checkpoints/
│   ├── best_models/
│   ├── tensorrt/
│   └── deployed/
├── logs/               # System logs
│   ├── training/
│   ├── deployment/
│   ├── system/
│   └── safety/
├── calibration/        # Calibration data
│   ├── cameras/
│   ├── robot/
│   └── sensors/
└── experiments/        # Experiment results
```

## Data Management

Use DVC for version control of large data files:

```bash
# Track new data
dvc add data/demonstrations/new_task/

# Push to remote storage
dvc push

# Pull data
dvc pull
```
