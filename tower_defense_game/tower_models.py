import math
from datetime import datetime

import dudraw


TOWER_TYPES = {}
SPECIAL_TOWERS = {}


def configure_tower_models(tower_types, special_towers):
    global TOWER_TYPES, SPECIAL_TOWERS

    TOWER_TYPES = tower_types
    SPECIAL_TOWERS = special_towers


def get_tower_stats(tower_type):
    if tower_type in TOWER_TYPES:
        return TOWER_TYPES[tower_type]

    return SPECIAL_TOWERS[tower_type]


def set_color(color):
    red, green, blue = color
    dudraw.set_pen_color_rgb(red, green, blue)


def brighten(color, amount):
    red, green, blue = color
    return (
        min(255, red + amount),
        min(255, green + amount),
        min(255, blue + amount),
    )


def darken(color, amount):
    red, green, blue = color
    return (
        max(0, red - amount),
        max(0, green - amount),
        max(0, blue - amount),
    )


def is_amazing(settings):
    return settings["graphics"] in ("amazing", "ultra")


def is_ultra(settings):
    return settings["graphics"] == "ultra"


def draw_shadow(x, y, scale):
    dudraw.set_pen_color_rgb(10, 13, 18)
    dudraw.filled_ellipse(x + 0.14 * scale, y - 0.36 * scale, 0.55 * scale, 0.16 * scale)
    dudraw.set_pen_color_rgb(44, 48, 51)
    dudraw.ellipse(x + 0.14 * scale, y - 0.36 * scale, 0.55 * scale, 0.16 * scale)


def draw_plinth(x, y, base, scale):
    set_color(darken(base, 45))
    dudraw.filled_triangle(
        x - 0.46 * scale,
        y - 0.34 * scale,
        x + 0.46 * scale,
        y - 0.34 * scale,
        x + 0.32 * scale,
        y - 0.02 * scale,
    )
    set_color(darken(base, 18))
    dudraw.filled_triangle(
        x - 0.46 * scale,
        y - 0.34 * scale,
        x - 0.32 * scale,
        y - 0.02 * scale,
        x + 0.32 * scale,
        y - 0.02 * scale,
    )
    set_color(brighten(base, 30))
    dudraw.line(x - 0.33 * scale, y - 0.02 * scale, x + 0.32 * scale, y - 0.02 * scale)
    set_color(brighten(base, 55))
    dudraw.filled_circle(x, y - 0.2 * scale, 0.035 * scale)


def draw_gem(x, y, color, scale):
    set_color(brighten(color, 60))
    dudraw.filled_triangle(x, y + 0.13 * scale, x - 0.12 * scale, y, x + 0.12 * scale, y)
    set_color(color)
    dudraw.filled_triangle(x, y - 0.13 * scale, x - 0.12 * scale, y, x + 0.12 * scale, y)
    dudraw.set_pen_color_rgb(246, 250, 238)
    dudraw.filled_circle(x - 0.035 * scale, y + 0.045 * scale, 0.025 * scale)


def draw_arcane_orbits(x, y, color, frame, radius, count, scale):
    for i in range(count):
        angle = frame * 0.035 + i * 2 * math.pi / count
        ox = x + math.cos(angle) * radius * scale
        oy = y + math.sin(angle) * radius * 0.72 * scale
        set_color(brighten(color, 72))
        dudraw.filled_circle(ox, oy, 0.045 * scale)
        set_color(brighten(color, 25))
        dudraw.circle(ox, oy, 0.08 * scale)


def draw_arrow_model(x, y, aim_x, aim_y, frame, scale):
    side_x = -aim_y
    side_y = aim_x
    sway = math.sin(frame * 0.05 + x) * 0.012 * scale

    # Open legs and ladder keep the tall lookout readable without hiding nearby units.
    dudraw.set_pen_color_rgb(78, 48, 29)
    dudraw.filled_triangle(x - 0.28 * scale, y - 0.34 * scale, x - 0.2 * scale, y - 0.34 * scale, x - 0.1 * scale, y + 0.17 * scale)
    dudraw.filled_triangle(x - 0.28 * scale, y - 0.34 * scale, x - 0.1 * scale, y + 0.17 * scale, x - 0.16 * scale, y + 0.17 * scale)
    dudraw.filled_triangle(x + 0.18 * scale, y - 0.34 * scale, x + 0.27 * scale, y - 0.34 * scale, x + 0.17 * scale, y + 0.17 * scale)
    dudraw.filled_triangle(x + 0.18 * scale, y - 0.34 * scale, x + 0.17 * scale, y + 0.17 * scale, x + 0.11 * scale, y + 0.17 * scale)
    dudraw.set_pen_color_rgb(151, 98, 50)
    dudraw.line(x - 0.1 * scale, y - 0.27 * scale, x + 0.12 * scale, y + 0.14 * scale)
    dudraw.line(x + 0.09 * scale, y - 0.27 * scale, x - 0.13 * scale, y + 0.14 * scale)
    for rung in range(3):
        rung_y = y - 0.2 * scale + rung * 0.11 * scale
        dudraw.line(x - 0.09 * scale, rung_y, x + 0.09 * scale, rung_y)

    # An offset platform, wall and roof establish a compact three-dimensional silhouette.
    dudraw.set_pen_color_rgb(87, 50, 27)
    dudraw.filled_triangle(x - 0.34 * scale, y + 0.14 * scale, x + 0.27 * scale, y + 0.14 * scale, x + 0.35 * scale, y + 0.23 * scale)
    dudraw.filled_triangle(x - 0.34 * scale, y + 0.14 * scale, x + 0.35 * scale, y + 0.23 * scale, x - 0.25 * scale, y + 0.23 * scale)
    dudraw.set_pen_color_rgb(187, 128, 65)
    dudraw.filled_triangle(x - 0.32 * scale, y + 0.23 * scale, x + 0.27 * scale, y + 0.23 * scale, x + 0.34 * scale, y + 0.29 * scale)
    dudraw.filled_triangle(x - 0.32 * scale, y + 0.23 * scale, x + 0.34 * scale, y + 0.29 * scale, x - 0.23 * scale, y + 0.29 * scale)
    dudraw.set_pen_color_rgb(131, 81, 42)
    dudraw.filled_rectangle(x - 0.02 * scale, y + 0.43 * scale, 0.23 * scale, 0.14 * scale)
    dudraw.set_pen_color_rgb(170, 113, 56)
    dudraw.filled_triangle(x - 0.25 * scale, y + 0.29 * scale, x - 0.25 * scale, y + 0.56 * scale, x + 0.2 * scale, y + 0.56 * scale)
    dudraw.filled_triangle(x - 0.25 * scale, y + 0.29 * scale, x + 0.2 * scale, y + 0.56 * scale, x + 0.2 * scale, y + 0.29 * scale)
    dudraw.set_pen_color_rgb(85, 113, 77)
    dudraw.filled_triangle(x - 0.36 * scale, y + 0.54 * scale, x + 0.18 * scale, y + 0.54 * scale, x - 0.06 * scale, y + 0.76 * scale)
    dudraw.set_pen_color_rgb(56, 79, 59)
    dudraw.filled_triangle(x + 0.18 * scale, y + 0.54 * scale, x + 0.35 * scale, y + 0.61 * scale, x - 0.06 * scale, y + 0.76 * scale)
    dudraw.set_pen_color_rgb(222, 173, 86)
    dudraw.filled_rectangle(x - 0.13 * scale, y + 0.43 * scale, 0.065 * scale, 0.075 * scale)

    # Ranger and bow stay on the upper deck, inside the footprint of the tower.
    ranger_x = x + sway
    ranger_y = y + 0.37 * scale
    dudraw.set_pen_color_rgb(48, 91, 53)
    dudraw.filled_triangle(ranger_x - 0.08 * scale, ranger_y - 0.09 * scale, ranger_x, ranger_y + 0.12 * scale, ranger_x + 0.08 * scale, ranger_y - 0.09 * scale)
    dudraw.set_pen_color_rgb(235, 216, 171)
    dudraw.filled_circle(ranger_x, ranger_y + 0.1 * scale, 0.055 * scale)
    dudraw.set_pen_color_rgb(96, 58, 32)
    dudraw.line(ranger_x - side_x * 0.11 * scale, ranger_y + side_y * -0.02 * scale, ranger_x + side_x * 0.11 * scale, ranger_y + side_y * 0.02 * scale)
    tip_x = ranger_x + aim_x * 0.32 * scale
    tip_y = ranger_y + aim_y * 0.32 * scale
    dudraw.line(ranger_x, ranger_y, tip_x, tip_y)
    dudraw.set_pen_color_rgb(248, 236, 183)
    dudraw.filled_triangle(
        tip_x,
        tip_y,
        tip_x - aim_x * 0.1 * scale + side_x * 0.045 * scale,
        tip_y - aim_y * 0.1 * scale + side_y * 0.045 * scale,
        tip_x - aim_x * 0.1 * scale - side_x * 0.045 * scale,
        tip_y - aim_y * 0.1 * scale - side_y * 0.045 * scale,
    )


def draw_cannon_model(x, y, aim_x, aim_y, frame, scale):
    side_x = -aim_y
    side_y = aim_x

    # A compact field emplacement: timber carriage, iron shield and short cannon.
    dudraw.set_pen_color_rgb(72, 44, 25)
    dudraw.filled_triangle(
        x - 0.31 * scale, y - 0.25 * scale,
        x + 0.24 * scale, y - 0.25 * scale,
        x + 0.32 * scale, y - 0.14 * scale,
    )
    dudraw.filled_triangle(
        x - 0.31 * scale, y - 0.25 * scale,
        x + 0.32 * scale, y - 0.14 * scale,
        x - 0.22 * scale, y - 0.14 * scale,
    )
    dudraw.set_pen_color_rgb(172, 111, 55)
    dudraw.filled_triangle(
        x - 0.28 * scale, y - 0.14 * scale,
        x + 0.25 * scale, y - 0.14 * scale,
        x + 0.3 * scale, y - 0.08 * scale,
    )
    dudraw.filled_triangle(
        x - 0.28 * scale, y - 0.14 * scale,
        x + 0.3 * scale, y - 0.08 * scale,
        x - 0.22 * scale, y - 0.08 * scale,
    )
    dudraw.set_pen_color_rgb(42, 45, 47)
    dudraw.filled_circle(x - 0.24 * scale, y - 0.24 * scale, 0.09 * scale)
    dudraw.filled_circle(x + 0.23 * scale, y - 0.18 * scale, 0.09 * scale)
    dudraw.set_pen_color_rgb(216, 165, 76)
    dudraw.filled_circle(x - 0.24 * scale, y - 0.24 * scale, 0.03 * scale)
    dudraw.filled_circle(x + 0.23 * scale, y - 0.18 * scale, 0.03 * scale)

    dudraw.set_pen_color_rgb(81, 91, 96)
    dudraw.filled_triangle(
        x - 0.17 * scale, y - 0.03 * scale,
        x - 0.13 * scale, y + 0.19 * scale,
        x + 0.2 * scale, y + 0.16 * scale,
    )
    dudraw.filled_triangle(
        x - 0.17 * scale, y - 0.03 * scale,
        x + 0.2 * scale, y + 0.16 * scale,
        x + 0.19 * scale, y - 0.02 * scale,
    )
    dudraw.set_pen_color_rgb(154, 164, 168)
    dudraw.line(x - 0.1 * scale, y + 0.13 * scale, x + 0.14 * scale, y + 0.11 * scale)

    mount_x = x
    mount_y = y - 0.02 * scale
    dudraw.set_pen_color_rgb(116, 74, 38)
    dudraw.filled_rectangle(mount_x, mount_y, 0.15 * scale, 0.08 * scale)
    dudraw.set_pen_color_rgb(48, 53, 57)
    dudraw.filled_circle(mount_x, y + 0.04 * scale, 0.125 * scale)
    dudraw.set_pen_color_rgb(174, 129, 63)
    dudraw.filled_circle(mount_x, y + 0.04 * scale, 0.042 * scale)

    breech_x = x + aim_x * 0.03 * scale
    breech_y = y + 0.08 * scale + aim_y * 0.03 * scale
    muzzle_x = x + aim_x * 0.47 * scale
    muzzle_y = y + 0.08 * scale + aim_y * 0.47 * scale
    dudraw.set_pen_color_rgb(38, 43, 47)
    dudraw.filled_triangle(
        breech_x - side_x * 0.09 * scale, breech_y - side_y * 0.09 * scale,
        muzzle_x - side_x * 0.07 * scale, muzzle_y - side_y * 0.07 * scale,
        muzzle_x + side_x * 0.07 * scale, muzzle_y + side_y * 0.07 * scale,
    )
    dudraw.filled_triangle(
        breech_x - side_x * 0.09 * scale, breech_y - side_y * 0.09 * scale,
        muzzle_x + side_x * 0.07 * scale, muzzle_y + side_y * 0.07 * scale,
        breech_x + side_x * 0.09 * scale, breech_y + side_y * 0.09 * scale,
    )
    dudraw.set_pen_color_rgb(93, 102, 107)
    dudraw.line(
        breech_x - side_x * 0.04 * scale, breech_y - side_y * 0.04 * scale,
        muzzle_x - side_x * 0.035 * scale, muzzle_y - side_y * 0.035 * scale,
    )
    dudraw.set_pen_color_rgb(60, 68, 73)
    dudraw.filled_circle(breech_x, breech_y, 0.1 * scale)
    dudraw.set_pen_color_rgb(137, 148, 153)
    dudraw.circle(breech_x, breech_y, 0.1 * scale)
    dudraw.set_pen_color_rgb(31, 35, 39)
    dudraw.filled_circle(muzzle_x, muzzle_y, 0.078 * scale)
    dudraw.set_pen_color_rgb(246, 127, 57)
    dudraw.filled_circle(muzzle_x, muzzle_y, 0.036 * scale)
    dudraw.set_pen_color_rgb(255, 213, 123)
    dudraw.circle(muzzle_x, muzzle_y, (0.084 + 0.01 * math.sin(frame * 0.14)) * scale)


def draw_frost_model(x, y, aim_x, aim_y, frame, scale):
    shimmer = 0.02 * math.sin(frame * 0.09) * scale

    # Icy masonry tower with offset side face and raised casting balcony.
    dudraw.set_pen_color_rgb(77, 145, 177)
    dudraw.filled_triangle(
        x - 0.27 * scale, y - 0.32 * scale,
        x + 0.18 * scale, y - 0.32 * scale,
        x + 0.24 * scale, y + 0.3 * scale,
    )
    dudraw.filled_triangle(
        x - 0.27 * scale, y - 0.32 * scale,
        x + 0.24 * scale, y + 0.3 * scale,
        x - 0.2 * scale, y + 0.3 * scale,
    )
    dudraw.set_pen_color_rgb(102, 189, 220)
    dudraw.filled_triangle(
        x + 0.18 * scale, y - 0.32 * scale,
        x + 0.32 * scale, y - 0.22 * scale,
        x + 0.3 * scale, y + 0.36 * scale,
    )
    dudraw.filled_triangle(
        x + 0.18 * scale, y - 0.32 * scale,
        x + 0.3 * scale, y + 0.36 * scale,
        x + 0.24 * scale, y + 0.3 * scale,
    )
    dudraw.set_pen_color_rgb(188, 238, 250)
    for window_y in (-0.12, 0.08):
        dudraw.filled_rectangle(x - 0.04 * scale, y + window_y * scale, 0.045 * scale, 0.06 * scale)
    dudraw.set_pen_color_rgb(221, 251, 255)
    dudraw.filled_triangle(
        x - 0.34 * scale, y + 0.3 * scale,
        x + 0.25 * scale, y + 0.3 * scale,
        x + 0.33 * scale, y + 0.38 * scale,
    )
    dudraw.filled_triangle(
        x - 0.34 * scale, y + 0.3 * scale,
        x + 0.33 * scale, y + 0.38 * scale,
        x - 0.26 * scale, y + 0.38 * scale,
    )
    dudraw.set_pen_color_rgb(83, 160, 196)
    dudraw.line(x - 0.27 * scale, y + 0.41 * scale, x - 0.27 * scale, y + 0.56 * scale)
    dudraw.line(x + 0.25 * scale, y + 0.42 * scale, x + 0.25 * scale, y + 0.57 * scale)
    dudraw.line(x - 0.27 * scale, y + 0.53 * scale, x + 0.25 * scale, y + 0.55 * scale)

    # A small frost wizard casts from the open turret platform.
    wizard_y = y + 0.52 * scale
    dudraw.set_pen_color_rgb(70, 130, 190)
    dudraw.filled_triangle(x - 0.1 * scale, wizard_y - 0.08 * scale, x, wizard_y + 0.14 * scale, x + 0.1 * scale, wizard_y - 0.08 * scale)
    dudraw.set_pen_color_rgb(234, 242, 245)
    dudraw.filled_circle(x, wizard_y + 0.14 * scale, 0.055 * scale)
    dudraw.set_pen_color_rgb(99, 186, 232)
    dudraw.filled_triangle(x - 0.11 * scale, wizard_y + 0.17 * scale, x + 0.01 * scale, wizard_y + 0.34 * scale, x + 0.12 * scale, wizard_y + 0.17 * scale)
    orb_x = x + aim_x * 0.2 * scale
    orb_y = wizard_y + 0.08 * scale + aim_y * 0.2 * scale
    dudraw.set_pen_color_rgb(213, 250, 255)
    dudraw.filled_circle(orb_x, orb_y, (0.048 * scale) + shimmer)
    dudraw.set_pen_color_rgb(137, 223, 247)
    dudraw.circle(orb_x, orb_y, 0.09 * scale)


def draw_sniper_model(x, y, aim_x, aim_y, frame, scale):
    side_x = -aim_y
    side_y = aim_x

    # Compact layered cliff with a flat firing shelf.
    dudraw.set_pen_color_rgb(49, 50, 59)
    dudraw.filled_triangle(
        x - 0.34 * scale, y - 0.32 * scale,
        x + 0.28 * scale, y - 0.32 * scale,
        x + 0.13 * scale, y + 0.25 * scale,
    )
    dudraw.set_pen_color_rgb(74, 77, 87)
    dudraw.filled_triangle(
        x - 0.34 * scale, y - 0.32 * scale,
        x + 0.13 * scale, y + 0.25 * scale,
        x - 0.22 * scale, y + 0.2 * scale,
    )
    dudraw.set_pen_color_rgb(112, 115, 124)
    dudraw.filled_triangle(
        x - 0.24 * scale, y + 0.19 * scale,
        x + 0.13 * scale, y + 0.25 * scale,
        x + 0.31 * scale, y + 0.2 * scale,
    )
    dudraw.filled_triangle(
        x - 0.24 * scale, y + 0.19 * scale,
        x + 0.31 * scale, y + 0.2 * scale,
        x - 0.08 * scale, y + 0.12 * scale,
    )
    dudraw.set_pen_color_rgb(188, 195, 202)
    dudraw.line(x - 0.22 * scale, y + 0.2 * scale, x + 0.13 * scale, y + 0.25 * scale)
    dudraw.set_pen_color_rgb(88, 93, 101)
    dudraw.line(x - 0.19 * scale, y - 0.08 * scale, x - 0.04 * scale, y + 0.1 * scale)
    dudraw.line(x + 0.05 * scale, y - 0.19 * scale, x + 0.15 * scale, y + 0.05 * scale)

    # Prone marksman and rifle follow target aim from the cliff edge.
    body_x = x - aim_x * 0.06 * scale
    body_y = y + 0.31 * scale - aim_y * 0.04 * scale
    boot_x = body_x - aim_x * 0.2 * scale
    boot_y = body_y - aim_y * 0.2 * scale
    dudraw.set_pen_color_rgb(35, 42, 39)
    dudraw.line(boot_x - side_x * 0.04 * scale, boot_y - side_y * 0.04 * scale, boot_x - aim_x * 0.08 * scale, boot_y - aim_y * 0.08 * scale)
    dudraw.line(boot_x + side_x * 0.04 * scale, boot_y + side_y * 0.04 * scale, boot_x - aim_x * 0.08 * scale, boot_y - aim_y * 0.08 * scale)
    dudraw.set_pen_color_rgb(55, 76, 62)
    dudraw.filled_triangle(
        boot_x - side_x * 0.07 * scale, boot_y - side_y * 0.07 * scale,
        body_x - side_x * 0.09 * scale, body_y - side_y * 0.09 * scale,
        body_x + side_x * 0.09 * scale, body_y + side_y * 0.09 * scale,
    )
    dudraw.filled_triangle(
        boot_x - side_x * 0.07 * scale, boot_y - side_y * 0.07 * scale,
        body_x + side_x * 0.09 * scale, body_y + side_y * 0.09 * scale,
        boot_x + side_x * 0.07 * scale, boot_y + side_y * 0.07 * scale,
    )
    shoulder_x = body_x + aim_x * 0.13 * scale
    shoulder_y = body_y + aim_y * 0.13 * scale
    dudraw.set_pen_color_rgb(72, 96, 76)
    dudraw.filled_circle(shoulder_x, shoulder_y, 0.075 * scale)
    head_x = body_x + aim_x * 0.21 * scale
    head_y = body_y + aim_y * 0.21 * scale + 0.02 * scale
    dudraw.set_pen_color_rgb(215, 203, 179)
    dudraw.filled_circle(head_x, head_y, 0.06 * scale)
    dudraw.set_pen_color_rgb(43, 59, 50)
    dudraw.filled_triangle(
        head_x - side_x * 0.067 * scale, head_y - side_y * 0.067 * scale + 0.025 * scale,
        head_x + aim_x * 0.08 * scale, head_y + aim_y * 0.08 * scale + 0.025 * scale,
        head_x + side_x * 0.067 * scale, head_y + side_y * 0.067 * scale + 0.025 * scale,
    )
    barrel_start_x = shoulder_x + aim_x * 0.01 * scale
    barrel_start_y = shoulder_y + aim_y * 0.01 * scale
    barrel_end_x = body_x + aim_x * 0.63 * scale
    barrel_end_y = body_y + aim_y * 0.63 * scale
    dudraw.set_pen_color_rgb(22, 25, 31)
    dudraw.line(barrel_start_x - side_x * 0.026 * scale, barrel_start_y - side_y * 0.026 * scale, barrel_end_x, barrel_end_y)
    dudraw.line(barrel_start_x + side_x * 0.026 * scale, barrel_start_y + side_y * 0.026 * scale, barrel_end_x, barrel_end_y)
    dudraw.set_pen_color_rgb(175, 204, 217)
    dudraw.filled_circle(body_x + aim_x * 0.36 * scale, body_y + aim_y * 0.36 * scale, 0.025 * scale)
    dudraw.set_pen_color_rgb(62, 66, 73)
    support_x = body_x + aim_x * 0.45 * scale
    support_y = body_y + aim_y * 0.45 * scale
    dudraw.line(support_x, support_y, support_x - side_x * 0.08 * scale, support_y - side_y * 0.08 * scale - 0.09 * scale)
    dudraw.line(support_x, support_y, support_x + side_x * 0.08 * scale, support_y + side_y * 0.08 * scale - 0.09 * scale)
    dudraw.set_pen_color_rgb(255, 225, 148)
    dudraw.filled_circle(barrel_end_x, barrel_end_y, (0.028 + 0.006 * math.sin(frame * 0.08)) * scale)


def draw_laser_model(x, y, aim_x, aim_y, frame, scale):
    pulse = 0.018 * math.sin(frame * 0.15)

    # Narrow metal transmission pylon, kept open so adjacent units remain legible.
    dudraw.set_pen_color_rgb(42, 48, 55)
    dudraw.line(x - 0.25 * scale, y - 0.32 * scale, x - 0.07 * scale, y + 0.49 * scale)
    dudraw.line(x + 0.25 * scale, y - 0.32 * scale, x + 0.07 * scale, y + 0.49 * scale)
    dudraw.set_pen_color_rgb(114, 125, 137)
    dudraw.line(x - 0.19 * scale, y - 0.07 * scale, x + 0.15 * scale, y + 0.15 * scale)
    dudraw.line(x + 0.19 * scale, y - 0.07 * scale, x - 0.15 * scale, y + 0.15 * scale)
    dudraw.line(x - 0.13 * scale, y + 0.2 * scale, x + 0.1 * scale, y + 0.35 * scale)
    dudraw.line(x + 0.13 * scale, y + 0.2 * scale, x - 0.1 * scale, y + 0.35 * scale)
    dudraw.set_pen_color_rgb(171, 182, 192)
    dudraw.line(x - 0.28 * scale, y - 0.31 * scale, x + 0.28 * scale, y - 0.31 * scale)
    dudraw.line(x - 0.2 * scale, y - 0.04 * scale, x + 0.2 * scale, y - 0.04 * scale)
    dudraw.line(x - 0.14 * scale, y + 0.2 * scale, x + 0.14 * scale, y + 0.2 * scale)
    dudraw.line(x - 0.31 * scale, y + 0.34 * scale, x + 0.31 * scale, y + 0.34 * scale)
    dudraw.set_pen_color_rgb(64, 72, 82)
    dudraw.line(x - 0.31 * scale, y + 0.34 * scale, x - 0.31 * scale, y + 0.23 * scale)
    dudraw.line(x + 0.31 * scale, y + 0.34 * scale, x + 0.31 * scale, y + 0.23 * scale)
    dudraw.set_pen_color_rgb(234, 220, 200)
    dudraw.filled_circle(x - 0.31 * scale, y + 0.2 * scale, 0.035 * scale)
    dudraw.filled_circle(x + 0.31 * scale, y + 0.2 * scale, 0.035 * scale)

    emitter_y = y + 0.53 * scale
    dudraw.set_pen_color_rgb(49, 55, 64)
    dudraw.filled_rectangle(x, y + 0.42 * scale, 0.09 * scale, 0.07 * scale)
    dudraw.set_pen_color_rgb(108, 10, 29)
    dudraw.filled_circle(x, emitter_y, (0.155 + pulse) * scale)
    dudraw.set_pen_color_rgb(248, 51, 83)
    dudraw.filled_circle(x, emitter_y, (0.11 + pulse) * scale)
    dudraw.set_pen_color_rgb(255, 192, 201)
    dudraw.filled_circle(x - 0.04 * scale, emitter_y + 0.045 * scale, 0.035 * scale)
    dudraw.set_pen_color_rgb(255, 86, 106)
    dudraw.circle(x, emitter_y, (0.205 + pulse) * scale)


def draw_mortar_model(x, y, aim_x, aim_y, frame, scale):
    side_x = -aim_y
    side_y = aim_x

    # A low sandbag nest keeps this indirect-fire unit compact and recognizable.
    dudraw.set_pen_color_rgb(54, 62, 53)
    dudraw.filled_ellipse(x, y - 0.26 * scale, 0.33 * scale, 0.1 * scale)
    dudraw.set_pen_color_rgb(133, 112, 70)
    for bag_x, bag_y in ((-0.27, -0.18), (-0.1, -0.23), (0.08, -0.23), (0.25, -0.17), (-0.17, -0.08), (0.18, -0.07)):
        dudraw.filled_ellipse(x + bag_x * scale, y + bag_y * scale, 0.1 * scale, 0.055 * scale)
    dudraw.set_pen_color_rgb(190, 161, 100)
    dudraw.line(x - 0.34 * scale, y - 0.14 * scale, x + 0.34 * scale, y - 0.13 * scale)

    dudraw.set_pen_color_rgb(47, 54, 51)
    dudraw.filled_circle(x, y - 0.06 * scale, 0.12 * scale)
    dudraw.set_pen_color_rgb(90, 101, 94)
    dudraw.circle(x, y - 0.06 * scale, 0.12 * scale)
    pivot_x = x + aim_x * 0.04 * scale
    pivot_y = y + aim_y * 0.04 * scale
    muzzle_x = x + aim_x * 0.26 * scale
    muzzle_y = y + 0.28 * scale + aim_y * 0.16 * scale
    dudraw.set_pen_color_rgb(34, 39, 39)
    dudraw.line(x - side_x * 0.09 * scale, y - 0.04 * scale - side_y * 0.09 * scale, pivot_x, pivot_y)
    dudraw.line(x + side_x * 0.09 * scale, y - 0.04 * scale + side_y * 0.09 * scale, pivot_x, pivot_y)
    dudraw.line(x, y - 0.07 * scale, x - aim_x * 0.1 * scale, y - 0.2 * scale - aim_y * 0.1 * scale)
    dudraw.set_pen_color_rgb(30, 35, 35)
    dudraw.line(pivot_x - side_x * 0.07 * scale, pivot_y - side_y * 0.07 * scale, muzzle_x - side_x * 0.06 * scale, muzzle_y - side_y * 0.06 * scale)
    dudraw.line(pivot_x + side_x * 0.07 * scale, pivot_y + side_y * 0.07 * scale, muzzle_x + side_x * 0.06 * scale, muzzle_y + side_y * 0.06 * scale)
    dudraw.set_pen_color_rgb(72, 83, 79)
    dudraw.line(pivot_x, pivot_y + 0.015 * scale, muzzle_x, muzzle_y + 0.015 * scale)
    dudraw.set_pen_color_rgb(24, 29, 29)
    dudraw.filled_circle(muzzle_x, muzzle_y, 0.067 * scale)
    dudraw.set_pen_color_rgb(255, 169, 72)
    dudraw.filled_circle(muzzle_x, muzzle_y, 0.029 * scale)

    dudraw.set_pen_color_rgb(46, 55, 49)
    dudraw.filled_rectangle(x + 0.27 * scale, y - 0.01 * scale, 0.08 * scale, 0.115 * scale)
    dudraw.set_pen_color_rgb(221, 159, 69)
    dudraw.filled_circle(x + 0.23 * scale, y + 0.06 * scale, 0.035 * scale)
    dudraw.filled_circle(x + 0.31 * scale, y + 0.1 * scale, 0.035 * scale)


def draw_venom_model(x, y, aim_x, aim_y, frame, scale):
    sway = math.sin(frame * 0.045 + x) * 0.025 * scale
    blink = math.sin(frame * 0.11) > 0.96
    side_x = -aim_y
    side_y = aim_x

    # A knotted jungle tree gives the poison attacker a natural perch.
    dudraw.set_pen_color_rgb(53, 38, 24)
    dudraw.filled_ellipse(x, y - 0.29 * scale, 0.34 * scale, 0.08 * scale)
    dudraw.set_pen_color_rgb(87, 57, 30)
    dudraw.filled_triangle(
        x - 0.19 * scale, y - 0.3 * scale,
        x - 0.12 * scale, y + 0.34 * scale,
        x + 0.12 * scale, y + 0.37 * scale,
    )
    dudraw.filled_triangle(
        x - 0.19 * scale, y - 0.3 * scale,
        x + 0.12 * scale, y + 0.37 * scale,
        x + 0.2 * scale, y - 0.3 * scale,
    )
    dudraw.set_pen_color_rgb(130, 82, 39)
    dudraw.line(x - 0.04 * scale, y - 0.2 * scale, x - 0.02 * scale, y + 0.3 * scale)
    dudraw.line(x + 0.03 * scale, y + 0.08 * scale, x + 0.36 * scale, y + 0.33 * scale)
    dudraw.line(x - 0.03 * scale, y + 0.2 * scale, x - 0.35 * scale, y + 0.42 * scale)
    dudraw.set_pen_color_rgb(69, 48, 26)
    dudraw.line(x - 0.16 * scale, y - 0.24 * scale, x - 0.32 * scale, y - 0.3 * scale)
    dudraw.line(x + 0.14 * scale, y - 0.25 * scale, x + 0.32 * scale, y - 0.3 * scale)

    dudraw.set_pen_color_rgb(42, 102, 51)
    for leaf_x, leaf_y, leaf_size in (
        (-0.29, 0.42, 0.16), (-0.11, 0.55, 0.19), (0.11, 0.54, 0.2),
        (0.3, 0.4, 0.16), (-0.38, 0.3, 0.12), (0.38, 0.29, 0.12),
    ):
        dudraw.filled_circle(x + leaf_x * scale, y + leaf_y * scale + sway, leaf_size * scale)
    dudraw.set_pen_color_rgb(83, 155, 66)
    dudraw.filled_circle(x - 0.13 * scale, y + 0.58 * scale + sway, 0.09 * scale)
    dudraw.filled_circle(x + 0.27 * scale, y + 0.43 * scale + sway, 0.075 * scale)

    # The snake curls over a branch and hangs below it before aiming its strike.
    dudraw.set_pen_color_rgb(35, 74, 33)
    dudraw.line(x - 0.2 * scale, y + 0.33 * scale, x + 0.18 * scale, y + 0.33 * scale)
    dudraw.set_pen_color_rgb(86, 183, 55)
    coil_points = ((-0.18, 0.37), (-0.06, 0.42), (0.07, 0.36), (0.16, 0.25), (0.12, 0.12))
    for first, second in zip(coil_points, coil_points[1:]):
        dudraw.line(
            x + first[0] * scale, y + first[1] * scale,
            x + second[0] * scale, y + second[1] * scale,
        )
    dudraw.set_pen_color_rgb(143, 226, 71)
    dudraw.line(x - 0.17 * scale, y + 0.39 * scale, x + 0.04 * scale, y + 0.38 * scale)
    head_x = x + 0.12 * scale + aim_x * 0.08 * scale
    head_y = y + 0.12 * scale + aim_y * 0.08 * scale
    dudraw.set_pen_color_rgb(77, 162, 45)
    dudraw.filled_circle(head_x, head_y, 0.1 * scale)
    dudraw.filled_triangle(
        head_x + aim_x * 0.12 * scale,
        head_y + aim_y * 0.12 * scale,
        head_x + side_x * 0.075 * scale,
        head_y + side_y * 0.075 * scale,
        head_x - side_x * 0.075 * scale,
        head_y - side_y * 0.075 * scale,
    )
    if not blink:
        dudraw.set_pen_color_rgb(247, 215, 70)
        dudraw.filled_circle(head_x + aim_x * 0.06 * scale + side_x * 0.04 * scale, head_y + aim_y * 0.06 * scale + side_y * 0.04 * scale, 0.017 * scale)
    dudraw.set_pen_color_rgb(236, 72, 80)
    tongue_x = head_x + aim_x * 0.18 * scale
    tongue_y = head_y + aim_y * 0.18 * scale
    dudraw.line(head_x + aim_x * 0.11 * scale, head_y + aim_y * 0.11 * scale, tongue_x, tongue_y)
    dudraw.line(tongue_x, tongue_y, tongue_x + aim_x * 0.04 * scale + side_x * 0.03 * scale, tongue_y + aim_y * 0.04 * scale + side_y * 0.03 * scale)
    dudraw.line(tongue_x, tongue_y, tongue_x + aim_x * 0.04 * scale - side_x * 0.03 * scale, tongue_y + aim_y * 0.04 * scale - side_y * 0.03 * scale)


def draw_storm_model(x, y, aim_x, aim_y, frame, scale):
    pulse = math.sin(frame * 0.13) * 0.018 * scale
    drift = math.sin(frame * 0.04 + x) * 0.025 * scale

    # A grounded conductor shrine traps a compact thundercloud above its rods.
    dudraw.set_pen_color_rgb(48, 53, 60)
    dudraw.filled_ellipse(x, y - 0.26 * scale, 0.35 * scale, 0.1 * scale)
    dudraw.set_pen_color_rgb(79, 89, 100)
    dudraw.filled_triangle(
        x - 0.32 * scale, y - 0.2 * scale,
        x + 0.31 * scale, y - 0.2 * scale,
        x + 0.23 * scale, y - 0.05 * scale,
    )
    dudraw.filled_triangle(
        x - 0.32 * scale, y - 0.2 * scale,
        x + 0.23 * scale, y - 0.05 * scale,
        x - 0.23 * scale, y - 0.05 * scale,
    )
    dudraw.set_pen_color_rgb(150, 163, 174)
    dudraw.line(x - 0.23 * scale, y - 0.05 * scale, x + 0.23 * scale, y - 0.05 * scale)
    dudraw.set_pen_color_rgb(56, 73, 91)
    dudraw.filled_circle(x, y - 0.02 * scale, 0.13 * scale)
    dudraw.set_pen_color_rgb(135, 199, 237)
    dudraw.circle(x, y - 0.02 * scale, (0.1 * scale) + pulse)

    for rod_x, rod_height in ((-0.22, 0.32), (0.0, 0.43), (0.22, 0.32)):
        dudraw.set_pen_color_rgb(92, 59, 35)
        dudraw.line(x + rod_x * scale, y - 0.03 * scale, x + rod_x * scale, y + rod_height * scale)
        dudraw.set_pen_color_rgb(194, 124, 56)
        dudraw.line(x + rod_x * scale + 0.025 * scale, y - 0.03 * scale, x + rod_x * scale + 0.025 * scale, y + rod_height * scale)
        dudraw.set_pen_color_rgb(251, 209, 107)
        dudraw.filled_circle(x + rod_x * scale + 0.012 * scale, y + rod_height * scale, 0.03 * scale)

    cloud_x = x + drift
    cloud_y = y + 0.49 * scale
    dudraw.set_pen_color_rgb(42, 48, 65)
    dudraw.filled_ellipse(cloud_x, cloud_y - 0.035 * scale, 0.35 * scale, 0.13 * scale)
    dudraw.filled_circle(cloud_x - 0.2 * scale, cloud_y + 0.04 * scale, 0.14 * scale)
    dudraw.filled_circle(cloud_x, cloud_y + 0.13 * scale, 0.2 * scale)
    dudraw.filled_circle(cloud_x + 0.2 * scale, cloud_y + 0.06 * scale, 0.15 * scale)
    dudraw.set_pen_color_rgb(91, 105, 135)
    dudraw.filled_circle(cloud_x - 0.05 * scale, cloud_y + 0.17 * scale, 0.09 * scale)
    dudraw.set_pen_color_rgb(113, 139, 172)
    dudraw.line(cloud_x - 0.23 * scale, cloud_y - 0.05 * scale, cloud_x + 0.2 * scale, cloud_y - 0.05 * scale)

    flash = 0.025 * math.sin(frame * 0.2)
    dudraw.set_pen_color_rgb(255, 239, 111)
    dudraw.filled_triangle(
        cloud_x - 0.04 * scale, cloud_y - 0.05 * scale,
        cloud_x + 0.08 * scale, cloud_y - 0.05 * scale,
        cloud_x - 0.02 * scale, y + (0.23 + flash) * scale,
    )
    dudraw.filled_triangle(
        cloud_x - 0.02 * scale, y + (0.23 + flash) * scale,
        cloud_x + 0.07 * scale, y + (0.23 + flash) * scale,
        x + 0.01 * scale, y + 0.04 * scale,
    )
    dudraw.set_pen_color_rgb(244, 251, 255)
    dudraw.line(cloud_x + 0.015 * scale, cloud_y - 0.045 * scale, x + 0.015 * scale, y + 0.07 * scale)


def draw_titan_model(x, y, aim_x, aim_y, frame, scale):
    pulse = math.sin(frame * 0.13) * 0.018 * scale

    # Marble cloud pedestal and flowing robes keep Zeus regal and readable.
    dudraw.set_pen_color_rgb(173, 186, 202)
    dudraw.filled_ellipse(x, y - 0.28 * scale, 0.43 * scale, 0.1 * scale)
    dudraw.set_pen_color_rgb(224, 231, 238)
    dudraw.filled_circle(x - 0.27 * scale, y - 0.2 * scale, 0.13 * scale)
    dudraw.filled_circle(x - 0.06 * scale, y - 0.16 * scale, 0.17 * scale)
    dudraw.filled_circle(x + 0.18 * scale, y - 0.19 * scale, 0.15 * scale)
    dudraw.set_pen_color_rgb(249, 250, 247)
    dudraw.filled_triangle(
        x - 0.2 * scale, y - 0.17 * scale,
        x - 0.11 * scale, y + 0.4 * scale,
        x + 0.15 * scale, y + 0.4 * scale,
    )
    dudraw.filled_triangle(
        x - 0.2 * scale, y - 0.17 * scale,
        x + 0.15 * scale, y + 0.4 * scale,
        x + 0.25 * scale, y - 0.17 * scale,
    )
    dudraw.set_pen_color_rgb(217, 188, 76)
    dudraw.line(x - 0.17 * scale, y + 0.06 * scale, x + 0.2 * scale, y + 0.06 * scale)
    dudraw.line(x - 0.02 * scale, y + 0.05 * scale, x + 0.11 * scale, y - 0.13 * scale)
    dudraw.set_pen_color_rgb(201, 209, 218)
    dudraw.line(x - 0.08 * scale, y - 0.1 * scale, x - 0.08 * scale, y + 0.25 * scale)
    dudraw.line(x + 0.03 * scale, y - 0.12 * scale, x + 0.03 * scale, y + 0.21 * scale)

    head_x = x
    head_y = y + 0.46 * scale
    dudraw.set_pen_color_rgb(224, 188, 148)
    dudraw.filled_circle(head_x, head_y, 0.13 * scale)
    dudraw.set_pen_color_rgb(241, 242, 238)
    dudraw.filled_circle(head_x - 0.09 * scale, head_y - 0.08 * scale, 0.08 * scale)
    dudraw.filled_circle(head_x + 0.01 * scale, head_y - 0.12 * scale, 0.1 * scale)
    dudraw.filled_circle(head_x + 0.1 * scale, head_y - 0.07 * scale, 0.07 * scale)
    dudraw.set_pen_color_rgb(232, 233, 228)
    dudraw.filled_circle(head_x, head_y + 0.12 * scale, 0.13 * scale)
    dudraw.set_pen_color_rgb(217, 188, 76)
    dudraw.filled_triangle(
        head_x - 0.14 * scale, head_y + 0.15 * scale,
        head_x - 0.07 * scale, head_y + 0.29 * scale,
        head_x, head_y + 0.17 * scale,
    )
    dudraw.filled_triangle(
        head_x, head_y + 0.17 * scale,
        head_x + 0.07 * scale, head_y + 0.3 * scale,
        head_x + 0.14 * scale, head_y + 0.15 * scale,
    )

    # His lifted arm carries a charged lightning bolt aimed into the lane.
    hand_x = x + 0.28 * scale
    hand_y = y + 0.48 * scale
    dudraw.set_pen_color_rgb(224, 188, 148)
    dudraw.line(x + 0.12 * scale, y + 0.3 * scale, hand_x, hand_y)
    dudraw.filled_circle(hand_x, hand_y, 0.045 * scale)
    bolt_x = hand_x + aim_x * 0.05 * scale
    bolt_y = hand_y + 0.06 * scale + aim_y * 0.05 * scale
    dudraw.set_pen_color_rgb(255, 232, 82)
    dudraw.filled_triangle(
        bolt_x - 0.04 * scale, bolt_y + 0.2 * scale,
        bolt_x + 0.1 * scale, bolt_y + 0.19 * scale,
        bolt_x, bolt_y + 0.03 * scale,
    )
    dudraw.filled_triangle(
        bolt_x, bolt_y + 0.03 * scale,
        bolt_x + 0.09 * scale, bolt_y + 0.04 * scale,
        bolt_x - 0.06 * scale, bolt_y - 0.18 * scale,
    )
    dudraw.set_pen_color_rgb(255, 248, 176)
    dudraw.line(bolt_x + 0.02 * scale, bolt_y + 0.16 * scale, bolt_x - 0.01 * scale, bolt_y - 0.08 * scale)
    dudraw.set_pen_color_rgb(255, 224, 88)
    dudraw.circle(hand_x, hand_y + 0.04 * scale, 0.16 * scale + pulse)


def draw_gold_vault_model(x, y, aim_x, aim_y, frame, scale):
    glint = 0.02 * math.sin(frame * 0.09) * scale

    # A small Greco-Roman treasury: marble stairs, columned facade and pediment.
    dudraw.set_pen_color_rgb(171, 178, 184)
    dudraw.filled_rectangle(x, y - 0.29 * scale, 0.43 * scale, 0.045 * scale)
    dudraw.set_pen_color_rgb(204, 211, 216)
    dudraw.filled_rectangle(x, y - 0.22 * scale, 0.37 * scale, 0.04 * scale)
    dudraw.set_pen_color_rgb(238, 241, 239)
    dudraw.filled_rectangle(x, y - 0.15 * scale, 0.31 * scale, 0.04 * scale)
    dudraw.set_pen_color_rgb(193, 202, 208)
    dudraw.filled_triangle(
        x - 0.34 * scale, y - 0.1 * scale,
        x + 0.34 * scale, y - 0.1 * scale,
        x + 0.4 * scale, y + 0.03 * scale,
    )
    dudraw.set_pen_color_rgb(249, 249, 245)
    dudraw.filled_rectangle(x, y + 0.22 * scale, 0.33 * scale, 0.31 * scale)
    dudraw.set_pen_color_rgb(212, 220, 225)
    dudraw.filled_triangle(
        x + 0.33 * scale, y - 0.09 * scale,
        x + 0.42 * scale, y + 0.02 * scale,
        x + 0.42 * scale, y + 0.48 * scale,
    )
    dudraw.filled_triangle(
        x + 0.33 * scale, y - 0.09 * scale,
        x + 0.42 * scale, y + 0.48 * scale,
        x + 0.33 * scale, y + 0.53 * scale,
    )

    for pillar_x in (-0.25, -0.09, 0.09, 0.25):
        dudraw.set_pen_color_rgb(224, 229, 230)
        dudraw.filled_rectangle(x + pillar_x * scale, y + 0.2 * scale, 0.04 * scale, 0.25 * scale)
        dudraw.set_pen_color_rgb(255, 255, 252)
        dudraw.line(x + (pillar_x - 0.018) * scale, y - 0.04 * scale, x + (pillar_x - 0.018) * scale, y + 0.43 * scale)
        dudraw.set_pen_color_rgb(186, 195, 201)
        dudraw.filled_rectangle(x + pillar_x * scale, y - 0.05 * scale, 0.06 * scale, 0.025 * scale)
        dudraw.filled_rectangle(x + pillar_x * scale, y + 0.46 * scale, 0.06 * scale, 0.025 * scale)

    dudraw.set_pen_color_rgb(82, 91, 105)
    dudraw.filled_rectangle(x, y + 0.08 * scale, 0.075 * scale, 0.15 * scale)
    dudraw.set_pen_color_rgb(215, 173, 63)
    dudraw.circle(x, y + 0.1 * scale, 0.032 * scale)
    dudraw.set_pen_color_rgb(239, 242, 240)
    dudraw.filled_triangle(
        x - 0.39 * scale, y + 0.5 * scale,
        x + 0.39 * scale, y + 0.5 * scale,
        x, y + 0.78 * scale,
    )
    dudraw.set_pen_color_rgb(196, 203, 208)
    dudraw.line(x - 0.4 * scale, y + 0.5 * scale, x + 0.4 * scale, y + 0.5 * scale)

    # Gold coin crest with a small dollar mark sits high on the front pediment.
    logo_y = y + 0.58 * scale
    dudraw.set_pen_color_rgb(188, 139, 35)
    dudraw.filled_circle(x, logo_y, (0.092 * scale) + glint)
    dudraw.set_pen_color_rgb(251, 209, 75)
    dudraw.filled_circle(x, logo_y, 0.068 * scale)
    dudraw.set_pen_color_rgb(139, 100, 27)
    dudraw.line(x, logo_y - 0.045 * scale, x, logo_y + 0.045 * scale)
    dudraw.line(x - 0.03 * scale, logo_y + 0.025 * scale, x + 0.029 * scale, logo_y + 0.025 * scale)
    dudraw.line(x - 0.03 * scale, logo_y - 0.025 * scale, x + 0.029 * scale, logo_y - 0.025 * scale)
    dudraw.line(x - 0.03 * scale, logo_y + 0.025 * scale, x + 0.029 * scale, logo_y - 0.025 * scale)


def draw_life_tree_model(x, y, aim_x, aim_y, frame, scale):
    sway = math.sin(frame * 0.045 + x) * 0.018 * scale
    glow = 0.012 * math.sin(frame * 0.12) * scale

    # Curling roots and an aged split trunk ground the healing landmark.
    dudraw.set_pen_color_rgb(62, 45, 29)
    dudraw.filled_ellipse(x, y - 0.29 * scale, 0.43 * scale, 0.09 * scale)
    dudraw.set_pen_color_rgb(97, 65, 36)
    dudraw.filled_triangle(
        x - 0.2 * scale, y - 0.28 * scale,
        x - 0.08 * scale, y + 0.42 * scale,
        x + 0.09 * scale, y + 0.42 * scale,
    )
    dudraw.filled_triangle(
        x - 0.2 * scale, y - 0.28 * scale,
        x + 0.09 * scale, y + 0.42 * scale,
        x + 0.2 * scale, y - 0.28 * scale,
    )
    dudraw.set_pen_color_rgb(140, 89, 44)
    dudraw.line(x - 0.07 * scale, y - 0.2 * scale, x - 0.04 * scale, y + 0.38 * scale)
    dudraw.line(x + 0.02 * scale, y + 0.14 * scale, x + 0.31 * scale, y + 0.46 * scale)
    dudraw.line(x - 0.03 * scale, y + 0.22 * scale, x - 0.3 * scale, y + 0.47 * scale)
    dudraw.set_pen_color_rgb(116, 76, 40)
    dudraw.line(x - 0.14 * scale, y - 0.23 * scale, x - 0.4 * scale, y - 0.3 * scale)
    dudraw.line(x + 0.14 * scale, y - 0.23 * scale, x + 0.4 * scale, y - 0.3 * scale)

    # Layered rounded canopy forms a lush heart orchard silhouette.
    dudraw.set_pen_color_rgb(36, 91, 51)
    for leaf_x, leaf_y, radius in (
        (-0.34, 0.43, 0.18), (-0.16, 0.58, 0.22), (0.06, 0.64, 0.23),
        (0.29, 0.51, 0.2), (-0.42, 0.28, 0.13), (0.4, 0.32, 0.14),
        (-0.08, 0.37, 0.21), (0.2, 0.37, 0.18),
    ):
        dudraw.filled_circle(x + leaf_x * scale, y + leaf_y * scale + sway, radius * scale)
    dudraw.set_pen_color_rgb(67, 139, 67)
    dudraw.filled_circle(x - 0.2 * scale, y + 0.63 * scale + sway, 0.11 * scale)
    dudraw.filled_circle(x + 0.15 * scale, y + 0.68 * scale + sway, 0.12 * scale)
    dudraw.filled_circle(x + 0.36 * scale, y + 0.45 * scale + sway, 0.08 * scale)

    # Heart apples hang beneath the crown as the tree's life-giving fruit.
    for fruit_x, fruit_y, fruit_scale in ((-0.25, 0.42, 0.08), (0.02, 0.47, 0.1), (0.27, 0.37, 0.075)):
        center_x = x + fruit_x * scale
        center_y = y + fruit_y * scale + sway
        dudraw.set_pen_color_rgb(89, 54, 30)
        dudraw.line(center_x, center_y + 0.07 * scale, center_x, center_y + 0.13 * scale)
        dudraw.set_pen_color_rgb(216, 54, 76)
        dudraw.filled_circle(center_x - fruit_scale * 0.45 * scale, center_y + fruit_scale * 0.28 * scale, fruit_scale * 0.58 * scale + glow)
        dudraw.filled_circle(center_x + fruit_scale * 0.45 * scale, center_y + fruit_scale * 0.28 * scale, fruit_scale * 0.58 * scale + glow)
        dudraw.filled_triangle(
            center_x - fruit_scale * scale, center_y + fruit_scale * 0.25 * scale,
            center_x + fruit_scale * scale, center_y + fruit_scale * 0.25 * scale,
            center_x, center_y - fruit_scale * 1.05 * scale,
        )
        dudraw.set_pen_color_rgb(255, 141, 150)
        dudraw.filled_circle(center_x - fruit_scale * 0.3 * scale, center_y + fruit_scale * 0.46 * scale, fruit_scale * 0.17 * scale)


def draw_meteor_model(x, y, aim_x, aim_y, frame, scale):
    pulse = math.sin(frame * 0.16) * 0.025 * scale
    smoke_drift = math.sin(frame * 0.045) * 0.04 * scale

    # A broken volcanic cone carries exposed molten channels up to its crater.
    dudraw.set_pen_color_rgb(40, 35, 34)
    dudraw.filled_ellipse(x, y - 0.29 * scale, 0.44 * scale, 0.09 * scale)
    dudraw.set_pen_color_rgb(53, 46, 44)
    dudraw.filled_triangle(
        x - 0.42 * scale, y - 0.28 * scale,
        x - 0.16 * scale, y + 0.43 * scale,
        x + 0.13 * scale, y + 0.43 * scale,
    )
    dudraw.filled_triangle(
        x - 0.42 * scale, y - 0.28 * scale,
        x + 0.13 * scale, y + 0.43 * scale,
        x + 0.42 * scale, y - 0.28 * scale,
    )
    dudraw.set_pen_color_rgb(82, 66, 58)
    dudraw.filled_triangle(
        x + 0.13 * scale, y + 0.43 * scale,
        x + 0.25 * scale, y + 0.34 * scale,
        x + 0.42 * scale, y - 0.28 * scale,
    )
    dudraw.set_pen_color_rgb(96, 75, 63)
    dudraw.line(x - 0.32 * scale, y - 0.2 * scale, x - 0.17 * scale, y + 0.23 * scale)
    dudraw.line(x + 0.31 * scale, y - 0.2 * scale, x + 0.16 * scale, y + 0.28 * scale)
    dudraw.set_pen_color_rgb(221, 63, 33)
    dudraw.line(x - 0.1 * scale, y - 0.22 * scale, x - 0.03 * scale, y + 0.3 * scale)
    dudraw.line(x + 0.16 * scale, y - 0.18 * scale, x + 0.07 * scale, y + 0.18 * scale)
    dudraw.set_pen_color_rgb(255, 133, 37)
    dudraw.line(x - 0.07 * scale, y - 0.16 * scale, x - 0.02 * scale, y + 0.25 * scale)

    crater_y = y + 0.39 * scale
    dudraw.set_pen_color_rgb(29, 27, 28)
    dudraw.filled_ellipse(x - 0.01 * scale, crater_y, 0.18 * scale, 0.07 * scale)
    dudraw.set_pen_color_rgb(245, 74, 32)
    dudraw.filled_ellipse(x - 0.01 * scale, crater_y + 0.008 * scale, 0.13 * scale + pulse, 0.045 * scale)
    dudraw.set_pen_color_rgb(255, 193, 55)
    dudraw.filled_ellipse(x - 0.03 * scale, crater_y + 0.018 * scale, 0.07 * scale, 0.025 * scale)

    # Smoke and a suspended lava bomb make the eruption readable before firing.
    dudraw.set_pen_color_rgb(92, 87, 88)
    dudraw.filled_circle(x + smoke_drift - 0.07 * scale, y + 0.55 * scale, 0.07 * scale)
    dudraw.set_pen_color_rgb(119, 113, 112)
    dudraw.filled_circle(x + smoke_drift + 0.02 * scale, y + 0.64 * scale, 0.08 * scale)
    dudraw.set_pen_color_rgb(64, 56, 52)
    dudraw.filled_circle(x + aim_x * 0.16 * scale, y + 0.57 * scale + aim_y * 0.08 * scale, 0.075 * scale)
    dudraw.set_pen_color_rgb(247, 81, 31)
    dudraw.filled_circle(x + aim_x * 0.16 * scale, y + 0.57 * scale + aim_y * 0.08 * scale, 0.05 * scale)
    dudraw.set_pen_color_rgb(255, 196, 57)
    dudraw.filled_circle(x + aim_x * 0.14 * scale - 0.015 * scale, y + 0.6 * scale + aim_y * 0.08 * scale, 0.017 * scale)


def draw_oracle_model(x, y, aim_x, aim_y, frame, scale):
    shimmer = math.sin(frame * 0.1) * 0.018 * scale
    lens_x = x - 0.05 * scale
    lens_y = y + 0.34 * scale

    # A ceremonial stand holds a huge search lens above the battlefield.
    dudraw.set_pen_color_rgb(53, 42, 70)
    dudraw.filled_ellipse(x, y - 0.28 * scale, 0.34 * scale, 0.08 * scale)
    dudraw.set_pen_color_rgb(120, 87, 47)
    dudraw.filled_triangle(
        x - 0.19 * scale, y - 0.26 * scale,
        x + 0.19 * scale, y - 0.26 * scale,
        x + 0.11 * scale, y - 0.16 * scale,
    )
    dudraw.filled_triangle(
        x - 0.19 * scale, y - 0.26 * scale,
        x + 0.11 * scale, y - 0.16 * scale,
        x - 0.11 * scale, y - 0.16 * scale,
    )
    dudraw.set_pen_color_rgb(210, 159, 68)
    dudraw.line(x - 0.15 * scale, y - 0.15 * scale, x + 0.08 * scale, y + 0.16 * scale)
    dudraw.set_pen_color_rgb(91, 64, 37)
    dudraw.line(x - 0.12 * scale, y - 0.18 * scale, x - 0.32 * scale, y - 0.28 * scale)
    dudraw.line(x + 0.1 * scale, y - 0.18 * scale, x + 0.3 * scale, y - 0.28 * scale)

    # The oversize lens tilts forward with a jeweled rim and visible glass face.
    dudraw.set_pen_color_rgb(91, 60, 123)
    dudraw.filled_circle(lens_x, lens_y, 0.4 * scale)
    dudraw.set_pen_color_rgb(231, 189, 75)
    dudraw.filled_circle(lens_x, lens_y, 0.355 * scale)
    dudraw.set_pen_color_rgb(100, 158, 194)
    dudraw.filled_circle(lens_x, lens_y, 0.305 * scale)
    dudraw.set_pen_color_rgb(163, 214, 235)
    dudraw.filled_circle(lens_x - 0.02 * scale, lens_y + 0.015 * scale, 0.27 * scale)
    dudraw.set_pen_color_rgb(216, 245, 254)
    dudraw.line(lens_x - 0.18 * scale, lens_y + 0.13 * scale, lens_x - 0.04 * scale, lens_y + 0.24 * scale)
    dudraw.line(lens_x - 0.21 * scale, lens_y + 0.05 * scale, lens_x - 0.12 * scale, lens_y + 0.12 * scale)
    dudraw.set_pen_color_rgb(250, 218, 105)
    dudraw.circle(lens_x, lens_y, 0.36 * scale + shimmer)

    handle_start_x = lens_x + 0.23 * scale
    handle_start_y = lens_y - 0.23 * scale
    dudraw.set_pen_color_rgb(99, 66, 39)
    dudraw.line(handle_start_x, handle_start_y, x + 0.43 * scale, y - 0.11 * scale)
    dudraw.set_pen_color_rgb(193, 133, 52)
    dudraw.line(handle_start_x + 0.025 * scale, handle_start_y + 0.02 * scale, x + 0.45 * scale, y - 0.09 * scale)

    focus_x = lens_x
    focus_y = lens_y
    dudraw.set_pen_color_rgb(255, 248, 178)
    dudraw.filled_circle(focus_x, focus_y, 0.045 * scale + shimmer)
    dudraw.set_pen_color_rgb(255, 221, 94)
    dudraw.circle(focus_x, focus_y, 0.095 * scale)


def draw_time_spire_model(x, y, aim_x, aim_y, frame, scale):
    now = datetime.now()
    seconds = now.second + now.microsecond / 1000000
    minutes = now.minute + seconds / 60
    hours = (now.hour % 12) + minutes / 60
    second_angle = math.pi / 2 - seconds * 2 * math.pi / 60
    minute_angle = math.pi / 2 - minutes * 2 * math.pi / 60
    hour_angle = math.pi / 2 - hours * 2 * math.pi / 12
    center_y = y + 0.36 * scale
    pulse = 0.012 * math.sin(frame * 0.12) * scale

    # Stone-and-brass monument holding an enormous working clock face.
    dudraw.set_pen_color_rgb(39, 53, 66)
    dudraw.filled_ellipse(x, y - 0.29 * scale, 0.39 * scale, 0.08 * scale)
    dudraw.set_pen_color_rgb(70, 97, 108)
    dudraw.filled_triangle(
        x - 0.32 * scale, y - 0.27 * scale,
        x + 0.32 * scale, y - 0.27 * scale,
        x + 0.25 * scale, y - 0.14 * scale,
    )
    dudraw.filled_triangle(
        x - 0.32 * scale, y - 0.27 * scale,
        x + 0.25 * scale, y - 0.14 * scale,
        x - 0.25 * scale, y - 0.14 * scale,
    )
    dudraw.set_pen_color_rgb(112, 143, 151)
    dudraw.filled_rectangle(x, y + 0.03 * scale, 0.18 * scale, 0.18 * scale)
    dudraw.set_pen_color_rgb(186, 157, 67)
    dudraw.line(x - 0.19 * scale, y - 0.12 * scale, x + 0.19 * scale, y - 0.12 * scale)
    dudraw.line(x - 0.13 * scale, y + 0.2 * scale, x + 0.13 * scale, y + 0.2 * scale)

    dudraw.set_pen_color_rgb(37, 51, 63)
    dudraw.filled_circle(x, center_y, 0.39 * scale)
    dudraw.set_pen_color_rgb(205, 171, 74)
    dudraw.filled_circle(x, center_y, 0.355 * scale)
    dudraw.set_pen_color_rgb(238, 244, 240)
    dudraw.filled_circle(x, center_y, 0.31 * scale)
    dudraw.set_pen_color_rgb(204, 223, 221)
    dudraw.circle(x, center_y, 0.28 * scale)

    for mark in range(12):
        angle = math.pi / 2 - mark * math.pi / 6
        inner = 0.246 if mark % 3 else 0.225
        dudraw.set_pen_color_rgb(65, 82, 90)
        dudraw.line(
            x + math.cos(angle) * inner * scale,
            center_y + math.sin(angle) * inner * scale,
            x + math.cos(angle) * 0.275 * scale,
            center_y + math.sin(angle) * 0.275 * scale,
        )

    dudraw.set_pen_color_rgb(49, 62, 70)
    dudraw.line(x, center_y, x + math.cos(hour_angle) * 0.16 * scale, center_y + math.sin(hour_angle) * 0.16 * scale)
    dudraw.set_pen_color_rgb(53, 108, 119)
    dudraw.line(x, center_y, x + math.cos(minute_angle) * 0.235 * scale, center_y + math.sin(minute_angle) * 0.235 * scale)
    dudraw.set_pen_color_rgb(209, 55, 57)
    dudraw.line(x, center_y, x + math.cos(second_angle) * 0.265 * scale, center_y + math.sin(second_angle) * 0.265 * scale)
    dudraw.set_pen_color_rgb(231, 190, 79)
    dudraw.filled_circle(x, center_y, 0.04 * scale + pulse)
    dudraw.circle(x, center_y, 0.075 * scale)


def draw_thornheart_model(x, y, aim_x, aim_y, frame, scale):
    pulse = math.sin(frame * 0.14) * 0.018 * scale

    # A broad tangled bramble mound keeps its heart protected behind hooked vines.
    dudraw.set_pen_color_rgb(35, 56, 34)
    dudraw.filled_ellipse(x, y - 0.27 * scale, 0.46 * scale, 0.11 * scale)
    for vine_start, vine_end, bend in (
        ((-0.4, -0.22), (-0.25, 0.39), (-0.45, 0.14)),
        ((-0.24, -0.25), (0.02, 0.52), (-0.11, 0.28)),
        ((0.01, -0.27), (0.34, 0.44), (0.16, 0.25)),
        ((0.23, -0.23), (0.45, 0.2), (0.39, -0.02)),
        ((-0.34, 0.04), (0.38, 0.1), (0.0, 0.34)),
    ):
        dudraw.set_pen_color_rgb(47, 105, 52)
        dudraw.line(x + vine_start[0] * scale, y + vine_start[1] * scale, x + bend[0] * scale, y + bend[1] * scale)
        dudraw.line(x + bend[0] * scale, y + bend[1] * scale, x + vine_end[0] * scale, y + vine_end[1] * scale)
        dudraw.set_pen_color_rgb(83, 155, 66)
        dudraw.filled_circle(x + vine_end[0] * scale, y + vine_end[1] * scale, 0.04 * scale)

    dudraw.set_pen_color_rgb(66, 126, 54)
    for leaf_x, leaf_y in ((-0.34, 0.25), (-0.16, 0.42), (0.18, 0.43), (0.34, 0.24), (-0.4, -0.02), (0.4, 0.04)):
        dudraw.filled_circle(x + leaf_x * scale, y + leaf_y * scale, 0.1 * scale)
    dudraw.set_pen_color_rgb(183, 196, 88)
    for thorn_x, thorn_y, turn in ((-0.32, 0.12, -1), (-0.12, 0.42, 1), (0.18, 0.34, -1), (0.33, 0.13, 1), (-0.22, -0.05, -1), (0.25, -0.02, 1)):
        dudraw.filled_triangle(
            x + thorn_x * scale, y + thorn_y * scale,
            x + (thorn_x + 0.095 * turn) * scale, y + (thorn_y + 0.07) * scale,
            x + (thorn_x + 0.02 * turn) * scale, y + (thorn_y - 0.01) * scale,
        )

    # The living heart supplies poison to each extending thorn lash.
    heart_y = y + 0.13 * scale
    dudraw.set_pen_color_rgb(108, 26, 45)
    dudraw.filled_circle(x - 0.065 * scale, heart_y + 0.045 * scale, 0.095 * scale + pulse)
    dudraw.filled_circle(x + 0.065 * scale, heart_y + 0.045 * scale, 0.095 * scale + pulse)
    dudraw.filled_triangle(
        x - 0.16 * scale, heart_y + 0.04 * scale,
        x + 0.16 * scale, heart_y + 0.04 * scale,
        x, heart_y - 0.17 * scale,
    )
    dudraw.set_pen_color_rgb(235, 67, 86)
    dudraw.line(x - 0.05 * scale, heart_y + 0.06 * scale, x + 0.04 * scale, heart_y - 0.05 * scale)
    dudraw.set_pen_color_rgb(253, 127, 132)
    dudraw.filled_circle(x - 0.06 * scale, heart_y + 0.08 * scale, 0.026 * scale)


def draw_royal_mint_model(x, y, aim_x, aim_y, frame, scale):
    spin = frame * 0.08
    smoke = math.sin(frame * 0.05) * 0.03 * scale

    # An industrial coin foundry contrasts the Treasury's clean marble facade.
    dudraw.set_pen_color_rgb(58, 52, 47)
    dudraw.filled_ellipse(x, y - 0.28 * scale, 0.43 * scale, 0.09 * scale)
    dudraw.set_pen_color_rgb(127, 75, 43)
    dudraw.filled_rectangle(x, y + 0.08 * scale, 0.35 * scale, 0.34 * scale)
    dudraw.set_pen_color_rgb(171, 99, 50)
    for brick_y in (-0.16, 0.02, 0.2):
        dudraw.line(x - 0.32 * scale, y + brick_y * scale, x + 0.32 * scale, y + brick_y * scale)
    dudraw.set_pen_color_rgb(73, 62, 54)
    dudraw.filled_rectangle(x - 0.18 * scale, y + 0.22 * scale, 0.09 * scale, 0.32 * scale)
    dudraw.set_pen_color_rgb(188, 113, 51)
    dudraw.filled_rectangle(x - 0.18 * scale, y + 0.55 * scale, 0.115 * scale, 0.025 * scale)
    dudraw.set_pen_color_rgb(102, 96, 92)
    dudraw.filled_circle(x - 0.19 * scale + smoke, y + 0.7 * scale, 0.075 * scale)
    dudraw.filled_circle(x - 0.13 * scale + smoke, y + 0.81 * scale, 0.09 * scale)

    # Copper roof and glowing press window establish the production building.
    dudraw.set_pen_color_rgb(92, 58, 40)
    dudraw.filled_triangle(
        x - 0.43 * scale, y + 0.37 * scale,
        x + 0.43 * scale, y + 0.37 * scale,
        x, y + 0.67 * scale,
    )
    dudraw.set_pen_color_rgb(208, 128, 54)
    dudraw.line(x - 0.38 * scale, y + 0.4 * scale, x + 0.37 * scale, y + 0.4 * scale)
    dudraw.set_pen_color_rgb(49, 42, 39)
    dudraw.filled_rectangle(x + 0.1 * scale, y + 0.1 * scale, 0.12 * scale, 0.16 * scale)
    dudraw.set_pen_color_rgb(253, 156, 44)
    dudraw.filled_rectangle(x + 0.1 * scale, y + 0.1 * scale, 0.075 * scale, 0.11 * scale)
    dudraw.set_pen_color_rgb(255, 224, 93)
    dudraw.filled_circle(x + 0.08 * scale, y + 0.12 * scale, 0.033 * scale)

    # The turning press wheel stamps coins before feeding them down a chute.
    gear_x = x - 0.11 * scale
    gear_y = y + 0.12 * scale
    dudraw.set_pen_color_rgb(102, 69, 37)
    dudraw.filled_circle(gear_x, gear_y, 0.15 * scale)
    dudraw.set_pen_color_rgb(225, 169, 55)
    dudraw.circle(gear_x, gear_y, 0.13 * scale)
    for tooth in range(8):
        angle = spin + tooth * math.pi / 4
        dudraw.line(
            gear_x + math.cos(angle) * 0.11 * scale,
            gear_y + math.sin(angle) * 0.11 * scale,
            gear_x + math.cos(angle) * 0.17 * scale,
            gear_y + math.sin(angle) * 0.17 * scale,
        )
    dudraw.set_pen_color_rgb(249, 205, 79)
    dudraw.filled_circle(gear_x, gear_y, 0.055 * scale)
    dudraw.set_pen_color_rgb(91, 62, 40)
    dudraw.line(x + 0.12 * scale, y - 0.06 * scale, x + 0.33 * scale, y - 0.17 * scale)
    dudraw.set_pen_color_rgb(245, 195, 62)
    dudraw.filled_circle(x + 0.3 * scale, y - 0.15 * scale, 0.047 * scale)
    dudraw.filled_circle(x + 0.38 * scale, y - 0.2 * scale, 0.04 * scale)


def draw_guardian_model(x, y, aim_x, aim_y, frame, scale):
    flicker = 0.012 * math.sin(frame * 0.14) * scale

    # Gothic stone posts and wrought iron form a gate directly across the road.
    dudraw.set_pen_color_rgb(39, 43, 48)
    dudraw.filled_ellipse(x, y - 0.29 * scale, 0.49 * scale, 0.075 * scale)
    for post_x in (-0.39, 0.39):
        dudraw.set_pen_color_rgb(61, 64, 70)
        dudraw.filled_rectangle(x + post_x * scale, y + 0.12 * scale, 0.095 * scale, 0.43 * scale)
        dudraw.set_pen_color_rgb(104, 108, 113)
        dudraw.filled_rectangle(x + post_x * scale, y - 0.27 * scale, 0.12 * scale, 0.045 * scale)
        dudraw.filled_rectangle(x + post_x * scale, y + 0.56 * scale, 0.12 * scale, 0.04 * scale)
        dudraw.set_pen_color_rgb(36, 38, 44)
        dudraw.filled_triangle(
            x + (post_x - 0.14) * scale, y + 0.59 * scale,
            x + (post_x + 0.14) * scale, y + 0.59 * scale,
            x + post_x * scale, y + 0.78 * scale,
        )

    dudraw.set_pen_color_rgb(25, 29, 35)
    dudraw.line(x - 0.29 * scale, y - 0.22 * scale, x - 0.29 * scale, y + 0.45 * scale)
    dudraw.line(x + 0.29 * scale, y - 0.22 * scale, x + 0.29 * scale, y + 0.45 * scale)
    dudraw.line(x - 0.29 * scale, y + 0.45 * scale, x, y + 0.64 * scale)
    dudraw.line(x, y + 0.64 * scale, x + 0.29 * scale, y + 0.45 * scale)
    dudraw.line(x - 0.29 * scale, y - 0.12 * scale, x + 0.29 * scale, y - 0.12 * scale)
    for bar_x in (-0.2, -0.1, 0.0, 0.1, 0.2):
        top_y = 0.57 - abs(bar_x) * 0.55
        dudraw.line(x + bar_x * scale, y - 0.18 * scale, x + bar_x * scale, y + top_y * scale)
        dudraw.filled_triangle(
            x + (bar_x - 0.035) * scale, y + top_y * scale,
            x + (bar_x + 0.035) * scale, y + top_y * scale,
            x + bar_x * scale, y + (top_y + 0.11) * scale,
        )
    dudraw.set_pen_color_rgb(92, 100, 112)
    dudraw.line(x - 0.27 * scale, y + 0.05 * scale, x + 0.27 * scale, y + 0.33 * scale)
    dudraw.line(x - 0.27 * scale, y + 0.33 * scale, x + 0.27 * scale, y + 0.05 * scale)

    # A cold lock-glow gives the gate its haunted defensive presence.
    dudraw.set_pen_color_rgb(151, 190, 213)
    dudraw.filled_rectangle(x, y + 0.12 * scale, 0.055 * scale, 0.065 * scale)
    dudraw.circle(x, y + 0.22 * scale, 0.06 * scale + flicker)
    dudraw.set_pen_color_rgb(218, 244, 249)
    dudraw.filled_circle(x, y + 0.22 * scale, 0.022 * scale)


def draw_starfall_model(x, y, aim_x, aim_y, frame, scale):
    turn = frame * 0.04
    pulse = 0.015 * math.sin(frame * 0.12)

    # An obsidian rooftop observatory supports a suspended celestial prism.
    dudraw.set_pen_color_rgb(29, 30, 49)
    dudraw.filled_ellipse(x, y - 0.3 * scale, 0.46 * scale, 0.1 * scale)
    dudraw.set_pen_color_rgb(45, 44, 70)
    dudraw.filled_rectangle(x, y - 0.17 * scale, 0.3 * scale, 0.17 * scale)
    dudraw.set_pen_color_rgb(69, 65, 99)
    dudraw.filled_triangle(
        x - 0.38 * scale, y - 0.06 * scale,
        x + 0.38 * scale, y - 0.06 * scale,
        x, y + 0.18 * scale,
    )
    dudraw.set_pen_color_rgb(188, 140, 56)
    dudraw.rectangle(x, y + 0.06 * scale, 0.29 * scale, 0.08 * scale)
    dudraw.line(x - 0.21 * scale, y + 0.1 * scale, x - 0.13 * scale, y + 0.46 * scale)
    dudraw.line(x + 0.21 * scale, y + 0.1 * scale, x + 0.13 * scale, y + 0.46 * scale)

    # Thin astrolabe rings turn around the crystal and catch the night sky.
    ring_y = y + 0.46 * scale
    dudraw.set_pen_color_rgb(205, 157, 64)
    dudraw.ellipse(x, ring_y, (0.31 + pulse) * scale, 0.13 * scale)
    dudraw.ellipse(x, ring_y, 0.14 * scale, 0.31 * scale)
    ring_x = x + math.cos(turn) * 0.3 * scale
    ring_dot_y = ring_y + math.sin(turn) * 0.13 * scale
    dudraw.filled_circle(ring_x, ring_dot_y, 0.035 * scale)
    dudraw.set_pen_color_rgb(219, 232, 255)
    dudraw.filled_circle(x - 0.27 * scale, y + 0.69 * scale, 0.025 * scale)
    dudraw.filled_circle(x + 0.3 * scale, y + 0.76 * scale, 0.018 * scale)

    # A luminous triangular prism breaks starlight into colored facets.
    dudraw.set_pen_color_rgb(117, 101, 203)
    dudraw.filled_triangle(
        x, y + 0.77 * scale,
        x - 0.14 * scale, y + 0.39 * scale,
        x + 0.15 * scale, y + 0.39 * scale,
    )
    dudraw.set_pen_color_rgb(115, 212, 239)
    dudraw.filled_triangle(
        x, y + 0.77 * scale,
        x, y + 0.39 * scale,
        x + 0.15 * scale, y + 0.39 * scale,
    )
    dudraw.set_pen_color_rgb(245, 142, 220)
    dudraw.line(x, y + 0.76 * scale, x - 0.13 * scale, y + 0.4 * scale)
    dudraw.set_pen_color_rgb(255, 250, 205)
    dudraw.filled_circle(x + 0.02 * scale, y + 0.56 * scale, (0.035 + pulse) * scale)


def draw_special_model(x, y, tower_type, aim_x, aim_y, frame, scale):
    stats = get_tower_stats(tower_type)
    base = stats["color"]
    draw_gem(x, y + 0.08 * scale, brighten(base, 25), 1.6 * scale)

    if tower_type == "starfall":
        dudraw.set_pen_color_rgb(35, 29, 55)
        dudraw.filled_triangle(x - 0.28 * scale, y - 0.18 * scale, x, y + 0.55 * scale, x + 0.28 * scale, y - 0.18 * scale)
        draw_arcane_orbits(x, y + 0.1 * scale, base, frame, 0.45, 5, scale)
    else:
        draw_arcane_orbits(x, y + 0.08 * scale, base, frame, 0.48, 6, scale)


def draw_tower_body(x, y, tower_type, aim_x, aim_y, frame, scale=1.0):
    if tower_type == "arrow":
        draw_arrow_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "cannon":
        draw_cannon_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "frost":
        draw_frost_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "sniper":
        draw_sniper_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "laser":
        draw_laser_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "mortar":
        draw_mortar_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "venom":
        draw_venom_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "storm":
        draw_storm_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "titan":
        draw_titan_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "gold_vault":
        draw_gold_vault_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "life_tree":
        draw_life_tree_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "meteor":
        draw_meteor_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "oracle":
        draw_oracle_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "time_spire":
        draw_time_spire_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "thornheart":
        draw_thornheart_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "royal_mint":
        draw_royal_mint_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "guardian":
        draw_guardian_model(x, y, aim_x, aim_y, frame, scale)
    elif tower_type == "starfall":
        draw_starfall_model(x, y, aim_x, aim_y, frame, scale)
    else:
        draw_special_model(x, y, tower_type, aim_x, aim_y, frame, scale)


def draw_upgrade_marks(tower, frame):
    if tower.level <= 1:
        return

    dudraw.set_pen_color_rgb(255, 239, 125)
    for i in range(tower.level):
        angle = frame * 0.05 + i * 2 * math.pi / tower.level
        dudraw.filled_triangle(
            tower.x + math.cos(angle) * 0.5,
            tower.y + math.sin(angle) * 0.42,
            tower.x + math.cos(angle + 0.18) * 0.43,
            tower.y + math.sin(angle + 0.18) * 0.36,
            tower.x + math.cos(angle - 0.18) * 0.43,
            tower.y + math.sin(angle - 0.18) * 0.36,
        )


def draw_thornheart_range(tower):
    dudraw.set_pen_color_rgb(95, 188, 83)
    dudraw.circle(tower.x, tower.y, tower.range)
    for angle in (0, math.pi / 2, math.pi, math.pi * 1.5):
        marker_x = tower.x + math.cos(angle) * tower.range
        marker_y = tower.y + math.sin(angle) * tower.range
        dudraw.filled_triangle(
            marker_x,
            marker_y,
            marker_x - math.cos(angle - 0.45) * 0.13,
            marker_y - math.sin(angle - 0.45) * 0.13,
            marker_x - math.cos(angle + 0.45) * 0.13,
            marker_y - math.sin(angle + 0.45) * 0.13,
        )


def draw_towers(towers, settings, frame):
    for tower in sorted(towers, key=lambda placed_tower: placed_tower.y, reverse=True):
        if tower.tower_type == "thornheart" and tower.range > 0 and settings.get("show_range", True):
            draw_thornheart_range(tower)

        if is_ultra(settings):
            draw_pixel_tower(tower, frame)
            continue

        scale = 1.2 if tower.is_special else 1.0
        draw_shadow(tower.x, tower.y, scale)

        if tower.tower_type not in ("arrow", "cannon", "frost", "sniper", "laser", "mortar", "venom", "storm", "titan", "gold_vault", "life_tree", "meteor", "oracle", "time_spire", "thornheart", "royal_mint", "guardian", "starfall"):
            set_color(darken(tower.color, 34))
            dudraw.filled_circle(tower.x, tower.y - 0.17 * scale, 0.48 * scale)
            set_color(brighten(tower.color, 24))
            dudraw.circle(tower.x, tower.y - 0.17 * scale, 0.48 * scale)
            draw_plinth(tower.x, tower.y, tower.color, scale)
        draw_tower_body(tower.x, tower.y + 0.03, tower.tower_type, tower.aim_x, tower.aim_y, frame, scale)

        if is_amazing(settings):
            draw_upgrade_marks(tower, frame)
            set_color(brighten(tower.color, 55))
            dudraw.filled_circle(tower.x - 0.24 * scale, tower.y + 0.03 * scale, 0.028 * scale)


def draw_pixel_block(cx, cy, px, py, w, h, color):
    pixel = 1 / 32
    x = cx - 0.5 + (px + w / 2) * pixel
    y = cy - 0.5 + (py + h / 2) * pixel
    set_color(color)
    dudraw.filled_rectangle(x, y, w * pixel / 2, h * pixel / 2)


def draw_pixel_tower(tower, frame):
    base = tower.color
    light = brighten(base, 70)
    dark = darken(base, 60)
    cx = int(tower.x) + 0.5
    cy = int(tower.y) + 0.5

    if tower.is_special and tower.tower_type not in ("titan", "gold_vault", "life_tree", "meteor", "oracle", "time_spire", "thornheart", "royal_mint", "guardian", "starfall"):
        for i in range(8):
            angle = frame * 0.05 + i * math.pi / 4
            set_color(brighten(base, 75))
            dudraw.filled_square(cx + math.cos(angle) * 0.48, cy + math.sin(angle) * 0.48, 0.04)

    if tower.tower_type == "arrow":
        draw_pixel_block(cx, cy, 6, 3, 20, 3, (65, 42, 26))
        draw_pixel_block(cx, cy, 8, 5, 3, 11, (108, 66, 34))
        draw_pixel_block(cx, cy, 21, 5, 3, 11, (82, 49, 29))
        draw_pixel_block(cx, cy, 11, 8, 10, 2, (161, 102, 47))
        draw_pixel_block(cx, cy, 7, 15, 20, 3, (97, 55, 29))
        draw_pixel_block(cx, cy, 8, 18, 16, 4, (188, 125, 59))
        draw_pixel_block(cx, cy, 10, 22, 13, 6, (155, 96, 45))
        draw_pixel_block(cx, cy, 7, 28, 19, 2, (55, 76, 53))
        draw_pixel_block(cx, cy, 10, 30, 13, 2, (79, 106, 70))
        draw_pixel_block(cx, cy, 15, 23, 3, 3, (234, 215, 168))
        draw_pixel_block(cx, cy, 17, 24, 8, 1, (240, 225, 178))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 1, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "cannon":
        draw_pixel_block(cx, cy, 7, 8, 19, 3, (75, 46, 25))
        draw_pixel_block(cx, cy, 9, 11, 15, 4, (174, 110, 52))
        draw_pixel_block(cx, cy, 8, 8, 4, 4, (39, 43, 46))
        draw_pixel_block(cx, cy, 21, 9, 4, 4, (39, 43, 46))
        draw_pixel_block(cx, cy, 13, 14, 7, 4, (111, 71, 37))
        draw_pixel_block(cx, cy, 13, 17, 8, 7, (88, 98, 104))
        draw_pixel_block(cx, cy, 15, 18, 5, 5, (48, 53, 57))
        draw_pixel_block(cx, cy, 18, 20, 10, 4, (40, 45, 49))
        draw_pixel_block(cx, cy, 25, 20, 4, 4, (25, 29, 33))
        draw_pixel_block(cx, cy, 26, 21, 2, 2, (242, 130, 56))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 5, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "frost":
        draw_pixel_block(cx, cy, 8, 4, 17, 3, (63, 124, 158))
        draw_pixel_block(cx, cy, 10, 7, 13, 15, (82, 161, 197))
        draw_pixel_block(cx, cy, 20, 8, 4, 14, (112, 199, 225))
        draw_pixel_block(cx, cy, 14, 10, 4, 3, (213, 247, 255))
        draw_pixel_block(cx, cy, 14, 16, 4, 3, (213, 247, 255))
        draw_pixel_block(cx, cy, 7, 22, 20, 3, (215, 248, 255))
        draw_pixel_block(cx, cy, 11, 25, 12, 3, (70, 135, 194))
        draw_pixel_block(cx, cy, 14, 28, 5, 3, (235, 243, 247))
        draw_pixel_block(cx, cy, 12, 30, 9, 2, (103, 190, 233))
        draw_pixel_block(cx, cy, 20, 28, 3, 3, (208, 250, 255))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "sniper":
        draw_pixel_block(cx, cy, 6, 5, 21, 3, (39, 40, 48))
        draw_pixel_block(cx, cy, 8, 8, 17, 8, (60, 63, 72))
        draw_pixel_block(cx, cy, 10, 16, 13, 5, (92, 96, 104))
        draw_pixel_block(cx, cy, 8, 20, 16, 3, (120, 123, 130))
        draw_pixel_block(cx, cy, 8, 23, 12, 4, (53, 73, 62))
        draw_pixel_block(cx, cy, 7, 22, 4, 2, (35, 42, 39))
        draw_pixel_block(cx, cy, 18, 24, 4, 4, (215, 203, 179))
        draw_pixel_block(cx, cy, 17, 27, 5, 2, (43, 59, 50))
        draw_pixel_block(cx, cy, 19, 25, 12, 2, (22, 25, 31))
        draw_pixel_block(cx, cy, 24, 22, 1, 3, (62, 66, 73))
        draw_pixel_block(cx, cy, 29, 25, 2, 2, (255, 225, 148))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "laser":
        draw_pixel_block(cx, cy, 7, 4, 19, 2, (52, 59, 68))
        draw_pixel_block(cx, cy, 9, 6, 2, 16, (83, 94, 105))
        draw_pixel_block(cx, cy, 21, 6, 2, 16, (83, 94, 105))
        draw_pixel_block(cx, cy, 11, 10, 10, 2, (144, 155, 166))
        draw_pixel_block(cx, cy, 12, 15, 8, 2, (144, 155, 166))
        draw_pixel_block(cx, cy, 7, 21, 19, 2, (161, 172, 182))
        draw_pixel_block(cx, cy, 8, 18, 2, 3, (232, 220, 203))
        draw_pixel_block(cx, cy, 22, 18, 2, 3, (232, 220, 203))
        draw_pixel_block(cx, cy, 14, 23, 4, 3, (55, 62, 70))
        draw_pixel_block(cx, cy, 12, 26, 8, 5, (225, 37, 68))
        draw_pixel_block(cx, cy, 14, 28, 3, 2, (255, 181, 193))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "mortar":
        draw_pixel_block(cx, cy, 6, 6, 21, 3, (91, 74, 48))
        draw_pixel_block(cx, cy, 8, 9, 5, 3, (151, 124, 77))
        draw_pixel_block(cx, cy, 14, 8, 5, 3, (151, 124, 77))
        draw_pixel_block(cx, cy, 20, 10, 5, 3, (151, 124, 77))
        draw_pixel_block(cx, cy, 13, 12, 7, 4, (48, 56, 53))
        draw_pixel_block(cx, cy, 15, 16, 4, 10, (31, 36, 36))
        draw_pixel_block(cx, cy, 15, 25, 5, 3, (26, 30, 30))
        draw_pixel_block(cx, cy, 22, 15, 4, 6, (46, 55, 49))
        draw_pixel_block(cx, cy, 23, 20, 2, 3, (221, 159, 69))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 3, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "venom":
        draw_pixel_block(cx, cy, 6, 4, 21, 3, (57, 40, 24))
        draw_pixel_block(cx, cy, 12, 7, 9, 15, (91, 59, 30))
        draw_pixel_block(cx, cy, 8, 19, 19, 3, (104, 67, 33))
        draw_pixel_block(cx, cy, 4, 20, 8, 7, (38, 99, 47))
        draw_pixel_block(cx, cy, 10, 23, 9, 7, (50, 119, 52))
        draw_pixel_block(cx, cy, 18, 22, 10, 7, (39, 104, 47))
        draw_pixel_block(cx, cy, 22, 18, 7, 5, (59, 133, 52))
        draw_pixel_block(cx, cy, 8, 20, 15, 2, (81, 177, 54))
        draw_pixel_block(cx, cy, 18, 17, 3, 5, (81, 177, 54))
        draw_pixel_block(cx, cy, 18, 14, 6, 4, (76, 160, 45))
        draw_pixel_block(cx, cy, 23, 15, 2, 2, (244, 214, 67))
        draw_pixel_block(cx, cy, 25, 14, 4, 1, (235, 70, 78))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "storm":
        draw_pixel_block(cx, cy, 6, 5, 21, 3, (48, 53, 60))
        draw_pixel_block(cx, cy, 8, 8, 17, 4, (78, 89, 100))
        draw_pixel_block(cx, cy, 13, 11, 7, 4, (55, 73, 91))
        draw_pixel_block(cx, cy, 9, 12, 2, 10, (187, 117, 53))
        draw_pixel_block(cx, cy, 15, 13, 2, 11, (204, 131, 57))
        draw_pixel_block(cx, cy, 21, 12, 2, 10, (187, 117, 53))
        draw_pixel_block(cx, cy, 8, 23, 17, 5, (42, 48, 65))
        draw_pixel_block(cx, cy, 5, 24, 7, 4, (42, 48, 65))
        draw_pixel_block(cx, cy, 12, 27, 10, 4, (52, 59, 78))
        draw_pixel_block(cx, cy, 20, 24, 8, 5, (42, 48, 65))
        draw_pixel_block(cx, cy, 15, 20, 4, 5, (255, 238, 108))
        draw_pixel_block(cx, cy, 13, 17, 4, 4, (255, 238, 108))
        draw_pixel_block(cx, cy, 14, 14, 2, 3, (244, 251, 255))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "titan":
        draw_pixel_block(cx, cy, 4, 4, 24, 4, (194, 204, 216))
        draw_pixel_block(cx, cy, 7, 7, 19, 4, (232, 237, 242))
        draw_pixel_block(cx, cy, 10, 10, 13, 13, (247, 248, 245))
        draw_pixel_block(cx, cy, 12, 12, 10, 2, (215, 187, 75))
        draw_pixel_block(cx, cy, 13, 22, 7, 5, (224, 188, 148))
        draw_pixel_block(cx, cy, 12, 25, 9, 4, (237, 238, 232))
        draw_pixel_block(cx, cy, 12, 28, 2, 3, (217, 188, 76))
        draw_pixel_block(cx, cy, 18, 28, 2, 3, (217, 188, 76))
        draw_pixel_block(cx, cy, 20, 20, 5, 2, (224, 188, 148))
        draw_pixel_block(cx, cy, 24, 22, 2, 3, (224, 188, 148))
        draw_pixel_block(cx, cy, 25, 25, 4, 2, (255, 232, 82))
        draw_pixel_block(cx, cy, 24, 22, 3, 4, (255, 232, 82))
        draw_pixel_block(cx, cy, 23, 20, 3, 3, (255, 232, 82))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "gold_vault":
        draw_pixel_block(cx, cy, 4, 4, 24, 3, (174, 182, 188))
        draw_pixel_block(cx, cy, 6, 7, 20, 3, (210, 216, 220))
        draw_pixel_block(cx, cy, 8, 10, 16, 3, (239, 242, 240))
        draw_pixel_block(cx, cy, 7, 13, 19, 12, (248, 249, 246))
        draw_pixel_block(cx, cy, 9, 13, 2, 11, (221, 227, 228))
        draw_pixel_block(cx, cy, 13, 13, 2, 11, (221, 227, 228))
        draw_pixel_block(cx, cy, 18, 13, 2, 11, (221, 227, 228))
        draw_pixel_block(cx, cy, 22, 13, 2, 11, (221, 227, 228))
        draw_pixel_block(cx, cy, 14, 13, 5, 7, (80, 90, 103))
        draw_pixel_block(cx, cy, 6, 24, 21, 2, (233, 237, 236))
        draw_pixel_block(cx, cy, 9, 26, 15, 2, (233, 237, 236))
        draw_pixel_block(cx, cy, 12, 28, 9, 3, (233, 237, 236))
        draw_pixel_block(cx, cy, 14, 25, 5, 4, (236, 193, 61))
        draw_pixel_block(cx, cy, 15, 25, 3, 4, (252, 213, 77))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "life_tree":
        draw_pixel_block(cx, cy, 4, 4, 24, 3, (60, 43, 28))
        draw_pixel_block(cx, cy, 11, 7, 10, 16, (101, 67, 37))
        draw_pixel_block(cx, cy, 7, 20, 18, 3, (132, 84, 42))
        draw_pixel_block(cx, cy, 4, 20, 8, 7, (34, 88, 49))
        draw_pixel_block(cx, cy, 8, 24, 9, 7, (43, 109, 54))
        draw_pixel_block(cx, cy, 15, 26, 10, 5, (51, 122, 57))
        draw_pixel_block(cx, cy, 22, 21, 7, 7, (37, 96, 48))
        draw_pixel_block(cx, cy, 8, 18, 4, 4, (214, 52, 74))
        draw_pixel_block(cx, cy, 9, 17, 2, 2, (255, 138, 148))
        draw_pixel_block(cx, cy, 15, 20, 5, 5, (214, 52, 74))
        draw_pixel_block(cx, cy, 16, 19, 2, 2, (255, 138, 148))
        draw_pixel_block(cx, cy, 22, 17, 4, 4, (214, 52, 74))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "meteor":
        draw_pixel_block(cx, cy, 4, 4, 24, 3, (39, 35, 34))
        draw_pixel_block(cx, cy, 7, 7, 19, 6, (55, 47, 44))
        draw_pixel_block(cx, cy, 10, 13, 14, 7, (64, 53, 48))
        draw_pixel_block(cx, cy, 13, 20, 8, 5, (47, 40, 39))
        draw_pixel_block(cx, cy, 14, 22, 6, 3, (245, 75, 31))
        draw_pixel_block(cx, cy, 15, 23, 4, 2, (255, 191, 52))
        draw_pixel_block(cx, cy, 12, 8, 2, 11, (224, 63, 32))
        draw_pixel_block(cx, cy, 20, 9, 2, 9, (246, 85, 30))
        draw_pixel_block(cx, cy, 18, 27, 5, 4, (107, 101, 99))
        draw_pixel_block(cx, cy, 21, 29, 5, 3, (125, 118, 115))
        draw_pixel_block(cx, cy, 23, 23, 4, 4, (246, 79, 30))
        draw_pixel_block(cx, cy, 24, 24, 2, 2, (255, 194, 53))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "oracle":
        draw_pixel_block(cx, cy, 7, 4, 20, 3, (63, 46, 81))
        draw_pixel_block(cx, cy, 10, 7, 12, 3, (167, 118, 53))
        draw_pixel_block(cx, cy, 17, 10, 3, 8, (185, 132, 54))
        draw_pixel_block(cx, cy, 7, 17, 17, 12, (92, 58, 122))
        draw_pixel_block(cx, cy, 8, 18, 15, 10, (224, 180, 73))
        draw_pixel_block(cx, cy, 10, 20, 11, 7, (136, 194, 219))
        draw_pixel_block(cx, cy, 11, 24, 5, 2, (216, 245, 254))
        draw_pixel_block(cx, cy, 18, 20, 2, 2, (247, 237, 255))
        draw_pixel_block(cx, cy, 22, 14, 7, 3, (173, 116, 46))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "time_spire":
        now = datetime.now()
        minute_angle = math.pi / 2 - (now.minute + now.second / 60) * 2 * math.pi / 60
        hour_angle = math.pi / 2 - ((now.hour % 12) + now.minute / 60) * 2 * math.pi / 12
        draw_pixel_block(cx, cy, 6, 4, 21, 3, (40, 54, 67))
        draw_pixel_block(cx, cy, 9, 7, 15, 5, (74, 99, 108))
        draw_pixel_block(cx, cy, 13, 12, 7, 6, (111, 141, 149))
        draw_pixel_block(cx, cy, 6, 17, 21, 13, (44, 58, 70))
        draw_pixel_block(cx, cy, 8, 19, 17, 10, (204, 171, 73))
        draw_pixel_block(cx, cy, 10, 20, 13, 8, (237, 243, 240))
        hand_x = cx
        hand_y = cy + 0.22
        dudraw.set_pen_color_rgb(48, 62, 70)
        dudraw.line(hand_x, hand_y, hand_x + math.cos(hour_angle) * 0.13, hand_y + math.sin(hour_angle) * 0.13)
        dudraw.set_pen_color_rgb(53, 108, 119)
        dudraw.line(hand_x, hand_y, hand_x + math.cos(minute_angle) * 0.19, hand_y + math.sin(minute_angle) * 0.19)
        dudraw.set_pen_color_rgb(212, 56, 57)
        dudraw.filled_circle(hand_x, hand_y, 0.025)
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "thornheart":
        draw_pixel_block(cx, cy, 4, 5, 24, 4, (35, 56, 34))
        draw_pixel_block(cx, cy, 5, 9, 22, 7, (47, 104, 51))
        draw_pixel_block(cx, cy, 8, 16, 17, 8, (56, 121, 53))
        draw_pixel_block(cx, cy, 5, 20, 5, 4, (80, 149, 63))
        draw_pixel_block(cx, cy, 23, 18, 5, 4, (80, 149, 63))
        draw_pixel_block(cx, cy, 7, 15, 3, 2, (184, 196, 89))
        draw_pixel_block(cx, cy, 13, 24, 2, 3, (184, 196, 89))
        draw_pixel_block(cx, cy, 22, 14, 3, 2, (184, 196, 89))
        draw_pixel_block(cx, cy, 12, 13, 9, 7, (112, 27, 45))
        draw_pixel_block(cx, cy, 14, 16, 5, 5, (222, 59, 80))
        draw_pixel_block(cx, cy, 15, 18, 2, 2, (253, 126, 132))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "royal_mint":
        draw_pixel_block(cx, cy, 5, 4, 23, 3, (59, 52, 47))
        draw_pixel_block(cx, cy, 7, 7, 19, 13, (130, 76, 43))
        draw_pixel_block(cx, cy, 18, 11, 6, 7, (48, 42, 39))
        draw_pixel_block(cx, cy, 20, 13, 3, 4, (253, 155, 44))
        draw_pixel_block(cx, cy, 4, 19, 24, 3, (91, 58, 40))
        draw_pixel_block(cx, cy, 8, 22, 17, 4, (197, 117, 51))
        draw_pixel_block(cx, cy, 8, 17, 5, 4, (102, 69, 37))
        draw_pixel_block(cx, cy, 9, 18, 3, 2, (245, 195, 62))
        draw_pixel_block(cx, cy, 7, 23, 4, 7, (73, 62, 54))
        draw_pixel_block(cx, cy, 8, 29, 5, 2, (111, 103, 97))
        draw_pixel_block(cx, cy, 23, 7, 5, 2, (244, 193, 61))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "guardian":
        draw_pixel_block(cx, cy, 3, 4, 26, 3, (38, 42, 47))
        draw_pixel_block(cx, cy, 4, 7, 6, 19, (68, 71, 77))
        draw_pixel_block(cx, cy, 22, 7, 6, 19, (68, 71, 77))
        draw_pixel_block(cx, cy, 3, 25, 8, 3, (105, 109, 114))
        draw_pixel_block(cx, cy, 21, 25, 8, 3, (105, 109, 114))
        draw_pixel_block(cx, cy, 5, 28, 4, 3, (36, 38, 44))
        draw_pixel_block(cx, cy, 23, 28, 4, 3, (36, 38, 44))
        for bar_x in (11, 14, 17, 20):
            draw_pixel_block(cx, cy, bar_x, 7, 1, 18, (25, 29, 35))
        draw_pixel_block(cx, cy, 10, 20, 12, 2, (27, 31, 37))
        draw_pixel_block(cx, cy, 15, 15, 3, 4, (150, 190, 212))
        draw_pixel_block(cx, cy, 16, 18, 1, 2, (219, 244, 249))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return
    if tower.tower_type == "starfall":
        draw_pixel_block(cx, cy, 6, 4, 20, 3, (30, 30, 49))
        draw_pixel_block(cx, cy, 9, 7, 14, 6, (47, 44, 71))
        draw_pixel_block(cx, cy, 7, 13, 18, 3, (71, 66, 99))
        draw_pixel_block(cx, cy, 10, 16, 2, 8, (194, 146, 57))
        draw_pixel_block(cx, cy, 20, 16, 2, 8, (194, 146, 57))
        draw_pixel_block(cx, cy, 8, 22, 16, 2, (205, 157, 64))
        draw_pixel_block(cx, cy, 13, 23, 6, 7, (114, 99, 203))
        draw_pixel_block(cx, cy, 16, 23, 4, 7, (112, 207, 237))
        draw_pixel_block(cx, cy, 16, 26, 2, 2, (255, 247, 198))
        draw_pixel_block(cx, cy, 6, 27, 2, 2, (221, 232, 255))
        draw_pixel_block(cx, cy, 24, 25, 2, 2, (221, 232, 255))
        if tower.level > 1:
            for i in range(tower.level):
                draw_pixel_block(cx, cy, 7 + i * 5, 2, 2, 2, (255, 237, 119))
        return

    draw_pixel_block(cx, cy, 5, 5, 22, 3, darken(base, 70))
    draw_pixel_block(cx, cy, 7, 8, 18, 4, dark)
    draw_pixel_block(cx, cy, 10, 12, 12, 14, base)
    draw_pixel_block(cx, cy, 12, 25, 8, 3, light)

    if tower.is_special:
        draw_pixel_block(cx, cy, 10, 12, 12, 13, light)
        draw_pixel_block(cx, cy, 14, 16, 4, 4, (255, 247, 190))

    if tower.level > 1:
        for i in range(tower.level):
            draw_pixel_block(cx, cy, 6 + i * 5, 28, 2, 2, (255, 237, 119))


def draw_release_tower(x, y, tower_type, frame, scale=1.0):
    stats = get_tower_stats(tower_type)
    bob = math.sin(frame * 0.045 + x) * 0.08
    aim_angle = math.sin(frame * 0.035 + x) * 0.36
    aim_x = math.cos(aim_angle)
    aim_y = math.sin(aim_angle)
    base = stats["color"]

    draw_shadow(x, y + bob, 1.2 * scale)
    if tower_type not in ("arrow", "cannon", "frost", "sniper", "laser", "mortar", "venom", "storm", "titan", "gold_vault", "life_tree", "meteor", "oracle", "time_spire", "thornheart", "royal_mint", "guardian", "starfall"):
        draw_plinth(x, y + bob, base, 1.22 * scale)

    if tower_type in SPECIAL_TOWERS and tower_type not in ("titan", "gold_vault", "life_tree", "meteor", "oracle", "time_spire", "thornheart", "royal_mint", "guardian", "starfall"):
        set_color(brighten(base, 55))
        dudraw.circle(x, y + bob + 0.08 * scale, 0.9 * scale)
        draw_arcane_orbits(x, y + bob + 0.08 * scale, base, frame, 0.75, 6, scale)

    draw_tower_body(x, y + bob + 0.08 * scale, tower_type, aim_x, aim_y, frame, 1.35 * scale)

    if stats["damage"] > 0 and tower_type not in ("arrow", "sniper"):
        muzzle_x = x + aim_x * 0.9 * scale
        muzzle_y = y + bob + 0.34 * scale + aim_y * 0.55 * scale
        set_color(stats["shot_color"])
        dudraw.filled_circle(muzzle_x, muzzle_y, 0.1 * scale)
        set_color(brighten(stats["shot_color"], 45))
        dudraw.circle(muzzle_x, muzzle_y, 0.16 * scale)
