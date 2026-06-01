import math

import dudraw
import dudraw.dudraw as dudraw_backend
import pygame

try:
    from tower_defense_game.maps import MAPS
    from tower_defense_game import tower_models
    from tower_defense_game.update_log import UPDATE_LOG
except ModuleNotFoundError:
    from maps import MAPS
    import tower_models
    from update_log import UPDATE_LOG


GRID_WIDTH = 24
GRID_HEIGHT = 16
CANVAS_WIDTH = 960
CANVAS_HEIGHT = 640
START_MONEY = 120
START_LIVES = 12
UPGRADE_COST = 60
SELL_REFUND = 0.65
MONEY_GAIN_RATE = 0.7
ENEMY_SPEED_SCALE = 1.12
ENEMY_SIZE_SCALE = 1.12
ATTACK_SPEED_SCALE = 0.88
DIFFICULTIES = {
    "easy": {
        "name": "Easy",
        "description": "Relaxed defense with steady income.",
        "color": (106, 211, 139),
        "damage": 1.0,
        "health": 1.0,
        "speed": 1.0,
        "money": 1.0,
        "lives": 1.0,
        "spawn": 1.0,
        "threat": 0,
    },
    "medium": {
        "name": "Medium",
        "description": "Less funding and quicker enemy pressure.",
        "color": (235, 192, 82),
        "damage": 0.9,
        "health": 1.2,
        "speed": 1.08,
        "money": 0.85,
        "lives": 0.85,
        "spawn": 0.92,
        "threat": 1,
    },
    "hard": {
        "name": "Hard",
        "description": "Tough waves punish weak placements.",
        "color": (230, 105, 76),
        "damage": 0.78,
        "health": 1.5,
        "speed": 1.18,
        "money": 0.7,
        "lives": 0.65,
        "spawn": 0.82,
        "threat": 2,
    },
    "insane": {
        "name": "Insane",
        "description": "Brutal pressure with almost no margin.",
        "color": (228, 80, 137),
        "damage": 0.62,
        "health": 1.9,
        "speed": 1.3,
        "money": 0.5,
        "lives": 0.45,
        "spawn": 0.7,
        "threat": 3,
    },
}
DEFAULT_SETTINGS = {
    "volume": 7,
    "graphics": "amazing",
    "special_tower": "titan",
    "difficulty": "easy",
    "fullscreen": False,
    "show_path_arrows": True,
    "show_health_bars": True,
    "show_threat_marks": True,
    "show_range": True,
    "show_target_links": True,
    "show_floating_text": True,
    "show_stats": True,
}
PLACEMENT_BLOCK_MESSAGES = {
    "bounds": "Outside the battlefield",
    "path": "The road must stay clear",
    "track": "Guardian Gate must be placed on the road",
    "island": "Build on island tiles here",
    "occupied": "That tile is occupied",
    "special": "Special tower already used",
    "money": "Not enough money",
}
CURRENT_VERSION = UPDATE_LOG[0]["version"]
DISPLAY_RECT = (0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
TOWER_ORDER = ("arrow", "cannon", "frost", "sniper", "laser", "mortar", "venom", "storm", "special")
TOWER_TYPES = {
    "arrow": {
        "name": "Arrow",
        "cost": 35,
        "range": 3.2,
        "damage": 18,
        "cooldown": 18,
        "color": (40, 87, 145),
        "shot_color": (245, 214, 74),
        "slow": 0,
        "splash": 0,
        "poison": 0,
    },
    "cannon": {
        "name": "Cannon",
        "cost": 60,
        "range": 2.6,
        "damage": 42,
        "cooldown": 38,
        "color": (95, 75, 62),
        "shot_color": (232, 105, 53),
        "slow": 0,
        "splash": 0.95,
        "poison": 0,
    },
    "frost": {
        "name": "Frost",
        "cost": 45,
        "range": 2.9,
        "damage": 8,
        "cooldown": 24,
        "color": (67, 151, 173),
        "shot_color": (128, 224, 235),
        "slow": 55,
        "splash": 0,
        "poison": 0,
    },
    "sniper": {
        "name": "Sniper",
        "cost": 75,
        "range": 6.0,
        "damage": 70,
        "cooldown": 60,
        "color": (98, 72, 148),
        "shot_color": (231, 173, 255),
        "slow": 0,
        "splash": 0,
        "poison": 0,
    },
    "laser": {
        "name": "Laser",
        "cost": 50,
        "range": 3.5,
        "damage": 10,
        "cooldown": 7,
        "color": (217, 60, 84),
        "shot_color": (255, 88, 108),
        "slow": 0,
        "splash": 0,
        "poison": 0,
    },
    "mortar": {
        "name": "Mortar",
        "cost": 90,
        "range": 4.4,
        "damage": 35,
        "cooldown": 52,
        "color": (64, 85, 77),
        "shot_color": (255, 168, 72),
        "slow": 0,
        "splash": 1.55,
        "poison": 0,
    },
    "venom": {
        "name": "Venom",
        "cost": 55,
        "range": 3.0,
        "damage": 9,
        "cooldown": 18,
        "color": (85, 152, 74),
        "shot_color": (130, 232, 88),
        "slow": 0,
        "splash": 0,
        "poison": 95,
    },
    "storm": {
        "name": "Storm",
        "cost": 85,
        "range": 3.7,
        "damage": 20,
        "cooldown": 32,
        "color": (54, 107, 189),
        "shot_color": (134, 184, 255),
        "slow": 80,
        "splash": 0.75,
        "poison": 0,
    },
}
TOWER_KEYS = {
    "1": "arrow",
    "2": "cannon",
    "3": "frost",
    "4": "sniper",
    "5": "laser",
    "6": "mortar",
    "7": "venom",
    "8": "storm",
}
DEFAULT_CONTROLS = {
    "arrow": "1",
    "cannon": "2",
    "frost": "3",
    "sniper": "4",
    "laser": "5",
    "mortar": "6",
    "venom": "7",
    "storm": "8",
    "special": "9",
    "cancel": "escape",
    "cycle_build": "tab",
    "start_wave": "return",
    "pause": " ",
    "speed": "v",
    "speed_down": ",",
    "speed_up": ".",
    "upgrade_power": "u",
    "upgrade_utility": "i",
    "sell": "x",
    "auto_pause": "a",
    "stats": "h",
    "links": "j",
    "health": "k",
    "floating": "o",
    "arrows": "y",
    "threat": "t",
    "restart": "r",
    "menu": "m",
    "fullscreen": "f",
    "quit": "q",
}
CONTROL_LABELS = {
    "arrow": "Build Arrow",
    "cannon": "Build Cannon",
    "frost": "Build Frost",
    "sniper": "Build Sniper",
    "laser": "Build Laser",
    "mortar": "Build Mortar",
    "venom": "Build Venom",
    "storm": "Build Storm",
    "special": "Build Special",
    "cancel": "Clear Selection",
    "cycle_build": "Cycle Builds",
    "start_wave": "Start Wave",
    "pause": "Pause / Resume",
    "speed": "Toggle Speed",
    "speed_down": "Slower",
    "speed_up": "Faster",
    "upgrade_power": "Power Upgrade",
    "upgrade_utility": "Speed Upgrade",
    "sell": "Sell Tower",
    "auto_pause": "Auto-Pause",
    "stats": "Match Stats",
    "links": "Target Links",
    "health": "Health Bars",
    "floating": "Floating Text",
    "arrows": "Path Arrows",
    "threat": "Threat Marks",
    "restart": "Restart Match",
    "menu": "Return To Menu",
    "fullscreen": "Fullscreen",
    "quit": "Quit Match",
}
CONTROL_ACTIONS = tuple(DEFAULT_CONTROLS)
SPECIAL_TOWERS = {
    "titan": {
        "name": "Zeus Titan",
        "cost": 0,
        "range": 5.0,
        "damage": 120,
        "cooldown": 42,
        "color": (231, 195, 76),
        "shot_color": (255, 231, 112),
        "slow": 0,
        "splash": 1.2,
        "poison": 0,
        "money_bonus": 0,
        "lives_bonus": 0,
        "description": "A Zeus-inspired ruler who hurls lightning into grouped enemies.",
    },
    "life_tree": {
        "name": "Heart Orchard",
        "cost": 0,
        "range": 0,
        "damage": 0,
        "cooldown": 999,
        "color": (74, 166, 90),
        "shot_color": (154, 240, 148),
        "slow": 0,
        "splash": 0,
        "poison": 0,
        "money_bonus": 0,
        "lives_bonus": 8,
        "description": "An ancient heart-fruit tree that grants 8 lives when planted.",
    },
    "gold_vault": {
        "name": "Pearl Treasury",
        "cost": 0,
        "range": 0,
        "damage": 0,
        "cooldown": 999,
        "color": (224, 164, 56),
        "shot_color": (255, 215, 93),
        "slow": 0,
        "splash": 0,
        "poison": 0,
        "money_bonus": 260,
        "lives_bonus": 0,
        "description": "A pearl-white classical bank that grants $260 when placed.",
    },
    "meteor": {
        "name": "Meteor Volcano",
        "cost": 0,
        "range": 4.3,
        "damage": 95,
        "cooldown": 58,
        "color": (210, 83, 51),
        "shot_color": (255, 116, 58),
        "slow": 0,
        "splash": 2.2,
        "poison": 0,
        "money_bonus": 0,
        "lives_bonus": 0,
        "description": "An erupting volcano that arcs molten meteors into enemy groups.",
    },
    "oracle": {
        "name": "Grand Oracle Lens",
        "cost": 0,
        "range": 7.0,
        "damage": 85,
        "cooldown": 30,
        "color": (153, 112, 219),
        "shot_color": (235, 199, 255),
        "slow": 0,
        "splash": 0,
        "poison": 0,
        "money_bonus": 0,
        "lives_bonus": 0,
        "description": "A huge magnifying glass that focuses a long-range beam.",
    },
    "time_spire": {
        "name": "World Clock Spire",
        "cost": 0,
        "range": 4.5,
        "damage": 24,
        "cooldown": 20,
        "color": (73, 184, 198),
        "shot_color": (157, 244, 255),
        "slow": 130,
        "splash": 1.3,
        "poison": 0,
        "money_bonus": 0,
        "lives_bonus": 0,
        "description": "A giant real-time clock whose pulse slows enemy groups.",
    },
    "thornheart": {
        "name": "Thornheart Bramble",
        "cost": 0,
        "range": 3.8,
        "damage": 28,
        "cooldown": 16,
        "color": (61, 145, 72),
        "shot_color": (119, 245, 92),
        "slow": 0,
        "splash": 0.8,
        "poison": 180,
        "money_bonus": 0,
        "lives_bonus": 3,
        "description": "A giant heart bush that lashes enemies with poisonous thorn vines.",
    },
    "royal_mint": {
        "name": "Royal Coinworks",
        "cost": 0,
        "range": 2.6,
        "damage": 22,
        "cooldown": 18,
        "color": (198, 151, 61),
        "shot_color": (255, 223, 115),
        "slow": 0,
        "splash": 0,
        "poison": 0,
        "money_bonus": 0,
        "kill_bonus": 18,
        "lives_bonus": 0,
        "description": "A coin foundry that mints bonus money for every enemy it defeats.",
    },
    "guardian": {
        "name": "Haunted Manor Gate",
        "cost": 0,
        "range": 0,
        "damage": 0,
        "cooldown": 999,
        "color": (91, 112, 142),
        "shot_color": (180, 207, 235),
        "slow": 0,
        "splash": 0,
        "poison": 0,
        "money_bonus": 0,
        "lives_bonus": 0,
        "block_duration": 95,
        "description": "A haunted estate gate placed on the road to halt each enemy once.",
    },
    "starfall": {
        "name": "Starfall Prism",
        "cost": 0,
        "range": 5.8,
        "damage": 55,
        "cooldown": 12,
        "color": (219, 91, 179),
        "shot_color": (255, 176, 230),
        "slow": 0,
        "splash": 0,
        "poison": 0,
        "money_bonus": 70,
        "lives_bonus": 2,
        "description": "A celestial observatory prism that rains brilliant star shards.",
    },
}
tower_models.configure_tower_models(TOWER_TYPES, SPECIAL_TOWERS)
ENEMY_TYPES = {
    "scout": {
        "name": "Scout",
        "health": 0.8,
        "speed": 1.15,
        "reward": 1.0,
        "radius": 0.28,
        "color": (184, 62, 54),
    },
    "runner": {
        "name": "Runner",
        "health": 0.55,
        "speed": 1.65,
        "reward": 0.9,
        "radius": 0.24,
        "color": (221, 121, 46),
    },
    "brute": {
        "name": "Brute",
        "health": 2.0,
        "speed": 0.68,
        "reward": 1.6,
        "radius": 0.4,
        "color": (112, 49, 47),
    },
    "shield": {
        "name": "Shield",
        "health": 1.35,
        "speed": 0.9,
        "reward": 1.35,
        "radius": 0.34,
        "color": (81, 93, 118),
    },
    "swarm": {
        "name": "Swarm",
        "health": 0.35,
        "speed": 1.9,
        "reward": 0.65,
        "radius": 0.2,
        "color": (178, 91, 38),
    },
    "wraith": {
        "name": "Wraith",
        "health": 0.85,
        "speed": 1.35,
        "reward": 1.2,
        "radius": 0.26,
        "color": (126, 105, 174),
    },
    "armored": {
        "name": "Armored",
        "health": 2.8,
        "speed": 0.55,
        "reward": 2.0,
        "radius": 0.42,
        "color": (72, 82, 88),
    },
    "splitter": {
        "name": "Splitter",
        "health": 1.15,
        "speed": 1.05,
        "reward": 1.25,
        "radius": 0.3,
        "color": (155, 78, 124),
    },
    "charger": {
        "name": "Charger",
        "health": 1.1,
        "speed": 2.15,
        "reward": 1.45,
        "radius": 0.31,
        "color": (205, 72, 74),
    },
    "boss": {
        "name": "Boss",
        "health": 6.0,
        "speed": 0.42,
        "reward": 5.0,
        "radius": 0.52,
        "color": (82, 37, 65),
    },
}
TOWER_DESCRIPTIONS = {
    "arrow": "Woodland lookout tower with a ranger firing from an elevated deck.",
    "cannon": "Compact field cannon with an iron shield and splash-impact shells.",
    "frost": "Ice wizard tower that launches snowflakes to slow advancing enemies.",
    "sniper": "Prone cliff-perch marksman firing high-damage rifle rounds.",
    "laser": "Steel power-line tower with a charged red beam emitter.",
    "mortar": "Portable sandbag mortar nest that rains wide splash shells.",
    "venom": "Tree-dwelling snake that spits venom for lingering poison damage.",
    "storm": "Thundercloud shrine that chains slowing lightning through groups.",
}
ENEMY_DESCRIPTIONS = {
    "scout": "The basic enemy. It is common, steady, and arrives from wave one.",
    "runner": "A fast enemy that appears in later waves. Fragile, but easy to leak.",
    "brute": "A slow tank with a huge health pool and a bigger reward.",
    "shield": "A durable enemy with armor-like health and moderate speed.",
    "swarm": "Tiny and very fast. Usually appears in packs.",
    "wraith": "A slippery mid-health enemy that moves faster than scouts.",
    "armored": "Extremely sturdy and slow. Bring splash or high damage.",
    "splitter": "A tricky mid-tier enemy with solid speed and health.",
    "charger": "A dangerous sprinter that can burn lives quickly.",
    "boss": "A rare wave monster with enormous health and a huge reward.",
}


def get_tower_stats(tower_type):
    if tower_type in TOWER_TYPES:
        return TOWER_TYPES[tower_type]

    return SPECIAL_TOWERS[tower_type]


def earned_money(amount, difficulty="easy"):
    return int(amount * MONEY_GAIN_RATE * DIFFICULTIES[difficulty]["money"])


def starting_lives(map_info, difficulty):
    lives = START_LIVES + map_info["lives_bonus"]
    return max(1, int(lives * DIFFICULTIES[difficulty]["lives"]))


class Enemy:
    def __init__(self, wave, enemy_type, difficulty="easy"):
        stats = ENEMY_TYPES[enemy_type]
        difficulty_stats = DIFFICULTIES[difficulty]

        self.path_index = 0
        self.x, self.y = PATH[0]
        self.enemy_type = enemy_type
        self.difficulty = difficulty
        self.name = stats["name"]
        self.health = (35 + wave * 12) * stats["health"] * difficulty_stats["health"]
        self.max_health = self.health
        self.base_speed = (0.035 + wave * 0.003) * stats["speed"] * ENEMY_SPEED_SCALE * difficulty_stats["speed"]
        self.radius = stats["radius"] * ENEMY_SIZE_SCALE
        self.color = stats["color"]
        self.slow_timer = 0
        self.gate_timer = 0
        self.blocked_gates = set()
        self.poison_timer = 0
        self.poison_source = None
        self.last_hit_tower = None
        self.reward = max(1, earned_money(int((10 + wave) * stats["reward"]), difficulty))
        self.alive = True
        self.escaped = False

    def move(self, towers=None):
        speed = self.base_speed

        if self.poison_timer > 0:
            self.take_damage(0.32, self.poison_source)
            self.poison_timer -= 1

        if self.gate_timer > 0:
            self.gate_timer -= 1
            return

        if self.slow_timer > 0:
            speed *= 0.48
            self.slow_timer -= 1

        if self.path_index >= len(PATH) - 1:
            self.alive = False
            self.escaped = True
            return

        target_x, target_y = PATH[self.path_index + 1]
        for tower in towers or ():
            gate_id = id(tower)
            if (
                tower.tower_type == "guardian"
                and gate_id not in self.blocked_gates
                and (
                    (tower.x == self.x and tower.y == self.y)
                    or (tower.x == target_x and tower.y == target_y)
                )
            ):
                self.blocked_gates.add(gate_id)
                self.gate_timer = tower.block_duration
                return

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= speed:
            self.x = target_x
            self.y = target_y
            self.path_index += 1
        else:
            self.x += dx / distance * speed
            self.y += dy / distance * speed

    def take_damage(self, damage, source=None):
        if source is not None:
            self.last_hit_tower = source
            source.total_damage += min(damage, max(0, self.health))
        self.health -= damage

        if self.health <= 0:
            self.alive = False

    def slow(self, duration):
        self.slow_timer = max(self.slow_timer, duration)

    def poison(self, duration, source=None):
        self.poison_timer = max(self.poison_timer, duration)
        if source is not None:
            self.poison_source = source


class Tower:
    def __init__(self, x, y, tower_type, difficulty="easy"):
        stats = get_tower_stats(tower_type)
        difficulty_stats = DIFFICULTIES[difficulty]

        self.x = x + 0.5
        self.y = y + 0.5
        self.tower_type = tower_type
        self.is_special = tower_type in SPECIAL_TOWERS
        self.name = stats["name"]
        self.range = stats["range"]
        self.damage = max(1, int(round(stats["damage"] * difficulty_stats["damage"]))) if stats["damage"] > 0 else 0
        self.max_cooldown = max(3, int(stats["cooldown"] * ATTACK_SPEED_SCALE))
        self.color = stats["color"]
        self.shot_color = stats["shot_color"]
        self.slow_duration = stats["slow"]
        self.splash_radius = stats["splash"]
        self.poison_duration = stats["poison"]
        self.kill_bonus = stats.get("kill_bonus", 0)
        self.block_duration = stats.get("block_duration", 0)
        self.cooldown = 0
        self.target = None
        self.level = 1
        self.power_level = 0
        self.utility_level = 0
        self.kills = 0
        self.total_damage = 0
        self.value = stats["cost"]
        self.aim_x = 1
        self.aim_y = 0

    def update(self, enemies, shots, particles):
        self.target = None

        if self.damage <= 0:
            return

        if self.cooldown > 0:
            self.cooldown -= 1
            return

        target = self.find_target(enemies)

        if target is not None:
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                self.aim_x = dx / distance
                self.aim_y = dy / distance

            self.attack_target(target, enemies)

            self.cooldown = self.max_cooldown
            self.target = target
            shot_x = self.x
            if self.tower_type == "laser":
                shot_y = self.y + 0.56
            elif self.tower_type == "mortar":
                shot_y = self.y + 0.30
            elif self.tower_type == "venom":
                shot_x = self.x + 0.12 + self.aim_x * 0.08
                shot_y = self.y + 0.15 + self.aim_y * 0.08
            elif self.tower_type == "storm":
                shot_x = self.x + self.aim_x * 0.04
                shot_y = self.y + 0.52
            elif self.tower_type == "titan":
                shot_x = self.x + 0.34
                shot_y = self.y + 0.66
            elif self.tower_type == "meteor":
                shot_y = self.y + 0.52
            elif self.tower_type == "oracle":
                shot_x = self.x - 0.05
                shot_y = self.y + 0.37
            elif self.tower_type == "time_spire":
                shot_y = self.y + 0.46
            elif self.tower_type == "thornheart":
                shot_y = self.y + 0.16
            elif self.tower_type == "royal_mint":
                shot_x = self.x + self.aim_x * 0.2
                shot_y = self.y + 0.23 + self.aim_y * 0.08
            elif self.tower_type == "starfall":
                shot_y = self.y + 0.58
            else:
                shot_y = self.y
            shots.append([shot_x, shot_y, target.x, target.y, 4, self.shot_color, self.tower_type])
            if self.tower_type != "arrow":
                particles.append([target.x, target.y, 0.18, 8, self.shot_color])

    def upgrade_cost(self, path):
        if path == "power":
            return UPGRADE_COST + self.power_level * 35

        return UPGRADE_COST + self.utility_level * 35

    def can_upgrade(self, path):
        if self.is_special:
            return False

        if path == "power":
            current_level = self.power_level
            other_level = self.utility_level
        else:
            current_level = self.utility_level
            other_level = self.power_level

        if current_level >= 4:
            return False

        # Once one path reaches tier 3, the other path is capped at tier 2.
        if other_level >= 3 and current_level >= 2:
            return False

        return True

    def upgrade(self, path):
        if not self.can_upgrade(path):
            return False

        cost = self.upgrade_cost(path)

        if path == "power":
            self.power_level += 1
            self.damage = int(self.damage * 1.35 + 3)
            self.max_cooldown = max(4, int(self.max_cooldown * 0.9))
        else:
            self.utility_level += 1
            self.range += 0.15
            self.max_cooldown = max(3, int(self.max_cooldown * 0.85))

        self.level += 1
        self.value += cost
        return True

    def attack_target(self, target, enemies):
        target.take_damage(self.damage, self)

        if self.slow_duration > 0:
            target.slow(self.slow_duration)

        if self.poison_duration > 0:
            target.poison(self.poison_duration, self)

        if self.splash_radius > 0:
            for enemy in enemies:
                if enemy is target or not enemy.alive:
                    continue

                dx = enemy.x - target.x
                dy = enemy.y - target.y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance <= self.splash_radius:
                    enemy.take_damage(self.damage * 0.45, self)
                    if self.slow_duration > 0:
                        enemy.slow(self.slow_duration // 2)

    def find_target(self, enemies):
        best_enemy = None
        best_progress = -1

        for enemy in enemies:
            if not enemy.alive:
                continue

            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance <= self.range and enemy.path_index > best_progress:
                best_enemy = enemy
                best_progress = enemy.path_index

        return best_enemy


CURRENT_MAP_KEY = "classic"
CURRENT_MAP = MAPS[CURRENT_MAP_KEY]
PATH = CURRENT_MAP["path"]
PATH_SQUARES = {(int(x), int(y)) for x, y in PATH}
BUILD_SQUARES = set(CURRENT_MAP.get("islands", set()))
CLASSIC_MAP_KEYS = tuple(key for key, map_info in MAPS.items() if not map_info.get("polished", False) and not map_info.get("three_d", False))
POLISHED_MAP_KEYS = tuple(key for key, map_info in MAPS.items() if map_info.get("polished", False))
THREE_D_MAP_KEYS = tuple(key for key, map_info in MAPS.items() if map_info.get("three_d", False))


def set_current_map(map_key):
    global CURRENT_MAP_KEY, CURRENT_MAP, PATH, PATH_SQUARES, BUILD_SQUARES

    CURRENT_MAP_KEY = map_key
    CURRENT_MAP = MAPS[map_key]
    PATH = CURRENT_MAP["path"]
    PATH_SQUARES = {(int(x), int(y)) for x, y in PATH}
    BUILD_SQUARES = set(CURRENT_MAP.get("islands", set()))


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


def canvas_mouse_position():
    offset_x, offset_y, scaled_width, scaled_height = DISPLAY_RECT
    mouse_x, mouse_y = dudraw_backend._mouse_pos

    if scaled_width <= 0 or scaled_height <= 0:
        return mouse_x, mouse_y

    canvas_x = (mouse_x - offset_x) * CANVAS_WIDTH / scaled_width
    canvas_y = (mouse_y - offset_y) * CANVAS_HEIGHT / scaled_height
    return canvas_x, canvas_y


def scaled_mouse_x():
    canvas_x, _ = canvas_mouse_position()
    return dudraw_backend._xmin + canvas_x * (dudraw_backend._xmax - dudraw_backend._xmin) / CANVAS_WIDTH


def scaled_mouse_y():
    _, canvas_y = canvas_mouse_position()
    return dudraw_backend._ymax - canvas_y * (dudraw_backend._ymax - dudraw_backend._ymin) / CANVAS_HEIGHT


def show_scaled_canvas():
    dudraw_backend._background.fill((0, 0, 0))
    offset_x, offset_y, scaled_width, scaled_height = DISPLAY_RECT

    if scaled_width == CANVAS_WIDTH and scaled_height == CANVAS_HEIGHT:
        dudraw_backend._background.blit(dudraw_backend._surface, (offset_x, offset_y))
    else:
        scaled_surface = pygame.transform.smoothscale(dudraw_backend._surface, (scaled_width, scaled_height))
        dudraw_backend._background.blit(scaled_surface, (offset_x, offset_y))

    pygame.display.flip()
    dudraw_backend._check_for_events()


def apply_display_mode(fullscreen):
    global DISPLAY_RECT

    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_width, screen_height = screen.get_size()
        scale = min(screen_width / CANVAS_WIDTH, screen_height / CANVAS_HEIGHT)
        scaled_width = int(CANVAS_WIDTH * scale)
        scaled_height = int(CANVAS_HEIGHT * scale)
        DISPLAY_RECT = (
            (screen_width - scaled_width) // 2,
            (screen_height - scaled_height) // 2,
            scaled_width,
            scaled_height,
        )
    else:
        pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
        DISPLAY_RECT = (0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)

    dudraw_backend._background = pygame.display.get_surface()


def toggle_fullscreen(settings):
    settings["fullscreen"] = not settings["fullscreen"]
    apply_display_mode(settings["fullscreen"])


def setup_canvas():
    dudraw.set_canvas_size(CANVAS_WIDTH, CANVAS_HEIGHT)
    dudraw.set_x_scale(0, GRID_WIDTH)
    dudraw.set_y_scale(0, GRID_HEIGHT + 2)
    dudraw_backend._show = show_scaled_canvas
    dudraw.mouse_x = scaled_mouse_x
    dudraw.mouse_y = scaled_mouse_y


def draw_background_details(x, y):
    dudraw.set_pen_color_rgb(130, 176, 95)
    if (x * 3 + y * 5) % 7 == 0:
        dudraw.line(x + 0.12, y + 0.12, x + 0.2, y + 0.34)
        dudraw.line(x + 0.2, y + 0.12, x + 0.3, y + 0.31)

    if (x * 11 + y * 13) % 31 == 0:
        dudraw.set_pen_color_rgb(104, 129, 95)
        dudraw.filled_circle(x + 0.82, y + 0.18, 0.055)
        dudraw.set_pen_color_rgb(84, 103, 79)
        dudraw.filled_circle(x + 0.86, y + 0.2, 0.027)

    if (x * 7 + y * 11) % 17 == 0:
        dudraw.set_pen_color_rgb(114, 157, 87)
        dudraw.filled_circle(x + 0.18, y + 0.25, 0.05)
        dudraw.filled_circle(x + 0.28, y + 0.2, 0.04)
        dudraw.filled_circle(x + 0.22, y + 0.12, 0.04)
    elif (x * 5 + y * 3) % 23 == 0:
        dudraw.set_pen_color_rgb(232, 221, 148)
        dudraw.filled_circle(x + 0.68, y + 0.72, 0.035)
        dudraw.filled_circle(x + 0.76, y + 0.66, 0.03)
        dudraw.set_pen_color_rgb(214, 144, 174)
        dudraw.filled_circle(x + 0.72, y + 0.69, 0.018)

    if (x * 17 + y * 7) % 37 == 0:
        dudraw.set_pen_color_rgb(93, 139, 82)
        dudraw.line(x + 0.62, y + 0.21, x + 0.72, y + 0.38)
        dudraw.line(x + 0.72, y + 0.38, x + 0.82, y + 0.24)


def pixel_color_for_tile(tile_type, x, y, px, py):
    noise = (x * 37 + y * 53 + px * 11 + py * 17 + px * py) % 100

    if tile_type == "path":
        if px in (0, 1, 30, 31) or py in (0, 1, 30, 31):
            return (116, 86, 54)
        if noise < 9:
            return (144, 108, 68)
        if noise < 28:
            return (189, 151, 96)
        if (px + py + x) % 13 == 0:
            return (226, 196, 132)

        return (204, 171, 112)

    if px in (0, 31) or py in (0, 31):
        return (117, 159, 97)
    if noise < 12:
        return (130, 183, 95)
    if noise < 26:
        return (158, 209, 118)
    if noise > 95:
        return (231, 224, 129)
    if (px - py + x * 2 + y) % 19 == 0:
        return (94, 143, 75)

    return (177, 221, 136) if (x + y) % 2 == 0 else (158, 207, 121)


def draw_32_pixel_tile(x, y, tile_type):
    pixel_size = 1 / 32
    half_pixel = pixel_size / 2

    for py in range(32):
        run_color = None
        run_start = 0

        for px in range(33):
            if px < 32:
                color = pixel_color_for_tile(tile_type, x, y, px, py)
            else:
                color = None

            if px == 0:
                run_color = color
                run_start = 0
            elif color != run_color:
                run_len = px - run_start
                center_x = x + (run_start + run_len / 2) * pixel_size
                center_y = y + (py + 0.5) * pixel_size
                set_color(run_color)
                dudraw.filled_rectangle(center_x, center_y, run_len * half_pixel, half_pixel)
                run_color = color
                run_start = px


def draw_ambient_effects(settings, frame):
    if not is_amazing(settings):
        return

    for i in range(18):
        x = ((i * 7 + frame * 0.025) % GRID_WIDTH) + 0.15
        y = ((i * 5 + frame * 0.012) % GRID_HEIGHT) + 0.15
        size = 0.035 + (i % 3) * 0.015

        if (int(x), int(y)) not in PATH_SQUARES:
            dudraw.set_pen_color_rgb(235, 242, 181)
            dudraw.filled_circle(x, y, size)

    for i in range(8):
        x = (i * 3.1 + math.sin(frame * 0.018 + i) * 0.35) % GRID_WIDTH
        y = 1.0 + ((i * 2.4 + frame * 0.018) % (GRID_HEIGHT - 1))
        dudraw.set_pen_color_rgb(112, 172, 178)
        dudraw.circle(x, y, 0.11 + 0.03 * math.sin(frame * 0.09 + i))


def draw_polished_tree(x, y, scale, frame):
    sway = math.sin(frame * 0.028 + x) * 0.05 * scale
    dudraw.set_pen_color_rgb(50, 102, 60)
    dudraw.filled_ellipse(x + 0.16 * scale, y - 0.12 * scale, 0.78 * scale, 0.18 * scale)
    dudraw.set_pen_color_rgb(91, 57, 38)
    dudraw.filled_rectangle(x, y + 0.22 * scale, 0.11 * scale, 0.42 * scale)
    dudraw.set_pen_color_rgb(122, 72, 38)
    dudraw.line(x, y + 0.35 * scale, x - 0.31 * scale + sway, y + 0.66 * scale)
    dudraw.line(x, y + 0.43 * scale, x + 0.33 * scale + sway, y + 0.79 * scale)
    dudraw.set_pen_color_rgb(49, 119, 67)
    dudraw.filled_circle(x - 0.32 * scale + sway, y + 0.74 * scale, 0.31 * scale)
    dudraw.filled_circle(x + 0.29 * scale + sway, y + 0.82 * scale, 0.36 * scale)
    dudraw.set_pen_color_rgb(69, 145, 76)
    dudraw.filled_circle(x + sway, y + 1.02 * scale, 0.45 * scale)
    dudraw.set_pen_color_rgb(128, 188, 99)
    dudraw.filled_circle(x - 0.12 * scale + sway, y + 1.13 * scale, 0.17 * scale)
    dudraw.set_pen_color_rgb(235, 169, 67)
    dudraw.filled_circle(x + 0.24 * scale + sway, y + 0.9 * scale, 0.045 * scale)
    dudraw.filled_circle(x - 0.27 * scale + sway, y + 0.78 * scale, 0.04 * scale)


def draw_polished_meadow(frame):
    # Continuous painted ground replaces tile boundaries for the polished edition.
    dudraw.set_pen_color_rgb(90, 158, 93)
    dudraw.filled_rectangle(GRID_WIDTH / 2, GRID_HEIGHT / 2, GRID_WIDTH / 2, GRID_HEIGHT / 2)
    dudraw.set_pen_color_rgb(64, 120, 76)
    dudraw.filled_ellipse(4.0, 15.8, 8.8, 2.4)
    dudraw.filled_ellipse(17.0, 15.8, 10.8, 2.6)
    dudraw.set_pen_color_rgb(112, 179, 101)
    dudraw.filled_ellipse(5.2, 13.8, 8.0, 3.0)
    dudraw.filled_ellipse(19.7, 2.1, 8.8, 3.2)
    dudraw.set_pen_color_rgb(77, 139, 86)
    dudraw.filled_ellipse(20.6, 14.7, 8.5, 2.35)
    dudraw.filled_ellipse(4.1, 1.05, 7.2, 1.8)

    # Moving cloud shade washes softly over the lawn.
    shade_x = (frame * 0.012) % 30 - 3
    dudraw.set_pen_color_rgb(82, 147, 90)
    dudraw.filled_ellipse(shade_x, 9.0, 2.7, 0.55)
    dudraw.filled_ellipse(shade_x + 2.4, 8.7, 2.0, 0.43)

    # A creek and lily pond sit below and inside the looping garden walk.
    dudraw.set_pen_color_rgb(49, 121, 130)
    dudraw.filled_rectangle(12, 1.7, 12, 0.42)
    dudraw.set_pen_color_rgb(65, 154, 158)
    for segment in range(12):
        water_x = segment * 2.15 + (frame * 0.015) % 2.15 - 1.0
        dudraw.line(water_x, 1.75, water_x + 0.72, 1.82)
        dudraw.line(water_x + 0.32, 1.5, water_x + 1.08, 1.57)
    dudraw.set_pen_color_rgb(44, 111, 119)
    dudraw.filled_ellipse(11.8, 8.1, 2.35, 1.38)
    dudraw.set_pen_color_rgb(67, 157, 155)
    dudraw.filled_ellipse(11.8, 8.17, 2.14, 1.22)
    for index in range(4):
        ripple = 0.16 + ((frame * 0.012 + index * 0.37) % 0.55)
        dudraw.set_pen_color_rgb(137, 203, 185)
        dudraw.ellipse(11.1 + index * 0.47, 8.02 + (index % 2) * 0.32, ripple, ripple * 0.4)
    dudraw.set_pen_color_rgb(71, 138, 79)
    dudraw.filled_circle(10.62, 8.45, 0.16)
    dudraw.filled_circle(12.53, 7.85, 0.2)
    dudraw.set_pen_color_rgb(242, 183, 202)
    dudraw.filled_circle(10.62, 8.48, 0.045)
    dudraw.set_pen_color_rgb(246, 229, 149)
    dudraw.filled_circle(12.53, 7.89, 0.045)

    # Rustic border fences and an orchard frame the original estate meadow.
    dudraw.set_pen_color_rgb(110, 73, 43)
    for post_x in range(1, 24, 2):
        dudraw.filled_rectangle(post_x, 14.95, 0.045, 0.3)
        if post_x < 23:
            dudraw.line(post_x, 15.02, post_x + 2, 15.02)
            dudraw.line(post_x, 14.8, post_x + 2, 14.8)
    for tree_x, tree_y, tree_scale in ((1.25, 2.2, 1.0), (3.05, 2.65, 0.82), (20.9, 13.2, 0.9), (22.65, 13.7, 1.05), (20.9, 5.2, 0.7)):
        draw_polished_tree(tree_x, tree_y, tree_scale, frame)

    # A tiny footbridge marks the creek without occupying the enemy road.
    dudraw.set_pen_color_rgb(101, 64, 39)
    dudraw.filled_rectangle(4.1, 1.72, 1.05, 0.26)
    dudraw.set_pen_color_rgb(183, 126, 68)
    for plank in range(6):
        plank_x = 3.25 + plank * 0.34
        dudraw.filled_rectangle(plank_x, 1.75, 0.14, 0.22)
    dudraw.set_pen_color_rgb(215, 162, 87)
    dudraw.line(3.1, 2.08, 5.12, 2.08)

    # Shrubs, flower groups, and grasses leave build space legible but natural.
    for index in range(72):
        x = 0.55 + (index * 5.37) % 23.0
        y = 0.5 + (index * 3.13) % 15.0
        if (int(x), int(y)) in PATH_SQUARES:
            continue
        sway = math.sin(frame * 0.045 + index) * 0.035
        dudraw.set_pen_color_rgb(61, 124, 69)
        dudraw.line(x, y - 0.06, x + sway, y + 0.24)
        dudraw.line(x + 0.02, y + 0.04, x + 0.15 + sway, y + 0.17)
        if index % 4 == 0:
            dudraw.set_pen_color_rgb(244, 218, 115)
            dudraw.filled_circle(x + sway, y + 0.27, 0.045)
        elif index % 5 == 0:
            dudraw.set_pen_color_rgb(240, 163, 184)
            dudraw.filled_circle(x + sway, y + 0.27, 0.045)

    # A few drifting leaves and fireflies make the backdrop feel alive.
    for index in range(26):
        x = (index * 3.7 + frame * (0.009 + (index % 3) * 0.004)) % GRID_WIDTH
        y = 0.4 + (index * 2.07 + math.sin(frame * 0.022 + index) * 0.3) % (GRID_HEIGHT - 0.8)
        if (int(x), int(y)) in PATH_SQUARES:
            continue
        if index % 2 == 0:
            dudraw.set_pen_color_rgb(255, 230, 130)
            dudraw.filled_circle(x, y, 0.035 + 0.012 * math.sin(frame * 0.15 + index))
            dudraw.set_pen_color_rgb(252, 240, 171)
            dudraw.circle(x, y, 0.095)
        else:
            dudraw.set_pen_color_rgb(157, 194, 94)
            dudraw.filled_ellipse(x, y, 0.07, 0.035)


def draw_polished_path(settings, frame):
    theme = CURRENT_MAP["theme"]

    # Rounded road layers form a garden trail rather than visible square cells.
    set_color(theme["edge"])
    for index, (x, y) in enumerate(PATH):
        dudraw.filled_circle(x, y, 0.66)
        if index + 1 < len(PATH):
            next_x, next_y = PATH[index + 1]
            dudraw.filled_rectangle((x + next_x) / 2, (y + next_y) / 2, abs(next_x - x) / 2 + 0.65, abs(next_y - y) / 2 + 0.65)
    set_color(theme["path"])
    for index, (x, y) in enumerate(PATH):
        dudraw.filled_circle(x, y, 0.51)
        if index + 1 < len(PATH):
            next_x, next_y = PATH[index + 1]
            dudraw.filled_rectangle((x + next_x) / 2, (y + next_y) / 2, abs(next_x - x) / 2 + 0.5, abs(next_y - y) / 2 + 0.5)

    # Soft cart tracks, cobbles, and verge grass provide detail without grid cells.
    dudraw.set_pen_color_rgb(183, 148, 99)
    for index, (x, y) in enumerate(PATH[:-1]):
        next_x, next_y = PATH[index + 1]
        dx = next_x - x
        dy = next_y - y
        side_x = -dy
        side_y = dx
        for offset in (-0.22, 0.22):
            dudraw.line(x + side_x * offset, y + side_y * offset, next_x + side_x * offset, next_y + side_y * offset)

    dudraw.set_pen_color_rgb(229, 205, 154)
    for index, (x, y) in enumerate(PATH):
        if index % 3 == 1:
            dudraw.filled_circle(x + 0.14, y - 0.14, 0.035)
        elif index % 3 == 2:
            dudraw.filled_circle(x - 0.2, y + 0.1, 0.028)
        if index % 4 == 0:
            dudraw.set_pen_color_rgb(92, 145, 75)
            dudraw.line(x - 0.59, y + 0.17, x - 0.64, y + 0.37)
            dudraw.line(x - 0.59, y + 0.17, x - 0.49, y + 0.34)
            dudraw.set_pen_color_rgb(229, 205, 154)

    # The entrance and exit gain estate-style stone markers.
    for marker_x, marker_y in ((0.48, 13.25), (23.48, 11.25)):
        dudraw.set_pen_color_rgb(89, 79, 65)
        dudraw.filled_rectangle(marker_x, marker_y, 0.14, 0.38)
        dudraw.set_pen_color_rgb(166, 151, 126)
        dudraw.filled_rectangle(marker_x, marker_y + 0.37, 0.18, 0.05)
        dudraw.filled_circle(marker_x, marker_y + 0.51, 0.09)

    if settings.get("show_path_arrows", True):
        dudraw.set_pen_color_rgb(119, 87, 53)
        for index in range(2, len(PATH) - 1, 7):
            x, y = PATH[index]
            next_x, next_y = PATH[index + 1]
            dx = next_x - x
            dy = next_y - y
            dudraw.filled_triangle(x + dx * 0.18, y + dy * 0.18, x - dx * 0.12 - dy * 0.11, y - dy * 0.12 + dx * 0.11, x - dx * 0.12 + dy * 0.11, y - dy * 0.12 - dx * 0.11)

        start_x, start_y = PATH[0]
        end_x, end_y = PATH[-1]
        dudraw.set_pen_color_rgb(79, 158, 95)
        dudraw.filled_circle(start_x, start_y, 0.2)
        dudraw.set_pen_color_rgb(196, 68, 65)
        dudraw.filled_circle(end_x, end_y, 0.2)


def draw_desert_palm(x, y, scale, frame):
    sway = math.sin(frame * 0.032 + x) * 0.09 * scale
    dudraw.set_pen_color_rgb(127, 77, 37)
    dudraw.line(x, y, x + sway * 0.25, y + 0.55 * scale)
    dudraw.line(x + sway * 0.25, y + 0.55 * scale, x + sway, y + 1.12 * scale)
    dudraw.set_pen_color_rgb(181, 112, 49)
    for knot in range(3):
        knot_y = y + (0.2 + knot * 0.25) * scale
        dudraw.line(x - 0.08 * scale, knot_y, x + 0.08 * scale, knot_y + 0.04 * scale)
    top_x = x + sway
    top_y = y + 1.12 * scale
    dudraw.set_pen_color_rgb(45, 113, 70)
    for leaf_x, leaf_y in ((-0.72, 0.2), (-0.48, 0.45), (0.0, 0.48), (0.46, 0.4), (0.74, 0.14)):
        dudraw.filled_triangle(top_x, top_y, top_x + leaf_x * scale, top_y + leaf_y * scale, top_x + leaf_x * 0.75 * scale, top_y - 0.08 * scale)
    dudraw.set_pen_color_rgb(88, 148, 77)
    dudraw.filled_circle(top_x - 0.1 * scale, top_y + 0.03 * scale, 0.06 * scale)


def draw_polished_desert(frame):
    # Broad ungridded dunes layer the desert into a warm, open landscape.
    dudraw.set_pen_color_rgb(207, 158, 81)
    dudraw.filled_rectangle(GRID_WIDTH / 2, GRID_HEIGHT / 2, GRID_WIDTH / 2, GRID_HEIGHT / 2)
    dudraw.set_pen_color_rgb(234, 190, 107)
    dudraw.filled_ellipse(4.5, 14.9, 8.0, 2.8)
    dudraw.filled_ellipse(19.2, 2.0, 9.5, 3.0)
    dudraw.set_pen_color_rgb(190, 136, 67)
    dudraw.filled_ellipse(20.4, 15.6, 8.2, 2.35)
    dudraw.filled_ellipse(3.0, 0.15, 7.0, 1.65)

    # Heat shadows drift over the sand while wind redraws fine dune ridges.
    heat_x = (frame * 0.014) % 32 - 4
    dudraw.set_pen_color_rgb(198, 146, 72)
    dudraw.filled_ellipse(heat_x, 10.0, 3.3, 0.38)
    dudraw.filled_ellipse(heat_x + 3.2, 9.75, 2.5, 0.25)
    dudraw.set_pen_color_rgb(239, 202, 125)
    for ridge in range(18):
        ridge_x = ((ridge * 2.1 + frame * 0.01) % 27) - 1.5
        ridge_y = 0.7 + (ridge * 3.21) % 14.1
        if (int(ridge_x), int(ridge_y)) not in PATH_SQUARES:
            dudraw.line(ridge_x, ridge_y, ridge_x + 0.9, ridge_y + 0.06)
            dudraw.line(ridge_x + 1.05, ridge_y + 0.06, ridge_x + 1.45, ridge_y + 0.04)

    # A shaded oasis and palms occupy the quiet basin between the road turns.
    dudraw.set_pen_color_rgb(153, 118, 58)
    dudraw.filled_ellipse(3.5, 9.4, 3.1, 1.8)
    dudraw.set_pen_color_rgb(38, 122, 139)
    dudraw.filled_ellipse(3.5, 9.5, 2.55, 1.36)
    dudraw.set_pen_color_rgb(62, 170, 178)
    dudraw.filled_ellipse(3.5, 9.57, 2.33, 1.18)
    for ripple in range(5):
        water_x = 1.8 + ripple * 0.76
        width = 0.22 + ((frame * 0.01 + ripple * 0.2) % 0.35)
        dudraw.set_pen_color_rgb(149, 222, 211)
        dudraw.ellipse(water_x, 9.45 + (ripple % 2) * 0.32, width, width * 0.32)
    for palm_x, palm_y, palm_scale in ((1.3, 9.6, 1.05), (5.7, 9.05, 0.9), (4.95, 10.48, 0.72)):
        draw_desert_palm(palm_x, palm_y, palm_scale, frame)

    # Weathered temple fragments make the upper plateau feel ancient and built.
    dudraw.set_pen_color_rgb(143, 101, 58)
    dudraw.filled_rectangle(19.6, 11.38, 3.08, 0.16)
    dudraw.set_pen_color_rgb(191, 143, 79)
    dudraw.filled_rectangle(19.6, 11.58, 2.75, 0.12)
    for column_x, height in ((17.75, 1.65), (18.85, 2.18), (20.0, 1.8), (22.1, 2.35)):
        dudraw.set_pen_color_rgb(176, 128, 70)
        dudraw.filled_rectangle(column_x, 11.75 + height / 2, 0.23, height / 2)
        dudraw.set_pen_color_rgb(226, 183, 104)
        dudraw.filled_rectangle(column_x, 11.82 + height, 0.3, 0.07)
        dudraw.set_pen_color_rgb(135, 93, 52)
        dudraw.line(column_x - 0.12, 12.0, column_x + 0.1, 12.17)
    dudraw.set_pen_color_rgb(193, 143, 78)
    dudraw.filled_triangle(17.35, 14.32, 22.55, 14.32, 19.95, 15.42)
    dudraw.set_pen_color_rgb(117, 82, 49)
    dudraw.filled_circle(19.95, 14.56, 0.2)
    dudraw.set_pen_color_rgb(232, 191, 108)
    dudraw.circle(19.95, 14.56, 0.26)

    # Broken pottery, cacti, and rolling tumbleweed fill open sand sparingly.
    for cactus_x, cactus_y, cactus_scale in ((11.0, 5.8, 0.75), (19.7, 4.4, 0.65), (13.0, 9.0, 0.5)):
        dudraw.set_pen_color_rgb(54, 116, 66)
        dudraw.filled_rectangle(cactus_x, cactus_y, 0.09 * cactus_scale, 0.42 * cactus_scale)
        dudraw.line(cactus_x, cactus_y + 0.12 * cactus_scale, cactus_x - 0.22 * cactus_scale, cactus_y + 0.27 * cactus_scale)
        dudraw.line(cactus_x, cactus_y + 0.2 * cactus_scale, cactus_x + 0.24 * cactus_scale, cactus_y + 0.38 * cactus_scale)
    dudraw.set_pen_color_rgb(154, 79, 45)
    dudraw.filled_ellipse(12.4, 11.0, 0.21, 0.15)
    dudraw.filled_ellipse(12.82, 10.9, 0.14, 0.12)
    tumble_x = (frame * 0.018) % 26 - 1
    tumble_y = 7.35 + math.sin(frame * 0.085) * 0.06
    dudraw.set_pen_color_rgb(144, 101, 46)
    dudraw.circle(tumble_x, tumble_y, 0.2)
    dudraw.line(tumble_x - 0.15, tumble_y - 0.12, tumble_x + 0.16, tumble_y + 0.11)
    dudraw.line(tumble_x - 0.15, tumble_y + 0.1, tumble_x + 0.16, tumble_y - 0.11)

    # Airborne sand motes supply low-contrast movement behind placed towers.
    dudraw.set_pen_color_rgb(248, 218, 145)
    for mote in range(24):
        x = (mote * 3.17 + frame * (0.018 + mote % 3 * 0.005)) % GRID_WIDTH
        y = 0.45 + (mote * 2.29 + math.sin(frame * 0.028 + mote) * 0.12) % 15
        if (int(x), int(y)) not in PATH_SQUARES:
            dudraw.filled_circle(x, y, 0.018 + (mote % 3) * 0.009)


def draw_polished_desert_path(settings, frame):
    theme = CURRENT_MAP["theme"]

    # A sunken sandstone causeway follows the original Desert Ruins route.
    set_color(theme["edge"])
    for index, (x, y) in enumerate(PATH):
        dudraw.filled_circle(x, y, 0.66)
        if index + 1 < len(PATH):
            next_x, next_y = PATH[index + 1]
            dudraw.filled_rectangle((x + next_x) / 2, (y + next_y) / 2, abs(next_x - x) / 2 + 0.65, abs(next_y - y) / 2 + 0.65)
    set_color(theme["path"])
    for index, (x, y) in enumerate(PATH):
        dudraw.filled_circle(x, y, 0.51)
        if index + 1 < len(PATH):
            next_x, next_y = PATH[index + 1]
            dudraw.filled_rectangle((x + next_x) / 2, (y + next_y) / 2, abs(next_x - x) / 2 + 0.5, abs(next_y - y) / 2 + 0.5)

    dudraw.set_pen_color_rgb(211, 165, 92)
    for index, (x, y) in enumerate(PATH):
        if index % 2 == 0:
            dudraw.filled_rectangle(x + 0.17, y - 0.14, 0.12, 0.055)
        if index % 5 == 0:
            dudraw.set_pen_color_rgb(117, 82, 49)
            dudraw.line(x - 0.26, y + 0.12, x + 0.14, y - 0.08)
            dudraw.set_pen_color_rgb(211, 165, 92)

    for marker_x, marker_y in ((0.48, 3.25), (23.48, 6.78)):
        dudraw.set_pen_color_rgb(150, 105, 56)
        dudraw.filled_rectangle(marker_x, marker_y, 0.15, 0.39)
        dudraw.set_pen_color_rgb(219, 172, 92)
        dudraw.filled_triangle(marker_x - 0.2, marker_y + 0.38, marker_x + 0.2, marker_y + 0.38, marker_x, marker_y + 0.62)

    if settings.get("show_path_arrows", True):
        dudraw.set_pen_color_rgb(105, 70, 39)
        for index in range(2, len(PATH) - 1, 7):
            x, y = PATH[index]
            next_x, next_y = PATH[index + 1]
            dx = next_x - x
            dy = next_y - y
            dudraw.filled_triangle(x + dx * 0.18, y + dy * 0.18, x - dx * 0.12 - dy * 0.11, y - dy * 0.12 + dx * 0.11, x - dx * 0.12 + dy * 0.11, y - dy * 0.12 - dx * 0.11)
        dudraw.set_pen_color_rgb(68, 145, 91)
        dudraw.filled_circle(PATH[0][0], PATH[0][1], 0.2)
        dudraw.set_pen_color_rgb(186, 62, 57)
        dudraw.filled_circle(PATH[-1][0], PATH[-1][1], 0.2)


def draw_polished_route(settings, edge, surface, highlight, accent):
    set_color(edge)
    for index, (x, y) in enumerate(PATH):
        dudraw.filled_circle(x, y, 0.66)
        if index + 1 < len(PATH):
            next_x, next_y = PATH[index + 1]
            dudraw.filled_rectangle((x + next_x) / 2, (y + next_y) / 2, abs(next_x - x) / 2 + 0.65, abs(next_y - y) / 2 + 0.65)
    set_color(surface)
    for index, (x, y) in enumerate(PATH):
        dudraw.filled_circle(x, y, 0.51)
        if index + 1 < len(PATH):
            next_x, next_y = PATH[index + 1]
            dudraw.filled_rectangle((x + next_x) / 2, (y + next_y) / 2, abs(next_x - x) / 2 + 0.5, abs(next_y - y) / 2 + 0.5)
        if index % 3 == 1:
            set_color(highlight)
            dudraw.filled_circle(x + 0.16, y - 0.13, 0.032)
            set_color(surface)
    if settings.get("show_path_arrows", True):
        set_color(accent)
        for index in range(2, len(PATH) - 1, 7):
            x, y = PATH[index]
            next_x, next_y = PATH[index + 1]
            dx = next_x - x
            dy = next_y - y
            dudraw.filled_triangle(x + dx * 0.18, y + dy * 0.18, x - dx * 0.12 - dy * 0.11, y - dy * 0.12 + dx * 0.11, x - dx * 0.12 + dy * 0.11, y - dy * 0.12 - dx * 0.11)
        dudraw.set_pen_color_rgb(75, 161, 101)
        dudraw.filled_circle(PATH[0][0], PATH[0][1], 0.2)
        dudraw.set_pen_color_rgb(201, 67, 68)
        dudraw.filled_circle(PATH[-1][0], PATH[-1][1], 0.2)


def draw_polished_mountain(frame):
    dudraw.set_pen_color_rgb(78, 104, 102)
    dudraw.filled_rectangle(12, 8, 12, 8)
    # Mountain walls, snow shelves, and lower valley floor give the pass depth.
    for x, peak_y, base_y, shade in ((1.5, 15.3, 10.7, (50, 65, 73)), (5.5, 15.8, 9.8, (56, 73, 80)), (10.2, 14.9, 10.6, (65, 84, 87)), (16.0, 15.9, 9.5, (48, 64, 72)), (21.8, 15.4, 10.3, (58, 76, 80))):
        set_color(shade)
        dudraw.filled_triangle(x - 3.6, base_y, x + 3.6, base_y, x, peak_y)
        dudraw.set_pen_color_rgb(227, 237, 236)
        dudraw.filled_triangle(x - 0.8, peak_y - 1.35, x + 0.8, peak_y - 1.35, x, peak_y)
        dudraw.set_pen_color_rgb(179, 199, 199)
        dudraw.line(x - 0.34, peak_y - 1.02, x - 1.12, peak_y - 2.0)
    dudraw.set_pen_color_rgb(101, 136, 115)
    dudraw.filled_ellipse(4.9, 2.0, 7.7, 2.25)
    dudraw.filled_ellipse(21.8, 7.0, 4.1, 2.0)

    # A glacial lake catches a waterfall dropping from the high ledge.
    dudraw.set_pen_color_rgb(39, 94, 114)
    dudraw.filled_ellipse(14.3, 7.0, 2.42, 1.2)
    dudraw.set_pen_color_rgb(71, 146, 161)
    dudraw.filled_ellipse(14.3, 7.05, 2.18, 1.02)
    dudraw.set_pen_color_rgb(150, 208, 212)
    for i in range(5):
        dudraw.line(13.0 + i * 0.48, 6.9, 13.45 + i * 0.48, 6.96 + math.sin(frame * 0.04 + i) * 0.05)
    waterfall_offset = (frame * 0.018) % 0.34
    dudraw.set_pen_color_rgb(182, 225, 226)
    for fall in range(4):
        fx = 16.0 + fall * 0.12
        dudraw.line(fx, 10.45 - waterfall_offset, fx - 0.12, 7.88 - waterfall_offset)
    dudraw.set_pen_color_rgb(216, 241, 239)
    dudraw.filled_circle(15.94, 7.75, 0.1 + 0.02 * math.sin(frame * 0.14))
    for tree_x, tree_y, size in ((1.4, 5.4, 1.0), (2.8, 6.1, 0.8), (21.0, 8.0, 1.1), (22.7, 3.0, 0.9), (7.3, 12.0, 0.65), (6.2, 5.3, 0.85), (22.0, 9.1, 0.72)):
        dudraw.set_pen_color_rgb(66, 52, 37)
        dudraw.filled_rectangle(tree_x, tree_y, 0.08 * size, 0.32 * size)
        dudraw.set_pen_color_rgb(31, 89, 70)
        dudraw.filled_triangle(tree_x - 0.45 * size, tree_y + 0.2 * size, tree_x + 0.45 * size, tree_y + 0.2 * size, tree_x, tree_y + 1.25 * size)
        dudraw.set_pen_color_rgb(48, 113, 82)
        dudraw.filled_triangle(tree_x - 0.37 * size, tree_y + 0.55 * size, tree_x + 0.37 * size, tree_y + 0.55 * size, tree_x, tree_y + 1.38 * size)
    # Cliff lodge and rope bridge sit in the quiet valley pocket.
    dudraw.set_pen_color_rgb(94, 60, 38)
    dudraw.filled_rectangle(7.3, 6.5, 0.62, 0.42)
    dudraw.set_pen_color_rgb(58, 44, 39)
    dudraw.filled_triangle(6.55, 6.88, 8.05, 6.88, 7.3, 7.47)
    dudraw.set_pen_color_rgb(246, 206, 97)
    dudraw.filled_rectangle(7.33, 6.56, 0.13, 0.14)
    dudraw.set_pen_color_rgb(119, 83, 47)
    dudraw.line(11.3, 11.0, 15.1, 11.0)
    dudraw.line(11.3, 11.42, 15.1, 11.42)
    for plank in range(9):
        bx = 11.45 + plank * 0.4
        dudraw.line(bx, 10.98, bx, 11.37 + math.sin(plank * 0.7) * 0.04)
    # High circling birds and falling snow keep the alpine horizon in motion.
    dudraw.set_pen_color_rgb(40, 52, 58)
    bird_x = 12.0 + math.sin(frame * 0.018) * 2.4
    dudraw.arc(bird_x - 0.13, 13.6, 0.18, 0, 160)
    dudraw.arc(bird_x + 0.13, 13.6, 0.18, 20, 180)
    dudraw.set_pen_color_rgb(232, 241, 238)
    for i in range(28):
        x = (i * 2.9 + frame * 0.012) % 24
        y = 0.5 + (i * 1.83 + frame * 0.008) % 15
        dudraw.filled_circle(x, y, 0.018 + (i % 3) * 0.01)


def draw_polished_ocean(frame):
    dudraw.set_pen_color_rgb(31, 116, 155)
    dudraw.filled_rectangle(12, 8, 12, 8)
    dudraw.set_pen_color_rgb(52, 155, 181)
    for wave in range(18):
        x = ((wave * 1.65 + frame * 0.018) % 27) - 1
        y = 0.65 + (wave * 3.29) % 14.7
        dudraw.line(x, y, x + 0.7, y + 0.06)
        dudraw.line(x + 0.85, y + 0.06, x + 1.16, y + 0.03)
    for island_x, island_y, wide in ((3.5, 12.5, 1.5), (9.5, 6.5, 1.45), (16.5, 4.5, 1.5), (21.0, 11.35, 0.94), (13.5, 14.5, 1.35), (7.5, 1.5, 1.35)):
        dudraw.set_pen_color_rgb(224, 202, 133)
        dudraw.filled_ellipse(island_x, island_y, wide, 0.62)
        dudraw.set_pen_color_rgb(78, 156, 96)
        dudraw.filled_ellipse(island_x, island_y + 0.13, wide * 0.72, 0.39)
        dudraw.set_pen_color_rgb(245, 224, 148)
        dudraw.ellipse(island_x, island_y, wide, 0.62)
    for bubble in range(12):
        x = (bubble * 4.2 + frame * 0.01) % 24
        y = (bubble * 2.47 + frame * 0.02) % 16
        dudraw.set_pen_color_rgb(128, 211, 220)
        dudraw.circle(x, y, 0.04 + bubble % 3 * 0.02)
    draw_desert_palm(3.55, 12.62, 0.54, frame)
    draw_desert_palm(21.05, 11.48, 0.42, frame)


def draw_polished_temple(frame):
    dudraw.set_pen_color_rgb(164, 193, 150)
    dudraw.filled_rectangle(12, 8, 12, 8)
    dudraw.set_pen_color_rgb(190, 211, 168)
    dudraw.filled_ellipse(4.0, 13.0, 6.5, 2.2)
    dudraw.filled_ellipse(18.7, 2.3, 7.0, 2.5)
    dudraw.set_pen_color_rgb(50, 110, 116)
    dudraw.filled_ellipse(14.2, 8.2, 2.2, 1.25)
    dudraw.set_pen_color_rgb(85, 154, 150)
    dudraw.filled_ellipse(14.2, 8.27, 1.98, 1.08)
    for x in (13.3, 14.0, 14.75):
        dudraw.set_pen_color_rgb(241, 181, 191)
        dudraw.filled_circle(x, 8.25 + math.sin(frame * 0.03 + x) * 0.05, 0.045)
    for tx, ty in ((20.5, 9.1), (21.9, 9.7), (2.2, 2.1)):
        dudraw.set_pen_color_rgb(78, 49, 43)
        dudraw.filled_rectangle(tx, ty, 0.1, 0.45)
        dudraw.set_pen_color_rgb(190, 105, 124)
        dudraw.filled_circle(tx - 0.24, ty + 0.55, 0.36)
        dudraw.filled_circle(tx + 0.25, ty + 0.64, 0.4)
        dudraw.set_pen_color_rgb(239, 166, 190)
        dudraw.filled_circle(tx, ty + 0.82, 0.45)
    dudraw.set_pen_color_rgb(115, 52, 56)
    dudraw.filled_rectangle(2.9, 13.7, 1.7, 0.12)
    dudraw.filled_rectangle(2.9, 14.65, 1.55, 0.09)
    dudraw.filled_rectangle(1.62, 14.15, 0.08, 0.58)
    dudraw.filled_rectangle(4.18, 14.15, 0.08, 0.58)
    # Tiered shrine, arched garden bridge, lantern walk, and koi deepen the sanctuary.
    dudraw.set_pen_color_rgb(121, 57, 57)
    dudraw.filled_rectangle(21.1, 2.0, 1.45, 0.18)
    dudraw.filled_rectangle(21.1, 3.12, 1.25, 0.13)
    dudraw.set_pen_color_rgb(235, 211, 163)
    dudraw.filled_rectangle(21.1, 2.5, 0.94, 0.45)
    dudraw.set_pen_color_rgb(106, 42, 48)
    dudraw.filled_triangle(19.2, 3.1, 23.0, 3.1, 21.1, 4.05)
    dudraw.filled_triangle(19.55, 2.02, 22.65, 2.02, 21.1, 2.65)
    dudraw.set_pen_color_rgb(234, 184, 70)
    dudraw.filled_circle(21.1, 2.66, 0.08)
    dudraw.set_pen_color_rgb(164, 64, 70)
    dudraw.arc(14.2, 8.5, 1.2, 0, 180)
    dudraw.line(13.0, 8.48, 15.4, 8.48)
    for lantern_x, lantern_y in ((7.2, 12.3), (9.2, 12.3), (15.8, 5.1), (17.1, 5.1)):
        dudraw.set_pen_color_rgb(75, 52, 44)
        dudraw.line(lantern_x, lantern_y, lantern_x, lantern_y + 0.43)
        dudraw.set_pen_color_rgb(238, 96, 76)
        dudraw.filled_rectangle(lantern_x, lantern_y + 0.32, 0.1, 0.13)
        dudraw.set_pen_color_rgb(255, 217, 111)
        dudraw.filled_circle(lantern_x, lantern_y + 0.32, 0.045 + 0.008 * math.sin(frame * 0.12 + lantern_x))
    dudraw.set_pen_color_rgb(240, 120, 95)
    for koi in range(3):
        kx = 13.45 + koi * 0.56 + math.sin(frame * 0.03 + koi) * 0.12
        ky = 8.0 + (koi % 2) * 0.35
        dudraw.filled_ellipse(kx, ky, 0.12, 0.04)
        dudraw.filled_triangle(kx - 0.08, ky, kx - 0.18, ky + 0.07, kx - 0.18, ky - 0.07)
    # A tea pavilion, stone garden, bell tower, and bamboo fence fill the grounds.
    dudraw.set_pen_color_rgb(112, 55, 48)
    dudraw.filled_rectangle(2.8, 7.55, 1.1, 0.13)
    dudraw.set_pen_color_rgb(224, 203, 165)
    dudraw.filled_rectangle(2.8, 8.03, 0.82, 0.37)
    dudraw.set_pen_color_rgb(99, 41, 48)
    dudraw.filled_triangle(1.35, 8.41, 4.25, 8.41, 2.8, 9.08)
    dudraw.set_pen_color_rgb(224, 173, 73)
    dudraw.filled_circle(2.8, 8.08, 0.06)
    dudraw.set_pen_color_rgb(124, 128, 114)
    for stone_x, stone_y, stone_size in ((7.4, 2.1, 0.24), (8.05, 2.42, 0.18), (8.66, 2.08, 0.28), (9.43, 2.39, 0.16), (10.0, 2.14, 0.23)):
        dudraw.filled_ellipse(stone_x, stone_y, stone_size, stone_size * 0.53)
    dudraw.set_pen_color_rgb(201, 186, 145)
    for rake in range(4):
        dudraw.arc(8.8, 2.2, 1.1 + rake * 0.18, 190, 345)
    dudraw.set_pen_color_rgb(102, 48, 48)
    dudraw.filled_rectangle(16.0, 14.2, 0.18, 0.72)
    dudraw.filled_rectangle(16.0, 15.0, 0.44, 0.08)
    dudraw.set_pen_color_rgb(182, 132, 58)
    dudraw.filled_circle(16.0, 14.42, 0.18)
    dudraw.set_pen_color_rgb(227, 190, 91)
    dudraw.line(16.0, 14.25, 16.0, 14.1)
    dudraw.set_pen_color_rgb(76, 124, 69)
    for bamboo in range(7):
        bx = 12.7 + bamboo * 0.38
        dudraw.line(bx, 14.35, bx, 15.55 + math.sin(frame * 0.025 + bamboo) * 0.06)
        dudraw.line(bx, 14.85, bx + 0.2, 15.03)
    for petal in range(25):
        x = (petal * 3.13 + frame * 0.008) % 24
        y = (petal * 1.79 - frame * 0.012) % 16
        dudraw.set_pen_color_rgb(245, 186, 206)
        dudraw.filled_ellipse(x, y, 0.04, 0.025)


def draw_polished_racetrack(frame):
    dudraw.set_pen_color_rgb(43, 83, 59)
    dudraw.filled_rectangle(12, 8, 12, 8)
    dudraw.set_pen_color_rgb(58, 107, 69)
    dudraw.filled_ellipse(12, 8, 8.2, 4.4)
    dudraw.set_pen_color_rgb(27, 37, 41)
    dudraw.filled_rectangle(12, 15.15, 8.6, 0.55)
    dudraw.set_pen_color_rgb(136, 146, 151)
    for i in range(12):
        dudraw.filled_rectangle(4.0 + i * 1.45, 15.22, 0.6, 0.04)
    dudraw.set_pen_color_rgb(225, 225, 217)
    dudraw.filled_rectangle(12, 1.0, 4.1, 0.14)
    dudraw.set_pen_color_rgb(194, 47, 52)
    for pit in range(7):
        dudraw.filled_rectangle(8.8 + pit * 1.06, 1.23, 0.38, 0.18)
    for light_x in (3.0, 8.0, 16.0, 21.0):
        dudraw.set_pen_color_rgb(65, 71, 74)
        dudraw.line(light_x, 14.2, light_x, 15.1)
        dudraw.set_pen_color_rgb(255, 236, 158)
        dudraw.filled_circle(light_x, 15.15, 0.08 + 0.015 * math.sin(frame * 0.15 + light_x))
    banner = (frame // 12) % 2
    for flag in range(8):
        dudraw.set_pen_color_rgb(244, 244, 237) if (flag + banner) % 2 else dudraw.set_pen_color_rgb(32, 34, 37)
        dudraw.filled_rectangle(20.8 + flag * 0.25, 9.0, 0.12, 0.13)
    # Score tower, tire barriers, podium, and a circling pace-light sell the circuit.
    dudraw.set_pen_color_rgb(33, 39, 43)
    dudraw.filled_rectangle(2.1, 5.0, 0.7, 1.45)
    dudraw.set_pen_color_rgb(240, 64, 59)
    dudraw.filled_rectangle(2.1, 6.08, 0.58, 0.17)
    dudraw.set_pen_color_rgb(243, 232, 193)
    for row in range(3):
        dudraw.filled_rectangle(2.1, 5.7 - row * 0.3, 0.4, 0.035)
    for tire in range(9):
        dudraw.set_pen_color_rgb(30, 33, 35) if tire % 2 else dudraw.set_pen_color_rgb(218, 51, 51)
        dudraw.filled_circle(6.1 + tire * 0.46, 1.9, 0.17)
    dudraw.set_pen_color_rgb(215, 217, 211)
    dudraw.filled_rectangle(12.1, 7.7, 1.15, 0.22)
    dudraw.set_pen_color_rgb(238, 194, 45)
    dudraw.filled_rectangle(12.1, 8.08, 0.28, 0.18)
    dudraw.set_pen_color_rgb(185, 186, 182)
    dudraw.filled_rectangle(11.45, 7.99, 0.24, 0.12)
    dudraw.filled_rectangle(12.75, 7.91, 0.24, 0.08)
    light_pos = int(frame / 3) % len(PATH)
    light_x, light_y = PATH[light_pos]
    dudraw.set_pen_color_rgb(244, 48, 54)
    dudraw.filled_circle(light_x, light_y, 0.075)
    dudraw.set_pen_color_rgb(255, 202, 93)
    dudraw.circle(light_x, light_y, 0.14)


def draw_polished_war(frame):
    dudraw.set_pen_color_rgb(69, 76, 56)
    dudraw.filled_rectangle(12, 8, 12, 8)
    dudraw.set_pen_color_rgb(87, 89, 61)
    dudraw.filled_ellipse(5.5, 13.8, 7.0, 2.1)
    dudraw.set_pen_color_rgb(50, 53, 44)
    for cx, cy, size in ((2, 10, 0.8), (11, 8, 1.0), (20, 2, 0.7), (20, 12.5, 0.9)):
        dudraw.filled_ellipse(cx, cy, size, size * 0.45)
        dudraw.set_pen_color_rgb(113, 98, 70)
        dudraw.ellipse(cx, cy, size * 0.7, size * 0.33)
        dudraw.set_pen_color_rgb(50, 53, 44)
    dudraw.set_pen_color_rgb(48, 43, 37)
    dudraw.filled_rectangle(11.4, 1.0, 3.0, 0.42)
    dudraw.set_pen_color_rgb(108, 93, 67)
    for sandbag in range(8):
        dudraw.filled_ellipse(8.8 + sandbag * 0.72, 1.48 + (sandbag % 2) * 0.17, 0.34, 0.17)
    dudraw.set_pen_color_rgb(36, 38, 34)
    for post in range(6):
        x = 0.8 + post * 4.4
        dudraw.line(x, 15.1, x, 15.65)
        dudraw.line(x, 15.35, x + 3.4, 15.35)
        dudraw.line(x, 15.52, x + 3.4, 15.52)
    for smoke in range(5):
        rise = (frame * 0.012 + smoke * 0.4) % 1.4
        dudraw.set_pen_color_rgb(93, 94, 83)
        dudraw.filled_circle(19.6 + math.sin(frame * 0.03 + smoke) * 0.12, 10.4 + rise, 0.12 + rise * 0.07)
    # Destroyed armor, duckboards, warning lights, and distant shell flashes.
    dudraw.set_pen_color_rgb(43, 48, 39)
    dudraw.filled_rectangle(21.1, 8.7, 1.15, 0.35)
    dudraw.filled_ellipse(21.1, 8.35, 1.25, 0.22)
    dudraw.set_pen_color_rgb(76, 83, 60)
    dudraw.filled_rectangle(20.9, 9.08, 0.52, 0.22)
    dudraw.set_pen_color_rgb(38, 41, 35)
    dudraw.line(21.2, 9.12, 22.45, 9.48)
    dudraw.set_pen_color_rgb(129, 96, 57)
    for plank in range(8):
        dudraw.filled_rectangle(5.0 + plank * 0.38, 10.8, 0.16, 0.36)
    for lamp_x in (1.2, 13.8, 22.1):
        dudraw.set_pen_color_rgb(54, 48, 40)
        dudraw.line(lamp_x, 3.8, lamp_x, 4.4)
        dudraw.set_pen_color_rgb(217, 142, 49)
        dudraw.filled_circle(lamp_x, 4.43, 0.06 + 0.012 * math.sin(frame * 0.14 + lamp_x))
    if frame % 90 < 8:
        dudraw.set_pen_color_rgb(238, 185, 85)
        dudraw.circle(5.5, 5.0, 0.35 + frame % 8 * 0.06)
        dudraw.set_pen_color_rgb(245, 224, 169)
        dudraw.filled_circle(5.5, 5.0, 0.06)


def draw_polished_miami(frame):
    dudraw.set_pen_color_rgb(235, 188, 111)
    dudraw.filled_rectangle(12, 8, 12, 8)
    dudraw.set_pen_color_rgb(36, 151, 181)
    dudraw.filled_rectangle(2.4, 8, 2.4, 8)
    dudraw.set_pen_color_rgb(81, 201, 210)
    for wave in range(12):
        y = 0.7 + wave * 1.3
        x = (frame * 0.014 + wave * 0.36) % 1.1
        dudraw.line(0.2 + x, y, 1.4 + x, y + 0.06)
    dudraw.set_pen_color_rgb(250, 213, 137)
    dudraw.filled_rectangle(5.1, 8, 0.35, 8)
    dudraw.set_pen_color_rgb(46, 68, 92)
    for bx, width, height in ((17.0, 0.7, 2.3), (18.6, 0.9, 3.0), (20.4, 0.65, 2.0), (22.0, 1.05, 3.6)):
        dudraw.filled_rectangle(bx, 15.4 - height / 2, width, height / 2)
        dudraw.set_pen_color_rgb(247, 205, 98)
        for window in range(2):
            dudraw.filled_rectangle(bx, 15.05 - window * 0.45, width * 0.55, 0.05)
        dudraw.set_pen_color_rgb(46, 68, 92)
    for px, py, size in ((6.5, 2.0, 0.8), (11.0, 9.0, 0.65), (21.5, 6.0, 0.75)):
        draw_desert_palm(px, py, size, frame)
    for umbrella_x, color in ((7.8, (240, 75, 126)), (10.0, (57, 184, 192)), (15.8, (247, 205, 67))):
        set_color(color)
        dudraw.filled_triangle(umbrella_x - 0.5, 3.1, umbrella_x + 0.5, 3.1, umbrella_x, 3.55)
        dudraw.set_pen_color_rgb(113, 75, 50)
        dudraw.line(umbrella_x, 3.12, umbrella_x, 2.7)


def draw_polished_retro(frame):
    dudraw.set_pen_color_rgb(15, 14, 36)
    dudraw.filled_rectangle(12, 8, 12, 8)
    dudraw.set_pen_color_rgb(36, 27, 66)
    dudraw.filled_rectangle(12, 12, 12, 4)
    dudraw.set_pen_color_rgb(246, 71, 181)
    dudraw.filled_circle(12, 13.6, 1.75)
    dudraw.set_pen_color_rgb(255, 143, 103)
    for band in range(5):
        dudraw.line(10.4, 13.0 + band * 0.27, 13.6, 13.0 + band * 0.27)
    dudraw.set_pen_color_rgb(10, 12, 30)
    for bx, height in ((2.0, 1.9), (3.1, 2.8), (4.2, 1.5), (18.0, 2.2), (19.4, 3.0), (21.0, 1.8), (22.5, 2.6)):
        dudraw.filled_rectangle(bx, 12.0 - height / 2, 0.48, height / 2)
    for star in range(28):
        x = (star * 4.17 + frame * 0.006) % 24
        y = 9.2 + (star * 1.73) % 6.3
        dudraw.set_pen_color_rgb(116, 226, 242) if star % 2 else dudraw.set_pen_color_rgb(255, 222, 92)
        dudraw.filled_circle(x, y, 0.018 + star % 3 * 0.009)
    # Perspective floor, animated billboards, flying traffic, and tower windows.
    dudraw.set_pen_color_rgb(47, 44, 89)
    for line_y in (0.8, 1.7, 2.9, 4.5, 6.4, 8.2):
        dudraw.line(0, line_y, 24, line_y)
    for vanish_x in range(-12, 37, 3):
        dudraw.line(12, 9.1, vanish_x, 0)
    for bx, height in ((2.0, 1.9), (3.1, 2.8), (4.2, 1.5), (18.0, 2.2), (19.4, 3.0), (21.0, 1.8), (22.5, 2.6)):
        for window in range(int(height * 2)):
            dudraw.set_pen_color_rgb(37, 213, 206) if (window + int(frame / 20)) % 3 else dudraw.set_pen_color_rgb(250, 76, 190)
            dudraw.filled_rectangle(bx, 10.55 + window * 0.3, 0.13, 0.035)
    glow = 0.02 * math.sin(frame * 0.12)
    dudraw.set_pen_color_rgb(33, 224, 218)
    dudraw.rectangle(6.1, 12.2, 1.1, 0.53)
    dudraw.set_pen_color_rgb(249, 74, 187)
    dudraw.text(6.1, 12.18, "PLAY")
    dudraw.set_pen_color_rgb(251, 202, 73)
    dudraw.circle(6.1, 12.2, 1.16 + glow)
    car_x = (frame * 0.04) % 27 - 1.5
    dudraw.set_pen_color_rgb(247, 68, 184)
    dudraw.filled_rectangle(car_x, 7.4, 0.42, 0.09)
    dudraw.set_pen_color_rgb(82, 229, 236)
    dudraw.line(car_x - 0.45, 7.4, car_x - 1.15, 7.4)
    dudraw.line(car_x + 0.45, 7.4, car_x + 1.15, 7.4)
    # CRT television texture: scanlines, a rolling bright band, and white-noise scratches.
    dudraw.set_pen_color_rgb(27, 28, 54)
    for scan in range(0, 32, 2):
        dudraw.line(0, scan * 0.5 + 0.1, 24, scan * 0.5 + 0.1)
    scan_y = (frame * 0.07) % 18 - 1
    dudraw.set_pen_color_rgb(78, 84, 126)
    dudraw.line(0, scan_y, 24, scan_y)
    dudraw.line(0, scan_y + 0.08, 24, scan_y + 0.08)
    for noise in range(28):
        nx = (noise * 5.31 + frame * 0.43) % 24
        ny = (noise * 2.19 + frame * (0.05 + noise % 3 * 0.01)) % 16
        if noise % 3 == 0:
            dudraw.set_pen_color_rgb(181, 185, 200)
        elif noise % 3 == 1:
            dudraw.set_pen_color_rgb(48, 205, 208)
        else:
            dudraw.set_pen_color_rgb(229, 79, 178)
        dudraw.line(nx, ny, min(24, nx + 0.08 + (noise % 4) * 0.07), ny)
    if frame % 84 < 6:
        glitch_y = 3.0 + (frame % 6) * 1.13
        dudraw.set_pen_color_rgb(70, 224, 219)
        dudraw.line(0, glitch_y, 9.0, glitch_y)
        dudraw.set_pen_color_rgb(241, 59, 183)
        dudraw.line(11.0, glitch_y + 0.04, 24, glitch_y + 0.04)


def draw_crystal_cluster(x, y, size, frame):
    pulse = int(18 * (0.5 + 0.5 * math.sin(frame * 0.06 + x)))
    dudraw.set_pen_color_rgb(58 + pulse, 170 + pulse, 206 + pulse)
    dudraw.filled_triangle(x - 0.32 * size, y, x + 0.02 * size, y, x - 0.1 * size, y + 0.9 * size)
    dudraw.filled_triangle(x - 0.02 * size, y, x + 0.42 * size, y, x + 0.18 * size, y + 1.25 * size)
    dudraw.set_pen_color_rgb(196, 247, 255)
    dudraw.line(x + 0.18 * size, y + 0.28 * size, x + 0.18 * size, y + 0.93 * size)


def draw_polished_crystal(frame):
    dudraw.set_pen_color_rgb(39, 36, 68)
    dudraw.filled_rectangle(12, 8, 12, 8)
    dudraw.set_pen_color_rgb(61, 54, 95)
    dudraw.filled_ellipse(5.0, 14.7, 7.6, 2.4)
    dudraw.filled_ellipse(19.4, 1.2, 8.0, 2.2)
    dudraw.set_pen_color_rgb(36, 103, 129)
    dudraw.filled_ellipse(18.5, 12.9, 3.1, 1.3)
    dudraw.set_pen_color_rgb(61, 170, 184)
    dudraw.filled_ellipse(18.5, 12.96, 2.75, 1.12)
    # Stalactite ceiling and a falling mineral stream frame the cavern.
    dudraw.set_pen_color_rgb(27, 26, 52)
    dudraw.filled_rectangle(12, 15.65, 12, 0.35)
    for spike_x, length in ((1.3, 1.0), (3.2, 0.7), (5.6, 1.25), (9.0, 0.8), (12.6, 1.35), (16.2, 0.75), (18.9, 1.1), (22.4, 0.85)):
        dudraw.filled_triangle(spike_x - 0.32, 15.35, spike_x + 0.32, 15.35, spike_x, 15.35 - length)
        dudraw.set_pen_color_rgb(88, 161, 185)
        dudraw.line(spike_x, 15.22, spike_x, 15.35 - length * 0.48)
    flow = (frame * 0.02) % 0.4
    dudraw.set_pen_color_rgb(91, 203, 215)
    for stream in range(4):
        sx = 16.0 + stream * 0.13
        dudraw.line(sx, 15.0 - flow, sx, 13.38 - flow)
    dudraw.set_pen_color_rgb(169, 240, 244)
    dudraw.filled_circle(16.22, 13.26, 0.1 + 0.025 * math.sin(frame * 0.12))
    for cluster in ((2.0, 3.0, 1.1), (7.0, 7.0, 0.9), (20.8, 3.7, 1.2), (21.5, 14.0, 0.85), (11.2, 12.0, 0.72)):
        draw_crystal_cluster(*cluster, frame)
    # Abandoned mining relics and bioluminescent mushrooms ground the fantasy.
    dudraw.set_pen_color_rgb(77, 56, 39)
    dudraw.line(5.3, 2.2, 8.7, 2.2)
    dudraw.line(5.3, 2.46, 8.7, 2.46)
    for tie in range(7):
        tx = 5.45 + tie * 0.48
        dudraw.line(tx, 2.1, tx, 2.56)
    dudraw.set_pen_color_rgb(72, 68, 74)
    dudraw.filled_rectangle(7.1, 2.76, 0.46, 0.24)
    dudraw.set_pen_color_rgb(130, 126, 121)
    dudraw.circle(6.82, 2.46, 0.1)
    dudraw.circle(7.38, 2.46, 0.1)
    for mx, my, tint in ((2.8, 11.0, (121, 218, 230)), (3.35, 10.86, (196, 120, 225)), (22.0, 7.0, (126, 236, 206)), (10.0, 1.0, (205, 132, 234))):
        dudraw.set_pen_color_rgb(89, 108, 126)
        dudraw.filled_rectangle(mx, my, 0.03, 0.13)
        set_color(tint)
        dudraw.filled_ellipse(mx, my + 0.15, 0.16, 0.07)
        dudraw.circle(mx, my + 0.15, 0.23 + 0.02 * math.sin(frame * 0.1 + mx))
    for mote in range(25):
        x = (mote * 4.13 + math.sin(frame * 0.025 + mote) * 0.2) % 24
        y = (mote * 2.11 + frame * 0.012) % 16
        dudraw.set_pen_color_rgb(154, 237, 248)
        dudraw.filled_circle(x, y, 0.02 + mote % 3 * 0.01)


def draw_3d_environment(frame):
    style = CURRENT_MAP["three_d_style"]
    if style == "desert":
        draw_polished_desert(frame)
    elif style == "mountain":
        draw_polished_mountain(frame)
    elif style == "ocean":
        draw_polished_ocean(frame)
    elif style == "temple":
        draw_polished_temple(frame)
    elif style == "racetrack":
        draw_polished_racetrack(frame)
    elif style == "war":
        draw_polished_war(frame)
    elif style == "miami":
        draw_polished_miami(frame)
    elif style == "retro":
        draw_polished_retro(frame)
    elif style == "crystal":
        draw_polished_crystal(frame)
    else:
        draw_polished_meadow(frame)


def draw_3d_build_platforms():
    if CURRENT_MAP["place_rule"] != "islands":
        return
    theme = CURRENT_MAP["theme"]
    for grid_x, grid_y in BUILD_SQUARES:
        x = grid_x + 0.5
        y = grid_y + 0.5
        set_color(darken(theme["edge"], 28))
        dudraw.filled_ellipse(x + 0.1, y - 0.17, 0.48, 0.2)
        dudraw.set_pen_color_rgb(204, 181, 111)
        dudraw.filled_ellipse(x, y - 0.03, 0.45, 0.19)
        set_color(brighten(theme["grass_a"], 12))
        dudraw.filled_ellipse(x, y + 0.08, 0.37, 0.15)


def draw_3d_path(settings, frame):
    theme = CURRENT_MAP["theme"]
    side = darken(theme["edge"], 30)
    rim = brighten(theme["edge"], 5)
    surface = brighten(theme["path"], 10)
    for index, (x, y) in enumerate(PATH):
        set_color(side)
        dudraw.filled_circle(x + 0.13, y - 0.2, 0.64)
        if index + 1 < len(PATH):
            next_x, next_y = PATH[index + 1]
            dudraw.filled_rectangle(
                (x + next_x) / 2 + 0.13,
                (y + next_y) / 2 - 0.2,
                abs(next_x - x) / 2 + 0.64,
                abs(next_y - y) / 2 + 0.64,
            )
    for index, (x, y) in enumerate(PATH):
        set_color(rim)
        dudraw.filled_circle(x, y - 0.03, 0.62)
        set_color(surface)
        dudraw.filled_circle(x, y + 0.04, 0.5)
        if index + 1 < len(PATH):
            next_x, next_y = PATH[index + 1]
            set_color(rim)
            dudraw.filled_rectangle(
                (x + next_x) / 2,
                (y + next_y) / 2 - 0.03,
                abs(next_x - x) / 2 + 0.62,
                abs(next_y - y) / 2 + 0.62,
            )
            set_color(surface)
            dudraw.filled_rectangle(
                (x + next_x) / 2,
                (y + next_y) / 2 + 0.04,
                abs(next_x - x) / 2 + 0.5,
                abs(next_y - y) / 2 + 0.5,
            )
        if index % 3 == 0:
            set_color(brighten(theme["path"], 32))
            dudraw.filled_circle(x - 0.13, y + 0.16, 0.04)
    start_x, start_y = PATH[0]
    end_x, end_y = PATH[-1]
    dudraw.set_pen_color_rgb(76, 205, 119)
    dudraw.filled_circle(start_x, start_y + 0.08, 0.18)
    dudraw.set_pen_color_rgb(235, 84, 79)
    dudraw.filled_circle(end_x, end_y + 0.08, 0.18)


def draw_3d_map(settings, frame):
    draw_3d_environment(frame)
    theme = CURRENT_MAP["theme"]
    set_color(darken(theme["grass_b"], 40))
    dudraw.filled_rectangle(GRID_WIDTH / 2 + 0.08, 0.14, GRID_WIDTH / 2 - 0.08, 0.14)
    dudraw.filled_rectangle(GRID_WIDTH - 0.14, GRID_HEIGHT / 2 - 0.08, 0.14, GRID_HEIGHT / 2 - 0.08)
    set_color(brighten(theme["grass_a"], 18))
    dudraw.line(0.08, GRID_HEIGHT - 0.09, GRID_WIDTH - 0.18, GRID_HEIGHT - 0.09)
    draw_3d_build_platforms()
    draw_3d_path(settings, frame)
    set_color(darken(theme["edge"], 22))
    dudraw.rectangle(GRID_WIDTH / 2, GRID_HEIGHT / 2, GRID_WIDTH / 2 - 0.04, GRID_HEIGHT / 2 - 0.04)


def draw_grid(settings, frame):
    dudraw.clear(dudraw.BLACK)
    theme = CURRENT_MAP["theme"]

    if CURRENT_MAP.get("three_d", False):
        draw_3d_map(settings, frame)
        return

    if CURRENT_MAP.get("polished", False):
        style = CURRENT_MAP.get("polished_style")
        if style == "desert":
            draw_polished_desert(frame)
            draw_polished_desert_path(settings, frame)
            dudraw.set_pen_color_rgb(111, 76, 43)
        elif style == "mountain":
            draw_polished_mountain(frame)
            draw_polished_route(settings, (63, 71, 74), (148, 143, 133), (207, 211, 204), (76, 85, 84))
            dudraw.set_pen_color_rgb(49, 61, 61)
        elif style == "ocean":
            draw_polished_ocean(frame)
            draw_polished_route(settings, (31, 86, 111), (224, 204, 139), (251, 231, 162), (106, 86, 55))
            dudraw.set_pen_color_rgb(22, 78, 105)
        elif style == "temple":
            draw_polished_temple(frame)
            draw_polished_route(settings, (103, 69, 73), (187, 142, 126), (232, 192, 170), (116, 69, 70))
            dudraw.set_pen_color_rgb(87, 66, 67)
        elif style == "racetrack":
            draw_polished_racetrack(frame)
            draw_polished_route(settings, (221, 222, 217), (54, 57, 60), (232, 65, 62), (244, 238, 205))
            dudraw.set_pen_color_rgb(39, 48, 43)
        elif style == "war":
            draw_polished_war(frame)
            draw_polished_route(settings, (42, 46, 40), (91, 77, 61), (152, 134, 96), (43, 47, 42))
            dudraw.set_pen_color_rgb(34, 39, 34)
        elif style == "miami":
            draw_polished_miami(frame)
            draw_polished_route(settings, (224, 78, 139), (70, 202, 209), (173, 244, 232), (226, 67, 122))
            dudraw.set_pen_color_rgb(204, 76, 128)
        elif style == "retro":
            draw_polished_retro(frame)
            draw_polished_route(settings, (244, 64, 192), (35, 207, 199), (148, 250, 241), (254, 224, 85))
            dudraw.set_pen_color_rgb(227, 55, 178)
        elif style == "crystal":
            draw_polished_crystal(frame)
            draw_polished_route(settings, (67, 191, 208), (129, 105, 170), (195, 244, 255), (79, 203, 217))
            dudraw.set_pen_color_rgb(60, 164, 188)
        else:
            draw_polished_meadow(frame)
            draw_polished_path(settings, frame)
            dudraw.set_pen_color_rgb(50, 94, 62)
        dudraw.rectangle(GRID_WIDTH / 2, GRID_HEIGHT / 2, GRID_WIDTH / 2 - 0.04, GRID_HEIGHT / 2 - 0.04)
        return

    if is_amazing(settings):
        set_color(theme["edge"])
        dudraw.filled_rectangle(GRID_WIDTH / 2, GRID_HEIGHT / 2, GRID_WIDTH / 2, GRID_HEIGHT / 2)

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if is_ultra(settings):
                tile_type = "path" if (x, y) in PATH_SQUARES else "grass"
                draw_32_pixel_tile(x, y, tile_type)
                continue

            if (x, y) in PATH_SQUARES:
                set_color(theme["path"])
            elif (x + y) % 2 == 0:
                set_color(theme["grass_a"])
            else:
                set_color(theme["grass_b"])

            dudraw.filled_square(x + 0.5, y + 0.5, 0.5)

            if is_amazing(settings) and (x, y) not in PATH_SQUARES:
                set_color(theme["detail"])
                dudraw.square(x + 0.5, y + 0.5, 0.5)
                if CURRENT_MAP["place_rule"] != "islands" or (x, y) in BUILD_SQUARES:
                    draw_background_details(x, y)

            if CURRENT_MAP["place_rule"] == "islands" and (x, y) in BUILD_SQUARES:
                dudraw.set_pen_color_rgb(94, 172, 106)
                dudraw.filled_circle(x + 0.5, y + 0.5, 0.42)
                dudraw.set_pen_color_rgb(226, 214, 143)
                dudraw.circle(x + 0.5, y + 0.5, 0.43)

    draw_path(settings, frame)
    draw_ambient_effects(settings, frame)

    if is_amazing(settings):
        set_color(darken(theme["edge"], 24))
        dudraw.rectangle(GRID_WIDTH / 2, GRID_HEIGHT / 2, GRID_WIDTH / 2 - 0.04, GRID_HEIGHT / 2 - 0.04)


def draw_path(settings, frame):
    theme = CURRENT_MAP["theme"]

    if is_ultra(settings):
        set_color(theme["edge"])
        for i, (x, y) in enumerate(PATH):
            if i + 1 < len(PATH):
                next_x, next_y = PATH[i + 1]
                dudraw.line(x, y, next_x, next_y)

        glow_index = int(frame / 4) % len(PATH)
        for offset in range(0, len(PATH), 10):
            x, y = PATH[(glow_index + offset) % len(PATH)]
            dudraw.set_pen_color_rgb(255, 226, 132)
            dudraw.filled_square(x, y, 0.08)
            dudraw.set_pen_color_rgb(255, 249, 198)
            dudraw.filled_square(x, y, 0.035)

        return

    if is_amazing(settings):
        set_color(theme["edge"])
        for x, y in PATH:
            dudraw.filled_square(x, y, 0.5)

        set_color(theme["edge"])
        for i, (x, y) in enumerate(PATH):
            if i + 1 < len(PATH):
                next_x, next_y = PATH[i + 1]
                dudraw.line(x, y, next_x, next_y)

    set_color(theme["path"])
    for x, y in PATH:
        dudraw.filled_square(x, y, 0.5)

    if not is_amazing(settings):
        return

    set_color(brighten(theme["path"], 18))
    for i, (x, y) in enumerate(PATH[:-1]):
        next_x, next_y = PATH[i + 1]
        if i % 2 == 0:
            dudraw.line(x, y, next_x, next_y)

    set_color(theme["edge"])
    for i, (x, y) in enumerate(PATH):
        if i % 3 == 0:
            dudraw.filled_circle(x - 0.13, y + 0.08, 0.035)
        elif i % 3 == 1:
            dudraw.filled_circle(x + 0.16, y - 0.1, 0.03)

        if i % 5 == 0:
            set_color(theme["edge"])
            dudraw.filled_rectangle(x, y - 0.22, 0.03, 0.09)
            set_color(theme["detail"])
            dudraw.filled_circle(x, y - 0.1, 0.045)
            dudraw.set_pen_color_rgb(255, 235, 165)
            dudraw.filled_circle(x, y - 0.1, 0.02)

    glow_index = int(frame / 4) % len(PATH)
    for offset in range(0, len(PATH), 12):
        x, y = PATH[(glow_index + offset) % len(PATH)]
        dudraw.set_pen_color_rgb(255, 226, 132)
        dudraw.filled_circle(x, y, 0.09)
        dudraw.set_pen_color_rgb(255, 249, 198)
        dudraw.filled_circle(x, y, 0.04)

    if settings.get("show_path_arrows", True):
        dudraw.set_pen_color_rgb(122, 95, 62)
        for index in range(2, len(PATH) - 1, 7):
            x, y = PATH[index]
            next_x, next_y = PATH[index + 1]
            dx = next_x - x
            dy = next_y - y
            side_x = -dy
            side_y = dx
            dudraw.filled_triangle(
                x + dx * 0.18,
                y + dy * 0.18,
                x - dx * 0.12 + side_x * 0.12,
                y - dy * 0.12 + side_y * 0.12,
                x - dx * 0.12 - side_x * 0.12,
                y - dy * 0.12 - side_y * 0.12,
            )

        start_x, start_y = PATH[0]
        end_x, end_y = PATH[-1]
        dudraw.set_pen_color_rgb(77, 151, 92)
        dudraw.filled_circle(start_x, start_y, 0.2)
        dudraw.circle(start_x, start_y, 0.29)
        dudraw.set_pen_color_rgb(238, 247, 219)
        dudraw.filled_triangle(start_x + 0.1, start_y, start_x - 0.09, start_y + 0.1, start_x - 0.09, start_y - 0.1)
        dudraw.set_pen_color_rgb(193, 66, 66)
        dudraw.filled_circle(end_x, end_y, 0.2)
        dudraw.circle(end_x, end_y, 0.29)
        dudraw.set_pen_color_rgb(255, 225, 199)
        dudraw.filled_rectangle(end_x, end_y, 0.08, 0.08)


def draw_tower_character_details(x, y, tower_type, aim_x, aim_y, frame, scale=1.0):
    side_x = -aim_y
    side_y = aim_x

    if tower_type == "arrow":
        dudraw.set_pen_color_rgb(42, 92, 55)
        dudraw.filled_triangle(
            x - 0.25 * scale,
            y + 0.06 * scale,
            x,
            y + 0.48 * scale,
            x + 0.25 * scale,
            y + 0.06 * scale,
        )
        dudraw.set_pen_color_rgb(228, 214, 168)
        dudraw.filled_circle(x, y + 0.25 * scale, 0.11 * scale)
        dudraw.set_pen_color_rgb(96, 58, 32)
        dudraw.line(x + side_x * 0.26 * scale, y + 0.12 * scale + side_y * 0.26 * scale, x + aim_x * 0.58 * scale, y + 0.18 * scale + aim_y * 0.58 * scale)
        dudraw.line(x - side_x * 0.18 * scale, y + 0.2 * scale - side_y * 0.18 * scale, x + side_x * 0.18 * scale, y + 0.2 * scale + side_y * 0.18 * scale)
        dudraw.set_pen_color_rgb(245, 234, 178)
        dudraw.filled_triangle(x + aim_x * 0.64 * scale, y + 0.18 * scale + aim_y * 0.64 * scale, x + aim_x * 0.49 * scale + side_x * 0.06 * scale, y + 0.18 * scale + aim_y * 0.49 * scale + side_y * 0.06 * scale, x + aim_x * 0.49 * scale - side_x * 0.06 * scale, y + 0.18 * scale + aim_y * 0.49 * scale - side_y * 0.06 * scale)
    elif tower_type == "cannon":
        dudraw.set_pen_color_rgb(59, 50, 42)
        dudraw.filled_rectangle(x, y - 0.1 * scale, 0.34 * scale, 0.18 * scale)
        dudraw.filled_circle(x - 0.28 * scale, y - 0.28 * scale, 0.12 * scale)
        dudraw.filled_circle(x + 0.28 * scale, y - 0.28 * scale, 0.12 * scale)
        dudraw.set_pen_color_rgb(37, 42, 48)
        dudraw.filled_circle(x, y + 0.05 * scale, 0.22 * scale)
        dudraw.filled_rectangle(x + aim_x * 0.28 * scale, y + 0.08 * scale + aim_y * 0.28 * scale, 0.18 * scale, 0.1 * scale)
        dudraw.set_pen_color_rgb(238, 123, 58)
        dudraw.filled_circle(x + aim_x * 0.6 * scale, y + 0.08 * scale + aim_y * 0.6 * scale, 0.07 * scale)
    elif tower_type == "frost":
        dudraw.set_pen_color_rgb(219, 250, 255)
        dudraw.filled_triangle(x - 0.22 * scale, y - 0.02 * scale, x, y + 0.52 * scale, x + 0.22 * scale, y - 0.02 * scale)
        dudraw.set_pen_color_rgb(114, 211, 232)
        dudraw.filled_triangle(x - 0.1 * scale, y + 0.02 * scale, x, y + 0.37 * scale, x + 0.1 * scale, y + 0.02 * scale)
        for i in range(4):
            angle = frame * 0.04 + i * math.pi / 2
            dudraw.set_pen_color_rgb(196, 242, 255)
            dudraw.filled_circle(x + math.cos(angle) * 0.38 * scale, y + 0.12 * scale + math.sin(angle) * 0.25 * scale, 0.045 * scale)
    elif tower_type == "sniper":
        dudraw.set_pen_color_rgb(64, 55, 85)
        dudraw.filled_rectangle(x, y + 0.05 * scale, 0.22 * scale, 0.46 * scale)
        dudraw.set_pen_color_rgb(222, 214, 236)
        dudraw.filled_circle(x - 0.05 * scale, y + 0.32 * scale, 0.13 * scale)
        dudraw.set_pen_color_rgb(31, 35, 42)
        dudraw.line(x, y + 0.32 * scale, x + aim_x * 0.8 * scale, y + 0.32 * scale + aim_y * 0.8 * scale)
        dudraw.filled_circle(x + aim_x * 0.86 * scale, y + 0.32 * scale + aim_y * 0.86 * scale, 0.06 * scale)
    elif tower_type == "laser":
        dudraw.set_pen_color_rgb(62, 22, 34)
        dudraw.filled_rectangle(x, y + 0.08 * scale, 0.24 * scale, 0.38 * scale)
        dudraw.set_pen_color_rgb(255, 120, 142)
        dudraw.filled_circle(x, y + 0.32 * scale, 0.14 * scale + 0.02 * math.sin(frame * 0.12))
        dudraw.set_pen_color_rgb(255, 190, 200)
        dudraw.line(x, y + 0.32 * scale, x + aim_x * 0.72 * scale, y + 0.32 * scale + aim_y * 0.72 * scale)
    elif tower_type == "mortar":
        dudraw.set_pen_color_rgb(50, 61, 55)
        dudraw.filled_rectangle(x, y - 0.05 * scale, 0.38 * scale, 0.22 * scale)
        dudraw.set_pen_color_rgb(28, 32, 32)
        dudraw.filled_rectangle(x + aim_x * 0.18 * scale, y + 0.22 * scale + aim_y * 0.18 * scale, 0.16 * scale, 0.38 * scale)
        dudraw.set_pen_color_rgb(255, 162, 66)
        dudraw.filled_circle(x + aim_x * 0.34 * scale, y + 0.48 * scale + aim_y * 0.34 * scale, 0.08 * scale)
    elif tower_type == "venom":
        dudraw.set_pen_color_rgb(44, 96, 53)
        dudraw.filled_triangle(x - 0.25 * scale, y - 0.16 * scale, x, y + 0.38 * scale, x + 0.25 * scale, y - 0.16 * scale)
        dudraw.set_pen_color_rgb(163, 247, 105)
        dudraw.filled_circle(x, y + 0.1 * scale, 0.15 * scale)
        dudraw.set_pen_color_rgb(212, 255, 153)
        dudraw.filled_circle(x + 0.05 * scale, y + 0.17 * scale, 0.045 * scale)
        dudraw.set_pen_color_rgb(94, 205, 72)
        dudraw.filled_circle(x + math.sin(frame * 0.08) * 0.2 * scale, y + 0.42 * scale, 0.04 * scale)
    elif tower_type == "storm":
        dudraw.set_pen_color_rgb(38, 68, 126)
        dudraw.filled_rectangle(x, y + 0.04 * scale, 0.26 * scale, 0.42 * scale)
        dudraw.set_pen_color_rgb(214, 233, 255)
        dudraw.filled_triangle(x - 0.14 * scale, y + 0.43 * scale, x + 0.02 * scale, y + 0.16 * scale, x + 0.16 * scale, y + 0.43 * scale)
        dudraw.set_pen_color_rgb(255, 241, 138)
        dudraw.line(x - 0.22 * scale, y + 0.25 * scale, x + 0.02 * scale, y + 0.45 * scale)
        dudraw.line(x + 0.02 * scale, y + 0.45 * scale, x - 0.04 * scale, y + 0.18 * scale)


def draw_towers(towers, settings, frame):
    for tower in towers:
        if is_ultra(settings):
            draw_pixel_tower(tower, frame)
            continue

        if is_amazing(settings):
            pulse = 0.05 * math.sin(frame * 0.08 + tower.x)
            aura_size = tower.range if tower.is_special else 0.62

            if tower.is_special:
                set_color(brighten(tower.color, 35))
                dudraw.circle(tower.x, tower.y, aura_size)
                dudraw.circle(tower.x, tower.y, aura_size - 0.18)

            set_color((42, 51, 52))
            shadow_size = 0.52 if tower.is_special else 0.42
            dudraw.filled_circle(tower.x + 0.08, tower.y - 0.08, shadow_size)

            set_color((218, 211, 190))
            base_size = 0.56 if tower.is_special else 0.46
            dudraw.filled_circle(tower.x, tower.y, base_size)

            set_color(brighten(tower.color, 45))
            dudraw.circle(tower.x, tower.y + 0.04, (0.52 if tower.is_special else 0.41) + pulse)

        set_color(tower.color)
        tower_size = 0.43 if tower.is_special else 0.34
        dudraw.filled_circle(tower.x, tower.y + 0.04, tower_size)

        if is_amazing(settings) and tower.level > 1:
            dudraw.set_pen_color_rgb(255, 241, 151)
            for i in range(tower.level):
                angle = frame * 0.045 + i * 2 * math.pi / tower.level
                dudraw.filled_circle(tower.x + math.cos(angle) * 0.46, tower.y + math.sin(angle) * 0.46, 0.045)

        if is_amazing(settings):
            dudraw.set_pen_color_rgb(236, 238, 224)
            dudraw.circle(tower.x, tower.y + 0.04, tower_size * 0.7)
            dudraw.set_pen_color_rgb(38, 44, 47)
            for i in range(4):
                angle = i * math.pi / 2 + 0.2
                dudraw.filled_circle(tower.x + math.cos(angle) * tower_size * 0.82, tower.y + 0.04 + math.sin(angle) * tower_size * 0.82, 0.025)

        barrel_length = 0.52 if not tower.is_special else 0.72
        barrel_width = 0.08 if not tower.is_special else 0.11
        barrel_x = tower.x + tower.aim_x * barrel_length / 2
        barrel_y = tower.y + 0.08 + tower.aim_y * barrel_length / 2
        muzzle_x = tower.x + tower.aim_x * barrel_length
        muzzle_y = tower.y + 0.08 + tower.aim_y * barrel_length

        dudraw.set_pen_color_rgb(23, 27, 32)
        dudraw.line(tower.x, tower.y + 0.08, muzzle_x, muzzle_y)
        dudraw.filled_circle(muzzle_x, muzzle_y, barrel_width)

        dudraw.set_pen_color_rgb(25, 31, 39)
        if not tower.is_special:
            draw_tower_character_details(tower.x, tower.y + 0.04, tower.tower_type, tower.aim_x, tower.aim_y, frame)
        elif tower.is_special:
            dudraw.filled_circle(tower.x, tower.y + 0.05, 0.22)
            dudraw.set_pen_color_rgb(255, 245, 190)
            dudraw.filled_circle(tower.x, tower.y + 0.08, 0.09)
            dudraw.set_pen_color_rgb(255, 255, 220)
            dudraw.filled_circle(tower.x, tower.y + 0.42, 0.08)
            if is_amazing(settings):
                for i in range(5):
                    angle = frame * 0.03 + i * 2 * math.pi / 5
                    set_color(brighten(tower.color, 70))
                    dudraw.filled_circle(tower.x + math.cos(angle) * 0.62, tower.y + math.sin(angle) * 0.62, 0.055)

        if tower.damage > 0 and tower.tower_type != "arrow":
            barrel_length = 0.58 if not tower.is_special else 0.78
            muzzle_x = tower.x + tower.aim_x * barrel_length
            muzzle_y = tower.y + 0.08 + tower.aim_y * barrel_length
            side_x = -tower.aim_y * 0.08
            side_y = tower.aim_x * 0.08

            dudraw.set_pen_color_rgb(12, 16, 20)
            dudraw.filled_triangle(
                tower.x + side_x,
                tower.y + 0.08 + side_y,
                tower.x - side_x,
                tower.y + 0.08 - side_y,
                muzzle_x,
                muzzle_y,
            )

            set_color(brighten(tower.color, 70))
            dudraw.filled_circle(muzzle_x, muzzle_y, 0.07 if not tower.is_special else 0.1)


def draw_pixel_block(cx, cy, px, py, w, h, color):
    pixel = 1 / 32
    x = cx - 0.5 + (px + w / 2) * pixel
    y = cy - 0.5 + (py + h / 2) * pixel
    set_color(color)
    dudraw.filled_rectangle(x, y, w * pixel / 2, h * pixel / 2)


def draw_pixel_tower(tower, frame):
    base = tower.color
    light = brighten(base, 65)
    dark = (
        max(0, base[0] - 60),
        max(0, base[1] - 60),
        max(0, base[2] - 60),
    )
    cx = int(tower.x) + 0.5
    cy = int(tower.y) + 0.5

    if tower.is_special:
        set_color(brighten(base, 75))
        dudraw.circle(cx, cy, tower.range)
        for i in range(8):
            angle = frame * 0.05 + i * math.pi / 4
            dudraw.filled_square(cx + math.cos(angle) * 0.46, cy + math.sin(angle) * 0.46, 0.04)

    draw_pixel_block(cx, cy, 7, 5, 18, 4, (57, 50, 45))
    draw_pixel_block(cx, cy, 8, 8, 16, 4, (218, 207, 177))
    draw_pixel_block(cx, cy, 9, 12, 14, 12, base)
    draw_pixel_block(cx, cy, 11, 23, 10, 3, light)
    draw_pixel_block(cx, cy, 9, 12, 3, 12, dark)
    draw_pixel_block(cx, cy, 20, 12, 3, 12, dark)

    if tower.level > 1:
        for i in range(tower.level):
            draw_pixel_block(cx, cy, 6 + i * 5, 27, 2, 2, (255, 237, 119))

    muzzle_x = tower.x + tower.aim_x * 0.58
    muzzle_y = tower.y + 0.08 + tower.aim_y * 0.58
    dudraw.set_pen_color_rgb(16, 18, 23)
    dudraw.line(tower.x, tower.y + 0.08, muzzle_x, muzzle_y)
    set_color(light)
    dudraw.filled_square(muzzle_x, muzzle_y, 0.07)

    if tower.tower_type == "frost":
        draw_pixel_block(cx, cy, 13, 15, 6, 6, (218, 250, 255))
    elif tower.tower_type == "venom":
        draw_pixel_block(cx, cy, 13, 15, 6, 6, (170, 255, 102))
    elif tower.tower_type == "storm":
        draw_pixel_block(cx, cy, 15, 13, 3, 10, (211, 230, 255))
    elif tower.tower_type == "mortar":
        draw_pixel_block(cx, cy, 12, 17, 8, 6, (31, 35, 37))
    elif tower.is_special:
        draw_pixel_block(cx, cy, 12, 14, 8, 8, (255, 246, 190))


def enemy_facing(enemy):
    if enemy.path_index >= len(PATH) - 1:
        return 1, 0

    target_x, target_y = PATH[enemy.path_index + 1]
    dx = target_x - enemy.x
    dy = target_y - enemy.y
    distance = math.sqrt(dx * dx + dy * dy)

    if distance == 0:
        return 1, 0

    return dx / distance, dy / distance


def draw_enemy_character(x, y, enemy_type, color, radius, frame, scale=1.0, facing_x=1, facing_y=0, poisoned=False, slowed=False):
    bob = math.sin(frame * 0.12 + x * 1.7) * 0.045 * scale
    stride = math.sin(frame * 0.24 + x) * 0.1 * scale
    side_x = -facing_y
    side_y = facing_x
    body = color

    if poisoned:
        body = (88, 156, 74)
    elif slowed:
        body = (97, 139, 196)

    dudraw.set_pen_color_rgb(35, 31, 29)
    dudraw.filled_ellipse(x + 0.1 * scale, y - 0.28 * scale, radius * 1.35 * scale, radius * 0.35 * scale)

    if poisoned:
        dudraw.set_pen_color_rgb(178, 242, 104)
        for i in range(2):
            bubble_x = x - 0.16 * scale + i * 0.24 * scale
            bubble_y = y + 0.42 * scale + 0.05 * math.sin(frame * 0.18 + i)
            dudraw.circle(bubble_x, bubble_y, (0.045 + i * 0.015) * scale)
    if slowed:
        dudraw.set_pen_color_rgb(204, 244, 255)
        dudraw.line(x - 0.22 * scale, y - 0.37 * scale, x - 0.08 * scale, y - 0.28 * scale)
        dudraw.line(x + 0.06 * scale, y - 0.37 * scale, x + 0.2 * scale, y - 0.28 * scale)

    if enemy_type == "swarm":
        for i in range(3):
            ox = (i - 1) * 0.13 * scale
            oy = math.sin(frame * 0.22 + i) * 0.05 * scale
            draw_small_enemy(x + ox, y + oy, body, radius * 0.78, scale)
        return

    if enemy_type == "wraith":
        set_color(brighten(body, 45))
        dudraw.circle(x, y + bob, radius * 1.65 * scale + 0.04 * math.sin(frame * 0.1))
        set_color(body)
        dudraw.filled_triangle(
            x - radius * 0.95 * scale,
            y + bob + radius * 0.55 * scale,
            x,
            y + bob - radius * 1.2 * scale,
            x + radius * 0.95 * scale,
            y + bob + radius * 0.55 * scale,
        )
        draw_enemy_face(x, y + bob + radius * 0.35 * scale, scale, facing_x, facing_y)
        return

    width = radius * (1.0 if enemy_type in ("runner", "charger") else 1.18) * scale
    height = radius * (1.65 if enemy_type in ("brute", "boss", "armored") else 1.35) * scale
    head_size = radius * (0.52 if enemy_type != "boss" else 0.62) * scale

    set_color(darken(body, 40))
    dudraw.line(x - side_x * width * 0.45, y + bob - height * 0.38, x - side_x * width * 0.45 + stride, y + bob - height * 0.85)
    dudraw.line(x + side_x * width * 0.45, y + bob - height * 0.38, x + side_x * width * 0.45 - stride, y + bob - height * 0.85)

    set_color(body)
    dudraw.filled_ellipse(x, y + bob - height * 0.08, width, height * 0.55)
    head_x = x + facing_x * width * 0.25
    head_y = y + bob + height * 0.42 + facing_y * height * 0.12

    set_color(brighten(body, 35))
    dudraw.filled_circle(head_x, head_y, head_size)

    set_color(darken(body, 55))
    dudraw.line(x - side_x * width * 0.7, y + bob + height * 0.08, x - side_x * width * 0.95 - stride * 0.45, y + bob - height * 0.22)
    dudraw.line(x + side_x * width * 0.7, y + bob + height * 0.08, x + side_x * width * 0.95 + stride * 0.45, y + bob - height * 0.22)

    draw_enemy_face(head_x + facing_x * width * 0.05, head_y + height * 0.03, scale, facing_x, facing_y)

    if enemy_type == "scout":
        dudraw.set_pen_color_rgb(245, 205, 96)
        nose_x = head_x + facing_x * width * 0.85
        nose_y = head_y + facing_y * height * 0.35
        dudraw.filled_triangle(nose_x, nose_y, head_x - side_x * width * 0.25, head_y - side_y * height * 0.22, head_x + side_x * width * 0.25, head_y + side_y * height * 0.22)
    elif enemy_type == "runner":
        dudraw.set_pen_color_rgb(255, 211, 96)
        dudraw.filled_circle(x - facing_x * width * 1.0, y + bob - height * 0.48, 0.08 * scale)
        dudraw.set_pen_color_rgb(255, 146, 73)
        dudraw.filled_triangle(x - facing_x * width * 1.35, y + bob - height * 0.48, x - facing_x * width * 0.9, y + bob - height * 0.3, x - facing_x * width * 0.9, y + bob - height * 0.66)
    elif enemy_type == "brute":
        dudraw.set_pen_color_rgb(72, 42, 36)
        dudraw.filled_rectangle(x, y + bob - height * 0.08, width * 0.28, height * 0.5)
        dudraw.filled_circle(x - side_x * width * 1.05, y + bob - height * 0.06, 0.12 * scale)
        dudraw.filled_circle(x + side_x * width * 1.05, y + bob - height * 0.06, 0.12 * scale)
    elif enemy_type == "shield":
        dudraw.set_pen_color_rgb(185, 200, 221)
        shield_x = x + facing_x * width * 0.95
        shield_y = y + bob - height * 0.02 + facing_y * height * 0.35
        dudraw.filled_rectangle(shield_x, shield_y, width * 0.62, height * 0.58)
        dudraw.set_pen_color_rgb(91, 108, 133)
        dudraw.rectangle(shield_x, shield_y, width * 0.62, height * 0.58)
        dudraw.line(shield_x, shield_y - height * 0.48, shield_x, shield_y + height * 0.48)
    elif enemy_type == "armored":
        dudraw.set_pen_color_rgb(166, 179, 184)
        dudraw.rectangle(x, y + bob - height * 0.08, width * 0.85, height * 0.55)
        dudraw.circle(head_x, head_y, head_size * 0.75)
        dudraw.set_pen_color_rgb(83, 92, 98)
        dudraw.filled_rectangle(x, y + bob + height * 0.12, width * 0.45, 0.045 * scale)
    elif enemy_type == "splitter":
        dudraw.set_pen_color_rgb(236, 165, 211)
        dudraw.filled_circle(x - side_x * width * 0.75, y + bob - height * 0.52, 0.07 * scale)
        dudraw.filled_circle(x + side_x * width * 0.75, y + bob - height * 0.52, 0.07 * scale)
        dudraw.line(x - side_x * width * 0.55, y + bob - height * 0.46, x + side_x * width * 0.55, y + bob - height * 0.46)
    elif enemy_type == "charger":
        dudraw.set_pen_color_rgb(255, 211, 126)
        horn_x = head_x + facing_x * width * 0.82
        horn_y = head_y + facing_y * height * 0.35
        dudraw.filled_triangle(horn_x, horn_y, head_x - side_x * width * 0.22, head_y - side_y * height * 0.2, head_x + side_x * width * 0.22, head_y + side_y * height * 0.2)
        dudraw.filled_triangle(horn_x + facing_x * width * 0.1, horn_y - height * 0.28, head_x - side_x * width * 0.18, head_y - height * 0.28 - side_y * height * 0.18, head_x + side_x * width * 0.18, head_y - height * 0.28 + side_y * height * 0.18)
    elif enemy_type == "boss":
        dudraw.set_pen_color_rgb(255, 218, 92)
        dudraw.filled_triangle(x - side_x * width * 0.78, y + bob + height * 0.9, x, y + bob + height * 1.18, x + side_x * width * 0.78, y + bob + height * 0.9)
        set_color(brighten(body, 45))
        dudraw.circle(x, y + bob - height * 0.08, width * 1.1 + 0.05 * math.sin(frame * 0.08))


def draw_small_enemy(x, y, color, radius, scale):
    set_color(color)
    dudraw.filled_circle(x, y, radius * scale)
    set_color(brighten(color, 45))
    dudraw.filled_circle(x - radius * 0.32 * scale, y + radius * 0.28 * scale, radius * 0.38 * scale)
    draw_enemy_face(x, y + radius * 0.12 * scale, scale * 0.7, 1, 0)


def enemy_offset(x, y, facing_x, facing_y, forward, side):
    return x + facing_x * forward - facing_y * side, y + facing_y * forward + facing_x * side


def draw_scout_enemy(x, y, body, radius, scale, facing_x, facing_y, frame):
    r = radius * scale
    stride = math.sin(frame * 0.25 + x) * r * 0.34
    cloak_sway = math.sin(frame * 0.16 + x) * r * 0.08
    lantern_sway = math.sin(frame * 0.21 + x) * r * 0.12
    side_x = -facing_y
    side_y = facing_x

    # Crisp boots and legs give the small silhouette a readable walking rhythm.
    for side, step in ((-1, stride), (1, -stride)):
        hip_x = x + side_x * side * r * 0.24
        hip_y = y - r * 0.52 + side_y * side * r * 0.1
        dudraw.set_pen_color_rgb(43, 32, 31)
        dudraw.line(hip_x, hip_y, hip_x + facing_x * step, hip_y - r * 0.43 + facing_y * step)
        boot_x = hip_x + facing_x * (step + r * 0.14)
        boot_y = hip_y - r * 0.45 + facing_y * step
        dudraw.set_pen_color_rgb(77, 49, 35)
        dudraw.filled_ellipse(boot_x, boot_y, r * 0.23, r * 0.1)
        dudraw.set_pen_color_rgb(166, 103, 42)
        dudraw.line(boot_x - r * 0.15, boot_y - r * 0.04, boot_x + r * 0.17, boot_y - r * 0.04)

    # Broad cloak, shoulder cape, seams, and belt create a clean rogue shape.
    dudraw.set_pen_color_rgb(45, 28, 36)
    dudraw.filled_triangle(x - r * 0.9, y - r * 0.62, x + r * 0.9, y - r * 0.62, x, y + r * 0.88)
    set_color(body)
    dudraw.filled_triangle(x - r * 0.72, y - r * 0.54, x + r * 0.72, y - r * 0.54, x + cloak_sway, y + r * 0.68)
    set_color(brighten(body, 28))
    dudraw.filled_triangle(x - r * 0.7, y + r * 0.16, x + r * 0.68, y + r * 0.16, x, y + r * 0.68)
    dudraw.set_pen_color_rgb(115, 41, 43)
    dudraw.line(x - r * 0.43, y - r * 0.43, x - r * 0.11 + cloak_sway, y + r * 0.42)
    dudraw.line(x + r * 0.43, y - r * 0.43, x + r * 0.11 + cloak_sway, y + r * 0.42)
    dudraw.set_pen_color_rgb(190, 130, 53)
    dudraw.line(x - r * 0.58, y - r * 0.02, x + r * 0.58, y - r * 0.02)
    dudraw.filled_circle(x, y + r * 0.2, r * 0.075)
    dudraw.set_pen_color_rgb(106, 61, 35)
    dudraw.filled_rectangle(x + side_x * r * 0.54, y + side_y * r * 0.54 - r * 0.08, r * 0.2, r * 0.22)
    dudraw.set_pen_color_rgb(216, 153, 60)
    dudraw.rectangle(x + side_x * r * 0.54, y + side_y * r * 0.54 - r * 0.08, r * 0.2, r * 0.22)

    # An oversized hood and half-mask read clearly from play distance.
    dudraw.set_pen_color_rgb(48, 29, 37)
    dudraw.filled_circle(x, y + r * 0.55, r * 0.6)
    set_color(body)
    dudraw.filled_triangle(x - r * 0.6, y + r * 0.42, x + r * 0.6, y + r * 0.42, x, y + r * 1.25)
    face_x, face_y = enemy_offset(x, y + r * 0.54, facing_x, facing_y, r * 0.05, 0)
    dudraw.set_pen_color_rgb(27, 24, 29)
    dudraw.filled_ellipse(face_x, face_y, r * 0.27, r * 0.24)
    dudraw.set_pen_color_rgb(195, 187, 170)
    dudraw.filled_rectangle(face_x, face_y - r * 0.12, r * 0.21, r * 0.07)
    dudraw.set_pen_color_rgb(255, 208, 82)
    for side in (-1, 1):
        eye_x, eye_y = enemy_offset(face_x, face_y, facing_x, facing_y, r * 0.08, side * r * 0.1)
        dudraw.filled_circle(eye_x, eye_y, r * 0.052)

    # A large caged lantern is his visual anchor, carried on an extended arm.
    wrist_x, wrist_y = enemy_offset(x, y, facing_x, facing_y, r * 0.05, -r * 0.63)
    lamp_x, lamp_y = enemy_offset(x, y, facing_x, facing_y, -r * 0.04, -r * 1.02)
    lamp_x += side_x * lantern_sway
    lamp_y += side_y * lantern_sway
    dudraw.set_pen_color_rgb(81, 45, 34)
    dudraw.line(x - side_x * r * 0.35, y - side_y * r * 0.35 + r * 0.12, wrist_x, wrist_y)
    dudraw.line(wrist_x, wrist_y, lamp_x, lamp_y + r * 0.36)
    dudraw.set_pen_color_rgb(255, 190, 58)
    dudraw.circle(lamp_x, lamp_y, r * (0.4 + 0.04 * math.sin(frame * 0.2)))
    dudraw.set_pen_color_rgb(92, 63, 39)
    dudraw.filled_rectangle(lamp_x, lamp_y, r * 0.24, r * 0.29)
    dudraw.set_pen_color_rgb(235, 167, 48)
    dudraw.rectangle(lamp_x, lamp_y, r * 0.24, r * 0.29)
    dudraw.line(lamp_x - r * 0.16, lamp_y, lamp_x + r * 0.16, lamp_y)
    dudraw.line(lamp_x, lamp_y - r * 0.23, lamp_x, lamp_y + r * 0.23)
    dudraw.set_pen_color_rgb(255, 229, 110)
    dudraw.filled_circle(lamp_x, lamp_y, r * 0.12)

    # The forward hand exposes a curved silver dagger.
    hand_x, hand_y = enemy_offset(x, y, facing_x, facing_y, r * 0.18, r * 0.52)
    tip_x, tip_y = enemy_offset(hand_x, hand_y, facing_x, facing_y, r * 0.58, 0)
    dudraw.set_pen_color_rgb(104, 61, 35)
    dudraw.line(hand_x - side_x * r * 0.16, hand_y - side_y * r * 0.16, hand_x + side_x * r * 0.16, hand_y + side_y * r * 0.16)
    dudraw.set_pen_color_rgb(219, 231, 233)
    dudraw.filled_triangle(tip_x, tip_y, hand_x - side_x * r * 0.12, hand_y - side_y * r * 0.12, hand_x + side_x * r * 0.06, hand_y + side_y * r * 0.06)
    dudraw.set_pen_color_rgb(251, 252, 247)
    dudraw.line(hand_x + facing_x * r * 0.12, hand_y + facing_y * r * 0.12, tip_x - facing_x * r * 0.09, tip_y - facing_y * r * 0.09)


def draw_hound_enemy(x, y, body, radius, scale, facing_x, facing_y, frame):
    r = radius * scale
    step = math.sin(frame * 0.32 + x) * r * 0.4
    set_color(darken(body, 35))
    for side in (-0.65, 0.65):
        leg_x = x - facing_y * side * r
        dudraw.line(leg_x, y - r * 0.2, leg_x + step * side, y - r * 0.72)
    set_color(body)
    dudraw.filled_ellipse(x, y, r * 1.2, r * 0.54)
    head_x, head_y = enemy_offset(x, y, facing_x, facing_y, r * 1.03, r * 0.18)
    dudraw.filled_triangle(head_x + facing_x * r * 0.45, head_y, head_x - facing_x * r * 0.3 - facing_y * r * 0.44, head_y - facing_y * r * 0.44, head_x - facing_x * r * 0.3 + facing_y * r * 0.44, head_y + facing_y * r * 0.44)
    dudraw.set_pen_color_rgb(230, 206, 124)
    eye_x, eye_y = enemy_offset(head_x, head_y, facing_x, facing_y, r * 0.04, -r * 0.13)
    dudraw.filled_circle(eye_x, eye_y, r * 0.09)
    tail_x, tail_y = enemy_offset(x, y, facing_x, facing_y, -r * 1.1, 0)
    dudraw.set_pen_color_rgb(101, 66, 54)
    dudraw.line(tail_x, tail_y, tail_x - facing_x * r * 0.45, tail_y + r * 0.42)


def draw_executioner_enemy(x, y, body, radius, scale, facing_x, facing_y, frame):
    r = radius * scale
    set_color(body)
    dudraw.filled_rectangle(x, y - r * 0.1, r * 0.9, r * 0.78)
    dudraw.set_pen_color_rgb(37, 31, 34)
    dudraw.filled_triangle(x - r * 0.62, y + r * 0.5, x + r * 0.62, y + r * 0.5, x, y + r * 1.34)
    dudraw.set_pen_color_rgb(217, 191, 153)
    dudraw.line(x - r * 0.23, y + r * 0.74, x + r * 0.23, y + r * 0.74)
    axe_x, axe_y = enemy_offset(x, y, facing_x, facing_y, r * 0.2, r * 1.05)
    dudraw.set_pen_color_rgb(83, 55, 38)
    dudraw.line(axe_x, axe_y - r, axe_x, axe_y + r * 0.9)
    dudraw.set_pen_color_rgb(160, 166, 168)
    dudraw.filled_triangle(axe_x, axe_y + r * 0.55, axe_x + r * 0.62, axe_y + r * 0.88, axe_x + r * 0.56, axe_y + r * 0.36)


def draw_shield_knight_enemy(x, y, body, radius, scale, facing_x, facing_y, frame):
    r = radius * scale
    set_color(body)
    dudraw.filled_rectangle(x, y - r * 0.1, r * 0.54, r * 0.65)
    dudraw.set_pen_color_rgb(162, 172, 187)
    dudraw.filled_circle(x, y + r * 0.7, r * 0.46)
    dudraw.set_pen_color_rgb(46, 54, 70)
    dudraw.line(x - r * 0.38, y + r * 0.68, x + r * 0.38, y + r * 0.68)
    shield_x, shield_y = enemy_offset(x, y, facing_x, facing_y, r * 0.55, 0)
    dudraw.set_pen_color_rgb(65, 76, 98)
    dudraw.filled_rectangle(shield_x, shield_y, r * 0.62, r * 0.86)
    dudraw.set_pen_color_rgb(191, 201, 216)
    dudraw.rectangle(shield_x, shield_y, r * 0.62, r * 0.86)
    dudraw.line(shield_x - r * 0.5, shield_y, shield_x + r * 0.5, shield_y)
    dudraw.line(shield_x, shield_y - r * 0.7, shield_x, shield_y + r * 0.7)


def draw_bat_swarm_enemy(x, y, body, radius, scale, frame):
    r = radius * scale
    flap = 0.25 + 0.25 * abs(math.sin(frame * 0.35))
    for index, (offset_x, offset_y) in enumerate(((-0.65, 0.15), (0.05, 0.58), (0.64, -0.1))):
        bx = x + offset_x * r
        by = y + offset_y * r + math.sin(frame * 0.2 + index) * r * 0.12
        set_color(body if index != 1 else brighten(body, 20))
        dudraw.filled_circle(bx, by, r * 0.19)
        dudraw.filled_triangle(bx - r * 0.16, by, bx - r * (0.58 + flap), by + r * flap, bx - r * 0.45, by - r * 0.16)
        dudraw.filled_triangle(bx + r * 0.16, by, bx + r * (0.58 + flap), by + r * flap, bx + r * 0.45, by - r * 0.16)
        dudraw.set_pen_color_rgb(244, 204, 101)
        dudraw.filled_circle(bx - r * 0.07, by + r * 0.04, r * 0.035)
        dudraw.filled_circle(bx + r * 0.07, by + r * 0.04, r * 0.035)


def draw_wraith_enemy(x, y, body, radius, scale, frame):
    r = radius * scale
    glow = r * (1.72 + 0.08 * math.sin(frame * 0.1))
    set_color(brighten(body, 52))
    dudraw.circle(x, y + r * 0.12, glow)
    set_color(body)
    dudraw.filled_circle(x, y + r * 0.48, r * 0.62)
    dudraw.filled_triangle(x - r * 0.64, y + r * 0.42, x + r * 0.64, y + r * 0.42, x + r * 0.24, y - r * 1.0)
    dudraw.set_pen_color_rgb(219, 225, 255)
    dudraw.filled_circle(x - r * 0.2, y + r * 0.52, r * 0.09)
    dudraw.filled_circle(x + r * 0.2, y + r * 0.52, r * 0.09)
    dudraw.set_pen_color_rgb(58, 43, 82)
    dudraw.line(x - r * 0.18, y - r * 0.5, x - r * 0.4, y - r * 0.78)
    dudraw.line(x + r * 0.12, y - r * 0.5, x + r * 0.34, y - r * 0.85)


def draw_golem_enemy(x, y, body, radius, scale, frame):
    r = radius * scale
    set_color(darken(body, 35))
    dudraw.filled_rectangle(x - r * 0.72, y - r * 0.06, r * 0.28, r * 0.62)
    dudraw.filled_rectangle(x + r * 0.72, y - r * 0.06, r * 0.28, r * 0.62)
    set_color(body)
    dudraw.filled_rectangle(x, y, r * 0.82, r * 0.75)
    dudraw.filled_rectangle(x, y + r * 0.8, r * 0.54, r * 0.36)
    dudraw.set_pen_color_rgb(166, 181, 187)
    dudraw.rectangle(x, y, r * 0.82, r * 0.75)
    dudraw.rectangle(x, y + r * 0.8, r * 0.54, r * 0.36)
    dudraw.set_pen_color_rgb(69, 188, 205)
    dudraw.filled_circle(x, y + r * 0.05, r * (0.14 + 0.025 * math.sin(frame * 0.16)))
    dudraw.set_pen_color_rgb(37, 46, 50)
    dudraw.line(x - r * 0.7, y - r * 0.72, x - r * 0.7, y - r * 1.05)
    dudraw.line(x + r * 0.7, y - r * 0.72, x + r * 0.7, y - r * 1.05)


def draw_mirror_enemy(x, y, body, radius, scale, frame):
    r = radius * scale
    shimmer = math.sin(frame * 0.16) * r * 0.08
    dudraw.set_pen_color_rgb(97, 47, 88)
    dudraw.filled_triangle(x, y - r * 1.02, x - r * 0.78, y, x, y + r * 1.04)
    set_color(body)
    dudraw.filled_triangle(x, y - r * 1.02, x + r * 0.78, y, x, y + r * 1.04)
    dudraw.set_pen_color_rgb(246, 183, 224)
    dudraw.line(x, y - r * 0.92, x, y + r * 0.92)
    for side in (-1, 1):
        mask_x = x + side * (r * 0.3 + shimmer * side)
        dudraw.filled_circle(mask_x, y + r * 0.24, r * 0.2)
        dudraw.set_pen_color_rgb(46, 34, 49)
        dudraw.filled_circle(mask_x + side * r * 0.04, y + r * 0.29, r * 0.045)


def draw_lancer_enemy(x, y, body, radius, scale, facing_x, facing_y, frame):
    r = radius * scale
    stride = math.sin(frame * 0.4) * r * 0.35
    set_color(darken(body, 35))
    dudraw.filled_ellipse(x, y - r * 0.16, r * 1.28, r * 0.54)
    for side in (-0.55, 0.55):
        dudraw.line(x - facing_y * side * r, y - r * 0.46, x - facing_y * side * r + stride * side, y - r)
    set_color(body)
    dudraw.filled_circle(x, y + r * 0.46, r * 0.36)
    dudraw.set_pen_color_rgb(50, 47, 62)
    dudraw.filled_triangle(x - r * 0.42, y + r * 0.55, x + r * 0.42, y + r * 0.55, x, y + r * 1.05)
    lance_x, lance_y = enemy_offset(x, y, facing_x, facing_y, r * 0.4, 0)
    tip_x, tip_y = enemy_offset(x, y, facing_x, facing_y, r * 2.1, 0)
    dudraw.set_pen_color_rgb(225, 193, 111)
    dudraw.line(lance_x, lance_y, tip_x, tip_y)
    dudraw.filled_triangle(tip_x + facing_x * r * 0.3, tip_y + facing_y * r * 0.3, tip_x - facing_y * r * 0.12, tip_y + facing_x * r * 0.12, tip_x + facing_y * r * 0.12, tip_y - facing_x * r * 0.12)


def draw_king_enemy(x, y, body, radius, scale, frame):
    r = radius * scale
    aura = r * (1.3 + 0.05 * math.sin(frame * 0.1))
    set_color(brighten(body, 45))
    dudraw.circle(x, y + r * 0.1, aura)
    set_color(body)
    dudraw.filled_triangle(x - r * 0.95, y - r * 0.92, x + r * 0.95, y - r * 0.92, x, y + r * 1.12)
    dudraw.set_pen_color_rgb(37, 29, 44)
    dudraw.filled_circle(x, y + r * 0.64, r * 0.5)
    dudraw.set_pen_color_rgb(244, 200, 65)
    dudraw.filled_triangle(x - r * 0.48, y + r * 0.98, x - r * 0.27, y + r * 1.45, x - r * 0.08, y + r * 0.98)
    dudraw.filled_triangle(x - r * 0.12, y + r * 0.98, x + r * 0.02, y + r * 1.58, x + r * 0.18, y + r * 0.98)
    dudraw.filled_triangle(x + r * 0.12, y + r * 0.98, x + r * 0.39, y + r * 1.4, x + r * 0.5, y + r * 0.98)
    dudraw.set_pen_color_rgb(235, 76, 108)
    dudraw.filled_circle(x, y + r * 1.2, r * 0.08)
    dudraw.set_pen_color_rgb(238, 230, 186)
    dudraw.filled_circle(x - r * 0.18, y + r * 0.68, r * 0.08)
    dudraw.filled_circle(x + r * 0.18, y + r * 0.68, r * 0.08)


def draw_enemy_face(x, y, scale, facing_x, facing_y):
    eye_x = facing_x * 0.035 * scale
    eye_y = facing_y * 0.025 * scale

    dudraw.set_pen_color_rgb(245, 236, 207)
    dudraw.filled_circle(x - 0.055 * scale + eye_x, y + 0.025 * scale + eye_y, 0.045 * scale)
    dudraw.filled_circle(x + 0.055 * scale + eye_x, y + 0.025 * scale + eye_y, 0.04 * scale)
    dudraw.set_pen_color_rgb(42, 34, 34)
    dudraw.filled_circle(x - 0.055 * scale + eye_x, y + 0.025 * scale + eye_y, 0.018 * scale)
    dudraw.filled_circle(x + 0.055 * scale + eye_x, y + 0.025 * scale + eye_y, 0.016 * scale)


def draw_enemies(enemies, settings, frame):
    for enemy in enemies:
        facing_x, facing_y = enemy_facing(enemy)

        if is_amazing(settings) and enemy.enemy_type in ("boss", "wraith"):
            set_color(brighten(enemy.color, 45))
            dudraw.circle(enemy.x, enemy.y, enemy.radius + 0.22 + 0.03 * math.sin(frame * 0.12))

        draw_enemy_character(
            enemy.x,
            enemy.y,
            enemy.enemy_type,
            enemy.color,
            enemy.radius,
            frame,
            1.0,
            facing_x,
            facing_y,
            enemy.poison_timer > 0,
            enemy.slow_timer > 0,
        )

        if enemy.path_index >= len(PATH) - 5:
            dudraw.set_pen_color_rgb(229, 81, 78)
            dudraw.circle(enemy.x, enemy.y, enemy.radius + 0.17 + 0.02 * math.sin(frame * 0.2))
            if frame % 24 < 12:
                dudraw.filled_triangle(enemy.x, enemy.y + 0.88, enemy.x - 0.08, enemy.y + 0.75, enemy.x + 0.08, enemy.y + 0.75)

        if settings.get("show_health_bars", True):
            health_width = 0.7 * max(enemy.health / enemy.max_health, 0)
            health_ratio = max(enemy.health / enemy.max_health, 0)
            dudraw.set_pen_color_rgb(18, 23, 28)
            dudraw.filled_rectangle(enemy.x, enemy.y + 0.55, 0.38, 0.05)
            dudraw.set_pen_color_rgb(112, 123, 132)
            dudraw.rectangle(enemy.x, enemy.y + 0.55, 0.38, 0.05)

            if health_ratio < 0.3:
                dudraw.set_pen_color_rgb(224, 79, 67)
            elif health_ratio < 0.65:
                dudraw.set_pen_color_rgb(232, 194, 70)
            else:
                dudraw.set_pen_color_rgb(62, 178, 82)
            dudraw.filled_rectangle(enemy.x - (0.7 - health_width) / 2, enemy.y + 0.55, health_width / 2, 0.035)
            if health_width > 0.1:
                dudraw.set_pen_color_rgb(237, 247, 227)
                dudraw.line(enemy.x - 0.34, enemy.y + 0.57, enemy.x - 0.34 + health_width * 0.7, enemy.y + 0.57)

        threat = DIFFICULTIES[enemy.difficulty]["threat"]
        if threat > 0 and settings.get("show_threat_marks", True):
            set_color(DIFFICULTIES[enemy.difficulty]["color"])
            for marker in range(threat):
                marker_x = enemy.x + (marker - (threat - 1) / 2) * 0.13
                dudraw.filled_triangle(
                    marker_x,
                    enemy.y + 0.72,
                    marker_x - 0.05,
                    enemy.y + 0.64,
                    marker_x + 0.05,
                    enemy.y + 0.64,
                )


def draw_shots(shots, settings):
    for shot in shots:
        start_x, start_y, end_x, end_y, timer, color = shot[:6]
        shot_type = shot[6] if len(shot) > 6 else "laser"
        if is_amazing(settings):
            set_color((255, 248, 196))
            if shot_type == "storm":
                draw_lightning_shot(start_x, start_y, end_x, end_y, timer)
            elif shot_type == "titan":
                draw_lightning_shot(start_x, start_y, end_x, end_y, timer)
            elif shot_type == "mortar":
                pass
            elif shot_type == "meteor":
                pass
            elif shot_type == "cannon":
                draw_shell_shot(start_x, start_y, end_x, end_y, timer, color)
            elif shot_type == "frost":
                draw_frost_shot(start_x, start_y, end_x, end_y, timer, color)
            elif shot_type == "venom":
                draw_venom_shot(start_x, start_y, end_x, end_y, timer, color)
            elif shot_type in ("arrow", "sniper"):
                pass
            elif shot_type == "oracle":
                pass
            elif shot_type == "thornheart":
                pass
            elif shot_type == "royal_mint":
                pass
            elif shot_type == "starfall":
                pass
            elif shot_type == "laser":
                dudraw.set_pen_color_rgb(126, 18, 39)
                dudraw.line(start_x, start_y, end_x, end_y)
                dudraw.set_pen_color_rgb(255, 101, 120)
                dudraw.line(start_x, start_y, end_x, end_y)
                dudraw.set_pen_color_rgb(255, 231, 235)
                dudraw.line(start_x, start_y, end_x, end_y)
            else:
                set_color(brighten(color, 90))
                dudraw.line(start_x, start_y, end_x, end_y)
                set_color(brighten(color, 35))
                dudraw.line(start_x, start_y, end_x, end_y)
            if shot_type not in ("arrow", "sniper"):
                set_color(brighten(color, 60))
                dudraw.filled_circle(end_x, end_y, 0.08 + timer * 0.015)
                dudraw.circle(end_x, end_y, 0.12 + timer * 0.025)
                for i in range(1, 4):
                    t = i / 4
                    spark_x = start_x + (end_x - start_x) * t
                    spark_y = start_y + (end_y - start_y) * t
                    dudraw.filled_circle(spark_x, spark_y, 0.025 + timer * 0.004)

        set_color(color)
        if shot_type == "storm":
            draw_lightning_shot(start_x, start_y, end_x, end_y, timer)
        elif shot_type == "titan":
            draw_lightning_shot(start_x, start_y, end_x, end_y, timer)
        elif shot_type == "mortar":
            draw_mortar_shell_shot(start_x, start_y, end_x, end_y, timer, color)
        elif shot_type == "meteor":
            draw_meteor_shot(start_x, start_y, end_x, end_y, timer, color)
        elif shot_type == "cannon":
            draw_shell_shot(start_x, start_y, end_x, end_y, timer, color)
        elif shot_type == "frost":
            draw_frost_shot(start_x, start_y, end_x, end_y, timer, color)
        elif shot_type == "venom":
            draw_venom_shot(start_x, start_y, end_x, end_y, timer, color)
        elif shot_type == "oracle":
            draw_oracle_sunbeam(start_x, start_y, end_x, end_y, timer)
        elif shot_type == "thornheart":
            draw_thorn_tentacle(start_x, start_y, end_x, end_y, timer)
        elif shot_type == "royal_mint":
            draw_minted_coin_shot(start_x, start_y, end_x, end_y, timer)
        elif shot_type == "starfall":
            draw_starfall_shot(start_x, start_y, end_x, end_y, timer)
        elif shot_type == "arrow":
            draw_arrow_shot(start_x, start_y, end_x, end_y, timer, color)
        elif shot_type == "sniper":
            draw_sniper_shot(start_x, start_y, end_x, end_y, timer, color)
        else:
            dudraw.line(start_x, start_y, end_x, end_y)
        shot[4] = timer - 1


def draw_lightning_shot(start_x, start_y, end_x, end_y, timer):
    dx = end_x - start_x
    dy = end_y - start_y
    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        return

    side_x = -dy / length
    side_y = dx / length
    last_x = start_x
    last_y = start_y

    dudraw.set_pen_color_rgb(246, 252, 255)
    for i in range(1, 6):
        t = i / 6
        jitter = ((i % 2) * 2 - 1) * (0.08 + timer * 0.01)
        next_x = start_x + dx * t + side_x * jitter
        next_y = start_y + dy * t + side_y * jitter
        dudraw.line(last_x, last_y, next_x, next_y)
        if i in (2, 4):
            dudraw.line(next_x, next_y, next_x + side_x * jitter * 1.8, next_y + side_y * jitter * 1.8)
        last_x = next_x
        last_y = next_y

    dudraw.line(last_x, last_y, end_x, end_y)


def draw_oracle_sunbeam(start_x, start_y, end_x, end_y, timer):
    dudraw.set_pen_color_rgb(164, 104, 22)
    dudraw.line(start_x, start_y, end_x, end_y)
    dudraw.set_pen_color_rgb(247, 185, 52)
    dudraw.line(start_x, start_y, end_x, end_y)
    dudraw.set_pen_color_rgb(255, 236, 128)
    dudraw.line(start_x, start_y, end_x, end_y)
    dudraw.set_pen_color_rgb(255, 255, 235)
    dudraw.line(start_x, start_y, end_x, end_y)

    dudraw.set_pen_color_rgb(255, 225, 90)
    dudraw.filled_circle(start_x, start_y, 0.09 + timer * 0.006)
    dudraw.circle(start_x, start_y, 0.15 + timer * 0.01)
    dudraw.set_pen_color_rgb(255, 244, 170)
    dudraw.circle(end_x, end_y, 0.18 + timer * 0.018)
    dudraw.set_pen_color_rgb(255, 255, 236)
    dudraw.filled_circle(end_x, end_y, 0.065 + timer * 0.006)


def draw_thorn_tentacle(start_x, start_y, end_x, end_y, timer):
    dx = end_x - start_x
    dy = end_y - start_y
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return

    side_x = -dy / length
    side_y = dx / length
    wave = 0.1 + timer * 0.012
    points = [(start_x, start_y)]
    for index in range(1, 7):
        progress = index / 7
        turn = -1 if index % 2 else 1
        points.append((
            start_x + dx * progress + side_x * wave * turn,
            start_y + dy * progress + side_y * wave * turn,
        ))
    points.append((end_x, end_y))

    dudraw.set_pen_color_rgb(32, 77, 39)
    for first, second in zip(points, points[1:]):
        dudraw.line(first[0], first[1], second[0], second[1])
    dudraw.set_pen_color_rgb(78, 166, 62)
    for first, second in zip(points, points[1:]):
        dudraw.line(first[0] + side_x * 0.015, first[1] + side_y * 0.015, second[0] + side_x * 0.015, second[1] + side_y * 0.015)

    dudraw.set_pen_color_rgb(207, 218, 112)
    for index in (2, 4, 6):
        thorn_x, thorn_y = points[index]
        dudraw.filled_triangle(
            thorn_x,
            thorn_y,
            thorn_x + side_x * 0.13 - dx / length * 0.035,
            thorn_y + side_y * 0.13 - dy / length * 0.035,
            thorn_x + side_x * 0.02 + dx / length * 0.04,
            thorn_y + side_y * 0.02 + dy / length * 0.04,
        )
    dudraw.set_pen_color_rgb(182, 45, 67)
    dudraw.filled_circle(end_x, end_y, 0.075 + timer * 0.01)
    dudraw.set_pen_color_rgb(119, 245, 92)
    dudraw.circle(end_x, end_y, 0.13 + timer * 0.012)


def draw_minted_coin_shot(start_x, start_y, end_x, end_y, timer):
    travel = max(0.18, min(0.94, 1 - timer * 0.18))
    x = start_x + (end_x - start_x) * travel
    y = start_y + (end_y - start_y) * travel + math.sin(travel * math.pi) * 0.12
    width = 0.035 + abs(math.sin(timer * math.pi / 2)) * 0.045
    dudraw.set_pen_color_rgb(131, 83, 23)
    dudraw.filled_ellipse(x, y, width + 0.018, 0.095)
    dudraw.set_pen_color_rgb(239, 187, 53)
    dudraw.filled_ellipse(x, y, width, 0.078)
    dudraw.set_pen_color_rgb(255, 232, 119)
    dudraw.line(x - width * 0.45, y + 0.02, x + width * 0.45, y + 0.02)
    dudraw.set_pen_color_rgb(252, 209, 73)
    dudraw.circle(end_x, end_y, 0.12 + timer * 0.012)


def draw_starfall_shot(start_x, start_y, end_x, end_y, timer):
    travel = max(0.2, min(0.96, 1 - timer * 0.18))
    x = start_x + (end_x - start_x) * travel
    y = start_y + (end_y - start_y) * travel + math.sin(travel * math.pi) * 0.34
    tail_x = start_x + (end_x - start_x) * max(0.0, travel - 0.13)
    tail_y = start_y + (end_y - start_y) * max(0.0, travel - 0.13) + math.sin(max(0.0, travel - 0.13) * math.pi) * 0.34

    dudraw.set_pen_color_rgb(87, 132, 229)
    dudraw.line(tail_x, tail_y, x, y)
    dudraw.set_pen_color_rgb(245, 152, 235)
    dudraw.line((tail_x + x) / 2, (tail_y + y) / 2, x, y)
    dudraw.set_pen_color_rgb(255, 242, 164)
    for index in range(5):
        first = math.pi / 2 + index * 4 * math.pi / 5
        second = math.pi / 2 + (index + 1) * 4 * math.pi / 5
        dudraw.line(
            x + math.cos(first) * 0.11,
            y + math.sin(first) * 0.11,
            x + math.cos(second) * 0.11,
            y + math.sin(second) * 0.11,
        )
    dudraw.set_pen_color_rgb(255, 251, 217)
    dudraw.filled_circle(x, y, 0.035)
    dudraw.set_pen_color_rgb(235, 151, 238)
    dudraw.circle(end_x, end_y, 0.12 + timer * 0.014)


def draw_shell_shot(start_x, start_y, end_x, end_y, timer, color):
    t = max(0.2, min(0.9, 1 - timer * 0.16))
    x = start_x + (end_x - start_x) * t
    y = start_y + (end_y - start_y) * t + math.sin(t * math.pi) * 0.28

    set_color(darken(color, 35))
    dudraw.filled_circle(x - (end_x - start_x) * 0.05, y - 0.04, 0.06)
    set_color(color)
    dudraw.filled_circle(x, y, 0.08 + timer * 0.006)
    set_color(brighten(color, 55))
    dudraw.filled_circle(x - 0.025, y + 0.025, 0.03)


def draw_mortar_shell_shot(start_x, start_y, end_x, end_y, timer, color):
    progress = min(1.0, max(0.13, 1 - (timer - 1) * 0.29))
    dx = end_x - start_x
    dy = end_y - start_y
    distance = math.sqrt(dx * dx + dy * dy)
    arc_height = min(2.6, max(1.25, distance * 0.46))
    x = start_x + dx * progress
    y = start_y + dy * progress + math.sin(progress * math.pi) * arc_height

    previous_progress = max(0.08, progress - 0.08)
    previous_x = start_x + dx * previous_progress
    previous_y = (
        start_y
        + dy * previous_progress
        + math.sin(previous_progress * math.pi) * arc_height
    )

    set_color(darken(color, 38))
    dudraw.line(previous_x, previous_y, x, y)
    dudraw.filled_circle(x, y, 0.095)
    set_color(color)
    dudraw.filled_circle(x, y, 0.075)
    set_color(brighten(color, 60))
    dudraw.filled_circle(x - 0.02, y + 0.024, 0.027)
    if progress > 0.78:
        set_color(brighten(color, 50))
        dudraw.circle(end_x, end_y, 0.12 + (progress - 0.78) * 0.3)


def draw_meteor_shot(start_x, start_y, end_x, end_y, timer, color):
    progress = min(1.0, max(0.1, 1 - (timer - 1) * 0.3))
    dx = end_x - start_x
    dy = end_y - start_y
    distance = math.sqrt(dx * dx + dy * dy)
    arc_height = min(3.15, max(1.55, distance * 0.52))
    x = start_x + dx * progress
    y = start_y + dy * progress + math.sin(progress * math.pi) * arc_height
    previous = max(0.04, progress - 0.1)
    tail_x = start_x + dx * previous
    tail_y = start_y + dy * previous + math.sin(previous * math.pi) * arc_height

    dudraw.set_pen_color_rgb(143, 44, 28)
    dudraw.line(tail_x, tail_y, x, y)
    dudraw.set_pen_color_rgb(255, 98, 28)
    dudraw.line((tail_x + x) / 2, (tail_y + y) / 2, x, y)
    dudraw.set_pen_color_rgb(55, 47, 45)
    dudraw.filled_circle(x, y, 0.14)
    set_color(color)
    dudraw.filled_circle(x, y, 0.105)
    dudraw.set_pen_color_rgb(255, 211, 66)
    dudraw.filled_circle(x - 0.035, y + 0.04, 0.04)
    if progress > 0.82:
        dudraw.set_pen_color_rgb(255, 121, 35)
        dudraw.circle(end_x, end_y, 0.18 + (progress - 0.82) * 0.75)


def draw_frost_shot(start_x, start_y, end_x, end_y, timer, color):
    travel = max(0.25, min(0.9, 1 - timer * 0.15))
    x = start_x + (end_x - start_x) * travel
    y = start_y + (end_y - start_y) * travel
    rotation = timer * 0.2

    set_color(darken(color, 18))
    dudraw.filled_circle(x, y, 0.095)
    dudraw.set_pen_color_rgb(229, 252, 255)
    for arm in range(6):
        angle = rotation + arm * math.pi / 3
        tip_x = x + math.cos(angle) * 0.16
        tip_y = y + math.sin(angle) * 0.16
        dudraw.line(x, y, tip_x, tip_y)
        branch_x = x + math.cos(angle) * 0.1
        branch_y = y + math.sin(angle) * 0.1
        dudraw.line(branch_x, branch_y, branch_x + math.cos(angle + 0.7) * 0.055, branch_y + math.sin(angle + 0.7) * 0.055)
        dudraw.line(branch_x, branch_y, branch_x + math.cos(angle - 0.7) * 0.055, branch_y + math.sin(angle - 0.7) * 0.055)

    set_color(brighten(color, 65))
    dudraw.filled_circle(x, y, 0.03)
    for trail in range(1, 4):
        t = max(0.1, travel - trail * 0.11)
        crystal_x = start_x + (end_x - start_x) * t
        crystal_y = start_y + (end_y - start_y) * t
        dudraw.filled_circle(crystal_x, crystal_y, 0.018 + trail * 0.006)


def draw_venom_shot(start_x, start_y, end_x, end_y, timer, color):
    set_color(color)
    for i in range(1, 4):
        t = i / 4
        x = start_x + (end_x - start_x) * t
        y = start_y + (end_y - start_y) * t - math.sin(t * math.pi) * 0.08
        dudraw.filled_circle(x, y, 0.045 + timer * 0.004)
        set_color(brighten(color, 65))
        dudraw.filled_circle(x - 0.012, y + 0.016, 0.014)
        set_color(color)


def draw_arrow_shot(start_x, start_y, end_x, end_y, timer, color):
    dx = end_x - start_x
    dy = end_y - start_y
    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        return

    aim_x = dx / length
    aim_y = dy / length
    side_x = -aim_y
    side_y = aim_x
    travel = max(0.24, min(0.94, 1 - timer * 0.17))
    tip_x = start_x + dx * travel
    tip_y = start_y + dy * travel
    tail_x = tip_x - aim_x * 0.34
    tail_y = tip_y - aim_y * 0.34

    dudraw.set_pen_color_rgb(103, 62, 33)
    dudraw.line(tail_x, tail_y, tip_x, tip_y)
    dudraw.set_pen_color_rgb(230, 190, 92)
    dudraw.line(tail_x + aim_x * 0.03, tail_y + aim_y * 0.03, tip_x - aim_x * 0.07, tip_y - aim_y * 0.07)
    dudraw.set_pen_color_rgb(230, 224, 187)
    dudraw.filled_triangle(
        tip_x,
        tip_y,
        tip_x - aim_x * 0.11 + side_x * 0.055,
        tip_y - aim_y * 0.11 + side_y * 0.055,
        tip_x - aim_x * 0.11 - side_x * 0.055,
        tip_y - aim_y * 0.11 - side_y * 0.055,
    )
    dudraw.set_pen_color_rgb(70, 112, 68)
    dudraw.filled_triangle(
        tail_x,
        tail_y,
        tail_x + aim_x * 0.1 + side_x * 0.07,
        tail_y + aim_y * 0.1 + side_y * 0.07,
        tail_x + aim_x * 0.1,
        tail_y + aim_y * 0.1,
    )
    dudraw.filled_triangle(
        tail_x,
        tail_y,
        tail_x + aim_x * 0.1 - side_x * 0.07,
        tail_y + aim_y * 0.1 - side_y * 0.07,
        tail_x + aim_x * 0.1,
        tail_y + aim_y * 0.1,
    )


def draw_sniper_shot(start_x, start_y, end_x, end_y, timer, color):
    dx = end_x - start_x
    dy = end_y - start_y
    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        return

    aim_x = dx / length
    aim_y = dy / length
    travel = max(0.3, min(0.96, 1 - timer * 0.18))
    bullet_x = start_x + dx * travel
    bullet_y = start_y + dy * travel
    tail_x = bullet_x - aim_x * 0.17
    tail_y = bullet_y - aim_y * 0.17

    dudraw.set_pen_color_rgb(255, 220, 130)
    dudraw.line(tail_x, tail_y, bullet_x, bullet_y)
    dudraw.set_pen_color_rgb(219, 177, 79)
    dudraw.filled_circle(bullet_x, bullet_y, 0.072)
    dudraw.set_pen_color_rgb(130, 92, 43)
    dudraw.circle(bullet_x, bullet_y, 0.076)
    dudraw.set_pen_color_rgb(255, 245, 193)
    dudraw.filled_circle(bullet_x + aim_x * 0.018, bullet_y + aim_y * 0.018, 0.03)


def draw_particles(particles, settings):
    if not is_amazing(settings):
        particles.clear()
        return

    for particle in particles[:]:
        x, y, size, timer, color = particle[:5]
        label = particle[5] if len(particle) > 5 else None
        set_color(color)
        if label is None or not settings.get("show_floating_text", True):
            dudraw.circle(x, y, size)
            dudraw.filled_circle(x, y, max(0.02, size * 0.28))
        else:
            dudraw.set_pen_color_rgb(18, 23, 30)
            dudraw.filled_rectangle(x, y + size, min(0.95, len(label) * 0.045 + 0.14), 0.13)
            set_color(color)
            dudraw.text(x, y + size, label)
            dudraw.filled_circle(x - 0.22, y + size * 0.9, 0.025)

        particle[1] = y + (0.03 if label is not None else 0)
        particle[2] = size + (0.018 if label is not None else 0.045)
        particle[3] = timer - 1

        if particle[3] <= 0:
            particles.remove(particle)


def draw_placement_preview(towers, selected_tower, special_placed, settings, money):
    if not is_amazing(settings) or selected_tower is None:
        return

    mouse_x = dudraw.mouse_x()
    mouse_y = dudraw.mouse_y()
    grid_x = int(mouse_x)
    grid_y = int(mouse_y)

    if selected_tower == "special":
        tower_type = settings["special_tower"]
    else:
        tower_type = selected_tower

    if grid_y < 0 or grid_y >= GRID_HEIGHT:
        return

    reason = placement_block_reason(grid_x, grid_y, towers, money, selected_tower, special_placed, settings)
    valid = reason is None
    stats = get_tower_stats(tower_type)

    if valid:
        set_color((238, 247, 218))
    else:
        set_color((237, 128, 111))

    dudraw.square(grid_x + 0.5, grid_y + 0.5, 0.5)
    dudraw.filled_square(grid_x + 0.5, grid_y + 0.5, 0.08)
    dudraw.circle(grid_x + 0.5, grid_y + 0.5, 0.32)

    if not valid:
        dudraw.line(grid_x + 0.25, grid_y + 0.25, grid_x + 0.75, grid_y + 0.75)
        dudraw.line(grid_x + 0.75, grid_y + 0.25, grid_x + 0.25, grid_y + 0.75)

    if stats["range"] > 0:
        set_color(brighten(stats["color"], 65))
        dudraw.circle(grid_x + 0.5, grid_y + 0.5, stats["range"])

    if not valid:
        dudraw.set_pen_color_rgb(20, 24, 31)
        dudraw.filled_rectangle(grid_x + 0.5, min(GRID_HEIGHT - 0.35, grid_y + 1.15), 1.75, 0.25)
        dudraw.set_pen_color_rgb(255, 221, 190)
        dudraw.text(grid_x + 0.5, min(GRID_HEIGHT - 0.37, grid_y + 1.13), PLACEMENT_BLOCK_MESSAGES[reason])


def draw_button(x, y, label, color, selected, affordable=True):
    if selected:
        dudraw.set_pen_color_rgb(246, 231, 148)
        dudraw.filled_rectangle(x, y, 1.18, 0.33)

    dudraw.set_pen_color_rgb(12, 16, 22)
    dudraw.filled_rectangle(x + 0.03, y - 0.035, 1.09, 0.27)
    dudraw.set_pen_color_rgb(28, 33, 41) if affordable else dudraw.set_pen_color_rgb(40, 39, 43)
    dudraw.filled_rectangle(x, y, 1.08, 0.26)
    dudraw.set_pen_color_rgb(68, 78, 91) if affordable else dudraw.set_pen_color_rgb(85, 61, 62)
    dudraw.rectangle(x, y, 1.08, 0.26)
    set_color(color if affordable else darken(color, 48))
    dudraw.filled_circle(x - 0.72, y, 0.16)
    set_color(brighten(color, 55) if affordable else color)
    dudraw.filled_circle(x - 0.77, y + 0.05, 0.055)
    set_color(color if affordable else darken(color, 48))
    dudraw.filled_rectangle(x, y - 0.22, 1.0, 0.018)

    if affordable:
        dudraw.set_pen_color(dudraw.WHITE)
    else:
        dudraw.set_pen_color_rgb(165, 164, 169)
    dudraw.text(x + 0.08, y - 0.02, label)


def draw_menu_button(x, y, half_width, half_height, label, selected=False):
    if selected:
        dudraw.set_pen_color_rgb(246, 231, 148)
        dudraw.filled_rectangle(x, y, half_width + 0.08, half_height + 0.08)

    dudraw.set_pen_color_rgb(10, 14, 20)
    dudraw.filled_rectangle(x + 0.04, y - 0.05, half_width, half_height)
    dudraw.set_pen_color_rgb(27, 35, 46)
    dudraw.filled_rectangle(x, y, half_width, half_height)
    dudraw.set_pen_color_rgb(91, 112, 134)
    dudraw.rectangle(x, y, half_width, half_height)
    dudraw.set_pen_color_rgb(53, 69, 84)
    dudraw.line(x - half_width + 0.12, y + half_height - 0.1, x + half_width - 0.12, y + half_height - 0.1)
    if selected:
        dudraw.set_pen_color_rgb(246, 231, 148)
        dudraw.filled_rectangle(x - half_width + 0.08, y, 0.025, half_height - 0.11)
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(x, y - 0.03, label)


def point_in_rect(px, py, x, y, half_width, half_height):
    return x - half_width <= px <= x + half_width and y - half_height <= py <= y + half_height


def draw_release_tower(x, y, tower_type, frame, scale=1.0):
    stats = get_tower_stats(tower_type)
    bob = math.sin(frame * 0.045 + x) * 0.08
    base = stats["color"]
    light = brighten(base, 65)
    dark = (
        max(0, base[0] - 55),
        max(0, base[1] - 55),
        max(0, base[2] - 55),
    )

    dudraw.set_pen_color_rgb(8, 12, 19)
    dudraw.filled_ellipse(x + 0.25 * scale, y - 0.62 * scale, 1.05 * scale, 0.26 * scale)

    dudraw.set_pen_color_rgb(188, 182, 167)
    dudraw.filled_ellipse(x, y - 0.38 * scale, 0.78 * scale, 0.28 * scale)
    dudraw.set_pen_color_rgb(72, 66, 61)
    dudraw.rectangle(x, y - 0.38 * scale, 0.78 * scale, 0.28 * scale)

    set_color(dark)
    dudraw.filled_rectangle(x - 0.08 * scale, y + bob, 0.52 * scale, 0.58 * scale)
    set_color(base)
    dudraw.filled_rectangle(x, y + bob + 0.04 * scale, 0.5 * scale, 0.55 * scale)
    set_color(light)
    dudraw.filled_ellipse(x, y + bob + 0.6 * scale, 0.53 * scale, 0.22 * scale)

    angle = math.sin(frame * 0.035 + x) * 0.35
    aim_x = math.cos(angle)
    aim_y = math.sin(angle)

    if tower_type in TOWER_TYPES:
        draw_tower_character_details(x, y + bob, tower_type, aim_x, aim_y, frame, scale)
    elif tower_type in SPECIAL_TOWERS:
        set_color(brighten(base, 70))
        dudraw.circle(x, y + bob + 0.08 * scale, 0.8 * scale)
        dudraw.set_pen_color_rgb(255, 245, 190)
        dudraw.filled_circle(x, y + bob + 0.2 * scale, 0.16 * scale)
        for i in range(5):
            orbit = frame * 0.035 + i * 2 * math.pi / 5
            set_color(brighten(base, 85))
            dudraw.filled_circle(x + math.cos(orbit) * 0.75 * scale, y + bob + math.sin(orbit) * 0.5 * scale, 0.06 * scale)

    if tower_type != "arrow":
        barrel_x = x + aim_x * 0.92 * scale
        barrel_y = y + bob + 0.45 * scale + aim_y * 0.4 * scale
        dudraw.set_pen_color_rgb(16, 20, 28)
        dudraw.line(x + 0.08 * scale, y + bob + 0.42 * scale, barrel_x, barrel_y)
        set_color(stats["shot_color"])
        dudraw.filled_circle(barrel_x, barrel_y, 0.12 * scale)

    if tower_type in ("storm", "frost", "laser"):
        set_color(brighten(stats["shot_color"], 45))
        dudraw.circle(x, y + bob + 0.1 * scale, 0.82 * scale + 0.08 * math.sin(frame * 0.08))


draw_towers = tower_models.draw_towers
draw_release_tower = tower_models.draw_release_tower


def draw_release_enemy(x, y, enemy_type, frame, scale=1.0):
    stats = ENEMY_TYPES[enemy_type]
    draw_enemy_character(x, y, enemy_type, stats["color"], stats["radius"] * ENEMY_SIZE_SCALE, frame, 1.45 * scale)


def draw_release_menu_background(frame):
    dudraw.clear(dudraw.BLACK)

    for band in range(18):
        y = band * (GRID_HEIGHT + 2) / 18
        red = 89 + band * 3
        green = 152 + band * 3
        blue = 196 + band * 2
        dudraw.set_pen_color_rgb(min(180, red), min(222, green), min(235, blue))
        dudraw.filled_rectangle(GRID_WIDTH / 2, y + 0.5, GRID_WIDTH / 2, 0.52)

    dudraw.set_pen_color_rgb(255, 229, 113)
    dudraw.filled_circle(20.0, 13.4, 1.05)
    dudraw.set_pen_color_rgb(255, 244, 166)
    dudraw.filled_circle(19.72, 13.75, 0.32)

    for i in range(7):
        cloud_x = (i * 4.0 + frame * 0.01) % 28 - 2
        cloud_y = 11.2 + (i % 3) * 1.0
        dudraw.set_pen_color_rgb(236, 246, 247)
        dudraw.filled_circle(cloud_x, cloud_y, 0.32)
        dudraw.filled_circle(cloud_x + 0.35, cloud_y + 0.08, 0.42)
        dudraw.filled_circle(cloud_x + 0.78, cloud_y, 0.3)

    dudraw.set_pen_color_rgb(83, 139, 83)
    dudraw.filled_rectangle(12, 6.3, 12, 1.2)
    for i in range(12):
        hill_x = i * 2.4 - 1.2
        dudraw.set_pen_color_rgb(101, 164, 97)
        dudraw.filled_circle(hill_x, 6.8, 1.45)

    dudraw.set_pen_color_rgb(164, 211, 126)
    dudraw.filled_rectangle(12, 3.15, 12, 3.15)

    for x in range(24):
        for y in range(0, 7):
            if (x + y) % 2 == 0:
                dudraw.set_pen_color_rgb(177, 221, 136)
            else:
                dudraw.set_pen_color_rgb(158, 207, 121)
            dudraw.filled_rectangle(x + 0.5, y + 0.5, 0.5, 0.5)

    road_points = [(0, 4.7), (5, 4.7), (5, 3.0), (11, 3.0), (11, 5.05), (18, 5.05), (18, 3.75), (24, 3.75)]
    dudraw.set_pen_color_rgb(114, 91, 61)
    for x, y in road_points:
        dudraw.filled_circle(x, y, 0.58)
    for index in range(len(road_points) - 1):
        x1, y1 = road_points[index]
        x2, y2 = road_points[index + 1]
        dudraw.line(x1, y1, x2, y2)

    dudraw.set_pen_color_rgb(207, 182, 136)
    for index in range(len(road_points) - 1):
        x1, y1 = road_points[index]
        x2, y2 = road_points[index + 1]
        dudraw.line(x1, y1, x2, y2)
    for x, y in road_points:
        dudraw.filled_circle(x, y, 0.43)

    pulse = int(frame / 4) % 9
    for i in range(9):
        px = (i * 2.7 + frame * 0.035) % GRID_WIDTH
        py = 4.2 + math.sin(frame * 0.04 + i) * 0.6
        if i == pulse:
            dudraw.set_pen_color_rgb(255, 239, 128)
        else:
            dudraw.set_pen_color_rgb(145, 105, 65)
        dudraw.filled_circle(px, py, 0.065)

    for i in range(42):
        x = (i * 5.13 + frame * 0.008) % GRID_WIDTH
        y = 0.55 + ((i * 2.31) % 6.0)
        if 2.45 < y < 5.55 and (x < 5.8 or 4.4 < x < 18.8):
            continue
        if i % 3 == 0:
            dudraw.set_pen_color_rgb(237, 222, 104)
        elif i % 3 == 1:
            dudraw.set_pen_color_rgb(238, 166, 191)
        else:
            dudraw.set_pen_color_rgb(111, 154, 86)
        dudraw.filled_circle(x, y, 0.035 + (i % 2) * 0.012)

    draw_release_tower(3.0, 3.4, "starfall", frame, 0.72)
    draw_release_tower(7.6, 5.25, "meteor", frame, 0.76)
    draw_release_tower(14.7, 5.85, "royal_mint", frame, 0.72)
    draw_release_tower(21.0, 4.8, "guardian", frame, 0.68)

    draw_release_enemy((frame * 0.035) % 26 - 1, 4.75, "runner", frame, 0.92)
    draw_release_enemy((frame * 0.025 + 8) % 26 - 1, 3.1, "shield", frame, 1.0)
    draw_release_enemy((frame * 0.018 + 15) % 27 - 1.5, 5.1, "boss", frame, 1.05)

    dudraw.set_pen_color_rgb(10, 14, 23)
    dudraw.filled_rectangle(6.2, 7.75, 3.0, 3.4)
    dudraw.filled_rectangle(16.55, 7.75, 4.25, 4.0)
    dudraw.set_pen_color_rgb(76, 99, 124)
    dudraw.rectangle(6.2, 7.75, 3.0, 3.4)
    dudraw.rectangle(16.55, 7.75, 4.25, 4.0)
    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.filled_rectangle(6.2, 11.15, 3.0, 0.035)
    dudraw.filled_rectangle(16.55, 11.75, 4.25, 0.035)


def draw_title_background(settings):
    dudraw.clear(dudraw.BLACK)

    if is_amazing(settings):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT + 2):
                if (x * 13 + y * 7) % 19 == 0:
                    dudraw.set_pen_color_rgb(39, 71, 84)
                    dudraw.filled_circle(x + 0.4, y + 0.25, 0.08)
                elif (x * 5 + y * 11) % 29 == 0:
                    dudraw.set_pen_color_rgb(86, 68, 112)
                    dudraw.filled_circle(x + 0.62, y + 0.6, 0.05)

    dudraw.set_pen_color_rgb(18, 25, 33)
    dudraw.filled_rectangle(12, 9, 9.5, 6.4)
    dudraw.set_pen_color_rgb(72, 93, 108)
    dudraw.rectangle(12, 9, 9.5, 6.4)
    dudraw.set_pen_color_rgb(37, 49, 62)
    dudraw.rectangle(12, 9, 9.25, 6.15)
    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.filled_rectangle(12, 15.28, 9.1, 0.035)


def draw_update_log_panel(scroll_index):
    panel_x = 16.55
    panel_y = 7.75
    page_size = 5
    max_scroll = ((len(UPDATE_LOG) - 1) // page_size) * page_size
    scroll_index = min(max(scroll_index, 0), max_scroll)

    dudraw.set_pen_color_rgb(12, 18, 28)
    dudraw.filled_rectangle(panel_x, panel_y, 4.25, 4.0)
    dudraw.set_pen_color_rgb(88, 111, 137)
    dudraw.rectangle(panel_x, panel_y, 4.25, 4.0)
    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.filled_rectangle(panel_x, panel_y + 3.94, 4.14, 0.025)

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(panel_x, panel_y + 3.5, f"UPDATE LOG  v{CURRENT_VERSION}")
    dudraw.set_pen_color_rgb(151, 169, 184)
    dudraw.text(panel_x, panel_y + 3.18, "CLICK A RELEASE FOR DETAILS")

    y = panel_y + 2.7
    for update in UPDATE_LOG[scroll_index:scroll_index + page_size]:
        entry_y = y
        dudraw.set_pen_color_rgb(43, 57, 70)
        dudraw.line(panel_x - 3.8, entry_y + 0.21, panel_x + 3.8, entry_y + 0.21)
        dudraw.set_pen_color_rgb(246, 231, 148)
        dudraw.filled_circle(panel_x - 3.65, entry_y, 0.045)
        dudraw.set_pen_color_rgb(223, 234, 239)
        dudraw.text(panel_x, y, f"v{update['version']}  {update['title']}")
        y -= 0.32

        dudraw.set_pen_color_rgb(163, 182, 194)
        for note in update["notes"][:2]:
            dudraw.text(panel_x, y, note)
            y -= 0.32

        y -= 0.2

    dudraw.set_pen_color_rgb(44, 56, 74)
    dudraw.filled_rectangle(panel_x - 3.25, panel_y - 3.55, 0.72, 0.28)
    dudraw.filled_rectangle(panel_x + 3.25, panel_y - 3.55, 0.72, 0.28)
    dudraw.set_pen_color_rgb(91, 112, 134)
    dudraw.rectangle(panel_x - 3.25, panel_y - 3.55, 0.72, 0.28)
    dudraw.rectangle(panel_x + 3.25, panel_y - 3.55, 0.72, 0.28)

    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(panel_x - 3.25, panel_y - 3.58, "PREV")
    dudraw.text(panel_x + 3.25, panel_y - 3.58, "NEXT")

    dudraw.set_pen_color_rgb(151, 169, 184)
    end_index = min(scroll_index + page_size, len(UPDATE_LOG))
    dudraw.text(panel_x, panel_y - 3.58, f"{scroll_index + 1}-{end_index} of {len(UPDATE_LOG)}")


def update_log_entry_at(x, y, scroll_index):
    entry_y = 10.45
    for index, update in enumerate(UPDATE_LOG[scroll_index:scroll_index + 5]):
        if point_in_rect(x, y, 16.55, entry_y - 0.32, 3.9, 0.5):
            return update
        entry_y -= 1.16
    return None


def draw_update_detail_screen(settings, update, page):
    draw_title_background(settings)
    details = update.get("details", update["notes"])
    page_size = 12
    max_page = max(0, (len(details) - 1) // page_size)
    page = min(max(page, 0), max_page)
    start = page * page_size
    end = min(start + page_size, len(details))

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 13.75, f"v{update['version']}  {update['title']}")
    dudraw.set_pen_color_rgb(184, 198, 207)
    dudraw.text(12, 13.15, f"CHANGE DETAILS   {start + 1}-{end} OF {len(details)}")

    dudraw.set_pen_color_rgb(12, 18, 28)
    dudraw.filled_rectangle(12, 8.4, 8.4, 4.15)
    dudraw.set_pen_color_rgb(88, 111, 137)
    dudraw.rectangle(12, 8.4, 8.4, 4.15)
    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.filled_rectangle(12, 12.48, 8.28, 0.03)

    y = 11.92
    for index, detail in enumerate(details[start:end], start + 1):
        dudraw.set_pen_color_rgb(246, 231, 148)
        dudraw.text(4.25, y, f"{index:03}")
        dudraw.set_pen_color_rgb(221, 230, 235)
        dudraw.text(12.45, y, detail)
        y -= 0.58

    draw_menu_button(6.2, 3.15, 1.65, 0.38, "PREV  (LEFT)", page > 0)
    draw_menu_button(12, 3.15, 1.65, 0.38, "BACK  (B)", True)
    draw_menu_button(17.8, 3.15, 1.65, 0.38, "NEXT  (RIGHT)", page < max_page)
    dudraw.show(25)


def run_update_detail_screen(settings, update):
    page = 0
    page_size = 12
    max_page = max(0, (len(update.get("details", update["notes"])) - 1) // page_size)

    while True:
        draw_update_detail_screen(settings, update, page)
        key = get_menu_key()
        if key in ("b", "escape"):
            return
        if key in ("left", "up"):
            page = max(0, page - 1)
        elif key in ("right", "down"):
            page = min(max_page, page + 1)
        elif key == "f":
            toggle_fullscreen(settings)

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()
            if point_in_rect(x, y, 6.2, 3.15, 1.65, 0.38):
                page = max(0, page - 1)
            elif point_in_rect(x, y, 12, 3.15, 1.65, 0.38):
                return
            elif point_in_rect(x, y, 17.8, 3.15, 1.65, 0.38):
                page = min(max_page, page + 1)


def draw_start_screen(settings, update_scroll=0, frame=0, present=True):
    draw_release_menu_background(frame)

    dudraw.set_pen_color_rgb(7, 11, 19)
    dudraw.text(12.08, 13.0, "PATHFALL DEFENSE")
    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 13.05, "PATHFALL DEFENSE")

    dudraw.set_pen_color_rgb(215, 226, 231)
    dudraw.text(12, 12.35, "Build towers. Hold the road. Survive the waves.")

    dudraw.set_pen_color_rgb(184, 198, 207)
    dudraw.text(12, 11.75, f"Current version: v{CURRENT_VERSION}")

    menu_x = 6.2
    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(menu_x, 10.88, "PLAY")
    draw_menu_button(menu_x, 10.35, 2.3, 0.38, "START  (S)", True)
    draw_menu_button(menu_x, 9.3, 2.3, 0.38, "SPECIAL  (P)")
    draw_menu_button(menu_x, 8.25, 2.3, 0.38, "DICTIONARY  (D)")
    draw_menu_button(menu_x, 7.2, 2.3, 0.38, "SETTINGS  (T)")
    draw_menu_button(menu_x, 6.15, 2.3, 0.38, "CONTROLS  (C)")
    draw_menu_button(menu_x, 5.1, 2.3, 0.38, "QUIT  (Q)")

    draw_update_log_panel(update_scroll)

    if present:
        dudraw.show(25)


def draw_settings_screen(settings):
    draw_title_background(settings)

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 12.55, "SETTINGS")

    dudraw.set_pen_color_rgb(215, 226, 231)
    dudraw.text(12, 11.15, "Use keys or click the buttons.")

    dudraw.text(12, 9.9, f"Volume: {settings['volume']}/10")
    draw_menu_button(9.5, 8.9, 1.1, 0.42, "-  LEFT")
    draw_menu_button(14.5, 8.9, 1.1, 0.42, "+  RIGHT")

    dudraw.text(12, 7.65, f"Graphics: {settings['graphics'].title()}")
    draw_menu_button(8.5, 6.65, 1.2, 0.42, "LOW", settings["graphics"] == "low")
    draw_menu_button(12.0, 6.65, 1.35, 0.42, "AMAZING", settings["graphics"] == "amazing")
    draw_menu_button(15.8, 6.65, 1.2, 0.42, "ULTRA", settings["graphics"] == "ultra")

    fullscreen_label = "FULLSCREEN ON  (F)" if settings["fullscreen"] else "FULLSCREEN OFF  (F)"
    draw_menu_button(12, 5.45, 2.65, 0.42, fullscreen_label, settings["fullscreen"])

    detail_full = settings.get("show_stats", True) and settings.get("show_health_bars", True)
    dudraw.set_pen_color_rgb(215, 226, 231)
    dudraw.text(12, 4.55, "HUD detail")
    draw_menu_button(9.8, 3.85, 1.55, 0.36, "FULL", detail_full)
    draw_menu_button(14.2, 3.85, 1.55, 0.36, "CLEAN", not detail_full)
    draw_menu_button(12, 2.75, 2.15, 0.4, "BACK  (B)")
    dudraw.show(25)


def get_menu_key():
    while dudraw.has_next_key_typed():
        return dudraw.next_key_typed().lower()

    return None


def run_start_screen(settings):
    update_scroll = 0
    update_page_size = 5
    max_update_page = ((len(UPDATE_LOG) - 1) // update_page_size) * update_page_size
    frame = 0

    while True:
        draw_start_screen(settings, update_scroll, frame)
        frame += 1
        key = get_menu_key()

        if key == "up":
            update_scroll = max(0, update_scroll - update_page_size)
        elif key == "down":
            update_scroll = min(max_update_page, update_scroll + update_page_size)
        if key == "s":
            return "start"
        if key == "d":
            return "dictionary"
        if key == "p":
            return "special"
        if key == "t":
            return "settings"
        if key == "c":
            return "controls"
        if key == "f":
            toggle_fullscreen(settings)
        if key == "q":
            return "quit"

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()

            if point_in_rect(x, y, 6.2, 10.35, 2.3, 0.38):
                return "start"
            if point_in_rect(x, y, 6.2, 9.3, 2.3, 0.38):
                return "special"
            if point_in_rect(x, y, 6.2, 8.25, 2.3, 0.38):
                return "dictionary"
            if point_in_rect(x, y, 6.2, 7.2, 2.3, 0.38):
                return "settings"
            if point_in_rect(x, y, 6.2, 6.15, 2.3, 0.38):
                return "controls"
            if point_in_rect(x, y, 6.2, 5.1, 2.3, 0.38):
                return "quit"
            if point_in_rect(x, y, 13.3, 4.2, 0.72, 0.28):
                update_scroll = max(0, update_scroll - update_page_size)
            if point_in_rect(x, y, 19.8, 4.2, 0.72, 0.28):
                update_scroll = min(max_update_page, update_scroll + update_page_size)
            selected_update = update_log_entry_at(x, y, update_scroll)
            if selected_update is not None:
                run_update_detail_screen(settings, selected_update)


def map_keys_for_collection(collection):
    if collection == "polished":
        return POLISHED_MAP_KEYS
    if collection == "3d":
        return THREE_D_MAP_KEYS
    return CLASSIC_MAP_KEYS


def draw_map_select_screen(settings, collection):
    draw_title_background(settings)
    map_keys = map_keys_for_collection(collection)
    selected_key = CURRENT_MAP_KEY if CURRENT_MAP_KEY in map_keys else map_keys[0]
    selected_map = MAPS[selected_key]

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 13.55, "CHOOSE A MAP")

    draw_menu_button(6.0, 12.65, 1.8, 0.36, "CLASSIC", collection == "classic")
    draw_menu_button(12.0, 12.65, 1.8, 0.36, "POLISHED", collection == "polished")
    draw_menu_button(18.0, 12.65, 1.8, 0.36, "3D", collection == "3d")

    for index, map_key in enumerate(map_keys):
        map_info = MAPS[map_key]
        column = index % 2
        row = index // 2
        x = 6.8 + column * 10.4
        y = 11.5 - row * 1.15
        label = f"{index + 1}. {map_info['name']}"

        draw_menu_button(x, y, 3.2, 0.38, label, map_key == CURRENT_MAP_KEY)

    dudraw.set_pen_color_rgb(184, 198, 207)
    dudraw.text(12, 4.25, selected_map["special"])
    if collection == "classic":
        dudraw.text(12, 3.75, "Classic collection   Press 0 for map 10.")
    elif collection == "polished":
        dudraw.text(12, 3.75, "Polished collection   All ten maps remastered.")
    else:
        dudraw.text(12, 3.75, "3D collection   Ten raised-terrain battlefields.")
    draw_menu_button(12, 3.15, 2.1, 0.42, "BACK  (B)")
    dudraw.show(25)


def map_at_point(x, y, collection):
    for index, map_key in enumerate(map_keys_for_collection(collection)):
        column = index % 2
        row = index // 2
        entry_x = 6.8 + column * 10.4
        entry_y = 11.5 - row * 1.15

        if point_in_rect(x, y, entry_x, entry_y, 3.2, 0.38):
            return map_key

    return None


def run_map_select_screen(settings):
    if CURRENT_MAP.get("three_d", False):
        collection = "3d"
    elif CURRENT_MAP.get("polished", False):
        collection = "polished"
    else:
        collection = "classic"
    collections = ("classic", "polished", "3d")

    while True:
        draw_map_select_screen(settings, collection)
        key = get_menu_key()

        if key in ("b", "m"):
            return None
        if key == "f":
            toggle_fullscreen(settings)
        if key == "left":
            collection = collections[max(0, collections.index(collection) - 1)]
        elif key == "right":
            collection = collections[min(len(collections) - 1, collections.index(collection) + 1)]
        if key is not None and key in "123456789":
            index = int(key) - 1
            map_keys = map_keys_for_collection(collection)
            if 0 <= index < len(map_keys):
                return map_keys[index]
        if key == "0":
            return map_keys_for_collection(collection)[9]

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()

            if point_in_rect(x, y, 12, 3.15, 2.1, 0.42):
                return None
            if point_in_rect(x, y, 6.0, 12.65, 1.8, 0.36):
                collection = "classic"
                continue
            if point_in_rect(x, y, 12.0, 12.65, 1.8, 0.36):
                collection = "polished"
                continue
            if point_in_rect(x, y, 18.0, 12.65, 1.8, 0.36):
                collection = "3d"
                continue

            map_key = map_at_point(x, y, collection)
            if map_key is not None:
                return map_key


def draw_difficulty_screen(settings):
    draw_title_background(settings)

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 13.25, "CHOOSE DIFFICULTY")
    dudraw.set_pen_color_rgb(215, 226, 231)
    dudraw.text(12, 12.45, "Higher difficulty means tougher waves and fewer resources.")

    y_positions = {"easy": 10.8, "medium": 9.55, "hard": 8.3, "insane": 7.05}
    for index, (difficulty_key, y) in enumerate(y_positions.items(), 1):
        stats = DIFFICULTIES[difficulty_key]
        label = f"{index}  {stats['name']}   DMG {int(stats['damage'] * 100)}%   HP {int(stats['health'] * 100)}%   SPD {int(stats['speed'] * 100)}%"
        draw_menu_button(12, y, 5.4, 0.42, label, settings["difficulty"] == difficulty_key)
        set_color(stats["color"])
        dudraw.filled_circle(7.08, y, 0.12)

    selected = DIFFICULTIES[settings["difficulty"]]
    preview_lives = starting_lives(CURRENT_MAP, settings["difficulty"])
    wave_money = earned_money(CURRENT_MAP["wave_bonus"], settings["difficulty"])
    set_color(selected["color"])
    dudraw.text(12, 5.75, selected["description"])
    dudraw.set_pen_color_rgb(184, 198, 207)
    dudraw.text(12, 5.18, f"Income {int(selected['money'] * 100)}%   Lives {preview_lives}   Wave reward ${wave_money}   Spawn pace {int(100 / selected['spawn'])}%")
    draw_menu_button(9.1, 3.95, 2.1, 0.42, "PLAY  (P)", True)
    draw_menu_button(14.9, 3.95, 2.1, 0.42, "BACK  (B)")
    dudraw.show(25)


def run_difficulty_screen(settings):
    choices = {"1": "easy", "2": "medium", "3": "hard", "4": "insane"}
    y_positions = {"easy": 10.8, "medium": 9.55, "hard": 8.3, "insane": 7.05}

    while True:
        draw_difficulty_screen(settings)
        key = get_menu_key()

        if key in choices:
            settings["difficulty"] = choices[key]
        elif key == "p":
            return True
        elif key in ("b", "m"):
            return False
        elif key == "f":
            toggle_fullscreen(settings)

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()
            for difficulty_key, entry_y in y_positions.items():
                if point_in_rect(x, y, 12, entry_y, 5.4, 0.42):
                    settings["difficulty"] = difficulty_key
            if point_in_rect(x, y, 9.1, 3.95, 2.1, 0.42):
                return True
            if point_in_rect(x, y, 14.9, 3.95, 2.1, 0.42):
                return False


def draw_future_update_popup(settings):
    draw_start_screen(settings, present=False)
    dudraw.set_pen_color_rgb(12, 16, 22)
    dudraw.filled_rectangle(12, 8.2, 6.3, 1.55)
    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.rectangle(12, 8.2, 6.3, 1.55)
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(12, 8.7, "Map selection supports Amazing graphics only.")
    dudraw.text(12, 8.15, "Low and Ultra map packs are coming in a future update.")
    dudraw.text(12, 7.55, "Click or press any key to return.")
    dudraw.show(25)


def run_future_update_popup(settings):
    while True:
        draw_future_update_popup(settings)

        if get_menu_key() is not None or dudraw.mouse_clicked():
            return


def run_settings_screen(settings):
    while True:
        draw_settings_screen(settings)
        key = get_menu_key()

        if key in ("b", "s"):
            return
        if key in ("left", "-"):
            settings["volume"] = max(0, settings["volume"] - 1)
        elif key in ("right", "+"):
            settings["volume"] = min(10, settings["volume"] + 1)
        elif key == "l":
            settings["graphics"] = "low"
        elif key in ("a", "g"):
            settings["graphics"] = "amazing"
        elif key == "u":
            settings["graphics"] = "ultra"
        elif key == "f":
            toggle_fullscreen(settings)

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()

            if point_in_rect(x, y, 9.5, 8.9, 1.1, 0.42):
                settings["volume"] = max(0, settings["volume"] - 1)
            elif point_in_rect(x, y, 14.5, 8.9, 1.1, 0.42):
                settings["volume"] = min(10, settings["volume"] + 1)
            elif point_in_rect(x, y, 8.5, 6.65, 1.2, 0.42):
                settings["graphics"] = "low"
            elif point_in_rect(x, y, 12.0, 6.65, 1.35, 0.42):
                settings["graphics"] = "amazing"
            elif point_in_rect(x, y, 15.8, 6.65, 1.2, 0.42):
                settings["graphics"] = "ultra"
            elif point_in_rect(x, y, 12, 5.45, 2.65, 0.42):
                toggle_fullscreen(settings)
            elif point_in_rect(x, y, 9.8, 3.85, 1.55, 0.36):
                settings.update({
                    "show_path_arrows": True,
                    "show_health_bars": True,
                    "show_threat_marks": True,
                    "show_range": True,
                    "show_target_links": True,
                    "show_floating_text": True,
                    "show_stats": True,
                })
            elif point_in_rect(x, y, 14.2, 3.85, 1.55, 0.36):
                settings.update({
                    "show_path_arrows": False,
                    "show_health_bars": False,
                    "show_threat_marks": False,
                    "show_range": False,
                    "show_target_links": False,
                    "show_floating_text": False,
                    "show_stats": False,
                })
            elif point_in_rect(x, y, 12, 2.75, 2.15, 0.4):
                return


def control_key_label(key):
    labels = {
        " ": "SPACE",
        "return": "ENTER",
        "escape": "ESC",
        "tab": "TAB",
        ",": "COMMA",
        ".": "PERIOD",
    }
    return labels.get(key, key.upper())


def draw_controls_screen(settings, page, rebinding=None, message=None):
    draw_title_background(settings)
    page_size = 15
    start = page * page_size
    actions = CONTROL_ACTIONS[start:start + page_size]

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 13.45, "CONTROLS")
    dudraw.set_pen_color_rgb(215, 226, 231)
    dudraw.text(12, 12.82, "Click a shortcut, then press a new key.")

    for index, action in enumerate(actions):
        column = index % 2
        row = index // 2
        x = 6.1 + column * 11.8
        y = 11.85 - row * 1.05
        label = f"{CONTROL_LABELS[action]}   [{control_key_label(settings['controls'][action])}]"
        draw_menu_button(x, y, 5.15, 0.38, label, rebinding == action)

    if rebinding is not None:
        set_color((246, 231, 148))
        dudraw.text(12, 2.85, f"Press a new key for {CONTROL_LABELS[rebinding]}. Click Back to cancel.")
    elif message is not None:
        dudraw.set_pen_color_rgb(191, 205, 214)
        dudraw.text(12, 2.85, message)

    draw_menu_button(5.2, 1.75, 1.65, 0.38, "PAGE 1", page == 0)
    draw_menu_button(9.0, 1.75, 1.65, 0.38, "PAGE 2", page == 1)
    draw_menu_button(14.3, 1.75, 2.05, 0.38, "RESET DEFAULTS")
    draw_menu_button(19.2, 1.75, 1.65, 0.38, "BACK  (B)")
    dudraw.show(25)


def control_at_point(x, y, page):
    actions = CONTROL_ACTIONS[page * 15:page * 15 + 15]
    for index, action in enumerate(actions):
        column = index % 2
        row = index // 2
        entry_x = 6.1 + column * 11.8
        entry_y = 11.85 - row * 1.05
        if point_in_rect(x, y, entry_x, entry_y, 5.15, 0.38):
            return action
    return None


def run_controls_screen(settings):
    page = 0
    rebinding = None
    message = "Gameplay shortcuts can be remapped here."

    while True:
        draw_controls_screen(settings, page, rebinding, message)
        key = get_menu_key()

        if rebinding is not None and key is not None:
            used_by = next((action for action, bound_key in settings["controls"].items() if bound_key == key and action != rebinding), None)
            if used_by is not None:
                message = f"{control_key_label(key)} is already used for {CONTROL_LABELS[used_by]}."
            else:
                settings["controls"][rebinding] = key
                message = f"{CONTROL_LABELS[rebinding]} is now {control_key_label(key)}."
                rebinding = None
            continue

        if key == "b":
            return
        if key in ("left", "1"):
            page = 0
        elif key in ("right", "2"):
            page = 1
        elif key == "r":
            settings["controls"] = DEFAULT_CONTROLS.copy()
            message = "Gameplay shortcuts restored to defaults."

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()
            action = control_at_point(x, y, page)
            if action is not None:
                rebinding = action
                message = None
            elif point_in_rect(x, y, 5.2, 1.75, 1.65, 0.38):
                page = 0
            elif point_in_rect(x, y, 9.0, 1.75, 1.65, 0.38):
                page = 1
            elif point_in_rect(x, y, 14.3, 1.75, 2.05, 0.38):
                settings["controls"] = DEFAULT_CONTROLS.copy()
                message = "Gameplay shortcuts restored to defaults."
            elif point_in_rect(x, y, 19.2, 1.75, 1.65, 0.38):
                return


def draw_special_stats(chosen, settings):
    description = chosen["description"]
    if len(description) > 58:
        description = description[:55] + "..."

    dudraw.set_pen_color_rgb(13, 18, 25)
    dudraw.filled_rectangle(12, 3.75, 6.2, 1.0)
    dudraw.set_pen_color_rgb(81, 101, 121)
    dudraw.rectangle(12, 3.75, 6.2, 1.0)

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 4.45, chosen["name"])

    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(12, 3.95, description)
    dudraw.text(
        12,
        3.35,
        f"Damage {chosen['damage']}   Range {chosen['range']}   Cooldown {chosen['cooldown']}   Splash {chosen['splash']}   Hold {chosen.get('block_duration', 0)}",
    )
    dudraw.text(
        12,
        2.85,
        f"Slow {chosen['slow']}   Poison {chosen['poison']}   Place +${earned_money(chosen['money_bonus'], settings['difficulty'])}   Kill +${earned_money(chosen.get('kill_bonus', 0), settings['difficulty'])}   Lives +{chosen['lives_bonus']}",
    )


def draw_special_showcase_box(chosen_key, frame):
    chosen = SPECIAL_TOWERS[chosen_key]

    dudraw.set_pen_color_rgb(10, 15, 23)
    dudraw.filled_rectangle(12, 8.2, 4.1, 3.15)
    dudraw.set_pen_color_rgb(83, 105, 127)
    dudraw.rectangle(12, 8.2, 4.1, 3.15)
    set_color(brighten(chosen["color"], 48))
    dudraw.filled_rectangle(12, 11.3, 4.0, 0.03)

    set_color(brighten(chosen["color"], 35))
    dudraw.circle(12, 8.4, chosen["range"] * 0.45 if chosen["range"] > 0 else 1.1)
    dudraw.circle(12, 8.4, 1.85 + 0.12 * math.sin(frame * 0.06))

    for i in range(14):
        angle = frame * 0.025 + i * 2 * math.pi / 14
        radius = 2.3 + (i % 3) * 0.18
        set_color(brighten(chosen["color"], 65))
        dudraw.filled_circle(12 + math.cos(angle) * radius, 8.4 + math.sin(angle) * radius * 0.65, 0.035)

    draw_release_tower(12, 8.1, chosen_key, frame, 1.55)


def draw_special_choice(x, y, special_type, selected):
    stats = SPECIAL_TOWERS[special_type]

    if selected:
        dudraw.set_pen_color_rgb(246, 231, 148)
        dudraw.filled_rectangle(x, y, 2.72, 0.42)

    dudraw.set_pen_color_rgb(10, 14, 20)
    dudraw.filled_rectangle(x + 0.04, y - 0.04, 2.55, 0.34)
    dudraw.set_pen_color_rgb(24, 32, 42)
    dudraw.filled_rectangle(x, y, 2.55, 0.34)
    dudraw.set_pen_color_rgb(78, 96, 113)
    dudraw.rectangle(x, y, 2.55, 0.34)
    set_color(stats["color"])
    dudraw.filled_circle(x - 1.98, y, 0.16)
    set_color(brighten(stats["color"], 55))
    dudraw.filled_circle(x - 2.03, y + 0.05, 0.055)
    set_color(stats["color"])
    dudraw.filled_rectangle(x, y - 0.29, 2.42, 0.018)
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(x + 0.15, y - 0.02, stats["name"])


def draw_special_screen(settings, frame=0):
    draw_title_background(settings)

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 13.45, "CHOOSE ONE SPECIAL TOWER")

    dudraw.set_pen_color_rgb(215, 226, 231)
    special_key = control_key_label(settings["controls"]["special"])
    dudraw.text(12, 12.55, f"Special towers cost $0, can be placed once, and use {special_key} in game.")

    for index, special_type in enumerate(SPECIAL_TOWERS):
        column = index % 2
        row = index // 2
        x = 3.9 if column == 0 else 20.1
        y = 11.35 - row * 1.0
        selected = settings["special_tower"] == special_type
        draw_special_choice(x, y, special_type, selected)

    chosen = SPECIAL_TOWERS[settings["special_tower"]]
    draw_special_showcase_box(settings["special_tower"], frame)
    draw_special_stats(chosen, settings)
    draw_menu_button(12, 1.75, 2.1, 0.42, "BACK  (B)")
    dudraw.show(25)


def special_item_at(x, y):
    for index, special_type in enumerate(SPECIAL_TOWERS):
        column = index % 2
        row = index // 2
        entry_x = 3.9 if column == 0 else 20.1
        entry_y = 11.35 - row * 1.0

        if point_in_rect(x, y, entry_x, entry_y, 2.55, 0.34):
            return special_type

    return None


def run_special_screen(settings):
    frame = 0

    while True:
        draw_special_screen(settings, frame)
        frame += 1
        key = get_menu_key()

        if key in ("b", "s"):
            return
        if key == "f":
            toggle_fullscreen(settings)

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()

            if point_in_rect(x, y, 12, 1.75, 2.1, 0.42):
                return

            special_type = special_item_at(x, y)
            if special_type is not None:
                settings["special_tower"] = special_type


def draw_dictionary_entry(x, y, label, color):
    dudraw.set_pen_color_rgb(10, 14, 20)
    dudraw.filled_rectangle(x + 0.035, y - 0.04, 2.25, 0.35)
    dudraw.set_pen_color_rgb(26, 34, 45)
    dudraw.filled_rectangle(x, y, 2.25, 0.35)
    dudraw.set_pen_color_rgb(78, 96, 113)
    dudraw.rectangle(x, y, 2.25, 0.35)
    set_color(color)
    dudraw.filled_circle(x - 1.65, y, 0.16)
    set_color(brighten(color, 45))
    dudraw.filled_circle(x - 1.7, y + 0.05, 0.045)
    set_color(color)
    dudraw.filled_rectangle(x, y - 0.3, 2.1, 0.018)
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(x + 0.2, y - 0.02, label)


def draw_mini_map_preview(map_key, center_x, center_y, scale):
    map_info = MAPS[map_key]
    theme = map_info["theme"]
    path_squares = {(int(x), int(y)) for x, y in map_info["path"]}
    islands = set(map_info.get("islands", set()))
    left = center_x - GRID_WIDTH * scale / 2
    bottom = center_y - GRID_HEIGHT * scale / 2

    dudraw.set_pen_color_rgb(13, 18, 25)
    dudraw.filled_rectangle(center_x, center_y, GRID_WIDTH * scale / 2 + 0.15, GRID_HEIGHT * scale / 2 + 0.15)
    dudraw.set_pen_color_rgb(85, 105, 126)
    dudraw.rectangle(center_x, center_y, GRID_WIDTH * scale / 2 + 0.15, GRID_HEIGHT * scale / 2 + 0.15)

    if map_info.get("three_d", False):
        set_color(darken(theme["grass_b"], 35))
        dudraw.filled_rectangle(center_x + 0.1, center_y - 0.14, GRID_WIDTH * scale / 2, GRID_HEIGHT * scale / 2)
        set_color(theme["grass_b"])
        dudraw.filled_rectangle(center_x, center_y, GRID_WIDTH * scale / 2, GRID_HEIGHT * scale / 2)
        set_color(brighten(theme["grass_a"], 8))
        dudraw.filled_ellipse(center_x - 3.0 * scale, center_y + 4.3 * scale, 5.5 * scale, 1.8 * scale)
        if map_info["place_rule"] == "islands":
            for x, y in islands:
                tile_x = left + (x + 0.5) * scale
                tile_y = bottom + (y + 0.5) * scale
                set_color(darken(theme["edge"], 28))
                dudraw.filled_ellipse(tile_x + 0.08 * scale, tile_y - 0.2 * scale, scale * 0.44, scale * 0.2)
                set_color(brighten(theme["grass_a"], 14))
                dudraw.filled_ellipse(tile_x, tile_y, scale * 0.36, scale * 0.16)
        set_color(darken(theme["edge"], 30))
        for x, y in map_info["path"]:
            dudraw.filled_circle(left + x * scale + scale * 0.15, bottom + y * scale - scale * 0.2, scale * 0.62)
        set_color(brighten(theme["edge"], 5))
        for x, y in map_info["path"]:
            dudraw.filled_circle(left + x * scale, bottom + y * scale, scale * 0.58)
        set_color(brighten(theme["path"], 10))
        for x, y in map_info["path"]:
            dudraw.filled_circle(left + x * scale, bottom + y * scale + scale * 0.06, scale * 0.45)
        start_x, start_y = map_info["path"][0]
        end_x, end_y = map_info["path"][-1]
        dudraw.set_pen_color_rgb(89, 211, 129)
        dudraw.filled_circle(left + start_x * scale, bottom + start_y * scale, scale * 0.22)
        dudraw.set_pen_color_rgb(227, 91, 82)
        dudraw.filled_circle(left + end_x * scale, bottom + end_y * scale, scale * 0.22)
        return

    if map_info.get("polished", False):
        set_color(theme["grass_b"])
        dudraw.filled_rectangle(center_x, center_y, GRID_WIDTH * scale / 2, GRID_HEIGHT * scale / 2)
        set_color(theme["grass_a"])
        dudraw.filled_ellipse(center_x - 2.8 * scale, center_y + 4.7 * scale, 6.0 * scale, 2.0 * scale)
        dudraw.filled_ellipse(center_x + 4.8 * scale, center_y - 4.5 * scale, 6.8 * scale, 1.8 * scale)
        style = map_info.get("polished_style")
        if style == "desert":
            dudraw.set_pen_color_rgb(48, 132, 145)
            dudraw.filled_ellipse(center_x - 2.9 * scale, center_y + 1.1 * scale, 2.15 * scale, 1.0 * scale)
            dudraw.set_pen_color_rgb(176, 128, 70)
            for column_x in (center_x + 2.8 * scale, center_x + 3.7 * scale, center_x + 4.6 * scale):
                dudraw.filled_rectangle(column_x, center_y + 3.6 * scale, 0.12 * scale, 1.15 * scale)
            dudraw.set_pen_color_rgb(218, 171, 93)
            dudraw.line(center_x + 2.35 * scale, center_y + 4.85 * scale, center_x + 5.05 * scale, center_y + 4.85 * scale)
        elif style == "mountain":
            dudraw.set_pen_color_rgb(62, 73, 78)
            for peak_x in (center_x - 4.0 * scale, center_x, center_x + 4.2 * scale):
                dudraw.filled_triangle(peak_x - 2.0 * scale, center_y + 5.8 * scale, peak_x + 2.0 * scale, center_y + 5.8 * scale, peak_x, center_y + 2.2 * scale)
        elif style == "ocean":
            dudraw.set_pen_color_rgb(225, 205, 139)
            for ix, iy in ((-3, 3), (1, -1), (4, 3)):
                dudraw.filled_ellipse(center_x + ix * scale, center_y + iy * scale, 1.1 * scale, 0.45 * scale)
        elif style == "temple":
            dudraw.set_pen_color_rgb(238, 164, 193)
            dudraw.filled_circle(center_x + 4.4 * scale, center_y + 3.3 * scale, 1.15 * scale)
            dudraw.set_pen_color_rgb(110, 52, 56)
            dudraw.filled_rectangle(center_x - 3.6 * scale, center_y + 4.0 * scale, 1.4 * scale, 0.12 * scale)
        elif style == "racetrack":
            dudraw.set_pen_color_rgb(44, 83, 58)
            dudraw.filled_ellipse(center_x, center_y, 4.2 * scale, 2.2 * scale)
            dudraw.set_pen_color_rgb(229, 60, 58)
            dudraw.line(center_x - 3 * scale, center_y - 4.8 * scale, center_x + 3 * scale, center_y - 4.8 * scale)
        elif style == "war":
            dudraw.set_pen_color_rgb(48, 52, 45)
            dudraw.filled_ellipse(center_x - 3 * scale, center_y + 2 * scale, 1.0 * scale, 0.5 * scale)
            dudraw.filled_ellipse(center_x + 4 * scale, center_y - scale, 1.2 * scale, 0.55 * scale)
        elif style == "miami":
            dudraw.set_pen_color_rgb(38, 156, 185)
            dudraw.filled_rectangle(center_x - 6.4 * scale, center_y, 1.2 * scale, 7.0 * scale)
            dudraw.set_pen_color_rgb(230, 75, 134)
            dudraw.line(center_x + 3 * scale, center_y + 5 * scale, center_x + 6 * scale, center_y + 5 * scale)
        elif style == "retro":
            dudraw.set_pen_color_rgb(244, 69, 182)
            dudraw.filled_circle(center_x, center_y + 3 * scale, 1.5 * scale)
            dudraw.set_pen_color_rgb(17, 16, 39)
            dudraw.filled_rectangle(center_x, center_y - 3 * scale, 7 * scale, 1.3 * scale)
        elif style == "crystal":
            dudraw.set_pen_color_rgb(81, 206, 220)
            for cx, cy in ((-3, -2), (2, 3), (5, -1)):
                dudraw.filled_triangle(center_x + (cx - 0.5) * scale, center_y + cy * scale, center_x + (cx + 0.5) * scale, center_y + cy * scale, center_x + cx * scale, center_y + (cy + 1.8) * scale)
        else:
            dudraw.set_pen_color_rgb(49, 121, 130)
            dudraw.filled_ellipse(center_x - 0.2 * scale, center_y, 1.7 * scale, 0.9 * scale)
        set_color(theme["edge"])
        for x, y in map_info["path"]:
            dudraw.filled_circle(left + x * scale, bottom + y * scale, scale * 0.62)
        set_color(theme["path"])
        for x, y in map_info["path"]:
            dudraw.filled_circle(left + x * scale, bottom + y * scale, scale * 0.47)
        start_x, start_y = map_info["path"][0]
        end_x, end_y = map_info["path"][-1]
        dudraw.set_pen_color_rgb(89, 211, 129)
        dudraw.filled_circle(left + start_x * scale, bottom + start_y * scale, scale * 0.22)
        dudraw.set_pen_color_rgb(227, 91, 82)
        dudraw.filled_circle(left + end_x * scale, bottom + end_y * scale, scale * 0.22)
        return

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            tile_x = left + (x + 0.5) * scale
            tile_y = bottom + (y + 0.5) * scale

            if (x, y) in path_squares:
                set_color(theme["path"])
            elif (x + y) % 2 == 0:
                set_color(theme["grass_a"])
            else:
                set_color(theme["grass_b"])

            dudraw.filled_rectangle(tile_x, tile_y, scale / 2, scale / 2)

            if map_info["place_rule"] == "islands" and (x, y) in islands:
                dudraw.set_pen_color_rgb(88, 178, 105)
                dudraw.filled_circle(tile_x, tile_y, scale * 0.38)

    set_color(theme["edge"])
    for index, (x, y) in enumerate(map_info["path"]):
        if index + 1 < len(map_info["path"]):
            next_x, next_y = map_info["path"][index + 1]
            start_x = left + x * scale
            start_y = bottom + y * scale
            end_x = left + next_x * scale
            end_y = bottom + next_y * scale
            dudraw.line(start_x, start_y, end_x, end_y)

    start_x, start_y = map_info["path"][0]
    end_x, end_y = map_info["path"][-1]
    dudraw.set_pen_color_rgb(89, 211, 129)
    dudraw.filled_circle(left + start_x * scale, bottom + start_y * scale, scale * 0.22)
    dudraw.set_pen_color_rgb(227, 91, 82)
    dudraw.filled_circle(left + end_x * scale, bottom + end_y * scale, scale * 0.22)


def get_map_rule_lines(map_key, difficulty="easy"):
    map_info = MAPS[map_key]
    lines = [map_info["special"]]

    if map_info["place_rule"] == "islands":
        lines.append("Placement: towers only go on island tiles.")
    else:
        lines.append("Placement: towers can be built on open non-path tiles.")

    lines.append(f"Starting money: ${START_MONEY + earned_money(map_info['money_bonus'], difficulty)}")
    lines.append(f"Starting lives: {starting_lives(map_info, difficulty)}")
    lines.append(f"Between-wave reward: ${earned_money(map_info['wave_bonus'], difficulty)}")

    return lines


def draw_dictionary_home(settings):
    draw_title_background(settings)

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 12.95, "DICTIONARY")

    dudraw.set_pen_color_rgb(215, 226, 231)
    dudraw.text(12, 11.75, "Choose a section to explore.")

    draw_menu_button(8.0, 9.35, 3.0, 1.0, "MAPS")
    draw_menu_button(16.0, 9.35, 3.0, 1.0, "CHARACTERS")

    dudraw.set_pen_color_rgb(184, 198, 207)
    dudraw.text(8.0, 7.8, "Layouts, themes, and map rules")
    dudraw.text(16.0, 7.8, "Towers, specials, enemies, and stats")

    draw_menu_button(12, 5.75, 2.1, 0.42, "BACK  (B)")
    dudraw.show(25)


def draw_maps_dictionary_screen(settings, selected_map, collection):
    draw_title_background(settings)
    map_keys = map_keys_for_collection(collection)
    if selected_map not in map_keys:
        selected_map = map_keys[0]

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 13.55, "MAP DICTIONARY")

    draw_menu_button(1.55, 12.65, 1.05, 0.29, "CLASSIC", collection == "classic")
    draw_menu_button(4.2, 12.65, 1.05, 0.29, "POLISHED", collection == "polished")
    draw_menu_button(6.85, 12.65, 1.05, 0.29, "3D", collection == "3d")

    for index, map_key in enumerate(map_keys):
        map_info = MAPS[map_key]
        y = 11.75 - index * 0.76
        label = f"{index + 1}. {map_info['name']}"
        draw_menu_button(4.2, y, 3.0, 0.31, label, map_key == selected_map)

    draw_mini_map_preview(selected_map, 15.0, 9.7, 0.31)

    selected = MAPS[selected_map]
    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(15.0, 6.7, selected["name"])

    dudraw.set_pen_color(dudraw.WHITE)
    for index, line in enumerate(get_map_rule_lines(selected_map, settings["difficulty"])):
        dudraw.text(15.0, 5.95 - index * 0.53, line)

    draw_menu_button(12, 2.35, 2.1, 0.42, "BACK  (B)")
    dudraw.show(25)


def dictionary_map_at(x, y, collection):
    for index, map_key in enumerate(map_keys_for_collection(collection)):
        entry_y = 11.75 - index * 0.76
        if point_in_rect(x, y, 4.2, entry_y, 3.0, 0.31):
            return map_key

    return None


def run_maps_dictionary_screen(settings):
    selected_map = CURRENT_MAP_KEY
    if CURRENT_MAP.get("three_d", False):
        collection = "3d"
    elif CURRENT_MAP.get("polished", False):
        collection = "polished"
    else:
        collection = "classic"
    collections = ("classic", "polished", "3d")

    while True:
        draw_maps_dictionary_screen(settings, selected_map, collection)
        key = get_menu_key()

        if key in ("b", "d"):
            return
        if key == "f":
            toggle_fullscreen(settings)
        if key == "left":
            collection = collections[max(0, collections.index(collection) - 1)]
            selected_map = map_keys_for_collection(collection)[0]
        elif key == "right":
            collection = collections[min(len(collections) - 1, collections.index(collection) + 1)]
            selected_map = map_keys_for_collection(collection)[0]
        if key is not None and key in "123456789":
            index = int(key) - 1
            map_keys = map_keys_for_collection(collection)
            if 0 <= index < len(map_keys):
                selected_map = map_keys[index]
        elif key == "0":
            selected_map = map_keys_for_collection(collection)[9]

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()

            if point_in_rect(x, y, 12, 2.35, 2.1, 0.42):
                return
            if point_in_rect(x, y, 1.55, 12.65, 1.05, 0.29):
                collection = "classic"
                selected_map = CLASSIC_MAP_KEYS[0]
                continue
            if point_in_rect(x, y, 4.2, 12.65, 1.05, 0.29):
                collection = "polished"
                selected_map = POLISHED_MAP_KEYS[0]
                continue
            if point_in_rect(x, y, 6.85, 12.65, 1.05, 0.29):
                collection = "3d"
                selected_map = THREE_D_MAP_KEYS[0]
                continue

            map_key = dictionary_map_at(x, y, collection)
            if map_key is not None:
                selected_map = map_key


def draw_dictionary_screen(settings):
    draw_title_background(settings)

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(12, 13.6, "CHARACTER DICTIONARY")

    dudraw.set_pen_color_rgb(215, 226, 231)
    dudraw.text(5.0, 12.45, "Towers")
    dudraw.text(12.0, 12.45, "Special")
    dudraw.text(19.0, 12.45, "Enemies")

    for index, tower_type in enumerate(TOWER_TYPES):
        stats = TOWER_TYPES[tower_type]
        y = 11.55 - index * 0.72
        label = f"{stats['name']}  ${stats['cost']}"
        draw_dictionary_entry(5.0, y, label, stats["color"])

    for index, special_type in enumerate(SPECIAL_TOWERS):
        stats = SPECIAL_TOWERS[special_type]
        y = 11.55 - index * 0.72
        label = stats["name"]
        draw_dictionary_entry(12.0, y, label, stats["color"])

    for index, enemy_type in enumerate(ENEMY_TYPES):
        stats = ENEMY_TYPES[enemy_type]
        y = 11.55 - index * 0.72
        label = stats["name"]
        draw_dictionary_entry(19.0, y, label, stats["color"])

    dudraw.set_pen_color_rgb(184, 198, 207)
    dudraw.text(12, 4.05, "Click an item to inspect it.")
    draw_menu_button(12, 3.1, 2.1, 0.42, "BACK  (B)")
    dudraw.show(25)


def dictionary_item_at(x, y):
    for index, tower_type in enumerate(TOWER_TYPES):
        entry_y = 11.55 - index * 0.72
        if point_in_rect(x, y, 5.0, entry_y, 2.25, 0.35):
            return "tower", tower_type

    for index, special_type in enumerate(SPECIAL_TOWERS):
        entry_y = 11.55 - index * 0.72
        if point_in_rect(x, y, 12.0, entry_y, 2.25, 0.35):
            return "special", special_type

    for index, enemy_type in enumerate(ENEMY_TYPES):
        entry_y = 11.55 - index * 0.72
        if point_in_rect(x, y, 19.0, entry_y, 2.25, 0.35):
            return "enemy", enemy_type

    return None, None


def draw_character_preview(item_type, item_key, center_x, center_y, frame):
    dudraw.set_pen_color_rgb(10, 15, 23)
    dudraw.filled_rectangle(center_x, center_y, 3.2, 2.55)
    dudraw.set_pen_color_rgb(83, 105, 127)
    dudraw.rectangle(center_x, center_y, 3.2, 2.55)
    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.filled_rectangle(center_x, center_y + 2.47, 3.05, 0.025)
    dudraw.set_pen_color_rgb(34, 45, 58)
    dudraw.filled_ellipse(center_x, center_y - 1.38, 1.95, 0.34)
    dudraw.set_pen_color_rgb(188, 174, 132)
    dudraw.filled_ellipse(center_x, center_y - 1.2, 1.45, 0.28)
    dudraw.set_pen_color_rgb(92, 75, 54)
    dudraw.rectangle(center_x, center_y - 1.2, 1.45, 0.28)
    dudraw.set_pen_color_rgb(217, 201, 153)
    dudraw.filled_ellipse(center_x, center_y - 1.15, 1.15, 0.08)

    if item_type in ("tower", "special"):
        stats = get_tower_stats(item_key)
        set_color(brighten(stats["color"], 45))
        dudraw.circle(center_x, center_y - 0.12, 1.45 + 0.08 * math.sin(frame * 0.07))

        draw_release_tower(center_x, center_y, item_key, frame, 1.25)
        return

    stats = ENEMY_TYPES[item_key]
    draw_enemy_character(center_x, center_y, item_key, stats["color"], stats["radius"] * ENEMY_SIZE_SCALE, frame, 2.1)


def draw_tower_detail(item_key, settings, frame=0):
    stats = get_tower_stats(item_key)
    draw_title_background(settings)

    item_type = "special" if item_key in SPECIAL_TOWERS else "tower"
    draw_character_preview(item_type, item_key, 6.0, 10.05, frame)

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(13.4, 12.4, stats["name"])

    dudraw.set_pen_color(dudraw.WHITE)
    if item_key in SPECIAL_TOWERS:
        dudraw.text(13.4, 11.3, stats["description"])
    else:
        dudraw.text(13.4, 11.3, TOWER_DESCRIPTIONS[item_key])
    dudraw.text(13.4, 9.95, f"Cost: ${stats['cost']}")
    dudraw.text(13.4, 9.3, f"Damage: {stats['damage']}")
    dudraw.text(13.4, 8.65, f"Range: {stats['range']}")
    dudraw.text(13.4, 8.0, f"Cooldown: {stats['cooldown']}")
    if stats.get("block_duration", 0) > 0:
        dudraw.text(13.4, 7.35, f"Stop time: {stats['block_duration']} ticks   Road placement only")
    else:
        dudraw.text(13.4, 7.35, f"Slow: {stats['slow']}   Splash: {stats['splash']}   Poison: {stats['poison']}")

    if item_key in SPECIAL_TOWERS:
        dudraw.text(13.4, 6.7, f"Place bonus: ${earned_money(stats['money_bonus'], settings['difficulty'])}   Kill bonus: ${earned_money(stats.get('kill_bonus', 0), settings['difficulty'])}   Lives: {stats['lives_bonus']}")

    draw_menu_button(12, 5.2, 2.2, 0.45, "BACK  (B)")
    dudraw.show(25)


def draw_enemy_detail(item_key, settings, frame=0):
    stats = ENEMY_TYPES[item_key]
    draw_title_background(settings)

    draw_character_preview("enemy", item_key, 6.0, 10.05, frame)

    dudraw.set_pen_color_rgb(246, 231, 148)
    dudraw.text(13.4, 12.4, stats["name"])

    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(13.4, 11.3, ENEMY_DESCRIPTIONS[item_key])
    dudraw.text(13.4, 9.95, f"Health multiplier: {stats['health']}")
    dudraw.text(13.4, 9.3, f"Speed multiplier: {stats['speed']}")
    dudraw.text(13.4, 8.65, f"Reward multiplier: {stats['reward']}")
    dudraw.text(13.4, 8.0, f"Size: {stats['radius'] * ENEMY_SIZE_SCALE:.2f}")

    draw_menu_button(12, 5.2, 2.2, 0.45, "BACK  (B)")
    dudraw.show(25)


def run_item_detail(item_type, item_key, settings):
    frame = 0

    while True:
        if item_type in ("tower", "special"):
            draw_tower_detail(item_key, settings, frame)
        else:
            draw_enemy_detail(item_key, settings, frame)

        key = get_menu_key()
        if key in ("b", "d"):
            return
        if key == "f":
            toggle_fullscreen(settings)

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()

            if point_in_rect(x, y, 12, 5.2, 2.2, 0.45):
                return

        frame += 1


def run_dictionary_screen(settings):
    while True:
        draw_dictionary_home(settings)
        key = get_menu_key()

        if key in ("b", "s"):
            return
        if key == "f":
            toggle_fullscreen(settings)
        if key == "m":
            run_maps_dictionary_screen(settings)
        elif key == "c":
            run_characters_dictionary_screen(settings)

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()

            if point_in_rect(x, y, 12, 5.75, 2.1, 0.42):
                return
            if point_in_rect(x, y, 8.0, 9.35, 3.0, 1.0):
                run_maps_dictionary_screen(settings)
            elif point_in_rect(x, y, 16.0, 9.35, 3.0, 1.0):
                run_characters_dictionary_screen(settings)


def run_characters_dictionary_screen(settings):
    while True:
        draw_dictionary_screen(settings)
        key = get_menu_key()

        if key in ("b", "d"):
            return
        if key == "f":
            toggle_fullscreen(settings)

        if dudraw.mouse_clicked():
            x = dudraw.mouse_x()
            y = dudraw.mouse_y()

            if point_in_rect(x, y, 12, 3.1, 2.1, 0.42):
                return

            item_type, item_key = dictionary_item_at(x, y)
            if item_type is not None:
                run_item_detail(item_type, item_key, settings)


def add_notice(notices, message, color=(229, 236, 240), timer=70):
    notices.append([message, timer, color])
    if len(notices) > 4:
        notices.pop(0)


def draw_notices(notices):
    y = 15.35
    for notice in notices[:]:
        message, timer, color = notice
        dudraw.set_pen_color_rgb(17, 23, 31)
        dudraw.filled_rectangle(12, y, min(4.8, 0.11 * len(message) + 0.42), 0.2)
        set_color(color)
        dudraw.filled_rectangle(12 - min(4.8, 0.11 * len(message) + 0.42) + 0.04, y, 0.025, 0.15)
        set_color(color)
        dudraw.text(12, y - 0.02, message)
        notice[1] = timer - 1
        if notice[1] <= 0:
            notices.remove(notice)
        y -= 0.48


def draw_match_stats(match_stats, towers, settings):
    if not settings.get("show_stats", True):
        return

    total_damage = int(round(match_stats["sold_damage"] + sum(tower.total_damage for tower in towers)))
    dudraw.set_pen_color_rgb(13, 18, 24)
    dudraw.filled_rectangle(20.7, 14.55, 2.8, 0.92)
    set_color(DIFFICULTIES[settings["difficulty"]]["color"])
    dudraw.rectangle(20.7, 14.55, 2.8, 0.92)
    dudraw.filled_rectangle(20.7, 15.42, 2.8, 0.025)
    dudraw.text(20.7, 15.13, f"Kills {match_stats['kills']}   Damage {total_damage}")
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(20.7, 14.57, f"Earned ${match_stats['earned']}   Spent ${match_stats['spent']}")
    dudraw.set_pen_color_rgb(191, 205, 214)
    dudraw.text(20.7, 14.02, f"Built {match_stats['built']}   Up {match_stats['upgrades']}   Leaks {match_stats['leaks']}   Clear {match_stats['waves']}")


def draw_ui(money, lives, wave, enemies_left, wave_total, selected_tower, special_placed, settings, game_over, paused, between_waves, speed_multiplier, frame):
    if selected_tower == "special":
        selected = SPECIAL_TOWERS[settings["special_tower"]]
    elif selected_tower is not None:
        selected = TOWER_TYPES[selected_tower]
    else:
        selected = None

    dudraw.set_pen_color_rgb(21, 27, 35)
    dudraw.filled_rectangle(GRID_WIDTH / 2, GRID_HEIGHT + 1, GRID_WIDTH / 2, 1)

    if lives <= 3 and not game_over:
        dudraw.set_pen_color_rgb(108, 33, 38)
        dudraw.rectangle(GRID_WIDTH / 2, GRID_HEIGHT / 2, GRID_WIDTH / 2 - 0.08, GRID_HEIGHT / 2 - 0.08)
        if frame % 30 < 15:
            dudraw.set_pen_color_rgb(201, 72, 73)
            dudraw.rectangle(GRID_WIDTH / 2, GRID_HEIGHT / 2, GRID_WIDTH / 2 - 0.22, GRID_HEIGHT / 2 - 0.22)

    dudraw.set_pen_color_rgb(58, 69, 83)
    dudraw.filled_rectangle(GRID_WIDTH / 2, GRID_HEIGHT + 0.04, GRID_WIDTH / 2, 0.04)
    dudraw.set_pen_color_rgb(34, 43, 54)
    for divider_x in (3.1, 5.25, 7.15, 10.15):
        dudraw.line(divider_x, GRID_HEIGHT + 1.08, divider_x, GRID_HEIGHT + 1.64)

    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(2.0, GRID_HEIGHT + 1.34, f"${money}")
    dudraw.text(4.2, GRID_HEIGHT + 1.34, f"Lives {lives}")
    dudraw.text(6.25, GRID_HEIGHT + 1.34, f"Wave {wave}")
    dudraw.text(9.3, GRID_HEIGHT + 1.34, f"Left {enemies_left}")

    difficulty_stats = DIFFICULTIES[settings["difficulty"]]
    dudraw.set_pen_color_rgb(31, 38, 48)
    dudraw.filled_rectangle(7.65, GRID_HEIGHT + 1.34, 0.82, 0.18)
    set_color(difficulty_stats["color"])
    dudraw.rectangle(7.65, GRID_HEIGHT + 1.34, 0.82, 0.18)
    dudraw.text(7.65, GRID_HEIGHT + 1.32, difficulty_stats["name"].upper())

    progress = 1 if wave_total <= 0 else max(0, min(1, 1 - enemies_left / wave_total))
    dudraw.set_pen_color_rgb(43, 52, 64)
    dudraw.filled_rectangle(5.65, GRID_HEIGHT + 0.95, 3.9, 0.06)
    dudraw.set_pen_color_rgb(108, 212, 164)
    dudraw.filled_rectangle(1.75 + progress * 3.9, GRID_HEIGHT + 0.95, progress * 3.9, 0.045)
    dudraw.set_pen_color_rgb(218, 244, 232)
    dudraw.filled_circle(1.75 + progress * 7.8, GRID_HEIGHT + 0.95, 0.055)

    status = "READY" if between_waves else ("PAUSED" if paused else f"{speed_multiplier}x")
    dudraw.set_pen_color_rgb(38, 47, 58)
    dudraw.filled_rectangle(8.65, GRID_HEIGHT + 0.92, 0.72, 0.18)
    dudraw.set_pen_color_rgb(245, 231, 148)
    dudraw.rectangle(8.65, GRID_HEIGHT + 0.92, 0.72, 0.18)
    dudraw.text(8.65, GRID_HEIGHT + 0.9, status)

    controls = settings["controls"]
    draw_button(12.0, GRID_HEIGHT + 1.46, f"{control_key_label(controls['arrow'])} Arrow", TOWER_TYPES["arrow"]["color"], selected_tower == "arrow", money >= TOWER_TYPES["arrow"]["cost"])
    draw_button(14.7, GRID_HEIGHT + 1.46, f"{control_key_label(controls['cannon'])} Cannon", TOWER_TYPES["cannon"]["color"], selected_tower == "cannon", money >= TOWER_TYPES["cannon"]["cost"])
    draw_button(17.5, GRID_HEIGHT + 1.46, f"{control_key_label(controls['frost'])} Frost", TOWER_TYPES["frost"]["color"], selected_tower == "frost", money >= TOWER_TYPES["frost"]["cost"])
    draw_button(20.3, GRID_HEIGHT + 1.46, f"{control_key_label(controls['sniper'])} Sniper", TOWER_TYPES["sniper"]["color"], selected_tower == "sniper", money >= TOWER_TYPES["sniper"]["cost"])
    draw_button(12.0, GRID_HEIGHT + 0.93, f"{control_key_label(controls['laser'])} Laser", TOWER_TYPES["laser"]["color"], selected_tower == "laser", money >= TOWER_TYPES["laser"]["cost"])
    draw_button(14.7, GRID_HEIGHT + 0.93, f"{control_key_label(controls['mortar'])} Mortar", TOWER_TYPES["mortar"]["color"], selected_tower == "mortar", money >= TOWER_TYPES["mortar"]["cost"])
    draw_button(17.5, GRID_HEIGHT + 0.93, f"{control_key_label(controls['venom'])} Venom", TOWER_TYPES["venom"]["color"], selected_tower == "venom", money >= TOWER_TYPES["venom"]["cost"])
    draw_button(20.3, GRID_HEIGHT + 0.93, f"{control_key_label(controls['storm'])} Storm", TOWER_TYPES["storm"]["color"], selected_tower == "storm", money >= TOWER_TYPES["storm"]["cost"])
    special = SPECIAL_TOWERS[settings["special_tower"]]
    draw_button(22.7, GRID_HEIGHT + 1.46, f"{control_key_label(controls['special'])} Spec", special["color"], selected_tower == "special", not special_placed)

    dudraw.set_pen_color_rgb(221, 228, 232)
    dudraw.set_pen_color_rgb(40, 50, 62)
    dudraw.filled_rectangle(12, GRID_HEIGHT + 0.4, GRID_WIDTH / 2, 0.26)
    dudraw.set_pen_color_rgb(221, 228, 232)
    dudraw.text(5.6, GRID_HEIGHT + 0.42, "Select a tower to build")
    special_status = "used" if special_placed else "ready"
    if selected is None:
        dudraw.text(11.2, GRID_HEIGHT + 0.42, "Build: none  Click button or use shortcut")
        dudraw.text(18.0, GRID_HEIGHT + 0.42, f"Special {special_status}   Click a placed tower for stats")
    else:
        dudraw.text(11.2, GRID_HEIGHT + 0.42, f"Build: {selected['name']}  Cost: ${selected['cost']}")
        dudraw.text(18.0, GRID_HEIGHT + 0.42, f"Dmg {selected['damage']}  Rng {selected['range']}  9 special {special_status}")

    if game_over:
        dudraw.set_pen_color_rgb(12, 16, 22)
        dudraw.filled_rectangle(12, 8, 6.2, 2.5)
        dudraw.set_pen_color_rgb(195, 68, 62)
        dudraw.filled_rectangle(12, 9.65, 6.2, 0.08)
        dudraw.rectangle(12, 8, 6.2, 2.5)
        dudraw.set_pen_color(dudraw.WHITE)
        dudraw.text(12, 9.05, "Game Over")
        draw_menu_button(9.1, 7.85, 1.75, 0.34, "RESTART  (R)", True)
        draw_menu_button(14.9, 7.85, 1.75, 0.34, "MENU  (M)")


def draw_debug_overlay(money, lives, wave, enemies, towers, shots, particles, speed_multiplier, paused, auto_pause, between_waves):
    dudraw.set_pen_color_rgb(13, 18, 24)
    dudraw.filled_rectangle(3.4, 3.0, 3.2, 2.15)
    dudraw.set_pen_color_rgb(92, 235, 160)
    dudraw.rectangle(3.4, 3.0, 3.2, 2.15)
    dudraw.text(3.4, 4.65, "DEBUG MODE")
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(3.4, 4.1, f"Money {money}  Lives {lives}  Wave {wave}")
    dudraw.text(3.4, 3.55, f"Enemies {len(enemies)}  Towers {len(towers)}")
    dudraw.text(3.4, 3.0, f"Shots {len(shots)}  Particles {len(particles)}")
    dudraw.text(3.4, 2.45, f"Speed {speed_multiplier}x  Paused {paused}")
    dudraw.text(3.4, 1.9, f"Auto {auto_pause}  Between {between_waves}")
    dudraw.text(3.4, 1.35, "V speed  G +money  L +lives  N wave  B boss")


def draw_selected_tower_panel(tower, money, settings):
    if tower is None:
        return

    dudraw.set_pen_color_rgb(13, 18, 24)
    dudraw.filled_rectangle(4.25, 2.55, 3.95, 1.72)
    dudraw.set_pen_color_rgb(255, 241, 151)
    dudraw.rectangle(4.25, 2.55, 3.95, 1.72)
    set_color(brighten(tower.color, 45))
    dudraw.filled_rectangle(4.25, 4.23, 3.95, 0.035)
    dudraw.filled_circle(0.62, 3.83, 0.13)
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(4.25, 3.83, f"{tower.name}   Kills: {tower.kills}   Damage: {int(round(tower.total_damage))}")
    dudraw.text(4.25, 3.3, f"Hit {tower.damage}   Range {tower.range:.2f}   Cooldown {tower.max_cooldown}")

    if tower.is_special:
        dudraw.text(4.25, 2.7, "Special tower: no upgrades")
    else:
        power_cost = f"${tower.upgrade_cost('power')}" if tower.can_upgrade("power") else "locked"
        utility_cost = f"${tower.upgrade_cost('utility')}" if tower.can_upgrade("utility") else "locked"
        dudraw.text(3.75, 2.72, f"Power {tower.power_level}/4  {power_cost}")
        dudraw.text(3.75, 2.18, f"Speed + Range {tower.utility_level}/4  {utility_cost}")
        for index in range(4):
            dudraw.set_pen_color_rgb(255, 235, 134) if index < tower.power_level else dudraw.set_pen_color_rgb(62, 73, 83)
            dudraw.filled_rectangle(5.82 + index * 0.17, 2.72, 0.06, 0.045)
            dudraw.set_pen_color_rgb(116, 213, 193) if index < tower.utility_level else dudraw.set_pen_color_rgb(62, 73, 83)
            dudraw.filled_rectangle(5.82 + index * 0.17, 2.18, 0.06, 0.045)
        draw_menu_button(7.25, 2.72, 0.45, 0.2, control_key_label(settings["controls"]["upgrade_power"]), money >= tower.upgrade_cost("power") and tower.can_upgrade("power"))
        draw_menu_button(7.25, 2.18, 0.45, 0.2, control_key_label(settings["controls"]["upgrade_utility"]), money >= tower.upgrade_cost("utility") and tower.can_upgrade("utility"))

    dudraw.set_pen_color_rgb(191, 205, 214)
    dudraw.text(3.75, 1.58, f"Sell: ${int(tower.value * SELL_REFUND)}")
    draw_menu_button(7.25, 1.58, 0.45, 0.2, control_key_label(settings["controls"]["sell"]))


def draw_selected_tower_range(tower, frame, settings):
    if tower is None or tower.range <= 0 or not settings.get("show_range", True):
        return

    set_color(brighten(tower.color, 60))
    dudraw.square(tower.x, tower.y, 0.47)
    dudraw.circle(tower.x, tower.y, tower.range)
    for angle in (0, math.pi / 2, math.pi, math.pi * 1.5):
        marker_x = tower.x + math.cos(angle) * tower.range
        marker_y = tower.y + math.sin(angle) * tower.range
        dudraw.filled_circle(marker_x, marker_y, 0.045)


def draw_tower_target_links(towers, settings):
    if not settings.get("show_target_links", True):
        return
    for tower in towers:
        target = tower.target
        if target is None or not target.alive:
            continue

        set_color(brighten(tower.shot_color, 40))
        dudraw.line(tower.x, tower.y + 0.08, target.x, target.y)


def draw_toolbar_hover(money, settings):
    tower_type = tower_choice_at(dudraw.mouse_x(), dudraw.mouse_y())
    if tower_type is None:
        return

    stats = SPECIAL_TOWERS[settings["special_tower"]] if tower_type == "special" else TOWER_TYPES[tower_type]
    difficulty = DIFFICULTIES[settings["difficulty"]]
    damage = max(1, int(round(stats["damage"] * difficulty["damage"])))
    affordability = "ONCE PER GAME" if tower_type == "special" else ("READY" if money >= stats["cost"] else f"NEED ${stats['cost'] - money}")
    dudraw.set_pen_color_rgb(13, 18, 24)
    dudraw.filled_rectangle(12, 14.75, 4.35, 0.48)
    set_color(brighten(stats["color"], 50))
    dudraw.rectangle(12, 14.75, 4.35, 0.48)
    dudraw.filled_rectangle(12, 15.2, 4.35, 0.025)
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(12, 14.9, f"{stats['name']}  ${stats['cost']}  Hit {damage}  Range {stats['range']}  {affordability}")
    effects = []
    if stats["slow"] > 0:
        effects.append("slow")
    if stats["splash"] > 0:
        effects.append("splash")
    if stats["poison"] > 0:
        effects.append("poison")
    if stats.get("block_duration", 0) > 0:
        effects.append(f"roadblock {stats['block_duration']} ticks")
    dudraw.set_pen_color_rgb(191, 205, 214)
    dudraw.text(12, 14.53, "Effects: " + (", ".join(effects) if effects else "direct damage"))


def can_place_tower(grid_x, grid_y, towers, money, selected_tower, special_placed, settings):
    return placement_block_reason(grid_x, grid_y, towers, money, selected_tower, special_placed, settings) is None


def placement_block_reason(grid_x, grid_y, towers, money, selected_tower, special_placed, settings):
    if selected_tower is None:
        return "selection"

    if selected_tower == "special":
        if special_placed:
            return "special"
        tower_type = settings["special_tower"]
    else:
        tower_type = selected_tower

    if money < get_tower_stats(tower_type)["cost"]:
        return "money"
    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y < 0 or grid_y >= GRID_HEIGHT:
        return "bounds"
    if tower_type == "guardian":
        if (grid_x, grid_y) not in PATH_SQUARES:
            return "track"
    elif (grid_x, grid_y) in PATH_SQUARES:
        return "path"
    if tower_type != "guardian" and CURRENT_MAP["place_rule"] == "islands" and (grid_x, grid_y) not in BUILD_SQUARES:
        return "island"

    for tower in towers:
        if int(tower.x) == grid_x and int(tower.y) == grid_y:
            return "occupied"

    return None


def tower_choice_at(x, y):
    button_choices = [
        (12.0, GRID_HEIGHT + 1.46, "arrow"),
        (14.7, GRID_HEIGHT + 1.46, "cannon"),
        (17.5, GRID_HEIGHT + 1.46, "frost"),
        (20.3, GRID_HEIGHT + 1.46, "sniper"),
        (12.0, GRID_HEIGHT + 0.93, "laser"),
        (14.7, GRID_HEIGHT + 0.93, "mortar"),
        (17.5, GRID_HEIGHT + 0.93, "venom"),
        (20.3, GRID_HEIGHT + 0.93, "storm"),
        (22.7, GRID_HEIGHT + 1.46, "special"),
    ]

    for button_x, button_y, tower_type in button_choices:
        if point_in_rect(x, y, button_x, button_y, 1.08, 0.26):
            return tower_type

    return None


def placed_tower_at(towers, x, y):
    for tower in towers:
        if abs(tower.x - x) <= 0.5 and abs(tower.y - y) <= 0.5:
            return tower

    return None


def handle_clicks(towers, money, lives, selected_tower, selected_placed_tower, special_placed, settings, particles, match_stats, notices):
    if dudraw.mouse_clicked():
        mouse_x = dudraw.mouse_x()
        mouse_y = dudraw.mouse_y()

        if selected_placed_tower is not None:
            if point_in_rect(mouse_x, mouse_y, 7.25, 2.72, 0.45, 0.2):
                if not selected_placed_tower.is_special and selected_placed_tower.can_upgrade("power"):
                    cost = selected_placed_tower.upgrade_cost("power")
                    if money >= cost and selected_placed_tower.upgrade("power"):
                        money -= cost
                        match_stats["spent"] += cost
                        match_stats["upgrades"] += 1
                        particles.append([selected_placed_tower.x, selected_placed_tower.y, 0.25, 14, (255, 235, 118)])
                        add_notice(notices, f"{selected_placed_tower.name} power upgraded", (255, 235, 118))
                return money, lives, selected_tower, selected_placed_tower, special_placed
            if point_in_rect(mouse_x, mouse_y, 7.25, 2.18, 0.45, 0.2):
                if not selected_placed_tower.is_special and selected_placed_tower.can_upgrade("utility"):
                    cost = selected_placed_tower.upgrade_cost("utility")
                    if money >= cost and selected_placed_tower.upgrade("utility"):
                        money -= cost
                        match_stats["spent"] += cost
                        match_stats["upgrades"] += 1
                        particles.append([selected_placed_tower.x, selected_placed_tower.y, 0.25, 14, (255, 235, 118)])
                        add_notice(notices, f"{selected_placed_tower.name} speed upgraded", (255, 235, 118))
                return money, lives, selected_tower, selected_placed_tower, special_placed
            if point_in_rect(mouse_x, mouse_y, 7.25, 1.58, 0.45, 0.2):
                refund = int(selected_placed_tower.value * SELL_REFUND)
                match_stats["sold_damage"] += selected_placed_tower.total_damage
                match_stats["sold"] += 1
                if selected_placed_tower.is_special:
                    special_placed = False
                towers.remove(selected_placed_tower)
                money += refund
                particles.append([selected_placed_tower.x, selected_placed_tower.y, 0.25, 12, (149, 222, 132)])
                add_notice(notices, f"Tower sold  +${refund}", (149, 222, 132))
                return money, lives, selected_tower, None, special_placed

        choice = tower_choice_at(mouse_x, mouse_y)

        if choice is not None:
            stats = SPECIAL_TOWERS[settings["special_tower"]] if choice == "special" else TOWER_TYPES[choice]
            add_notice(notices, f"Build selected: {stats['name']}", brighten(stats["color"], 55))
            return money, lives, choice, None, special_placed

        clicked_tower = placed_tower_at(towers, mouse_x, mouse_y)
        if clicked_tower is not None:
            add_notice(notices, f"Selected {clicked_tower.name}", brighten(clicked_tower.color, 55), 45)
            return money, lives, None, clicked_tower, special_placed

        if selected_tower is None:
            return money, lives, selected_tower, selected_placed_tower, special_placed

        grid_x = int(mouse_x)
        grid_y = int(mouse_y)

        if can_place_tower(grid_x, grid_y, towers, money, selected_tower, special_placed, settings):
            if selected_tower == "special":
                tower_type = settings["special_tower"]
                special_placed = True
            else:
                tower_type = selected_tower

            stats = get_tower_stats(tower_type)
            towers.append(Tower(grid_x, grid_y, tower_type, settings["difficulty"]))
            money -= stats["cost"]
            match_stats["spent"] += stats["cost"]
            match_stats["built"] += 1
            money_bonus = earned_money(stats.get("money_bonus", 0), settings["difficulty"])
            money += money_bonus
            match_stats["earned"] += money_bonus
            lives += stats.get("lives_bonus", 0)
            particles.append([grid_x + 0.5, grid_y + 0.82, 0.05, 22, (255, 235, 118), f"-${stats['cost']}"])
            if money_bonus > 0:
                particles.append([grid_x + 0.5, grid_y + 1.1, 0.05, 24, (118, 230, 134), f"+${money_bonus}"])
            if stats.get("lives_bonus", 0) > 0:
                particles.append([grid_x + 0.5, grid_y + 1.36, 0.05, 24, (255, 137, 147), f"+{stats['lives_bonus']} lives"])
            add_notice(notices, f"{stats['name']} built", brighten(stats["color"], 60), 45)
        else:
            reason = placement_block_reason(grid_x, grid_y, towers, money, selected_tower, special_placed, settings)
            add_notice(notices, PLACEMENT_BLOCK_MESSAGES[reason], (237, 128, 111), 45)

    return money, lives, selected_tower, selected_placed_tower, special_placed


def handle_keys(settings):
    while dudraw.has_next_key_typed():
        key = dudraw.next_key_typed().lower()

        if key in ("escape", "esc", "\x1b"):
            return "cancel"
        for action, bound_key in settings["controls"].items():
            if key == bound_key:
                return action
        if key == "d":
            return "debug"
        if key == "g":
            return "debug_money"
        if key == "l":
            return "debug_lives"
        if key == "n":
            return "debug_wave"
        if key == "b":
            return "debug_boss"

    return None


def tower_under_mouse(towers):
    mouse_x = dudraw.mouse_x()
    mouse_y = dudraw.mouse_y()

    for tower in towers:
        if abs(tower.x - mouse_x) <= 0.5 and abs(tower.y - mouse_y) <= 0.5:
            return tower

    return None


def choose_enemy_type(wave, enemies_to_spawn):
    if wave >= 10 and enemies_to_spawn % 13 == 0:
        return "boss"
    if wave >= 8 and enemies_to_spawn % 7 == 0:
        return "armored"
    if wave >= 7 and enemies_to_spawn % 6 == 0:
        return "charger"
    if wave >= 6 and enemies_to_spawn % 5 == 0:
        return "wraith"
    if wave >= 5 and enemies_to_spawn % 7 == 0:
        return "brute"
    if wave >= 4 and enemies_to_spawn % 5 == 0:
        return "shield"
    if wave >= 4 and enemies_to_spawn % 4 == 0:
        return "splitter"
    if wave >= 3 and enemies_to_spawn % 3 == 0:
        return "runner"
    if wave >= 2 and enemies_to_spawn % 2 == 0:
        return "swarm"

    return "scout"


def run_game(settings):
    difficulty = settings["difficulty"]
    money = START_MONEY + earned_money(CURRENT_MAP["money_bonus"], difficulty)
    lives = starting_lives(CURRENT_MAP, difficulty)
    wave = 1
    spawn_timer = 0
    enemies_to_spawn = 8
    wave_total = enemies_to_spawn
    enemies = []
    towers = []
    shots = []
    particles = []
    notices = []
    match_stats = {
        "kills": 0,
        "earned": 0,
        "spent": 0,
        "built": 0,
        "upgrades": 0,
        "sold": 0,
        "sold_damage": 0,
        "leaks": 0,
        "waves": 0,
    }
    selected_tower = None
    selected_placed_tower = None
    special_placed = False
    game_over = False
    frame = 0
    debug_mode = False
    auto_pause = True
    between_waves = True
    paused = True
    speed_multiplier = 1

    while True:
        frame += 1
        action = handle_keys(settings)

        if action == "quit":
            return "quit"
        if action == "menu":
            return "menu"
        if action == "restart":
            return "restart"
        if action == "fullscreen":
            toggle_fullscreen(settings)
        if action in TOWER_TYPES or action == "special":
            selected_tower = action
            selected_placed_tower = None
            name = SPECIAL_TOWERS[settings["special_tower"]]["name"] if action == "special" else TOWER_TYPES[action]["name"]
            add_notice(notices, f"Build selected: {name}", (225, 233, 238), 45)
        if action == "cancel":
            selected_tower = None
            selected_placed_tower = None
            add_notice(notices, "Selection cleared", (191, 205, 214), 40)
        if action == "cycle_build":
            current = TOWER_ORDER.index(selected_tower) if selected_tower in TOWER_ORDER else -1
            selected_tower = TOWER_ORDER[(current + 1) % len(TOWER_ORDER)]
            selected_placed_tower = None
            add_notice(notices, f"Build selected: {selected_tower.title()}", (225, 233, 238), 40)
        if action == "debug":
            debug_mode = not debug_mode
        if action == "pause" and not game_over:
            paused = not paused
            if not paused and between_waves:
                between_waves = False
            add_notice(notices, "Paused" if paused else "Wave resumed", (191, 205, 214), 40)
        if action == "start_wave" and paused and not game_over:
            paused = False
            between_waves = False
            add_notice(notices, f"Wave {wave} started", (255, 235, 118), 45)
        if action == "auto_pause":
            auto_pause = not auto_pause
            add_notice(notices, f"Auto-pause: {'on' if auto_pause else 'off'}", (191, 205, 214), 45)
        if action == "speed":
            speed_multiplier = 1 if speed_multiplier == 2 else 2
            add_notice(notices, f"Speed {speed_multiplier}x", (186, 227, 250), 35)
        if action == "speed_up":
            speed_multiplier = min(3, speed_multiplier + 1)
            add_notice(notices, f"Speed {speed_multiplier}x", (186, 227, 250), 35)
        if action == "speed_down":
            speed_multiplier = max(1, speed_multiplier - 1)
            add_notice(notices, f"Speed {speed_multiplier}x", (186, 227, 250), 35)
        toggle_actions = {
            "stats": ("show_stats", "Match stats"),
            "links": ("show_target_links", "Target links"),
            "health": ("show_health_bars", "Health bars"),
            "floating": ("show_floating_text", "Floating text"),
            "arrows": ("show_path_arrows", "Path arrows"),
            "threat": ("show_threat_marks", "Threat marks"),
        }
        if action in toggle_actions:
            setting_key, label = toggle_actions[action]
            settings[setting_key] = not settings.get(setting_key, True)
            state = "on" if settings[setting_key] else "off"
            add_notice(notices, f"{label}: {state}", (191, 205, 214), 50)
        if game_over and dudraw.mouse_clicked():
            mouse_x = dudraw.mouse_x()
            mouse_y = dudraw.mouse_y()
            if point_in_rect(mouse_x, mouse_y, 9.1, 7.85, 1.75, 0.34):
                return "restart"
            if point_in_rect(mouse_x, mouse_y, 14.9, 7.85, 1.75, 0.34):
                return "menu"
        if debug_mode and action == "debug_money":
            money += 250
        if debug_mode and action == "debug_lives":
            lives += 5
        if debug_mode and action == "debug_wave":
            enemies.clear()
            enemies_to_spawn = 0
        if debug_mode and action == "debug_boss":
            enemies.append(Enemy(max(wave, 10), "boss", difficulty))
        if action in ("upgrade_power", "upgrade_utility"):
            path = "power" if action == "upgrade_power" else "utility"
            tower = selected_placed_tower
            if tower is not None and not tower.is_special and tower.can_upgrade(path):
                cost = tower.upgrade_cost(path)
                if money >= cost and tower.upgrade(path):
                    money -= cost
                    match_stats["spent"] += cost
                    match_stats["upgrades"] += 1
                    particles.append([tower.x, tower.y, 0.25, 14, (255, 235, 118)])
                    particles.append([tower.x, tower.y + 0.4, 0.05, 20, (255, 235, 118), "UPGRADE"])
                    add_notice(notices, f"{tower.name} upgraded", (255, 235, 118), 50)
                elif money < cost:
                    add_notice(notices, f"Need ${cost - money} for upgrade", (237, 128, 111), 50)
            elif tower is None:
                add_notice(notices, "Select a placed tower first", (237, 128, 111), 45)
        if action == "sell":
            tower = selected_placed_tower
            if tower is not None:
                refund = int(tower.value * SELL_REFUND)
                match_stats["sold"] += 1
                match_stats["sold_damage"] += tower.total_damage
                if tower.is_special:
                    special_placed = False
                towers.remove(tower)
                money += refund
                particles.append([tower.x, tower.y, 0.25, 12, (149, 222, 132)])
                particles.append([tower.x, tower.y + 0.35, 0.05, 22, (149, 222, 132), f"+${refund}"])
                add_notice(notices, f"{tower.name} sold  +${refund}", (149, 222, 132), 50)
                selected_placed_tower = None
            else:
                add_notice(notices, "Select a tower to sell", (237, 128, 111), 45)

        if not game_over and (not paused or between_waves):
            money, lives, selected_tower, selected_placed_tower, special_placed = handle_clicks(
                towers, money, lives, selected_tower, selected_placed_tower, special_placed, settings, particles, match_stats, notices
            )

        if not game_over and not paused:
            if between_waves:
                between_waves = False

            for tick in range(speed_multiplier):
                if enemies_to_spawn > 0:
                    spawn_timer -= 1
                    if spawn_timer <= 0:
                        enemy_type = choose_enemy_type(wave, enemies_to_spawn)
                        enemies.append(Enemy(wave, enemy_type, difficulty))
                        enemies_to_spawn -= 1
                        spawn_timer = max(8, int((45 - wave * 2) * DIFFICULTIES[difficulty]["spawn"]))

                for enemy in enemies:
                    enemy.move(towers)

                for tower in towers:
                    tower.update(enemies, shots, particles)

            for enemy in enemies[:]:
                if not enemy.alive:
                    enemies.remove(enemy)

                    if enemy.escaped:
                        lives -= 1
                        match_stats["leaks"] += 1
                        particles.append([enemy.x, enemy.y, 0.28, 10, (240, 82, 78)])
                        particles.append([enemy.x, enemy.y + 0.35, 0.05, 22, (255, 125, 130), "-1 life"])
                        add_notice(notices, "Enemy leaked  -1 life", (255, 125, 130), 50)
                    else:
                        if enemy.last_hit_tower is not None:
                            enemy.last_hit_tower.kills += 1
                            bounty = earned_money(enemy.last_hit_tower.kill_bonus, difficulty)
                            if bounty > 0:
                                money += bounty
                                match_stats["earned"] += bounty
                                particles.append([enemy.x, enemy.y + 0.65, 0.05, 24, (255, 211, 80), f"MINT +${bounty}"])
                        match_stats["kills"] += 1
                        match_stats["earned"] += enemy.reward
                        money += enemy.reward
                        particles.append([enemy.x, enemy.y, 0.22, 12, brighten(enemy.color, 80)])
                        particles.append([enemy.x, enemy.y + 0.35, 0.05, 20, (118, 230, 134), f"+${enemy.reward}"])

            if enemies_to_spawn == 0 and len(enemies) == 0:
                wave += 1
                enemies_to_spawn = 7 + wave * 2
                wave_total = enemies_to_spawn
                wave_reward = earned_money(CURRENT_MAP["wave_bonus"], difficulty)
                money += wave_reward
                match_stats["earned"] += wave_reward
                match_stats["waves"] += 1
                add_notice(notices, f"Wave {wave - 1} cleared  +${wave_reward}", (255, 235, 118), 80)
                particles.append([12, 8.8, 0.05, 32, (255, 235, 118), f"Wave {wave}  +${wave_reward}"])
                between_waves = True
                paused = auto_pause

                if not auto_pause:
                    between_waves = False

            if lives <= 0:
                game_over = True

        shots = [shot for shot in shots if shot[4] > 0]

        draw_grid(settings, frame)
        draw_placement_preview(towers, selected_tower, special_placed, settings, money)
        draw_selected_tower_range(selected_placed_tower, frame, settings)
        draw_towers(towers, settings, frame)
        draw_enemies(enemies, settings, frame)
        draw_tower_target_links(towers, settings)
        draw_shots(shots, settings)
        draw_particles(particles, settings)
        draw_ui(money, lives, wave, enemies_to_spawn + len(enemies), wave_total, selected_tower, special_placed, settings, game_over, paused, between_waves, speed_multiplier, frame)
        draw_selected_tower_panel(selected_placed_tower, money, settings)
        draw_match_stats(match_stats, towers, settings)
        draw_toolbar_hover(money, settings)
        draw_notices(notices)
        if paused:
            dudraw.set_pen_color_rgb(13, 18, 24)
            dudraw.filled_rectangle(12, 8, 3.2, 0.9)
            dudraw.set_pen_color(dudraw.WHITE)
            if between_waves:
                dudraw.text(12, 8.2, "BETWEEN WAVES")
                start_key = control_key_label(settings["controls"]["start_wave"])
                pause_key = control_key_label(settings["controls"]["pause"])
                dudraw.text(12, 7.75, f"Press {pause_key} or {start_key} to start")
            else:
                dudraw.text(12, 8, "PAUSED")
        if debug_mode:
            draw_debug_overlay(money, lives, wave, enemies, towers, shots, particles, speed_multiplier, paused, auto_pause, between_waves)
        dudraw.show(25)


def main():
    setup_canvas()
    settings = DEFAULT_SETTINGS.copy()
    settings["controls"] = DEFAULT_CONTROLS.copy()

    while True:
        action = run_start_screen(settings)

        if action == "quit":
            return

        if action == "settings":
            run_settings_screen(settings)
            continue

        if action == "controls":
            run_controls_screen(settings)
            continue

        if action == "dictionary":
            run_dictionary_screen(settings)
            continue

        if action == "special":
            run_special_screen(settings)
            continue

        if settings["graphics"] != "amazing":
            run_future_update_popup(settings)
            continue

        map_key = run_map_select_screen(settings)

        if map_key is None:
            continue

        set_current_map(map_key)

        if not run_difficulty_screen(settings):
            continue

        game_action = "restart"

        while game_action == "restart":
            game_action = run_game(settings)

        if game_action == "quit":
            return


if __name__ == "__main__":
    main()
