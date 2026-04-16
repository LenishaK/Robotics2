#region VEXcode Generated Robot Configuration
from vex import *
import math

brain = Brain()

brain_inertial = Inertial()

left_motor = Motor(Ports.PORT6)
right_motor = Motor(Ports.PORT10, True)
arm_motor = Motor(Ports.PORT3)
claw_motor = Motor(Ports.PORT4)

wait(100, MSEC)
#endregion VEXcode Generated Robot Configuration

# Sort plan
# pickup point > drop point
ITEMS_TO_SORT = [
    ("A", "1"),
    ("B", "2"),
    ("C", "3")
]

# Settings
DRIVE_SPEED = 22
TURN_SPEED_FAST = 16
TURN_SPEED_SLOW = 7
MICRO_CORRECT_SPEED = 6
ARM_SPEED = 28
CLAW_SPEED = 32

STEP_PAUSE = 0.40
TURN_PAUSE = 0.35
ACTION_PAUSE = 0.45

WHEEL_DIAMETER_MM = 60.0
DISTANCE_SCALE = 1.00

# Pickup points in front of home
PICKUP_DISTANCES_MM = {
    "A": 90,
    "B": 180,
    "C": 270
}

# New drop points around home
# 1 = 180 degrees behind home
# 2 = 90 degrees to one side
# 3 = 270 degrees to the other side
DROP_POINTS = {
    "1": {"heading_offset": 180, "distance_mm": 120},
    "2": {"heading_offset": 90,  "distance_mm": 120},
    "3": {"heading_offset": 270, "distance_mm": 120}
}

PICK_APPROACH_MM = 50
DROP_APPROACH_MM = 40

# Arm height settings
ARM_DEFAULT_TIME = 0.30
ARM_EXTRA_LIFT_TIME = 1.20

arm_height = "default"

# Starting heading
START_HEADING = 0.0

# Display and helpers
def show_status(text):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print(text)

def pause(t=STEP_PAUSE):
    wait(t, SECONDS)

def mm_to_deg(mm):
    return (mm * DISTANCE_SCALE) / (math.pi * WHEEL_DIAMETER_MM) * 360.0

def normalize_heading(angle):
    while angle >= 360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle

# Gyro functions
def calibrate():
    show_status("Calibrating gyro")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        wait(50, MSEC)
    pause()

def capture_start_heading():
    global START_HEADING
    START_HEADING = brain_inertial.heading(DEGREES)

def heading_error(target, current):
    error = target - current
    while error > 180:
        error -= 360
    while error < -180:
        error += 360
    return error

def turn_to_heading(target_heading):
    target_heading = normalize_heading(target_heading)
    error = heading_error(target_heading, brain_inertial.heading(DEGREES))

    while abs(error) > 20:
        if error > 0:
            left_motor.spin(FORWARD, TURN_SPEED_FAST, PERCENT)
            right_motor.spin(REVERSE, TURN_SPEED_FAST, PERCENT)
        else:
            left_motor.spin(REVERSE, TURN_SPEED_FAST, PERCENT)
            right_motor.spin(FORWARD, TURN_SPEED_FAST, PERCENT)
        error = heading_error(target_heading, brain_inertial.heading(DEGREES))

    while abs(error) > 2:
        if error > 0:
            left_motor.spin(FORWARD, TURN_SPEED_SLOW, PERCENT)
            right_motor.spin(REVERSE, TURN_SPEED_SLOW, PERCENT)
        else:
            left_motor.spin(REVERSE, TURN_SPEED_SLOW, PERCENT)
            right_motor.spin(FORWARD, TURN_SPEED_SLOW, PERCENT)
        error = heading_error(target_heading, brain_inertial.heading(DEGREES))

    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)
    pause(TURN_PAUSE)

def straighten_to_heading(target_heading):
    target_heading = normalize_heading(target_heading)
    error = heading_error(target_heading, brain_inertial.heading(DEGREES))

    if abs(error) <= 1.5:
        return

    while abs(error) > 1.5:
        if error > 0:
            left_motor.spin(FORWARD, MICRO_CORRECT_SPEED, PERCENT)
            right_motor.spin(REVERSE, MICRO_CORRECT_SPEED, PERCENT)
        else:
            left_motor.spin(REVERSE, MICRO_CORRECT_SPEED, PERCENT)
            right_motor.spin(FORWARD, MICRO_CORRECT_SPEED, PERCENT)

        error = heading_error(target_heading, brain_inertial.heading(DEGREES))

    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)
    pause(0.20)

def face_start_heading():
    turn_to_heading(START_HEADING)

def get_drop_heading(delivery):
    return normalize_heading(START_HEADING + DROP_POINTS[delivery]["heading_offset"])

# Drive functions
def drive_forward_mm(mm, correct_heading=None):
    deg = mm_to_deg(mm)
    left_motor.spin_for(FORWARD, deg, DEGREES, DRIVE_SPEED, PERCENT, False)
    right_motor.spin_for(FORWARD, deg, DEGREES, DRIVE_SPEED, PERCENT, True)
    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)
    pause()

    if correct_heading is not None:
        straighten_to_heading(correct_heading)

def drive_backward_mm(mm, correct_heading=None):
    deg = mm_to_deg(mm)
    left_motor.spin_for(REVERSE, deg, DEGREES, DRIVE_SPEED, PERCENT, False)
    right_motor.spin_for(REVERSE, deg, DEGREES, DRIVE_SPEED, PERCENT, True)
    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)
    pause()

    if correct_heading is not None:
        straighten_to_heading(correct_heading)

# Arm functions
def go_to_default_height():
    global arm_height
    if arm_height == "high":
        show_status("Arm default")
        arm_motor.spin(REVERSE, ARM_SPEED, PERCENT)
        wait(ARM_EXTRA_LIFT_TIME, SECONDS)
        arm_motor.stop(HOLD)
        arm_height = "default"
        pause(ACTION_PAUSE)

def go_to_high_height():
    global arm_height
    if arm_height == "default":
        show_status("Arm high")
        arm_motor.spin(FORWARD, ARM_SPEED, PERCENT)
        wait(ARM_EXTRA_LIFT_TIME, SECONDS)
        arm_motor.stop(HOLD)
        arm_height = "high"
        pause(ACTION_PAUSE)

def move_to_start_height():
    show_status("Arm start")
    arm_motor.spin(FORWARD, ARM_SPEED, PERCENT)
    wait(ARM_DEFAULT_TIME, SECONDS)
    arm_motor.stop(HOLD)
    pause(ACTION_PAUSE)

# Claw functions
def open_claw():
    show_status("Open claw")
    claw_motor.spin(REVERSE, CLAW_SPEED, PERCENT)
    wait(0.7, SECONDS)
    claw_motor.stop(HOLD)
    pause(ACTION_PAUSE)

def close_claw():
    show_status("Close claw")
    claw_motor.spin(FORWARD, CLAW_SPEED, PERCENT)
    wait(0.9, SECONDS)
    claw_motor.stop(HOLD)
    pause(ACTION_PAUSE)

# Pickup and drop functions
def pick_item():
    go_to_default_height()

    show_status("Approach item")
    drive_forward_mm(PICK_APPROACH_MM, START_HEADING)

    close_claw()

    show_status("Back from item")
    drive_backward_mm(PICK_APPROACH_MM, START_HEADING)

    go_to_high_height()

def release_item_without_lowering(drop_heading):
    show_status("Approach drop")
    drive_forward_mm(DROP_APPROACH_MM, drop_heading)

    open_claw()

    show_status("Back from drop")
    drive_backward_mm(DROP_APPROACH_MM, drop_heading)

# Sort cycle
def sort_item(pickup, delivery):
    drop_heading = get_drop_heading(delivery)
    drop_distance = DROP_POINTS[delivery]["distance_mm"]

    show_status("Next: " + pickup + "->" + delivery)
    pause(0.6)

    face_start_heading()
    go_to_default_height()
    open_claw()

    # Go to pickup
    show_status("To pickup " + pickup)
    drive_forward_mm(PICKUP_DISTANCES_MM[pickup], START_HEADING)

    pick_item()

    # Return home
    show_status("Home from " + pickup)
    drive_backward_mm(PICKUP_DISTANCES_MM[pickup], START_HEADING)

    # Turn to drop direction
    show_status("Face drop " + delivery)
    turn_to_heading(drop_heading)

    # Go to drop point
    show_status("To drop " + delivery)
    drive_forward_mm(drop_distance, drop_heading)

    release_item_without_lowering(drop_heading)

    # Return home from drop point
    show_status("Home from " + delivery)
    drive_backward_mm(drop_distance, drop_heading)

    # Face front again
    show_status("Face home")
    face_start_heading()

    go_to_default_height()

# Main
def main():
    calibrate()

    move_to_start_height()
    capture_start_heading()

    for pickup, delivery in ITEMS_TO_SORT:
        sort_item(pickup, delivery)
        pause(0.8)

    show_status("Finished")
    left_motor.stop(BRAKE)
    right_motor.stop(BRAKE)
    arm_motor.stop(HOLD)
    claw_motor.stop(HOLD)

main()
