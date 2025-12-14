# Electrical Interface Specification: Kuka Legacy to ML Controller

## Document Purpose
This document specifies the electrical interfaces between the legacy Kuka CNC system components and the new Jetson-based ML controller, ensuring compatibility and safe integration.

---

## 1. Motor Interface Mapping

### 1.1 Motor Power Connections

| Legacy System | New System | Interface Type | Specification |
|--------------|------------|----------------|---------------|
| Kuka Motor 1 Power | Servo Drive 1 Motor Out | 3-Phase Power | 48VDC, 10A continuous, Phoenix Contact MSTB 2.5/3-ST |
| Kuka Motor 2 Power | Servo Drive 2 Motor Out | 3-Phase Power | 48VDC, 10A continuous, Phoenix Contact MSTB 2.5/3-ST |
| Kuka Motor 3 Power | Servo Drive 3 Motor Out | 3-Phase Power | 48VDC, 8A continuous, Phoenix Contact MSTB 2.5/3-ST |
| Kuka Motor 4 Power | Servo Drive 4 Motor Out | 3-Phase Power | 48VDC, 6A continuous, Phoenix Contact MSTB 2.5/3-ST |
| Kuka Motor 5 Power | Servo Drive 5 Motor Out | 3-Phase Power | 48VDC, 6A continuous, Phoenix Contact MSTB 2.5/3-ST |
| Kuka Turning Bed Motor | Servo Drive 6 Motor Out | 3-Phase Power | 48VDC, 15A continuous, Phoenix Contact MSTB 2.5/4-ST |

**Notes:**
- All motor power cables are shielded, 16 AWG minimum
- Shield connected to earth ground at drive end only
- Maximum cable length: 10 meters
- Use ferrules on all wire terminations

### 1.2 Encoder Interface Connections

| Motor Axis | Encoder Type | Connector | Pin Assignment | Signal Type |
|------------|--------------|-----------|----------------|-------------|
| Axis 1 | Absolute, 23-bit | D-Sub 15 Male | See Pinout Table 1.2.1 | Differential RS-422 |
| Axis 2 | Absolute, 23-bit | D-Sub 15 Male | See Pinout Table 1.2.1 | Differential RS-422 |
| Axis 3 | Absolute, 23-bit | D-Sub 15 Male | See Pinout Table 1.2.1 | Differential RS-422 |
| Axis 4 | Absolute, 23-bit | D-Sub 15 Male | See Pinout Table 1.2.1 | Differential RS-422 |
| Axis 5 | Absolute, 23-bit | D-Sub 15 Male | See Pinout Table 1.2.1 | Differential RS-422 |
| Turning Bed | Absolute, 23-bit | D-Sub 15 Male | See Pinout Table 1.2.1 | Differential RS-422 |

#### Table 1.2.1: Encoder D-Sub 15 Pinout

```
Pin | Signal Name    | Direction | Description
----|----------------|-----------|---------------------------
1   | A+             | Output    | Channel A positive
2   | A-             | Output    | Channel A negative
3   | B+             | Output    | Channel B positive
4   | B-             | Output    | Channel B negative
5   | Z+             | Output    | Index/Zero positive
6   | Z-             | Output    | Index/Zero negative
7   | U+             | Output    | Commutation U positive
8   | U-             | Output    | Commutation U negative
9   | V+             | Output    | Commutation V positive
10  | V-             | Output    | Commutation V negative
11  | W+             | Output    | Commutation W positive
12  | W-             | Output    | Commutation W negative
13  | +5V            | Power     | Encoder supply positive
14  | GND            | Power     | Encoder supply ground
15  | SHIELD         | Shield    | Cable shield connection
```

**Electrical Specifications:**
- Signal voltage: 5V differential (RS-422)
- Maximum frequency: 1 MHz
- Cable: Shielded twisted pair, max 30m
- Termination: 120Ω across differential pairs at receiver

---

## 2. EtherCAT Network Interface

### 2.1 Network Topology

```
Jetson Orin               Drive 1              Drive 2              Drive 3
  Nano Super               (Axis 1)             (Axis 2)             (Axis 3)
     |                        |                    |                    |
[ETH0]---RJ45---[IN]----[OUT]----RJ45----[IN]----[OUT]----RJ45----[IN]----[OUT]
                                                                            |
                                                                        RJ45
                                                                            |
                                                                            |
        Drive 6                 Drive 5              Drive 4              |
       (Turn Bed)               (Axis 5)             (Axis 4)             |
           |                        |                    |                |
      [IN]----[OUT]----RJ45----[IN]----[OUT]----RJ45----[IN]----[OUT]----+
           
           
[I/O Module]
     |
[IN]----+
```

**Configuration:**
- Protocol: EtherCAT (IEC 61158)
- Cycle time: 1 ms (1 kHz)
- Cable: CAT5e or CAT6, shielded
- Connector: RJ45
- Maximum segment length: 100m
- Total network length: <400m

### 2.2 EtherCAT Device Addressing

| Device | Type | Address | PDO Size (bytes) | Watchdog (ms) |
|--------|------|---------|------------------|---------------|
| Drive 1 (Axis 1) | Servo Drive | 1001 | Input: 16, Output: 16 | 100 |
| Drive 2 (Axis 2) | Servo Drive | 1002 | Input: 16, Output: 16 | 100 |
| Drive 3 (Axis 3) | Servo Drive | 1003 | Input: 16, Output: 16 | 100 |
| Drive 4 (Axis 4) | Servo Drive | 1004 | Input: 16, Output: 16 | 100 |
| Drive 5 (Axis 5) | Servo Drive | 1005 | Input: 16, Output: 16 | 100 |
| Drive 6 (Turn Bed) | Servo Drive | 1006 | Input: 16, Output: 16 | 100 |
| I/O Module | Digital/Analog I/O | 2001 | Input: 32, Output: 32 | 200 |

### 2.3 Process Data Objects (PDO) Mapping

**Servo Drive Output PDO (Master → Drive):**
```
Byte 0-1:   Control Word (0x6040)
Byte 2-5:   Target Position (0x607A)
Byte 6-9:   Target Velocity (0x60FF)
Byte 10-11: Target Torque (0x6071)
Byte 12-15: User-defined (reserved)
```

**Servo Drive Input PDO (Drive → Master):**
```
Byte 0-1:   Status Word (0x6041)
Byte 2-5:   Actual Position (0x6064)
Byte 6-9:   Actual Velocity (0x606C)
Byte 10-11: Actual Torque (0x6077)
Byte 12-15: Following Error (0x60F4)
```

---

## 3. Digital I/O Interface

### 3.1 Safety Inputs (Critical - Hardware Interlocked)

| Signal Name | Source | Connector | Pin | Logic Level | Response Time |
|-------------|--------|-----------|-----|-------------|---------------|
| E-Stop Button 1 | Main Panel | TB1 | 1-2 | 24VDC, NO | <10ms |
| E-Stop Button 2 | Pendant | TB1 | 3-4 | 24VDC, NO | <10ms |
| Door Interlock 1 | Front Door | TB1 | 5-6 | 24VDC, NC | <50ms |
| Door Interlock 2 | Side Door | TB1 | 7-8 | 24VDC, NC | <50ms |
| Light Curtain | Perimeter | TB1 | 9-10 | 24VDC, OSSD | <20ms |

**Connection Diagram:**
```
+24V ----[E-Stop 1 NO]----[E-Stop 2 NO]----[Door 1 NC]----[Door 2 NC]----+
                                                                          |
                                                                    [Safety Relay 1]
                                                                          |
                                                                    [Safety Relay 2]
                                                                          |
                                                                    [Watchdog OK] ---+
                                                                                     |
                                                                         +-----------+
                                                                         |
                                                              [Safe Torque Off (STO)]
                                                                         |
                                                              +----------+---------+
                                                              |          |         |
                                                           Drive 1   Drive 2   ...Drive 6
```

### 3.2 Standard Digital Inputs

| Signal Name | Function | Connector | Pin | Logic Level | Debounce |
|-------------|----------|-----------|-----|-------------|----------|
| Axis 1 Limit+ | Positive Limit | TB2 | 1 | 24VDC | 10ms |
| Axis 1 Limit- | Negative Limit | TB2 | 2 | 24VDC | 10ms |
| Axis 2 Limit+ | Positive Limit | TB2 | 3 | 24VDC | 10ms |
| Axis 2 Limit- | Negative Limit | TB2 | 4 | 24VDC | 10ms |
| Axis 3 Limit+ | Positive Limit | TB2 | 5 | 24VDC | 10ms |
| Axis 3 Limit- | Negative Limit | TB2 | 6 | 24VDC | 10ms |
| Axis 4 Limit+ | Positive Limit | TB2 | 7 | 24VDC | 10ms |
| Axis 4 Limit- | Negative Limit | TB2 | 8 | 24VDC | 10ms |
| Axis 5 Limit+ | Positive Limit | TB2 | 9 | 24VDC | 10ms |
| Axis 5 Limit- | Negative Limit | TB2 | 10 | 24VDC | 10ms |
| Home Switch 1 | Axis 1 Home | TB2 | 11 | 24VDC | 10ms |
| Home Switch 2 | Axis 2 Home | TB2 | 12 | 24VDC | 10ms |
| Proximity Sensor | Tool Detection | TB2 | 13 | 24VDC | 5ms |

**Interface Circuit:**
```
+24V ----[1kΩ]----+----[Digital Input]----[Optocoupler]----[GPIO Pin]
                  |
              [Switch/Sensor]
                  |
                 GND
```

### 3.3 Digital Outputs

| Signal Name | Function | Connector | Pin | Output Type | Max Current |
|-------------|----------|-----------|-----|-------------|-------------|
| Drive Enable | Master Enable | TB3 | 1 | 24VDC, Source | 500mA |
| Brake Release 1 | Axis 1 Brake | TB3 | 2 | 24VDC, Source | 1A |
| Brake Release 2 | Axis 2 Brake | TB3 | 3 | 24VDC, Source | 1A |
| Brake Release 3 | Axis 3 Brake | TB3 | 4 | 24VDC, Source | 1A |
| Coolant Pump | Coolant On/Off | TB3 | 5 | 24VDC, Relay | 2A |
| Spindle Enable | Spindle Enable | TB3 | 6 | 24VDC, Source | 500mA |
| Work Light | LED Work Light | TB3 | 7 | 24VDC, Source | 1A |

**Output Driver Circuit:**
```
[GPIO Pin]----[Transistor/MOSFET]----[Output Terminal]----[Load]----+24V
                      |
                     GND
                     
Protection: Flyback diode across inductive loads
```

---

## 4. Analog I/O Interface

### 4.1 Analog Inputs (via EtherCAT I/O Module)

| Signal Name | Source | Range | Resolution | Update Rate | Connector |
|-------------|--------|-------|------------|-------------|-----------|
| Force X | Force/Torque Sensor | ±10V | 16-bit | 1kHz | TB4-1,2 |
| Force Y | Force/Torque Sensor | ±10V | 16-bit | 1kHz | TB4-3,4 |
| Force Z | Force/Torque Sensor | ±10V | 16-bit | 1kHz | TB4-5,6 |
| Torque X | Force/Torque Sensor | ±10V | 16-bit | 1kHz | TB4-7,8 |
| Torque Y | Force/Torque Sensor | ±10V | 16-bit | 1kHz | TB4-9,10 |
| Torque Z | Force/Torque Sensor | ±10V | 16-bit | 1kHz | TB4-11,12 |
| Temp Motor 1 | Thermistor | 0-10V | 12-bit | 100Hz | TB4-13,14 |
| Temp Motor 2 | Thermistor | 0-10V | 12-bit | 100Hz | TB4-15,16 |
| Spindle Current | Current Sensor | 0-10V | 12-bit | 1kHz | TB4-17,18 |

**Force/Torque Sensor Specifications:**
- Sensor: ATI Mini40 or equivalent
- Output: ±10V corresponds to ±40N force, ±2Nm torque
- Excitation: 24VDC provided by I/O module
- Calibration matrix required

### 4.2 Analog Outputs (via EtherCAT I/O Module)

| Signal Name | Destination | Range | Resolution | Update Rate | Connector |
|-------------|-------------|-------|------------|-------------|-----------|
| Spindle Speed | VFD Speed Input | 0-10V | 12-bit | 100Hz | TB5-1,2 |
| Spindle Torque | VFD Torque Limit | 0-10V | 12-bit | 100Hz | TB5-3,4 |

**Spindle Control Specifications:**
- 0V = 0 RPM
- 10V = 24,000 RPM
- Linearity: ±1%
- Update rate: 100Hz sufficient for speed control

---

## 5. Power Supply Specifications

### 5.1 Main DC Bus (Motor Power)

```
AC Input → Rectifier/PFC → 48VDC ± 5% → Motor Drives
230VAC      Power Supply    20A max
50/60Hz
```

**Specifications:**
- Model: Mean Well RSP-1000-48 or equivalent
- Output: 48VDC, 21A continuous (1000W)
- Efficiency: >90%
- Features: Active PFC, over-current, over-voltage, over-temperature protection
- Connector: Phoenix Contact MSTB 2.5/2-ST for output

**Distribution:**
```
48VDC Bus ----[10A Fuse]---- Drive 1
          ----[10A Fuse]---- Drive 2
          ----[8A Fuse]---- Drive 3
          ----[6A Fuse]---- Drive 4
          ----[6A Fuse]---- Drive 5
          ----[15A Fuse]---- Drive 6
          ----[5A Fuse]---- Spindle VFD
```

### 5.2 Control Power (24VDC)

```
AC Input → Switching PSU → 24VDC ± 2% → Control Circuits
230VAC      Power Supply    5A max
```

**Specifications:**
- Model: Mean Well HDR-100-24 or equivalent
- Output: 24VDC, 4.2A continuous (100W)
- DIN rail mount
- Features: Over-current, short circuit protection
- Connector: Terminal blocks

**Distribution:**
```
24VDC ----[1A Fuse]---- GPIO Expander & I/O
      ----[2A Fuse]---- Safety Relays & Watchdog
      ----[1A Fuse]---- Brake Release Circuits
      ----[0.5A Fuse]---- Indicators & Misc
```

### 5.3 Jetson Power (5VDC, 3.3VDC)

```
24VDC → DC-DC Converter → 5VDC ± 5% → Jetson Orin Nano Super
                           4A max
```

**Specifications:**
- Model: RECOM R-78E5.0-1.0 or equivalent
- Input: 9-36VDC (24VDC nominal)
- Output: 5VDC, 1A (for Jetson + peripherals)
- Efficiency: >90%
- Protection: Thermal shutdown, over-current

**Jetson Power Budget:**
- Jetson module: 15W typical, 25W max
- USB peripherals: 5W
- GPIO expander: 0.5W
- **Total: ~5VDC @ 5A recommended**

---

## 6. Grounding & Shielding

### 6.1 Grounding Architecture

```
                    Earth Ground (PE)
                           |
        +------------------+-----------------+
        |                  |                 |
   Motor Drives      Control Panel    Jetson Enclosure
        |                  |                 |
    Motor Frames     Safety Relays      Chassis Ground
        |                  |                 |
    Shield Grounds   Signal Ground      Signal Ground
```

**Grounding Rules:**
1. Single point ground for signal circuits
2. Motor frames bonded to earth ground
3. Cable shields grounded at drive end only
4. Separate power ground from signal ground
5. Use star grounding topology

### 6.2 Cable Shielding

**Motor Cables:**
- Type: Shielded, twisted pair (3-conductor)
- Shield: Tinned copper braid, 90% coverage
- Connection: Shield to drive chassis at drive end via 360° clamp
- Leave shield floating at motor end

**Encoder Cables:**
- Type: Shielded, twisted pair for each differential signal
- Shield: Overall foil + drain wire
- Connection: Shield to D-Sub connector shell, bonded to drive
- Maximum length: 30m

**EtherCAT Cables:**
- Type: CAT6 S/FTP (shielded, foiled twisted pair)
- Connection: Shield bonded to RJ45 connector shell on both ends
- Avoid running parallel to motor power cables

---

## 7. EMC & Noise Mitigation

### 7.1 Filtering

**Motor Drive AC Input:**
- Install EMI filter on AC mains input
- Filter type: Single-phase, 10A minimum
- Attenuation: >40dB at 150kHz-30MHz

**Control Power:**
- Ferrite beads on 24VDC lines near sensitive devices
- Common-mode choke on EtherCAT cable at Jetson end

### 7.2 Layout Recommendations

1. **Separation:**
   - Keep motor power cables >50mm from signal cables
   - Cross at 90° if cables must intersect
   
2. **Cable Routing:**
   - Use metal cable ducts where possible
   - Segregate power and signal cables
   - Minimize loop areas

3. **PCB Layout:**
   - Separate analog and digital grounds
   - Use ground plane
   - Route high-speed signals with controlled impedance

---

## 8. Connector Specifications

### 8.1 Motor Power Connectors

**Type:** Phoenix Contact MSTB 2.5/3-ST
- Pitch: 5.08mm
- Wire range: 22-12 AWG
- Current rating: 12A per contact
- Voltage rating: 320V
- Mounting: Screw terminal block, DIN rail

### 8.2 Encoder Connectors

**Type:** D-Sub 15-pin male (DE-15)
- Shell: Metal, EMI shielding
- Contacts: Gold-plated
- Cable: Soldered or crimped
- Hood: Metal with cable strain relief
- Mounting: Panel mount with 4-40 screws

### 8.3 EtherCAT Connectors

**Type:** RJ45 shielded (Cat6)
- Contacts: 8P8C, gold-plated
- Cable: Cat6 S/FTP
- Connector shell: Metal for EMI shielding
- Mounting: Standard RJ45 socket

### 8.4 I/O Terminal Blocks

**Type:** Phoenix Contact MSTB 2.5/2-ST (2-position)
- Pitch: 5.08mm
- Wire range: 22-12 AWG
- Current rating: 12A per contact
- Voltage rating: 320V
- Color coding: Orange for safety, gray for standard

---

## 9. Interface Board Design

### 9.1 Recommended Interface Board

**Purpose:** Adapt Jetson Orin Nano Super to industrial control signals

**Features:**
- EtherCAT master interface (Ethernet → EtherCAT)
- GPIO expander (MCP23017) for additional I/O
- Optoisolated digital inputs (24VDC)
- Relay/MOSFET outputs (24VDC, 2A)
- 24V → 5V power regulation
- Watchdog timer (MAX6369)
- Status LEDs

**Block Diagram:**
```
Jetson GPIO ----[Level Shifter]----[Optocoupler Array]----[DI Terminal Blocks]
                                                               (24VDC Inputs)

Jetson GPIO ----[I2C]----[MCP23017 GPIO Expander]----[MOSFET Drivers]----[DO Terminal Blocks]
                                                                              (24VDC Outputs)

Jetson ETH ----[RJ45]----[EtherCAT Master IC]----[RJ45]----[EtherCAT Network]
                          (Optional: Beckhoff CX51xx)

24VDC Input ----[Fuse]----[DC-DC Converter]----[5VDC]----[Jetson Power]
                                                           [Logic Power]

Jetson GPIO ----[Watchdog IC]----[Safety Relay Driver]
     |                                    |
     +----[Heartbeat]            [24VDC to Safety System]
```

### 9.2 PCB Stackup

**4-Layer PCB:**
- Layer 1: Signal/Component (Top)
- Layer 2: Ground Plane
- Layer 3: Power Plane (5V, 3.3V, 24V)
- Layer 4: Signal/Component (Bottom)

**Specifications:**
- Board size: 100mm x 150mm
- Thickness: 1.6mm
- Copper weight: 1oz (35μm)
- Silkscreen: Both sides
- Solder mask: Green

---

## 10. Testing & Validation

### 10.1 Continuity Tests

Before power-on:
- [ ] Verify all motor power connections
- [ ] Verify encoder connections and pinouts
- [ ] Verify ground continuity
- [ ] Verify shield connections
- [ ] Check for shorts between phases
- [ ] Check for shorts to ground

### 10.2 Power-On Tests

With drives disconnected:
- [ ] Measure 48VDC bus voltage (47-50VDC acceptable)
- [ ] Measure 24VDC control voltage (23-25VDC acceptable)
- [ ] Measure 5VDC Jetson power (4.75-5.25VDC acceptable)
- [ ] Verify safety relay operation
- [ ] Test emergency stop function
- [ ] Test watchdog timer

### 10.3 Signal Tests

With oscilloscope:
- [ ] Verify EtherCAT signal integrity
- [ ] Verify encoder differential signals (±5V)
- [ ] Measure noise on analog inputs (<10mV RMS)
- [ ] Verify digital I/O switching levels

### 10.4 Functional Tests

- [ ] Test single motor operation
- [ ] Test encoder feedback
- [ ] Test force/torque sensor reading
- [ ] Test analog outputs (spindle control)
- [ ] Test all digital I/O
- [ ] Verify EtherCAT communication (no errors)

---

## 11. Safety Certification Notes

### Required Compliance
- **ISO 13849-1:** Safety of machinery - Safety-related parts of control systems
  - Target: Category 3, Performance Level d (PLd)
  - Requires redundant safety circuits
  - Requires diagnostic coverage

- **IEC 61800-5-2:** Safety functions in adjustable speed electrical power drive systems
  - STO (Safe Torque Off) implemented in drives
  - Hardware-based implementation

### Documentation Required
- [ ] Risk assessment per ISO 12100
- [ ] Circuit diagrams showing safety functions
- [ ] Failure mode analysis (FMEA)
- [ ] Validation test reports
- [ ] Declaration of conformity

---

## 12. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-12-14 | ML Controller Team | Initial specification |

---

## 13. Appendix: Bill of Materials

### Critical Components

| Item | Part Number | Manufacturer | Qty | Unit Cost | Notes |
|------|-------------|--------------|-----|-----------|-------|
| Jetson Orin Nano Super | 945-13767-0000-000 | NVIDIA | 1 | $500 | Main controller |
| Servo Drive | AKD-P00306 | Kollmorgen | 6 | $800 | EtherCAT, 48V, 3A |
| Power Supply 48V | RSP-1000-48 | Mean Well | 1 | $120 | 1000W |
| Power Supply 24V | HDR-100-24 | Mean Well | 1 | $45 | 100W, DIN rail |
| Safety Relay | PNOZ s3 | Pilz | 2 | $250 | Category 3 |
| GPIO Expander | MCP23017 | Microchip | 1 | $1.50 | I2C, 16-bit |
| Watchdog Timer | MAX6369 | Maxim | 1 | $3 | Voltage monitor |
| EtherCAT I/O | EL3104 | Beckhoff | 1 | $150 | 4-ch analog input |
| Force/Torque Sensor | Mini40 | ATI | 1 | $2000 | 6-axis, ±40N |
| Terminal Blocks | MSTB 2.5 | Phoenix Contact | 50 | $2 | Various configs |
| Connectors D-Sub15 | DE-15P | Amphenol | 6 | $8 | Metal shell |
| RJ45 Connectors | Cat6 shielded | Various | 10 | $5 | Industrial grade |

**Estimated Total Hardware Cost: $8,000 - $12,000**

---

## Document Approval

**Prepared by:** ML Controller Engineering Team  
**Reviewed by:** ___________________  Date: __________  
**Approved by:** ___________________  Date: __________
