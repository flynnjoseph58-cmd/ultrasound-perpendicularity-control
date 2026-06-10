#!/usr/bin/env python3
"""
Phase 1 — Open Loop Straight Line Path Following
=================================================
Moves the LoCoBot WidowX 250s arm along the y-axis at constant height
with the probe pointing straight down (pitch=pi/2) throughout.

Confirmed working on physical hardware at MSU Robotics Lab.

Robot  : locobot_wx250s
SDK    : Interbotix Python SDK
ROS    : Noetic
"""

from interbotix_xs_modules.locobot import InterbotixLocobotXS
import time
import math

# ── CONFIG ───────────────────────────────────────────────────────────────────
PITCH_DOWN  = math.pi / 2   # 1.5708 rad — probe pointing straight down
X_POS       = 0.30           # fixed x position (m)
Z_HEIGHT    = 0.25           # fixed height (m)
MOVE_TIME   = 3.0            # seconds per move — slow for safety
Y_START     = -0.10          # start of scan path (m)
Y_END       =  0.10          # end of scan path (m)
Y_STEP      =  0.05          # step size (m)
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("PHASE 1 — STRAIGHT LINE PATH FOLLOWING")
    print(f"Path   : y = {Y_START} to {Y_END} in {Y_STEP}m steps")
    print(f"Height : z = {Z_HEIGHT}m (constant)")
    print(f"Pitch  : {PITCH_DOWN:.4f} rad (straight down)")
    print("=" * 55)

    bot = InterbotixLocobotXS(robot_model='locobot_wx250s', arm_model='wx250s')

    # Step 1 — go to home pose
    print("\n[1] Going to home pose...")
    bot.arm.go_to_home_pose(moving_time=MOVE_TIME)
    time.sleep(1)

    # Step 2 — move to start position with probe pointing down
    print(f"[2] Moving to start position (x={X_POS}, y={Y_START}, z={Z_HEIGHT})...")
    bot.arm.set_ee_pose_components(
        x=X_POS,
        y=Y_START,
        z=Z_HEIGHT,
        pitch=PITCH_DOWN,
        moving_time=MOVE_TIME
    )
    time.sleep(2)

    # Step 3 — sweep along y-axis
    print(f"\n[3] Starting y-axis sweep...")
    current_y = Y_START
    waypoints = []
    y = Y_START
    while y <= Y_END + 0.001:
        waypoints.append(round(y, 4))
        y += Y_STEP

    for i, target_y in enumerate(waypoints):
        dy = target_y - current_y
        if abs(dy) > 0.001:
            print(f"  Waypoint {i+1}/{len(waypoints)} | y={target_y:+.3f}m")
            bot.arm.set_ee_cartesian_trajectory(
                y=dy,
                moving_time=MOVE_TIME
            )
            time.sleep(MOVE_TIME + 0.5)
        current_y = target_y

    print("\n[4] Path complete — returning to sleep pose...")
    bot.arm.go_to_sleep_pose(moving_time=MOVE_TIME)
    print("Done.")

if __name__ == '__main__':
    main()
