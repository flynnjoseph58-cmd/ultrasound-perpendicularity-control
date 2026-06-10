# Phase 2 Results — HC-SR04 Height Control

**Status:** In Progress 🔄  
**Date:** [FILL IN DATE]  
**Hardware:** LoCoBot WidowX 250s + HC-SR04 + Arduino Uno

---

## Objective

Implement closed loop height control — arm maintains constant standoff distance above a surface using HC-SR04 distance sensor feedback.

---

## Test Configuration

| Parameter | Value |
|---|---|
| Target standoff distance | 20.0 cm |
| Trigger threshold | 1.5 cm |
| Confirm threshold | 0.8 cm over 5 samples |
| x position | 0.30 m |
| y range | -0.10 to +0.10 m |
| y step size | 0.01 m |
| pitch | 1.5708 rad (locked) |
| Serial port | /dev/ttyACM0 |
| Baud rate | 9600 |

---

## Sensor Validation

HC-SR04 serial output confirmed stable before arm integration:
```
[1] 6.75 cm
[2] 6.78 cm
[3] 6.78 cm
[4] 6.77 cm
[5] 6.78 cm
```
Readings stable within ±0.03 cm on static surface.

---

## Attempt 1 — Initial Test

**Result:** Unstable

**Three issues identified:**

### Issue 1 — Sensor Not Rigidly Mounted
Sensor was hand-held during initial test. Small hand movements caused constant false corrections — arm was correcting for hand movement rather than surface height changes.

**Fix:** Mount sensor rigidly to gripper before further testing.

### Issue 2 — Pitch Drift During Corrections
When only z was commanded via `set_ee_cartesian_trajectory(z=value)`, the wrist joints shifted and probe orientation drifted from pointing straight down.

**Fix:** Use full pose command `set_ee_pose_components(x, y, z, pitch=1.5708)` for every correction rather than relative z moves. This recruits all DOF to maintain pitch explicitly.

### Issue 3 — Motor Vibration Corrupting Readings
Continuous sensor readings while arm was moving returned corrupted values due to vibration from Dynamixel motors affecting sensor readings.

**Fix:** Two-mode architecture — scanning mode where arm moves with pitch locked and no corrections, correction mode where arm stops completely before reading sensor and applying correction.

---

## Improved Architecture — Written, Not Yet Tested

```
SCANNING MODE
  arm moves along y with pitch=1.5708 locked
  reads sensor after each 1cm step
  if error > 1.5cm → switch to CORRECTION MODE

CORRECTION MODE
  arm stops completely
  take 5 confirmation readings
  if confirmed error > 0.8cm → apply full pose correction
  restore pitch=1.5708 explicitly
  switch back to SCANNING MODE
```

---

## Hardware Fault — June 9th

All Dynamixel motors lost power during testing session due to power connector issue. Technician inspection scheduled. Arm unavailable until resolved.

**Diagnosis:**
- Direct SDK ping at all baudrates returned no response on all 11 motor IDs
- Camera and computer unaffected (separate power circuit)
- U2D2 detected on /dev/ttyUSB0 — data chain intact
- Suspected cause: spark on 20V power connector during removal

---

## Video

[FILL IN — YouTube unlisted link or note mp4 filename once recorded]

**What the video will show:**
- Live sensor readings responding to hand movement
- Arm moving along y-axis
- Height correction triggering when surface changes

---

## Next Steps

1. Resolve hardware power fault (technician June 9th)
2. Mount HC-SR04 rigidly to gripper
3. Test improved two-mode architecture on hardware
4. Run Phase 3 — robustness test with surface height change mid-scan
