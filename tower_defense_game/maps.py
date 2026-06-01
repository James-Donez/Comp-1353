def make_path():
    path = []

    for x in range(0, 7):
        path.append((x + 0.5, 12.5))
    for y in range(11, 4, -1):
        path.append((6.5, y + 0.5))
    for x in range(6, 17):
        path.append((x + 0.5, 4.5))
    for y in range(5, 11):
        path.append((16.5, y + 0.5))
    for x in range(17, 24):
        path.append((x + 0.5, 10.5))

    return path


def make_path_from_points(points):
    path = []

    for index in range(len(points) - 1):
        start_x, start_y = points[index]
        end_x, end_y = points[index + 1]
        dx = 0 if end_x == start_x else (1 if end_x > start_x else -1)
        dy = 0 if end_y == start_y else (1 if end_y > start_y else -1)
        x = start_x
        y = start_y

        if index == 0:
            path.append((x + 0.5, y + 0.5))

        while (x, y) != (end_x, end_y):
            x += dx
            y += dy
            path.append((x + 0.5, y + 0.5))

    return path


MAPS = {
    "classic": {
        "name": "Classic Meadow",
        "special": "Balanced starter map.",
        "path": make_path(),
        "theme": {
            "grass_a": (189, 225, 156),
            "grass_b": (169, 210, 139),
            "path": (207, 182, 136),
            "edge": (114, 91, 61),
            "detail": (145, 184, 126),
        },
        "money_bonus": 0,
        "lives_bonus": 0,
        "wave_bonus": 25,
        "place_rule": "normal",
    },
    "polished_classic": {
        "name": "Polished Classic Meadow",
        "special": "A living meadow edition of the original balanced map.",
        "path": make_path(),
        "theme": {
            "grass_a": (116, 184, 108),
            "grass_b": (87, 157, 94),
            "path": (211, 181, 128),
            "edge": (107, 77, 51),
            "detail": (224, 219, 139),
        },
        "money_bonus": 0,
        "lives_bonus": 0,
        "wave_bonus": 25,
        "place_rule": "normal",
        "polished": True,
        "polished_style": "meadow",
    },
    "desert": {
        "name": "Desert Ruins",
        "special": "Start with extra money, but fewer wave bonuses.",
        "path": make_path_from_points([(0, 3), (8, 3), (8, 13), (15, 13), (15, 6), (23, 6)]),
        "theme": {
            "grass_a": (222, 188, 111),
            "grass_b": (204, 169, 91),
            "path": (169, 122, 70),
            "edge": (113, 79, 51),
            "detail": (235, 213, 143),
        },
        "money_bonus": 80,
        "lives_bonus": 0,
        "wave_bonus": 15,
        "place_rule": "normal",
    },
    "polished_desert": {
        "name": "Polished Desert Ruins",
        "special": "A wind-carved oasis edition with rich starting funds.",
        "path": make_path_from_points([(0, 3), (8, 3), (8, 13), (15, 13), (15, 6), (23, 6)]),
        "theme": {
            "grass_a": (226, 187, 103),
            "grass_b": (202, 151, 76),
            "path": (179, 126, 68),
            "edge": (102, 67, 41),
            "detail": (244, 210, 123),
        },
        "money_bonus": 80,
        "lives_bonus": 0,
        "wave_bonus": 15,
        "place_rule": "normal",
        "polished": True,
        "polished_style": "desert",
    },
    "mountain": {
        "name": "Mountain Pass",
        "special": "Tight turns make splash towers strong.",
        "path": make_path_from_points([(0, 14), (4, 14), (4, 9), (10, 9), (10, 2), (18, 2), (18, 12), (23, 12)]),
        "theme": {
            "grass_a": (126, 154, 131),
            "grass_b": (104, 132, 113),
            "path": (143, 139, 129),
            "edge": (75, 82, 80),
            "detail": (188, 197, 191),
        },
        "money_bonus": 20,
        "lives_bonus": 2,
        "wave_bonus": 25,
        "place_rule": "normal",
    },
    "polished_mountain": {
        "name": "Polished Mountain Pass",
        "special": "An alpine cliff edition where tight turns reward splash.",
        "path": make_path_from_points([(0, 14), (4, 14), (4, 9), (10, 9), (10, 2), (18, 2), (18, 12), (23, 12)]),
        "theme": {"grass_a": (127, 157, 137), "grass_b": (92, 122, 112), "path": (156, 148, 134), "edge": (65, 75, 78), "detail": (214, 225, 225)},
        "money_bonus": 20, "lives_bonus": 2, "wave_bonus": 25, "place_rule": "normal",
        "polished": True, "polished_style": "mountain",
    },
    "ocean": {
        "name": "Island Chain",
        "special": "Towers can only be placed on islands.",
        "path": make_path_from_points([(0, 8), (5, 8), (5, 3), (12, 3), (12, 12), (19, 12), (19, 7), (23, 7)]),
        "theme": {
            "grass_a": (68, 151, 177),
            "grass_b": (47, 128, 158),
            "path": (224, 204, 139),
            "edge": (41, 91, 120),
            "detail": (112, 188, 203),
        },
        "islands": {(3, 12), (4, 12), (9, 6), (10, 6), (16, 4), (17, 4), (20, 11), (21, 11), (13, 14), (14, 14), (7, 1), (8, 1)},
        "money_bonus": 120,
        "lives_bonus": 0,
        "wave_bonus": 25,
        "place_rule": "islands",
    },
    "polished_ocean": {
        "name": "Polished Island Chain",
        "special": "A rolling-tide archipelago; towers still require islands.",
        "path": make_path_from_points([(0, 8), (5, 8), (5, 3), (12, 3), (12, 12), (19, 12), (19, 7), (23, 7)]),
        "theme": {"grass_a": (63, 163, 185), "grass_b": (33, 120, 157), "path": (229, 208, 143), "edge": (32, 84, 112), "detail": (136, 218, 220)},
        "islands": {(3, 12), (4, 12), (9, 6), (10, 6), (16, 4), (17, 4), (20, 11), (21, 11), (13, 14), (14, 14), (7, 1), (8, 1)},
        "money_bonus": 120, "lives_bonus": 0, "wave_bonus": 25, "place_rule": "islands",
        "polished": True, "polished_style": "ocean",
    },
    "temple": {
        "name": "Cherry Temple",
        "special": "More lives from temple protection.",
        "path": make_path_from_points([(0, 5), (5, 5), (5, 11), (11, 11), (11, 4), (18, 4), (18, 13), (23, 13)]),
        "theme": {
            "grass_a": (203, 220, 169),
            "grass_b": (184, 208, 157),
            "path": (184, 134, 122),
            "edge": (108, 76, 78),
            "detail": (238, 166, 191),
        },
        "money_bonus": 0,
        "lives_bonus": 5,
        "wave_bonus": 25,
        "place_rule": "normal",
    },
    "polished_temple": {
        "name": "Polished Cherry Temple",
        "special": "A lantern-lit blossom sanctuary with temple protection.",
        "path": make_path_from_points([(0, 5), (5, 5), (5, 11), (11, 11), (11, 4), (18, 4), (18, 13), (23, 13)]),
        "theme": {"grass_a": (202, 221, 176), "grass_b": (168, 196, 153), "path": (188, 140, 124), "edge": (100, 67, 69), "detail": (242, 168, 194)},
        "money_bonus": 0, "lives_bonus": 5, "wave_bonus": 25, "place_rule": "normal",
        "polished": True, "polished_style": "temple",
    },
    "racetrack": {
        "name": "Race Track Loop",
        "special": "Fast waves, higher rewards.",
        "path": make_path_from_points([(0, 8), (5, 8), (5, 13), (19, 13), (19, 3), (5, 3), (5, 8), (23, 8)]),
        "theme": {
            "grass_a": (82, 116, 92),
            "grass_b": (68, 101, 79),
            "path": (72, 72, 74),
            "edge": (220, 220, 220),
            "detail": (235, 70, 70),
        },
        "money_bonus": 30,
        "lives_bonus": 0,
        "wave_bonus": 40,
        "place_rule": "normal",
    },
    "polished_racetrack": {
        "name": "Polished Race Track Loop",
        "special": "A floodlit circuit edition with fast high-value waves.",
        "path": make_path_from_points([(0, 8), (5, 8), (5, 13), (19, 13), (19, 3), (5, 3), (5, 8), (23, 8)]),
        "theme": {"grass_a": (68, 117, 80), "grass_b": (43, 80, 59), "path": (60, 63, 67), "edge": (228, 230, 227), "detail": (230, 63, 60)},
        "money_bonus": 30, "lives_bonus": 0, "wave_bonus": 40, "place_rule": "normal",
        "polished": True, "polished_style": "racetrack",
    },
    "war": {
        "name": "Warzone",
        "special": "Begin with extra lives.",
        "path": make_path_from_points([(0, 2), (7, 2), (7, 7), (3, 7), (3, 13), (15, 13), (15, 5), (23, 5)]),
        "theme": {
            "grass_a": (99, 111, 82),
            "grass_b": (82, 94, 69),
            "path": (91, 82, 69),
            "edge": (48, 54, 47),
            "detail": (129, 123, 101),
        },
        "money_bonus": 20,
        "lives_bonus": 6,
        "wave_bonus": 20,
        "place_rule": "normal",
    },
    "polished_war": {
        "name": "Polished Warzone",
        "special": "A scarred trenchland edition that begins with extra lives.",
        "path": make_path_from_points([(0, 2), (7, 2), (7, 7), (3, 7), (3, 13), (15, 13), (15, 5), (23, 5)]),
        "theme": {"grass_a": (102, 108, 78), "grass_b": (69, 77, 58), "path": (92, 77, 60), "edge": (43, 47, 42), "detail": (155, 139, 103)},
        "money_bonus": 20, "lives_bonus": 6, "wave_bonus": 20, "place_rule": "normal",
        "polished": True, "polished_style": "war",
    },
    "miami": {
        "name": "Miami Beach",
        "special": "High money economy.",
        "path": make_path_from_points([(0, 11), (6, 11), (6, 6), (13, 6), (13, 14), (20, 14), (20, 4), (23, 4)]),
        "theme": {
            "grass_a": (244, 207, 128),
            "grass_b": (235, 190, 109),
            "path": (76, 202, 209),
            "edge": (236, 111, 154),
            "detail": (67, 184, 151),
        },
        "money_bonus": 100,
        "lives_bonus": 0,
        "wave_bonus": 35,
        "place_rule": "normal",
    },
    "polished_miami": {
        "name": "Polished Miami Beach",
        "special": "A neon shoreline edition with the same thriving economy.",
        "path": make_path_from_points([(0, 11), (6, 11), (6, 6), (13, 6), (13, 14), (20, 14), (20, 4), (23, 4)]),
        "theme": {"grass_a": (246, 208, 135), "grass_b": (227, 178, 101), "path": (72, 204, 212), "edge": (224, 78, 139), "detail": (70, 190, 157)},
        "money_bonus": 100, "lives_bonus": 0, "wave_bonus": 35, "place_rule": "normal",
        "polished": True, "polished_style": "miami",
    },
    "retro": {
        "name": "Retro Grid",
        "special": "Extra wave rewards, neon visuals.",
        "path": make_path_from_points([(0, 1), (11, 1), (11, 8), (2, 8), (2, 15), (21, 15), (21, 5), (23, 5)]),
        "theme": {
            "grass_a": (42, 35, 73),
            "grass_b": (32, 27, 58),
            "path": (39, 207, 198),
            "edge": (241, 76, 196),
            "detail": (255, 231, 98),
        },
        "money_bonus": 40,
        "lives_bonus": 0,
        "wave_bonus": 45,
        "place_rule": "normal",
    },
    "polished_retro": {
        "name": "Polished Retro Grid",
        "special": "A synthwave skyline edition with boosted wave rewards.",
        "path": make_path_from_points([(0, 1), (11, 1), (11, 8), (2, 8), (2, 15), (21, 15), (21, 5), (23, 5)]),
        "theme": {"grass_a": (39, 30, 70), "grass_b": (18, 17, 42), "path": (37, 211, 203), "edge": (243, 65, 192), "detail": (255, 226, 89)},
        "money_bonus": 40, "lives_bonus": 0, "wave_bonus": 45, "place_rule": "normal",
        "polished": True, "polished_style": "retro",
    },
    "crystal": {
        "name": "Crystal Cavern",
        "special": "Rich crystals grant money and lives.",
        "path": make_path_from_points([(0, 13), (9, 13), (9, 10), (4, 10), (4, 4), (14, 4), (14, 9), (23, 9)]),
        "theme": {
            "grass_a": (78, 71, 117),
            "grass_b": (61, 55, 96),
            "path": (128, 106, 166),
            "edge": (87, 216, 220),
            "detail": (190, 248, 255),
        },
        "money_bonus": 70,
        "lives_bonus": 3,
        "wave_bonus": 30,
        "place_rule": "normal",
    },
    "polished_crystal": {
        "name": "Polished Crystal Cavern",
        "special": "A luminous cavern edition rich in treasure and lives.",
        "path": make_path_from_points([(0, 13), (9, 13), (9, 10), (4, 10), (4, 4), (14, 4), (14, 9), (23, 9)]),
        "theme": {"grass_a": (74, 66, 112), "grass_b": (43, 39, 76), "path": (135, 111, 176), "edge": (71, 193, 209), "detail": (194, 247, 255)},
        "money_bonus": 70, "lives_bonus": 3, "wave_bonus": 30, "place_rule": "normal",
        "polished": True, "polished_style": "crystal",
    },
}


THREE_D_SOURCE_KEYS = (
    "classic", "desert", "mountain", "ocean", "temple",
    "racetrack", "war", "miami", "retro", "crystal",
)

for source_key in THREE_D_SOURCE_KEYS:
    source = MAPS[source_key]
    map_3d = {
        "name": f"3D {source['name']}",
        "special": f"Raised-terrain edition. {source['special']}",
        "path": source["path"],
        "theme": source["theme"],
        "money_bonus": source["money_bonus"],
        "lives_bonus": source["lives_bonus"],
        "wave_bonus": source["wave_bonus"],
        "place_rule": source["place_rule"],
        "three_d": True,
        "three_d_style": source_key,
    }
    if "islands" in source:
        map_3d["islands"] = source["islands"]
    MAPS[f"3d_{source_key}"] = map_3d
