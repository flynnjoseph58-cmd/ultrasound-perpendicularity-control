# Phase 1 Results — Open Loop Straight Line Path Following

**Status:** Complete ✅  
**Date:** [FILL IN DATE]  
**Hardware:** LoCoBot WidowX 250s, MSU Robotics Lab

---

## Objective

Validate that the arm can follow a straight line path along the y-axis at constant height with the probe pointing straight down throughout the entire motion.

---

## Test Configuration

| Parameter | Value |
|---|---|
| x position | 0.30 m (fixed) |
| z height | 0.25 m (fixed) |
| y range | -0.10 to +0.10 m |
| y step size | 0.05 m |
| pitch | 1.5708 rad (π/2) |
| moving_time | 3.0 s per step |

---

## Results

### Test 1 — Home Pose
- Arm successfully moved to home pose and returned to sleep pose
- No errors

### Test 2 — Y-Axis Straight Line
- Arm swept from y=-0.10 to y=+0.10 at constant height
- Motion smooth with no jerking
- Constant height maintained throughout

### Test 3 — Probe Pointing Down
- pitch=1.5708 successfully maintained probe pointing straight down
- Orientation held throughout full y-axis sweep
- Visually confirmed perpendicular to horizontal surface

### Test 4 — Z Relative Correction
- Confirmed set_ee_cartesian_trajectory(z=value) is relative not absolute
- Down 5cm then up 5cm returned to original height exactly

### Workspace Mapping
Full workspace probe at pitch=1.5708 confirmed all positions reachable:

| x (m) | z (m) | y_min (m) | y_max (m) | y_span (m) |
|---|---|---|---|---|
| 0.20 | 0.10–0.30 | -0.20 | +0.20 | 0.40 |
| 0.30 | 0.10–0.30 | -0.20 | +0.20 | 0.40 |
| 0.40 | 0.10–0.30 | -0.20 | +0.20 | 0.40 |

All tested positions reachable — workspace larger than required scan path.

---

## Key Findings

1. `InterbotixLocobotXS` requires `arm_model='wx250s'` to load arm interface
2. `pitch=math.pi/2` successfully points probe straight down
3. `set_ee_cartesian_trajectory()` z moves are relative — confirmed by up/down test
4. Full workspace ±0.20m in y is available at all tested x and z values
5. `forearm_roll` joint identified as key joint for future perpendicularity control

---

## Issues Encountered

| Issue | Resolution |
|---|---|
| `roll` parameter in `set_ee_pose_components` had no effect at pitch=π/2 | Gimbal lock singularity — use `forearm_roll` joint directly |
| `wrist_rotate` motor had hardware error (red LED) | Fixed by SDK reboot call |
| `load_configs:=true` caused EEPROM write failure | Fixed with `load_configs:=false` |

---

## Video

[FILL IN — YouTube unlisted link or note mp4 filename]

**What the video shows:**
- Arm initialising and moving to home pose
- Straight line sweep along y-axis at constant height
- Probe visibly pointing straight down throughout
- Return to sleep pose

---

## Next Steps

Proceed to Phase 2 — integrate HC-SR04 sensor for height feedback control.
