# GitHub Repository Structure Proposal
## Kuka Robot Arm AI-Driven Controller Replacement Project

**Document Version:** 1.0  
**Date:** December 14, 2025  
**Project Phase:** Planning & Documentation  
**Document Type:** Repository Organization and Collaboration Guidelines

---

## Table of Contents

1. [Overview and Philosophy](#1-overview-and-philosophy)
2. [Complete Directory Structure](#2-complete-directory-structure)
3. [Directory Descriptions and Rationale](#3-directory-descriptions-and-rationale)
4. [Main Repository README](#4-main-repository-readme)
5. [Subdirectory README Templates](#5-subdirectory-readme-templates)
6. [File Naming Conventions](#6-file-naming-conventions)
7. [Documentation Hierarchy](#7-documentation-hierarchy)
8. [Version Control Strategy](#8-version-control-strategy)
9. [Collaboration Guidelines](#9-collaboration-guidelines)
10. [Large File Management](#10-large-file-management)
11. [CI/CD Integration](#11-cicd-integration)
12. [Example Workflows](#12-example-workflows)

---

## 1. Overview and Philosophy

### 1.1 Repository Organization Philosophy

This repository structure is designed to support a **48-week, 7-phase project** involving multiple disciplines:
- **ML Engineers** - Developing and training neural network models
- **Control Engineers** - Implementing real-time control systems
- **Hardware Technicians** - Installing and configuring physical components
- **Safety Officers** - Ensuring compliance and safety validation
- **Integration Engineers** - Coordinating system-wide testing

**Core Principles:**

1. **Separation of Concerns** - Clear boundaries between ML, control, hardware, and safety code
2. **Phase-Based Organization** - Structure supports incremental development across 7 phases
3. **Multi-Disciplinary Collaboration** - Easy navigation for team members with different expertise
4. **Documentation-First** - Comprehensive documentation at every level
5. **Safety-Critical Design** - Special attention to safety-related code and documentation
6. **Reproducibility** - All experiments, tests, and deployments are reproducible
7. **Scalability** - Structure accommodates growth from proof-of-concept to production

### 1.2 Project Context

**System Overview:**
- Replace Kuka KR C2 controller with NVIDIA Jetson Orin Nano Super
- 6 servo drives (480V AC, 7.5kW each) with EtherCAT communication
- Multi-modal sensing (3-5 cameras, force/torque, encoders)
- ML-based autonomous control + G-code compatibility
- ISO 13849-1 Category 3 safety compliance

**Key Technical Requirements:**
- Real-time control at 1kHz
- ML inference at 100Hz with <10ms latency
- Safety response time <50ms
- Position accuracy ±0.05mm
- 48-week development timeline

---

## 2. Complete Directory Structure

```
kuka-ml-controller/
├── .github/                          # GitHub-specific configuration
│   ├── workflows/                    # CI/CD workflows
│   │   ├── tests.yml                # Automated testing
│   │   ├── lint.yml                 # Code quality checks
│   │   ├── docs.yml                 # Documentation builds
│   │   └── deploy.yml               # Deployment automation
│   ├── ISSUE_TEMPLATE/              # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   ├── safety_issue.md          # Critical safety issues
│   │   └── hardware_issue.md
│   ├── PULL_REQUEST_TEMPLATE.md     # PR template
│   └── CODEOWNERS                   # Code ownership rules
│
├── docs/                            # Comprehensive documentation
│   ├── README.md                    # Documentation index
│   ├── project/                     # Project-level documentation
│   │   ├── project_analysis.md      # From analysis phase
│   │   ├── requirements.md          # System requirements
│   │   ├── architecture.md          # System architecture
│   │   ├── roadmap.md              # 7-phase roadmap
│   │   └── budget.md               # Budget and resources
│   ├── technical/                   # Technical specifications
│   │   ├── hardware/
│   │   │   ├── electrical_specs.md
│   │   │   ├── mechanical_specs.md
│   │   │   ├── network_topology.md
│   │   │   └── sensor_specs.md
│   │   ├── software/
│   │   │   ├── control_architecture.md
│   │   │   ├── ml_architecture.md
│   │   │   ├── safety_architecture.md
│   │   │   └── communication_protocols.md
│   │   └── integration/
│   │       ├── system_integration.md
│   │       └── interface_specifications.md
│   ├── api/                         # API documentation
│   │   ├── control_api.md
│   │   ├── ml_api.md
│   │   ├── hardware_api.md
│   │   └── safety_api.md
│   ├── guides/                      # User and developer guides
│   │   ├── developer/
│   │   │   ├── setup_guide.md
│   │   │   ├── coding_standards.md
│   │   │   ├── testing_guide.md
│   │   │   └── deployment_guide.md
│   │   ├── operator/
│   │   │   ├── operation_manual.md
│   │   │   ├── safety_procedures.md
│   │   │   └── troubleshooting.md
│   │   └── maintenance/
│   │       ├── maintenance_schedule.md
│   │       ├── calibration_procedures.md
│   │       └── spare_parts.md
│   ├── safety/                      # Safety documentation
│   │   ├── risk_assessment.md
│   │   ├── safety_validation.md
│   │   ├── compliance_report.md
│   │   ├── loto_procedures.md
│   │   └── emergency_procedures.md
│   ├── diagrams/                    # System diagrams
│   │   ├── architecture/
│   │   ├── electrical/
│   │   ├── mechanical/
│   │   ├── network/
│   │   └── dataflow/
│   └── tutorials/                   # Step-by-step tutorials
│       ├── 01_environment_setup.md
│       ├── 02_data_collection.md
│       ├── 03_model_training.md
│       ├── 04_deployment.md
│       └── 05_testing.md
│
├── src/                             # Source code
│   ├── __init__.py
│   ├── control/                     # Real-time control system
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── realtime_controller.py   # Main control loop
│   │   ├── kinematics.py           # Forward/inverse kinematics
│   │   ├── trajectory_planner.py   # Path planning
│   │   ├── pid_controller.py       # PID control loops
│   │   ├── gcode_interpreter.py    # G-code parser
│   │   ├── mode_manager.py         # Mode switching (ML/G-code/Manual)
│   │   └── feedforward.py          # Feedforward compensation
│   ├── hardware/                    # Hardware interfaces
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── ethercat_master.py      # EtherCAT communication
│   │   ├── drive_interface.py      # Motor drive control
│   │   ├── gpio_interface.py       # GPIO for safety signals
│   │   ├── encoder_interface.py    # Encoder reading
│   │   └── io_module.py           # Digital/analog I/O
│   ├── sensors/                     # Sensor interfaces
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── camera_manager.py       # Multi-camera management
│   │   ├── force_torque_sensor.py  # F/T sensor interface
│   │   ├── temperature_sensor.py   # Temperature monitoring
│   │   └── calibration.py          # Sensor calibration
│   ├── models/                      # ML models
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── base_model.py           # Base model class
│   │   ├── behavioral_cloning.py   # BC model
│   │   ├── act_model.py            # Action Chunking Transformer
│   │   ├── diffusion_policy.py     # Diffusion-based policy
│   │   ├── vision_encoder.py       # Vision feature extraction
│   │   └── online_learning.py      # Online learning framework
│   ├── data/                        # Data handling
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── dataset_manager.py      # Dataset storage/retrieval
│   │   ├── preprocessing.py        # Data preprocessing
│   │   ├── augmentation.py         # Data augmentation
│   │   ├── dataloader.py          # PyTorch dataloaders
│   │   └── visualization.py        # Data visualization
│   ├── training/                    # Training pipeline
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── trainer.py              # Training loop
│   │   ├── evaluator.py           # Model evaluation
│   │   ├── callbacks.py           # Training callbacks
│   │   └── metrics.py             # Performance metrics
│   ├── deployment/                  # Deployment tools
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── tensorrt_converter.py   # TensorRT optimization
│   │   ├── model_server.py         # Model serving
│   │   ├── hot_swap.py            # Model hot-swapping
│   │   └── benchmarking.py        # Performance benchmarking
│   ├── safety/                      # Safety systems
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── safety_monitor.py       # Safety validation
│   │   ├── collision_checker.py    # Collision detection
│   │   ├── limit_checker.py        # Joint/velocity limits
│   │   ├── watchdog.py            # Hardware watchdog
│   │   └── emergency_stop.py      # E-stop handling
│   ├── teleoperation/              # Teleoperation for data collection
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── teleop_controller.py    # Main teleop controller
│   │   ├── input_devices.py        # Device interfaces
│   │   └── recording.py           # Demonstration recording
│   ├── simulation/                  # Simulation environment
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── robot_sim.py           # Robot simulation
│   │   ├── physics_engine.py      # Physics simulation
│   │   └── domain_randomization.py # Sim-to-real transfer
│   └── utils/                       # Utility functions
│       ├── __init__.py
│       ├── README.md
│       ├── config.py               # Configuration management
│       ├── logging.py              # Logging utilities
│       ├── transforms.py           # Coordinate transforms
│       ├── math_utils.py          # Mathematical utilities
│       └── visualization.py        # Visualization tools
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── README.md
│   ├── conftest.py                 # Pytest configuration
│   ├── unit/                       # Unit tests
│   │   ├── test_kinematics.py
│   │   ├── test_safety.py
│   │   ├── test_models.py
│   │   ├── test_preprocessing.py
│   │   └── test_utils.py
│   ├── integration/                # Integration tests
│   │   ├── test_control_system.py
│   │   ├── test_ml_pipeline.py
│   │   ├── test_hardware_interface.py
│   │   └── test_safety_system.py
│   ├── hardware/                   # Hardware-in-the-loop tests
│   │   ├── test_single_axis.py
│   │   ├── test_multi_axis.py
│   │   ├── test_sensors.py
│   │   └── test_ethercat.py
│   ├── performance/                # Performance benchmarks
│   │   ├── benchmark_inference.py
│   │   ├── benchmark_control_loop.py
│   │   └── benchmark_network.py
│   └── fixtures/                   # Test fixtures and data
│       ├── sample_trajectories.py
│       ├── mock_hardware.py
│       └── test_data/
│
├── scripts/                         # Utility scripts
│   ├── README.md
│   ├── setup/                      # Setup scripts
│   │   ├── install_dependencies.sh
│   │   ├── configure_jetson.sh
│   │   ├── setup_ethercat.sh
│   │   └── install_tensorrt.sh
│   ├── data/                       # Data management scripts
│   │   ├── collect_demonstrations.py
│   │   ├── process_dataset.py
│   │   ├── split_dataset.py
│   │   └── export_dataset.py
│   ├── training/                   # Training scripts
│   │   ├── train_bc.py
│   │   ├── train_act.py
│   │   ├── train_diffusion.py
│   │   └── evaluate_model.py
│   ├── deployment/                 # Deployment scripts
│   │   ├── convert_to_tensorrt.py
│   │   ├── deploy_model.py
│   │   ├── benchmark_model.py
│   │   └── hot_swap_model.py
│   ├── calibration/                # Calibration scripts
│   │   ├── calibrate_cameras.py
│   │   ├── calibrate_robot.py
│   │   ├── calibrate_force_sensor.py
│   │   └── home_axes.py
│   ├── testing/                    # Testing scripts
│   │   ├── run_all_tests.sh
│   │   ├── test_single_axis.py
│   │   ├── test_safety_system.py
│   │   └── measure_performance.py
│   └── maintenance/                # Maintenance scripts
│       ├── backup_system.sh
│       ├── update_firmware.py
│       └── generate_report.py
│
├── config/                          # Configuration files
│   ├── README.md
│   ├── robot/                      # Robot configuration
│   │   ├── kuka_kr150.yaml         # KR150 parameters
│   │   ├── kuka_kr180.yaml         # KR180 parameters
│   │   ├── kuka_kr210.yaml         # KR210 parameters
│   │   └── joint_limits.yaml       # Joint limits
│   ├── hardware/                   # Hardware configuration
│   │   ├── ethercat_network.yaml   # Network topology
│   │   ├── drives.yaml             # Drive parameters
│   │   ├── sensors.yaml            # Sensor configuration
│   │   └── io_mapping.yaml         # I/O assignments
│   ├── control/                    # Control configuration
│   │   ├── pid_gains.yaml          # PID parameters
│   │   ├── trajectory_limits.yaml  # Velocity/acceleration limits
│   │   └── feedforward.yaml        # Feedforward parameters
│   ├── safety/                     # Safety configuration
│   │   ├── safety_limits.yaml      # Safety thresholds
│   │   ├── collision_zones.yaml    # Collision boundaries
│   │   └── emergency_config.yaml   # E-stop configuration
│   ├── ml/                         # ML configuration
│   │   ├── bc_config.yaml          # Behavioral cloning
│   │   ├── act_config.yaml         # ACT model
│   │   ├── diffusion_config.yaml   # Diffusion policy
│   │   └── training_config.yaml    # Training parameters
│   ├── cameras/                    # Camera configuration
│   │   ├── camera_intrinsics.yaml  # Calibration data
│   │   ├── camera_extrinsics.yaml  # Camera poses
│   │   └── camera_settings.yaml    # Exposure, gain, etc.
│   └── deployment/                 # Deployment configuration
│       ├── jetson_config.yaml      # Jetson settings
│       ├── tensorrt_config.yaml    # TensorRT optimization
│       └── logging_config.yaml     # Logging settings
│
├── data/                            # Data storage (gitignored, use LFS/DVC)
│   ├── README.md
│   ├── .gitkeep
│   ├── demonstrations/             # Collected demonstrations
│   │   ├── phase1_lerobot/        # Phase 1 PoC data
│   │   ├── phase5_training/       # Phase 5 training data
│   │   └── online_learning/       # Continuous learning data
│   ├── datasets/                   # Processed datasets
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   ├── models/                     # Trained models
│   │   ├── checkpoints/           # Training checkpoints
│   │   ├── best_models/           # Best performing models
│   │   ├── tensorrt/              # TensorRT optimized models
│   │   └── deployed/              # Currently deployed models
│   ├── logs/                       # System logs
│   │   ├── training/              # Training logs
│   │   ├── deployment/            # Deployment logs
│   │   ├── system/                # System operation logs
│   │   └── safety/                # Safety event logs
│   ├── calibration/                # Calibration data
│   │   ├── cameras/
│   │   ├── robot/
│   │   └── sensors/
│   └── experiments/                # Experiment results
│       ├── phase1_poc/
│       ├── phase5_ml/
│       └── phase6_integration/
│
├── hardware/                        # Hardware documentation and files
│   ├── README.md
│   ├── electrical/                 # Electrical documentation
│   │   ├── schematics/            # Circuit diagrams
│   │   │   ├── power_distribution.pdf
│   │   │   ├── control_circuits.pdf
│   │   │   ├── safety_circuits.pdf
│   │   │   └── io_wiring.pdf
│   │   ├── wiring_diagrams/       # Wiring diagrams
│   │   │   ├── ethercat_network.pdf
│   │   │   ├── motor_connections.pdf
│   │   │   └── sensor_wiring.pdf
│   │   ├── panel_layouts/         # Control panel layouts
│   │   ├── cable_schedules/       # Cable lists and routing
│   │   └── as_built/              # As-built documentation
│   ├── mechanical/                 # Mechanical documentation
│   │   ├── cad/                   # CAD files
│   │   │   ├── robot_model.step
│   │   │   ├── mounting_brackets.step
│   │   │   └── sensor_mounts.step
│   │   ├── drawings/              # Engineering drawings
│   │   ├── assembly/              # Assembly instructions
│   │   └── bom/                   # Bill of materials
│   ├── datasheets/                 # Component datasheets
│   │   ├── drives/
│   │   ├── sensors/
│   │   ├── controllers/
│   │   └── safety_components/
│   ├── firmware/                   # Firmware files
│   │   ├── drives/
│   │   ├── io_modules/
│   │   └── safety_relay/
│   └── specifications/             # Hardware specifications
│       ├── system_requirements.md
│       ├── component_selection.md
│       └── interface_specs.md
│
├── notebooks/                       # Jupyter notebooks
│   ├── README.md
│   ├── exploration/                # Data exploration
│   │   ├── 01_dataset_analysis.ipynb
│   │   ├── 02_trajectory_visualization.ipynb
│   │   └── 03_sensor_data_analysis.ipynb
│   ├── experiments/                # Experimental notebooks
│   │   ├── model_comparison.ipynb
│   │   ├── hyperparameter_tuning.ipynb
│   │   └── ablation_studies.ipynb
│   ├── visualization/              # Visualization notebooks
│   │   ├── performance_plots.ipynb
│   │   ├── training_curves.ipynb
│   │   └── system_monitoring.ipynb
│   └── reports/                    # Report generation
│       ├── phase1_report.ipynb
│       ├── phase5_report.ipynb
│       └── final_validation.ipynb
│
├── docker/                          # Docker configuration
│   ├── README.md
│   ├── Dockerfile.dev              # Development environment
│   ├── Dockerfile.jetson           # Jetson deployment
│   ├── Dockerfile.training         # Training environment
│   ├── docker-compose.yml          # Multi-container setup
│   └── .dockerignore
│
├── deployment/                      # Deployment artifacts
│   ├── README.md
│   ├── systemd/                    # Systemd service files
│   │   ├── kuka-controller.service
│   │   ├── kuka-safety.service
│   │   └── kuka-logging.service
│   ├── ansible/                    # Ansible playbooks
│   │   ├── deploy.yml
│   │   ├── update.yml
│   │   └── rollback.yml
│   ├── kubernetes/                 # K8s manifests (if applicable)
│   └── monitoring/                 # Monitoring configuration
│       ├── prometheus.yml
│       ├── grafana_dashboards/
│       └── alerting_rules.yml
│
├── tools/                           # Development tools
│   ├── README.md
│   ├── linters/                    # Code quality tools
│   │   ├── .flake8
│   │   ├── .pylintrc
│   │   └── mypy.ini
│   ├── formatters/                 # Code formatters
│   │   ├── .black.toml
│   │   └── .isort.cfg
│   ├── pre-commit/                 # Pre-commit hooks
│   │   └── .pre-commit-config.yaml
│   └── ide/                        # IDE configurations
│       ├── vscode/
│       └── pycharm/
│
├── .gitignore                       # Git ignore rules
├── .gitattributes                   # Git LFS configuration
├── .dvcignore                       # DVC ignore rules (if using DVC)
├── README.md                        # Main repository README
├── LICENSE                          # Project license
├── CONTRIBUTING.md                  # Contribution guidelines
├── CODE_OF_CONDUCT.md              # Code of conduct
├── CHANGELOG.md                     # Version history
├── requirements.txt                 # Python dependencies
├── requirements-dev.txt             # Development dependencies
├── setup.py                         # Package setup
├── pyproject.toml                   # Python project configuration
└── Makefile                         # Common commands
```

---

## 3. Directory Descriptions and Rationale

### 3.1 Source Code (`src/`)

**Purpose:** Contains all production source code organized by functional area.

**Rationale:**
- **Modular Design:** Each subdirectory represents a distinct system component
- **Clear Ownership:** Different teams can work on different modules with minimal conflicts
- **Testability:** Modular structure facilitates unit and integration testing
- **Reusability:** Components can be reused across different phases

**Key Subdirectories:**

#### `src/control/`
- **Purpose:** Real-time control system (1kHz loop)
- **Team:** Control Engineers
- **Critical Files:** `realtime_controller.py`, `kinematics.py`, `safety_monitor.py`
- **Dependencies:** Hardware interfaces, safety systems

#### `src/models/`
- **Purpose:** ML model implementations
- **Team:** ML Engineers
- **Critical Files:** `act_model.py`, `diffusion_policy.py`, `online_learning.py`
- **Dependencies:** Data preprocessing, training pipeline

#### `src/safety/`
- **Purpose:** Safety-critical code (ISO 13849-1 compliance)
- **Team:** Safety Officers + Control Engineers
- **Critical Files:** `safety_monitor.py`, `emergency_stop.py`, `collision_checker.py`
- **Special Requirements:** Extra code review, formal verification

### 3.2 Documentation (`docs/`)

**Purpose:** Comprehensive project documentation for all stakeholders.

**Rationale:**
- **Multi-Audience:** Separate sections for developers, operators, and maintenance personnel
- **Safety Compliance:** Dedicated safety documentation for ISO 13849-1
- **Knowledge Transfer:** Detailed guides enable onboarding and knowledge sharing
- **Traceability:** Links requirements to implementation

**Key Subdirectories:**

#### `docs/project/`
- Contains high-level project documentation
- Includes the comprehensive project analysis from planning phase
- Roadmap tracks progress through 7 phases

#### `docs/safety/`
- **Critical for Compliance:** Risk assessments, validation reports, LOTO procedures
- **Audience:** Safety officers, auditors, regulatory bodies
- **Version Control:** All safety docs must be version controlled and reviewed

#### `docs/guides/`
- **Operator Guides:** For production use
- **Developer Guides:** For software development
- **Maintenance Guides:** For system upkeep

### 3.3 Testing (`tests/`)

**Purpose:** Comprehensive test suite covering all system aspects.

**Rationale:**
- **Safety-Critical System:** Extensive testing required for safety certification
- **Multi-Level Testing:** Unit, integration, hardware-in-the-loop, performance
- **Continuous Validation:** Automated tests run on every commit
- **Regression Prevention:** Catch issues before they reach hardware

**Test Hierarchy:**
1. **Unit Tests:** Individual functions and classes
2. **Integration Tests:** Component interactions
3. **Hardware Tests:** Real hardware validation
4. **Performance Tests:** Timing and throughput benchmarks

### 3.4 Configuration (`config/`)

**Purpose:** Centralized configuration management.

**Rationale:**
- **Separation of Code and Config:** Easy to modify parameters without code changes
- **Environment-Specific:** Different configs for development, testing, production
- **Version Control:** Track configuration changes over time
- **Safety Parameters:** Safety limits stored separately and reviewed

**Organization:**
- **By System:** Robot, hardware, control, safety, ML
- **YAML Format:** Human-readable, easy to edit
- **Validation:** Config files validated on load

### 3.5 Data (`data/`)

**Purpose:** Storage for datasets, models, logs, and calibration data.

**Rationale:**
- **Large Files:** Not stored in Git (use LFS or DVC)
- **Organized by Type:** Demonstrations, datasets, models, logs
- **Phase-Based:** Data organized by project phase
- **Backup Strategy:** Critical data backed up regularly

**Special Considerations:**
- **Git Ignored:** Add to `.gitignore` to avoid bloating repository
- **DVC/LFS:** Use Data Version Control or Git LFS for large files
- **Access Control:** Sensitive data may require access restrictions

### 3.6 Hardware (`hardware/`)

**Purpose:** Hardware documentation, schematics, CAD files, datasheets.

**Rationale:**
- **Complete Documentation:** All hardware information in one place
- **As-Built Records:** Track actual installation vs. design
- **Maintenance Support:** Technicians need access to schematics and datasheets
- **Safety Compliance:** Electrical diagrams required for inspections

**File Types:**
- **PDFs:** Schematics, drawings (version controlled)
- **CAD Files:** STEP, DXF formats for mechanical parts
- **Datasheets:** Component specifications
- **Photos:** Installation photos, as-built documentation

### 3.7 Scripts (`scripts/`)

**Purpose:** Utility scripts for common tasks.

**Rationale:**
- **Automation:** Reduce manual work and errors
- **Reproducibility:** Standardize procedures
- **Documentation:** Scripts serve as executable documentation
- **Phase Support:** Scripts for each phase of development

**Categories:**
- **Setup:** Environment configuration
- **Data:** Data collection and processing
- **Training:** Model training workflows
- **Deployment:** Model deployment and optimization
- **Calibration:** System calibration procedures
- **Testing:** Test execution scripts

---

## 4. Main Repository README

```markdown
# Kuka Robot Arm AI-Driven Controller

[![Tests](https://miro.medium.com/v2/resize:fit:900/1*ti0sy9BO5w5ieFi1hq5m4A.png)](https://github.com/chadwick-yao/KUKA-Controller)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Safety](https://img.shields.io/badge/safety-ISO%2013849--1%20Cat%203-green.svg)](docs/safety/)

## Overview

This project replaces the legacy Kuka KR C2 controller with an AI-driven system powered by NVIDIA Jetson Orin Nano Super. The system enables autonomous task execution via trained neural networks while maintaining G-code compatibility and adding 3D printing capability.

**⚠️ SAFETY WARNING:** This system operates at 480V AC 3-phase power and controls a heavy industrial robot. All work must follow strict safety procedures. See [Safety Documentation](docs/safety/) before proceeding.

## Key Features

- **ML-Based Autonomous Control:** Action Chunking Transformer (ACT) and Diffusion Policy models
- **Real-Time Performance:** 1kHz control loop, 100Hz ML inference
- **Multi-Modal Sensing:** 3-5 cameras, force/torque sensor, absolute encoders
- **Safety Compliance:** ISO 13849-1 Category 3, Performance Level d (PLd)
- **G-Code Compatible:** Maintains traditional CNC operation mode
- **Online Learning:** Continuous improvement from human corrections

## Project Status

**Current Phase:** Phase 1 - LeRobot Proof of Concept (Weeks 1-8)  
**Timeline:** 48 weeks total (7 phases)  
**Team Size:** 5 key roles (Mechanical, Electrical, Software/Controls, ML, Integration & Testing)

See [Project Roadmap](docs/project/roadmap.md) for detailed timeline.

## Quick Start

### Prerequisites

- NVIDIA Jetson Orin Nano Super with JetPack 5.1.2+
- Ubuntu 22.04 with PREEMPT_RT kernel
- Python 3.10+
- EtherCAT-compatible motor drives (6x)
- Licensed electrician for 480V work

### Installation

```bash
# Clone repository
git clone https://github.com/chadwick-yao/KUKA-Controller
cd kuka-ml-controller

# Run setup script
./scripts/setup/install_dependencies.sh

# Configure Jetson for real-time operation
./scripts/setup/configure_jetson.sh

# Install EtherCAT master
./scripts/setup/setup_ethercat.sh
```

See [Setup Guide](docs/guides/developer/setup_guide.md) for detailed instructions.

### Running Tests

```bash
# Run all tests
make test

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/hardware/  # Requires hardware connection
```

### Training a Model

```bash
# Collect demonstrations
python scripts/data/collect_demonstrations.py --task pick_and_place --num_demos 100

# Train behavioral cloning model
python scripts/training/train_bc.py --config config/ml/bc_config.yaml

# Evaluate model
python scripts/training/evaluate_model.py --model models/checkpoints/bc_best.pth
```

### Deployment

```bash
# Convert model to TensorRT
python scripts/deployment/convert_to_tensorrt.py --model models/best_models/act_model.pth

# Deploy to Jetson
python scripts/deployment/deploy_model.py --model models/tensorrt/act_model.trt

# Benchmark performance
python scripts/deployment/benchmark_model.py
```

## Documentation

- **[Project Documentation](docs/project/)** - High-level project information
- **[Technical Specifications](docs/technical/)** - Detailed technical specs
- **[API Documentation](docs/api/)** - API reference
- **[User Guides](docs/guides/)** - Operator and developer guides
- **[Safety Documentation](docs/safety/)** - Safety procedures and compliance
- **[Tutorials](docs/tutorials/)** - Step-by-step tutorials

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Jetson Orin Nano Super                   │
│  ┌──────────────┐  ���──────────────┐  ┌──────────────┐     │
│  │  ML Inference│  │ Real-Time    │  │   Safety     │     │
│  │  (100Hz)     │  │ Control      │  │   Monitor    │     │
│  │              │  │ (1kHz)       │  │   (<50ms)    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
└────────────────────────────┼────────────────────────────────┘
                             │ EtherCAT (1kHz)
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
   │ Drive 1 │   ...   │ Drive 6 │         │ I/O     │
   │ (Axis 1)│         │ (Turn   │         │ Module  │
   └─────────┘         │  Bed)   │         └─────────┘
                       └─────────┘
```

See [Architecture Documentation](docs/project/architecture.md) for details.

## Safety

**⚠️ CRITICAL:** This system operates at 480V AC and controls a heavy industrial robot.

- **All electrical work must be performed by licensed electricians**
- **NFPA 70E training required for all personnel**
- **Arc-rated PPE mandatory for 480V work**
- **Never work alone on high-voltage systems**
- **Follow LOTO procedures before any work**

See [Safety Procedures](docs/safety/) for complete safety documentation.

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

### Development Workflow

1. Create feature branch from `develop`
2. Implement changes with tests
3. Run linters and formatters: `make lint format`
4. Run test suite: `make test`
5. Submit pull request with description
6. Address review comments
7. Merge after approval

See [Coding Standards](docs/guides/developer/coding_standards.md) for code style guidelines.

## Team

- **Project Manager:** [Name]
- **Electrical Lead:** [Name] (Licensed Electrician)
- **Mechanical Lead:** [Name]
- **Software/Controls Lead:** [Name]
- **ML Lead:** [Name]
- **Integration Lead:** [Name]
- **Safety Officer:** [Name]

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Kuka Robotics for robot documentation
- NVIDIA for Jetson platform and support
- Open-source robotics community

## Contact

- **Project Email:** kuka-ml-project@example.com
- **Safety Issues:** safety@example.com (24/7 response)
- **Technical Support:** support@example.com

## References

- [Project Analysis](docs/project/project_analysis.md)
- [Coding Tasks](docs/guides/developer/coding_tasks.md)
- [Human Tasks](docs/guides/operator/human_tasks.md)
- [ISO 13849-1 Safety Standard](https://www.iso.org/standard/69883.html)
- [NFPA 70E Electrical Safety](https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=70E)
```

---

## 5. Subdirectory README Templates

### 5.1 Source Code Module README Template

```markdown
# [Module Name]

## Overview

Brief description of module purpose and functionality.

## Responsibilities

- Responsibility 1
- Responsibility 2
- Responsibility 3

## Key Components

### [Component 1]
- **File:** `component1.py`
- **Purpose:** Description
- **Dependencies:** List dependencies
- **Usage Example:**
  ```python
  from module import Component1
  component = Component1(config)
  result = component.process(data)
  ```

### [Component 2]
- **File:** `component2.py`
- **Purpose:** Description
- **Dependencies:** List dependencies

## Configuration

Configuration files used by this module:
- `config/module/config1.yaml` - Description
- `config/module/config2.yaml` - Description

## Testing

Run module tests:
```bash
pytest tests/unit/test_module.py
pytest tests/integration/test_module_integration.py
```

## Performance Considerations

- Performance requirement 1
- Performance requirement 2
- Optimization notes

## Safety Considerations

(If applicable)
- Safety requirement 1
- Safety requirement 2
- Failure modes and handling

## Dependencies

- External library 1 (version)
- External library 2 (version)
- Internal module dependencies

## Team Ownership

- **Primary Owner:** [Name/Team]
- **Reviewers:** [Names]
- **Safety Review Required:** Yes/No

## References

- Related documentation
- External references
```

### 5.2 Hardware Subdirectory README Template

```markdown
# [Hardware Component]

## Overview

Description of hardware component and its role in the system.

## Specifications

- **Manufacturer:** [Name]
- **Model:** [Model Number]
- **Part Number:** [P/N]
- **Voltage:** [Voltage]
- **Current:** [Current]
- **Power:** [Power]
- **Communication:** [Protocol]

## Documentation

- **Datasheet:** `datasheets/component/datasheet.pdf`
- **User Manual:** `datasheets/component/manual.pdf`
- **Schematic:** `electrical/schematics/component_schematic.pdf`
- **Wiring Diagram:** `electrical/wiring_diagrams/component_wiring.pdf`

## Installation

### Prerequisites
- Tool 1
- Tool 2
- Safety equipment

### Procedure
1. Step 1
2. Step 2
3. Step 3

### Verification
- Check 1
- Check 2
- Check 3

## Configuration

### Software Configuration
```yaml
component:
  parameter1: value1
  parameter2: value2
```

### Hardware Configuration
- DIP switch settings
- Jumper positions
- Address configuration

## Testing

### Functional Tests
- Test 1
- Test 2

### Performance Tests
- Test 1
- Test 2

## Troubleshooting

### Issue 1
- **Symptoms:** Description
- **Cause:** Likely cause
- **Resolution:** How to fix

### Issue 2
- **Symptoms:** Description
- **Cause:** Likely cause
- **Resolution:** How to fix

## Maintenance

- **Inspection Frequency:** [Frequency]
- **Maintenance Tasks:**
  - Task 1
  - Task 2
- **Replacement Parts:** List of consumables

## Safety

**⚠️ WARNING:** Safety warnings specific to this component

- Safety consideration 1
- Safety consideration 2

## Vendor Contact

- **Manufacturer:** [Name]
- **Technical Support:** [Phone/Email]
- **Website:** [URL]
```

---

## 6. File Naming Conventions

### 6.1 General Principles

1. **Lowercase with underscores:** `my_module.py`, `test_kinematics.py`
2. **Descriptive names:** Names should clearly indicate purpose
3. **Consistent prefixes:** Use prefixes to group related files
4. **Version suffixes:** Avoid version numbers in filenames (use Git tags)

### 6.2 Python Files

**Format:** `[prefix_]descriptive_name.py`

**Examples:**
- `realtime_controller.py` - Main controller
- `test_kinematics.py` - Test file (prefix: `test_`)
- `benchmark_inference.py` - Benchmark script (prefix: `benchmark_`)

**Conventions:**
- **Classes:** PascalCase in code, but file is lowercase: `class RealtimeController` in `realtime_controller.py`
- **Test files:** Prefix with `test_`
- **Scripts:** Descriptive action names: `collect_demonstrations.py`

### 6.3 Configuration Files

**Format:** `[component_]config_name.yaml`

**Examples:**
- `robot_config.yaml` - Robot parameters
- `kuka_kr150.yaml` - Specific robot model
- `pid_gains.yaml` - PID parameters
- `safety_limits.yaml` - Safety thresholds

**Conventions:**
- **YAML format:** Preferred for configuration
- **Hierarchical:** Use subdirectories for organization
- **Environment-specific:** `config_dev.yaml`, `config_prod.yaml`

### 6.4 Documentation Files

**Format:** `descriptive_name.md`

**Examples:**
- `project_analysis.md` - Project analysis
- `setup_guide.md` - Setup instructions
- `api_reference.md` - API documentation

**Conventions:**
- **Markdown format:** `.md` extension
- **Numbered tutorials:** `01_environment_setup.md`, `02_data_collection.md`
- **README files:** Always `README.md` (uppercase)

### 6.5 Hardware Files

**Format:** `[component_]descriptive_name.[ext]`

**Examples:**
- `power_distribution.pdf` - Electrical schematic
- `robot_model.step` - CAD file
- `drive_datasheet.pdf` - Component datasheet
- `wiring_diagram_v2.pdf` - Wiring diagram (version in name acceptable for PDFs)

**Conventions:**
- **PDFs:** For schematics, drawings, datasheets
- **CAD files:** STEP, DXF, DWG formats
- **Photos:** `installation_photo_001.jpg` (numbered sequence)

### 6.6 Data Files

**Format:** `[type_]descriptive_name_[timestamp].[ext]`

**Examples:**
- `demo_pick_place_20251214_143022.h5` - Demonstration recording
- `model_act_epoch50.pth` - Model checkpoint
- `log_system_20251214.log` - System log
- `calibration_camera1_20251214.yaml` - Calibration data

**Conventions:**
- **Timestamps:** ISO 8601 format `YYYYMMDD_HHMMSS`
- **Datasets:** HDF5 (`.h5`) or Zarr (`.zarr`)
- **Models:** PyTorch (`.pth`), ONNX (`.onnx`), TensorRT (`.trt`)
- **Logs:** `.log` extension

### 6.7 Script Files

**Format:** `action_description.py` or `action_description.sh`

**Examples:**
- `install_dependencies.sh` - Installation script
- `train_bc.py` - Training script
- `deploy_model.py` - Deployment script
- `backup_system.sh` - Backup script

**Conventions:**
- **Action verbs:** Start with action (install, train, deploy, backup)
- **Shell scripts:** `.sh` extension
- **Python scripts:** `.py` extension
- **Executable:** Mark as executable (`chmod +x`)

---

## 7. Documentation Hierarchy

### 7.1 Documentation Levels

```
Level 1: Repository README
    ├── Level 2: docs/README.md (Documentation Index)
    │   ├── Level 3: docs/project/ (Project Documentation)
    │   ├── Level 3: docs/technical/ (Technical Specifications)
    │   ├── Level 3: docs/api/ (API Documentation)
    │   ├── Level 3: docs/guides/ (User Guides)
    │   └── Level 3: docs/safety/ (Safety Documentation)
    ├── Level 2: src/[module]/README.md (Module Documentation)
    ├── Level 2: tests/README.md (Testing Documentation)
    ├── Level 2: scripts/README.md (Scripts Documentation)
    └── Level 2: hardware/README.md (Hardware Documentation)
```

### 7.2 Documentation Flow

**For New Developers:**
1. Start with main `README.md`
2. Read `docs/guides/developer/setup_guide.md`
3. Review `docs/project/architecture.md`
4. Explore module-specific READMEs in `src/`
5. Read `docs/guides/developer/coding_standards.md`

**For Operators:**
1. Start with main `README.md`
2. Read `docs/guides/operator/operation_manual.md`
3. Review `docs/safety/safety_procedures.md`
4. Refer to `docs/guides/operator/troubleshooting.md` as needed

**For Hardware Technicians:**
1. Start with `hardware/README.md`
2. Review electrical schematics in `hardware/electrical/`
3. Read `docs/guides/operator/human_tasks.md`
4. Refer to component datasheets in `hardware/datasheets/`

**For Safety Officers:**
1. Start with `docs/safety/README.md`
2. Review `docs/safety/risk_assessment.md`
3. Read `docs/safety/compliance_report.md`
4. Check `docs/safety/safety_validation.md`

### 7.3 Cross-Referencing

**Use relative links in Markdown:**
```markdown
See [Architecture Documentation](../project/architecture.md) for details.
Refer to [Safety Procedures](../../safety/safety_procedures.md).
```

**Link to code:**
```markdown
Implementation: [`src/control/realtime_controller.py`](../../src/control/realtime_controller.py)
```

**Link to configuration:**
```markdown
Configuration: [`config/robot/kuka_kr150.yaml`](../../config/robot/kuka_kr150.yaml)
```

### 7.4 Documentation Standards

**Markdown Style:**
- Use ATX-style headers (`#`, `##`, `###`)
- Include table of contents for long documents
- Use code blocks with language specification
- Include diagrams where helpful (Mermaid, PlantUML, or images)

**Code Documentation:**
- **Docstrings:** All public functions, classes, and modules
- **Type hints:** Use Python type hints
- **Comments:** Explain "why", not "what"
- **Examples:** Include usage examples in docstrings

**API Documentation:**
- **Auto-generated:** Use Sphinx or similar tool
- **Keep updated:** Regenerate on code changes
- **Examples:** Include request/response examples

---

## 8. Version Control Strategy

### 8.1 Branching Model

**Git Flow Variant:**

```
main (production)
    ├── develop (integration)
    │   ├── feature/phase1-lerobot-poc
    │   ├── feature/ml-act-model
    │   ├── feature/safety-monitor
    │   ├── bugfix/encoder-reading-issue
    │   └── hotfix/emergency-stop-fix
    ├── release/v1.0.0
    └── hotfix/critical-safety-fix
```

**Branch Types:**

1. **`main`** - Production-ready code
   - Protected branch
   - Requires pull request + reviews
   - Tagged with version numbers
   - Deployed to production

2. **`develop`** - Integration branch
   - All features merge here first
   - Continuous integration testing
   - Staging environment deployment

3. **`feature/*`** - Feature development
   - Branch from `develop`
   - Naming: `feature/phase[N]-description` or `feature/component-description`
   - Examples: `feature/phase1-lerobot-poc`, `feature/ml-diffusion-policy`
   - Merge back to `develop` via pull request

4. **`bugfix/*`** - Bug fixes
   - Branch from `develop`
   - Naming: `bugfix/issue-description`
   - Example: `bugfix/encoder-noise-filtering`

5. **`hotfix/*`** - Critical production fixes
   - Branch from `main`
   - Naming: `hotfix/critical-issue`
   - Merge to both `main` and `develop`
   - Example: `hotfix/safety-system-timeout`

6. **`release/*`** - Release preparation
   - Branch from `develop`
   - Naming: `release/v[major].[minor].[patch]`
   - Example: `release/v1.0.0`
   - Merge to `main` and `develop`

### 8.2 Commit Conventions

**Format:** `<type>(<scope>): <subject>`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `safety`: Safety-related changes (requires extra review)

**Scopes:**
- `control`: Control system
- `ml`: Machine learning
- `hardware`: Hardware interfaces
- `safety`: Safety systems
- `data`: Data handling
- `docs`: Documentation
- `config`: Configuration
- `tests`: Testing

**Examples:**
```
feat(ml): implement ACT model with 10-step action chunks
fix(control): correct inverse kinematics singularity handling
docs(safety): update risk assessment for 480V system
safety(hardware): add redundant E-stop circuit validation
test(integration): add multi-axis coordination tests
perf(ml): optimize TensorRT inference to 8ms
```

**Commit Message Body:**
```
feat(ml): implement ACT model with 10-step action chunks

- Add transformer encoder for observation processing
- Add transformer decoder for action prediction
- Implement positional encoding
- Add training script with proper loss function
- Benchmark inference time: 9.2ms on Jetson

Closes #123
```

### 8.3 Tagging Strategy

**Version Format:** `v[major].[minor].[patch]`

**Semantic Versioning:**
- **Major:** Breaking changes, major milestones (e.g., phase completion)
- **Minor:** New features, non-breaking changes
- **Patch:** Bug fixes, minor improvements

**Examples:**
- `v0.1.0` - Phase 1 (LeRobot PoC) complete
- `v0.2.0` - Phase 2 (System Analysis) complete
- `v0.3.0` - Phase 3 (Hardware Design) complete
- `v1.0.0` - Phase 7 (Production Deployment) complete
- `v1.0.1` - Bug fix release
- `v1.1.0` - New feature added

**Tag Annotations:**
```bash
git tag -a v0.1.0 -m "Phase 1: LeRobot Proof of Concept Complete

- Follower arm assembled and operational
- Collected 150 demonstrations
- Trained BC model with 85% success rate
- Inference latency: 42ms on Jetson
- Team validated ML approach

Deliverables:
- Functional LeRobot system
- Trained baseline models
- Performance benchmarking report
- Scaling requirements document"
```

### 8.4 Pull Request Process

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Safety-critical change (requires extra review)

## Related Issues
Closes #123
Related to #456

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Hardware tests performed (if applicable)
- [ ] All tests passing

## Safety Impact
- [ ] No safety impact
- [ ] Safety impact assessed (describe below)
- [ ] Safety review required

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added for new functionality
- [ ] All tests passing

## Screenshots/Videos
(If applicable)

## Additional Notes
Any additional information
```

**Review Requirements:**
- **Standard PRs:** 1 approval required
- **Safety-critical PRs:** 2 approvals required (including safety officer)
- **Hardware PRs:** 1 approval from hardware team
- **ML PRs:** 1 approval from ML team

**Merge Strategy:**
- **Squash and merge:** For feature branches (clean history)
- **Merge commit:** For release branches (preserve history)
- **Rebase and merge:** For small bug fixes

### 8.5 Protected Branches

**`main` Branch Protection:**
- Require pull request reviews (2 approvals for safety-critical)
- Require status checks to pass
- Require branches to be up to date
- Restrict who can push
- Require signed commits (optional but recommended)

**`develop` Branch Protection:**
- Require pull request reviews (1 approval)
- Require status checks to pass
- Allow force pushes by admins only

---

## 9. Collaboration Guidelines

### 9.1 Code Review Process

**Review Checklist:**

**Functionality:**
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] No obvious bugs

**Code Quality:**
- [ ] Follows coding standards
- [ ] Well-structured and readable
- [ ] Appropriate comments
- [ ] No code duplication
- [ ] Efficient implementation

**Testing:**
- [ ] Tests included
- [ ] Tests cover main functionality
- [ ] Tests cover edge cases
- [ ] All tests passing

**Documentation:**
- [ ] Docstrings present
- [ ] README updated if needed
- [ ] API docs updated if needed
- [ ] Comments explain complex logic

**Safety (if applicable):**
- [ ] Safety requirements met
- [ ] Failure modes considered
- [ ] Safety limits enforced
- [ ] Emergency stop handling correct

**Review Timeline:**
- **Standard PRs:** Review within 2 business days
- **Urgent PRs:** Review within 1 business day
- **Safety-critical PRs:** Review within 4 hours

### 9.2 Issue Templates

**Bug Report Template:**
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Hardware: [Jetson/Development PC]
- OS: [Ubuntu version]
- Python version:
- Branch/Commit:

## Logs/Screenshots
Attach relevant logs or screenshots

## Severity
- [ ] Critical (system unsafe or non-functional)
- [ ] High (major functionality broken)
- [ ] Medium (functionality impaired)
- [ ] Low (minor issue)

## Safety Impact
- [ ] No safety impact
- [ ] Potential safety impact (describe)
```

**Feature Request Template:**
```markdown
## Feature Description
Clear description of the proposed feature

## Motivation
Why is this feature needed?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other approaches considered

## Implementation Notes
Technical considerations

## Phase
Which project phase does this relate to?
- [ ] Phase 1: LeRobot PoC
- [ ] Phase 2: System Analysis
- [ ] Phase 3: Hardware Design
- [ ] Phase 4: Software Development
- [ ] Phase 5: ML Development
- [ ] Phase 6: Integration & Testing
- [ ] Phase 7: Production Deployment

## Priority
- [ ] Critical
- [ ] High
- [ ] Medium
- [ ] Low
```

**Safety Issue Template:**
```markdown
## ⚠️ SAFETY ISSUE ⚠️

## Issue Description
Clear description of the safety concern

## Severity
- [ ] CRITICAL - Immediate danger to personnel
- [ ] HIGH - Potential danger to personnel
- [ ] MEDIUM - Equipment damage risk
- [ ] LOW - Minor safety concern

## Affected Systems
- [ ] Emergency stop system
- [ ] Safety monitoring
- [ ] Collision detection
- [ ] Limit checking
- [ ] Hardware interlocks
- [ ] Other: ___________

## Immediate Actions Taken
What has been done to mitigate the issue?

## Root Cause (if known)
What caused this issue?

## Proposed Resolution
How should this be fixed?

## Verification Required
How will the fix be verified?

## Notification
- [ ] Safety officer notified
- [ ] Project manager notified
- [ ] Team notified
- [ ] Operations notified (if in production)
```

### 9.3 Communication Channels

**Synchronous Communication:**
- **Daily Standups:** 15 minutes, 9:00 AM
  - What did you do yesterday?
  - What will you do today?
  - Any blockers?

- **Weekly Team Meetings:** 1 hour, Mondays 10:00 AM
  - Progress review
  - Upcoming tasks
  - Technical discussions
  - Risk review

- **Phase Review Meetings:** 2 hours, end of each phase
  - Phase completion review
  - Lessons learned
  - Next phase planning

**Asynchronous Communication:**
- **GitHub Issues:** Task tracking, bug reports
- **GitHub Discussions:** Technical discussions, Q&A
- **Pull Request Comments:** Code review feedback
- **Slack/Teams:** Quick questions, coordination
- **Email:** Formal communications, external stakeholders

**Documentation:**
- **Wiki/Confluence:** Long-form documentation
- **GitHub README files:** Module documentation
- **Shared Drive:** Hardware docs, datasheets, photos

### 9.4 Code Ownership

**CODEOWNERS File:**
```
# Global owners
* @project-lead @safety-officer

# Source code
/src/control/ @control-team @safety-officer
/src/models/ @ml-team
/src/hardware/ @hardware-team @electrical-lead
/src/safety/ @safety-officer @control-team
/src/data/ @ml-team
/src/training/ @ml-team

# Configuration
/config/safety/ @safety-officer
/config/robot/ @control-team
/config/ml/ @ml-team

# Documentation
/docs/safety/ @safety-officer
/docs/technical/ @technical-writer
/docs/guides/ @technical-writer

# Hardware
/hardware/electrical/ @electrical-lead
/hardware/mechanical/ @mechanical-lead

# Tests
/tests/safety/ @safety-officer
/tests/hardware/ @hardware-team

# Critical files
/src/safety/emergency_stop.py @safety-officer @control-team @project-lead
/config/safety/safety_limits.yaml @safety-officer @project-lead
```

**Ownership Responsibilities:**
- **Review PRs** affecting owned code
- **Maintain documentation** for owned modules
- **Respond to issues** related to owned code
- **Ensure quality** of owned code

### 9.5 Contribution Workflow

**For Team Members:**

1. **Create Issue** (if not exists)
   - Describe task/bug/feature
   - Assign to yourself
   - Add labels and milestone

2. **Create Branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

3. **Develop**
   - Write code
   - Write tests
   - Update documentation
   - Commit regularly with good messages

4. **Test Locally**
   ```bash
   make lint
   make format
   make test
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create PR on GitHub
   ```

6. **Address Review Comments**
   - Make requested changes
   - Push updates
   - Respond to comments

7. **Merge**
   - After approval, merge PR
   - Delete feature branch

**For External Contributors:**

1. **Fork Repository**
2. **Create Branch** in your fork
3. **Develop** and test
4. **Submit PR** from your fork
5. **Sign CLA** (if required)
6. **Address Review Comments**
7. **Maintainer Merges** after approval

---

## 10. Large File Management

### 10.1 Problem Statement

**Large files in this project:**
- **Datasets:** Demonstration recordings (100+ GB)
- **Models:** Trained neural networks (100+ MB each)
- **Logs:** System operation logs (GB per day)
- **CAD Files:** Mechanical designs (10+ MB each)
- **Videos:** Training demonstrations, test recordings

**Git limitations:**
- Slow cloning with large files
- Repository bloat
- Difficult to manage versions

### 10.2 Solution: Git LFS + DVC

**Git LFS (Large File Storage):**
- For binary files that need version control
- CAD files, firmware, some models

**DVC (Data Version Control):**
- For datasets and experiment tracking
- ML models, training data, logs

### 10.3 Git LFS Configuration

**Installation:**
```bash
# Install Git LFS
git lfs install

# Track file types
git lfs track "*.pth"
git lfs track "*.onnx"
git lfs track "*.trt"
git lfs track "*.h5"
git lfs track "*.step"
git lfs track "*.stl"
git lfs track "*.pdf"
git lfs track "*.mp4"
git lfs track "*.avi"
```

**.gitattributes:**
```
# ML Models
*.pth filter=lfs diff=lfs merge=lfs -text
*.onnx filter=lfs diff=lfs merge=lfs -text
*.trt filter=lfs diff=lfs merge=lfs -text

# Datasets
*.h5 filter=lfs diff=lfs merge=lfs -text
*.zarr filter=lfs diff=lfs merge=lfs -text

# CAD Files
*.step filter=lfs diff=lfs merge=lfs -text
*.stl filter=lfs diff=lfs merge=lfs -text
*.dxf filter=lfs diff=lfs merge=lfs -text

# Documents
*.pdf filter=lfs diff=lfs merge=lfs -text

# Videos
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.avi filter=lfs diff=lfs merge=lfs -text
```

**Usage:**
```bash
# Add file (automatically tracked by LFS)
git add model.pth
git commit -m "Add trained model"
git push

# Clone repository (LFS files downloaded automatically)
git clone https://github.com/chadwick-yao/KUKA-Controller
```

### 10.4 DVC Configuration

**Installation:**
```bash
# Install DVC
pip install dvc[s3]  # or [gs], [azure], etc.

# Initialize DVC
dvc init

# Configure remote storage (S3 example)
dvc remote add -d storage s3://my-bucket/kuka-ml-data
dvc remote modify storage region us-west-2
```

**Tracking Data:**
```bash
# Track dataset
dvc add data/demonstrations/phase1_lerobot/
git add data/demonstrations/phase1_lerobot/.dvc .gitignore
git commit -m "Add Phase 1 demonstration data"

# Push data to remote storage
dvc push

# Pull data from remote storage
dvc pull
```

**DVC Pipeline:**
```yaml
# dvc.yaml
stages:
  preprocess:
    cmd: python scripts/data/process_dataset.py
    deps:
      - data/demonstrations/
      - scripts/data/process_dataset.py
    outs:
      - data/datasets/processed/
    
  train:
    cmd: python scripts/training/train_act.py
    deps:
      - data/datasets/processed/
      - src/models/act_model.py
      - config/ml/act_config.yaml
    outs:
      - models/checkpoints/
    metrics:
      - metrics/training_metrics.json
    
  evaluate:
    cmd: python scripts/training/evaluate_model.py
    deps:
      - models/checkpoints/best.pth
      - data/datasets/test/
    metrics:
      - metrics/evaluation_metrics.json
```

**Run Pipeline:**
```bash
# Run entire pipeline
dvc repro

# Run specific stage
dvc repro train

# Show metrics
dvc metrics show

# Compare experiments
dvc metrics diff
```

### 10.5 Storage Strategy

**Git Repository:**
- Source code
- Configuration files
- Documentation (Markdown)
- Small test fixtures

**Git LFS:**
- Trained models (best models only)
- CAD files
- Firmware binaries
- Important PDFs

**DVC + Remote Storage:**
- Demonstration datasets
- Training datasets
- Model checkpoints (all)
- Experiment logs
- Large test data

**Local Only (not tracked):**
- Temporary files
- Build artifacts
- Cache files
- Personal notes

**.gitignore:**
```
# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
*.egg-info/

# Data (tracked by DVC)
/data/demonstrations/
/data/datasets/
/data/models/checkpoints/
/data/logs/

# Temporary
*.tmp
*.temp
.cache/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Build
build/
dist/
```

### 10.6 Best Practices

**Do:**
- ✅ Use DVC for datasets and experiments
- ✅ Use Git LFS for binary files that need version control
- ✅ Keep repository size reasonable (<1 GB)
- ✅ Document data storage locations
- ✅ Backup remote storage regularly

**Don't:**
- ❌ Commit large files directly to Git
- ❌ Track temporary or generated files
- ❌ Store sensitive data in repository
- ❌ Track every model checkpoint (only best/important ones)

---

## 11. CI/CD Integration

### 11.1 Continuous Integration

**GitHub Actions Workflows:**

#### Test Workflow (`.github/workflows/tests.yml`)
```yaml
name: Tests

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run unit tests
        run: |
          pytest tests/unit/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
  
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run integration tests
        run: |
          pytest tests/integration/
  
  safety-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run safety tests
        run: |
          pytest tests/unit/test_safety.py -v
          pytest tests/integration/test_safety_system.py -v
      
      - name: Safety test report
        if: failure()
        run: |
          echo "⚠️ SAFETY TESTS FAILED ⚠️"
          echo "Do not merge until safety tests pass!"
```

#### Lint Workflow (`.github/workflows/lint.yml`)
```yaml
name: Lint

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install linters
        run: |
          pip install flake8 black mypy pylint
      
      - name: Run flake8
        run: flake8 src/ tests/
      
      - name: Check formatting with black
        run: black --check src/ tests/
      
      - name: Run mypy
        run: mypy src/
      
      - name: Run pylint
        run: pylint src/
```

#### Documentation Workflow (`.github/workflows/docs.yml`)
```yaml
name: Documentation

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install sphinx sphinx-rtd-theme
      
      - name: Build documentation
        run: |
          cd docs/
          make html
      
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/_build/html
```

### 11.2 Continuous Deployment

**Deployment Workflow (`.github/workflows/deploy.yml`):**
```yaml
name: Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy-jetson:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest tests/
      
      - name: Build deployment package
        run: |
          python setup.py sdist bdist_wheel
      
      - name: Deploy to Jetson (staging)
        if: contains(github.ref, 'rc')
        run: |
          # Deploy to staging Jetson
          ansible-playbook deployment/ansible/deploy.yml -i staging
      
      - name: Deploy to Jetson (production)
        if: "!contains(github.ref, 'rc')"
        run: |
          # Deploy to production Jetson
          ansible-playbook deployment/ansible/deploy.yml -i production
      
      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: contains(github.ref, 'rc')
```

### 11.3 Pre-commit Hooks

**`.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
  
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.10
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ['--profile', 'black']
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

**Installation:**
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### 11.4 Automated Testing Strategy

**Test Pyramid:**
```
        /\
       /  \
      / E2E \          End-to-End Tests (few, slow)
     /______\
    /        \
   /Integration\       Integration Tests (some, medium)
  /____________\
 /              \
/   Unit Tests   \     Unit Tests (many, fast)
/__________________\
```

**Test Execution:**
- **On every commit:** Unit tests, linting
- **On pull request:** Unit + integration tests
- **Nightly:** Full test suite including hardware tests
- **Before release:** Complete validation including performance tests

**Test Coverage Goals:**
- **Overall:** >80%
- **Safety-critical code:** >95%
- **Control system:** >90%
- **ML models:** >70% (focus on interfaces)

---

## 12. Example Workflows

### 12.1 Adding a New ML Model

**Scenario:** Implement a new Diffusion Policy model

**Steps:**

1. **Create Feature Branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/ml-diffusion-policy
   ```

2. **Create Model File**
   ```bash
   # Create model implementation
   touch src/models/diffusion_policy.py
   
   # Create configuration
   touch config/ml/diffusion_config.yaml
   
   # Create training script
   touch scripts/training/train_diffusion.py
   ```

3. **Implement Model**
   - Write model code in `src/models/diffusion_policy.py`
   - Add docstrings and type hints
   - Follow coding standards

4. **Add Tests**
   ```bash
   # Create test file
   touch tests/unit/test_diffusion_policy.py
   
   # Write tests
   # - Test model initialization
   # - Test forward pass
   # - Test loss computation
   # - Test inference
   ```

5. **Update Documentation**
   ```bash
   # Update model README
   vim src/models/README.md
   
   # Add API documentation
   vim docs/api/ml_api.md
   
   # Add training guide
   vim docs/guides/developer/training_guide.md
   ```

6. **Test Locally**
   ```bash
   # Run tests
   pytest tests/unit/test_diffusion_policy.py -v
   
   # Run linters
   make lint
   
   # Format code
   make format
   
   # Run all tests
   make test
   ```

7. **Commit and Push**
   ```bash
   git add src/models/diffusion_policy.py
   git add config/ml/diffusion_config.yaml
   git add scripts/training/train_diffusion.py
   git add tests/unit/test_diffusion_policy.py
   git add docs/
   
   git commit -m "feat(ml): implement Diffusion Policy model

   - Add DiffusionPolicy class with U-Net denoising
   - Add training script with proper loss function
   - Add configuration file with hyperparameters
   - Add unit tests for model components
   - Update documentation with usage examples
   
   Closes #234"
   
   git push origin feature/ml-diffusion-policy
   ```

8. **Create Pull Request**
   - Go to GitHub
   - Create PR from `feature/ml-diffusion-policy` to `develop`
   - Fill out PR template
   - Request review from ML team

9. **Address Review Comments**
   - Make requested changes
   - Push updates
   - Respond to comments

10. **Merge**
    - After approval, squash and merge
    - Delete feature branch

### 12.2 Fixing a Safety-Critical Bug

**Scenario:** Emergency stop response time exceeds 50ms requirement

**Steps:**

1. **Create Hotfix Branch** (if in production)
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/emergency-stop-timeout
   ```
   
   Or feature branch (if in development):
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b bugfix/emergency-stop-timeout
   ```

2. **Create Safety Issue**
   - Use safety issue template
   - Mark as CRITICAL
   - Notify safety officer immediately

3. **Investigate**
   - Review code in `src/safety/emergency_stop.py`
   - Check timing measurements
   - Identify root cause

4. **Fix Issue**
   - Modify code to reduce response time
   - Add timing measurements
   - Optimize critical path

5. **Test Thoroughly**
   ```bash
   # Run safety tests
   pytest tests/unit/test_safety.py -v
   pytest tests/integration/test_safety_system.py -v
   
   # Run hardware tests
   pytest tests/hardware/test_emergency_stop.py -v
   
   # Measure response time
   python scripts/testing/measure_estop_response.py
   ```

6. **Document Fix**
   - Update safety documentation
   - Document root cause
   - Document verification results

7. **Commit with Safety Tag**
   ```bash
   git add src/safety/emergency_stop.py
   git add tests/
   git add docs/safety/
   
   git commit -m "safety(hardware): fix emergency stop response time

   Root cause: GPIO interrupt handling had excessive latency
   
   Changes:
   - Optimize GPIO interrupt handler
   - Reduce safety monitor loop time
   - Add real-time priority to safety thread
   
   Verification:
   - Response time now 38ms (was 62ms)
   - Tested 100 times, max 42ms
   - All safety tests passing
   
   CRITICAL FIX - Requires immediate review
   
   Closes #567"
   
   git push origin hotfix/emergency-stop-timeout
   ```

8. **Create Urgent PR**
   - Mark as urgent
   - Request review from safety officer + control lead
   - Provide detailed test results

9. **Fast-Track Review**
   - Safety officer reviews within 4 hours
   - Control lead reviews
   - Both approve

10. **Merge and Deploy**
    ```bash
    # Merge to main (if hotfix)
    git checkout main
    git merge --no-ff hotfix/emergency-stop-timeout
    git tag -a v1.0.2 -m "Hotfix: Emergency stop response time"
    git push origin main --tags
    
    # Merge to develop
    git checkout develop
    git merge --no-ff hotfix/emergency-stop-timeout
    git push origin develop
    
    # Deploy immediately
    ansible-playbook deployment/ansible/deploy.yml -i production
    ```

11. **Verify in Production**
    - Test emergency stop on actual system
    - Measure response time
    - Document verification

12. **Update Safety Records**
    - Update incident report
    - Update safety validation report
    - Notify team of resolution

### 12.3 Collecting and Training on New Data

**Scenario:** Collect demonstrations for a new task and train a model

**Steps:**

1. **Setup Data Collection**
   ```bash
   # Create branch
   git checkout develop
   git checkout -b feature/data-new-task
   
   # Configure teleoperation
   vim config/teleoperation/teleop_config.yaml
   ```

2. **Collect Demonstrations**
   ```bash
   # Start teleoperation system
   python scripts/data/collect_demonstrations.py \
     --task pick_and_place_new \
     --num_demos 150 \
     --output data/demonstrations/new_task/
   ```

3. **Process Dataset**
   ```bash
   # Process raw demonstrations
   python scripts/data/process_dataset.py \
     --input data/demonstrations/new_task/ \
     --output data/datasets/new_task_processed/
   
   # Split dataset
   python scripts/data/split_dataset.py \
     --input data/datasets/new_task_processed/ \
     --train 0.8 --val 0.1 --test 0.1
   ```

4. **Track with DVC**
   ```bash
   # Add to DVC
   dvc add data/demonstrations/new_task/
   dvc add data/datasets/new_task_processed/
   
   # Commit DVC files
   git add data/demonstrations/new_task/.dvc
   git add data/datasets/new_task_processed/.dvc
   git add .gitignore
   git commit -m "data: add new task demonstrations (150 demos)"
   
   # Push data to remote
   dvc push
   ```

5. **Train Model**
   ```bash
   # Train ACT model
   python scripts/training/train_act.py \
     --config config/ml/act_config.yaml \
     --dataset data/datasets/new_task_processed/ \
     --output models/checkpoints/new_task_act/
   ```

6. **Track Experiment**
   ```bash
   # DVC tracks metrics automatically
   dvc metrics show
   
   # Compare with baseline
   dvc metrics diff
   ```

7. **Evaluate Model**
   ```bash
   # Evaluate on test set
   python scripts/training/evaluate_model.py \
     --model models/checkpoints/new_task_act/best.pth \
     --dataset data/datasets/new_task_processed/test/
   ```

8. **Convert to TensorRT**
   ```bash
   # Optimize for Jetson
   python scripts/deployment/convert_to_tensorrt.py \
     --model models/checkpoints/new_task_act/best.pth \
     --output models/tensorrt/new_task_act.trt
   
   # Benchmark
   python scripts/deployment/benchmark_model.py \
     --model models/tensorrt/new_task_act.trt
   ```

9. **Commit Results**
   ```bash
   # Add model to Git LFS
   git add models/checkpoints/new_task_act/best.pth
   git add models/tensorrt/new_task_act.trt
   
   # Add metrics
   git add metrics/
   
   # Commit
   git commit -m "feat(ml): train ACT model for new task

   - Collected 150 demonstrations
   - Trained ACT model for 100 epochs
   - Achieved 87% success rate on test set
   - Inference time: 8.5ms on Jetson
   
   Metrics:
   - Train loss: 0.023
   - Val loss: 0.031
   - Test accuracy: 87%
   
   Closes #345"
   
   git push origin feature/data-new-task
   ```

10. **Create PR and Deploy**
    - Create pull request
    - Get review from ML team
    - Merge to develop
    - Deploy to staging for testing
    - Deploy to production after validation

---

## Conclusion

This repository structure is designed to support the **48-week, 7-phase Kuka robot arm AI-driven controller replacement project**. It provides:

1. **Clear Organization:** Separate directories for code, docs, tests, data, hardware
2. **Multi-Disciplinary Support:** Structure accommodates ML engineers, control engineers, hardware technicians, and safety officers
3. **Safety-First Design:** Special attention to safety-critical code and documentation
4. **Scalability:** Grows from proof-of-concept to production deployment
5. **Collaboration:** Clear guidelines for code review, issues, and pull requests
6. **Version Control:** Comprehensive strategy for code, data, and large files
7. **Automation:** CI/CD pipelines for testing, linting, and deployment
8. **Documentation:** Comprehensive docs at every level

**Key Success Factors:**

- **Follow the structure:** Don't deviate without team discussion
- **Document everything:** Code, decisions, changes, issues
- **Test thoroughly:** Especially safety-critical code
- **Review carefully:** All PRs require review, safety PRs require extra scrutiny
- **Communicate clearly:** Use issues, PRs, and meetings effectively
- **Safety first:** Never compromise on safety for speed

**Next Steps:**

1. Create repository with this structure
2. Set up CI/CD pipelines
3. Configure Git LFS and DVC
4. Create initial documentation
5. Begin Phase 1 development

---

**Document Version:** 1.0  
**Last Updated:** December 14, 2025  
**Maintained By:** Project Lead, Technical Lead  
**Review Schedule:** Monthly during active development

---

**END OF REPOSITORY STRUCTURE DOCUMENTATION**
