# Kuka Robot Arm AI-Driven Controller: Coding Tasks Documentation

**Document Version:** 1.0  
**Date:** December 14, 2025  
**Target Audience:** Developers and AI Agents  
**Project Phase:** Implementation Planning

---

## Table of Contents

1. [Overview](#overview)
2. [Development Environment Setup](#development-environment-setup)
3. [Data Collection and Preprocessing](#data-collection-and-preprocessing)
4. [ML Model Development](#ml-model-development)
5. [Real-Time Control System Implementation](#real-time-control-system-implementation)
6. [Hardware Interface Integration](#hardware-interface-integration)
7. [Testing and Validation](#testing-and-validation)
8. [Code Organization and Structure](#code-organization-and-structure)
9. [Implementation Priorities](#implementation-priorities)
10. [References](#references)

---

## Overview

### Project Goal
Replace the legacy Kuka KR C2 controller with an AI-driven system powered by NVIDIA Jetson Orin Nano Super, enabling autonomous task execution via trained neural networks while maintaining G-code compatibility and adding 3D printing capability.

### Technical Context
- **Source Analysis:** `./analysis/project_analysis.md`
- **Robot System:** Kuka 5-axis arm + turning bed (KR 150/180/210 series)
- **Computing Platform:** NVIDIA Jetson Orin Nano Super (8-core ARM, 1024 CUDA cores, 8GB RAM)
- **Control Protocol:** EtherCAT (1kHz cycle time)
- **Power System:** 480V AC 3-phase (CRITICAL: High voltage safety requirements)
- **Motor Drives:** 6x 7.5kW servo drives (replacement required - existing drives use DeviceNet/PROFIBUS, not EtherCAT)

### Key Technical Specifications
- **Control Loop Frequency:** 1kHz for low-level control
- **ML Inference Frequency:** 100Hz
- **Sensor Acquisition:** 60Hz
- **Safety Response Time:** <50ms
- **ML Inference Latency Target:** <10ms
- **Position Accuracy Target:** ±0.05mm
- **Repeatability Target:** ±0.02mm

### Development Phases
This coding documentation supports the following implementation phases:
- **Phase 1:** LeRobot Proof of Concept (Weeks 1-8)
- **Phase 4:** Software Architecture Development (Weeks 21-28)
- **Phase 5:** ML Model Development (Weeks 29-36)
- **Phase 6:** System Integration & Testing (Weeks 37-44)

---

## Development Environment Setup

### 1.1 Hardware Requirements

#### Primary Development Platform
- **NVIDIA Jetson Orin Nano Super**
  - 8-core ARM CPU
  - 1024 CUDA cores
  - 8GB RAM
  - NVMe storage (minimum 256GB recommended)
  - Cost: ~$500

#### Development Workstation
- **Recommended Specs:**
  - CPU: 8+ cores (Intel i7/i9 or AMD Ryzen 7/9)
  - GPU: NVIDIA RTX 3060 or better (for model training)
  - RAM: 32GB minimum, 64GB recommended
  - Storage: 1TB NVMe SSD
  - OS: Ubuntu 22.04 LTS

#### Network Infrastructure
- **EtherCAT Network:**
  - CAT5e or CAT6 shielded cables
  - Dedicated network interface for EtherCAT
  - 1kHz cycle time capability
  - Maximum segment length: 100m

### 1.2 Operating System Configuration

#### Jetson Orin Nano Setup

```bash
# Flash JetPack 5.1.2 or later
# Download from: https://developer.nvidia.com/embedded/jetpack

# Update system
sudo apt update && sudo apt upgrade -y

# Install PREEMPT_RT kernel for real-time performance
sudo apt install linux-rt-image-generic

# Configure CPU isolation for real-time tasks
# Edit /etc/default/grub
sudo nano /etc/default/grub
# Add: GRUB_CMDLINE_LINUX="isolcpus=4,5,6,7 nohz_full=4,5,6,7 rcu_nocbs=4,5,6,7"

# Update grub
sudo update-grub

# Reboot
sudo reboot
```

#### Real-Time Configuration

```bash
# Set CPU governor to performance
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Disable CPU frequency scaling
sudo systemctl disable ondemand

# Configure memory locking
sudo nano /etc/security/limits.conf
# Add:
# * soft memlock unlimited
# * hard memlock unlimited

# Set real-time priorities
sudo nano /etc/security/limits.conf
# Add:
# * soft rtprio 99
# * hard rtprio 99
```

### 1.3 Software Dependencies

#### Core System Libraries

```bash
# Install build essentials
sudo apt install -y build-essential cmake git pkg-config

# Install Python 3.10+
sudo apt install -y python3.10 python3.10-dev python3-pip

# Install real-time libraries
sudo apt install -y libc6-dev libpthread-stubs0-dev

# Install EtherCAT master (IgH EtherCAT Master)
cd /tmp
git clone https://gitlab.com/etherlab.org/ethercat.git
cd ethercat
./bootstrap
./configure --enable-cycles --enable-hrtimer --disable-8139too --disable-eoe
make
sudo make install
sudo depmod

# Configure EtherCAT master
sudo nano /etc/sysconfig/ethercat
# Set MASTER0_DEVICE to your network interface MAC address
# Set DEVICE_MODULES to "generic"

# Start EtherCAT service
sudo systemctl enable ethercat
sudo systemctl start ethercat
```

#### Python Environment

```bash
# Create virtual environment
python3 -m venv ~/kuka_ml_env
source ~/kuka_ml_env/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install PyTorch for Jetson (CUDA-enabled)
# Download from: https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
pip install torch-*.whl torchvision-*.whl

# Install ML/DL libraries
pip install numpy==1.24.3
pip install scipy==1.10.1
pip install scikit-learn==1.3.0
pip install opencv-python==4.8.0.74
pip install pillow==10.0.0

# Install robotics libraries
pip install transforms3d==0.4.1
pip install pyquaternion==1.0.0

# Install data handling
pip install h5py==3.9.0
pip install zarr==2.16.0
pip install pandas==2.0.3

# Install visualization
pip install matplotlib==3.7.2
pip install seaborn==0.12.2
pip install tensorboard==2.13.0

# Install ROS2 Humble (optional but recommended)
sudo apt install -y ros-humble-desktop
sudo apt install -y ros-humble-control-msgs
sudo apt install -y ros-humble-trajectory-msgs
```

#### TensorRT for Model Optimization

```bash
# TensorRT should be included in JetPack
# Verify installation
python3 -c "import tensorrt; print(tensorrt.__version__)"

# Install Python bindings
pip install pycuda==2022.2.2

# Install ONNX for model conversion
pip install onnx==1.14.0
pip install onnx-simplifier==0.4.33
```

#### Additional Development Tools

```bash
# Install debugging tools
sudo apt install -y gdb valgrind

# Install profiling tools
sudo apt install -y linux-tools-generic
pip install py-spy==0.3.14

# Install code quality tools
pip install black==23.7.0
pip install flake8==6.1.0
pip install mypy==1.5.0
pip install pytest==7.4.0
pip install pytest-cov==4.1.0

# Install documentation tools
pip install sphinx==7.1.2
pip install sphinx-rtd-theme==1.3.0
```

### 1.4 Development Tools Setup

#### Version Control

```bash
# Initialize git repository
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create .gitignore
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# Data
data/
datasets/
*.h5
*.zarr
*.bag

# Models
models/*.pth
models/*.onnx
models/*.trt
!models/.gitkeep

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp

# System
.DS_Store
EOF
```

#### IDE Configuration (VS Code)

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "~/kuka_ml_env/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

---

## Data Collection and Preprocessing

### 2.1 Teleoperation System for Data Collection

#### 2.1.1 Teleoperation Interface Design

**Objective:** Create a teleoperation system to collect demonstration data for imitation learning.

**Requirements:**
- Support multiple input devices (SpaceMouse, gamepad, follower arm)
- Real-time robot control at 60Hz
- Synchronized multi-camera recording
- Force/torque sensor data logging
- Emergency stop capability

**Implementation:**

```python
# src/teleoperation/teleop_controller.py

import numpy as np
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import threading

@dataclass
class TeleopConfig:
    """Configuration for teleoperation system."""
    control_frequency: float = 60.0  # Hz
    max_joint_velocity: float = 0.5  # rad/s
    max_cartesian_velocity: float = 0.1  # m/s
    deadzone: float = 0.05
    enable_force_feedback: bool = True
    safety_limits_enabled: bool = True

class TeleopController:
    """Main teleoperation controller for data collection."""
    
    def __init__(self, config: TeleopConfig, robot_interface):
        self.config = config
        self.robot = robot_interface
        self.running = False
        self.emergency_stop = False
        
        # Control loop timing
        self.dt = 1.0 / config.control_frequency
        
        # Data buffers
        self.observation_buffer = []
        self.action_buffer = []
        
    def start(self):
        """Start teleoperation control loop."""
        self.running = True
        self.emergency_stop = False
        
        control_thread = threading.Thread(target=self._control_loop)
        control_thread.start()
        
    def stop(self):
        """Stop teleoperation."""
        self.running = False
        
    def _control_loop(self):
        """Main control loop running at specified frequency."""
        while self.running and not self.emergency_stop:
            start_time = time.time()
            
            # Read input device
            raw_input = self._read_input_device()
            
            # Apply deadzone and scaling
            scaled_input = self._apply_deadzone(raw_input)
            
            # Convert to robot commands
            robot_command = self._input_to_command(scaled_input)
            
            # Safety checks
            if not self._safety_check(robot_command):
                self.emergency_stop = True
                self.robot.stop()
                break
            
            # Send command to robot
            self.robot.send_command(robot_command)
            
            # Record observation and action
            observation = self._get_observation()
            self.observation_buffer.append(observation)
            self.action_buffer.append(robot_command)
            
            # Maintain control frequency
            elapsed = time.time() - start_time
            if elapsed < self.dt:
                time.sleep(self.dt - elapsed)
                
    def _read_input_device(self) -> np.ndarray:
        """Read from input device (implement based on device type)."""
        # TODO: Implement for specific device (SpaceMouse, gamepad, etc.)
        pass
        
    def _apply_deadzone(self, raw_input: np.ndarray) -> np.ndarray:
        """Apply deadzone to input."""
        output = raw_input.copy()
        mask = np.abs(output) < self.config.deadzone
        output[mask] = 0.0
        return output
        
    def _input_to_command(self, scaled_input: np.ndarray) -> Dict:
        """Convert input to robot command."""
        # Scale to velocity limits
        joint_velocities = scaled_input * self.config.max_joint_velocity
        
        return {
            'joint_velocities': joint_velocities,
            'timestamp': time.time()
        }
        
    def _safety_check(self, command: Dict) -> bool:
        """Verify command is safe to execute."""
        if not self.config.safety_limits_enabled:
            return True
            
        # Check velocity limits
        velocities = command['joint_velocities']
        if np.any(np.abs(velocities) > self.config.max_joint_velocity):
            return False
            
        # Check joint limits
        current_positions = self.robot.get_joint_positions()
        predicted_positions = current_positions + velocities * self.dt
        
        if not self.robot.check_joint_limits(predicted_positions):
            return False
            
        return True
        
    def _get_observation(self) -> Dict:
        """Collect current observation from all sensors."""
        return {
            'joint_positions': self.robot.get_joint_positions(),
            'joint_velocities': self.robot.get_joint_velocities(),
            'camera_images': self.robot.get_camera_images(),
            'force_torque': self.robot.get_force_torque(),
            'timestamp': time.time()
        }
        
    def save_demonstration(self, filename: str):
        """Save collected demonstration to file."""
        import h5py
        
        with h5py.File(filename, 'w') as f:
            # Save observations
            obs_group = f.create_group('observations')
            
            # Stack all observations
            joint_pos = np.array([obs['joint_positions'] for obs in self.observation_buffer])
            joint_vel = np.array([obs['joint_velocities'] for obs in self.observation_buffer])
            timestamps = np.array([obs['timestamp'] for obs in self.observation_buffer])
            
            obs_group.create_dataset('joint_positions', data=joint_pos)
            obs_group.create_dataset('joint_velocities', data=joint_vel)
            obs_group.create_dataset('timestamps', data=timestamps)
            
            # Save actions
            actions = np.array([act['joint_velocities'] for act in self.action_buffer])
            f.create_dataset('actions', data=actions)
            
            # Save metadata
            f.attrs['duration'] = timestamps[-1] - timestamps[0]
            f.attrs['num_steps'] = len(self.observation_buffer)
            f.attrs['control_frequency'] = self.config.control_frequency
```

#### 2.1.2 Multi-Camera Synchronization

**Objective:** Synchronize multiple camera feeds for consistent observation data.

**Requirements:**
- 3-5 RGB cameras at 1920x1080 @ 60fps
- 1 depth camera (Intel RealSense D435)
- Hardware-triggered synchronization
- Timestamp alignment

**Implementation:**

```python
# src/sensors/camera_manager.py

import cv2
import numpy as np
import pyrealsense2 as rs
from typing import List, Dict, Tuple
import threading
import queue

class CameraManager:
    """Manages multiple synchronized cameras."""
    
    def __init__(self, camera_configs: List[Dict]):
        self.cameras = []
        self.camera_configs = camera_configs
        self.frame_queue = queue.Queue(maxsize=10)
        self.running = False
        
        # Initialize cameras
        for config in camera_configs:
            if config['type'] == 'rgb':
                cam = self._init_rgb_camera(config)
            elif config['type'] == 'depth':
                cam = self._init_depth_camera(config)
            else:
                raise ValueError(f"Unknown camera type: {config['type']}")
            self.cameras.append(cam)
            
    def _init_rgb_camera(self, config: Dict) -> cv2.VideoCapture:
        """Initialize RGB camera."""
        cap = cv2.VideoCapture(config['device_id'])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['width'])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['height'])
        cap.set(cv2.CAP_PROP_FPS, config['fps'])
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        return cap
        
    def _init_depth_camera(self, config: Dict) -> rs.pipeline:
        """Initialize RealSense depth camera."""
        pipeline = rs.pipeline()
        rs_config = rs.config()
        
        rs_config.enable_stream(
            rs.stream.depth,
            config['width'],
            config['height'],
            rs.format.z16,
            config['fps']
        )
        rs_config.enable_stream(
            rs.stream.color,
            config['width'],
            config['height'],
            rs.format.bgr8,
            config['fps']
        )
        
        pipeline.start(rs_config)
        return pipeline
        
    def start_capture(self):
        """Start capturing from all cameras."""
        self.running = True
        capture_thread = threading.Thread(target=self._capture_loop)
        capture_thread.start()
        
    def stop_capture(self):
        """Stop capturing."""
        self.running = False
        
    def _capture_loop(self):
        """Main capture loop."""
        while self.running:
            timestamp = time.time()
            frames = {}
            
            # Capture from all cameras
            for i, (cam, config) in enumerate(zip(self.cameras, self.camera_configs)):
                if config['type'] == 'rgb':
                    ret, frame = cam.read()
                    if ret:
                        frames[f"camera_{i}"] = frame
                elif config['type'] == 'depth':
                    frameset = cam.wait_for_frames()
                    color_frame = frameset.get_color_frame()
                    depth_frame = frameset.get_depth_frame()
                    
                    if color_frame and depth_frame:
                        frames[f"camera_{i}_color"] = np.asanyarray(color_frame.get_data())
                        frames[f"camera_{i}_depth"] = np.asanyarray(depth_frame.get_data())
            
            # Add timestamp and queue
            frames['timestamp'] = timestamp
            
            try:
                self.frame_queue.put(frames, block=False)
            except queue.Full:
                # Drop oldest frame
                self.frame_queue.get()
                self.frame_queue.put(frames)
                
    def get_latest_frames(self) -> Dict:
        """Get latest synchronized frames."""
        try:
            return self.frame_queue.get(timeout=0.1)
        except queue.Empty:
            return None
            
    def calibrate_cameras(self) -> Dict:
        """Perform camera calibration for intrinsic and extrinsic parameters."""
        # TODO: Implement camera calibration using checkerboard or ArUco markers
        pass
```

### 2.2 Data Storage and Management

#### 2.2.1 Dataset Structure

**Objective:** Define efficient data storage format for large-scale demonstration datasets.

**Format:** HDF5 with Zarr for large arrays

**Structure:**
```
dataset/
├── episode_0000.h5
│   ├── observations/
│   │   ├── camera_0_rgb          [T, H, W, 3] uint8
│   │   ├── camera_1_rgb          [T, H, W, 3] uint8
│   │   ├── camera_2_rgb          [T, H, W, 3] uint8
│   │   ├── depth_camera_rgb      [T, H, W, 3] uint8
│   │   ├── depth_camera_depth    [T, H, W] uint16
│   │   ├── joint_positions       [T, 6] float32
│   │   ├── joint_velocities      [T, 6] float32
│   │   ├── force_torque          [T, 6] float32
│   │   └── timestamps            [T] float64
│   ├── actions/
│   │   ├── joint_positions       [T, 6] float32
│   │   └── joint_velocities      [T, 6] float32
│   └── metadata/
│       ├── task_description      string
│       ├── success               bool
│       ├── duration              float
│       └── operator_id           string
├── episode_0001.h5
└── ...
```

**Implementation:**

```python
# src/data/dataset_manager.py

import h5py
import zarr
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class DatasetConfig:
    """Configuration for dataset storage."""
    root_dir: str
    compression: str = 'gzip'
    compression_level: int = 4
    chunk_size: int = 100
    image_format: str = 'jpeg'  # 'jpeg' or 'png'
    image_quality: int = 95

class DatasetManager:
    """Manages demonstration dataset storage and retrieval."""
    
    def __init__(self, config: DatasetConfig):
        self.config = config
        self.root_dir = Path(config.root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)
        
        # Create metadata file
        self.metadata_file = self.root_dir / 'dataset_metadata.json'
        if not self.metadata_file.exists():
            self._init_metadata()
            
    def _init_metadata(self):
        """Initialize dataset metadata."""
        metadata = {
            'version': '1.0',
            'num_episodes': 0,
            'total_steps': 0,
            'tasks': [],
            'camera_configs': [],
            'robot_config': {}
        }
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    def save_episode(self, 
                     observations: Dict[str, np.ndarray],
                     actions: Dict[str, np.ndarray],
                     metadata: Dict) -> str:
        """Save a single episode to dataset."""
        
        # Load current metadata
        with open(self.metadata_file, 'r') as f:
            dataset_meta = json.load(f)
            
        episode_id = dataset_meta['num_episodes']
        episode_file = self.root_dir / f'episode_{episode_id:06d}.h5'
        
        with h5py.File(episode_file, 'w') as f:
            # Save observations
            obs_group = f.create_group('observations')
            for key, value in observations.items():
                if 'camera' in key and 'rgb' in key:
                    # Compress images
                    obs_group.create_dataset(
                        key,
                        data=value,
                        compression=self.config.compression,
                        compression_opts=self.config.compression_level,
                        chunks=(1, value.shape[1], value.shape[2], value.shape[3])
                    )
                else:
                    obs_group.create_dataset(key, data=value)
                    
            # Save actions
            act_group = f.create_group('actions')
            for key, value in actions.items():
                act_group.create_dataset(key, data=value)
                
            # Save metadata
            meta_group = f.create_group('metadata')
            for key, value in metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    meta_group.attrs[key] = value
                    
        # Update dataset metadata
        dataset_meta['num_episodes'] += 1
        dataset_meta['total_steps'] += len(observations['timestamps'])
        if metadata.get('task_description') not in dataset_meta['tasks']:
            dataset_meta['tasks'].append(metadata.get('task_description'))
            
        with open(self.metadata_file, 'w') as f:
            json.dump(dataset_meta, f, indent=2)
            
        return str(episode_file)
        
    def load_episode(self, episode_id: int) -> Dict:
        """Load a single episode from dataset."""
        episode_file = self.root_dir / f'episode_{episode_id:06d}.h5'
        
        if not episode_file.exists():
            raise FileNotFoundError(f"Episode {episode_id} not found")
            
        with h5py.File(episode_file, 'r') as f:
            # Load observations
            observations = {}
            for key in f['observations'].keys():
                observations[key] = f['observations'][key][:]
                
            # Load actions
            actions = {}
            for key in f['actions'].keys():
                actions[key] = f['actions'][key][:]
                
            # Load metadata
            metadata = dict(f['metadata'].attrs)
            
        return {
            'observations': observations,
            'actions': actions,
            'metadata': metadata
        }
        
    def get_dataset_stats(self) -> Dict:
        """Get statistics about the dataset."""
        with open(self.metadata_file, 'r') as f:
            metadata = json.load(f)
            
        return {
            'num_episodes': metadata['num_episodes'],
            'total_steps': metadata['total_steps'],
            'tasks': metadata['tasks'],
            'avg_episode_length': metadata['total_steps'] / max(metadata['num_episodes'], 1)
        }
```

#### 2.2.2 Data Preprocessing Pipeline

**Objective:** Preprocess raw sensor data for ML model training.

**Requirements:**
- Image normalization and resizing
- Joint position/velocity normalization
- Data augmentation
- Temporal alignment

**Implementation:**

```python
# src/data/preprocessing.py

import numpy as np
import cv2
from typing import Dict, Tuple, Optional
import torch
from torchvision import transforms

class DataPreprocessor:
    """Preprocesses raw sensor data for ML training."""
    
    def __init__(self, 
                 image_size: Tuple[int, int] = (224, 224),
                 joint_limits: Optional[np.ndarray] = None,
                 augmentation: bool = True):
        self.image_size = image_size
        self.joint_limits = joint_limits
        self.augmentation = augmentation
        
        # Image transforms
        self.image_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Augmentation transforms
        if augmentation:
            self.augment_transform = transforms.Compose([
                transforms.ToPILImage(),
                transforms.Resize(image_size),
                transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
                transforms.RandomRotation(5),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                   std=[0.229, 0.224, 0.225])
            ])
            
    def preprocess_observation(self, 
                               observation: Dict,
                               augment: bool = False) -> Dict:
        """Preprocess a single observation."""
        processed = {}
        
        # Process images
        for key, value in observation.items():
            if 'camera' in key and 'rgb' in key:
                if augment and self.augmentation:
                    processed[key] = self.augment_transform(value)
                else:
                    processed[key] = self.image_transform(value)
            elif 'joint_positions' in key:
                # Normalize joint positions to [-1, 1]
                if self.joint_limits is not None:
                    normalized = 2.0 * (value - self.joint_limits[:, 0]) / \
                                (self.joint_limits[:, 1] - self.joint_limits[:, 0]) - 1.0
                    processed[key] = torch.tensor(normalized, dtype=torch.float32)
                else:
                    processed[key] = torch.tensor(value, dtype=torch.float32)
            elif 'joint_velocities' in key or 'force_torque' in key:
                processed[key] = torch.tensor(value, dtype=torch.float32)
                
        return processed
        
    def preprocess_action(self, action: np.ndarray) -> torch.Tensor:
        """Preprocess action data."""
        # Normalize actions if joint limits provided
        if self.joint_limits is not None:
            normalized = 2.0 * (action - self.joint_limits[:, 0]) / \
                        (self.joint_limits[:, 1] - self.joint_limits[:, 0]) - 1.0
            return torch.tensor(normalized, dtype=torch.float32)
        else:
            return torch.tensor(action, dtype=torch.float32)
            
    def denormalize_action(self, action: torch.Tensor) -> np.ndarray:
        """Denormalize action back to joint space."""
        if self.joint_limits is not None:
            action_np = action.cpu().numpy()
            denormalized = (action_np + 1.0) / 2.0 * \
                          (self.joint_limits[:, 1] - self.joint_limits[:, 0]) + \
                          self.joint_limits[:, 0]
            return denormalized
        else:
            return action.cpu().numpy()
```

### 2.3 Data Augmentation Strategies

**Objective:** Increase dataset diversity and model robustness through augmentation.

**Techniques:**
- Image augmentations (color jitter, rotation, cropping)
- Noise addition to joint positions (±5% of range)
- Time-warping trajectories (±10% speed variation)
- Synthetic viewpoints

**Implementation:**

```python
# src/data/augmentation.py

import numpy as np
import cv2
from typing import Dict, Tuple
import random

class DataAugmenter:
    """Applies data augmentation to demonstrations."""
    
    def __init__(self, config: Dict):
        self.config = config
        
    def augment_episode(self, episode: Dict) -> Dict:
        """Apply augmentation to entire episode."""
        augmented = {
            'observations': {},
            'actions': episode['actions'].copy(),
            'metadata': episode['metadata'].copy()
        }
        
        # Time warping
        if self.config.get('time_warp', False):
            episode = self._time_warp(episode)
            
        # Image augmentation
        for key, value in episode['observations'].items():
            if 'camera' in key and 'rgb' in key:
                augmented['observations'][key] = self._augment_images(value)
            else:
                augmented['observations'][key] = value.copy()
                
        # Joint noise
        if 'joint_positions' in episode['observations']:
            augmented['observations']['joint_positions'] = self._add_joint_noise(
                episode['observations']['joint_positions']
            )
            
        return augmented
        
    def _time_warp(self, episode: Dict, warp_factor: float = 0.1) -> Dict:
        """Apply time warping to trajectory."""
        # Random speed variation
        speed_factor = 1.0 + random.uniform(-warp_factor, warp_factor)
        
        # Resample trajectory
        original_length = len(episode['observations']['timestamps'])
        new_length = int(original_length * speed_factor)
        
        warped = {'observations': {}, 'actions': {}, 'metadata': episode['metadata']}
        
        for key, value in episode['observations'].items():
            if len(value.shape) == 1:
                warped['observations'][key] = np.interp(
                    np.linspace(0, original_length-1, new_length),
                    np.arange(original_length),
                    value
                )
            else:
                # For multi-dimensional arrays
                warped['observations'][key] = np.array([
                    np.interp(
                        np.linspace(0, original_length-1, new_length),
                        np.arange(original_length),
                        value[:, i]
                    ) for i in range(value.shape[1])
                ]).T
                
        # Resample actions similarly
        for key, value in episode['actions'].items():
            warped['actions'][key] = np.array([
                np.interp(
                    np.linspace(0, original_length-1, new_length),
                    np.arange(original_length),
                    value[:, i]
                ) for i in range(value.shape[1])
            ]).T
            
        return warped
        
    def _augment_images(self, images: np.ndarray) -> np.ndarray:
        """Apply image augmentation."""
        augmented = []
        
        for img in images:
            # Color jitter
            if random.random() < 0.5:
                img = self._color_jitter(img)
                
            # Random crop and resize
            if random.random() < 0.3:
                img = self._random_crop(img)
                
            # Gaussian noise
            if random.random() < 0.2:
                img = self._add_gaussian_noise(img)
                
            augmented.append(img)
            
        return np.array(augmented)
        
    def _color_jitter(self, img: np.ndarray) -> np.ndarray:
        """Apply color jitter."""
        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Adjust hue, saturation, value
        hsv[:, :, 0] += random.uniform(-10, 10)
        hsv[:, :, 1] *= random.uniform(0.8, 1.2)
        hsv[:, :, 2] *= random.uniform(0.8, 1.2)
        
        # Clip and convert back
        hsv = np.clip(hsv, 0, 255).astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
    def _random_crop(self, img: np.ndarray, crop_ratio: float = 0.9) -> np.ndarray:
        """Apply random crop and resize."""
        h, w = img.shape[:2]
        new_h, new_w = int(h * crop_ratio), int(w * crop_ratio)
        
        top = random.randint(0, h - new_h)
        left = random.randint(0, w - new_w)
        
        cropped = img[top:top+new_h, left:left+new_w]
        return cv2.resize(cropped, (w, h))
        
    def _add_gaussian_noise(self, img: np.ndarray, sigma: float = 5.0) -> np.ndarray:
        """Add Gaussian noise to image."""
        noise = np.random.normal(0, sigma, img.shape)
        noisy = img.astype(np.float32) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)
        
    def _add_joint_noise(self, joint_positions: np.ndarray, noise_ratio: float = 0.05) -> np.ndarray:
        """Add noise to joint positions."""
        noise = np.random.normal(0, noise_ratio, joint_positions.shape)
        return joint_positions + noise * np.ptp(joint_positions, axis=0)
```

---

## ML Model Development

### 3.1 Model Architectures

#### 3.1.1 Behavioral Cloning (BC) - Baseline

**Objective:** Implement baseline imitation learning model.

**Architecture:**
- Vision encoder: ResNet-18 or EfficientNet-B0
- Proprioception encoder: MLP
- Fusion layer: Concatenation + MLP
- Action decoder: MLP

**Implementation:**

```python
# src/models/behavioral_cloning.py

import torch
import torch.nn as nn
import torchvision.models as models
from typing import Dict, Tuple

class BehavioralCloningModel(nn.Module):
    """Baseline behavioral cloning model."""
    
    def __init__(self,
                 num_cameras: int = 3,
                 image_size: Tuple[int, int] = (224, 224),
                 proprioception_dim: int = 12,  # 6 positions + 6 velocities
                 action_dim: int = 6,
                 hidden_dim: int = 256):
        super().__init__()
        
        self.num_cameras = num_cameras
        self.action_dim = action_dim
        
        # Vision encoder (shared across cameras)
        resnet = models.resnet18(pretrained=True)
        self.vision_encoder = nn.Sequential(*list(resnet.children())[:-1])
        vision_feature_dim = 512
        
        # Freeze early layers
        for param in list(self.vision_encoder.parameters())[:-10]:
            param.requires_grad = False
            
        # Proprioception encoder
        self.proprio_encoder = nn.Sequential(
            nn.Linear(proprioception_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # Fusion network
        fusion_input_dim = vision_feature_dim * num_cameras + hidden_dim
        self.fusion_network = nn.Sequential(
            nn.Linear(fusion_input_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1)
        )
        
        # Action decoder
        self.action_decoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # Output in [-1, 1]
        )
        
    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Forward pass."""
        batch_size = observations['joint_positions'].shape[0]
        
        # Encode images from all cameras
        vision_features = []
        for i in range(self.num_cameras):
            img = observations[f'camera_{i}_rgb']
            feat = self.vision_encoder(img)
            feat = feat.view(batch_size, -1)
            vision_features.append(feat)
        vision_features = torch.cat(vision_features, dim=1)
        
        # Encode proprioception
        proprio = torch.cat([
            observations['joint_positions'],
            observations['joint_velocities']
        ], dim=1)
        proprio_features = self.proprio_encoder(proprio)
        
        # Fuse features
        fused = torch.cat([vision_features, proprio_features], dim=1)
        fused_features = self.fusion_network(fused)
        
        # Decode action
        action = self.action_decoder(fused_features)
        
        return action
        
    def compute_loss(self, 
                     predictions: torch.Tensor,
                     targets: torch.Tensor) -> torch.Tensor:
        """Compute MSE loss."""
        return nn.functional.mse_loss(predictions, targets)
```

#### 3.1.2 Action Chunking Transformer (ACT)

**Objective:** Implement ACT model for temporal consistency.

**Architecture:**
- Vision encoder: ResNet-18
- Transformer encoder for observations
- Transformer decoder for action sequences
- Predicts 10-step action chunks

**Implementation:**

```python
# src/models/act_model.py

import torch
import torch.nn as nn
import torchvision.models as models
from typing import Dict, Tuple
import math

class PositionalEncoding(nn.Module):
    """Positional encoding for transformer."""
    
    def __init__(self, d_model: int, max_len: int = 5000):
        super().__init__()
        
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        
        self.register_buffer('pe', pe)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Add positional encoding."""
        return x + self.pe[:x.size(0)]

class ACTModel(nn.Module):
    """Action Chunking Transformer model."""
    
    def __init__(self,
                 num_cameras: int = 3,
                 image_size: Tuple[int, int] = (224, 224),
                 proprioception_dim: int = 12,
                 action_dim: int = 6,
                 chunk_size: int = 10,
                 hidden_dim: int = 256,
                 num_encoder_layers: int = 4,
                 num_decoder_layers: int = 4,
                 num_heads: int = 8,
                 dropout: float = 0.1):
        super().__init__()
        
        self.num_cameras = num_cameras
        self.action_dim = action_dim
        self.chunk_size = chunk_size
        self.hidden_dim = hidden_dim
        
        # Vision encoder
        resnet = models.resnet18(pretrained=True)
        self.vision_encoder = nn.Sequential(*list(resnet.children())[:-1])
        vision_feature_dim = 512
        
        # Project vision features
        self.vision_proj = nn.Linear(vision_feature_dim * num_cameras, hidden_dim)
        
        # Proprioception encoder
        self.proprio_encoder = nn.Linear(proprioception_dim, hidden_dim)
        
        # Positional encoding
        self.pos_encoder = PositionalEncoding(hidden_dim)
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim * 4,
            dropout=dropout,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_encoder_layers
        )
        
        # Transformer decoder
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim * 4,
            dropout=dropout,
            batch_first=True
        )
        self.transformer_decoder = nn.TransformerDecoder(
            decoder_layer,
            num_layers=num_decoder_layers
        )
        
        # Action queries (learnable)
        self.action_queries = nn.Parameter(torch.randn(chunk_size, hidden_dim))
        
        # Action head
        self.action_head = nn.Linear(hidden_dim, action_dim)
        
    def forward(self, 
                observations: Dict[str, torch.Tensor],
                observation_history: int = 10) -> torch.Tensor:
        """
        Forward pass.
        
        Args:
            observations: Dict with keys:
                - camera_*_rgb: [B, T, C, H, W]
                - joint_positions: [B, T, 6]
                - joint_velocities: [B, T, 6]
            observation_history: Number of past observations to use
            
        Returns:
            actions: [B, chunk_size, action_dim]
        """
        batch_size = observations['joint_positions'].shape[0]
        seq_len = observations['joint_positions'].shape[1]
        
        # Encode observations over time
        encoded_obs = []
        for t in range(seq_len):
            # Encode images
            vision_features = []
            for i in range(self.num_cameras):
                img = observations[f'camera_{i}_rgb'][:, t]
                feat = self.vision_encoder(img)
                feat = feat.view(batch_size, -1)
                vision_features.append(feat)
            vision_feat = torch.cat(vision_features, dim=1)
            vision_feat = self.vision_proj(vision_feat)
            
            # Encode proprioception
            proprio = torch.cat([
                observations['joint_positions'][:, t],
                observations['joint_velocities'][:, t]
            ], dim=1)
            proprio_feat = self.proprio_encoder(proprio)
            
            # Combine
            obs_feat = vision_feat + proprio_feat
            encoded_obs.append(obs_feat)
            
        # Stack observations: [B, T, hidden_dim]
        encoded_obs = torch.stack(encoded_obs, dim=1)
        
        # Add positional encoding
        encoded_obs = self.pos_encoder(encoded_obs.transpose(0, 1)).transpose(0, 1)
        
        # Transformer encoder
        memory = self.transformer_encoder(encoded_obs)
        
        # Prepare action queries
        action_queries = self.action_queries.unsqueeze(0).expand(batch_size, -1, -1)
        
        # Transformer decoder
        decoded = self.transformer_decoder(action_queries, memory)
        
        # Predict actions
        actions = self.action_head(decoded)
        actions = torch.tanh(actions)
        
        return actions
        
    def compute_loss(self,
                     predictions: torch.Tensor,
                     targets: torch.Tensor) -> torch.Tensor:
        """
        Compute loss for action chunks.
        
        Args:
            predictions: [B, chunk_size, action_dim]
            targets: [B, chunk_size, action_dim]
        """
        return nn.functional.mse_loss(predictions, targets)
```

#### 3.1.3 Diffusion Policy

**Objective:** Implement diffusion-based policy for robust action generation.

**Architecture:**
- Vision encoder: ResNet-18
- Diffusion model: U-Net for denoising
- Conditional on observations
- Iterative denoising process

**Implementation:**

```python
# src/models/diffusion_policy.py

import torch
import torch.nn as nn
import torchvision.models as models
from typing import Dict, Tuple
import numpy as np

class SinusoidalPositionEmbeddings(nn.Module):
    """Sinusoidal position embeddings for diffusion timesteps."""
    
    def __init__(self, dim: int):
        super().__init__()
        self.dim = dim
        
    def forward(self, time: torch.Tensor) -> torch.Tensor:
        device = time.device
        half_dim = self.dim // 2
        embeddings = math.log(10000) / (half_dim - 1)
        embeddings = torch.exp(torch.arange(half_dim, device=device) * -embeddings)
        embeddings = time[:, None] * embeddings[None, :]
        embeddings = torch.cat((embeddings.sin(), embeddings.cos()), dim=-1)
        return embeddings

class DiffusionUNet(nn.Module):
    """U-Net for diffusion denoising."""
    
    def __init__(self,
                 action_dim: int,
                 condition_dim: int,
                 hidden_dim: int = 256,
                 time_embed_dim: int = 128):
        super().__init__()
        
        self.action_dim = action_dim
        
        # Time embedding
        self.time_mlp = nn.Sequential(
            SinusoidalPositionEmbeddings(time_embed_dim),
            nn.Linear(time_embed_dim, time_embed_dim * 2),
            nn.GELU(),
            nn.Linear(time_embed_dim * 2, time_embed_dim)
        )
        
        # Encoder
        self.encoder1 = nn.Sequential(
            nn.Linear(action_dim + condition_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        self.encoder2 = nn.Sequential(
            nn.Linear(hidden_dim + time_embed_dim, hidden_dim * 2),
            nn.GELU(),
            nn.Linear(hidden_dim * 2, hidden_dim * 2)
        )
        
        # Bottleneck
        self.bottleneck = nn.Sequential(
            nn.Linear(hidden_dim * 2 + time_embed_dim, hidden_dim * 2),
            nn.GELU(),
            nn.Linear(hidden_dim * 2, hidden_dim * 2)
        )
        
        # Decoder
        self.decoder2 = nn.Sequential(
            nn.Linear(hidden_dim * 4 + time_embed_dim, hidden_dim * 2),
            nn.GELU(),
            nn.Linear(hidden_dim * 2, hidden_dim)
        )
        
        self.decoder1 = nn.Sequential(
            nn.Linear(hidden_dim * 2 + time_embed_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, action_dim)
        )
        
    def forward(self,
                noisy_action: torch.Tensor,
                timestep: torch.Tensor,
                condition: torch.Tensor) -> torch.Tensor:
        """
        Denoise action given timestep and condition.
        
        Args:
            noisy_action: [B, action_dim]
            timestep: [B]
            condition: [B, condition_dim]
        """
        # Time embedding
        t_emb = self.time_mlp(timestep)
        
        # Encoder
        x = torch.cat([noisy_action, condition], dim=1)
        enc1 = self.encoder1(x)
        
        x = torch.cat([enc1, t_emb], dim=1)
        enc2 = self.encoder2(x)
        
        # Bottleneck
        x = torch.cat([enc2, t_emb], dim=1)
        bottleneck = self.bottleneck(x)
        
        # Decoder with skip connections
        x = torch.cat([bottleneck, enc2, t_emb], dim=1)
        dec2 = self.decoder2(x)
        
        x = torch.cat([dec2, enc1, t_emb], dim=1)
        output = self.decoder1(x)
        
        return output

class DiffusionPolicy(nn.Module):
    """Diffusion-based policy model."""
    
    def __init__(self,
                 num_cameras: int = 3,
                 proprioception_dim: int = 12,
                 action_dim: int = 6,
                 hidden_dim: int = 256,
                 num_diffusion_steps: int = 100):
        super().__init__()
        
        self.num_cameras = num_cameras
        self.action_dim = action_dim
        self.num_diffusion_steps = num_diffusion_steps
        
        # Vision encoder
        resnet = models.resnet18(pretrained=True)
        self.vision_encoder = nn.Sequential(*list(resnet.children())[:-1])
        vision_feature_dim = 512
        
        # Condition encoder
        condition_input_dim = vision_feature_dim * num_cameras + proprioception_dim
        self.condition_encoder = nn.Sequential(
            nn.Linear(condition_input_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # Diffusion U-Net
        self.unet = DiffusionUNet(
            action_dim=action_dim,
            condition_dim=hidden_dim,
            hidden_dim=hidden_dim
        )
        
        # Noise schedule (linear)
        self.register_buffer('betas', torch.linspace(0.0001, 0.02, num_diffusion_steps))
        self.register_buffer('alphas', 1.0 - self.betas)
        self.register_buffer('alphas_cumprod', torch.cumprod(self.alphas, dim=0))
        
    def encode_condition(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Encode observations into condition vector."""
        batch_size = observations['joint_positions'].shape[0]
        
        # Encode images
        vision_features = []
        for i in range(self.num_cameras):
            img = observations[f'camera_{i}_rgb']
            feat = self.vision_encoder(img)
            feat = feat.view(batch_size, -1)
            vision_features.append(feat)
        vision_feat = torch.cat(vision_features, dim=1)
        
        # Encode proprioception
        proprio = torch.cat([
            observations['joint_positions'],
            observations['joint_velocities']
        ], dim=1)
        
        # Combine and encode
        condition_input = torch.cat([vision_feat, proprio], dim=1)
        condition = self.condition_encoder(condition_input)
        
        return condition
        
    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Generate action through denoising process.
        
        Args:
            observations: Dict of observation tensors
            
        Returns:
            action: [B, action_dim]
        """
        batch_size = observations['joint_positions'].shape[0]
        device = observations['joint_positions'].device
        
        # Encode condition
        condition = self.encode_condition(observations)
        
        # Start from random noise
        action = torch.randn(batch_size, self.action_dim, device=device)
        
        # Iterative denoising
        for t in reversed(range(self.num_diffusion_steps)):
            timestep = torch.full((batch_size,), t, device=device, dtype=torch.long)
            
            # Predict noise
            predicted_noise = self.unet(action, timestep, condition)
            
            # Denoise
            alpha = self.alphas[t]
            alpha_cumprod = self.alphas_cumprod[t]
            beta = self.betas[t]
            
            if t > 0:
                noise = torch.randn_like(action)
            else:
                noise = torch.zeros_like(action)
                
            action = (1 / torch.sqrt(alpha)) * (
                action - (beta / torch.sqrt(1 - alpha_cumprod)) * predicted_noise
            ) + torch.sqrt(beta) * noise
            
        return torch.tanh(action)
        
    def compute_loss(self,
                     observations: Dict[str, torch.Tensor],
                     actions: torch.Tensor) -> torch.Tensor:
        """
        Compute diffusion training loss.
        
        Args:
            observations: Dict of observation tensors
            actions: [B, action_dim] ground truth actions
        """
        batch_size = actions.shape[0]
        device = actions.device
        
        # Encode condition
        condition = self.encode_condition(observations)
        
        # Sample random timestep
        t = torch.randint(0, self.num_diffusion_steps, (batch_size,), device=device)
        
        # Sample noise
        noise = torch.randn_like(actions)
        
        # Add noise to actions
        alpha_cumprod = self.alphas_cumprod[t].view(-1, 1)
        noisy_actions = torch.sqrt(alpha_cumprod) * actions + \
                       torch.sqrt(1 - alpha_cumprod) * noise
        
        # Predict noise
        predicted_noise = self.unet(noisy_actions, t, condition)
        
        # Compute loss
        loss = nn.functional.mse_loss(predicted_noise, noise)
        
        return loss
```

### 3.2 Training Pipeline

#### 3.2.1 Training Loop

**Objective:** Implement training loop with logging and checkpointing.

**Implementation:**

```python
# src/training/trainer.py

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from typing import Dict, Optional
from pathlib import Path
import time
from tqdm import tqdm

class Trainer:
    """Training pipeline for robot learning models."""
    
    def __init__(self,
                 model: nn.Module,
                 train_loader: DataLoader,
                 val_loader: DataLoader,
                 optimizer: torch.optim.Optimizer,
                 scheduler: Optional[torch.optim.lr_scheduler._LRScheduler] = None,
                 device: str = 'cuda',
                 log_dir: str = './logs',
                 checkpoint_dir: str = './checkpoints'):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = device
        
        # Logging
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.writer = SummaryWriter(log_dir)
        
        # Checkpointing
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        self.global_step = 0
        self.epoch = 0
        self.best_val_loss = float('inf')
        
    def train_epoch(self) -> Dict[str, float]:
        """Train for one epoch."""
        self.model.train()
        
        total_loss = 0.0
        num_batches = 0
        
        pbar = tqdm(self.train_loader, desc=f'Epoch {self.epoch}')
        for batch in pbar:
            # Move to device
            observations = {k: v.to(self.device) for k, v in batch['observations'].items()}
            actions = batch['actions'].to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            
            if hasattr(self.model, 'compute_loss'):
                # Model has custom loss computation
                loss = self.model.compute_loss(observations, actions)
            else:
                # Standard supervised learning
                predictions = self.model(observations)
                loss = nn.functional.mse_loss(predictions, actions)
            
            # Backward pass
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            self.optimizer.step()
            
            # Logging
            total_loss += loss.item()
            num_batches += 1
            
            self.writer.add_scalar('train/loss', loss.item(), self.global_step)
            self.writer.add_scalar('train/lr', self.optimizer.param_groups[0]['lr'], self.global_step)
            
            pbar.set_postfix({'loss': f'{loss.item():.4f}'})
            
            self.global_step += 1
            
        avg_loss = total_loss / num_batches
        return {'loss': avg_loss}
        
    def validate(self) -> Dict[str, float]:
        """Validate model."""
        self.model.eval()
        
        total_loss = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for batch in tqdm(self.val_loader, desc='Validation'):
                # Move to device
                observations = {k: v.to(self.device) for k, v in batch['observations'].items()}
                actions = batch['actions'].to(self.device)
                
                # Forward pass
                if hasattr(self.model, 'compute_loss'):
                    loss = self.model.compute_loss(observations, actions)
                else:
                    predictions = self.model(observations)
                    loss = nn.functional.mse_loss(predictions, actions)
                
                total_loss += loss.item()
                num_batches += 1
                
        avg_loss = total_loss / num_batches
        self.writer.add_scalar('val/loss', avg_loss, self.epoch)
        
        return {'loss': avg_loss}
        
    def train(self, num_epochs: int):
        """Train for multiple epochs."""
        for epoch in range(num_epochs):
            self.epoch = epoch
            
            # Train
            train_metrics = self.train_epoch()
            print(f"Epoch {epoch}: Train Loss = {train_metrics['loss']:.4f}")
            
            # Validate
            val_metrics = self.validate()
            print(f"Epoch {epoch}: Val Loss = {val_metrics['loss']:.4f}")
            
            # Learning rate scheduling
            if self.scheduler is not None:
                self.scheduler.step(val_metrics['loss'])
                
            # Save checkpoint
            self.save_checkpoint(val_metrics['loss'])
            
    def save_checkpoint(self, val_loss: float):
        """Save model checkpoint."""
        checkpoint = {
            'epoch': self.epoch,
            'global_step': self.global_step,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'val_loss': val_loss
        }
        
        if self.scheduler is not None:
            checkpoint['scheduler_state_dict'] = self.scheduler.state_dict()
            
        # Save latest
        torch.save(checkpoint, self.checkpoint_dir / 'latest.pth')
        
        # Save best
        if val_loss < self.best_val_loss:
            self.best_val_loss = val_loss
            torch.save(checkpoint, self.checkpoint_dir / 'best.pth')
            print(f"Saved best model with val_loss = {val_loss:.4f}")
            
    def load_checkpoint(self, checkpoint_path: str):
        """Load model checkpoint."""
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epoch = checkpoint['epoch']
        self.global_step = checkpoint['global_step']
        self.best_val_loss = checkpoint['val_loss']
        
        if self.scheduler is not None and 'scheduler_state_dict' in checkpoint:
            self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
            
        print(f"Loaded checkpoint from epoch {self.epoch}")
```

### 3.3 Model Optimization for Jetson

#### 3.3.1 TensorRT Conversion

**Objective:** Convert PyTorch models to TensorRT for optimized inference on Jetson.

**Implementation:**

```python
# src/deployment/tensorrt_converter.py

import torch
import torch.onnx
import tensorrt as trt
import numpy as np
from pathlib import Path
import pycuda.driver as cuda
import pycuda.autoinit

class TensorRTConverter:
    """Convert PyTorch models to TensorRT."""
    
    def __init__(self, precision: str = 'fp16'):
        """
        Args:
            precision: 'fp32', 'fp16', or 'int8'
        """
        self.precision = precision
        self.logger = trt.Logger(trt.Logger.WARNING)
        
    def convert(self,
                pytorch_model: torch.nn.Module,
                input_shapes: dict,
                output_path: str,
                onnx_path: Optional[str] = None):
        """
        Convert PyTorch model to TensorRT.
        
        Args:
            pytorch_model: PyTorch model
            input_shapes: Dict of input names to shapes
            output_path: Path to save TensorRT engine
            onnx_path: Optional path to save intermediate ONNX model
        """
        # Step 1: Export to ONNX
        if onnx_path is None:
            onnx_path = output_path.replace('.trt', '.onnx')
            
        self._export_onnx(pytorch_model, input_shapes, onnx_path)
        
        # Step 2: Build TensorRT engine
        self._build_engine(onnx_path, output_path)
        
    def _export_onnx(self,
                     model: torch.nn.Module,
                     input_shapes: dict,
                     onnx_path: str):
        """Export PyTorch model to ONNX."""
        model.eval()
        
        # Create dummy inputs
        dummy_inputs = {}
        for name, shape in input_shapes.items():
            dummy_inputs[name] = torch.randn(*shape).cuda()
            
        # Export
        torch.onnx.export(
            model,
            tuple(dummy_inputs.values()),
            onnx_path,
            export_params=True,
            opset_version=13,
            do_constant_folding=True,
            input_names=list(input_shapes.keys()),
            output_names=['output'],
            dynamic_axes={name: {0: 'batch_size'} for name in input_shapes.keys()}
        )
        
        print(f"Exported ONNX model to {onnx_path}")
        
    def _build_engine(self, onnx_path: str, engine_path: str):
        """Build TensorRT engine from ONNX."""
        builder = trt.Builder(self.logger)
        network = builder.create_network(
            1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
        )
        parser = trt.OnnxParser(network, self.logger)
        
        # Parse ONNX
        with open(onnx_path, 'rb') as f:
            if not parser.parse(f.read()):
                for error in range(parser.num_errors):
                    print(parser.get_error(error))
                raise RuntimeError("Failed to parse ONNX file")
                
        # Configure builder
        config = builder.create_builder_config()
        config.max_workspace_size = 1 << 30  # 1GB
        
        if self.precision == 'fp16':
            config.set_flag(trt.BuilderFlag.FP16)
        elif self.precision == 'int8':
            config.set_flag(trt.BuilderFlag.INT8)
            # TODO: Add INT8 calibration
            
        # Build engine
        print("Building TensorRT engine... This may take a while.")
        engine = builder.build_engine(network, config)
        
        if engine is None:
            raise RuntimeError("Failed to build TensorRT engine")
            
        # Save engine
        with open(engine_path, 'wb') as f:
            f.write(engine.serialize())
            
        print(f"Saved TensorRT engine to {engine_path}")
        
    def benchmark(self, engine_path: str, input_shapes: dict, num_iterations: int = 100):
        """Benchmark TensorRT engine."""
        # Load engine
        with open(engine_path, 'rb') as f:
            engine = trt.Runtime(self.logger).deserialize_cuda_engine(f.read())
            
        context = engine.create_execution_context()
        
        # Allocate buffers
        inputs = []
        outputs = []
        bindings = []
        
        for binding in engine:
            shape = engine.get_binding_shape(binding)
            size = trt.volume(shape)
            dtype = trt.nptype(engine.get_binding_dtype(binding))
            
            # Allocate host and device buffers
            host_mem = cuda.pagelocked_empty(size, dtype)
            device_mem = cuda.mem_alloc(host_mem.nbytes)
            
            bindings.append(int(device_mem))
            
            if engine.binding_is_input(binding):
                inputs.append({'host': host_mem, 'device': device_mem})
            else:
                outputs.append({'host': host_mem, 'device': device_mem})
                
        # Create stream
        stream = cuda.Stream()
        
        # Warm up
        for _ in range(10):
            context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
        stream.synchronize()
        
        # Benchmark
        import time
        start = time.time()
        
        for _ in range(num_iterations):
            context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
        stream.synchronize()
        
        end = time.time()
        
        avg_time = (end - start) / num_iterations * 1000  # ms
        print(f"Average inference time: {avg_time:.2f} ms")
        print(f"Throughput: {1000/avg_time:.2f} FPS")
        
        return avg_time
```

---

## Real-Time Control System Implementation

### 4.1 EtherCAT Communication

#### 4.1.1 EtherCAT Master Interface

**Objective:** Implement EtherCAT master for communication with servo drives.

**Requirements:**
- 1kHz cycle time
- PDO mapping for position, velocity, torque
- Watchdog monitoring
- Error handling

**Implementation:**

```python
# src/hardware/ethercat_master.py

import ctypes
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
import time

# Load EtherCAT library
ethercat_lib = ctypes.CDLL('/opt/etherlab/lib/libethercat.so')

@dataclass
class DriveConfig:
    """Configuration for a single servo drive."""
    address: int
    name: str
    max_position: float
    min_position: float
    max_velocity: float
    max_torque: float

class EtherCATMaster:
    """EtherCAT master for servo drive communication."""
    
    def __init__(self, drive_configs: List[DriveConfig], cycle_time_ns: int = 1000000):
        """
        Args:
            drive_configs: List of drive configurations
            cycle_time_ns: Cycle time in nanoseconds (default 1ms = 1000000ns)
        """
        self.drive_configs = drive_configs
        self.num_drives = len(drive_configs)
        self.cycle_time_ns = cycle_time_ns
        
        # Initialize master
        self.master = None
        self.domain = None
        self.domain_pd = None
        
        # Drive states
        self.drive_states = {}
        for config in drive_configs:
            self.drive_states[config.address] = {
                'position': 0.0,
                'velocity': 0.0,
                'torque': 0.0,
                'status': 0,
                'enabled': False
            }
            
    def initialize(self) -> bool:
        """Initialize EtherCAT master."""
        try:
            # Request master
            self.master = ethercat_lib.ecrt_request_master(0)
            if not self.master:
                print("Failed to request EtherCAT master")
                return False
                
            # Create domain
            self.domain = ethercat_lib.ecrt_master_create_domain(self.master)
            if not self.domain:
                print("Failed to create domain")
                return False
                
            # Configure slaves
            for config in self.drive_configs:
                self._configure_slave(config)
                
            # Activate master
            if ethercat_lib.ecrt_master_activate(self.master) < 0:
                print("Failed to activate master")
                return False
                
            # Get domain process data
            self.domain_pd = ethercat_lib.ecrt_domain_data(self.domain)
            
            print("EtherCAT master initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing EtherCAT master: {e}")
            return False
            
    def _configure_slave(self, config: DriveConfig):
        """Configure a single slave drive."""
        # This is a simplified example
        # Actual implementation depends on specific drive vendor and model
        
        # Configure PDOs (Process Data Objects)
        # Output PDOs (Master -> Slave)
        # - Control Word (0x6040)
        # - Target Position (0x607A)
        # - Target Velocity (0x60FF)
        # - Target Torque (0x6071)
        
        # Input PDOs (Slave -> Master)
        # - Status Word (0x6041)
        # - Actual Position (0x6064)
        # - Actual Velocity (0x606C)
        # - Actual Torque (0x6077)
        
        pass
        
    def send_commands(self, commands: Dict[int, Dict]):
        """
        Send commands to drives.
        
        Args:
            commands: Dict mapping drive address to command dict with keys:
                - target_position: float
                - target_velocity: float
                - target_torque: float
                - control_word: int
        """
        # Receive process data
        ethercat_lib.ecrt_master_receive(self.master)
        ethercat_lib.ecrt_domain_process(self.domain)
        
        # Write commands to process data
        for address, command in commands.items():
            # Write to PDO memory
            # This is simplified - actual implementation uses offset calculations
            pass
            
        # Send process data
        ethercat_lib.ecrt_domain_queue(self.domain)
        ethercat_lib.ecrt_master_send(self.master)
        
    def read_states(self) -> Dict[int, Dict]:
        """Read current states from all drives."""
        # Receive process data
        ethercat_lib.ecrt_master_receive(self.master)
        ethercat_lib.ecrt_domain_process(self.domain)
        
        # Read from process data
        for config in self.drive_configs:
            # Read from PDO memory
            # This is simplified - actual implementation uses offset calculations
            pass
            
        return self.drive_states
        
    def enable_drives(self):
        """Enable all drives."""
        commands = {}
        for config in self.drive_configs:
            commands[config.address] = {
                'control_word': 0x000F,  # Enable operation
                'target_position': 0.0,
                'target_velocity': 0.0,
                'target_torque': 0.0
            }
        self.send_commands(commands)
        
    def disable_drives(self):
        """Disable all drives."""
        commands = {}
        for config in self.drive_configs:
            commands[config.address] = {
                'control_word': 0x0006,  # Disable operation
                'target_position': 0.0,
                'target_velocity': 0.0,
                'target_torque': 0.0
            }
        self.send_commands(commands)
        
    def emergency_stop(self):
        """Trigger emergency stop."""
        commands = {}
        for config in self.drive_configs:
            commands[config.address] = {
                'control_word': 0x0002,  # Quick stop
                'target_position': 0.0,
                'target_velocity': 0.0,
                'target_torque': 0.0
            }
        self.send_commands(commands)
        
    def shutdown(self):
        """Shutdown EtherCAT master."""
        if self.master:
            self.disable_drives()
            ethercat_lib.ecrt_master_deactivate(self.master)
            ethercat_lib.ecrt_release_master(self.master)
            print("EtherCAT master shutdown")
```

### 4.2 Real-Time Control Loop

#### 4.2.1 Multi-Rate Control Architecture

**Objective:** Implement hierarchical control loops at different frequencies.

**Control Hierarchy:**
- Sensor acquisition: 60Hz
- ML inference: 100Hz
- Safety validation: 1kHz
- Low-level control: 1kHz
- Motor commands: 1kHz

**Implementation:**

```python
# src/control/realtime_controller.py

import threading
import time
import numpy as np
from typing import Dict, Optional, Callable
from dataclasses import dataclass
import ctypes

# Set real-time priority
libc = ctypes.CDLL('libc.so.6')

@dataclass
class ControlConfig:
    """Configuration for real-time control."""
    sensor_frequency: float = 60.0  # Hz
    ml_frequency: float = 100.0  # Hz
    control_frequency: float = 1000.0  # Hz
    safety_enabled: bool = True
    use_ml_control: bool = True

class RealtimeController:
    """Multi-rate real-time controller."""
    
    def __init__(self,
                 config: ControlConfig,
                 ethercat_master,
                 ml_model,
                 camera_manager,
                 safety_monitor):
        self.config = config
        self.ethercat = ethercat_master
        self.ml_model = ml_model
        self.cameras = camera_manager
        self.safety = safety_monitor
        
        # Control state
        self.running = False
        self.emergency_stop = False
        self.control_mode = 'idle'  # 'idle', 'ml', 'gcode', 'manual'
        
        # Timing
        self.sensor_dt = 1.0 / config.sensor_frequency
        self.ml_dt = 1.0 / config.ml_frequency
        self.control_dt = 1.0 / config.control_frequency
        
        # State buffers
        self.current_observation = None
        self.current_action = None
        self.joint_states = np.zeros(6)
        self.joint_velocities = np.zeros(6)
        
        # Action buffer for ACT model (10-step chunks)
        self.action_buffer = []
        self.action_buffer_index = 0
        
    def start(self):
        """Start real-time control."""
        self.running = True
        self.emergency_stop = False
        
        # Set real-time priority
        self._set_realtime_priority()
        
        # Start control threads
        sensor_thread = threading.Thread(target=self._sensor_loop, daemon=True)
        ml_thread = threading.Thread(target=self._ml_loop, daemon=True)
        control_thread = threading.Thread(target=self._control_loop, daemon=True)
        
        sensor_thread.start()
        ml_thread.start()
        control_thread.start()
        
        print("Real-time controller started")
        
    def stop(self):
        """Stop real-time control."""
        self.running = False
        self.ethercat.disable_drives()
        print("Real-time controller stopped")
        
    def _set_realtime_priority(self):
        """Set real-time scheduling priority."""
        # Set SCHED_FIFO with priority 80
        sched_param = ctypes.c_int(80)
        result = libc.sched_setscheduler(0, 1, ctypes.byref(sched_param))  # 1 = SCHED_FIFO
        if result == 0:
            print("Set real-time priority successfully")
        else:
            print("Warning: Failed to set real-time priority")
            
    def _sensor_loop(self):
        """Sensor acquisition loop at 60Hz."""
        while self.running:
            start_time = time.time()
            
            # Read joint states from EtherCAT
            drive_states = self.ethercat.read_states()
            self.joint_states = np.array([
                drive_states[addr]['position'] 
                for addr in sorted(drive_states.keys())
            ])
            self.joint_velocities = np.array([
                drive_states[addr]['velocity']
                for addr in sorted(drive_states.keys())
            ])
            
            # Capture camera images
            frames = self.cameras.get_latest_frames()
            
            # Update observation
            if frames is not None:
                self.current_observation = {
                    'joint_positions': self.joint_states.copy(),
                    'joint_velocities': self.joint_velocities.copy(),
                    'camera_images': frames,
                    'timestamp': time.time()
                }
                
            # Maintain frequency
            elapsed = time.time() - start_time
            if elapsed < self.sensor_dt:
                time.sleep(self.sensor_dt - elapsed)
                
    def _ml_loop(self):
        """ML inference loop at 100Hz."""
        while self.running:
            start_time = time.time()
            
            if self.control_mode == 'ml' and self.current_observation is not None:
                # Run ML inference
                action = self._run_ml_inference(self.current_observation)
                
                if action is not None:
                    self.current_action = action
                    
            # Maintain frequency
            elapsed = time.time() - start_time
            if elapsed < self.ml_dt:
                time.sleep(self.ml_dt - elapsed)
                
    def _control_loop(self):
        """Low-level control loop at 1kHz."""
        while self.running and not self.emergency_stop:
            start_time = time.time()
            
            # Get target action
            if self.control_mode == 'ml' and self.current_action is not None:
                target_action = self.current_action
            elif self.control_mode == 'gcode':
                target_action = self._get_gcode_action()
            elif self.control_mode == 'manual':
                target_action = self._get_manual_action()
            else:
                target_action = np.zeros(6)
                
            # Safety validation
            if self.config.safety_enabled:
                safe, reason = self.safety.validate_action(
                    target_action,
                    self.joint_states,
                    self.joint_velocities
                )
                
                if not safe:
                    print(f"Safety violation: {reason}")
                    self.emergency_stop = True
                    self.ethercat.emergency_stop()
                    break
                    
            # Compute motor commands
            commands = self._compute_motor_commands(target_action)
            
            # Send to EtherCAT
            self.ethercat.send_commands(commands)
            
            # Maintain frequency
            elapsed = time.time() - start_time
            if elapsed < self.control_dt:
                time.sleep(self.control_dt - elapsed)
            else:
                print(f"Warning: Control loop overrun by {(elapsed - self.control_dt)*1000:.2f}ms")
                
    def _run_ml_inference(self, observation: Dict) -> Optional[np.ndarray]:
        """Run ML model inference."""
        try:
            import torch
            
            # Preprocess observation
            # (Implementation depends on model type)
            
            # Run inference
            with torch.no_grad():
                action = self.ml_model(observation)
                
            return action.cpu().numpy()
            
        except Exception as e:
            print(f"ML inference error: {e}")
            return None
            
    def _compute_motor_commands(self, target_action: np.ndarray) -> Dict:
        """Compute motor commands from target action."""
        commands = {}
        
        for i, config in enumerate(self.ethercat.drive_configs):
            # Simple position control
            # In practice, this would include PID control, feedforward, etc.
            commands[config.address] = {
                'control_word': 0x000F,  # Enable operation
                'target_position': target_action[i],
                'target_velocity': 0.0,
                'target_torque': 0.0
            }
            
        return commands
        
    def _get_gcode_action(self) -> np.ndarray:
        """Get action from G-code interpreter."""
        # TODO: Implement G-code interpreter
        return np.zeros(6)
        
    def _get_manual_action(self) -> np.ndarray:
        """Get action from manual control."""
        # TODO: Implement manual control interface
        return np.zeros(6)
```

### 4.3 Kinematics and Trajectory Planning

#### 4.3.1 Forward and Inverse Kinematics

**Objective:** Implement kinematics for Kuka robot arm.

**Requirements:**
- Forward kinematics using DH parameters
- Inverse kinematics using numerical methods
- Singularity handling
- Joint limit checking

**Implementation:**

```python
# src/control/kinematics.py

import numpy as np
from scipy.optimize import minimize
from typing import Tuple, Optional
import transforms3d

class KukaKinematics:
    """Kinematics for Kuka robot arm."""
    
    def __init__(self, dh_params: np.ndarray, joint_limits: np.ndarray):
        """
        Args:
            dh_params: DH parameters [a, alpha, d, theta_offset] for each joint
            joint_limits: Joint limits [min, max] for each joint
        """
        self.dh_params = dh_params
        self.joint_limits = joint_limits
        self.num_joints = len(dh_params)
        
    def forward_kinematics(self, joint_angles: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute forward kinematics.
        
        Args:
            joint_angles: Joint angles [rad]
            
        Returns:
            position: End-effector position [x, y, z]
            orientation: End-effector orientation as rotation matrix
        """
        T = np.eye(4)
        
        for i, (a, alpha, d, theta_offset) in enumerate(self.dh_params):
            theta = joint_angles[i] + theta_offset
            
            # DH transformation matrix
            ct = np.cos(theta)
            st = np.sin(theta)
            ca = np.cos(alpha)
            sa = np.sin(alpha)
            
            T_i = np.array([
                [ct, -st*ca, st*sa, a*ct],
                [st, ct*ca, -ct*sa, a*st],
                [0, sa, ca, d],
                [0, 0, 0, 1]
            ])
            
            T = T @ T_i
            
        position = T[:3, 3]
        orientation = T[:3, :3]
        
        return position, orientation
        
    def inverse_kinematics(self,
                          target_position: np.ndarray,
                          target_orientation: np.ndarray,
                          initial_guess: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        """
        Compute inverse kinematics using numerical optimization.
        
        Args:
            target_position: Target position [x, y, z]
            target_orientation: Target orientation as rotation matrix
            initial_guess: Initial joint angles guess
            
        Returns:
            joint_angles: Joint angles [rad] or None if no solution found
        """
        if initial_guess is None:
            initial_guess = np.zeros(self.num_joints)
            
        def objective(q):
            pos, orient = self.forward_kinematics(q)
            
            # Position error
            pos_error = np.linalg.norm(pos - target_position)
            
            # Orientation error (Frobenius norm)
            orient_error = np.linalg.norm(orient - target_orientation, 'fro')
            
            return pos_error + 0.1 * orient_error
            
        def constraint(q):
            # Joint limits
            return np.concatenate([
                q - self.joint_limits[:, 0],
                self.joint_limits[:, 1] - q
            ])
            
        result = minimize(
            objective,
            initial_guess,
            method='SLSQP',
            constraints={'type': 'ineq', 'fun': constraint},
            options={'maxiter': 1000}
        )
        
        if result.success and objective(result.x) < 0.01:
            return result.x
        else:
            return None
            
    def jacobian(self, joint_angles: np.ndarray) -> np.ndarray:
        """
        Compute Jacobian matrix.
        
        Args:
            joint_angles: Joint angles [rad]
            
        Returns:
            J: Jacobian matrix [6, num_joints]
        """
        epsilon = 1e-6
        J = np.zeros((6, self.num_joints))
        
        pos0, orient0 = self.forward_kinematics(joint_angles)
        
        for i in range(self.num_joints):
            q_plus = joint_angles.copy()
            q_plus[i] += epsilon
            
            pos_plus, orient_plus = self.forward_kinematics(q_plus)
            
            # Position Jacobian
            J[:3, i] = (pos_plus - pos0) / epsilon
            
            # Orientation Jacobian (simplified)
            # In practice, use proper angular velocity Jacobian
            J[3:, i] = 0.0
            
        return J
        
    def check_singularity(self, joint_angles: np.ndarray, threshold: float = 0.01) -> bool:
        """
        Check if configuration is near singularity.
        
        Args:
            joint_angles: Joint angles [rad]
            threshold: Singularity threshold
            
        Returns:
            is_singular: True if near singularity
        """
        J = self.jacobian(joint_angles)
        manipulability = np.sqrt(np.linalg.det(J @ J.T))
        
        return manipulability < threshold
```

### 4.4 Safety Monitoring

#### 4.4.1 Safety Validator

**Objective:** Implement comprehensive safety validation for all robot commands.

**Requirements:**
- Joint limit checking
- Velocity limit checking
- Collision detection
- Force limit checking
- Workspace boundaries
- Response time <50ms

**Implementation:**

```python
# src/safety/safety_monitor.py

import numpy as np
from typing import Tuple, Dict, Optional
from dataclasses import dataclass

@dataclass
class SafetyLimits:
    """Safety limits for robot operation."""
    joint_position_limits: np.ndarray  # [num_joints, 2] (min, max)
    joint_velocity_limits: np.ndarray  # [num_joints] (max absolute)
    joint_acceleration_limits: np.ndarray  # [num_joints] (max absolute)
    force_limits: np.ndarray  # [6] (max force/torque)
    workspace_limits: np.ndarray  # [3, 2] (x, y, z min/max)
    max_cartesian_velocity: float  # m/s
    safety_stop_deceleration: float  # rad/s^2

class SafetyMonitor:
    """Monitors robot safety and validates commands."""
    
    def __init__(self, limits: SafetyLimits, kinematics):
        self.limits = limits
        self.kinematics = kinematics
        
        # State history for acceleration calculation
        self.prev_velocity = None
        self.prev_time = None
        
    def validate_action(self,
                       target_action: np.ndarray,
                       current_position: np.ndarray,
                       current_velocity: np.ndarray) -> Tuple[bool, str]:
        """
        Validate if action is safe to execute.
        
        Args:
            target_action: Target joint positions or velocities
            current_position: Current joint positions
            current_velocity: Current joint velocities
            
        Returns:
            is_safe: True if action is safe
            reason: Reason for failure if not safe
        """
        # Check joint position limits
        if not self._check_joint_limits(target_action):
            return False, "Joint position limits exceeded"
            
        # Check velocity limits
        target_velocity = target_action - current_position  # Simplified
        if not self._check_velocity_limits(target_velocity):
            return False, "Joint velocity limits exceeded"
            
        # Check acceleration limits
        if not self._check_acceleration_limits(target_velocity, current_velocity):
            return False, "Joint acceleration limits exceeded"
            
        # Check workspace limits
        if not self._check_workspace_limits(target_action):
            return False, "Workspace limits exceeded"
            
        # Check for collisions
        if not self._check_collisions(target_action):
            return False, "Collision detected"
            
        return True, ""
        
    def _check_joint_limits(self, joint_positions: np.ndarray) -> bool:
        """Check if joint positions are within limits."""
        within_limits = np.all(
            (joint_positions >= self.limits.joint_position_limits[:, 0]) &
            (joint_positions <= self.limits.joint_position_limits[:, 1])
        )
        return within_limits
        
    def _check_velocity_limits(self, joint_velocities: np.ndarray) -> bool:
        """Check if joint velocities are within limits."""
        within_limits = np.all(
            np.abs(joint_velocities) <= self.limits.joint_velocity_limits
        )
        return within_limits
        
    def _check_acceleration_limits(self,
                                   target_velocity: np.ndarray,
                                   current_velocity: np.ndarray) -> bool:
        """Check if acceleration is within limits."""
        if self.prev_velocity is None:
            self.prev_velocity = current_velocity
            self.prev_time = time.time()
            return True
            
        dt = time.time() - self.prev_time
        if dt < 1e-6:
            return True
            
        acceleration = (target_velocity - self.prev_velocity) / dt
        
        within_limits = np.all(
            np.abs(acceleration) <= self.limits.joint_acceleration_limits
        )
        
        self.prev_velocity = target_velocity
        self.prev_time = time.time()
        
        return within_limits
        
    def _check_workspace_limits(self, joint_positions: np.ndarray) -> bool:
        """Check if end-effector is within workspace limits."""
        position, _ = self.kinematics.forward_kinematics(joint_positions)
        
        within_limits = np.all(
            (position >= self.limits.workspace_limits[:, 0]) &
            (position <= self.limits.workspace_limits[:, 1])
        )
        return within_limits
        
    def _check_collisions(self, joint_positions: np.ndarray) -> bool:
        """Check for self-collisions and environment collisions."""
        # TODO: Implement collision detection
        # This requires:
        # 1. Robot geometry model
        # 2. Environment model
        # 3. Collision checking algorithm (e.g., FCL library)
        return True
        
    def emergency_stop_required(self, force_torque: np.ndarray) -> bool:
        """Check if emergency stop is required based on force/torque."""
        excessive_force = np.any(np.abs(force_torque) > self.limits.force_limits)
        return excessive_force
```

---

## Hardware Interface Integration

### 5.1 Jetson Orin Nano Setup

#### 5.1.1 GPIO and I/O Configuration

**Objective:** Configure GPIO pins for digital I/O and safety signals.

**Requirements:**
- Emergency stop inputs (hardware-triggered)
- Drive enable outputs
- Status LEDs
- Interrupt handling for safety signals

**Implementation:**

```python
# src/hardware/gpio_interface.py

import Jetson.GPIO as GPIO
import threading
import time
from typing import Callable, Dict

class GPIOInterface:
    """GPIO interface for Jetson Orin Nano."""
    
    # Pin definitions (BCM numbering)
    ESTOP_PIN_1 = 7  # Emergency stop button 1
    ESTOP_PIN_2 = 11  # Emergency stop button 2
    DOOR_INTERLOCK_1 = 13  # Door interlock 1
    DOOR_INTERLOCK_2 = 15  # Door interlock 2
    
    DRIVE_ENABLE_PIN = 16  # Drive enable output
    STATUS_LED_GREEN = 18  # Status LED green
    STATUS_LED_RED = 22  # Status LED red
    
    def __init__(self):
        self.estop_callback = None
        self.interlock_callback = None
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        # Setup input pins
        GPIO.setup(self.ESTOP_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.ESTOP_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.DOOR_INTERLOCK_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.DOOR_INTERLOCK_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Setup output pins
        GPIO.setup(self.DRIVE_ENABLE_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.STATUS_LED_GREEN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.STATUS_LED_RED, GPIO.OUT, initial=GPIO.LOW)
        
        # Setup interrupts for safety signals
        GPIO.add_event_detect(self.ESTOP_PIN_1, GPIO.FALLING, 
                            callback=self._estop_interrupt, bouncetime=10)
        GPIO.add_event_detect(self.ESTOP_PIN_2, GPIO.FALLING,
                            callback=self._estop_interrupt, bouncetime=10)
        GPIO.add_event_detect(self.DOOR_INTERLOCK_1, GPIO.FALLING,
                            callback=self._interlock_interrupt, bouncetime=50)
        GPIO.add_event_detect(self.DOOR_INTERLOCK_2, GPIO.FALLING,
                            callback=self._interlock_interrupt, bouncetime=50)
                            
    def _estop_interrupt(self, channel):
        """Emergency stop interrupt handler."""
        if self.estop_callback:
            self.estop_callback()
            
    def _interlock_interrupt(self, channel):
        """Door interlock interrupt handler."""
        if self.interlock_callback:
            self.interlock_callback()
            
    def register_estop_callback(self, callback: Callable):
        """Register callback for emergency stop."""
        self.estop_callback = callback
        
    def register_interlock_callback(self, callback: Callable):
        """Register callback for door interlock."""
        self.interlock_callback = callback
        
    def enable_drives(self):
        """Enable servo drives."""
        GPIO.output(self.DRIVE_ENABLE_PIN, GPIO.HIGH)
        
    def disable_drives(self):
        """Disable servo drives."""
        GPIO.output(self.DRIVE_ENABLE_PIN, GPIO.LOW)
        
    def set_status_led(self, color: str):
        """Set status LED color."""
        if color == 'green':
            GPIO.output(self.STATUS_LED_GREEN, GPIO.HIGH)
            GPIO.output(self.STATUS_LED_RED, GPIO.LOW)
        elif color == 'red':
            GPIO.output(self.STATUS_LED_GREEN, GPIO.LOW)
            GPIO.output(self.STATUS_LED_RED, GPIO.HIGH)
        elif color == 'yellow':
            GPIO.output(self.STATUS_LED_GREEN, GPIO.HIGH)
            GPIO.output(self.STATUS_LED_RED, GPIO.HIGH)
        else:
            GPIO.output(self.STATUS_LED_GREEN, GPIO.LOW)
            GPIO.output(self.STATUS_LED_RED, GPIO.LOW)
            
    def check_safety_signals(self) -> Dict[str, bool]:
        """Check all safety signals."""
        return {
            'estop_1': GPIO.input(self.ESTOP_PIN_1) == GPIO.LOW,
            'estop_2': GPIO.input(self.ESTOP_PIN_2) == GPIO.LOW,
            'door_1': GPIO.input(self.DOOR_INTERLOCK_1) == GPIO.LOW,
            'door_2': GPIO.input(self.DOOR_INTERLOCK_2) == GPIO.LOW
        }
        
    def cleanup(self):
        """Cleanup GPIO."""
        GPIO.cleanup()
```

### 5.2 Sensor Integration

#### 5.2.1 Force/Torque Sensor Interface

**Objective:** Interface with 6-axis force/torque sensor.

**Requirements:**
- Read analog signals (±10V)
- 1kHz sampling rate
- Calibration and zeroing
- Filtering

**Implementation:**

```python
# src/sensors/force_torque_sensor.py

import numpy as np
from typing import Optional
import time

class ForceTorqueSensor:
    """Interface for 6-axis force/torque sensor (e.g., ATI Mini40)."""
    
    def __init__(self,
                 calibration_matrix: np.ndarray,
                 voltage_range: float = 10.0,
                 adc_resolution: int = 16):
        """
        Args:
            calibration_matrix: 6x6 calibration matrix from manufacturer
            voltage_range: Voltage range (±V)
            adc_resolution: ADC resolution in bits
        """
        self.calibration_matrix = calibration_matrix
        self.voltage_range = voltage_range
        self.adc_resolution = adc_resolution
        self.adc_max = 2 ** (adc_resolution - 1) - 1
        
        # Bias (zero offset)
        self.bias = np.zeros(6)
        self.bias_samples = []
        
        # Filtering
        self.filter_alpha = 0.1  # Low-pass filter coefficient
        self.filtered_reading = np.zeros(6)
        
    def read_raw(self) -> np.ndarray:
        """Read raw ADC values."""
        # TODO: Implement actual ADC reading via EtherCAT I/O module
        # This is a placeholder
        raw_values = np.zeros(6)
        return raw_values
        
    def read(self) -> np.ndarray:
        """
        Read calibrated force/torque values.
        
        Returns:
            ft: [Fx, Fy, Fz, Tx, Ty, Tz] in N and Nm
        """
        # Read raw ADC values
        raw = self.read_raw()
        
        # Convert to voltages
        voltages = (raw / self.adc_max) * self.voltage_range
        
        # Apply calibration matrix
        ft = self.calibration_matrix @ voltages
        
        # Subtract bias
        ft = ft - self.bias
        
        # Apply low-pass filter
        self.filtered_reading = (self.filter_alpha * ft + 
                                (1 - self.filter_alpha) * self.filtered_reading)
        
        return self.filtered_reading
        
    def zero(self, num_samples: int = 100):
        """Zero the sensor by averaging readings."""
        print("Zeroing force/torque sensor...")
        samples = []
        
        for _ in range(num_samples):
            raw = self.read_raw()
            voltages = (raw / self.adc_max) * self.voltage_range
            ft = self.calibration_matrix @ voltages
            samples.append(ft)
            time.sleep(0.01)
            
        self.bias = np.mean(samples, axis=0)
        print(f"Bias set to: {self.bias}")
        
    def get_magnitude(self) -> float:
        """Get magnitude of force/torque vector."""
        ft = self.read()
        force_mag = np.linalg.norm(ft[:3])
        torque_mag = np.linalg.norm(ft[3:])
        return force_mag, torque_mag
```

---

## Testing and Validation

### 6.1 Unit Testing

#### 6.1.1 Test Framework Setup

**Objective:** Implement comprehensive unit tests for all modules.

**Implementation:**

```python
# tests/test_kinematics.py

import pytest
import numpy as np
from src.control.kinematics import KukaKinematics

@pytest.fixture
def kuka_kinematics():
    """Create Kuka kinematics instance for testing."""
    # Example DH parameters (replace with actual values)
    dh_params = np.array([
        [0, -np.pi/2, 0.4, 0],
        [0.6, 0, 0, 0],
        [0, -np.pi/2, 0, 0],
        [0, np.pi/2, 0.62, 0],
        [0, -np.pi/2, 0, 0],
        [0, 0, 0.115, 0]
    ])
    
    joint_limits = np.array([
        [-np.pi, np.pi],
        [-np.pi/2, np.pi/2],
        [-np.pi, np.pi],
        [-np.pi, np.pi],
        [-np.pi, np.pi],
        [-np.pi, np.pi]
    ])
    
    return KukaKinematics(dh_params, joint_limits)

def test_forward_kinematics_zero_position(kuka_kinematics):
    """Test forward kinematics at zero position."""
    joint_angles = np.zeros(6)
    position, orientation = kuka_kinematics.forward_kinematics(joint_angles)
    
    assert position.shape == (3,)
    assert orientation.shape == (3, 3)
    assert np.allclose(np.linalg.det(orientation), 1.0)  # Valid rotation matrix

def test_inverse_kinematics_consistency(kuka_kinematics):
    """Test that IK followed by FK returns to original pose."""
    # Random joint angles
    joint_angles = np.random.uniform(-np.pi/4, np.pi/4, 6)
    
    # Forward kinematics
    target_pos, target_orient = kuka_kinematics.forward_kinematics(joint_angles)
    
    # Inverse kinematics
    result = kuka_kinematics.inverse_kinematics(target_pos, target_orient, joint_angles)
    
    if result is not None:
        # Forward kinematics again
        result_pos, result_orient = kuka_kinematics.forward_kinematics(result)
        
        # Check consistency
        assert np.allclose(result_pos, target_pos, atol=0.01)

def test_jacobian_shape(kuka_kinematics):
    """Test Jacobian matrix shape."""
    joint_angles = np.zeros(6)
    J = kuka_kinematics.jacobian(joint_angles)
    
    assert J.shape == (6, 6)

def test_singularity_detection(kuka_kinematics):
    """Test singularity detection."""
    # Zero position might be singular
    joint_angles = np.zeros(6)
    is_singular = kuka_kinematics.check_singularity(joint_angles)
    
    assert isinstance(is_singular, bool)
```

```python
# tests/test_safety.py

import pytest
import numpy as np
from src.safety.safety_monitor import SafetyMonitor, SafetyLimits
from src.control.kinematics import KukaKinematics

@pytest.fixture
def safety_monitor(kuka_kinematics):
    """Create safety monitor for testing."""
    limits = SafetyLimits(
        joint_position_limits=np.array([
            [-np.pi, np.pi],
            [-np.pi/2, np.pi/2],
            [-np.pi, np.pi],
            [-np.pi, np.pi],
            [-np.pi, np.pi],
            [-np.pi, np.pi]
        ]),
        joint_velocity_limits=np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
        joint_acceleration_limits=np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0]),
        force_limits=np.array([40, 40, 40, 2, 2, 2]),
        workspace_limits=np.array([[-1, 1], [-1, 1], [0, 2]]),
        max_cartesian_velocity=0.5,
        safety_stop_deceleration=10.0
    )
    
    return SafetyMonitor(limits, kuka_kinematics)

def test_joint_limits_validation(safety_monitor):
    """Test joint limit checking."""
    current_pos = np.zeros(6)
    current_vel = np.zeros(6)
    
    # Valid action
    valid_action = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    is_safe, reason = safety_monitor.validate_action(valid_action, current_pos, current_vel)
    assert is_safe
    
    # Invalid action (exceeds limits)
    invalid_action = np.array([4.0, 0, 0, 0, 0, 0])
    is_safe, reason = safety_monitor.validate_action(invalid_action, current_pos, current_vel)
    assert not is_safe

def test_velocity_limits_validation(safety_monitor):
    """Test velocity limit checking."""
    current_pos = np.zeros(6)
    current_vel = np.zeros(6)
    
    # Action that would exceed velocity limits
    fast_action = np.array([2.0, 0, 0, 0, 0, 0])
    is_safe, reason = safety_monitor.validate_action(fast_action, current_pos, current_vel)
    assert not is_safe
    assert "velocity" in reason.lower()
```

### 6.2 Integration Testing

#### 6.2.1 Hardware-in-the-Loop Testing

**Objective:** Test complete system with actual hardware.

**Test Scenarios:**
1. Single-axis motion
2. Multi-axis coordinated motion
3. Emergency stop response
4. Mode switching (ML ↔ G-code ↔ Manual)
5. Sensor data acquisition
6. Safety system validation

**Implementation:**

```python
# tests/integration/test_system_integration.py

import pytest
import numpy as np
import time
from src.control.realtime_controller import RealtimeController, ControlConfig
from src.hardware.ethercat_master import EtherCATMaster
from src.safety.safety_monitor import SafetyMonitor

@pytest.mark.hardware
class TestSystemIntegration:
    """Integration tests requiring actual hardware."""
    
    @pytest.fixture(scope="class")
    def system(self):
        """Setup complete system."""
        # Initialize components
        # (Actual initialization code here)
        yield system
        # Cleanup
        system.stop()
        
    def test_single_axis_motion(self, system):
        """Test single axis motion."""
        # Move axis 1 to target position
        target = np.array([0.5, 0, 0, 0, 0, 0])
        
        system.set_target(target)
        time.sleep(2.0)
        
        current = system.get_current_position()
        assert np.allclose(current[0], target[0], atol=0.01)
        
    def test_emergency_stop_response(self, system):
        """Test emergency stop response time."""
        # Start motion
        system.start_motion()
        
        # Trigger emergency stop
        start_time = time.time()
        system.trigger_emergency_stop()
        
        # Wait for stop
        while system.is_moving():
            time.sleep(0.001)
            
        stop_time = time.time() - start_time
        
        # Should stop within 50ms
        assert stop_time < 0.05
        
    def test_mode_switching(self, system):
        """Test switching between control modes."""
        # Start in idle
        assert system.get_mode() == 'idle'
        
        # Switch to ML mode
        system.set_mode('ml')
        assert system.get_mode() == 'ml'
        
        # Switch to G-code mode
        system.set_mode('gcode')
        assert system.get_mode() == 'gcode'
        
        # Switch back to idle
        system.set_mode('idle')
        assert system.get_mode() == 'idle'
```

### 6.3 Performance Benchmarking

#### 6.3.1 Latency and Throughput Measurement

**Objective:** Measure system performance metrics.

**Metrics:**
- ML inference latency
- Control loop jitter
- EtherCAT cycle time
- End-to-end latency (sensor → action)

**Implementation:**

```python
# tests/benchmark/benchmark_performance.py

import time
import numpy as np
from typing import List
import matplotlib.pyplot as plt

class PerformanceBenchmark:
    """Benchmark system performance."""
    
    def __init__(self, system):
        self.system = system
        
    def benchmark_ml_inference(self, num_iterations: int = 1000) -> dict:
        """Benchmark ML inference latency."""
        latencies = []
        
        for _ in range(num_iterations):
            # Create dummy observation
            observation = self.system.get_current_observation()
            
            start = time.time()
            action = self.system.ml_model(observation)
            end = time.time()
            
            latencies.append((end - start) * 1000)  # ms
            
        return {
            'mean': np.mean(latencies),
            'std': np.std(latencies),
            'min': np.min(latencies),
            'max': np.max(latencies),
            'p50': np.percentile(latencies, 50),
            'p95': np.percentile(latencies, 95),
            'p99': np.percentile(latencies, 99)
        }
        
    def benchmark_control_loop(self, duration: float = 10.0) -> dict:
        """Benchmark control loop timing."""
        timestamps = []
        
        start_time = time.time()
        while time.time() - start_time < duration:
            timestamps.append(time.time())
            time.sleep(0.001)  # 1kHz target
            
        # Calculate jitter
        intervals = np.diff(timestamps) * 1000  # ms
        target_interval = 1.0  # ms
        jitter = np.abs(intervals - target_interval)
        
        return {
            'mean_interval': np.mean(intervals),
            'std_interval': np.std(intervals),
            'mean_jitter': np.mean(jitter),
            'max_jitter': np.max(jitter),
            'missed_deadlines': np.sum(intervals > target_interval * 1.1)
        }
        
    def plot_results(self, results: dict):
        """Plot benchmark results."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # ML inference latency
        axes[0, 0].bar(results['ml_inference'].keys(), results['ml_inference'].values())
        axes[0, 0].set_title('ML Inference Latency (ms)')
        axes[0, 0].set_ylabel('Time (ms)')
        
        # Control loop jitter
        axes[0, 1].bar(results['control_loop'].keys(), results['control_loop'].values())
        axes[0, 1].set_title('Control Loop Performance')
        
        plt.tight_layout()
        plt.savefig('benchmark_results.png')
        print("Saved benchmark results to benchmark_results.png")
```

---

## Code Organization and Structure

### 7.1 Repository Structure

**Recommended Directory Layout:**

```
kuka_ml_controller/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── .gitignore
├── docs/
│   ├── api/
│   ├── tutorials/
│   └── deployment/
├── src/
│   ├── __init__.py
│   ├── control/
│   │   ├── __init__.py
│   │   ├── realtime_controller.py
│   │   ├── kinematics.py
│   │   ├── trajectory_planner.py
│   │   └── gcode_interpreter.py
│   ├── hardware/
│   │   ├── __init__.py
│   │   ├── ethercat_master.py
│   │   ├── gpio_interface.py
│   │   └── motor_driver.py
│   ├── sensors/
│   │   ├── __init__.py
│   │   ├── camera_manager.py
│   │   ├── force_torque_sensor.py
│   │   └── encoder_interface.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── behavioral_cloning.py
│   │   ├── act_model.py
│   │   ├── diffusion_policy.py
│   │   └── model_base.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── dataset_manager.py
│   │   ├── preprocessing.py
│   │   └── augmentation.py
│   ├── training/
│   │   ├── __init__.py
│   │   ├── trainer.py
│   │   ├── dataset.py
│   │   └── utils.py
│   ├── deployment/
│   │   ├── __init__.py
│   │   ├── tensorrt_converter.py
│   │   └── model_server.py
│   ├── safety/
│   │   ├── __init__.py
│   │   ├── safety_monitor.py
│   │   └── collision_checker.py
│   ├── teleoperation/
│   │   ├── __init__.py
│   │   ├── teleop_controller.py
│   │   └── input_devices.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       ├── config.py
│       └── visualization.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_kinematics.py
│   │   ├── test_safety.py
│   │   └── test_models.py
│   ├── integration/
│   │   └── test_system_integration.py
│   └── benchmark/
│       └── benchmark_performance.py
├── scripts/
│   ├── train_model.py
│   ├── collect_data.py
│   ├── deploy_model.py
│   └── calibrate_system.py
├── config/
│   ├── robot_config.yaml
│   ├── training_config.yaml
│   └── safety_config.yaml
├── data/
│   ├── demonstrations/
│   ├── models/
│   └── logs/
└── notebooks/
    ├── data_analysis.ipynb
    └── model_evaluation.ipynb
```

### 7.2 Configuration Management

**Objective:** Centralized configuration using YAML files.

**Implementation:**

```python
# src/utils/config.py

import yaml
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, field

@dataclass
class RobotConfig:
    """Robot configuration."""
    name: str = "Kuka KR150"
    num_joints: int = 6
    dh_parameters: list = field(default_factory=list)
    joint_limits: list = field(default_factory=list)
    velocity_limits: list = field(default_factory=list)
    
@dataclass
class ControlConfig:
    """Control system configuration."""
    sensor_frequency: float = 60.0
    ml_frequency: float = 100.0
    control_frequency: float = 1000.0
    use_ml_control: bool = True
    safety_enabled: bool = True
    
@dataclass
class MLConfig:
    """ML model configuration."""
    model_type: str = "act"  # 'bc', 'act', 'diffusion'
    num_cameras: int = 3
    image_size: tuple = (224, 224)
    hidden_dim: int = 256
    chunk_size: int = 10
    
class ConfigManager:
    """Manages system configuration."""
    
    def __init__(self, config_dir: str = "./config"):
        self.config_dir = Path(config_dir)
        self.robot_config = None
        self.control_config = None
        self.ml_config = None
        
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_file = self.config_dir / f"{config_name}.yaml"
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            
        return config
        
    def load_all_configs(self):
        """Load all configuration files."""
        robot_dict = self.load_config('robot_config')
        self.robot_config = RobotConfig(**robot_dict)
        
        control_dict = self.load_config('control_config')
        self.control_config = ControlConfig(**control_dict)
        
        ml_dict = self.load_config('ml_config')
        self.ml_config = MLConfig(**ml_dict)
        
    def save_config(self, config: Dict[str, Any], config_name: str):
        """Save configuration to YAML file."""
        config_file = self.config_dir / f"{config_name}.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
```

**Example Configuration Files:**

```yaml
# config/robot_config.yaml

name: "Kuka KR150"
num_joints: 6

dh_parameters:
  - [0.0, -1.5708, 0.4, 0.0]    # Joint 1
  - [0.6, 0.0, 0.0, 0.0]         # Joint 2
  - [0.0, -1.5708, 0.0, 0.0]     # Joint 3
  - [0.0, 1.5708, 0.62, 0.0]     # Joint 4
  - [0.0, -1.5708, 0.0, 0.0]     # Joint 5
  - [0.0, 0.0, 0.115, 0.0]       # Joint 6

joint_limits:  # [min, max] in radians
  - [-3.14159, 3.14159]
  - [-1.5708, 1.5708]
  - [-3.14159, 3.14159]
  - [-3.14159, 3.14159]
  - [-3.14159, 3.14159]
  - [-3.14159, 3.14159]

velocity_limits:  # rad/s
  - 1.0
  - 1.0
  - 1.0
  - 1.5
  - 1.5
  - 2.0

ethercat:
  cycle_time_ms: 1
  drives:
    - address: 1001
      name: "Axis 1"
      max_torque: 100.0
    - address: 1002
      name: "Axis 2"
      max_torque: 100.0
    - address: 1003
      name: "Axis 3"
      max_torque: 80.0
    - address: 1004
      name: "Axis 4"
      max_torque: 50.0
    - address: 1005
      name: "Axis 5"
      max_torque: 50.0
    - address: 1006
      name: "Turning Bed"
      max_torque: 150.0
```

```yaml
# config/training_config.yaml

model:
  type: "act"  # 'bc', 'act', 'diffusion'
  num_cameras: 3
  image_size: [224, 224]
  hidden_dim: 256
  chunk_size: 10
  num_encoder_layers: 4
  num_decoder_layers: 4
  num_heads: 8
  dropout: 0.1

training:
  batch_size: 32
  num_epochs: 100
  learning_rate: 0.0001
  weight_decay: 0.0001
  gradient_clip: 1.0
  
  optimizer: "adamw"
  scheduler: "reduce_on_plateau"
  scheduler_patience: 5
  scheduler_factor: 0.5
  
  early_stopping: true
  early_stopping_patience: 10

data:
  dataset_dir: "./data/demonstrations"
  train_split: 0.8
  val_split: 0.1
  test_split: 0.1
  
  augmentation: true
  augmentation_config:
    color_jitter: true
    random_crop: true
    gaussian_noise: true
    time_warp: true

logging:
  log_dir: "./logs"
  checkpoint_dir: "./checkpoints"
  tensorboard: true
  log_interval: 10
  save_interval: 1000
```

### 7.3 Logging and Monitoring

**Objective:** Comprehensive logging for debugging and monitoring.

**Implementation:**

```python
# src/utils/logging.py

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class SystemLogger:
    """Centralized logging system."""
    
    def __init__(self, 
                 log_dir: str = "./logs",
                 log_level: int = logging.INFO,
                 console_output: bool = True):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("KukaMLController")
        self.logger.setLevel(log_level)
        
        # File handler
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"system_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            self.logger.addHandler(console_handler)
            
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
        
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
        
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
        
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)
        
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
```

---

## Implementation Priorities

### Phase-by-Phase Implementation Sequence

#### Phase 1: LeRobot Proof of Concept (Weeks 1-8)

**Priority 1: Development Environment Setup**
- [ ] Install JetPack on Jetson Orin Nano
- [ ] Configure PREEMPT_RT kernel
- [ ] Install Python dependencies
- [ ] Setup version control

**Priority 2: Basic Data Collection**
- [ ] Implement teleoperation controller
- [ ] Setup camera capture
- [ ] Implement dataset manager
- [ ] Collect 100+ demonstrations

**Priority 3: Baseline ML Model**
- [ ] Implement Behavioral Cloning model
- [ ] Implement training pipeline
- [ ] Train baseline model
- [ ] Benchmark inference latency

**Success Criteria:**
- Model achieves >80% success rate on simple tasks
- Inference latency <50ms
- Team confident in ML approach

#### Phase 4: Software Architecture Development (Weeks 21-28)

**Priority 1: Real-Time Control Foundation**
- [ ] Implement EtherCAT master interface
- [ ] Implement multi-rate control loops
- [ ] Implement kinematics library
- [ ] Test control loop timing (1kHz)

**Priority 2: Safety Systems**
- [ ] Implement safety monitor
- [ ] Implement GPIO interface for E-stop
- [ ] Test emergency stop response (<50ms)
- [ ] Implement collision detection

**Priority 3: G-Code Interpreter**
- [ ] Implement G-code parser
- [ ] Implement trajectory planner
- [ ] Test with simple G-code programs
- [ ] Validate accuracy

**Priority 4: ML Integration**
- [ ] Integrate ML inference into control loop
- [ ] Implement mode switching
- [ ] Test ML control mode
- [ ] Optimize inference latency (<10ms)

#### Phase 5: ML Model Development (Weeks 29-36)

**Priority 1: Advanced Models**
- [ ] Implement ACT model
- [ ] Implement Diffusion Policy
- [ ] Train on 1000+ demonstrations
- [ ] Compare model performance

**Priority 2: Model Optimization**
- [ ] Convert models to ONNX
- [ ] Convert to TensorRT
- [ ] Benchmark optimized models
- [ ] Deploy best model

**Priority 3: Online Learning**
- [ ] Implement online learning framework
- [ ] Implement model hot-swapping
- [ ] Test continuous improvement
- [ ] Validate safety during updates

#### Phase 6: System Integration & Testing (Weeks 37-44)

**Priority 1: Component Integration**
- [ ] Integrate all hardware interfaces
- [ ] Test single-axis motion
- [ ] Test multi-axis coordination
- [ ] Test full system

**Priority 2: Performance Validation**
- [ ] Measure positioning accuracy
- [ ] Measure repeatability
- [ ] Benchmark cycle times
- [ ] Compare to baseline

**Priority 3: Endurance Testing**
- [ ] Run 8+ hour tests
- [ ] Monitor for failures
- [ ] Validate thermal performance
- [ ] Test recovery procedures

---

## References

### Source Documents
- **Project Analysis:** `./analysis/project_analysis.md`
  - Sections: All (comprehensive reference)
  - Key information: Hardware specs, control architecture, ML requirements, safety, phases

### Technical Specifications
- **EtherCAT Protocol:** IEC 61158
- **Safety Standards:** ISO 13849-1 Category 3, IEC 61800-5-2
- **Electrical Safety:** NFPA 70E (480V AC systems)

### Hardware Documentation
- **Jetson Orin Nano:** NVIDIA Developer Documentation
- **Motor Drives:** Kollmorgen AKD-P, Beckhoff AX5000 manuals
- **Force/Torque Sensor:** ATI Mini40 specifications
- **Intel RealSense D435:** SDK documentation

### Software Libraries
- **PyTorch:** https://pytorch.org/
- **TensorRT:** https://developer.nvidia.com/tensorrt
- **ROS2:** https://docs.ros.org/
- **EtherCAT Master:** https://gitlab.com/etherlab.org/ethercat

### ML Research Papers
- **Behavioral Cloning:** Pomerleau, D. A. (1991). "Efficient Training of Artificial Neural Networks for Autonomous Navigation"
- **Action Chunking Transformer (ACT):** Zhao et al. (2023). "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware"
- **Diffusion Policy:** Chi et al. (2023). "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion"

### Key Implementation Notes

1. **Critical Safety Requirements:**
   - 480V AC system requires licensed electrician
   - Hardware E-stop independent of software
   - Response time <50ms for safety systems
   - Comprehensive LOTO procedures

2. **Real-Time Performance:**
   - Control loop: 1kHz deterministic
   - ML inference: <10ms target
   - CPU core isolation required
   - Memory locking essential

3. **Communication Protocol:**
   - Existing drives use DeviceNet/PROFIBUS (NOT EtherCAT)
   - Drive replacement required (~$7,200)
   - Alternative: Protocol gateway (~$1,500-2,500)

4. **Model Optimization:**
   - Train in PyTorch
   - Export to ONNX
   - Convert to TensorRT
   - Target: <10ms inference on Jetson

5. **Data Collection:**
   - Minimum 100 demonstrations per task
   - Multi-modal: vision + proprioception + force
   - Data augmentation essential
   - Continuous collection for online learning

---

**End of Coding Tasks Documentation**

This document provides comprehensive implementation guidance for developers and AI agents working on the Kuka robot arm AI-driven controller system. All technical specifications and requirements are extracted from the project analysis document (`./analysis/project_analysis.md`).

For human task documentation and repository structure proposals, refer to the companion documents in the `./final/` directory.
