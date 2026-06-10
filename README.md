# Ultrasound Perpendicularity Control

**MS Research Project — Flynn Antony Joseph  
**Supervisor: Sunil Kishore Chakrapani
---

## Project Overview

This project develops an autonomous robotic arm control system that maintains constant standoff distance and probe perpendicularity above a surface using only air-coupled ultrasonic feedback — no contact, no coupling medium, no prior surface knowledge, and no structured light.

The core novelty is the use of echo amplitude maximum and echo width minimum as simultaneous indicators of perpendicular alignment. This dual-signal approach has been confirmed novel by the supervising professor.

**Scope:** Smooth surfaces only. Flat surfaces primary target. Smooth curved surfaces as stretch goal.

---

## Hardware

| Component | Details |
|---|---|
| Robot | LoCoBot with WidowX 250s 6DOF arm |
| Robot model string | locobot_wx250s |
| ROS version | Noetic |
| OS | Ubuntu 20.04 |
| Sensor (Phase 2) | HC-SR04 ultrasonic distance sensor |
| Sensor (Phase 4+) | 60kHz air-coupled ultrasonic transducer (pending order) |
| Microcontroller | Arduino Uno |
| Camera | Intel RealSense D435 |
| SDK | Interbotix Python SDK |

---

## Project Phases

| Phase | Description | Status |
|---|---|---|
| 1 | Open loop straight line path following | ✅ Complete |
| 2 | HC-SR04 closed loop height control | 🔄 In Progress |
| 3 | Robustness test — surface height change mid-scan | ⏳ Pending |
| 4 | 60kHz transducer signal characterisation | ⏳ Pending |
| 5 | Perpendicularity control | ⏳ Pending |
| 6 | Combined height and perpendicularity on flat surface | ⏳ Pending |
| 7 | Curved surface demonstration | ⏳ Stretch Goal |

---

## Key Parameters

```
Robot model     : locobot_wx250s
Arm             : WidowX 250 6DOF
Pitch down      : 1.5708 rad (π/2)
Target standoff : 20 cm
Path length     : 20 cm along y-axis
Safe x range    : 0.20 – 0.40 m
Safe y range    : -0.20 – +0.20 m
Safe z range    : 0.10 – 0.30 m
Serial port ARM : /dev/ttyUSB0
Serial port MCU : /dev/ttyACM0
Arduino baud    : 9600
Dynamixel baud  : 1000000
```

---

## Setup

### 1. ROS Network Configuration
```bash
export ROS_IP=35.12.212.57
export ROS_MASTER_URI=http://35.12.212.57:11311
```

### 2. Launch Robot
```bash
roslaunch interbotix_xslocobot_control xslocobot_control.launch \
  robot_model:=locobot_wx250s \
  use_base:=false \
  use_lidar:=false \
  use_camera:=false \
  load_configs:=false
```

### 3. Run Scripts
```bash
# Phase 1 — straight line path
python3 src/phase1_straight_line.py

# Phase 2 — height control
python3 src/phase2_height_control.py
```

---

## Repository Structure

```
ultrasound-perpendicularity-control/
├── README.md               — this file
├── weekly_log.md           — weekly progress log
├── src/
│   ├── phase1_straight_line.py     — open loop path following
│   ├── phase2_height_control.py    — HC-SR04 height control loop
│   └── arduino/
│       └── hcsr04_tof_distance.ino — Arduino sketch (TOF + distance)
├── results/
│   ├── phase1/
│   │   ├── phase1_notes.md         — observations and findings
│   │   └── phase1_run1.mp4         — video (or YouTube link)
│   └── phase2/
│       ├── phase2_notes.md         — observations and findings
│       └── phase2_run1.mp4         — video (or YouTube link)
├── docs/
│   └── system_architecture.md      — full system design document
└── hardware/
    └── fixture_design.md           — sensor mounting notes
```

---

## Known Hardware Issues

- `load_configs` must be `false` after initial robot setup
- `wrist_rotate` motor required reboot on first session — fixed via SDK reboot call
- Power fault identified June 9th — technician inspection scheduled

---

## Dependencies

```
pyserial
dynamixel_sdk
numpy
```
