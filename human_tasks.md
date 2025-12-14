# Human Task Documentation
## Kuka Robot Arm AI-Driven Controller Replacement Project

**Document Version:** 1.0  
**Date:** December 14, 2025  
**Project Phase:** Planning & Documentation  
**Document Type:** Human Task Procedures and Safety Guidelines

---

## ⚠️ CRITICAL SAFETY WARNING ⚠️

**THIS SYSTEM OPERATES AT 480V AC 3-PHASE POWER - EXTREMELY DANGEROUS**

- **480V AC can cause FATAL electrocution**
- **Arc flash hazard can cause severe burns even without direct contact**
- **ALL electrical work MUST be performed by licensed electricians**
- **NEVER work alone on high-voltage systems**
- **ALWAYS follow Lockout/Tagout (LOTO) procedures**
- **Arc-rated PPE is MANDATORY for all high-voltage work**

**If you are not qualified to work with 480V systems, DO NOT proceed. Contact a licensed electrician immediately.**

---

## Table of Contents

1. [Overview and Introduction](#1-overview-and-introduction)
2. [Personnel Qualifications and Certifications](#2-personnel-qualifications-and-certifications)
3. [Required Equipment and Tools](#3-required-equipment-and-tools)
4. [Safety Protocols and Training](#4-safety-protocols-and-training)
5. [Hardware Setup and Wiring Procedures](#5-hardware-setup-and-wiring-procedures)
6. [Sensor Installation and Calibration](#6-sensor-installation-and-calibration)
7. [Safety System Verification and Compliance](#7-safety-system-verification-and-compliance)
8. [System Integration Procedures](#8-system-integration-procedures)
9. [Testing Protocols and Validation](#9-testing-protocols-and-validation)
10. [Troubleshooting Guides](#10-troubleshooting-guides)
11. [Documentation and Reporting Requirements](#11-documentation-and-reporting-requirements)
12. [Appendices](#12-appendices)

---

## 1. Overview and Introduction

### 1.1 Project Overview

This document provides comprehensive human task procedures for replacing the traditional Kuka KR C2 controller with an AI-driven system powered by an NVIDIA Jetson Orin Nano Super. The project involves:

- **Replacing legacy controller** with ML-based system
- **Installing new motor drives** (EtherCAT-compatible, 480V-rated)
- **Integrating sensors** (cameras, force/torque, encoders)
- **Implementing safety systems** (ISO 13849-1 Category 3)
- **Testing and validation** of complete system

### 1.2 System Specifications

**Current System:**
- **Controller:** Kuka KR C2 (MP 9 variant)
- **Motor Drives:** UNI2402 (6 drives, 7.5kW each)
- **Power:** 380-480V AC, 3-Phase, 50/60Hz
- **Total Power:** ~50kW (67 HP)
- **Robot Model:** KR 150/180/210 (to be confirmed)

**New System:**
- **Controller:** NVIDIA Jetson Orin Nano Super
- **Motor Drives:** Kollmorgen AKD-P or Beckhoff AX5000 (480V variants)
- **Communication:** EtherCAT network (1kHz cycle time)
- **Safety:** Category 3, Performance Level d (PLd)

### 1.3 Document Purpose

This document provides:
- **Step-by-step procedures** for hardware installation
- **Safety protocols** for high-voltage work
- **Verification checklists** for each task
- **Troubleshooting guides** for common issues
- **Documentation templates** for compliance

### 1.4 Document Scope

**Included:**
- Hardware setup and wiring
- Sensor installation and calibration
- Safety system verification
- System integration procedures
- Testing and validation protocols

**Excluded:**
- Software development tasks (see coding_tasks.md)
- ML model training procedures
- G-code programming
- Advanced troubleshooting requiring software debugging

### 1.5 Reference Documents

This document is based on:
- **project_analysis.md** - Comprehensive project analysis
- **ISO 13849-1** - Safety of machinery
- **IEC 61800-5-2** - Safety functions in drive systems
- **NFPA 70E** - Electrical safety in the workplace
- **Kuka KR C2 Technical Documentation**

---

## 2. Personnel Qualifications and Certifications

### 2.1 Required Qualifications

#### 2.1.1 Electrical Work (High Voltage)

**MANDATORY REQUIREMENTS:**
- ✅ Licensed electrician (state/local requirements)
- ✅ NFPA 70E Electrical Safety Training (current certification)
- ✅ Arc Flash Protection Training
- ✅ Lockout/Tagout (LOTO) Training
- ✅ First Aid/CPR with electrical injury focus
- ✅ Minimum 5 years experience with industrial 480V systems

**ADDITIONAL QUALIFICATIONS:**
- Experience with motor drive systems
- Knowledge of EtherCAT or industrial fieldbus protocols
- Familiarity with safety relay systems

#### 2.1.2 Mechanical Work

**REQUIRED:**
- ✅ Mechanical engineering background or equivalent experience
- ✅ Experience with industrial robotics
- ✅ Knowledge of robot kinematics and calibration
- ✅ Familiarity with precision measurement tools

**PREFERRED:**
- Kuka robot experience
- CNC machine experience
- CAD software proficiency

#### 2.1.3 Integration and Testing

**REQUIRED:**
- ✅ Systems integration experience
- ✅ Industrial automation background
- ✅ Understanding of safety systems
- ✅ Experience with commissioning procedures

**PREFERRED:**
- EtherCAT network configuration experience
- Robot programming experience
- Quality assurance background

### 2.2 Safety Certifications

**MANDATORY FOR ALL TEAM MEMBERS:**

| Certification | Provider | Validity | Renewal |
|--------------|----------|----------|---------|
| NFPA 70E Electrical Safety | Qualified Training Provider | 3 years | Required |
| Arc Flash Protection | OSHA-approved Provider | 3 years | Required |
| Lockout/Tagout (LOTO) | OSHA-approved Provider | Annual | Required |
| First Aid/CPR | Red Cross or equivalent | 2 years | Required |

**ADDITIONAL FOR ELECTRICAL PERSONNEL:**

| Certification | Provider | Validity | Renewal |
|--------------|----------|----------|---------|
| Licensed Electrician | State Licensing Board | Varies | As required |
| High Voltage Safety | Industry Training Provider | 3 years | Required |
| Electrical Safety Auditor | NFPA or equivalent | 5 years | Optional |

### 2.3 Team Roles and Responsibilities

#### Electrical Lead (Licensed Electrician)
- **Responsibilities:**
  - All 480V power system work
  - Motor drive installation and wiring
  - Safety system electrical installation
  - Electrical permits and inspections
  - Arc flash hazard analysis
  - LOTO procedure implementation

#### Mechanical Lead
- **Responsibilities:**
  - Sensor mounting and installation
  - Mechanical interface design
  - Robot calibration procedures
  - Precision measurement and validation
  - Mechanical documentation

#### Integration Lead
- **Responsibilities:**
  - System integration coordination
  - Network configuration (EtherCAT)
  - Component interfacing
  - Testing protocol execution
  - Documentation and reporting

#### Safety Officer
- **Responsibilities:**
  - Safety protocol enforcement
  - Risk assessment and mitigation
  - Safety training coordination
  - Incident investigation
  - Compliance verification

---

## 3. Required Equipment and Tools

### 3.1 Safety Equipment (MANDATORY)

#### 3.1.1 Personal Protective Equipment (PPE)

**Arc-Rated PPE (Minimum Category 2 for 480V):**

| Item | Specification | Quantity | Notes |
|------|--------------|----------|-------|
| Arc-rated shirt/jacket | Min 8 cal/cm² | 1 per person | Long sleeves required |
| Arc-rated pants | Min 8 cal/cm² | 1 per person | No synthetic materials |
| Arc-rated face shield | Min 8 cal/cm² | 1 per person | Full face coverage |
| Voltage-rated gloves | Class 2 (17kV) for 480V | 2 pairs | Inspect before each use |
| Leather protector gloves | For voltage-rated gloves | 2 pairs | Worn over voltage gloves |
| Safety glasses | ANSI Z87.1 rated | 1 per person | Always worn |
| Hard hat | Class E (electrical) | 1 per person | Non-conductive |
| Insulated safety boots | ASTM F2413 | 1 pair per person | Steel toe, electrical hazard rated |
| Hearing protection | NRR 25+ | 1 per person | For testing phases |

**Additional Safety Equipment:**

| Item | Specification | Quantity | Purpose |
|------|--------------|----------|---------|
| Insulated mat | 36" x 48", 30kV rated | 2 | Work area protection |
| Voltage detector | Non-contact, CAT IV 600V | 2 | Verify de-energized |
| Multimeter | CAT III/IV 600V+ | 2 | Voltage measurement |
| Insulated tools set | 1000V rated | 1 set | All electrical work |
| LOTO kit | Padlocks, tags, hasps | 1 per person | Energy isolation |
| Fire extinguisher | Class C (electrical) | 2 | Within 25 feet of work area |
| First aid kit | Industrial, electrical injury supplies | 1 | Readily accessible |

### 3.2 Measurement and Testing Equipment

#### 3.2.1 Electrical Testing

| Equipment | Specification | Purpose |
|-----------|--------------|---------|
| Digital multimeter | Fluke 87V or equivalent, CAT III 1000V | Voltage, current, resistance measurement |
| Clamp meter | Fluke 376 or equivalent | Current measurement without breaking circuit |
| Megohmmeter | 500V/1000V insulation tester | Insulation resistance testing |
| Power quality analyzer | Fluke 435 or equivalent | 3-phase power analysis |
| Oscilloscope | 100MHz, 4-channel | Signal analysis, encoder verification |
| Ground resistance tester | Fluke 1625 or equivalent | Grounding system verification |

#### 3.2.2 Mechanical Measurement

| Equipment | Specification | Purpose |
|-----------|--------------|---------|
| Laser tracker or CMM | ±0.01mm accuracy | Robot positioning accuracy measurement |
| Dial indicator set | 0.001mm resolution | Mechanical alignment |
| Digital calipers | 0.01mm resolution | Dimension verification |
| Torque wrench set | 5-200 Nm range | Proper fastener torque |
| Level (precision) | 0.02mm/m accuracy | Mounting surface verification |
| Tape measure | 25ft, metric/imperial | General measurements |

#### 3.2.3 Network and Communication

| Equipment | Specification | Purpose |
|-----------|--------------|---------|
| Network cable tester | CAT5e/CAT6 certification | EtherCAT cable verification |
| Laptop with EtherCAT tools | Windows/Linux, TwinCAT or equivalent | Network configuration and diagnostics |
| USB-to-serial adapter | FTDI chipset recommended | Legacy device communication |
| Logic analyzer | 8+ channels, 100MHz+ | Protocol debugging |

### 3.3 Installation Tools

#### 3.3.1 Hand Tools

| Tool | Specification | Quantity |
|------|--------------|----------|
| Screwdriver set | Insulated, 1000V rated | 1 set |
| Allen key set | Metric, 1.5-10mm | 2 sets |
| Wrench set | Metric, 8-24mm | 1 set |
| Socket set | Metric, 8-24mm | 1 set |
| Wire strippers | 12-24 AWG | 2 |
| Crimping tool | Ferrule and terminal crimper | 1 |
| Cable cutters | Heavy duty | 2 |
| Pliers set | Needle nose, diagonal, linesman | 1 set |
| Utility knife | Retractable blade | 2 |

#### 3.3.2 Power Tools

| Tool | Specification | Notes |
|------|--------------|-------|
| Drill/driver | 18V cordless | With bit set |
| Impact driver | 18V cordless | For heavy fasteners |
| Angle grinder | 4.5", with cut-off and grinding wheels | For metal work |
| Heat gun | Variable temperature | For heat shrink tubing |
| Label maker | Industrial grade | For wire and component labeling |

### 3.4 Consumables and Supplies

#### 3.4.1 Electrical Supplies

| Item | Specification | Estimated Quantity |
|------|--------------|-------------------|
| Wire (power) | 10 AWG, THHN, 600V | 500 ft |
| Wire (control) | 18 AWG, shielded, 300V | 1000 ft |
| Wire (signal) | 22 AWG, shielded twisted pair | 500 ft |
| EtherCAT cable | CAT5e/CAT6, shielded, industrial | 100 ft |
| Ferrules | Assorted sizes, 18-10 AWG | 500 pcs |
| Terminal blocks | DIN rail mount, various sizes | 50 pcs |
| Cable ties | UV-resistant, various sizes | 500 pcs |
| Heat shrink tubing | Assorted sizes and colors | 1 kit |
| Electrical tape | 3M Super 33+, black | 10 rolls |
| Wire labels | Thermal transfer, industrial | 500 labels |
| Conduit | Flexible and rigid, various sizes | As needed |
| Cable glands | M12, M16, M20 | 50 pcs |

#### 3.4.2 Mounting Hardware

| Item | Specification | Estimated Quantity |
|------|--------------|-------------------|
| DIN rail | 35mm, aluminum | 10 ft |
| Mounting brackets | Various sizes | 20 pcs |
| Standoffs | M4, M5, M6, various lengths | 100 pcs |
| Screws/bolts | Metric, M4-M10, various lengths | Assorted kit |
| Washers | Metric, M4-M10 | Assorted kit |
| Lock washers | Metric, M4-M10 | Assorted kit |
| Nuts | Metric, M4-M10 | Assorted kit |

---

## 4. Safety Protocols and Training

### 4.1 High Voltage Safety Procedures

#### 4.1.1 General High Voltage Safety Rules

**ALWAYS:**
- ✅ Assume all circuits are energized until proven otherwise
- ✅ Use proper PPE for the voltage level and arc flash hazard
- ✅ Follow LOTO procedures before any work
- ✅ Verify de-energized state with voltage detector
- ✅ Work with a qualified observer (never alone)
- ✅ Maintain proper working distances
- ✅ Keep work area clean and organized
- ✅ Use insulated tools rated for voltage level
- ✅ Inspect all equipment before use
- ✅ Know location of emergency shutoff and first aid

**NEVER:**
- ❌ Work on energized circuits unless absolutely necessary
- ❌ Bypass safety interlocks or devices
- ❌ Work alone on high voltage systems
- ❌ Use damaged tools or equipment
- ❌ Wear jewelry or conductive items
- ❌ Work when fatigued or distracted
- ❌ Rush or take shortcuts
- ❌ Assume someone else locked out the system

#### 4.1.2 Arc Flash Hazard

**Understanding Arc Flash:**
- Arc flash is an explosive release of energy from electrical equipment
- Can reach temperatures of 35,000°F (19,400°C)
- Can cause severe burns, blindness, hearing loss, and death
- Can occur even without direct contact with conductors
- 480V 3-phase systems have significant arc flash hazard

**Arc Flash Boundaries:**

| Boundary | Distance | PPE Required | Who Can Enter |
|----------|----------|--------------|---------------|
| Limited | Calculated per NFPA 70E | Standard work clothes | Qualified persons only |
| Restricted | Calculated per NFPA 70E | Arc-rated PPE (Category 2+) | Qualified persons with training |
| Prohibited | Calculated per NFPA 70E | Maximum arc-rated PPE | Qualified persons with specific authorization |

**Arc Flash PPE Categories for 480V Systems:**

For this project, **minimum Category 2** PPE is required:
- Arc-rated clothing (min 8 cal/cm²)
- Arc-rated face shield
- Safety glasses
- Hearing protection
- Voltage-rated gloves with leather protectors
- Hard hat (Class E)

#### 4.1.3 Lockout/Tagout (LOTO) Procedures

**LOTO Purpose:**
- Prevent accidental energization during maintenance
- Protect personnel from electrical hazards
- Ensure only authorized personnel can restore power

**LOTO Procedure Steps:**

**Step 1: Preparation**
- [ ] Identify all energy sources (480V main, 24V control, compressed air, etc.)
- [ ] Notify all affected personnel
- [ ] Review equipment documentation
- [ ] Gather LOTO devices and PPE

**Step 2: Shutdown**
- [ ] Follow normal shutdown procedures
- [ ] Verify all axes are stopped
- [ ] Engage mechanical brakes if present
- [ ] Press emergency stop button

**Step 3: Isolation**
- [ ] Open main circuit breaker (480V)
- [ ] Open control power disconnect (24V)
- [ ] Close and lock all disconnect switches
- [ ] Disconnect compressed air (if applicable)
- [ ] Disconnect any other energy sources

**Step 4: Lockout**
- [ ] Apply lockout device to each energy isolation point
- [ ] Each person working on equipment applies their own lock
- [ ] Attach tag with name, date, and reason for lockout
- [ ] Verify locks are secure and cannot be removed without key

**Step 5: Stored Energy Release**
- [ ] Discharge capacitors in drives (wait 5 minutes minimum)
- [ ] Release hydraulic/pneumatic pressure
- [ ] Block or support moving parts
- [ ] Verify all stored energy is released

**Step 6: Verification**
- [ ] Use voltage detector to verify de-energized state
- [ ] Test at multiple points in the circuit
- [ ] Attempt to start equipment (should not start)
- [ ] Verify zero voltage with multimeter
- [ ] Place "DO NOT OPERATE" tags on controls

**Step 7: Work Completion**
- [ ] Remove all tools and equipment
- [ ] Reinstall guards and covers
- [ ] Verify all personnel are clear
- [ ] Remove tags and locks (only by person who installed them)
- [ ] Restore energy sources in reverse order
- [ ] Test equipment operation

**LOTO Documentation:**

| Date | Equipment | Energy Sources | Locked Out By | Lock # | Restored By | Time |
|------|-----------|----------------|---------------|--------|-------------|------|
| | | | | | | |

### 4.2 Mechanical Safety Procedures

#### 4.2.1 Robot Movement Hazards

**Hazards:**
- Crushing between robot and fixed objects
- Impact from moving robot arm
- Pinch points at joints
- Unexpected motion during testing

**Safety Measures:**
- ✅ Establish safety perimeter (minimum 2m from robot reach)
- ✅ Use safety fencing or light curtains
- ✅ Post warning signs
- ✅ Limit speed during testing (25% maximum initially)
- ✅ Use teach pendant with deadman switch
- ✅ Ensure emergency stop buttons are accessible
- ✅ Never enter robot workspace during operation

#### 4.2.2 Lifting and Handling

**Motor Drives (each ~15-20 kg):**
- Use proper lifting technique (bend knees, straight back)
- Two-person lift if necessary
- Use lifting equipment for panel installation

**Robot Arm (payload 150-210 kg):**
- DO NOT attempt to move without proper equipment
- Use overhead crane or forklift
- Secure with appropriate rigging
- Follow manufacturer's lifting procedures

### 4.3 Emergency Procedures

#### 4.3.1 Electrical Shock Response

**If someone receives electrical shock:**

1. **DO NOT TOUCH THE VICTIM** if still in contact with electrical source
2. **DE-ENERGIZE** the circuit immediately (emergency stop or main breaker)
3. **Call 911** immediately
4. **Begin CPR** if victim is unconscious and not breathing
5. **Treat for shock** - keep victim warm and lying down
6. **Do not move victim** unless in immediate danger
7. **Wait for emergency medical services**

**Important:**
- Electrical shock can cause cardiac arrest even with no visible injuries
- Victim must be evaluated by medical professionals even if appears okay
- Document incident thoroughly

#### 4.3.2 Arc Flash Injury Response

**If arc flash occurs:**

1. **Evacuate area** immediately
2. **Call 911** for medical emergency
3. **Do not remove burned clothing** (may be fused to skin)
4. **Cool burns** with clean water (not ice)
5. **Cover burns** with clean, dry cloth
6. **Treat for shock**
7. **Secure the scene** - prevent others from entering
8. **Document incident**

#### 4.3.3 Fire Response

**If electrical fire occurs:**

1. **Activate fire alarm**
2. **Evacuate personnel**
3. **Call 911**
4. **Use Class C fire extinguisher** if safe to do so
5. **DO NOT use water** on electrical fires
6. **Close doors** to contain fire
7. **Meet at designated assembly point**
8. **Account for all personnel**

#### 4.3.4 Emergency Stop Activation

**When to activate emergency stop:**
- Unexpected robot motion
- Personnel in danger zone
- Equipment malfunction
- Unusual sounds or smells
- Any unsafe condition

**After emergency stop:**
- [ ] Identify and resolve cause
- [ ] Inspect for damage
- [ ] Document incident
- [ ] Reset only when safe
- [ ] Notify supervisor

### 4.4 Required Safety Training

#### 4.4.1 Pre-Project Training (All Personnel)

**Week 1 - Before Any Work Begins:**

| Training | Duration | Provider | Certification |
|----------|----------|----------|---------------|
| NFPA 70E Electrical Safety | 8 hours | Qualified instructor | Required |
| Arc Flash Protection | 4 hours | Qualified instructor | Required |
| Lockout/Tagout (LOTO) | 4 hours | OSHA-approved | Required |
| First Aid/CPR | 8 hours | Red Cross or equivalent | Required |
| Project Safety Overview | 2 hours | Safety Officer | Attendance record |

**Week 2 - Role-Specific Training:**

| Role | Training | Duration |
|------|----------|----------|
| Electrical Lead | High Voltage Work Practices | 8 hours |
| All Personnel | Robot Safety Awareness | 2 hours |
| Integration Team | EtherCAT Safety | 2 hours |
| All Personnel | Emergency Response Procedures | 2 hours |

#### 4.4.2 Ongoing Safety Training

**Monthly:**
- Safety toolbox talks (30 minutes)
- Incident review and lessons learned
- PPE inspection and replacement

**Quarterly:**
- LOTO procedure review and practice
- Emergency response drill
- Safety equipment inspection

**Annual:**
- LOTO recertification
- Safety training refresher
- First Aid/CPR renewal (as needed)

### 4.5 Safety Checklists

#### 4.5.1 Daily Safety Checklist

**Before Starting Work Each Day:**

- [ ] All personnel have required PPE
- [ ] PPE inspected and in good condition
- [ ] Work area clean and organized
- [ ] Emergency stop buttons tested
- [ ] Fire extinguisher present and charged
- [ ] First aid kit accessible
- [ ] Emergency contact numbers posted
- [ ] All personnel briefed on day's tasks
- [ ] Hazards identified and mitigated
- [ ] Communication plan established

#### 4.5.2 Pre-Energization Safety Checklist

**Before Applying Power:**

- [ ] All wiring inspected and verified
- [ ] All connections tight and secure
- [ ] No exposed conductors
- [ ] Proper grounding verified
- [ ] Insulation resistance tested (>1MΩ)
- [ ] All personnel clear of equipment
- [ ] Guards and covers installed
- [ ] Emergency stop circuit tested
- [ ] Safety interlocks verified
- [ ] Voltage detector and multimeter ready
- [ ] Arc-rated PPE worn
- [ ] Observer present
- [ ] Supervisor approval obtained

---

## 5. Hardware Setup and Wiring Procedures

### 5.1 Pre-Installation Preparation

#### 5.1.1 System Backup (CRITICAL - Do First)

**Purpose:** Preserve existing system configuration before any modifications

**Procedure:**

**Step 1: Document Current System**
- [ ] Photograph entire system (minimum 100 photos)
  - Overall system views (4 angles)
  - Each motor drive (front, connections)
  - Control cabinet interior (multiple angles)
  - All wiring and cable routing
  - All labels and nameplates
  - Pendant and operator interface
- [ ] Video record system operation (10+ minutes)
  - Normal startup sequence
  - Typical operations
  - Shutdown sequence
- [ ] Create photo/video index document

**Step 2: Backup KR C2 Controller**
- [ ] Connect to KR C2 via KCP (Kuka Control Panel) or USB
- [ ] Navigate to backup menu
- [ ] Create full system backup including:
  - All KRL programs (C:\KRC\ROBOTER\)
  - Configuration files (C:\KRC\STEU\)
  - System parameters
  - User data
  - Calibration data
- [ ] Save backup to multiple locations:
  - USB drive #1 (keep with system)
  - USB drive #2 (off-site storage)
  - Network storage
- [ ] Verify backup integrity by checking file sizes and dates
- [ ] Test restore procedure on same controller (if possible)

**Step 3: Document Electrical System**
- [ ] Create wiring diagram of current system
- [ ] Label all wires before disconnection (use label maker)
- [ ] Measure and record all voltages:
  - Main power (480V 3-phase)
  - Control power (24V DC)
  - Signal voltages
- [ ] Document all circuit breaker settings
- [ ] Photograph electrical panel before any changes

**Step 4: Identify Robot Model**
- [ ] Locate nameplate on robot base
- [ ] Record exact model number (KR 150, 180, or 210)
- [ ] Record serial number
- [ ] Record manufacturing date
- [ ] Photograph nameplate
- [ ] Obtain technical documentation from Kuka if available

**Step 5: Measure Performance Baseline**
- [ ] Run standard test program
- [ ] Measure positioning accuracy (use laser tracker or CMM)
- [ ] Measure repeatability (10+ cycles)
- [ ] Record cycle times
- [ ] Document surface finish quality
- [ ] Save baseline data for comparison

#### 5.1.2 Site Preparation

**Step 1: Work Area Setup**
- [ ] Clear minimum 3m radius around robot
- [ ] Establish designated work zones:
  - High voltage work area (restricted access)
  - Assembly/testing area
  - Tool and equipment storage
  - Documentation station
- [ ] Install temporary lighting if needed
- [ ] Ensure adequate ventilation
- [ ] Set up workbenches and tool storage

**Step 2: Safety Equipment Installation**
- [ ] Install emergency stop buttons (minimum 2 locations)
- [ ] Post safety signs:
  - "DANGER - HIGH VOLTAGE"
  - "AUTHORIZED PERSONNEL ONLY"
  - "ARC FLASH HAZARD"
  - Emergency contact numbers
- [ ] Install safety barriers/fencing
- [ ] Position fire extinguishers (within 25 feet)
- [ ] Set up first aid station
- [ ] Install LOTO station with locks and tags

**Step 3: Electrical Preparation**
- [ ] Verify available power capacity (100A+ at 480V)
- [ ] Inspect existing electrical panel
- [ ] Identify main disconnect location
- [ ] Verify grounding system integrity
- [ ] Check for code violations in existing installation
- [ ] Obtain electrical permits (if required by local code)
- [ ] Schedule licensed electrician

**Step 4: Component Receiving and Inspection**
- [ ] Verify all components received against packing list
- [ ] Inspect for shipping damage
- [ ] Check component specifications match order
- [ ] Test components if possible (bench test drives, etc.)
- [ ] Store components in clean, dry location
- [ ] Organize components by installation phase

### 5.2 Power System Installation

**⚠️ WARNING: ALL POWER SYSTEM WORK MUST BE PERFORMED BY LICENSED ELECTRICIAN ⚠️**

#### 5.2.1 Power System Architecture

**System Overview:**
```
480V 3-Phase AC Input (existing)
     |
[Main Disconnect - 100A]
     |
[Isolating Transformer - REQUIRED for safety]
     |
[Main Circuit Breaker - 30A]
     |
+----+----+----+----+----+----+
|    |    |    |    |    |    |
Dr1  Dr2  Dr3  Dr4  Dr5  Dr6  [Step Down Transformer]
(7.5kW each)                   |
                               |
                          [24V DC Power Supply - Control]
                               |
                          [5V DC Power Supply - Jetson]
```

**Power Requirements:**
- **Motor Drives:** 6 × 7.5kW = 45kW
- **Spindle:** 3-5kW
- **Control Systems:** 500W
- **Total:** ~50kW (67 HP)
- **Input Current:** ~100A at 480V 3-phase

#### 5.2.2 Isolating Transformer Installation

**Purpose:** Provides electrical isolation and reduces ground fault hazards

**Specifications:**
- **Rating:** 50kVA minimum
- **Primary:** 480V 3-phase
- **Secondary:** 480V 3-phase (isolated)
- **Type:** Dry-type, K-factor rated
- **Cost:** ~$2,500

**Installation Procedure (Licensed Electrician Only):**

**Step 1: Pre-Installation**
- [ ] Verify transformer specifications
- [ ] Check mounting location (adequate clearance)
- [ ] Verify floor load capacity
- [ ] Ensure adequate ventilation
- [ ] Review electrical code requirements

**Step 2: LOTO Procedure**
- [ ] Follow Section 4.1.3 LOTO procedures
- [ ] Lock out main 480V disconnect
- [ ] Verify de-energized with voltage detector
- [ ] Test with multimeter (0V confirmed)
- [ ] Place "DO NOT OPERATE" tags

**Step 3: Mechanical Installation**
- [ ] Position transformer on mounting pad
- [ ] Level transformer (use precision level)
- [ ] Secure to floor (anchor bolts)
- [ ] Verify clearances per NEC:
  - Front: 36" minimum
  - Sides: 12" minimum
  - Top: 36" minimum

**Step 4: Primary Wiring (480V Input)**
- [ ] Wear full arc-rated PPE
- [ ] Route primary conductors in conduit
- [ ] Use 10 AWG minimum (based on load calculation)
- [ ] Connect to primary terminals:
  - L1 (Phase A)
  - L2 (Phase B)
  - L3 (Phase C)
- [ ] Torque terminals per manufacturer spec
- [ ] Install primary overcurrent protection (100A breaker)

**Step 5: Secondary Wiring (480V Output)**
- [ ] Route secondary conductors in separate conduit
- [ ] Use 10 AWG minimum
- [ ] Connect to secondary terminals:
  - L1' (Phase A)
  - L2' (Phase B)
  - L3' (Phase C)
- [ ] Torque terminals per manufacturer spec
- [ ] Install secondary overcurrent protection (30A breaker)

**Step 6: Grounding**
- [ ] Connect transformer case to building ground
- [ ] Use 6 AWG minimum ground conductor
- [ ] Verify ground resistance <5Ω (use ground resistance tester)
- [ ] Bond secondary neutral (if applicable)
- [ ] Label all ground connections

**Step 7: Testing**
- [ ] Verify all connections tight
- [ ] Measure insulation resistance (>1MΩ)
- [ ] Remove LOTO devices
- [ ] Energize primary (stand clear)
- [ ] Measure secondary voltage (should be 480V ±5%)
- [ ] Check phase rotation (A-B-C)
- [ ] Measure voltage balance (<2% imbalance)
- [ ] Check for unusual sounds or smells
- [ ] De-energize and re-apply LOTO

**Step 8: Documentation**
- [ ] Update electrical drawings
- [ ] Install arc flash label (calculated per NFPA 70E)
- [ ] Record test results
- [ ] Obtain electrical inspection (if required)

#### 5.2.3 Motor Drive Installation

**Drives to Install:**
- **Option 1:** Kollmorgen AKD-P01207 (7.5kW, 480V) - $1,200 each
- **Option 2:** Beckhoff AX5206 (6.5kW, 480V) - $1,000 each
- **Quantity:** 6 drives (5 axes + turning bed)

**Installation Procedure (Licensed Electrician Only):**

**Step 1: Drive Mounting**
- [ ] Verify mounting location in control cabinet
- [ ] Ensure adequate spacing between drives (minimum 50mm)
- [ ] Ensure adequate ventilation (top and bottom clearance)
- [ ] Mount drives on DIN rail or backplane
- [ ] Secure with mounting brackets
- [ ] Verify drives are level and secure

**Step 2: Power Wiring (480V AC Input)**

**⚠️ CRITICAL: Follow LOTO procedures before any wiring ⚠️**

For each drive:
- [ ] Route power conductors in conduit (separate from signal cables)
- [ ] Use shielded power cable (10 AWG minimum)
- [ ] Connect to drive power terminals:
  - L1 (Phase A from transformer secondary)
  - L2 (Phase B from transformer secondary)
  - L3 (Phase C from transformer secondary)
  - PE (Protective Earth - 6 AWG minimum)
- [ ] Torque terminals per manufacturer specification
- [ ] Install individual circuit breakers (20A per drive)
- [ ] Label all power connections clearly

**Step 3: Motor Wiring (480V AC Output)**

For each drive:
- [ ] Route motor cables in conduit (separate from signal cables)
- [ ] Use shielded motor cable (10 AWG minimum)
- [ ] Connect to drive motor terminals:
  - U (Motor Phase 1)
  - V (Motor Phase 2)
  - W (Motor Phase 3)
  - PE (Motor ground)
- [ ] Connect to motor terminals (verify motor nameplate)
- [ ] Torque terminals per manufacturer specification
- [ ] Verify motor winding resistance (should be balanced)
- [ ] Measure insulation resistance (>1MΩ)
- [ ] Label all motor connections

**Step 4: Brake Wiring (24V DC)**

For each axis with brake:
- [ ] Identify brake wires (typically red/black)
- [ ] Connect to drive brake output terminals
- [ ] Verify brake voltage (24V DC typical)
- [ ] Verify brake resistance (check motor documentation)
- [ ] Test brake operation (mechanical test, no power)
- [ ] Label brake connections

**Step 5: Control Power (24V DC)**

- [ ] Install 24V DC power supply (10A minimum)
- [ ] Connect to transformer secondary via step-down transformer
- [ ] Route 24V wiring in separate conduit
- [ ] Connect to each drive control power input
- [ ] Use 18 AWG minimum for 24V wiring
- [ ] Install fuses or circuit breakers for 24V circuits
- [ ] Label all 24V connections

**Step 6: Grounding and Shielding**

- [ ] Connect drive chassis to cabinet ground bus
- [ ] Use star grounding topology (single point ground)
- [ ] Connect cable shields at drive end only (avoid ground loops)
- [ ] Verify ground continuity (<0.1Ω)
- [ ] Ensure all metal parts bonded to ground
- [ ] Install ferrite cores on motor cables if EMI issues

**Step 7: Drive Configuration (Initial)**

- [ ] Connect laptop to drive via USB or Ethernet
- [ ] Install drive configuration software
- [ ] Load motor parameters:
  - Motor type (from nameplate)
  - Rated voltage (480V)
  - Rated current (from nameplate)
  - Rated speed (from nameplate)
  - Encoder type and resolution
- [ ] Configure drive operating mode (CSP - Cyclic Synchronous Position)
- [ ] Set current limits (110% of rated current)
- [ ] Set velocity limits (per axis specifications)
- [ ] Configure brake control
- [ ] Save configuration to drive

**Step 8: Pre-Power Checks**

- [ ] Visual inspection of all connections
- [ ] Verify all terminals tight (torque check)
- [ ] Verify no exposed conductors
- [ ] Measure insulation resistance (>1MΩ)
- [ ] Verify grounding (< 5Ω to earth)
- [ ] Check for proper wire routing (no pinch points)
- [ ] Verify all labels in place
- [ ] Document all connections

#### 5.2.4 Safety System Wiring

**Safety System Architecture:**

The safety system must be **independent of the main control system** per ISO 13849-1 Category 3 requirements.

**Safety Components:**
- Emergency stop buttons (2 minimum)
- Safety relay (Pilz PNOZ Multi or equivalent)
- Door interlocks (2 minimum)
- Light curtain (optional but recommended)
- Safe Torque Off (STO) inputs on all drives

**Safety Circuit Wiring:**

**Step 1: Emergency Stop Buttons**

- [ ] Install E-Stop button #1 (main panel)
  - Type: 40mm mushroom head, red, twist-to-release
  - Contacts: 2 NC (normally closed) for redundancy
  - Mounting: Accessible location, not obstructed
- [ ] Install E-Stop button #2 (pendant or secondary location)
  - Same specifications as button #1
- [ ] Wire E-Stop buttons in series:
  ```
  24V+ ─┬─[E-Stop 1 NC]─┬─[E-Stop 2 NC]─┬─ To Safety Relay
        └─[E-Stop 1 NC]─┴─[E-Stop 2 NC]─┘  (Redundant path)
  ```
- [ ] Use 18 AWG, shielded cable
- [ ] Route in separate conduit from power cables
- [ ] Test button operation (mechanical test, no power)

**Step 2: Safety Relay Installation**

- [ ] Mount safety relay (Pilz PNOZ Multi or equivalent)
- [ ] Connect E-Stop inputs (dual channel)
- [ ] Connect door interlock inputs (if applicable)
- [ ] Connect light curtain inputs (if applicable)
- [ ] Connect safety outputs to drive STO inputs
- [ ] Configure safety relay per manufacturer instructions
- [ ] Set response time <50ms
- [ ] Program safety logic:
  - Any E-Stop → All drives STO active
  - Door open → All drives STO active
  - Light curtain break → All drives STO active

**Step 3: Safe Torque Off (STO) Wiring**

For each drive:
- [ ] Identify STO input terminals (typically STO1, STO2)
- [ ] Connect STO1 to safety relay output channel 1
- [ ] Connect STO2 to safety relay output channel 2 (redundant)
- [ ] Use 18 AWG, shielded cable
- [ ] Verify STO inputs are 24V DC
- [ ] Test STO function (see Section 7.2)

**Step 4: Safety Circuit Testing**

- [ ] Apply 24V control power
- [ ] Verify safety relay powers up
- [ ] Test E-Stop button #1:
  - Press button
  - Verify safety relay de-energizes
  - Verify all STO outputs de-energize
  - Release button
  - Verify system resets (may require reset button)
- [ ] Test E-Stop button #2 (same procedure)
- [ ] Test door interlocks (if applicable)
- [ ] Measure response time (<50ms required)
- [ ] Document all test results

**Safety Circuit Verification Checklist:**

- [ ] All E-Stop buttons tested and functional
- [ ] Safety relay configured correctly
- [ ] STO inputs wired to all drives
- [ ] Redundant safety paths verified
- [ ] Response time <50ms confirmed
- [ ] Safety circuit independent of main control
- [ ] All safety devices labeled
- [ ] Safety circuit diagram updated
- [ ] Compliance with ISO 13849-1 Category 3 verified

### 5.3 EtherCAT Network Installation

#### 5.3.1 Network Topology

**EtherCAT Network Configuration:**
```
Jetson Orin Nano Super (EtherCAT Master)
     |
     +-- EtherCAT Network (daisy chain)
         |
         +-- Drive 1 (Axis 1) - Address 1001
         |
         +-- Drive 2 (Axis 2) - Address 1002
         |
         +-- Drive 3 (Axis 3) - Address 1003
         |
         +-- Drive 4 (Axis 4) - Address 1004
         |
         +-- Drive 5 (Axis 5) - Address 1005
         |
         +-- Drive 6 (Turning Bed) - Address 1006
         |
         +-- I/O Module (Digital/Analog) - Address 2001
         |
         +-- Spindle Controller (VFD)
```

**Network Specifications:**
- **Protocol:** EtherCAT (IEC 61158)
- **Cycle Time:** 1ms (1kHz)
- **Cable:** CAT5e or CAT6, shielded
- **Connector:** RJ45
- **Maximum Segment Length:** 100m
- **Total Network Length:** <400m

#### 5.3.2 Cable Installation

**Step 1: Cable Selection**
- [ ] Use industrial-grade EtherCAT cable
- [ ] Shielded CAT5e or CAT6
- [ ] UV-resistant jacket (if exposed)
- [ ] Flexible for moving applications
- [ ] Pre-made cables with RJ45 connectors (preferred)

**Step 2: Cable Routing**
- [ ] Route cables in cable tray or conduit
- [ ] Separate from power cables (minimum 300mm)
- [ ] Avoid sharp bends (minimum bend radius 4× cable diameter)
- [ ] Secure cables every 300mm with cable ties
- [ ] Leave service loops at each device (300mm)
- [ ] Protect cables from mechanical damage

**Step 3: Cable Connection**

For each device in daisy chain:
- [ ] Connect "IN" port to previous device (or master)
- [ ] Connect "OUT" port to next device
- [ ] Ensure RJ45 connectors fully seated (click)
- [ ] Verify link LEDs illuminate (green)
- [ ] Label each cable at both ends
- [ ] Document cable routing in diagram

**Step 4: Shield Grounding**
- [ ] Ground cable shields at master end only
- [ ] Use cable glands with shield connection
- [ ] Avoid ground loops (do not ground at both ends)
- [ ] Verify shield continuity

**Step 5: Cable Testing**
- [ ] Use network cable tester
- [ ] Verify all 8 conductors continuous
- [ ] Check for shorts between conductors
- [ ] Verify shield continuity
- [ ] Measure cable length (should be <100m per segment)
- [ ] Document test results

#### 5.3.3 Network Configuration

**Step 1: Master Configuration (Jetson)**

- [ ] Install EtherCAT master software (IgH EtherCAT Master or SOEM)
- [ ] Configure network interface:
  - Interface: eth0 (or appropriate)
  - Cycle time: 1ms (1kHz)
  - Distributed clocks: Enabled
- [ ] Scan network for devices
- [ ] Verify all devices detected

**Step 2: Device Addressing**

For each device:
- [ ] Assign EtherCAT address:
  - Drive 1: 1001
  - Drive 2: 1002
  - Drive 3: 1003
  - Drive 4: 1004
  - Drive 5: 1005
  - Drive 6: 1006
  - I/O Module: 2001
- [ ] Configure device parameters
- [ ] Set watchdog timeout (100ms for drives, 200ms for I/O)
- [ ] Save configuration to device

**Step 3: PDO Mapping**

For each servo drive, configure Process Data Objects (PDO):

**Output PDO (Master → Drive):**
- Bytes 0-1: Control Word (0x6040)
- Bytes 2-5: Target Position (0x607A)
- Bytes 6-9: Target Velocity (0x60FF)
- Bytes 10-11: Target Torque (0x6071)

**Input PDO (Drive → Master):**
- Bytes 0-1: Status Word (0x6041)
- Bytes 2-5: Actual Position (0x6064)
- Bytes 6-9: Actual Velocity (0x606C)
- Bytes 10-11: Actual Torque (0x6077)
- Bytes 12-15: Following Error (0x60F4)

**Step 4: Distributed Clocks**

- [ ] Enable distributed clocks on all devices
- [ ] Set reference clock (typically first drive)
- [ ] Configure synchronization mode (DC-Sync0)
- [ ] Verify clock synchronization (<1μs jitter)

**Step 5: Network Testing**

- [ ] Start EtherCAT master
- [ ] Verify all devices in OP (Operational) state
- [ ] Monitor network statistics:
  - Lost frames: 0
  - Delayed frames: 0
  - Cycle time jitter: <10μs
- [ ] Test communication with each device
- [ ] Verify PDO data exchange
- [ ] Document network configuration

**EtherCAT Network Verification Checklist:**

- [ ] All devices detected and addressed
- [ ] All devices in OP state
- [ ] PDO mapping configured correctly
- [ ] Distributed clocks synchronized
- [ ] Network cycle time stable (1ms)
- [ ] No communication errors
- [ ] Watchdog timeouts configured
- [ ] Network diagram updated
- [ ] Configuration backed up

### 5.4 Encoder and Feedback System Wiring

#### 5.4.1 Encoder Specifications

**Encoder Type:** Absolute encoders (existing on robot)
- **Resolution:** 23-bit (8,388,608 counts/revolution)
- **Interface:** Differential RS-422
- **Signals:** A, A', B, B', Z, Z' (incremental) + absolute data
- **Voltage:** 5V DC
- **Cable:** Shielded, twisted pair

#### 5.4.2 Encoder Wiring Procedure

For each axis encoder:

**Step 1: Cable Preparation**
- [ ] Use shielded encoder cable (manufacturer-supplied preferred)
- [ ] Verify cable length adequate (add service loop)
- [ ] Strip cable jacket carefully (do not damage shield)
- [ ] Separate signal pairs (A/A', B/B', Z/Z')
- [ ] Prepare shield for termination

**Step 2: Motor-Side Connection**
- [ ] Identify encoder connector on motor
- [ ] Verify pin assignments (check motor documentation)
- [ ] Connect encoder cable to motor connector
- [ ] Typical pinout:
  - Pin 1: +5V
  - Pin 2: GND
  - Pin 3: A
  - Pin 4: A'
  - Pin 5: B
  - Pin 6: B'
  - Pin 7: Z
  - Pin 8: Z'
  - Shield: Connector shell
- [ ] Secure connector (locking mechanism)
- [ ] Protect connector from contamination

**Step 3: Drive-Side Connection**
- [ ] Identify encoder input on drive
- [ ] Connect encoder signals:
  - A, A' → Encoder A input (differential)
  - B, B' → Encoder B input (differential)
  - Z, Z' → Encoder Z input (differential)
  - +5V → Encoder power output
  - GND → Encoder ground
- [ ] Connect shield to drive chassis (one end only)
- [ ] Torque terminals per specification
- [ ] Verify polarity (especially power)

**Step 4: Cable Routing**
- [ ] Route encoder cables separately from power cables
- [ ] Use cable tray or conduit
- [ ] Avoid parallel runs with power cables
- [ ] Secure cables every 300mm
- [ ] Protect from mechanical damage
- [ ] Label cables at both ends

**Step 5: Encoder Testing**

- [ ] Apply encoder power (5V DC)
- [ ] Measure encoder power at motor (should be 5V ±0.25V)
- [ ] Use oscilloscope to verify encoder signals:
  - A, A' should be differential (180° out of phase)
  - B, B' should be differential
  - A and B should be 90° out of phase (quadrature)
  - Z, Z' should pulse once per revolution
- [ ] Manually rotate motor shaft
- [ ] Verify encoder counts increment/decrement
- [ ] Verify direction (clockwise should increment)
- [ ] Check for noise or signal integrity issues
- [ ] Document encoder configuration

**Encoder Verification Checklist:**

- [ ] All encoder cables connected
- [ ] Encoder power verified (5V)
- [ ] Differential signals verified
- [ ] Quadrature relationship verified (A/B 90° phase)
- [ ] Index pulse (Z) verified
- [ ] Direction verified (CW = increment)
- [ ] No signal noise or errors
- [ ] Encoder resolution configured in drive
- [ ] All encoders tested and functional

### 5.5 Wiring Documentation

#### 5.5.1 Wiring Diagram Requirements

**Create comprehensive wiring diagrams including:**

- [ ] Power distribution (480V 3-phase)
- [ ] Motor drive connections (power and control)
- [ ] Motor connections (U, V, W, PE, brake)
- [ ] Encoder connections (all signals)
- [ ] EtherCAT network topology
- [ ] Safety circuit (E-Stop, STO, interlocks)
- [ ] Control power (24V DC distribution)
- [ ] I/O connections (digital and analog)
- [ ] Grounding scheme (star topology)

**Diagram Standards:**
- Use standard electrical symbols (IEC or ANSI)
- Include wire colors and gauges
- Show terminal numbers
- Include cable labels
- Show connector pinouts
- Include notes and warnings

#### 5.5.2 Labeling Requirements

**All labels must be:**
- Permanent (thermal transfer or engraved)
- Legible (minimum 3mm text height)
- Consistent (use standard naming convention)
- Weatherproof (if exposed to environment)

**Label all:**
- [ ] Wires (both ends)
- [ ] Cables (both ends)
- [ ] Terminal blocks
- [ ] Circuit breakers
- [ ] Devices (drives, relays, etc.)
- [ ] Connectors
- [ ] Conduits
- [ ] Panels and enclosures

**Labeling Convention:**
```
Format: [System]-[Subsystem]-[Component]-[Number]

Examples:
PWR-MAIN-L1    (Power, Main, Phase L1)
MTR-AX1-U      (Motor, Axis 1, Phase U)
ENC-AX1-A      (Encoder, Axis 1, Signal A)
ECAT-DR1-IN    (EtherCAT, Drive 1, Input)
SAFE-ESTOP1    (Safety, Emergency Stop 1)
```

#### 5.5.3 As-Built Documentation

**After installation complete:**

- [ ] Update all wiring diagrams to reflect as-built conditions
- [ ] Photograph all connections
- [ ] Create cable schedule (list of all cables with routing)
- [ ] Document any deviations from original design
- [ ] Create troubleshooting guide
- [ ] Compile all documentation into binder
- [ ] Create digital backup of all documentation
- [ ] Provide copies to maintenance personnel

---

## 6. Sensor Installation and Calibration

### 6.1 Vision System Installation

#### 6.1.1 Camera Specifications

**RGB Cameras:**
- **Quantity:** 3-5 units
- **Resolution:** 1920×1080 (Full HD)
- **Frame Rate:** 60 fps
- **Interface:** USB 3.0 or GigE
- **Lens:** Adjustable focus, appropriate field of view
- **Mounting:** Rigid, vibration-isolated

**Depth Camera:**
- **Model:** Intel RealSense D435 or equivalent
- **Resolution:** 1280×720 depth + 1920×1080 RGB
- **Frame Rate:** 30 fps (depth), 60 fps (RGB)
- **Range:** 0.3m to 3m
- **Interface:** USB 3.0

#### 6.1.2 Camera Mounting Procedure

**Step 1: Mounting Location Selection**

For each camera:
- [ ] Determine optimal viewing angle
- [ ] Ensure clear view of workspace
- [ ] Avoid backlighting (windows, bright lights)
- [ ] Minimize occlusions
- [ ] Consider cable routing
- [ ] Verify mounting surface rigidity

**Recommended Camera Positions:**
- Camera 1: Front view (eye-level with workspace)
- Camera 2: Side view (45° angle)
- Camera 3: Top view (overhead)
- Camera 4: Wrist-mounted (end-effector view)
- Camera 5: Depth camera (front, centered)

**Step 2: Mounting Hardware Installation**

- [ ] Select appropriate mounting bracket
- [ ] Ensure bracket is rigid (no flex)
- [ ] Install vibration isolation if needed
- [ ] Mount bracket to structure:
  - Use appropriate fasteners (M6 or M8 bolts)
  - Torque to specification
  - Verify secure mounting
- [ ] Adjust bracket to desired angle
- [ ] Lock adjustment mechanism

**Step 3: Camera Installation**

- [ ] Attach camera to mounting bracket
- [ ] Secure with appropriate fasteners
- [ ] Adjust camera angle
- [ ] Verify field of view covers workspace
- [ ] Tighten all adjustments
- [ ] Verify camera is level (if required)

**Step 4: Cable Routing**

- [ ] Route USB 3.0 cable to Jetson
- [ ] Use cable management (cable tray or conduit)
- [ ] Avoid sharp bends (minimum bend radius per cable spec)
- [ ] Secure cable every 300mm
- [ ] Leave service loop at camera (300mm)
- [ ] Protect cable from mechanical damage
- [ ] Label cable at both ends

**Step 5: Camera Connection**

- [ ] Connect USB cable to camera
- [ ] Connect USB cable to Jetson USB 3.0 port
- [ ] Verify connection (LED indicator on camera)
- [ ] Power on Jetson
- [ ] Verify camera detected by system:
  ```bash
  lsusb  # Should show camera device
  v4l2-ctl --list-devices  # Should list camera
  ```
- [ ] Test camera capture:
  ```bash
  ffplay /dev/video0  # Or appropriate device
  ```

**Step 6: Initial Camera Configuration**

- [ ] Set resolution (1920×1080)
- [ ] Set frame rate (60 fps)
- [ ] Adjust focus (manual or auto)
- [ ] Adjust exposure (avoid over/under exposure)
- [ ] Adjust white balance
- [ ] Disable auto-adjust features (for consistency)
- [ ] Save camera settings

#### 6.1.3 Camera Calibration

**Purpose:** Determine intrinsic and extrinsic camera parameters for accurate 3D reconstruction

**Required Equipment:**
- Calibration checkerboard (e.g., 9×6 squares, 25mm square size)
- Good lighting
- Calibration software (OpenCV, ROS camera_calibration, etc.)

**Step 1: Intrinsic Calibration (Per Camera)**

- [ ] Print calibration checkerboard on rigid surface
- [ ] Verify checkerboard is flat (no warping)
- [ ] Launch calibration software
- [ ] Capture 20-30 images of checkerboard:
  - Various positions in field of view
  - Various orientations (tilted, rotated)
  - Various distances
  - Cover entire field of view
- [ ] Run calibration algorithm
- [ ] Verify reprojection error (<0.5 pixels)
- [ ] Save calibration parameters:
  - Camera matrix (focal length, principal point)
  - Distortion coefficients (k1, k2, p1, p2, k3)
- [ ] Test calibration (undistort test image)

**Step 2: Extrinsic Calibration (Camera-to-Robot)**

**Purpose:** Determine transformation from camera frame to robot base frame

**Method 1: Hand-Eye Calibration (Wrist-Mounted Camera)**
- [ ] Attach calibration target to fixed location
- [ ] Move robot to multiple poses (10-20 poses)
- [ ] At each pose:
  - Record robot pose (from forward kinematics)
  - Capture image of calibration target
  - Detect target in image
- [ ] Run hand-eye calibration algorithm (OpenCV or ROS)
- [ ] Verify calibration accuracy (<5mm error)
- [ ] Save transformation matrix (camera to end-effector)

**Method 2: Fixed Camera Calibration**
- [ ] Attach calibration target to robot end-effector
- [ ] Move robot to multiple poses (10-20 poses)
- [ ] At each pose:
  - Record robot pose
  - Capture image of calibration target
  - Detect target in image
- [ ] Run calibration algorithm
- [ ] Verify calibration accuracy (<5mm error)
- [ ] Save transformation matrix (camera to robot base)

**Step 3: Multi-Camera Calibration**

If using multiple cameras:
- [ ] Calibrate each camera individually (intrinsic)
- [ ] Calibrate each camera to robot (extrinsic)
- [ ] Optionally: Calibrate cameras relative to each other (stereo calibration)
- [ ] Verify consistency between cameras
- [ ] Save all calibration parameters

**Step 4: Depth Camera Calibration**

For Intel RealSense D435:
- [ ] Use RealSense SDK calibration tools
- [ ] Calibrate RGB camera (intrinsic)
- [ ] Calibrate depth camera (intrinsic)
- [ ] Calibrate RGB-to-depth alignment
- [ ] Verify depth accuracy (compare to known distances)
- [ ] Save calibration parameters

**Camera Calibration Verification Checklist:**

- [ ] All cameras calibrated (intrinsic)
- [ ] Reprojection error <0.5 pixels
- [ ] Camera-to-robot calibration complete (extrinsic)
- [ ] Calibration accuracy verified (<5mm)
- [ ] Depth camera calibrated and aligned
- [ ] Calibration parameters saved
- [ ] Calibration date documented
- [ ] Recalibration schedule established (quarterly)

### 6.2 Force/Torque Sensor Installation

#### 6.2.1 Force/Torque Sensor Specifications

**Recommended Sensor:**
- **Model:** ATI Mini40 or equivalent
- **Force Range:** ±40N (X, Y, Z axes)
- **Torque Range:** ±2Nm (X, Y, Z axes)
- **Resolution:** 0.02N force, 0.001Nm torque
- **Output:** ±10V analog or digital (RS-485, EtherCAT)
- **Update Rate:** 1kHz
- **Cost:** ~$2,000

#### 6.2.2 Mounting Procedure

**Step 1: Mounting Location**

- [ ] Typical location: Between robot flange and end-effector
- [ ] Verify sensor load capacity adequate for end-effector + payload
- [ ] Ensure sensor orientation matches coordinate system

**Step 2: Mechanical Installation**

- [ ] Clean mounting surfaces (robot flange and end-effector)
- [ ] Apply thread-locking compound to fasteners
- [ ] Attach sensor to robot flange:
  - Use appropriate fasteners (typically M6 or M8)
  - Torque to specification (check sensor manual)
  - Use torque wrench
  - Verify even tightening (star pattern)
- [ ] Attach end-effector to sensor:
  - Same procedure as above
  - Verify alignment
- [ ] Verify sensor is secure (no movement)

**Step 3: Cable Routing**

- [ ] Route sensor cable along robot arm
- [ ] Use cable carrier or cable management system
- [ ] Avoid sharp bends
- [ ] Secure cable to prevent snagging
- [ ] Leave adequate slack for full range of motion
- [ ] Protect cable from pinch points

**Step 4: Electrical Connection**

**For Analog Output (±10V):**
- [ ] Connect to analog input module (EtherCAT I/O)
- [ ] Connect 6 channels (Fx, Fy, Fz, Tx, Ty, Tz)
- [ ] Use shielded cable
- [ ] Connect shield to ground at one end only
- [ ] Verify input range matches sensor output (±10V)
- [ ] Connect sensor power (typically 24V DC)

**For Digital Output (EtherCAT):**
- [ ] Connect to EtherCAT network
- [ ] Configure sensor address
- [ ] Configure PDO mapping
- [ ] Verify communication

**Step 5: Sensor Configuration**

- [ ] Apply sensor power
- [ ] Connect to sensor configuration software
- [ ] Set sensor parameters:
  - Calibration matrix (from factory calibration)
  - Coordinate system orientation
  - Filter settings (low-pass filter, cutoff frequency)
  - Bias removal (zero sensor with no load)
- [ ] Save configuration

#### 6.2.3 Force/Torque Sensor Calibration

**Step 1: Zero Calibration (Bias Removal)**

- [ ] Remove all loads from sensor
- [ ] Ensure robot is in stable position
- [ ] Allow sensor to warm up (5 minutes)
- [ ] Record sensor readings (should be near zero)
- [ ] Apply bias removal (zero offset)
- [ ] Verify readings are now zero (±0.1N, ±0.01Nm)

**Step 2: Gravity Compensation**

- [ ] Measure end-effector mass and center of gravity
- [ ] Calculate gravity force in sensor frame
- [ ] Implement gravity compensation in software:
  ```
  F_compensated = F_measured - F_gravity(robot_pose)
  ```
- [ ] Verify compensation (move robot, sensor should read ~zero)

**Step 3: Calibration Verification**

- [ ] Apply known force (e.g., hang known mass)
- [ ] Verify sensor reading matches expected force
- [ ] Repeat for multiple orientations
- [ ] Verify accuracy (±2% of full scale)
- [ ] Document calibration results

**Step 4: Dynamic Testing**

- [ ] Move robot through typical motions
- [ ] Monitor sensor readings
- [ ] Verify no excessive noise or drift
- [ ] Check for cable interference (readings should not change with cable position)
- [ ] Verify update rate (1kHz)

**Force/Torque Sensor Verification Checklist:**

- [ ] Sensor mechanically secure
- [ ] Electrical connections verified
- [ ] Sensor communication functional
- [ ] Zero calibration complete
- [ ] Gravity compensation implemented
- [ ] Calibration accuracy verified (±2%)
- [ ] Dynamic testing complete
- [ ] No noise or drift issues
- [ ] Update rate verified (1kHz)

### 6.3 Additional Sensors

#### 6.3.1 Limit Switches

**Purpose:** Hardware limits to prevent over-travel

**Installation (Per Axis):**

- [ ] Identify positive and negative travel limits
- [ ] Mount limit switches at limit positions
- [ ] Adjust switch position (trigger just before hard stop)
- [ ] Wire switches to I/O module:
  - Use NC (normally closed) contacts
  - Wire in series with drive enable
  - Connect to safety circuit if critical
- [ ] Test switch operation:
  - Manually trigger switch
  - Verify drive disables
  - Verify software detects limit
- [ ] Label switches clearly
- [ ] Document switch positions

#### 6.3.2 Home Switches

**Purpose:** Establish reference position for absolute positioning

**Installation (Per Axis):**

- [ ] Identify home position (typically mid-travel or zero position)
- [ ] Mount home switch at home position
- [ ] Adjust switch position for repeatability
- [ ] Wire switch to I/O module
- [ ] Test switch operation:
  - Move axis to home position
  - Verify switch triggers
  - Verify repeatability (±0.01mm)
- [ ] Implement homing procedure in software
- [ ] Test homing sequence
- [ ] Document home position

#### 6.3.3 Temperature Sensors

**Purpose:** Monitor motor and drive temperatures

**Installation:**

- [ ] Install thermistor or thermocouple on each motor
- [ ] Typical location: Motor housing near windings
- [ ] Use thermal paste for good contact
- [ ] Secure sensor with adhesive or clamp
- [ ] Route cable to analog input module
- [ ] Connect to analog input (0-10V or 4-20mA)
- [ ] Configure input scaling (temperature per volt)
- [ ] Set temperature alarm thresholds:
  - Warning: 70°C
  - Shutdown: 80°C
- [ ] Test temperature reading
- [ ] Document sensor locations

#### 6.3.4 Current Monitoring

**Purpose:** Monitor motor currents for fault detection

**Installation:**

- [ ] Install current sensors on motor power lines
- [ ] Use hall-effect current sensors (non-invasive)
- [ ] Typical location: Between drive and motor
- [ ] Mount sensor on power cable
- [ ] Connect sensor output to analog input
- [ ] Configure input scaling (amps per volt)
- [ ] Set current alarm thresholds:
  - Warning: 110% of rated current
  - Shutdown: 150% of rated current
- [ ] Test current reading (compare to drive current reading)
- [ ] Document sensor locations

### 6.4 Sensor System Verification

**Complete Sensor System Checklist:**

- [ ] All cameras installed and calibrated
- [ ] Camera frame rates verified (60 fps)
- [ ] Camera calibration accuracy verified (<5mm)
- [ ] Force/torque sensor installed and calibrated
- [ ] F/T sensor accuracy verified (±2%)
- [ ] All encoders connected and tested
- [ ] Encoder resolution verified (23-bit)
- [ ] Limit switches installed and tested
- [ ] Home switches installed and tested
- [ ] Temperature sensors installed and configured
- [ ] Current sensors installed and configured
- [ ] All sensor cables labeled
- [ ] All sensor data logging to system
- [ ] Sensor system documentation complete

---

## 7. Safety System Verification and Compliance

### 7.1 Safety System Overview

**Safety Requirements:**
- **Standard:** ISO 13849-1, Category 3, Performance Level d (PLd)
- **Response Time:** <50ms total (detection to safe state)
- **Architecture:** Redundant safety circuits, independent of main control
- **Compliance:** IEC 61800-5-2 (drive safety functions)

**Safety System Components:**
- Emergency stop buttons (2 minimum)
- Safety relay (Category 3, dual-channel)
- Safe Torque Off (STO) in all drives
- Door interlocks (if applicable)
- Light curtain (optional)
- Hardware watchdog

### 7.2 Emergency Stop System Testing

#### 7.2.1 E-Stop Button Testing

**Test Procedure:**

**Test 1: E-Stop Button #1 (Main Panel)**

- [ ] **Pre-Test:**
  - Verify system powered and operational
  - Verify all drives enabled
  - Position robot in safe location (mid-workspace)
  - Clear all personnel from robot workspace
  - Wear appropriate PPE

- [ ] **Test Execution:**
  - Press E-Stop button #1
  - Observe system response

- [ ] **Expected Results:**
  - Safety relay de-energizes immediately
  - All drive STO inputs de-energize
  - All motor power removed (Safe Torque Off)
  - Robot motion stops immediately
  - Brakes engage (if equipped)
  - Status indicators show E-Stop active
  - Software detects E-Stop state

- [ ] **Measurements:**
  - Response time (trigger to motion stop): _______ ms (must be <50ms)
  - Stopping distance: _______ mm
  - Deceleration rate: _______ m/s²

- [ ] **Reset Test:**
  - Twist E-Stop button to release
  - Verify system does NOT automatically restart
  - Press reset button (if required)
  - Verify system ready to restart
  - Manually enable drives
  - Verify normal operation resumes

**Test 2: E-Stop Button #2 (Secondary Location)**

- [ ] Repeat all steps above for E-Stop button #2
- [ ] Verify identical behavior

**Test 3: Simultaneous E-Stop**

- [ ] Press both E-Stop buttons simultaneously
- [ ] Verify system responds correctly
- [ ] Release one button
- [ ] Verify system remains in E-Stop state
- [ ] Release second button
- [ ] Verify system can be reset

**Test 4: E-Stop During Motion**

- [ ] Start robot motion (slow speed, 10% maximum)
- [ ] Press E-Stop during motion
- [ ] Verify immediate stop
- [ ] Measure stopping distance
- [ ] Verify no overshoot or oscillation
- [ ] Repeat for different speeds (25%, 50%, 75%, 100%)

**Test 5: E-Stop Redundancy**

- [ ] Disconnect one E-Stop channel (simulate failure)
- [ ] Verify system enters safe state (fail-safe)
- [ ] Reconnect channel
- [ ] Repeat for other channel
- [ ] Verify redundancy functional

#### 7.2.2 Safe Torque Off (STO) Testing

**Purpose:** Verify STO function removes power to motors independent of control system

**Test Procedure (Per Drive):**

**Test 1: STO Activation**

- [ ] Enable drive
- [ ] Command small motion (10% speed)
- [ ] Manually trigger STO input (disconnect or short to ground)
- [ ] Observe drive response

**Expected Results:**
- [ ] Drive immediately removes motor power
- [ ] Motor coasts to stop (no active braking)
- [ ] Drive status indicates STO active
- [ ] Drive cannot be enabled while STO active
- [ ] No error or fault condition (STO is normal function)

**Test 2: STO Response Time**

- [ ] Use oscilloscope to measure STO response time
- [ ] Trigger STO input
- [ ] Measure time from trigger to motor power removal
- [ ] Response time: _______ ms (must be <10ms per IEC 61800-5-2)

**Test 3: STO Redundancy**

- [ ] Verify drive has dual-channel STO (STO1 and STO2)
- [ ] Trigger STO1 only
- [ ] Verify motor power removed
- [ ] Reset STO1, trigger STO2 only
- [ ] Verify motor power removed
- [ ] Verify both channels required for operation (AND logic)

**Test 4: STO Independence**

- [ ] Disconnect communication to drive (EtherCAT)
- [ ] Verify STO still functional
- [ ] Trigger STO
- [ ] Verify motor power removed
- [ ] This confirms STO is independent of communication

**Repeat for all 6 drives**

#### 7.2.3 Safety Relay Testing

**Test Procedure:**

**Test 1: Safety Relay Configuration**

- [ ] Verify safety relay model and specifications
- [ ] Verify Category 3 architecture (dual-channel)
- [ ] Verify all safety inputs connected:
  - E-Stop button #1 (dual-channel)
  - E-Stop button #2 (dual-channel)
  - Door interlocks (if applicable)
  - Light curtain (if applicable)
- [ ] Verify all safety outputs connected:
  - Drive 1 STO (dual-channel)
  - Drive 2 STO (dual-channel)
  - Drive 3 STO (dual-channel)
  - Drive 4 STO (dual-channel)
  - Drive 5 STO (dual-channel)
  - Drive 6 STO (dual-channel)

**Test 2: Safety Logic**

- [ ] Verify safety relay logic configuration:
  - All E-Stops in series (any E-Stop → all drives STO)
  - All interlocks in series
  - Outputs energized only when all inputs safe
- [ ] Test logic with each input
- [ ] Verify correct behavior

**Test 3: Response Time**

- [ ] Measure total response time (E-Stop press to STO activation)
- [ ] Use oscilloscope or high-speed data logging
- [ ] Trigger E-Stop
- [ ] Measure time to STO activation
- [ ] Total response time: _______ ms (must be <50ms)

**Test 4: Fault Detection**

- [ ] Simulate input fault (short circuit, open circuit)
- [ ] Verify safety relay detects fault
- [ ] Verify system enters safe state
- [ ] Verify fault indication (LED, status output)
- [ ] Clear fault
- [ ] Verify system can be reset

**Test 5: Power Interruption**

- [ ] Remove power from safety relay
- [ ] Verify all outputs de-energize (fail-safe)
- [ ] Verify all drives enter STO state
- [ ] Restore power
- [ ] Verify safety relay restarts correctly
- [ ] Verify system requires manual reset

### 7.3 Safety System Documentation

#### 7.3.1 Risk Assessment

**Required per ISO 12100:**

- [ ] Identify all hazards:
  - Crushing hazards (robot motion)
  - Electrical hazards (480V)
  - Thermal hazards (hot motors)
  - Noise hazards (operation)
  - Ergonomic hazards (repetitive tasks)

- [ ] Assess risk for each hazard:
  - Severity (S): 1-4 (1=minor, 4=fatal)
  - Frequency (F): 1-5 (1=rare, 5=continuous)
  - Probability (P): 1-5 (1=unlikely, 5=certain)
  - Risk = S × F × P

- [ ] Implement risk reduction measures:
  - Eliminate hazard (design)
  - Guard hazard (physical barriers)
  - Warn of hazard (signs, training)
  - Provide PPE

- [ ] Document residual risk

- [ ] Create risk assessment report

#### 7.3.2 Safety Validation Report

**Document must include:**

- [ ] Safety system architecture diagram
- [ ] Safety component specifications
- [ ] Safety circuit schematics
- [ ] Test procedures and results
- [ ] Response time measurements
- [ ] Failure mode analysis
- [ ] Compliance statement (ISO 13849-1 Category 3, PLd)
- [ ] Validation date and personnel
- [ ] Approval signatures

#### 7.3.3 Safety Compliance Checklist

**ISO 13849-1 Category 3 Requirements:**

- [ ] Redundant safety circuits (dual-channel)
- [ ] Fault detection capability
- [ ] Single fault does not lead to loss of safety function
- [ ] Single fault detected at or before next demand
- [ ] Common cause failures prevented (separation, diversity)
- [ ] Well-tried components used
- [ ] Performance Level d (PLd) achieved
- [ ] Mean Time to Dangerous Failure (MTTFd) calculated
- [ ] Diagnostic Coverage (DC) adequate
- [ ] Common Cause Failure (CCF) measures implemented

**IEC 61800-5-2 Requirements (Drive Safety):**

- [ ] Safe Torque Off (STO) implemented in all drives
- [ ] STO response time <10ms
- [ ] STO independent of communication
- [ ] STO dual-channel (redundant)
- [ ] STO fault detection
- [ ] Drive safety manual reviewed
- [ ] Drive safety parameters configured

**NFPA 70E Requirements (Electrical Safety):**

- [ ] Arc flash hazard analysis completed
- [ ] Arc flash labels installed
- [ ] Appropriate PPE specified
- [ ] Electrical safety training completed
- [ ] LOTO procedures documented
- [ ] Electrical drawings up to date
- [ ] Grounding verified

**Compliance Verification:**

- [ ] All requirements met
- [ ] All tests passed
- [ ] All documentation complete
- [ ] Independent review completed (if required)
- [ ] Certification obtained (if required)
- [ ] Compliance certificate issued

### 7.4 Periodic Safety Verification

**Safety systems must be tested regularly:**

**Daily (Before Operation):**
- [ ] Test emergency stop buttons
- [ ] Visual inspection of safety devices
- [ ] Verify safety indicators functional

**Weekly:**
- [ ] Test all safety interlocks
- [ ] Inspect safety barriers/fencing
- [ ] Check safety labels and signs

**Monthly:**
- [ ] Full safety system functional test
- [ ] Measure response times
- [ ] Inspect safety relay
- [ ] Test STO on all drives
- [ ] Review safety incidents (if any)

**Quarterly:**
- [ ] Comprehensive safety audit
- [ ] Review and update risk assessment
- [ ] Safety training refresher
- [ ] Inspect and test all safety equipment
- [ ] Update safety documentation

**Annually:**
- [ ] Complete safety system recertification
- [ ] Third-party safety audit (recommended)
- [ ] Update safety procedures
- [ ] Renew safety certifications

---

## 8. System Integration Procedures

### 8.1 Controller Installation

#### 8.1.1 Jetson Orin Nano Super Installation

**Step 1: Mounting**

- [ ] Select mounting location in control cabinet
- [ ] Ensure adequate ventilation (top and bottom clearance)
- [ ] Avoid high-temperature areas (near drives or transformers)
- [ ] Mount on DIN rail or standoffs
- [ ] Use vibration isolation if necessary
- [ ] Secure mounting (verify no movement)

**Step 2: Power Connection**

- [ ] Verify power requirements (5V DC, 5A typical)
- [ ] Install 5V DC power supply (10A capacity recommended)
- [ ] Connect power supply to 24V DC bus via DC-DC converter
- [ ] Connect 5V power to Jetson
- [ ] Verify voltage at Jetson (5V ±0.25V)
- [ ] Connect ground

**Step 3: Network Connection**

- [ ] Connect Ethernet cable to Jetson (for EtherCAT master)
- [ ] Connect second Ethernet cable (for programming/monitoring)
- [ ] Verify network link LEDs

**Step 4: Peripheral Connections**

- [ ] Connect USB hub (for cameras)
- [ ] Connect cameras to USB 3.0 ports
- [ ] Connect keyboard/mouse (for initial setup)
- [ ] Connect monitor via HDMI (for initial setup)

**Step 5: Storage**

- [ ] Install NVMe SSD (if not pre-installed)
- [ ] Verify SSD capacity (minimum 256GB recommended)
- [ ] Format and partition SSD

**Step 6: Initial Boot**

- [ ] Apply power to Jetson
- [ ] Verify boot sequence on monitor
- [ ] Complete initial setup (Ubuntu)
- [ ] Set hostname, user account, password
- [ ] Configure network settings
- [ ] Update system packages:
  ```bash
  sudo apt update
  sudo apt upgrade
  ```

**Step 7: Software Installation**

- [ ] Install real-time kernel (PREEMPT_RT)
- [ ] Install EtherCAT master software
- [ ] Install ROS2 (if using)
- [ ] Install ML frameworks (PyTorch, TensorRT)
- [ ] Install camera drivers
- [ ] Install development tools
- [ ] Configure system for real-time operation

**Step 8: System Configuration**

- [ ] Configure CPU governor (performance mode)
- [ ] Disable power management
- [ ] Configure CPU core isolation (for real-time tasks)
- [ ] Set process priorities
- [ ] Configure memory locking
- [ ] Disable unnecessary services
- [ ] Configure automatic startup

#### 8.1.2 I/O Module Installation

**Step 1: Module Selection**

- [ ] Select EtherCAT I/O module (e.g., Beckhoff EL1xxx/EL2xxx/EL3xxx)
- [ ] Verify sufficient I/O channels:
  - Digital inputs: 16+ (limit switches, home switches, status)
  - Digital outputs: 16+ (drive enable, brake release, indicators)
  - Analog inputs: 8+ (force/torque, temperature, current)
  - Analog outputs: 2+ (spindle speed, torque limit)

**Step 2: Mounting**

- [ ] Mount I/O module on DIN rail
- [ ] Position near terminal blocks for short wiring
- [ ] Ensure adequate spacing for wiring

**Step 3: Power Connection**

- [ ] Connect 24V DC power to I/O module
- [ ] Verify voltage (24V ±10%)
- [ ] Connect ground

**Step 4: EtherCAT Connection**

- [ ] Connect I/O module to EtherCAT network
- [ ] Assign address (2001)
- [ ] Configure PDO mapping
- [ ] Verify communication

**Step 5: I/O Wiring**

**Digital Inputs:**
- [ ] Wire limit switches (NC contacts)
- [ ] Wire home switches (NO contacts)
- [ ] Wire status inputs from drives
- [ ] Wire auxiliary inputs
- [ ] Label all inputs

**Digital Outputs:**
- [ ] Wire drive enable signals
- [ ] Wire brake release outputs
- [ ] Wire indicator lights
- [ ] Wire auxiliary outputs
- [ ] Label all outputs

**Analog Inputs:**
- [ ] Wire force/torque sensor (6 channels, ±10V)
- [ ] Wire temperature sensors (0-10V)
- [ ] Wire current sensors (0-10V)
- [ ] Wire auxiliary analog inputs
- [ ] Configure input scaling
- [ ] Label all inputs

**Analog Outputs:**
- [ ] Wire spindle speed control (0-10V)
- [ ] Wire spindle torque limit (0-10V)
- [ ] Configure output scaling
- [ ] Label all outputs

**Step 6: I/O Testing**

- [ ] Test each digital input (manually trigger)
- [ ] Test each digital output (manually activate)
- [ ] Test each analog input (apply known voltage)
- [ ] Test each analog output (measure output voltage)
- [ ] Verify all I/O functional
- [ ] Document I/O configuration

### 8.2 Component Integration

#### 8.2.1 Integration Sequence

**Phase 1: Benchtop Testing**
- Test individual components on bench before installation
- Verify communication and basic functionality
- Identify and resolve issues in controlled environment

**Phase 2: Single-Axis Integration**
- Integrate one axis at a time
- Test each axis independently
- Verify safety systems for each axis
- Proceed to next axis only after successful test

**Phase 3: Multi-Axis Coordination**
- Integrate multiple axes
- Test coordinated motion
- Verify kinematics and trajectory planning
- Test safety systems with multiple axes

**Phase 4: Full System Integration**
- Integrate all components
- Test complete system functionality
- Verify all modes (G-code, ML, manual)
- Conduct endurance testing

#### 8.2.2 Single-Axis Integration Procedure

**For Each Axis (Repeat 6 times):**

**Step 1: Pre-Integration Checks**

- [ ] Verify drive installed and powered
- [ ] Verify motor connected
- [ ] Verify encoder connected
- [ ] Verify brake connected (if applicable)
- [ ] Verify EtherCAT communication
- [ ] Verify safety systems (E-Stop, STO)

**Step 2: Drive Configuration**

- [ ] Load motor parameters
- [ ] Configure encoder
- [ ] Configure brake control
- [ ] Set current limits
- [ ] Set velocity limits
- [ ] Set position limits
- [ ] Configure control mode (CSP - Cyclic Synchronous Position)
- [ ] Save configuration

**Step 3: Initial Motion Test (No Load)**

- [ ] Ensure axis is free to move (no obstructions)
- [ ] Ensure personnel clear
- [ ] Enable drive
- [ ] Command small motion (1° or 1mm)
- [ ] Observe motion:
  - Direction correct?
  - Smooth motion?
  - No unusual sounds?
  - Encoder feedback correct?
- [ ] If issues, stop and troubleshoot
- [ ] If successful, proceed

**Step 4: Homing Procedure**

- [ ] Move axis to home switch
- [ ] Verify home switch triggers
- [ ] Implement homing sequence:
  - Move toward home switch at slow speed
  - Detect home switch trigger
  - Back off home switch
  - Approach again at very slow speed
  - Set position to zero
- [ ] Verify homing repeatability (±0.01mm)
- [ ] Test homing sequence 10 times

**Step 5: Limit Testing**

- [ ] Move axis to positive limit
- [ ] Verify positive limit switch triggers
- [ ] Verify drive stops
- [ ] Verify software detects limit
- [ ] Move axis to negative limit
- [ ] Verify negative limit switch triggers
- [ ] Verify drive stops
- [ ] Verify software detects limit

**Step 6: Position Control Testing**

- [ ] Command axis to specific position
- [ ] Verify axis moves to position
- [ ] Measure position accuracy (use encoder or external measurement)
- [ ] Repeat for multiple positions across range
- [ ] Verify accuracy (±0.05mm or ±0.01° target)
- [ ] Test repeatability (10 cycles to same position)

**Step 7: Velocity Control Testing**

- [ ] Command axis to move at specific velocity
- [ ] Verify velocity (use encoder feedback)
- [ ] Test multiple velocities (10%, 25%, 50%, 75%, 100%)
- [ ] Verify smooth acceleration and deceleration
- [ ] Verify no overshoot

**Step 8: Safety Testing**

- [ ] Test E-Stop during motion
- [ ] Verify immediate stop
- [ ] Test STO during motion
- [ ] Verify immediate power removal
- [ ] Test limit switches
- [ ] Verify drive disables at limits

**Step 9: Performance Characterization**

- [ ] Measure maximum velocity
- [ ] Measure maximum acceleration
- [ ] Measure positioning accuracy
- [ ] Measure repeatability
- [ ] Measure following error
- [ ] Document performance

**Step 10: Documentation**

- [ ] Record all test results
- [ ] Document any issues and resolutions
- [ ] Update configuration files
- [ ] Mark axis as "Integrated and Tested"

**Repeat for all 6 axes before proceeding to multi-axis integration**

#### 8.2.3 Multi-Axis Integration Procedure

**Step 1: Kinematics Implementation**

- [ ] Implement forward kinematics (joint angles → end-effector pose)
- [ ] Implement inverse kinematics (end-effector pose → joint angles)
- [ ] Verify kinematics with known poses
- [ ] Test singularity handling
- [ ] Test workspace limits

**Step 2: Coordinated Motion Testing**

- [ ] Command simple coordinated motion (e.g., straight line)
- [ ] Verify all axes move smoothly
- [ ] Verify end-effector follows desired path
- [ ] Measure path accuracy
- [ ] Test circular motion
- [ ] Test complex trajectories

**Step 3: Trajectory Planning**

- [ ] Implement trajectory planner
- [ ] Test velocity profiling (trapezoidal or S-curve)
- [ ] Verify smooth acceleration/deceleration
- [ ] Test trajectory blending (continuous path)
- [ ] Verify no jerky motion

**Step 4: Collision Detection**

- [ ] Implement collision detection (self-collision and environment)
- [ ] Test collision detection with known collisions
- [ ] Verify system stops before collision
- [ ] Test false positive rate (should be low)

**Step 5: Force Control Testing (If Applicable)**

- [ ] Implement force control loop
- [ ] Test force control with known forces
- [ ] Verify force accuracy (±2% target)
- [ ] Test compliance (robot yields to external forces)

**Step 6: Multi-Axis Safety Testing**

- [ ] Test E-Stop during coordinated motion
- [ ] Verify all axes stop simultaneously
- [ ] Test STO during coordinated motion
- [ ] Verify all axes enter safe state
- [ ] Test collision detection triggers E-Stop

**Step 7: Performance Testing**

- [ ] Run standard test trajectory
- [ ] Measure cycle time
- [ ] Measure path accuracy
- [ ] Measure repeatability
- [ ] Compare to baseline (original system)

### 8.3 Network Configuration and Verification

#### 8.3.1 EtherCAT Network Verification

**Step 1: Network Scan**

- [ ] Start EtherCAT master
- [ ] Scan network for devices
- [ ] Verify all devices detected:
  - Drive 1 (Address 1001)
  - Drive 2 (Address 1002)
  - Drive 3 (Address 1003)
  - Drive 4 (Address 1004)
  - Drive 5 (Address 1005)
  - Drive 6 (Address 1006)
  - I/O Module (Address 2001)
- [ ] Verify device order matches physical topology

**Step 2: Communication Testing**

- [ ] Verify all devices in OP (Operational) state
- [ ] Monitor network statistics:
  - Lost frames: 0
  - Delayed frames: 0
  - Cycle time: 1ms ±10μs
  - Jitter: <10μs
- [ ] Test communication with each device
- [ ] Verify PDO data exchange

**Step 3: Distributed Clocks Verification**

- [ ] Verify distributed clocks enabled
- [ ] Check clock synchronization:
  - Offset: <1μs
  - Drift: <10ns/s
- [ ] Monitor clock over time (should remain stable)

**Step 4: Network Load Testing**

- [ ] Run system at full speed
- [ ] Monitor network statistics
- [ ] Verify no communication errors
- [ ] Verify cycle time remains stable
- [ ] Test for extended period (1 hour minimum)

**Step 5: Fault Injection Testing**

- [ ] Disconnect one device
- [ ] Verify master detects fault
- [ ] Verify system enters safe state
- [ ] Reconnect device
- [ ] Verify system recovers
- [ ] Repeat for each device

**Step 6: Network Documentation**

- [ ] Create network topology diagram
- [ ] Document device addresses
- [ ] Document PDO mappings
- [ ] Document network configuration
- [ ] Save configuration files

#### 8.3.2 Network Performance Optimization

**If network issues detected:**

- [ ] Check cable quality (replace if necessary)
- [ ] Verify cable routing (separate from power cables)
- [ ] Check for EMI sources (motors, drives, transformers)
- [ ] Add ferrite cores to cables
- [ ] Adjust cycle time (increase if necessary)
- [ ] Optimize PDO mappings (reduce data if possible)
- [ ] Update device firmware
- [ ] Consult device manufacturer

### 8.4 System Integration Verification Checklist

**Hardware Integration:**

- [ ] All drives installed and configured
- [ ] All motors connected and tested
- [ ] All encoders connected and tested
- [ ] All brakes connected and tested
- [ ] All sensors installed and calibrated
- [ ] All I/O wired and tested
- [ ] All safety systems installed and tested
- [ ] All network connections verified

**Software Integration:**

- [ ] Real-time control system operational
- [ ] Kinematics implemented and tested
- [ ] Trajectory planning functional
- [ ] Safety systems integrated
- [ ] Sensor data acquisition functional
- [ ] Data logging operational
- [ ] User interface functional

**Performance Verification:**

- [ ] All axes move smoothly
- [ ] Position accuracy meets requirements (±0.05mm)
- [ ] Repeatability meets requirements (±0.02mm)
- [ ] Velocity control functional
- [ ] Force control functional (if applicable)
- [ ] Coordinated motion functional
- [ ] Safety systems functional

**Documentation:**

- [ ] All wiring diagrams updated
- [ ] All configuration files saved
- [ ] All test results documented
- [ ] All issues and resolutions documented
- [ ] Integration report complete

---

## 9. Testing Protocols and Validation

### 9.1 Pre-Power Testing

**CRITICAL: Complete all pre-power checks before applying power**

#### 9.1.1 Visual Inspection Checklist

**Electrical System:**

- [ ] All wiring complete per drawings
- [ ] All connections tight and secure
- [ ] No exposed conductors
- [ ] All wire labels in place
- [ ] All cable routing neat and secure
- [ ] No pinched or damaged cables
- [ ] All conduit properly installed
- [ ] All cable shields properly terminated
- [ ] All grounding connections secure
- [ ] All circuit breakers in OFF position

**Mechanical System:**

- [ ] All components securely mounted
- [ ] No loose fasteners
- [ ] All guards and covers installed
- [ ] No obstructions in robot workspace
- [ ] All sensors properly mounted
- [ ] All cables properly routed (no interference with motion)
- [ ] All emergency stop buttons accessible
- [ ] All safety signs posted

**Safety System:**

- [ ] All E-Stop buttons installed
- [ ] All safety interlocks installed
- [ ] Safety relay installed and wired
- [ ] All STO connections verified
- [ ] Safety circuit complete per drawings
- [ ] All safety labels installed

#### 9.1.2 Electrical Testing (De-Energized)

**Continuity Testing:**

- [ ] Verify continuity of all power conductors
- [ ] Verify continuity of all control conductors
- [ ] Verify continuity of all signal conductors
- [ ] Verify continuity of all ground conductors
- [ ] Verify continuity of all safety circuits

**Insulation Resistance Testing:**

**⚠️ WARNING: Disconnect sensitive electronics before megger testing ⚠️**

- [ ] Disconnect Jetson and sensitive electronics
- [ ] Disconnect drives (or set to test mode)
- [ ] Test insulation resistance (500V or 1000V megger):
  - Phase-to-phase: >1MΩ required
  - Phase-to-ground: >1MΩ required
  - Control circuits: >1MΩ required
- [ ] Document all measurements
- [ ] Reconnect electronics after testing

**Grounding Verification:**

- [ ] Measure ground resistance (should be <5Ω to earth)
- [ ] Verify ground continuity to all components (<0.1Ω)
- [ ] Verify no ground loops (measure voltage between grounds)
- [ ] Verify proper grounding topology (star ground)

**Polarity Verification:**

- [ ] Verify 24V DC polarity (+ and -)
- [ ] Verify motor phase sequence (U, V, W)
- [ ] Verify encoder polarity (+ and -)
- [ ] Verify sensor polarity

#### 9.1.3 Pre-Power Checklist

**Before applying any power:**

- [ ] All visual inspections complete
- [ ] All electrical tests complete and passed
- [ ] All personnel briefed on test procedure
- [ ] All personnel wearing appropriate PPE
- [ ] Emergency stop buttons tested (mechanical test)
- [ ] Fire extinguisher present and accessible
- [ ] First aid kit present and accessible
- [ ] Emergency contact numbers posted
- [ ] Work area clear of unnecessary personnel
- [ ] Supervisor approval obtained

### 9.2 Power-Up and Commissioning

#### 9.2.1 Initial Power-Up Procedure

**⚠️ WARNING: Licensed electrician must perform all high-voltage work ⚠️**

**Step 1: Control Power (24V DC)**

- [ ] Verify all circuit breakers OFF
- [ ] Verify LOTO devices removed (authorized personnel only)
- [ ] Wear arc-rated PPE
- [ ] Have observer present
- [ ] Close 24V DC circuit breaker
- [ ] Measure 24V DC voltage (should be 24V ±2V)
- [ ] Verify no unusual sounds or smells
- [ ] Verify no smoke or sparks
- [ ] Check for hot components (use thermal camera if available)
- [ ] If any issues, immediately open breaker and investigate

**Step 2: Safety System Power**

- [ ] Verify 24V DC stable
- [ ] Verify safety relay powers up
- [ ] Verify safety relay status LEDs (should indicate safe state)
- [ ] Test E-Stop button (press and release)
- [ ] Verify safety relay responds correctly
- [ ] Verify STO outputs de-energize when E-Stop pressed
- [ ] Reset E-Stop
- [ ] Verify safety relay resets (may require reset button)

**Step 3: Jetson Power (5V DC)**

- [ ] Verify 5V DC power supply output (5V ±0.25V)
- [ ] Apply power to Jetson
- [ ] Verify Jetson boots (monitor boot sequence)
- [ ] Verify no errors during boot
- [ ] Log in to Jetson
- [ ] Verify all services start correctly

**Step 4: Drive Control Power**

- [ ] Verify 24V DC stable
- [ ] Apply control power to drives (do not apply motor power yet)
- [ ] Verify each drive powers up
- [ ] Verify drive status LEDs
- [ ] Connect to each drive via software
- [ ] Verify drive configuration loaded
- [ ] Verify no drive faults

**Step 5: Motor Power (480V AC) - CRITICAL STEP**

**⚠️ EXTREME CAUTION: 480V AC IS LETHAL ⚠️**

- [ ] Verify all previous steps complete and successful
- [ ] Verify all personnel clear of equipment
- [ ] Verify all guards and covers installed
- [ ] Verify emergency stop buttons accessible
- [ ] Wear full arc-rated PPE (Category 2 minimum)
- [ ] Have observer present (also in PPE)
- [ ] Stand to side of electrical panel (not in front)
- [ ] Close main 480V circuit breaker (transformer primary)
- [ ] Verify transformer energizes (may hear hum)
- [ ] Measure transformer secondary voltage (480V ±5%)
- [ ] Verify phase balance (<2% imbalance)
- [ ] Verify no unusual sounds, smells, or smoke
- [ ] If any issues, immediately open breaker and investigate
- [ ] Close drive power circuit breakers (one at a time)
- [ ] Verify each drive receives motor power
- [ ] Verify drive status (should be "Ready" or "Standby")
- [ ] Verify no drive faults

**Step 6: Initial System Check**

- [ ] Verify all systems powered and operational
- [ ] Verify EtherCAT network operational (all devices in OP state)
- [ ] Verify all sensors reading correctly
- [ ] Verify all I/O functional
- [ ] Verify safety systems functional
- [ ] Document all voltage measurements
- [ ] Document any issues or anomalies

#### 9.2.2 First Motion Test

**⚠️ CRITICAL SAFETY: First motion test is high-risk ⚠️**

**Pre-Motion Checklist:**

- [ ] All power-up steps complete and successful
- [ ] All personnel briefed on test procedure
- [ ] All personnel clear of robot workspace (minimum 3m)
- [ ] Safety barriers in place
- [ ] Emergency stop buttons tested and accessible
- [ ] Supervisor present
- [ ] Video recording of test (for analysis if issues occur)

**Test Procedure (Single Axis):**

**Step 1: Brake Release Test**

- [ ] Select one axis for first test (typically Axis 1)
- [ ] Verify axis is in safe position (mid-travel)
- [ ] Enable drive (do not command motion yet)
- [ ] Verify brake releases (may hear click)
- [ ] Verify axis does not move (gravity load should be balanced)
- [ ] If axis moves unexpectedly, immediately disable drive and investigate

**Step 2: Minimal Motion Test**

- [ ] Command very small motion (0.1° or 0.1mm)
- [ ] Observe motion carefully:
  - Direction correct?
  - Smooth motion?
  - No unusual sounds?
  - No vibration?
  - Encoder feedback correct?
- [ ] If any issues, immediately stop and investigate
- [ ] If successful, command return to start position
- [ ] Verify axis returns correctly

**Step 3: Incremental Motion Test**

- [ ] Gradually increase motion distance:
  - 1° or 1mm
  - 5° or 5mm
  - 10° or 10mm
  - 45° or 50mm
- [ ] At each step, verify:
  - Smooth motion
  - Correct direction
  - Accurate positioning
  - No issues
- [ ] If any issues at any step, stop and investigate

**Step 4: Velocity Test**

- [ ] Gradually increase velocity:
  - 10% of maximum
  - 25% of maximum
  - 50% of maximum
  - 75% of maximum
  - 100% of maximum
- [ ] At each step, verify:
  - Smooth motion
  - No vibration
  - No unusual sounds
  - Accurate positioning
- [ ] If any issues at any step, stop and investigate

**Step 5: Full Range Test**

- [ ] Move axis through full range of motion
- [ ] Verify limit switches trigger correctly
- [ ] Verify smooth motion throughout range
- [ ] Verify no interference or binding

**Step 6: Repeat for All Axes**

- [ ] Repeat Steps 1-5 for each axis
- [ ] Test axes individually before coordinated motion
- [ ] Document results for each axis

**Step 7: Coordinated Motion Test**

- [ ] After all axes tested individually, test coordinated motion
- [ ] Start with simple motions (two axes)
- [ ] Gradually increase complexity
- [ ] Verify smooth coordinated motion
- [ ] Verify no interference between axes

#### 9.2.3 Commissioning Checklist

**System Commissioning Complete When:**

- [ ] All power systems operational
- [ ] All drives operational
- [ ] All motors operational
- [ ] All encoders operational
- [ ] All sensors operational
- [ ] All I/O operational
- [ ] All safety systems operational
- [ ] All axes move smoothly
- [ ] All axes reach full range of motion
- [ ] Coordinated motion functional
- [ ] No faults or errors
- [ ] All tests documented

### 9.3 Performance Validation

#### 9.3.1 Positioning Accuracy Test

**Purpose:** Verify robot can position end-effector accurately

**Equipment Required:**
- Laser tracker or CMM (±0.01mm accuracy)
- Calibration target (sphere or retroreflector)

**Test Procedure:**

**Step 1: Setup**

- [ ] Mount calibration target on robot end-effector
- [ ] Set up laser tracker or CMM
- [ ] Calibrate measurement system
- [ ] Define test points (minimum 20 points throughout workspace)

**Step 2: Measurement**

For each test point:
- [ ] Command robot to test point
- [ ] Allow robot to settle (2 seconds)
- [ ] Measure actual position with laser tracker
- [ ] Record commanded position and actual position
- [ ] Calculate position error (Euclidean distance)

**Step 3: Analysis**

- [ ] Calculate mean position error
- [ ] Calculate maximum position error
- [ ] Calculate standard deviation
- [ ] Create error map (visualize errors in workspace)

**Acceptance Criteria:**
- [ ] Mean error <0.05mm
- [ ] Maximum error <0.10mm
- [ ] Standard deviation <0.02mm

**If criteria not met:**
- [ ] Check for mechanical issues (loose fasteners, worn bearings)
- [ ] Verify encoder calibration
- [ ] Verify kinematics parameters
- [ ] Recalibrate robot if necessary

#### 9.3.2 Repeatability Test

**Purpose:** Verify robot can return to same position repeatedly

**Test Procedure:**

**Step 1: Setup**

- [ ] Select test point (typically center of workspace)
- [ ] Set up measurement system (laser tracker or dial indicator)

**Step 2: Measurement**

- [ ] Command robot to test point
- [ ] Measure position
- [ ] Move robot away (at least 100mm)
- [ ] Return robot to test point
- [ ] Measure position again
- [ ] Repeat 30 times

**Step 3: Analysis**

- [ ] Calculate mean position
- [ ] Calculate standard deviation (repeatability)
- [ ] Calculate maximum deviation

**Acceptance Criteria:**
- [ ] Repeatability (±3σ) <0.02mm

**If criteria not met:**
- [ ] Check for backlash in mechanical system
- [ ] Verify encoder resolution adequate
- [ ] Check for thermal drift (allow warm-up time)
- [ ] Verify control system tuning

#### 9.3.3 Path Accuracy Test

**Purpose:** Verify robot can follow desired path accurately

**Test Procedure:**

**Step 1: Setup**

- [ ] Define test path (e.g., straight line, circle, complex curve)
- [ ] Set up measurement system (laser tracker with continuous tracking)

**Step 2: Measurement**

- [ ] Command robot to follow test path
- [ ] Measure actual path with laser tracker
- [ ] Record path at high frequency (100Hz minimum)
- [ ] Repeat 10 times

**Step 3: Analysis**

- [ ] Calculate path error (perpendicular distance from desired path)
- [ ] Calculate mean path error
- [ ] Calculate maximum path error
- [ ] Visualize path error along trajectory

**Acceptance Criteria:**
- [ ] Mean path error <0.10mm
- [ ] Maximum path error <0.20mm

**If criteria not met:**
- [ ] Check trajectory planning (velocity profiling)
- [ ] Verify control loop tuning (PID gains)
- [ ] Check for mechanical compliance
- [ ] Verify feedforward compensation

#### 9.3.4 Velocity and Acceleration Test

**Purpose:** Verify robot can achieve required velocities and accelerations

**Test Procedure:**

**Step 1: Velocity Test**

- [ ] Command robot to move at specific velocity
- [ ] Measure actual velocity (from encoder feedback)
- [ ] Repeat for multiple velocities (10%, 25%, 50%, 75%, 100%)
- [ ] Calculate velocity error

**Acceptance Criteria:**
- [ ] Velocity error <5% of commanded velocity

**Step 2: Acceleration Test**

- [ ] Command robot to accelerate at specific rate
- [ ] Measure actual acceleration (from encoder feedback)
- [ ] Repeat for multiple accelerations
- [ ] Calculate acceleration error

**Acceptance Criteria:**
- [ ] Acceleration error <10% of commanded acceleration

#### 9.3.5 Force Control Test (If Applicable)

**Purpose:** Verify force control accuracy

**Test Procedure:**

**Step 1: Setup**

- [ ] Mount force/torque sensor on robot
- [ ] Set up test fixture (e.g., compliant surface)

**Step 2: Force Control Test**

- [ ] Command robot to apply specific force
- [ ] Measure actual force (from F/T sensor)
- [ ] Repeat for multiple forces (5N, 10N, 20N, 40N)
- [ ] Calculate force error

**Acceptance Criteria:**
- [ ] Force error <2% of full scale (±0.8N for 40N sensor)

**Step 3: Compliance Test**

- [ ] Enable force control
- [ ] Manually push robot
- [ ] Verify robot yields to external force
- [ ] Verify robot maintains desired force

#### 9.3.6 Cycle Time Test

**Purpose:** Verify robot can complete tasks in required time

**Test Procedure:**

**Step 1: Define Test Cycle**

- [ ] Select representative task (e.g., pick-and-place, machining operation)
- [ ] Define start and end points

**Step 2: Measurement**

- [ ] Run test cycle 10 times
- [ ] Measure cycle time for each run
- [ ] Calculate mean cycle time
- [ ] Calculate standard deviation

**Step 3: Comparison**

- [ ] Compare to baseline (original system)
- [ ] Calculate percentage difference

**Acceptance Criteria:**
- [ ] Cycle time within 90-110% of baseline

#### 9.3.7 Endurance Test

**Purpose:** Verify system reliability over extended operation

**Test Procedure:**

**Step 1: Setup**

- [ ] Define test program (representative of typical operation)
- [ ] Set up monitoring (temperatures, currents, errors)
- [ ] Prepare for extended test (8+ hours)

**Step 2: Execution**

- [ ] Start test program
- [ ] Run continuously for 8 hours minimum
- [ ] Monitor system continuously
- [ ] Log all data (positions, velocities, temperatures, currents, errors)

**Step 3: Analysis**

- [ ] Review all logged data
- [ ] Check for:
  - Temperature rise (should stabilize)
  - Position drift (should be minimal)
  - Errors or faults (should be zero)
  - Performance degradation (should be none)

**Acceptance Criteria:**
- [ ] No faults or errors during test
- [ ] No performance degradation
- [ ] Temperatures within limits (<70°C)
- [ ] Position accuracy maintained

### 9.4 Safety System Validation

**Comprehensive safety testing per Section 7.2**

- [ ] Emergency stop system tested
- [ ] Safe Torque Off tested
- [ ] Safety relay tested
- [ ] Response times measured (<50ms)
- [ ] All safety interlocks tested
- [ ] Safety system documentation complete

### 9.5 Validation Documentation

#### 9.5.1 Test Report Template

**Test Report Contents:**

1. **Test Information**
   - Test name and number
   - Date and time
   - Personnel (names and roles)
   - Equipment used

2. **Test Procedure**
   - Detailed procedure followed
   - Any deviations from planned procedure

3. **Test Results**
   - Raw data (tables, graphs)
   - Calculated results
   - Pass/fail determination

4. **Issues and Observations**
   - Any issues encountered
   - Unusual observations
   - Recommendations

5. **Conclusions**
   - Summary of results
   - Compliance with requirements
   - Next steps

6. **Approvals**
   - Signatures of test personnel
   - Supervisor approval

#### 9.5.2 Validation Checklist

**System Validation Complete When:**

- [ ] All pre-power tests passed
- [ ] Power-up successful
- [ ] First motion tests successful
- [ ] All axes operational
- [ ] Positioning accuracy validated (<0.05mm)
- [ ] Repeatability validated (<0.02mm)
- [ ] Path accuracy validated (<0.10mm)
- [ ] Velocity control validated
- [ ] Force control validated (if applicable)
- [ ] Cycle time validated (90-110% of baseline)
- [ ] Endurance test passed (8+ hours)
- [ ] Safety systems validated
- [ ] All tests documented
- [ ] All issues resolved
- [ ] System approved for production use

---

## 10. Troubleshooting Guides

### 10.1 Electrical Issues

#### 10.1.1 No Power to System

**Symptoms:**
- No power indicators
- System completely dead

**Diagnostic Steps:**

1. **Check Main Power**
   - [ ] Verify 480V power available at main disconnect
   - [ ] Check main circuit breaker (should be closed)
   - [ ] Measure voltage at main disconnect (480V 3-phase)
   - [ ] Check for tripped breakers upstream

2. **Check Transformer**
   - [ ] Verify transformer primary voltage (480V)
   - [ ] Verify transformer secondary voltage (480V)
   - [ ] Check transformer fuses (if equipped)
   - [ ] Listen for transformer hum (should be present)

3. **Check Control Power**
   - [ ] Verify 24V DC power supply output (24V)
   - [ ] Check 24V circuit breakers
   - [ ] Measure voltage at loads

4. **Check Jetson Power**
   - [ ] Verify 5V DC power supply output (5V)
   - [ ] Check connections to Jetson
   - [ ] Verify Jetson power LED

**Common Causes:**
- Tripped circuit breaker
- Blown fuse
- Loose connection
- Failed power supply
- LOTO device not removed

**Resolution:**
- Reset tripped breakers (investigate cause first)
- Replace blown fuses (investigate cause first)
- Tighten loose connections
- Replace failed power supply
- Remove LOTO devices (authorized personnel only)

#### 10.1.2 Drive Faults

**Symptoms:**
- Drive status LED shows fault
- Drive error message
- Motor does not move

**Diagnostic Steps:**

1. **Identify Fault Code**
   - [ ] Read fault code from drive display or software
   - [ ] Consult drive manual for fault description

2. **Common Fault Codes:**

**Overcurrent Fault:**
- **Cause:** Motor current exceeded limit
- **Check:** Motor wiring (short circuit?), motor insulation, load on motor
- **Resolution:** Fix wiring issue, reduce load, increase current limit (if appropriate)

**Overvoltage Fault:**
- **Cause:** DC bus voltage too high
- **Check:** Input voltage, regenerative braking, deceleration rate
- **Resolution:** Check input voltage, add braking resistor, reduce deceleration rate

**Undervoltage Fault:**
- **Cause:** DC bus voltage too low
- **Check:** Input voltage, power supply capacity, loose connections
- **Resolution:** Fix input voltage, increase power supply capacity, tighten connections

**Encoder Fault:**
- **Cause:** Encoder signal lost or invalid
- **Check:** Encoder wiring, encoder power, encoder alignment
- **Resolution:** Fix wiring, verify encoder power (5V), realign encoder

**Following Error:**
- **Cause:** Actual position differs from commanded position by too much
- **Check:** Mechanical binding, insufficient motor torque, control tuning
- **Resolution:** Remove binding, increase current limit, retune control loop

**STO Active:**
- **Cause:** Safe Torque Off input active (safety system)
- **Check:** E-Stop buttons, safety relay, STO wiring
- **Resolution:** Release E-Stop, reset safety system, fix STO wiring

**Communication Error:**
- **Cause:** EtherCAT communication lost
- **Check:** Network cable, network configuration, master status
- **Resolution:** Fix cable, verify configuration, restart master

3. **Clear Fault**
   - [ ] Resolve underlying cause
   - [ ] Clear fault (reset drive)
   - [ ] Verify drive returns to ready state
   - [ ] Test operation

#### 10.1.3 EtherCAT Communication Issues

**Symptoms:**
- Devices not detected
- Communication errors
- Devices in INIT or PREOP state (not OP)

**Diagnostic Steps:**

1. **Check Physical Layer**
   - [ ] Verify all cables connected
   - [ ] Check cable quality (use cable tester)
   - [ ] Verify link LEDs on devices (should be green)
   - [ ] Check for damaged cables

2. **Check Network Configuration**
   - [ ] Verify master configuration
   - [ ] Verify device addresses
   - [ ] Verify PDO mappings
   - [ ] Check for address conflicts

3. **Check Device Status**
   - [ ] Read device state (INIT, PREOP, SAFEOP, OP)
   - [ ] If not OP, check device error register
   - [ ] Consult device manual for error codes

4. **Check Timing**
   - [ ] Verify cycle time (should be 1ms)
   - [ ] Check for cycle time violations
   - [ ] Verify distributed clocks synchronized

**Common Causes:**
- Damaged cable
- Loose connection
- Incorrect configuration
- Device fault
- EMI interference

**Resolution:**
- Replace damaged cable
- Tighten connections
- Correct configuration
- Resolve device fault
- Add shielding, ferrite cores

#### 10.1.4 Encoder Issues

**Symptoms:**
- Encoder fault on drive
- Incorrect position feedback
- Erratic motion

**Diagnostic Steps:**

1. **Check Encoder Power**
   - [ ] Measure encoder power at motor (should be 5V ±0.25V)
   - [ ] Check encoder power supply
   - [ ] Check wiring for voltage drop

2. **Check Encoder Signals**
   - [ ] Use oscilloscope to view encoder signals
   - [ ] Verify differential signals (A, A', B, B')
   - [ ] Verify quadrature relationship (A and B 90° out of phase)
   - [ ] Verify index pulse (Z)
   - [ ] Check signal amplitude (should be >2V differential)

3. **Check Encoder Wiring**
   - [ ] Verify wiring per motor documentation
   - [ ] Check for damaged cable
   - [ ] Check for loose connections
   - [ ] Verify shield grounded at one end only

4. **Check Encoder Alignment**
   - [ ] Verify encoder mechanically aligned with motor shaft
   - [ ] Check for excessive runout
   - [ ] Verify encoder mounting secure

**Common Causes:**
- Insufficient encoder power
- Damaged encoder cable
- EMI interference
- Encoder misalignment
- Failed encoder

**Resolution:**
- Fix encoder power supply
- Replace damaged cable
- Add shielding, separate from power cables
- Realign encoder
- Replace failed encoder

### 10.2 Mechanical Issues

#### 10.2.1 Binding or Sticking

**Symptoms:**
- Axis difficult to move
- High motor current
- Following error
- Jerky motion

**Diagnostic Steps:**

1. **Manual Movement Test**
   - [ ] Disable drives (remove power)
   - [ ] Manually move axis
   - [ ] Feel for binding or resistance
   - [ ] Identify location of binding

2. **Check for Obstructions**
   - [ ] Visual inspection for obstructions
   - [ ] Check cable routing (cables snagging?)
   - [ ] Check for debris or contamination

3. **Check Mechanical Components**
   - [ ] Check bearings (worn or damaged?)
   - [ ] Check gears (worn or damaged?)
   - [ ] Check belts (too tight?)
   - [ ] Check lubrication (insufficient?)

4. **Check Alignment**
   - [ ] Verify components aligned
   - [ ] Check for bent shafts
   - [ ] Check for loose mounting

**Resolution:**
- Remove obstructions
- Replace worn components
- Adjust belt tension
- Lubricate as needed
- Realign components
- Tighten loose mounting

#### 10.2.2 Excessive Vibration

**Symptoms:**
- Visible vibration
- Audible noise
- Poor surface finish
- Reduced accuracy

**Diagnostic Steps:**

1. **Identify Frequency**
   - [ ] Use vibration sensor or accelerometer
   - [ ] Determine vibration frequency
   - [ ] Compare to motor speed, gear ratios

2. **Check Mechanical Components**
   - [ ] Check for loose fasteners
   - [ ] Check for unbalanced rotating parts
   - [ ] Check for worn bearings
   - [ ] Check for damaged gears

3. **Check Control System**
   - [ ] Check control loop tuning (too aggressive?)
   - [ ] Check for resonance (natural frequency?)
   - [ ] Check velocity profiling (too fast acceleration?)

**Common Causes:**
- Loose fasteners
- Unbalanced rotating parts
- Worn bearings
- Control loop instability
- Mechanical resonance

**Resolution:**
- Tighten loose fasteners
- Balance rotating parts
- Replace worn bearings
- Retune control loops
- Add damping, change natural frequency

#### 10.2.3 Inaccurate Positioning

**Symptoms:**
- Position error exceeds tolerance
- Repeatability poor
- Path error excessive

**Diagnostic Steps:**

1. **Verify Encoder Function**
   - [ ] Check encoder signals (see Section 10.1.4)
   - [ ] Verify encoder resolution
   - [ ] Check for encoder errors

2. **Check Mechanical System**
   - [ ] Check for backlash (gears, belts)
   - [ ] Check for compliance (flexing)
   - [ ] Check for thermal expansion

3. **Check Kinematics**
   - [ ] Verify kinematics parameters (DH parameters)
   - [ ] Check for calibration errors
   - [ ] Verify tool offset

4. **Check Control System**
   - [ ] Verify control loop tuning
   - [ ] Check for following error
   - [ ] Verify feedforward compensation

**Resolution:**
- Fix encoder issues
- Reduce backlash (adjust preload, replace worn parts)
- Increase stiffness (reinforce structure)
- Recalibrate robot
- Retune control loops

### 10.3 Software Issues

#### 10.3.1 Real-Time Performance Issues

**Symptoms:**
- Control loop jitter
- Missed deadlines
- Jerky motion
- Communication errors

**Diagnostic Steps:**

1. **Check CPU Load**
   - [ ] Monitor CPU usage (should be <80%)
   - [ ] Identify high-load processes
   - [ ] Check for background processes

2. **Check Real-Time Configuration**
   - [ ] Verify PREEMPT_RT kernel installed
   - [ ] Verify CPU core isolation
   - [ ] Verify process priorities
   - [ ] Verify memory locking

3. **Check Timing**
   - [ ] Measure control loop timing
   - [ ] Check for timing violations
   - [ ] Verify cycle time consistent

**Resolution:**
- Reduce CPU load (optimize code, disable unnecessary processes)
- Configure real-time properly (see coding_tasks.md)
- Increase cycle time if necessary
- Optimize algorithms

#### 10.3.2 ML Inference Issues

**Symptoms:**
- Slow inference (<10ms target)
- Incorrect predictions
- System crashes

**Diagnostic Steps:**

1. **Check Model Performance**
   - [ ] Measure inference time
   - [ ] Check GPU utilization
   - [ ] Verify TensorRT optimization

2. **Check Input Data**
   - [ ] Verify camera images valid
   - [ ] Check image preprocessing
   - [ ] Verify sensor data valid

3. **Check Model Loading**
   - [ ] Verify model file present
   - [ ] Check model version
   - [ ] Verify model compatible with TensorRT version

**Resolution:**
- Optimize model (see coding_tasks.md)
- Fix input data issues
- Update model file
- Increase inference cycle time if necessary

#### 10.3.3 Safety System Software Issues

**Symptoms:**
- False E-Stop triggers
- Safety system not responding
- Incorrect safety state

**Diagnostic Steps:**

1. **Check Safety Inputs**
   - [ ] Verify E-Stop button states
   - [ ] Check safety relay status
   - [ ] Verify STO inputs

2. **Check Safety Logic**
   - [ ] Review safety logic code
   - [ ] Verify correct implementation
   - [ ] Check for race conditions

3. **Check Safety Timing**
   - [ ] Measure safety response time
   - [ ] Verify <50ms requirement met

**Resolution:**
- Fix input wiring issues
- Correct safety logic code
- Optimize safety response time
- Add debouncing if false triggers

### 10.4 Sensor Issues

#### 10.4.1 Camera Issues

**Symptoms:**
- No image
- Poor image quality
- Low frame rate

**Diagnostic Steps:**

1. **Check Camera Connection**
   - [ ] Verify USB cable connected
   - [ ] Check USB port (use `lsusb`)
   - [ ] Try different USB port

2. **Check Camera Settings**
   - [ ] Verify resolution and frame rate
   - [ ] Check exposure settings
   - [ ] Verify focus

3. **Check Lighting**
   - [ ] Verify adequate lighting
   - [ ] Check for backlighting
   - [ ] Adjust exposure if necessary

**Resolution:**
- Fix connection issues
- Adjust camera settings
- Improve lighting

#### 10.4.2 Force/Torque Sensor Issues

**Symptoms:**
- Incorrect force readings
- Noisy signal
- Sensor drift

**Diagnostic Steps:**

1. **Check Sensor Connection**
   - [ ] Verify wiring
   - [ ] Check power supply (24V)
   - [ ] Verify communication

2. **Check Calibration**
   - [ ] Verify zero calibration
   - [ ] Check gravity compensation
   - [ ] Verify calibration matrix

3. **Check for Interference**
   - [ ] Check for EMI sources
   - [ ] Verify cable shielding
   - [ ] Check grounding

**Resolution:**
- Fix wiring issues
- Recalibrate sensor
- Add shielding, improve grounding

### 10.5 Troubleshooting Flowcharts

#### 10.5.1 System Won't Start Flowchart

```
System Won't Start
        |
        v
    Power present? ----NO----> Check main power
        |                      Check circuit breakers
       YES                     Check LOTO devices
        |
        v
    24V DC present? ---NO----> Check 24V power supply
        |                      Check 24V breakers
       YES                     Check wiring
        |
        v
    Jetson boots? -----NO----> Check 5V power
        |                      Check Jetson connections
       YES                     Check Jetson (may be failed)
        |
        v
    Drives power up? --NO----> Check drive power
        |                      Check drive fuses
       YES                     Check drive configuration
        |
        v
    EtherCAT OK? ------NO----> Check network cables
        |                      Check network configuration
       YES                     Check device status
        |
        v
    Safety system OK? -NO----> Check E-Stop buttons
        |                      Check safety relay
       YES                     Check STO wiring
        |
        v
    System Ready!
```

#### 10.5.2 Axis Won't Move Flowchart

```
Axis Won't Move
        |
        v
    Drive enabled? ----NO----> Enable drive
        |                      Check enable signal
       YES
        |
        v
    Drive ready? ------NO----> Check drive fault
        |                      Clear fault
       YES                     Check drive status
        |
        v
    STO active? -------YES---> Release E-Stop
        |                      Reset safety system
        NO
        |
        v
    Brake released? ---NO----> Check brake wiring
        |                      Check brake power
       YES                     Check brake function
        |
        v
    Command received? -NO----> Check communication
        |                      Check software
       YES
        |
        v
    Mechanical binding? YES--> Remove obstruction
        |                      Check lubrication
        NO                     Check alignment
        |
        v
    Encoder OK? -------NO----> Check encoder wiring
        |                      Check encoder power
       YES                     Check encoder signals
        |
        v
    Check control tuning
    Check motor current
    Check for overload
```

### 10.6 Common Error Messages

| Error Message | Possible Cause | Resolution |
|--------------|----------------|------------|
| "EtherCAT device not found" | Cable disconnected, device powered off | Check cables, check device power |
| "Drive overcurrent fault" | Motor short circuit, overload | Check motor wiring, reduce load |
| "Encoder error" | Encoder wiring issue, encoder failed | Check encoder wiring, replace encoder |
| "Following error exceeded" | Mechanical binding, insufficient torque | Remove binding, increase current limit |
| "E-Stop active" | E-Stop button pressed | Release E-Stop, reset system |
| "STO active" | Safety system triggered | Check safety inputs, reset safety system |
| "Communication timeout" | Network issue, device not responding | Check network, check device status |
| "Position limit exceeded" | Commanded position outside limits | Check commanded position, adjust limits |
| "Velocity limit exceeded" | Commanded velocity too high | Reduce velocity, adjust limits |
| "Temperature warning" | Motor or drive overheating | Reduce load, improve cooling, check for issues |

---

## 11. Documentation and Reporting Requirements

### 11.1 Daily Documentation

#### 11.1.1 Daily Work Log

**Required Information:**
- Date
- Personnel present
- Tasks performed
- Hours worked per task
- Materials used
- Issues encountered
- Resolutions implemented
- Tasks completed
- Tasks remaining
- Notes and observations

**Template:**

```
DAILY WORK LOG

Date: _______________
Project: Kuka Robot Arm AI Controller Replacement
Phase: _______________

Personnel:
- Name: _______________ Role: _______________
- Name: _______________ Role: _______________

Tasks Performed:
1. _______________________________________________
   Status: [ ] Complete [ ] In Progress [ ] Blocked
   Hours: _______

2. _______________________________________________
   Status: [ ] Complete [ ] In Progress [ ] Blocked
   Hours: _______

Materials Used:
- _______________________________________________
- _______________________________________________

Issues Encountered:
1. _______________________________________________
   Resolution: _____________________________________

2. _______________________________________________
   Resolution: _____________________________________

Safety Incidents: [ ] None [ ] See incident report

Notes:
___________________________________________________
___________________________________________________

Next Day Tasks:
1. _______________________________________________
2. _______________________________________________

Supervisor Signature: _______________ Date: _______
```

#### 11.1.2 Safety Checklist

**Complete daily before work:**

```
DAILY SAFETY CHECKLIST

Date: _______________

Pre-Work Safety Check:
[ ] All personnel have required PPE
[ ] PPE inspected and in good condition
[ ] Work area clean and organized
[ ] Emergency stop buttons tested
[ ] Fire extinguisher present and charged
[ ] First aid kit accessible
[ ] Emergency contact numbers posted
[ ] All personnel briefed on day's tasks
[ ] Hazards identified and mitigated

High Voltage Work (if applicable):
[ ] Arc-rated PPE worn
[ ] Voltage detector available
[ ] Insulated tools available
[ ] Observer present
[ ] LOTO procedures followed

Notes:
___________________________________________________

Completed by: _______________ Time: _______________
```

### 11.2 Test Documentation

#### 11.2.1 Test Report Template

**Use for all formal tests:**

```
TEST REPORT

Test ID: _______________
Test Name: _______________________________________________
Date: _______________
Time: _______________

Personnel:
- Test Engineer: _______________
- Technician: _______________
- Observer: _______________
- Supervisor: _______________

Equipment Used:
- _______________________________________________
- _______________________________________________

Test Objective:
___________________________________________________
___________________________________________________

Test Procedure:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Test Results:
___________________________________________________
___________________________________________________

Data:
[Attach data tables, graphs, screenshots]

Pass/Fail Criteria:
___________________________________________________

Result: [ ] PASS [ ] FAIL

Issues Encountered:
___________________________________________________
___________________________________________________

Recommendations:
___________________________________________________
___________________________________________________

Approvals:
Test Engineer: _______________ Date: _______________
Supervisor: _______________ Date: _______________
```

#### 11.2.2 Test Data Recording

**Record all test data:**
- Raw measurements
- Calculated results
- Timestamps
- Environmental conditions (temperature, humidity)
- System configuration
- Software versions

**Data Storage:**
- Save data in structured format (CSV, JSON)
- Include metadata (test ID, date, personnel)
- Backup data to multiple locations
- Maintain data for duration of project + 5 years

### 11.3 Compliance Documentation

#### 11.3.1 Safety Compliance Report

**Required for ISO 13849-1 compliance:**

```
SAFETY COMPLIANCE REPORT

Project: Kuka Robot Arm AI Controller Replacement
Date: _______________
Prepared by: _______________

1. RISK ASSESSMENT
   - Hazards identified: _______________
   - Risk levels: _______________
   - Mitigation measures: _______________
   - Residual risk: _______________

2. SAFETY SYSTEM ARCHITECTURE
   - Category: 3
   - Performance Level: d (PLd)
   - Architecture diagram: [Attach]

3. SAFETY COMPONENTS
   - Emergency stop buttons: _______________
   - Safety relay: _______________
   - Safe Torque Off: _______________
   - Other: _______________

4. SAFETY TESTING
   - E-Stop response time: _______ ms (<50ms required)
   - STO response time: _______ ms (<10ms required)
   - Test results: [Attach]

5. COMPLIANCE STATEMENT
   This system complies with:
   [ ] ISO 13849-1 Category 3, PLd
   [ ] IEC 61800-5-2 (Drive safety)
   [ ] NFPA 70E (Electrical safety)

6. VALIDATION
   - Validation date: _______________
   - Validated by: _______________
   - Independent review: [ ] Yes [ ] No
   - Reviewer: _______________

Approvals:
Safety Engineer: _______________ Date: _______________
Project Manager: _______________ Date: _______________
```

#### 11.3.2 Electrical Compliance Documentation

**Required for electrical inspection:**

- [ ] Electrical drawings (as-built)
- [ ] Arc flash analysis
- [ ] Arc flash labels installed
- [ ] Grounding verification test results
- [ ] Insulation resistance test results
- [ ] Voltage measurements
- [ ] Load calculations
- [ ] Circuit breaker coordination study
- [ ] LOTO procedures
- [ ] Electrical safety training records

### 11.4 Maintenance Documentation

#### 11.4.1 Maintenance Log

**Record all maintenance activities:**

```
MAINTENANCE LOG

Equipment: Kuka Robot Arm AI Controller System
Serial Number: _______________

Date: _______________
Maintenance Type: [ ] Preventive [ ] Corrective [ ] Emergency

Performed by: _______________

Tasks Performed:
[ ] Visual inspection
[ ] Lubrication
[ ] Fastener torque check
[ ] Electrical connections check
[ ] Safety system test
[ ] Calibration
[ ] Software update
[ ] Other: _______________

Parts Replaced:
- Part: _______________ Qty: ___ Serial: _______________
- Part: _______________ Qty: ___ Serial: _______________

Issues Found:
___________________________________________________
___________________________________________________

Corrective Actions:
___________________________________________________
___________________________________________________

System Status After Maintenance:
[ ] Operational
[ ] Requires additional work
[ ] Out of service

Next Maintenance Due: _______________

Supervisor Approval: _______________ Date: _______________
```

#### 11.4.2 Preventive Maintenance Schedule

**Daily:**
- Visual inspection
- Safety system test (E-Stop buttons)
- Check for unusual sounds or vibrations

**Weekly:**
- Clean work area
- Check cable routing (no damage or wear)
- Test all safety interlocks
- Check for loose fasteners

**Monthly:**
- Lubricate moving parts per manufacturer specifications
- Torque check critical fasteners
- Test all sensors
- Backup system configuration
- Review error logs

**Quarterly:**
- Comprehensive safety system test
- Calibration verification
- Encoder alignment check
- Temperature sensor calibration
- Force/torque sensor calibration
- Software updates

**Annually:**
- Complete system recalibration
- Replace wear items (belts, bearings as needed)
- Electrical system inspection
- Insulation resistance testing
- Safety certification renewal
- Third-party audit (recommended)

### 11.5 Incident Reporting

#### 11.5.1 Incident Report Form

**Complete for all safety incidents, near-misses, and equipment failures:**

```
INCIDENT REPORT

Incident ID: _______________
Date: _______________ Time: _______________
Location: _______________

Reported by: _______________
Supervisor: _______________

Incident Type:
[ ] Safety incident (injury)
[ ] Near-miss (no injury)
[ ] Equipment failure
[ ] Property damage
[ ] Other: _______________

Severity:
[ ] Minor (no injury, minimal damage)
[ ] Moderate (minor injury, moderate damage)
[ ] Serious (significant injury or damage)
[ ] Critical (life-threatening or major damage)

Description:
___________________________________________________
___________________________________________________
___________________________________________________

Personnel Involved:
- Name: _______________ Role: _______________
- Name: _______________ Role: _______________

Witnesses:
- Name: _______________ Contact: _______________
- Name: _______________ Contact: _______________

Immediate Actions Taken:
___________________________________________________
___________________________________________________

Root Cause Analysis:
___________________________________________________
___________________________________________________

Corrective Actions:
1. _______________________________________________
   Responsible: _______________ Due: _______________

2. _______________________________________________
   Responsible: _______________ Due: _______________

Preventive Actions:
___________________________________________________
___________________________________________________

Follow-Up Required: [ ] Yes [ ] No
Follow-Up Date: _______________

Approvals:
Supervisor: _______________ Date: _______________
Safety Officer: _______________ Date: _______________
Project Manager: _______________ Date: _______________
```

#### 11.5.2 Incident Investigation

**For serious incidents, conduct formal investigation:**

1. **Secure the Scene**
   - Do not disturb evidence
   - Photograph scene
   - Document equipment state

2. **Gather Information**
   - Interview personnel involved
   - Interview witnesses
   - Review logs and data
   - Review procedures

3. **Analyze**
   - Identify root cause (use 5 Whys, Fishbone diagram)
   - Identify contributing factors
   - Identify systemic issues

4. **Develop Corrective Actions**
   - Address root cause
   - Address contributing factors
   - Prevent recurrence

5. **Implement and Verify**
   - Implement corrective actions
   - Verify effectiveness
   - Update procedures
   - Train personnel

6. **Document**
   - Complete investigation report
   - Share lessons learned
   - Update risk assessment

### 11.6 Project Documentation Package

**At project completion, compile comprehensive documentation package:**

#### 11.6.1 Technical Documentation

- [ ] System overview and specifications
- [ ] Electrical drawings (as-built)
- [ ] Mechanical drawings (as-built)
- [ ] Network topology diagram
- [ ] Software architecture documentation
- [ ] Configuration files (backed up)
- [ ] Calibration data
- [ ] Performance test results
- [ ] Validation reports

#### 11.6.2 Safety Documentation

- [ ] Risk assessment
- [ ] Safety system documentation
- [ ] Safety compliance report
- [ ] Safety test results
- [ ] Arc flash analysis
- [ ] LOTO procedures
- [ ] Safety training records

#### 11.6.3 Operational Documentation

- [ ] Operating procedures
- [ ] Maintenance procedures
- [ ] Troubleshooting guide
- [ ] Emergency procedures
- [ ] Training materials
- [ ] Spare parts list

#### 11.6.4 Compliance Documentation

- [ ] Electrical permits and inspections
- [ ] Safety certifications
- [ ] Compliance statements
- [ ] Third-party audit reports (if applicable)

#### 11.6.5 Project Records

- [ ] Daily work logs
- [ ] Test reports
- [ ] Incident reports
- [ ] Change orders
- [ ] Lessons learned

**Documentation Format:**
- Organize in binder or digital folder structure
- Include table of contents
- Include revision history
- Provide copies to:
  - Operations team
  - Maintenance team
  - Management
  - Archive (long-term storage)

---

## 12. Appendices

### 12.1 Reference Standards and Regulations

#### 12.1.1 Safety Standards

**ISO 13849-1: Safety of machinery - Safety-related parts of control systems**
- Defines safety categories (B, 1, 2, 3, 4)
- Defines performance levels (a, b, c, d, e)
- This project requires Category 3, Performance Level d (PLd)
- Available from: ISO (www.iso.org)

**IEC 61800-5-2: Adjustable speed electrical power drive systems - Safety requirements - Functional**
- Defines safety functions for drive systems
- Includes Safe Torque Off (STO), Safe Stop 1 (SS1), etc.
- This project requires STO implementation
- Available from: IEC (www.iec.ch)

**ISO 12100: Safety of machinery - General principles for design - Risk assessment and risk reduction**
- Framework for risk assessment
- Hierarchy of risk reduction measures
- Required for compliance documentation
- Available from: ISO (www.iso.org)

#### 12.1.2 Electrical Standards

**NFPA 70E: Standard for Electrical Safety in the Workplace**
- Electrical safety requirements for 480V systems
- Arc flash hazard analysis
- PPE requirements
- LOTO procedures
- Available from: NFPA (www.nfpa.org)

**NEC (NFPA 70): National Electrical Code**
- Electrical installation requirements
- Wiring methods
- Grounding requirements
- Circuit protection
- Available from: NFPA (www.nfpa.org)

**IEC 61158: Industrial communication networks - Fieldbus specifications**
- Includes EtherCAT protocol specification
- Available from: IEC (www.iec.ch)

#### 12.1.3 Robot Standards

**ISO 10218-1: Robots and robotic devices - Safety requirements for industrial robots - Part 1: Robots**
- Safety requirements for robot design
- Protective measures
- Information for use
- Available from: ISO (www.iso.org)

**ISO 10218-2: Robots and robotic devices - Safety requirements for industrial robots - Part 2: Robot systems and integration**
- Safety requirements for robot system integration
- Risk assessment
- Safeguarding
- Available from: ISO (www.iso.org)

### 12.2 Vendor Contact Information

#### 12.2.1 Component Manufacturers

**Kuka Robotics**
- Website: www.kuka.com
- Technical Support: [Contact via website]
- For: Robot documentation, spare parts, technical assistance

**Kollmorgen (Motor Drives)**
- Website: www.kollmorgen.com
- Technical Support: 1-540-633-3545
- For: AKD-P drive support, configuration assistance

**Beckhoff Automation (Motor Drives, I/O)**
- Website: www.beckhoff.com
- Technical Support: 1-952-890-0000
- For: AX5000 drives, EtherCAT I/O modules

**NVIDIA (Jetson)**
- Website: developer.nvidia.com/embedded-computing
- Developer Forums: forums.developer.nvidia.com
- For: Jetson support, software issues

**Intel (RealSense Cameras)**
- Website: www.intelrealsense.com
- Support: [Contact via website]
- For: RealSense D435 support

**ATI Industrial Automation (Force/Torque Sensors)**
- Website: www.ati-ia.com
- Technical Support: 1-919-772-0115
- For: Force/torque sensor support, calibration

**Pilz (Safety Components)**
- Website: www.pilz.com
- Technical Support: 1-877-745-9872
- For: Safety relay support, safety system design

#### 12.2.2 Training Providers

**NFPA 70E Training**
- Multiple providers available
- Search: "NFPA 70E training near me"
- Verify provider is qualified

**Arc Flash Training**
- Multiple providers available
- Often combined with NFPA 70E training

**OSHA Training**
- OSHA Training Institute: www.osha.gov/oti
- Authorized trainers: www.osha.gov/ote

**First Aid/CPR**
- American Red Cross: www.redcross.org
- American Heart Association: www.heart.org

### 12.3 Glossary of Terms

**AC (Alternating Current):** Electrical current that reverses direction periodically

**Arc Flash:** Explosive release of energy from electrical equipment

**Category 3:** Safety system architecture with redundancy and fault detection (ISO 13849-1)

**CSP (Cyclic Synchronous Position):** EtherCAT control mode for position control

**DC (Direct Current):** Electrical current that flows in one direction

**DH Parameters (Denavit-Hartenberg):** Standard method for describing robot kinematics

**EtherCAT:** Industrial Ethernet protocol for real-time communication

**F/T Sensor:** Force/Torque sensor

**LOTO (Lockout/Tagout):** Safety procedure to prevent accidental energization

**ML (Machine Learning):** Artificial intelligence technique for learning from data

**NC (Normally Closed):** Contact that is closed when not activated

**NO (Normally Open):** Contact that is open when not activated

**PDO (Process Data Object):** EtherCAT data structure for real-time data exchange

**PLd (Performance Level d):** Safety performance level per ISO 13849-1

**PPE (Personal Protective Equipment):** Safety equipment worn by personnel

**PREEMPT_RT:** Real-time Linux kernel patch

**STO (Safe Torque Off):** Safety function that removes power to motor

**TensorRT:** NVIDIA library for optimizing neural networks

### 12.4 Acronyms

| Acronym | Full Term |
|---------|-----------|
| AC | Alternating Current |
| AI | Artificial Intelligence |
| AWG | American Wire Gauge |
| CAD | Computer-Aided Design |
| CAN | Controller Area Network |
| CMM | Coordinate Measuring Machine |
| CNC | Computer Numerical Control |
| CPU | Central Processing Unit |
| CSP | Cyclic Synchronous Position |
| DC | Direct Current |
| DH | Denavit-Hartenberg |
| EMI | Electromagnetic Interference |
| F/T | Force/Torque |
| FMEA | Failure Mode and Effects Analysis |
| GPU | Graphics Processing Unit |
| I/O | Input/Output |
| IEC | International Electrotechnical Commission |
| ISO | International Organization for Standardization |
| KRL | Kuka Robot Language |
| LED | Light-Emitting Diode |
| LOTO | Lockout/Tagout |
| ML | Machine Learning |
| NC | Normally Closed |
| NEC | National Electrical Code |
| NFPA | National Fire Protection Association |
| NO | Normally Open |
| NVMe | Non-Volatile Memory Express |
| OP | Operational (EtherCAT state) |
| OSHA | Occupational Safety and Health Administration |
| PDO | Process Data Object |
| PID | Proportional-Integral-Derivative |
| PLd | Performance Level d |
| PPE | Personal Protective Equipment |
| PREEMPT_RT | Preemptible Real-Time |
| RGB | Red-Green-Blue |
| ROS | Robot Operating System |
| RPM | Revolutions Per Minute |
| RS-422 | Recommended Standard 422 (differential signaling) |
| STO | Safe Torque Off |
| USB | Universal Serial Bus |
| VFD | Variable Frequency Drive |

### 12.5 Conversion Tables

#### 12.5.1 Electrical Units

| From | To | Multiply by |
|------|-----|-------------|
| Volts (V) | Millivolts (mV) | 1000 |
| Amps (A) | Milliamps (mA) | 1000 |
| Watts (W) | Kilowatts (kW) | 0.001 |
| Kilowatts (kW) | Horsepower (HP) | 1.341 |
| Horsepower (HP) | Kilowatts (kW) | 0.746 |

#### 12.5.2 Mechanical Units

| From | To | Multiply by |
|------|-----|-------------|
| Millimeters (mm) | Inches (in) | 0.03937 |
| Inches (in) | Millimeters (mm) | 25.4 |
| Meters (m) | Feet (ft) | 3.281 |
| Feet (ft) | Meters (m) | 0.3048 |
| Degrees (°) | Radians (rad) | 0.01745 |
| Radians (rad) | Degrees (°) | 57.296 |
| Newton-meters (Nm) | Foot-pounds (ft-lb) | 0.7376 |
| Foot-pounds (ft-lb) | Newton-meters (Nm) | 1.356 |

#### 12.5.3 Wire Gauge (AWG) Reference

| AWG | Diameter (mm) | Current Capacity (A) @ 60°C |
|-----|---------------|----------------------------|
| 10 | 2.588 | 30 |
| 12 | 2.053 | 20 |
| 14 | 1.628 | 15 |
| 16 | 1.291 | 10 |
| 18 | 1.024 | 7 |
| 20 | 0.812 | 5 |
| 22 | 0.644 | 3 |

### 12.6 Forms and Templates

#### 12.6.1 Pre-Task Safety Briefing

```
PRE-TASK SAFETY BRIEFING

Date: _______________ Time: _______________
Task: _______________________________________________

Personnel Present:
- _______________________________________________
- _______________________________________________
- _______________________________________________

Task Description:
___________________________________________________
___________________________________________________

Hazards Identified:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Control Measures:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Required PPE:
[ ] Arc-rated clothing
[ ] Voltage-rated gloves
[ ] Safety glasses
[ ] Hard hat
[ ] Hearing protection
[ ] Other: _______________

Emergency Procedures Reviewed:
[ ] Emergency stop locations
[ ] Fire extinguisher location
[ ] First aid kit location
[ ] Emergency contact numbers
[ ] Evacuation route

Questions/Concerns:
___________________________________________________
___________________________________________________

All personnel understand task and hazards:
Signature: _______________ Date: _______________
Signature: _______________ Date: _______________
Signature: _______________ Date: _______________

Supervisor Approval: _______________ Date: _______________
```

#### 12.6.2 Equipment Inspection Form

```
EQUIPMENT INSPECTION FORM

Date: _______________
Equipment: _______________________________________________
Serial Number: _______________
Inspector: _______________

Visual Inspection:
[ ] No visible damage
[ ] All fasteners tight
[ ] No corrosion
[ ] Labels legible
[ ] Guards in place
[ ] Cables not damaged

Electrical:
[ ] Connections tight
[ ] No exposed conductors
[ ] Grounding intact
[ ] No signs of overheating

Mechanical:
[ ] Smooth operation
[ ] No unusual sounds
[ ] No excessive vibration
[ ] Lubrication adequate

Safety Systems:
[ ] E-Stop buttons functional
[ ] Safety interlocks functional
[ ] Warning labels present

Issues Found:
___________________________________________________
___________________________________________________

Corrective Actions Required:
___________________________________________________
___________________________________________________

Equipment Status:
[ ] Approved for use
[ ] Requires maintenance
[ ] Out of service - DO NOT USE

Inspector Signature: _______________ Date: _______________
Supervisor Approval: _______________ Date: _______________
```

### 12.7 Quick Reference Guides

#### 12.7.1 Emergency Contact Numbers

```
EMERGENCY CONTACTS

EMERGENCY SERVICES:
Fire/Medical/Police: 911

FACILITY CONTACTS:
Facility Manager: _______________
Safety Officer: _______________
Maintenance: _______________
Security: _______________

PROJECT CONTACTS:
Project Manager: _______________
Electrical Lead: _______________
Mechanical Lead: _______________
Integration Lead: _______________

VENDOR SUPPORT:
Kuka Support: _______________
Drive Manufacturer: _______________
Jetson Support: _______________

UTILITIES:
Electric Company: _______________
Emergency Shutoff Location: _______________

POST THIS INFORMATION IN VISIBLE LOCATION
```

#### 12.7.2 Emergency Shutdown Procedure

```
EMERGENCY SHUTDOWN PROCEDURE

IN CASE OF EMERGENCY:

1. PRESS EMERGENCY STOP BUTTON (RED)
   - Located: [Specify locations]

2. OPEN MAIN CIRCUIT BREAKER
   - Located: [Specify location]
   - Turn to OFF position

3. CALL FOR HELP
   - Dial 911 for medical emergency
   - Notify supervisor: [Phone number]

4. RENDER AID (if trained)
   - Do not move injured person unless in immediate danger
   - Begin CPR if necessary
   - Control bleeding
   - Treat for shock

5. SECURE THE SCENE
   - Prevent others from entering
   - Do not disturb evidence
   - Wait for emergency services

DO NOT ATTEMPT TO RESTART SYSTEM
UNTIL AUTHORIZED BY SUPERVISOR

POST THIS INFORMATION IN VISIBLE LOCATION
```

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | December 14, 2025 | FileDocGenerator | Initial release |

---

## Document Approval

**Prepared by:**
Name: _______________
Title: _______________
Signature: _______________ Date: _______________

**Reviewed by:**
Name: _______________
Title: Safety Officer
Signature: _______________ Date: _______________

**Approved by:**
Name: _______________
Title: Project Manager
Signature: _______________ Date: _______________

---

**END OF HUMAN TASK DOCUMENTATION**

---

**IMPORTANT REMINDERS:**

1. **SAFETY FIRST** - 480V AC is extremely dangerous. Always follow safety procedures.

2. **NEVER WORK ALONE** on high-voltage systems.

3. **ALWAYS USE PROPER PPE** - Arc-rated clothing is mandatory for 480V work.

4. **FOLLOW LOTO PROCEDURES** - Lock out and verify de-energized before any work.

5. **TEST EMERGENCY STOPS** - Before every work session.

6. **DOCUMENT EVERYTHING** - Maintain detailed records of all work.

7. **WHEN IN DOUBT, STOP** - Consult supervisor or expert before proceeding.

8. **LICENSED ELECTRICIAN REQUIRED** - For all 480V power system work.

**Your safety and the safety of your team members is the top priority. No task is so important that it cannot be done safely.**
