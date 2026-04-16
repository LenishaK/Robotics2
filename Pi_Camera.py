## Below is the code for the Raspberry Pi, that i coded on thonny but due to hardware issues last minute we couldnt integrate it as we had hoped:

import os
import time
import subprocess
from PIL import Image
import numpy as np
import colorsys

IMAGE_FILE = "/home/lenishak/image.jpg"
DEBUG_DIR = "/home/lenishak/debug_regions"
OUTPUT_FILE = "/home/lenishak/assignments.txt"

# only using 3 colours and 3 places
TARGET_COLOURS = ["yellow", "blue", "pink"]
FIXED_POSITIONS = ["A", "B", "C"]   # A = left, B = middle, C = right

def take_picture():
    os.makedirs(DEBUG_DIR, exist_ok=True)

    result = subprocess.run(
        ["rpicam-jpeg", "-o", IMAGE_FILE, "-t", "1000", "--awb", "auto"],
        capture_output=True,
        text=True
    )

    time.sleep(1)

    if not os.path.isfile(IMAGE_FILE):
        print("Image was not created")
        print(result.stderr)
        return False

    return True

def classify_colour(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

    hue = h * 360
    sat = s * 100
    val = v * 100

    # too dark so it is harder to trust
    if val < 18:
        return None

    if 190 <= hue <= 255 and sat > 25 and val > 20:
        return "blue"

    if 35 <= hue <= 75 and sat > 35 and val > 45 and r > 100 and g > 100:
        return "yellow"

    if ((300 <= hue <= 360) or (0 <= hue <= 18)) and sat > 20 and val > 45 and r > g and b > g:
        return "pink"

    return None

def detect_region_colour(region_np, debug_name):
    debug_path = os.path.join(DEBUG_DIR, debug_name)
    Image.fromarray(region_np).save(debug_path)

    height, width, _ = region_np.shape

    # cut a bit off the edges so background does not affect it as much
    margin_x = int(width * 0.15)
    margin_y = int(height * 0.15)

    core = region_np[margin_y:height - margin_y, margin_x:width - margin_x]

    counts = {
        "yellow": 0,
        "blue": 0,
        "pink": 0
    }

    total_checked = 0
    r_total = 0
    g_total = 0
    b_total = 0

    # checking every 2 pixels so it runs a bit faster
    for y in range(0, core.shape[0], 2):
        for x in range(0, core.shape[1], 2):
            r, g, b = core[y, x]

            r_total += r
            g_total += g
            b_total += b
            total_checked += 1

            colour = classify_colour(r, g, b)
            if colour in counts:
                counts[colour] += 1

    if total_checked == 0:
        return None, counts

    avg_r = r_total / total_checked
    avg_g = g_total / total_checked
    avg_b = b_total / total_checked

    print("\nRegion", debug_name)
    print("Average RGB:", round(avg_r, 1), round(avg_g, 1), round(avg_b, 1))
    print("Pixel counts:", counts)
    print("Debug image saved to:", debug_path)

    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    top_colour, top_count = sorted_counts[0]

    # not enough pixels to be sure
    if top_count < 30:
        return None, counts

    # make sure the top colour is clearly stronger than the next one
    if len(sorted_counts) > 1:
        second_colour, second_count = sorted_counts[1]
        if second_count > 0 and top_count < second_count * 1.2:
            return None, counts

    return top_colour, counts

def split_into_three_vertical_regions(img_np):
    height, width, _ = img_np.shape
    third = width // 3

    regions = {
        "A": img_np[:, 0:third],
        "B": img_np[:, third:third * 2],
        "C": img_np[:, third * 2:width]
    }

    return regions

def detect_all_positions():
    img = Image.open(IMAGE_FILE).convert("RGB")
    img_np = np.array(img)

    regions = split_into_three_vertical_regions(img_np)

    position_to_colour = {}
    used_colours = set()

    for position in FIXED_POSITIONS:
        region = regions[position]
        colour, counts = detect_region_colour(region, f"{position}.jpg")

        # if the first result is empty or already used, try the next best one
        if colour is None or colour in used_colours:
            sorted_options = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            chosen = None

            for option_colour, option_count in sorted_options:
                if option_colour not in used_colours and option_count >= 30:
                    chosen = option_colour
                    break

            colour = chosen

        position_to_colour[position] = colour

        if colour is not None:
            used_colours.add(colour)

        print(position, "->", colour)

    return position_to_colour

def save_assignments(position_to_colour):
    with open(OUTPUT_FILE, "w") as f:
        for position in FIXED_POSITIONS:
            colour = position_to_colour.get(position)
            if colour is not None:
                f.write(f"{colour}:{position}\n")

        f.write("\n")

        for position in FIXED_POSITIONS:
            colour = position_to_colour.get(position)
            if colour is None:
                f.write(f"{position}:unknown\n")
            else:
                f.write(f"{position}:{colour}\n")

print("Starting 3 part colour detection...")

if not take_picture():
    print("Failed to take picture")
else:
    position_to_colour = detect_all_positions()

    print("\nFinal position to colour:")
    for position in FIXED_POSITIONS:
        print(position, "->", position_to_colour[position])

    save_assignments(position_to_colour)
    print("\nSaved to", OUTPUT_FILE)
