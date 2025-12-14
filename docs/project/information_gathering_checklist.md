# Kuka CNC ML Controller: Information Gathering Checklist

## Purpose
This document provides a systematic checklist for gathering all necessary information about the existing Kuka 5-axis CNC system to enable successful ML controller replacement.

---

## 1. Mechanical System Information

### 1.1 Robot Arm Specifications
- [ ] **Manufacturer & Model**
  - Full model number and serial number
  - Year of manufacture
  - Robot generation/version

- [ ] **Kinematic Configuration**
  - DH parameters (Denavit-Hartenberg notation)
  - Link lengths (mm)
  - Joint offset angles
  - Working envelope dimensions (reach, height)
  - Joint ranges (min/max angles for each axis)

- [ ] **Weight & Payload**
  - Robot arm weight (kg)
  - Maximum payload capacity (kg)
  - Payload at maximum reach
  - Center of gravity locations

- [ ] **Performance Specifications**
  - Maximum joint velocities (deg/s or rad/s)
  - Maximum joint accelerations
  - Rated continuous torque per joint
  - Peak torque per joint
  - Position repeatability specification

### 1.2 Turning Bed/Rotary Table
- [ ] **Specifications**
  - Diameter and load capacity
  - Rotation range (continuous or limited)
  - Maximum rotational speed (RPM)
  - Positioning accuracy
  - Brake and holding torque

- [ ] **Drive System**
  - Motor type and specifications
  - Gear ratio
  - Encoder type and resolution

### 1.3 End Effector/Spindle
- [ ] **Tool Interface**
  - Mounting interface type (ISO, HSK, etc.)
  - Tool changer type (if applicable)
  - Maximum tool weight

- [ ] **Spindle Specifications**
  - Power rating (kW)
  - Speed range (RPM)
  - Torque curve
  - Cooling system type
  - Control interface (analog, digital, bus)

---

## 2. Electrical & Control Systems

### 2.1 Motor & Drive Information
For each axis (Axis 1-5 + turning bed):

- [ ] **Motor Specifications**
  - Motor type (servo, stepper, brushless DC, etc.)
  - Manufacturer and model number
  - Voltage rating (VDC or VAC)
  - Current rating (continuous and peak)
  - Power rating (W)
  - Torque constant (Nm/A)
  - Speed constant (RPM/V)
  - Electrical time constant
  - Mechanical time constant
  - Rotor inertia

- [ ] **Encoder Specifications**
  - Encoder type (incremental, absolute, resolver)
  - Resolution (pulses per revolution)
  - Number of channels (A, B, Z, etc.)
  - Output type (differential, single-ended)
  - Communication protocol

- [ ] **Motor Driver/Amplifier**
  - Manufacturer and model number
  - Control mode capabilities (position, velocity, torque)
  - Input command type (±10V analog, PWM, digital bus)
  - Communication protocol (EtherCAT, CANopen, Profibus, etc.)
  - Firmware version
  - Configuration parameters

### 2.2 Communication Protocols
- [ ] **Primary Control Bus**
  - Protocol type (EtherCAT, CANopen, Profibus, etc.)
  - Bus speed and cycle time
  - Network topology diagram
  - Device addresses/node IDs

- [ ] **Secondary Interfaces**
  - Ethernet connectivity
  - USB or serial ports
  - Fieldbus connections
  - Wireless interfaces (if any)

### 2.3 Power Systems
- [ ] **Main Power Supply**
  - Input voltage and phase (single/three-phase)
  - Power consumption (kW)
  - Circuit breaker ratings
  - Power distribution diagram

- [ ] **Control Power**
  - 24VDC supply specifications
  - 5VDC/12VDC requirements
  - Battery backup (if applicable)

- [ ] **Power Distribution**
  - Wiring diagrams
  - Connector types and pinouts
  - Cable specifications (gauge, shielding)
  - Grounding scheme

### 2.4 Safety Systems
- [ ] **Emergency Stop System**
  - E-stop button locations
  - E-stop circuit diagram
  - Safety relay specifications
  - Response time requirements

- [ ] **Safety Interlocks**
  - Door interlocks
  - Light curtains
  - Pressure-sensitive mats
  - Safety PLC (if applicable)

- [ ] **Limit Switches**
  - Hardware limit switch locations
  - Software limit configurations
  - Homing switch positions

- [ ] **Monitoring Systems**
  - Temperature sensors
  - Vibration sensors
  - Current monitoring
  - Fault detection logic

---

## 3. Sensors & Feedback Systems

### 3.1 Existing Sensors
- [ ] **Position Sensors**
  - Linear encoders (if any)
  - Rotary encoders (documented above)
  - Laser interferometers
  - Calibration data

- [ ] **Force/Torque Sensors**
  - Current sensors (if any)
  - Dedicated force sensors
  - Measurement ranges
  - Calibration certificates

- [ ] **Environmental Sensors**
  - Temperature sensors
  - Vibration monitors
  - Acoustic emission sensors

### 3.2 Additional Sensors Needed for ML
- [ ] **Vision System Requirements**
  - Camera mounting locations (identified)
  - Field of view requirements
  - Lighting requirements
  - Depth sensing needs

- [ ] **Tactile/Force Sensing**
  - Force/torque sensor specifications
  - Mounting locations
  - Required sensitivity

- [ ] **Proximity/Collision Detection**
  - Sensor types selected
  - Coverage zones defined

---

## 4. Software & Control

### 4.1 Current Control Software
- [ ] **CNC Controller**
  - Manufacturer and model
  - Software version
  - License information
  - Configuration files (backup)

- [ ] **Control Algorithms**
  - Control loop structure (PID parameters)
  - Trajectory generation method
  - Interpolation algorithms
  - Compensation tables (backlash, thermal, etc.)

- [ ] **G-Code Dialect**
  - Supported G-codes list
  - Supported M-codes list
  - Custom macros and subroutines
  - Post-processor specifications

### 4.2 Programming & Interface
- [ ] **Human-Machine Interface (HMI)**
  - Software platform
  - Screen layouts and workflows
  - User access levels
  - Backup of interface configuration

- [ ] **Programming Methods**
  - Teach pendant capabilities
  - CAM software integration
  - Manual data input (MDI) functionality
  - Program storage and management

### 4.3 Data & Logs
- [ ] **Historical Data**
  - Performance logs
  - Alarm history
  - Maintenance records
  - Parts programs library

- [ ] **Calibration Data**
  - Robot calibration parameters
  - Tool offsets
  - Work offsets
  - Kinematic compensation data

---

## 5. Documentation & Reference Materials

### 5.1 Manufacturer Documentation
- [ ] **Manuals**
  - Robot operation manual
  - Maintenance manual
  - Electrical schematics
  - Pneumatic/hydraulic schematics
  - Parts catalog

- [ ] **Software Documentation**
  - Programming manual
  - Parameter manual
  - Network configuration guide
  - API documentation (if available)

- [ ] **Safety & Compliance**
  - CE marking documentation
  - Risk assessment
  - Safety manual
  - Compliance certificates

### 5.2 As-Built Documentation
- [ ] **Physical Documentation**
  - Photographs of controller interior
  - Photographs of all connectors (labeled)
  - Photographs of wiring
  - Video of system in operation

- [ ] **Electrical Drawings**
  - Updated wiring diagrams
  - Cable schedule
  - Connector pinout tables
  - Panel layout

---

## 6. Performance & Operational Data

### 6.1 Baseline Performance Metrics
- [ ] **Positioning Accuracy**
  - Measured accuracy at multiple points in workspace
  - Repeatability measurements
  - Method of measurement documented

- [ ] **Speed & Acceleration**
  - Actual maximum velocities achieved
  - Actual accelerations achieved
  - Settling times

- [ ] **Process Performance**
  - Typical cutting parameters
  - Feed rates for different materials
  - Spindle speeds
  - Tool life data

### 6.2 Operational Characteristics
- [ ] **Cycle Times**
  - Typical part cycle times
  - Best and worst case scenarios
  - Breakdown of time (cutting, rapids, tool changes)

- [ ] **Quality Metrics**
  - Surface finish achieved (Ra, Rz)
  - Dimensional accuracy (tolerances held)
  - Defect rates
  - Quality control procedures

- [ ] **Utilization Data**
  - Typical daily operating hours
  - Uptime/downtime statistics
  - Maintenance frequency
  - Failure modes and rates

---

## 7. Environmental & Installation

### 7.1 Physical Environment
- [ ] **Space Requirements**
  - Floor space occupied
  - Height clearance
  - Access requirements
  - Safety zone dimensions

- [ ] **Environmental Conditions**
  - Ambient temperature range
  - Humidity levels
  - Dust/contamination levels
  - Vibration environment

### 7.2 Utilities & Services
- [ ] **Required Utilities**
  - Compressed air (pressure, flow rate)
  - Coolant system
  - Chip removal/vacuum
  - Mist collector

- [ ] **Infrastructure**
  - Floor loading requirements
  - Foundation/mounting specifications
  - Cable routing
  - Network connectivity

---

## 8. Materials & Tooling

### 8.1 Materials Processed
- [ ] **Material Types**
  - List of materials (wood, foam, plastic, metal)
  - Material properties (hardness, density)
  - Typical stock sizes

- [ ] **Cutting Parameters**
  - Speeds and feeds database
  - Tool recommendations by material
  - Coolant requirements

### 8.2 Tooling
- [ ] **Tool Inventory**
  - Tool types used
  - Tool geometries
  - Tool holders
  - Tool measurement system

- [ ] **Tool Management**
  - Tool life monitoring
  - Tool offset measurement
  - Tool breakage detection

---

## 9. Maintenance & Support

### 9.1 Maintenance Requirements
- [ ] **Scheduled Maintenance**
  - Daily maintenance tasks
  - Weekly/monthly tasks
  - Annual tasks
  - Lubrication schedule

- [ ] **Spare Parts**
  - Critical spare parts list
  - Vendor information
  - Lead times
  - Part numbers

### 9.2 Support Resources
- [ ] **Technical Support**
  - Manufacturer support contacts
  - Service contract details
  - Training resources
  - User community forums

---

## 10. ML-Specific Requirements

### 10.1 Task Definitions
- [ ] **Current Tasks**
  - List of all tasks performed
  - Task complexity assessment
  - Task frequency
  - Success criteria

- [ ] **Desired Autonomous Tasks**
  - Tasks to be ML-enabled
  - Decision points in tasks
  - Variability and exceptions
  - Human intervention scenarios

### 10.2 Training Data Requirements
- [ ] **Demonstration Collection**
  - Methods for collecting expert demonstrations
  - Number of demonstrations needed per task
  - Variance in demonstrations
  - Annotation requirements

- [ ] **Simulation Requirements**
  - CAD models for digital twin
  - Material properties for physics sim
  - Process models (cutting forces, etc.)

---

## Information Collection Methods

### Direct Measurement
Use calibrated instruments to measure:
- Positioning accuracy (laser tracker, CMM)
- Velocities and accelerations (encoders, tachometers)
- Forces and torques (force gauges, current meters)
- Environmental conditions (thermometer, hygrometer)

### Data Extraction
Extract from existing controller:
- Parameter files
- Configuration databases
- Log files
- Program libraries

### Documentation Review
Thoroughly review:
- All manufacturer manuals
- Previous service records
- Modification history
- Training materials

### Operational Observation
Document through observation:
- Operator workflows
- Common issues and workarounds
- Emergency procedures
- Quality inspection methods

### Testing & Validation
Conduct controlled tests:
- Run test parts and measure results
- Execute diagnostic routines
- Test safety systems
- Verify limit conditions

---

## Data Organization & Storage

### Folder Structure
```
kuka_system_documentation/
├── 1_mechanical/
│   ├── specifications/
│   ├── cad_models/
│   ├── photos/
│   └── measurements/
├── 2_electrical/
│   ├── schematics/
│   ├── wiring_diagrams/
│   ├── component_specs/
│   └── photos/
├── 3_control_software/
│   ├── backups/
│   ├── parameters/
│   ├── programs/
│   └── configurations/
├── 4_documentation/
│   ├── manuals/
│   ├── certifications/
│   └── procedures/
├── 5_performance_data/
│   ├── measurements/
│   ├── logs/
│   └── benchmarks/
└── 6_ml_requirements/
    ├── task_definitions/
    ├── demonstration_videos/
    └── simulation_assets/
```

### Documentation Standards
- All measurements include units, date, person, method
- Photos include scale reference, labels, date
- Videos include timestamp, description of what's shown
- Files named descriptively: `YYYY-MM-DD_description_version.ext`
- Maintain revision history for all documents

---

## Verification Checklist

Before proceeding to design phase, verify:
- [ ] All critical specifications have been documented
- [ ] Measurement accuracy is sufficient for design
- [ ] Documentation has been reviewed by at least 2 people
- [ ] Backups of all data have been created
- [ ] Unknowns have been clearly identified
- [ ] Access to original equipment for validation questions
- [ ] Manufacturer has been contacted for unavailable info
- [ ] Safety-critical information has been triple-checked

---

## Contact Information

Maintain list of key contacts:
- Original equipment manufacturer technical support
- Motor/drive suppliers
- Sensor suppliers
- Previous integrators (if any)
- Subject matter experts
- Regulatory/compliance consultants
