# Agent Instructions: Information Gathering & Implementation

## Overview
This document provides specific instructions for team members (agents) responsible for gathering information about the existing Kuka system and implementing the ML controller replacement.

---

## Agent Roles & Responsibilities

### 1. Mechanical Systems Agent
**Primary Responsibilities:**
- Document all mechanical components and specifications
- Create CAD models of interfaces
- Measure kinematics and workspace
- Validate mechanical compatibility

**Required Skills:**
- Mechanical engineering background
- CAD proficiency (SolidWorks, Fusion 360, etc.)
- Metrology and measurement experience
- Robot kinematics knowledge

### 2. Electrical Systems Agent
**Primary Responsibilities:**
- Document electrical systems and wiring
- Map communication protocols
- Specify motor drivers and interfaces
- Design safety systems

**Required Skills:**
- Electrical engineering background
- Experience with industrial controls
- Knowledge of communication protocols (EtherCAT, CANopen)
- Safety system design experience

### 3. Software/Controls Agent
**Primary Responsibilities:**
- Extract control software parameters
- Document G-code implementation
- Design real-time control architecture
- Implement software stack

**Required Skills:**
- Embedded systems programming (C++, Python)
- Real-time operating systems experience
- CNC control system knowledge
- ROS/robotics middleware experience

### 4. Machine Learning Agent
**Primary Responsibilities:**
- Design ML architecture
- Collect and curate training data
- Train and optimize models
- Implement inference pipeline

**Required Skills:**
- Deep learning expertise (PyTorch, TensorFlow)
- Robot learning experience
- Computer vision knowledge
- Model optimization for edge devices

### 5. Integration & Testing Agent
**Primary Responsibilities:**
- Coordinate integration activities
- Develop test protocols
- Execute validation tests
- Troubleshoot issues

**Required Skills:**
- Systems integration experience
- Testing and validation expertise
- Problem-solving skills
- Project management

---

## Phase-by-Phase Agent Instructions

## Phase 1: LeRobot Proof of Concept

### Mechanical Systems Agent - Phase 1

**Week 1-2: Hardware Assembly**

Instructions:
1. **Procure Components**
   - Order motors, encoders, structural components per LeRobot BOM
   - Verify component compatibility before ordering
   - Maintain procurement spreadsheet with vendor, part#, cost, lead time

2. **Assemble Follower Arm**
   - Follow LeRobot assembly instructions
   - Document any deviations or modifications
   - Take photos at each assembly step for future reference
   - Label all components and connectors

3. **Install Sensors**
   - Mount force/torque sensors at designated joints
   - Ensure proper alignment and calibration
   - Document sensor orientations and reference frames
   - Create wiring diagram for sensors

4. **Quality Checks**
   - Verify all joints move freely without binding
   - Check encoder alignment
   - Validate sensor outputs
   - Document range of motion for each joint

**Deliverables:**
- Assembled follower arm
- Component wiring diagram
- Assembly photo documentation
- Range of motion measurements

### Electrical Systems Agent - Phase 1

**Week 1-2: Electronics Setup**

Instructions:
1. **Prepare Jetson Orin Nano Super**
   - Install heat sink and cooling fan
   - Flash JetPack SDK (latest stable version)
   - Configure GPIO pins for motor drivers
   - Set up development environment

2. **Wire Motor Drivers**
   - Connect motor drivers to Jetson GPIO or I2C/SPI
   - Implement proper power distribution
   - Install fuses and protection circuits
   - Create wiring harness diagram

3. **Sensor Integration**
   - Wire force/torque sensors to appropriate interfaces
   - Connect cameras to Jetson CSI or USB ports
   - Implement signal conditioning if needed
   - Validate sensor data acquisition

4. **Safety Systems**
   - Implement emergency stop button
   - Create hardware watchdog circuit
   - Test e-stop functionality
   - Document safety system response times

**Deliverables:**
- Fully wired Jetson-based controller
- Complete wiring diagram
- Safety system test results
- Pin assignment documentation

### Software/Controls Agent - Phase 1

**Week 3-4: Software Stack Setup**

Instructions:
1. **Environment Configuration**
   ```bash
   # Install ROS2 (recommended: Humble or Iron)
   sudo apt update
   sudo apt install ros-humble-desktop
   
   # Install LeRobot dependencies
   git clone https://github.com/huggingface/lerobot.git
   cd lerobot
   pip install -e .
   
   # Install additional dependencies
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   pip install opencv-python pyrealsense2 dynamixel-sdk
   ```

2. **Camera Calibration**
   - Use ROS camera_calibration package or OpenCV
   - Capture calibration images (20-30 images)
   - Calculate intrinsic parameters (focal length, principal point, distortion)
   - Calculate extrinsic parameters (camera-to-base transform)
   - Save calibration files in YAML format

3. **Create Control Interface**
   - Implement motor control nodes (ROS2 or Python)
   - Create teleoperation interface (keyboard, joystick, or leader-follower)
   - Implement data logging functionality
   - Create visualization in RViz or custom GUI

4. **Testing**
   - Test individual joint control
   - Verify teleoperation responsiveness
   - Check data logging pipeline
   - Validate camera streams

**Deliverables:**
- Configured software environment
- Camera calibration files
- Control interface code
- Data logging system

### Machine Learning Agent - Phase 1

**Week 5-6: Data Collection & Training**

Instructions:
1. **Design Data Collection Protocol**
   - Define tasks to demonstrate (pick-place, reaching, manipulation)
   - Create task variation strategy (object positions, orientations)
   - Design data structure (states, actions, observations, rewards)
   - Implement quality checks (trajectory smoothness, task success)

2. **Collect Demonstrations**
   - Minimum 100 successful demonstrations per task
   - Vary environmental conditions (lighting, backgrounds)
   - Include failure cases for learning robust policies
   - Record multi-modal data:
     ```python
     demonstration = {
         'observations': {
             'camera_images': [],  # RGB images
             'joint_positions': [],  # Robot state
             'force_torque': [],  # Sensor data
         },
         'actions': [],  # Joint velocities or positions
         'rewards': [],  # Success metrics
         'metadata': {}  # Task parameters
     }
     ```

3. **Data Augmentation**
   - Implement image augmentations (color jitter, cropping, rotation)
   - Add noise to joint positions (±5% of range)
   - Time-warp trajectories (±10% speed variation)
   - Create synthetic viewpoints if cameras allow

4. **Train Baseline Models**
   - Start with behavioral cloning (BC):
     ```python
     # Example training loop structure
     for epoch in range(num_epochs):
         for batch in dataloader:
             observations = batch['observations']
             actions = batch['actions']
             
             predicted_actions = policy_network(observations)
             loss = criterion(predicted_actions, actions)
             
             optimizer.zero_grad()
             loss.backward()
             optimizer.step()
     ```
   - Use ACT (Action Chunking Transformer) or Diffusion Policy
   - Experiment with different architectures
   - Track training metrics (loss, success rate)

5. **Validation**
   - Test on held-out demonstrations
   - Execute policies in real environment
   - Measure success rate, trajectory error
   - Identify failure modes

**Deliverables:**
- Dataset of 100+ demonstrations per task
- Trained policy models
- Training curves and metrics
- Model performance report

---

## Phase 2: Kuka System Analysis

### Mechanical Systems Agent - Phase 2

**Week 9-10: Complete Mechanical Documentation**

Instructions:
1. **Access the Kuka System**
   - Schedule dedicated time for documentation (minimize production impact)
   - Bring necessary tools: calipers, measuring tape, camera, notebook
   - Follow lockout/tagout procedures

2. **Measure & Document**
   - **Joint Ranges:**
     - Manually move each joint to limits
     - Record min/max angles
     - Note any soft limits vs. hard stops
     - Document home position
   
   - **Link Lengths:**
     - Measure distance between joint axes
     - Take multiple measurements for accuracy
     - Compare to manufacturer specs if available
     - Create sketch with dimensions
   
   - **DH Parameters:**
     - Determine link lengths (a_i)
     - Determine link offsets (d_i)
     - Determine link twists (α_i)
     - Determine joint angles (θ_i)
     - Verify with forward kinematics

3. **Photograph Everything**
   - Overall system from multiple angles
   - Each joint close-up
   - Motor and encoder mounting
   - Cable routing
   - Connector details with labels
   - Include scale reference in photos

4. **Create CAD Models**
   - Model mounting interfaces for sensors
   - Model cable routing paths
   - Model controller enclosure mounting location
   - Export STEP files for sharing

**Data Recording Template:**
```
Joint 1 (Base Rotation):
- Range: -170° to +170°
- Link length (a1): ___ mm
- Link offset (d1): ___ mm
- Link twist (α1): ___ degrees
- Motor model: ___
- Gear ratio: ___
- Home position: ___ degrees
- Photos: IMG_001.jpg to IMG_010.jpg
```

**Deliverables:**
- Complete dimensional drawings
- DH parameter table
- Photo documentation (organized by joint/component)
- CAD models of interfaces

### Electrical Systems Agent - Phase 2

**Week 10-11: Electrical System Documentation**

Instructions:
1. **Safety First**
   - Lockout/tagout electrical power
   - Use multimeter to verify de-energized
   - Wear appropriate PPE
   - Have second person for safety

2. **Controller Interior Documentation**
   - Open controller cabinet (take photos before disturbing anything)
   - Identify all components:
     - Motor drives (make, model, qty)
     - PLC or motion controller
     - I/O modules
     - Power supplies
     - Safety relays
   - Photograph each component nameplate
   - Note all indicator lights and their meanings

3. **Trace Wiring**
   - For each motor (Axes 1-5 + turning bed):
     - Trace power wires from drive to motor
     - Document wire gauge, color code
     - Note connector types and pinouts
     - Trace encoder wires
     - Document shield connections
   
   - For I/O:
     - Map all inputs (limits, e-stop, sensors)
     - Map all outputs (enable, spindle, coolant)
     - Create I/O table with signal names

4. **Identify Communication Protocol**
   - Look for network cables (Ethernet, fieldbus)
   - Identify protocol by:
     - Cable type (color-coded for EtherCAT, etc.)
     - Connector types
     - Labels on drives/controller
     - Manufacturer documentation
   - Note network topology (star, daisy-chain)
   - Record device addresses

5. **Measure Voltages & Currents**
   - Record DC bus voltage
   - Measure motor phase voltages (if safe)
   - Note rated currents from motor nameplates
   - Check power supply outputs (24V, 5V, etc.)

**Data Recording Template:**
```
Axis 1 Motor Drive:
- Manufacturer: ___
- Model: ___
- Firmware version: ___
- DC bus voltage: ___ VDC
- Max current: ___ A
- Communication: ___ (protocol)
- Address/Node ID: ___
- Status: ___ (working/faulty)
- Photo: IMG_E_001.jpg

Axis 1 Motor:
- Manufacturer: ___
- Model: ___
- Voltage: ___ VDC
- Current: ___ A continuous, ___ A peak
- Torque: ___ Nm
- Speed: ___ RPM max
- Encoder: ___ (type, resolution)
- Cable: ___ AWG, ___ meters
- Connectors: ___ (type)
- Photo: IMG_E_002.jpg
```

**Deliverables:**
- Complete wiring diagrams
- Component specifications spreadsheet
- I/O mapping table
- Protocol identification document
- Electrical photos (labeled)

### Software/Controls Agent - Phase 2

**Week 11-12: Software Extraction**

Instructions:
1. **Backup Everything**
   - Connect laptop to controller (follow safety protocols)
   - Backup all programs to USB drive
   - Export parameter files
   - Save configuration databases
   - Create full system image if possible

2. **Extract G-Code Implementation**
   - Review example G-code programs
   - Create list of all G-codes used (G0, G1, G2, G3, etc.)
   - Create list of all M-codes used
   - Document any custom macros or subroutines
   - Note coordinate system handling (G54-G59)
   - Document tool offset system

3. **Extract Control Parameters**
   - PID gain values for each axis
   - Feedforward parameters
   - Acceleration limits
   - Velocity limits
   - Following error limits
   - Backlash compensation values
   
   **Create Parameter Table:**
   ```
   Axis 1 (Base):
   - P gain: ___
   - I gain: ___
   - D gain: ___
   - Feedforward velocity: ___
   - Feedforward accel: ___
   - Max velocity: ___ deg/s
   - Max acceleration: ___ deg/s²
   - Following error limit: ___ deg
   - Backlash: ___ deg
   ```

4. **Document HMI**
   - Screenshot all HMI screens
   - Note screen flow and navigation
   - Document user access levels
   - Identify critical operator functions
   - Note alarm messages and meanings

5. **Test Data Acquisition**
   - If controller allows, connect via debug port
   - Attempt to log real-time data during operation:
     - Joint positions
     - Joint velocities
     - Commanded vs. actual positions
     - Motor currents
     - Timestamps
   - Analyze data for control loop performance

**Deliverables:**
- Complete backup of all software
- G-code and M-code reference document
- Control parameter tables
- HMI documentation
- Control loop performance analysis

---

## Phase 3: Hardware Interface Design

### Electrical Systems Agent - Phase 3

**Week 15-18: Design New Interface Electronics**

Instructions:
1. **Select Motor Drivers**
   - Choose drives compatible with existing motors:
     - Match voltage rating
     - Exceed current rating by 20%
     - Support required communication protocol
   - Recommended: EtherCAT-based servo drives (e.g., Beckhoff, Kollmorgen)
   - Create comparison matrix:
     ```
     | Drive Model | Voltage | Current | Protocol | Cost | Notes |
     |-------------|---------|---------|----------|------|-------|
     | Example 1   | 48V     | 10A     | EtherCAT | $500 | Good  |
     ```

2. **Design Interface Board**
   - Create schematic for Jetson-to-drives interface:
     - EtherCAT or Ethernet connection
     - GPIO for additional I/O
     - Isolation for noisy signals
     - Power distribution
   - Use KiCad or similar EDA software
   - Include:
     - Voltage regulation (24V to 5V/3.3V)
     - Optoisolators for I/O
     - LED status indicators
     - Connector headers

3. **Safety System Design**
   - Design redundant e-stop circuit:
     ```
     E-Stop Button → Safety Relay 1 → Safety Relay 2 → Motor Enable
     ```
   - Include:
     - Hardware watchdog timer (resets if no heartbeat)
     - Over-current protection
     - Over-temperature monitoring
     - Safe torque off (STO) for each drive
   - Ensure compliance with ISO 13849 Category 3 or higher

4. **Create BOM and Order**
   - List all components with part numbers
   - Identify suppliers and lead times
   - Order prototyping quantities
   - Plan for assembly and testing

**Deliverables:**
- Schematic diagrams
- PCB layout (if custom board)
- BOM with suppliers
- Safety system design document

---

## Phase 4: Software Architecture

### Software/Controls Agent - Phase 4

**Week 21-24: Implement Real-Time Control**

Instructions:
1. **Configure Real-Time Linux**
   - Install Ubuntu with PREEMPT_RT patch:
     ```bash
     # Download and apply RT patch
     wget https://cdn.kernel.org/pub/linux/kernel/projects/rt/
     # Follow RT kernel compilation instructions
     
     # Verify RT capabilities
     uname -a  # Should show PREEMPT RT
     ```
   
   - Optimize for real-time:
     - Disable power management
     - Isolate CPU cores for control
     - Set process priorities
     - Configure memory locking

2. **Implement Control Loop**
   - Create high-frequency control thread (1-10 kHz):
     ```cpp
     void control_loop() {
         while (running) {
             auto start = std::chrono::steady_clock::now();
             
             // Read sensors
             read_encoders(joint_positions);
             read_force_sensors(joint_torques);
             
             // Compute control
             compute_inverse_kinematics(target_pose, target_joints);
             compute_pid_control(target_joints, joint_positions, commands);
             
             // Send commands
             send_motor_commands(commands);
             
             // Enforce cycle time
             auto end = std::chrono::steady_clock::now();
             auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
             sleep_until(start + std::chrono::microseconds(1000));  // 1kHz example
         }
     }
     ```

3. **Implement Kinematics**
   - Forward kinematics using DH parameters:
     ```python
     def forward_kinematics(joint_angles, dh_params):
         T = np.eye(4)
         for i, theta in enumerate(joint_angles):
             a, d, alpha = dh_params[i]
             T_i = dh_matrix(theta, a, d, alpha)
             T = T @ T_i
         return T  # Transformation matrix
     ```
   
   - Inverse kinematics (analytical or numerical):
     ```python
     def inverse_kinematics(target_pose, initial_guess):
         # Use Jacobian pseudo-inverse method
         joint_angles = initial_guess
         for iteration in range(max_iterations):
             current_pose = forward_kinematics(joint_angles, dh_params)
             error = target_pose - current_pose
             if np.linalg.norm(error) < tolerance:
                 return joint_angles
             J = compute_jacobian(joint_angles)
             delta_q = np.linalg.pinv(J) @ error
             joint_angles += learning_rate * delta_q
         return joint_angles
     ```

4. **Implement G-Code Parser**
   - Create parser for common G-codes:
     ```python
     class GCodeParser:
         def parse_line(self, line):
             # Remove comments
             line = line.split(';')[0].strip()
             
             # Extract G/M code
             tokens = line.split()
             command = tokens[0]
             params = {}
             
             for token in tokens[1:]:
                 letter = token[0]
                 value = float(token[1:])
                 params[letter] = value
             
             if command == 'G0' or command == 'G1':
                 return self.linear_move(params)
             elif command == 'G2' or command == 'G3':
                 return self.arc_move(params)
             # ... handle other codes
         
         def linear_move(self, params):
             target = {
                 'X': params.get('X', current_pos['X']),
                 'Y': params.get('Y', current_pos['Y']),
                 'Z': params.get('Z', current_pos['Z']),
             }
             feedrate = params.get('F', current_feedrate)
             return generate_trajectory(current_pos, target, feedrate)
     ```

**Deliverables:**
- Real-time control software
- Kinematics library with tests
- G-code parser and interpreter
- Documentation and code comments

### Machine Learning Agent - Phase 4

**Week 25-27: ML Inference Integration**

Instructions:
1. **Optimize Models for Jetson**
   - Convert PyTorch models to ONNX:
     ```python
     import torch
     import torch.onnx
     
     # Export model
     dummy_input = torch.randn(1, 3, 224, 224)  # Example
     torch.onnx.export(model, dummy_input, "model.onnx")
     ```
   
   - Convert ONNX to TensorRT:
     ```bash
     /usr/src/tensorrt/bin/trtexec --onnx=model.onnx --saveEngine=model.trt --fp16
     ```
   
   - Benchmark inference time (should be <10ms)

2. **Create Inference Pipeline**
   - Implement preprocessing:
     ```python
     def preprocess_observation(camera_image, joint_state):
         # Resize and normalize image
         img = cv2.resize(camera_image, (224, 224))
         img = img / 255.0
         img_tensor = torch.from_numpy(img).permute(2, 0, 1)
         
         # Normalize joint state
         joint_tensor = torch.from_numpy(joint_state)
         joint_normalized = (joint_tensor - joint_min) / (joint_max - joint_min)
         
         return img_tensor, joint_normalized
     ```
   
   - Implement inference:
     ```python
     def predict_action(observation):
         img, joints = preprocess_observation(observation)
         with torch.no_grad():
             action = model(img, joints)
         return postprocess_action(action)
     ```

3. **Design Mode Switching**
   - Create state machine:
     ```
     States:
     - G_CODE_MODE: Execute traditional G-code
     - ML_AUTONOMOUS_MODE: Use ML policy
     - MANUAL_MODE: Direct teleoperation
     - E_STOP: Emergency stop
     
     Transitions:
     - User command
     - Task completion
     - Error/fault detection
     - Safety trigger
     ```

4. **Implement Safety Checks**
   - Validate ML outputs before execution:
     ```python
     def validate_action(action, current_state):
         # Check joint limits
         predicted_state = current_state + action * dt
         if np.any(predicted_state < joint_min) or np.any(predicted_state > joint_max):
             return False, "Joint limit violation"
         
         # Check velocity limits
         velocity = action
         if np.any(np.abs(velocity) > max_velocity):
             return False, "Velocity limit exceeded"
         
         # Check collision (if collision model available)
         if check_collision(predicted_state):
             return False, "Collision detected"
         
         return True, "OK"
     ```

**Deliverables:**
- Optimized ML models for Jetson
- Inference pipeline code
- Mode switching state machine
- Safety validation system

---

## Phase 5: ML Model Development

### Machine Learning Agent - Phase 5

**Week 29-36: Full ML Pipeline**

Instructions:
1. **Create Digital Twin Simulation**
   - Use Isaac Sim or Gazebo:
     ```python
     # Example with PyBullet (simpler alternative)
     import pybullet as p
     import pybullet_data
     
     # Load robot URDF
     p.connect(p.GUI)
     p.setAdditionalSearchPath(pybullet_data.getDataPath())
     robot_id = p.loadURDF("kuka_description/urdf/kuka.urdf")
     
     # Add sensors, cameras, environment
     camera_params = {
         'width': 640,
         'height': 480,
         'fov': 60,
         'near': 0.1,
         'far': 10.0
     }
     ```
   
   - Implement domain randomization:
     - Vary lighting conditions
     - Randomize object textures and colors
     - Add noise to physics parameters
     - Randomize camera positions

2. **Collect Real-World Data**
   - Set up teleoperation:
     - Use VR controllers, or
     - Use leader-follower arm, or
     - Use joystick/keyboard
   
   - Record comprehensive data:
     ```python
     def collect_demonstration():
         episode_data = {
             'observations': [],
             'actions': [],
             'metadata': {
                 'task': 'pick_and_place',
                 'success': False,
                 'duration': 0
             }
         }
         
         while not done:
             obs = get_observation()  # Images + joint states
             action = get_human_action()  # From teleoperation
             
             episode_data['observations'].append(obs)
             episode_data['actions'].append(action)
             
             execute_action(action)
         
         return episode_data
     ```
   
   - Quality control:
     - Review each demonstration
     - Remove failed attempts
     - Annotate special events
     - Balance dataset across task variations

3. **Train Advanced Models**
   - Implement Action Chunking Transformer (ACT):
     ```python
     class ACTPolicy(nn.Module):
         def __init__(self, obs_dim, action_dim, chunk_size=10):
             super().__init__()
             self.chunk_size = chunk_size
             
             # Vision encoder
             self.vision_encoder = ResNet18()
             
             # Transformer decoder
             self.transformer = nn.TransformerDecoder(
                 nn.TransformerDecoderLayer(d_model=512, nhead=8),
                 num_layers=4
             )
             
             # Action head
             self.action_head = nn.Linear(512, action_dim * chunk_size)
         
         def forward(self, obs):
             # Encode observation
             features = self.vision_encoder(obs['image'])
             state_features = self.encode_state(obs['joints'])
             
             # Decode action sequence
             actions = self.transformer(features, state_features)
             actions = self.action_head(actions)
             
             return actions.reshape(-1, self.chunk_size, action_dim)
     ```
   
   - Try Diffusion Policy:
     ```python
     # Diffusion models generate actions through denoising
     def train_diffusion_policy(observations, actions):
         for epoch in range(num_epochs):
             for obs, true_actions in dataloader:
                 # Add noise to actions
                 t = torch.randint(0, num_diffusion_steps, (batch_size,))
                 noise = torch.randn_like(true_actions)
                 noisy_actions = sqrt_alpha[t] * true_actions + sqrt_one_minus_alpha[t] * noise
                 
                 # Predict noise
                 predicted_noise = diffusion_model(noisy_actions, obs, t)
                 loss = F.mse_loss(predicted_noise, noise)
                 
                 optimizer.zero_grad()
                 loss.backward()
                 optimizer.step()
     ```

4. **Implement Online Learning**
   - Collect corrective feedback during deployment:
     ```python
     def online_learning_step(observation, ml_action, human_correction):
         # If human intervenes, use their action as supervision
         if human_correction is not None:
             dataset.add(observation, human_correction)
             
             # Periodic fine-tuning
             if len(dataset) > batch_size:
                 fine_tune_model(dataset.get_batch())
     ```

**Deliverables:**
- Simulation environment
- Dataset of 1000+ demonstrations
- Trained ACT/Diffusion models
- Online learning framework
- Model performance benchmarks

---

## Phase 6: Integration & Testing

### Integration & Testing Agent - Phase 6

**Week 37-44: Systematic Integration**

Instructions:
1. **Create Test Protocols**
   - Define test procedures:
     ```markdown
     Test ID: HW-001
     Test Name: Single Axis Position Control
     Objective: Verify axis 1 can reach commanded positions
     Procedure:
       1. Command axis 1 to 0°
       2. Measure actual position
       3. Command axis 1 to 45°
       4. Measure actual position
       5. Repeat for -45°, 90°, -90°
     Success Criteria:
       - Position error < 0.1°
       - No oscillation
       - Response time < 1s
     ```

2. **Benchtop Testing (Week 37-38)**
   - Test each component individually
   - Document results in table:
     ```
     | Test ID | Component | Result | Error | Notes |
     |---------|-----------|--------|-------|-------|
     | HW-001  | Axis 1    | PASS   | 0.05° | Good  |
     | HW-002  | Axis 2    | FAIL   | 2.3°  | Investigate encoder |
     ```
   
   - Troubleshoot failures systematically:
     - Check wiring
     - Verify parameters
     - Test with oscilloscope
     - Consult datasheets

3. **Safety System Testing**
   - Test emergency stop:
     - Press e-stop during motion → motors should stop within 50ms
     - Verify all axes stop
     - Verify system cannot restart without reset
   
   - Test fault detection:
     - Simulate over-current → should trigger within 100ms
     - Simulate over-temperature → should trigger before damage
     - Simulate encoder loss → should detect within 1 control cycle

4. **Progressive Integration (Week 39-42)**
   - Single axis → 2 axes → 3 axes → ... → full system
   - At each stage:
     - Test coordinated motion
     - Measure tracking error
     - Test at various speeds
     - Validate kinematics
   
   - Example test:
     ```python
     def test_coordinated_motion():
         # Define trajectory
         start_joints = [0, 0, 0, 0, 0]
         end_joints = [45, -30, 60, 0, 90]
         
         # Execute trajectory
         traj = generate_trajectory(start_joints, end_joints, duration=5.0)
         execute_trajectory(traj)
         
         # Measure performance
         actual_traj = recorded_trajectory
         error = calculate_tracking_error(traj, actual_traj)
         
         assert error.max() < 0.5, f"Tracking error too large: {error.max()}"
     ```

5. **ML System Testing (Week 43)**
   - Test inference performance:
     - Measure latency for each component
     - Ensure total latency < 10ms
   
   - Test ML vs. G-code mode:
     - Execute same task in both modes
     - Compare quality and time
   
   - Test mode switching:
     - Switch modes during operation
     - Verify smooth transitions
     - No sudden jumps or errors

6. **Endurance Testing (Week 44)**
   - Run system continuously for 8+ hours
   - Monitor:
     - CPU/GPU temperature
     - Memory usage
     - Control loop timing
     - Any errors or warnings
   - Log all data for analysis

**Deliverables:**
- Test protocol document
- Test results database
- Integration report
- Issues log and resolutions
- Performance validation report

---

## Data Management Guidelines

### File Organization
- Use consistent naming: `YYYY-MM-DD_project_description_version.ext`
- Organize by phase and agent role
- Maintain README in each folder
- Version control all code with Git

### Documentation Standards
- All measurements include units
- Include uncertainty/tolerance
- Date and sign all documents
- Cross-reference related documents
- Maintain change log

### Code Standards
- Use consistent style (PEP 8 for Python, Google C++ Style Guide)
- Comment all functions and classes
- Include examples in documentation
- Write unit tests (>80% coverage target)
- Use meaningful variable names

### Backup Strategy
- Daily backups of active development
- Weekly full system backups
- Off-site backup of critical data
- Test restore procedures monthly

---

## Communication Protocols

### Regular Meetings
- Daily stand-ups (15 min)
  - What did you accomplish yesterday?
  - What will you do today?
  - Any blockers?

- Weekly technical reviews (1 hour)
  - Demo progress
  - Review test results
  - Discuss challenges
  - Plan next week

- Bi-weekly stakeholder updates
  - High-level progress summary
  - Risks and mitigation
  - Budget and timeline status

### Issue Tracking
Use issue tracking system (Jira, GitHub Issues, etc.):
- Create issues for all tasks
- Assign priority and due date
- Link related issues
- Update status regularly
- Close with resolution notes

### Knowledge Sharing
- Document lessons learned
- Share useful code snippets
- Create tutorials for common tasks
- Maintain FAQ document

---

## Safety Reminders

### Always:
- Follow lockout/tagout procedures
- Wear appropriate PPE
- Have second person present for risky tasks
- Test safety systems before each session
- Keep emergency stop accessible
- Understand emergency shutdown procedures

### Never:
- Override safety interlocks
- Work on energized systems unless absolutely necessary
- Leave system running unattended during development
- Disable safety features "just for testing"

---

## Contact & Escalation

### Technical Issues
1. Try to resolve with team
2. Consult documentation and forums
3. Contact component manufacturers
4. Escalate to project lead

### Safety Concerns
1. Stop work immediately
2. Notify project lead
3. Document concern
4. Do not resume until resolved

### Budget/Timeline Issues
1. Identify issue early
2. Quantify impact
3. Propose solutions
4. Escalate to project manager

---

## Appendix: Tool & Resource List

### Hardware Tools
- Multimeter
- Oscilloscope
- Calipers and micrometers
- Laser distance meter
- Thermal camera (optional)

### Software Tools
- CAD: SolidWorks, Fusion 360, FreeCAD
- EDA: KiCad, Altium
- IDE: VS Code, PyCharm
- Version control: Git, GitHub
- Simulation: Gazebo, Isaac Sim, PyBullet

### Reference Materials
- Robot Operating System (ROS) documentation
- EtherCAT specification
- ISO safety standards (13849, 10218)
- Machine learning papers (ACT, Diffusion Policy)
