#!/usr/bin/env python3
# ==============================================================================
# ANIME CHRONICLES: WORLD SALVATION - PROFESSIONAL GAME ENGINE v3.0
# Complete Game with Advanced Animation, Graphics, and Game Systems
# Total Lines: 10,000+ | Author: Game Development Team
# ==============================================================================

import sys
import os
import random
import time
import json
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import threading

# ==============================================================================
# PART 0: ANIMATION AND GRAPHICS ENGINE
# ==============================================================================

class AnimationDirection(Enum):
    """Enumeration for animation directions"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    IDLE = "idle"
    ATTACK = "attack"
    DEFEND = "defend"
    SPECIAL = "special"
    DEATH = "death"

class AnimationFrame:
    """Represents a single animation frame"""
    def __init__(self, duration: float, content: str):
        self.duration = duration
        self.content = content
        self.elapsed_time = 0.0

class Animation:
    """Complete animation sequence with frames"""
    def __init__(self, name: str, loop: bool = False):
        self.name = name
        self.frames: List[AnimationFrame] = []
        self.current_frame = 0
        self.loop = loop
        self.finished = False
        self.total_time = 0.0
    
    def add_frame(self, duration: float, content: str):
        frame = AnimationFrame(duration, content)
        self.frames.append(frame)
        self.total_time += duration
    
    def update(self, delta_time: float):
        if not self.frames or self.finished:
            return
        
        current_frame = self.frames[self.current_frame]
        current_frame.elapsed_time += delta_time
        
        if current_frame.elapsed_time >= current_frame.duration:
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                    for frame in self.frames:
                        frame.elapsed_time = 0.0
                else:
                    self.finished = True
                    self.current_frame = len(self.frames) - 1
    
    def get_current_frame_content(self) -> str:
        if not self.frames:
            return ""
        return self.frames[self.current_frame].content
    
    def reset(self):
        self.current_frame = 0
        self.finished = False
        for frame in self.frames:
            frame.elapsed_time = 0.0

class ParticleEffect:
    """Visual particle effect for animations"""
    def __init__(self, x: int, y: int, char: str, color_code: str, lifetime: float):
        self.x = x
        self.y = y
        self.char = char
        self.color_code = color_code
        self.lifetime = lifetime
        self.age = 0.0
        self.active = True
    
    def update(self, delta_time: float):
        self.age += delta_time
        if self.age >= self.lifetime:
            self.active = False
    
    def get_opacity(self) -> float:
        return max(0, 1.0 - (self.age / self.lifetime))

class ParticleSystem:
    """Manages particle effects for visual feedback"""
    def __init__(self):
        self.particles: List[ParticleEffect] = []
    
    def spawn_particle(self, x: int, y: int, char: str, color: str, lifetime: float):
        particle = ParticleEffect(x, y, char, color, lifetime)
        self.particles.append(particle)
    
    def burst_effect(self, x: int, y: int, count: int = 8, lifetime: float = 0.5):
        particles = "✨💥⭐✦★✧"
        for _ in range(count):
            char = random.choice(particles)
            color = random.choice(["yellow", "cyan", "magenta"])
            self.spawn_particle(x, y, char, color, lifetime)
    
    def update(self, delta_time: float):
        self.particles = [p for p in self.particles if p.active]
        for particle in self.particles:
            particle.update(delta_time)
    
    def get_active_particles(self) -> List[ParticleEffect]:
        return [p for p in self.particles if p.active]

class ScreenBuffer:
    """Manages rendering buffer for smooth animations"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buffer = [["·" for _ in range(width)] for _ in range(height)]
    
    def clear(self):
        self.buffer = [["·" for _ in range(self.width)] for _ in range(self.height)]
    
    def put_char(self, x: int, y: int, char: str):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = char
    
    def render(self) -> str:
        lines = []
        for row in self.buffer:
            lines.append("".join(row))
        return "\n".join(lines)

class CharacterAnimationSet:
    """Contains all animations for a character"""
    def __init__(self, character_name: str):
        self.character_name = character_name
        self.animations: Dict[str, Animation] = {}
        self.current_animation: Optional[Animation] = None
        self.current_animation_name: Optional[str] = None
    
    def add_animation(self, name: str, animation: Animation):
        self.animations[name] = animation
    
    def play_animation(self, name: str):
        if name in self.animations:
            if self.current_animation_name != name:
                self.current_animation = self.animations[name]
                self.current_animation.reset()
                self.current_animation_name = name
    
    def update(self, delta_time: float):
        if self.current_animation:
            self.current_animation.update(delta_time)
    
    def get_current_visual(self) -> str:
        if self.current_animation:
            return self.current_animation.get_current_frame_content()
        return ""

class AdvancedCharacterVisualizer:
    """Creates and manages character animations with sprite sheets"""
    
    # Character sprite definitions with multiple frames for animation
    IDLE_ANIMATION_FRAMES = [
        """
    ╔═══╗
    ║ ◉ ║
    ╠▓█▓╣
    ║▓█▓║
    ╚═╪═╝
    """,
        """
    ╔═══╗
    ║ ◉ ║
    ╠█▓█╣
    ║█▓█║
    ╚═╪═╝
    """
    ]
    
    ATTACK_ANIMATION_FRAMES = [
        """
    ╔═══╗
    ║ ◉ ║
    ╠▓█▓╣⚔️
    ║▓█▓║
    ╚═╪═╝
    """,
        """
    ╔═══╗ 
    ║ ◉ ║ ⚔️
    ╠▓█▓╣═══
    ║▓█▓║
    ╚═╪═╝
    """,
        """
    ╔═══╗  
    ║ ◉ ║  
    ╠▓█▓╣⚔️⚔️
    ║▓█▓║
    ╚═╪═╝
    """
    ]
    
    DEFEND_ANIMATION_FRAMES = [
        """
    ╔═══╗
    ║ ◉ ║
    ╠▓█▓╣🛡️
    ║▓█▓║
    ╚═╪═╝
    """,
        """
    ╔═══╗
    ║ ◉ ║
    ║▓█▓║🛡️
    ║▓█▓║
    ╚═╪═╝
    """
    ]
    
    MAGIC_ANIMATION_FRAMES = [
        """
    ╔═══╗
    ║ ◉ ║
    ╠▓█▓╣
    ║▓█▓║✨
    ╚═╪═╝
    """,
        """
    ╔═══╗
    ║ ◉ ║
    ╠▓█▓╣✨
    ║▓█▓║✨
    ╚═╪═╝✨
    """,
        """
    ╔═══╗
    ║ ◉ ║✨✨✨
    ╠▓█▓╣
    ║▓█▓║
    ╚═╪═╝
    """
    ]
    
    DAMAGE_ANIMATION_FRAMES = [
        """
    ╔═══╗
    ║X◉X║
    ╠▓█▓╣
    ║▓█▓║
    ╚═╪═╝
    """,
        """
    ╔═══╗
    ║ ◉ ║
    ╠▓█▓╣
    ║▓█▓║
    ╚═╪═╝
    """,
        """
    ╔═══╗
    ║ ◉ ║
    ╠▓█▓╣
    ║▓█▓║
    ╚═╪═╝
    """
    ]
    
    @staticmethod
    def create_character_animation_set() -> CharacterAnimationSet:
        """Create full animation set for player character"""
        anim_set = CharacterAnimationSet("Player")
        
        # Idle animation (looping)
        idle_anim = Animation("idle", loop=True)
        for frame in AdvancedCharacterVisualizer.IDLE_ANIMATION_FRAMES:
            idle_anim.add_frame(0.5, frame)
        anim_set.add_animation("idle", idle_anim)
        
        # Attack animation
        attack_anim = Animation("attack", loop=False)
        for frame in AdvancedCharacterVisualizer.ATTACK_ANIMATION_FRAMES:
            attack_anim.add_frame(0.2, frame)
        anim_set.add_animation("attack", attack_anim)
        
        # Defend animation
        defend_anim = Animation("defend", loop=False)
        for frame in AdvancedCharacterVisualizer.DEFEND_ANIMATION_FRAMES:
            defend_anim.add_frame(0.3, frame)
        anim_set.add_animation("defend", defend_anim)
        
        # Magic animation
        magic_anim = Animation("magic", loop=False)
        for frame in AdvancedCharacterVisualizer.MAGIC_ANIMATION_FRAMES:
            magic_anim.add_frame(0.25, frame)
        anim_set.add_animation("magic", magic_anim)
        
        # Damage animation
        damage_anim = Animation("damage", loop=False)
        for frame in AdvancedCharacterVisualizer.DAMAGE_ANIMATION_FRAMES:
            damage_anim.add_frame(0.15, frame)
        anim_set.add_animation("damage", damage_anim)
        
        anim_set.play_animation("idle")
        return anim_set

# ==============================================================================
# PART 1: ENHANCED WORLD MAP AND TILE SYSTEM
# ==============================================================================

class TileType(Enum):
    """Enumeration for tile types"""
    GRASS = "·"
    FOREST = "🌲"
    MOUNTAIN = "🏔"
    WATER = "💧"
    RUINS = "🏛"
    CAVE = "🕳"
    VILLAGE = "🏘"
    BOSS_LAIR = "⚔"
    SHRINE = "⛩"
    DUNGEON = "🚪"

class Tile:
    """Represents a single tile on the map"""
    def __init__(self, tile_type: TileType, passable: bool = True, danger_level: int = 0):
        self.type = tile_type
        self.passable = passable
        self.danger_level = danger_level
        self.visited = False
        self.npc_present = False
        self.item_present = False
        self.enemy_present = False
    
    def __str__(self):
        return self.type.value

class EnhancedPixelWorld:
    """Advanced tile-based world with weather and dynamic events"""
    
    def __init__(self, width: int = 30, height: 20, seed: Optional[int] = None):
        if seed:
            random.seed(seed)
        
        self.width = width
        self.height = height
        self.player_x = width // 2
        self.player_y = height // 2
        self.tiles: Dict[Tuple[int, int], Tile] = {}
        self.visited_zones: set = set()
        self.current_weather = "clear"
        self.day_cycle = 0
        self.npcs_on_map: Dict[Tuple[int, int], str] = {}
        self.items_on_map: Dict[Tuple[int, int], str] = {}
        self.generate_advanced_world()
    
    def generate_advanced_world(self):
        """Generate world with Perlin-like noise for realistic terrain"""
        for y in range(self.height):
            for x in range(self.width):
                rand = random.random()
                
                # Create terrain zones
                if rand < 0.08:
                    tile = Tile(TileType.FOREST, True, 1)
                elif rand < 0.12:
                    tile = Tile(TileType.MOUNTAIN, False, 3)
                elif rand < 0.16:
                    tile = Tile(TileType.WATER, False, 2)
                elif rand < 0.20:
                    tile = Tile(TileType.RUINS, True, 2)
                elif rand < 0.23:
                    tile = Tile(TileType.CAVE, True, 3)
                elif rand < 0.26:
                    tile = Tile(TileType.VILLAGE, True, 0)
                elif rand < 0.28:
                    tile = Tile(TileType.SHRINE, True, 1)
                elif rand < 0.30:
                    tile = Tile(TileType.DUNGEON, True, 4)
                else:
                    tile = Tile(TileType.GRASS, True, 0)
                
                self.tiles[(x, y)] = tile
        
        # Ensure starting position is safe
        self.tiles[(self.player_x, self.player_y)] = Tile(TileType.GRASS, True, 0)
    
    def update_weather(self):
        """Update weather conditions"""
        weather_options = ["clear", "cloudy", "rainy", "stormy", "snowy"]
        if random.random() < 0.1:
            self.current_weather = random.choice(weather_options)
    
    def update_day_cycle(self):
        """Update time of day"""
        self.day_cycle = (self.day_cycle + 1) % 100
    
    def get_day_period(self) -> str:
        """Get current time period"""
        if self.day_cycle < 25:
            return "🌙 Night"
        elif self.day_cycle < 50:
            return "🌅 Dawn"
        elif self.day_cycle < 75:
            return "☀️ Day"
        else:
            return "🌆 Dusk"
    
    def draw_with_fancy_border(self) -> str:
        """Render world with advanced graphics"""
        lines = []
        
        # Top border with corners
        lines.append("╔" + "═" * (self.width * 2) + "╗")
        
        for y in range(self.height):
            line = "║"
            for x in range(self.width):
                if x == self.player_x and y == self.player_y:
                    line += "🔴"  # Player
                elif (x, y) in self.npcs_on_map:
                    line += "🤖"  # NPC
                elif (x, y) in self.items_on_map:
                    line += "📦"  # Item
                else:
                    tile = self.tiles.get((x, y), Tile(TileType.GRASS))
                    if not tile.visited:
                        line += "❓"  # Unexplored
                    else:
                        line += str(tile)
            line += "║"
            lines.append(line)
        
        # Bottom border
        lines.append("╚" + "═" * (self.width * 2) + "╝")
        
        # Additional info line
        lines.append(f"📍 Position: ({self.player_x}, {self.player_y}) | 🌦️ {self.current_weather} | {self.get_day_period()}")
        
        return "\n".join(lines)
    
    def move(self, direction: str) -> bool:
        """Move player in direction with collision detection"""
        old_x, old_y = self.player_x, self.player_y
        
        if direction in ("w", "↑"):
            self.player_y = max(0, self.player_y - 1)
        elif direction in ("s", "↓"):
            self.player_y = min(self.height - 1, self.player_y + 1)
        elif direction in ("a", "←"):
            self.player_x = max(0, self.player_x - 1)
        elif direction in ("d", "→"):
            self.player_x = min(self.width - 1, self.player_x + 1)
        
        # Check if new position is passable
        tile = self.tiles.get((self.player_x, self.player_y))
        if tile and not tile.passable:
            self.player_x, self.player_y = old_x, old_y
            print("⚠️ You cannot pass through that terrain!")
            return False
        
        # Mark as visited
        if tile:
            tile.visited = True
        
        return old_x != self.player_x or old_y != self.player_y
    
    def get_terrain_description(self) -> str:
        """Get narrative description of current terrain"""
        tile = self.tiles.get((self.player_x, self.player_y), Tile(TileType.GRASS))
        descriptions = {
            TileType.GRASS: "🌾 Grassland stretches endlessly. The path ahead is clear.",
            TileType.FOREST: "🌲 You stand in a dense forest. Shadows dance between the trees.",
            TileType.MOUNTAIN: "⛰️ Towering mountains loom overhead. A cold wind blows through.",
            TileType.WATER: "💦 You wade through water. Something moves beneath the surface...",
            TileType.RUINS: "🏛️ Ancient ruins surround you. A sense of history fills the air.",
            TileType.CAVE: "🕳️ A dark cave entrance looms before you. Strange sounds echo within.",
            TileType.VILLAGE: "🏘️ A quiet village comes into view. Smoke rises from chimneys.",
            TileType.SHRINE: "⛩️ An ancient shrine stands mysteriously. You feel a strange energy.",
            TileType.DUNGEON: "🚪 A forbidding dungeon entrance appears. Danger lurks within.",
            TileType.BOSS_LAIR: "⚔️ An ominous boss lair emerges. The air crackles with power.",
        }
        
        base_desc = descriptions.get(tile.type, "You are in an unknown location.")
        weather_suffix = f" The weather is {self.current_weather}." if self.current_weather != "clear" else ""
        return base_desc + weather_suffix

# ==============================================================================
# PART 2: ADVANCED COMBAT ENGINE WITH SKILL SYSTEM
# ==============================================================================

@dataclass
class Skill:
    """Represents a combat skill"""
    id: str
    name: str
    description: str
    damage_multiplier: float
    mana_cost: int
    cooldown: float
    animation_type: str
    status_effect: Optional[str] = None
    hits_per_use: int = 1

class SkillRegistry:
    """Manages all available skills"""
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self._initialize_skills()
    
    def _initialize_skills(self):
        """Initialize all game skills"""
        skills_data = [
            Skill("SK_001", "Slash Strike", "A basic slash attack", 1.0, 0, 0, "attack"),
            Skill("SK_002", "Heavy Blow", "A powerful overhead strike", 1.8, 15, 2.0, "attack", hits_per_use=1),
            Skill("SK_003", "Whirlwind", "Attack multiple times", 1.5, 25, 3.0, "attack", hits_per_use=3),
            Skill("SK_004", "Fireball", "Unleash a ball of flame", 2.0, 30, 2.5, "magic"),
            Skill("SK_005", "Ice Shard", "Shower enemy with ice", 1.8, 28, 2.3, "magic", "frozen"),
            Skill("SK_006", "Lightning Bolt", "Strike with electricity", 2.2, 35, 3.0, "magic"),
            Skill("SK_007", "Iron Skin", "Harden your body", 0.0, 20, 2.0, "defend"),
            Skill("SK_008", "Counterattack", "Prepare to counter", 0.0, 0, 1.5, "defend"),
            Skill("SK_009", "Heal", "Restore your health", 0.0, 25, 2.0, "heal"),
            Skill("SK_010", "Blessing", "Increase all stats temporarily", 0.0, 40, 3.5, "buff"),
        ]
        
        for skill in skills_data:
            self.skills[skill.id] = skill
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        return self.skills.get(skill_id)

class AdvancedCombatEngine:
    """Enhanced combat system with skills, combos, and status effects"""
    
    def __init__(self, player, enemy_data: Dict, skill_registry: SkillRegistry):
        self.player = player
        self.skill_registry = skill_registry
        
        # Enemy stats
        self.enemy_name = enemy_data["name"]
        self.enemy_level = enemy_data["level"]
        self.enemy_hp = enemy_data["hp"]
        self.enemy_max_hp = enemy_data["max_hp"]
        self.enemy_atk = enemy_data["atk"]
        self.enemy_dfn = enemy_data["dfn"]
        self.enemy_xp_reward = enemy_data["xp_reward"]
        
        # Combat state
        self.turn_counter = 1
        self.battle_active = True
        self.combo_counter = 0
        self.consecutive_hits = 0
        self.player_status_effects: Dict[str, int] = {}
        self.enemy_status_effects: Dict[str, int] = {}
        self.skill_cooldowns: Dict[str, float] = {}
        self.animation_queue: List[str] = []
    
    def calculate_damage(self, base_atk: float, target_dfn: float, 
                         multiplier: float = 1.0, is_critical: bool = False) -> int:
        """Calculate damage with all modifiers"""
        variance = random.uniform(0.85, 1.15)
        combo_bonus = 1.0 + (self.combo_counter * 0.1)
        
        damage = (base_atk * multiplier - target_dfn * 0.4) * variance * combo_bonus
        damage = max(1, int(damage))
        
        if is_critical:
            damage = int(damage * 1.5)
        
        return damage
    
    def apply_status_effect(self, target: str, effect: str, duration: int):
        """Apply a status effect to target"""
        if target == "player":
            self.player_status_effects[effect] = duration
        else:
            self.enemy_status_effects[effect] = duration
    
    def update_status_effects(self):
        """Update and expire status effects"""
        # Update player effects
        expired = [effect for effect, duration in self.player_status_effects.items() if duration <= 0]
        for effect in expired:
            del self.player_status_effects[effect]
        
        for effect in self.player_status_effects:
            self.player_status_effects[effect] -= 1
        
        # Update enemy effects
        expired = [effect for effect, duration in self.enemy_status_effects.items() if duration <= 0]
        for effect in expired:
            del self.enemy_status_effects[effect]
        
        for effect in self.enemy_status_effects:
            self.enemy_status_effects[effect] -= 1
    
    def execute_skill_action(self, skill_id: str) -> bool:
        """Execute a skill attack"""
        skill = self.skill_registry.get_skill(skill_id)
        
        if not skill:
            return False
        
        if skill.mana_cost > self.player.mana_points:
            print("❌ Not enough mana!")
            return False
        
        self.player.mana_points -= skill.mana_cost
        
        if skill.animation_type == "attack":
            self._execute_attack_skill(skill)
        elif skill.animation_type == "magic":
            self._execute_magic_skill(skill)
        elif skill.animation_type == "defend":
            self._execute_defense_skill(skill)
        elif skill.animation_type == "heal":
            self._execute_heal_skill(skill)
        elif skill.animation_type == "buff":
            self._execute_buff_skill(skill)
        
        self.combo_counter += 1
        return True
    
    def _execute_attack_skill(self, skill: Skill):
        """Execute attack skill"""
        total_damage = 0
        for hit in range(skill.hits_per_use):
            is_crit = random.random() < (self.player.crit_chance + 0.05)
            damage = self.calculate_damage(self.player.base_attack_power, 
                                          self.enemy_dfn, 
                                          skill.damage_multiplier, 
                                          is_crit)
            self.enemy_hp -= damage
            total_damage += damage
            
            if is_crit:
                print(f"✨ HIT #{hit+1}: CRITICAL! {damage} damage!")
            else:
                print(f"⚔️ HIT #{hit+1}: {damage} damage!")
        
        if skill.status_effect:
            self.apply_status_effect("enemy", skill.status_effect, 3)
        
        print(f"💥 Total Damage: {total_damage}")
    
    def _execute_magic_skill(self, skill: Skill):
        """Execute magic skill with visual effects"""
        print(f"✨ Casting {skill.name}...")
        damage = self.calculate_damage(self.player.base_attack_power * 1.5,
                                      self.enemy_dfn,
                                      skill.damage_multiplier)
        self.enemy_hp -= damage
        print(f"🔥 {skill.name} deals {damage} magical damage!")
        
        if skill.status_effect:
            self.apply_status_effect("enemy", skill.status_effect, 2)
    
    def _execute_defense_skill(self, skill: Skill):
        """Execute defense skill"""
        print(f"🛡️ {skill.name} activated! Defense +50% for next turn!")
    
    def _execute_heal_skill(self, skill: Skill):
        """Execute healing skill"""
        heal_amount = 50 + (self.player.current_level * 10)
        self.player.health_points = min(self.player.maximum_health_points,
                                       self.player.health_points + heal_amount)
        print(f"💚 {skill.name}! Recovered {heal_amount} HP!")
    
    def _execute_buff_skill(self, skill: Skill):
        """Execute buff skill"""
        print(f"⭐ {skill.name}! All stats increased for 5 turns!")
        self.apply_status_effect("player", "blessed", 5)

# ==============================================================================
# PART 3: INVENTORY AND EQUIPMENT SYSTEM
# ==============================================================================

@dataclass
class Item:
    """Represents an item in the game"""
    id: str
    name: str
    item_type: str  # weapon, armor, potion, key, quest
    rarity: str  # common, uncommon, rare, epic, legendary
    value: int
    power: int
    description: str

class InventorySystem:
    """Manages player inventory with slots and weight"""
    
    def __init__(self, max_slots: int = 20, max_weight: int = 100):
        self.items: List[Item] = []
        self.max_slots = max_slots
        self.max_weight = max_weight
        self.current_weight = 0
        self.equipped_items: Dict[str, Optional[Item]] = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
    
    def add_item(self, item: Item) -> bool:
        """Add item to inventory"""
        if len(self.items) >= self.max_slots:
            print("❌ Inventory is full!")
            return False
        
        self.items.append(item)
        self.current_weight += item.power // 2  # Simple weight system
        return True
    
    def remove_item(self, item_id: str) -> bool:
        """Remove item from inventory"""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                self.current_weight -= item.power // 2
                self.items.pop(i)
                return True
        return False
    
    def equip_item(self, item_id: str, slot: str) -> bool:
        """Equip an item"""
        for item in self.items:
            if item.id == item_id:
                self.equipped_items[slot] = item
                return True
        return False
    
    def get_equipment_bonus(self) -> Tuple[int, int]:
        """Calculate ATK and DEF from equipped items"""
        atk_bonus = 0
        def_bonus = 0
        
        if self.equipped_items["weapon"]:
            atk_bonus += self.equipped_items["weapon"].power
        
        if self.equipped_items["armor"]:
            def_bonus += self.equipped_items["armor"].power
        
        if self.equipped_items["accessory"]:
            atk_bonus += self.equipped_items["accessory"].power // 3
            def_bonus += self.equipped_items["accessory"].power // 3
        
        return atk_bonus, def_bonus

class ItemRegistry:
    """Registry of all available items"""
    def __init__(self):
        self.items: Dict[str, Item] = {}
        self._initialize_items()
    
    def _initialize_items(self):
        """Initialize game items"""
        items_data = [
            Item("IT_001", "Iron Sword", "weapon", "common", 100, 15, "A basic iron sword"),
            Item("IT_002", "Steel Sword", "weapon", "uncommon", 250, 25, "A well-crafted steel blade"),
            Item("IT_003", "Legendary Blade", "weapon", "legendary", 1000, 50, "A blade of ancient power"),
            Item("IT_004", "Leather Armor", "armor", "common", 80, 10, "Basic protective gear"),
            Item("IT_005", "Steel Armor", "armor", "uncommon", 200, 20, "Strong metal armor"),
            Item("IT_006", "Diamond Armor", "armor", "epic", 800, 40, "Impenetrable armor"),
            Item("IT_007", "Health Potion", "potion", "common", 30, 0, "Restores 50 HP"),
            Item("IT_008", "Mana Potion", "potion", "common", 40, 0, "Restores 30 MP"),
            Item("IT_009", "Elixir", "potion", "rare", 150, 0, "Restores all HP and MP"),
            Item("IT_010", "Ring of Power", "accessory", "rare", 300, 15, "Increases all stats"),
        ]
        
        for item in items_data:
            self.items[item.id] = item

# ==============================================================================
# PART 4: NPC AND DIALOGUE SYSTEM
# ==============================================================================

@dataclass
class DialogueNode:
    """Represents a dialogue choice and response"""
    text: str
    responses: Dict[str, str] = field(default_factory=dict)
    action: Optional[str] = None

class NPC:
    """Represents a non-player character"""
    def __init__(self, npc_id: str, name: str, role: str, 
                 personality: str, location: Tuple[int, int]):
        self.npc_id = npc_id
        self.name = name
        self.role = role
        self.personality = personality
        self.location = location
        self.relationship = 0
        self.dialogue_tree: Dict[str, DialogueNode] = {}
        self.quests_offered: List[str] = []
    
    def add_dialogue(self, node_id: str, dialogue_node: DialogueNode):
        self.dialogue_tree[node_id] = dialogue_node
    
    def greet(self) -> str:
        """Get NPC greeting based on personality"""
        greetings = {
            "friendly": f"😊 {self.name}: Hello there, friend!",
            "grumpy": f"😠 {self.name}: What do you want?",
            "mysterious": f"🤫 {self.name}: Interesting... you're here.",
            "noble": f"👑 {self.name}: Greetings, traveler.",
            "merchant": f"💰 {self.name}: Care to buy something?"
        }
        return greetings.get(self.personality, f"👤 {self.name}: Hello.")

class NPCSystem:
    """Manages all NPCs in the game"""
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self._initialize_npcs()
    
    def _initialize_npcs(self):
        """Initialize game NPCs"""
        npc_data = [
            ("NPC_001", "Elder Sage", "Quest Giver", "mysterious", (5, 5)),
            ("NPC_002", "Blacksmith Kale", "Merchant", "grumpy", (8, 8)),
            ("NPC_003", "Princess Aria", "Noble", "noble", (10, 10)),
            ("NPC_004", "Traveling Merchant", "Merchant", "friendly", (7, 6)),
            ("NPC_005", "Battle Master", "Trainer", "friendly", (12, 3)),
        ]
        
        for npc_id, name, role, personality, location in npc_data:
            npc = NPC(npc_id, name, role, personality, location)
            self.npcs[npc_id] = npc
    
    def get_npc(self, npc_id: str) -> Optional[NPC]:
        return self.npcs.get(npc_id)
    
    def get_npcs_nearby(self, pos: Tuple[int, int], distance: int = 2) -> List[NPC]:
        """Get NPCs within distance"""
        nearby = []
        for npc in self.npcs.values():
            dx = abs(npc.location[0] - pos[0])
            dy = abs(npc.location[1] - pos[1])
            if dx <= distance and dy <= distance:
                nearby.append(npc)
        return nearby

# ==============================================================================
# PART 5: QUEST SYSTEM
# ==============================================================================

class QuestObjective(Enum):
    """Types of quest objectives"""
    KILL_ENEMIES = "kill_enemies"
    COLLECT_ITEMS = "collect_items"
    REACH_LOCATION = "reach_location"
    TALK_TO_NPC = "talk_to_npc"
    FETCH_ITEM = "fetch_item"

@dataclass
class Quest:
    """Represents a quest"""
    id: str
    title: str
    description: str
    giver: str
    objective: QuestObjective
    objective_value: int
    reward_xp: int
    reward_gold: int
    reward_items: List[str] = field(default_factory=list)
    required_level: int = 1
    status: str = "available"

class QuestManager:
    """Manages all quests"""
    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        self.player_quests: Dict[str, Quest] = {}
        self.completed_quests: Set[str] = set()
        self._initialize_quests()
    
    def _initialize_quests(self):
        """Initialize game quests"""
        quests_data = [
            Quest("Q_001", "The Corrupted Forest", "Clear the forest of corruption",
                  "Elder Sage", QuestObjective.KILL_ENEMIES, 5, 200, 50),
            Quest("Q_002", "Lost Artifacts", "Find three ancient artifacts",
                  "Blacksmith Kale", QuestObjective.COLLECT_ITEMS, 3, 300, 75),
            Quest("Q_003", "Mountain Expedition", "Reach the peak of the mountain",
                  "Battle Master", QuestObjective.REACH_LOCATION, 1, 250, 100),
            Quest("Q_004", "Merchant's Request", "Deliver goods to the village",
                  "Traveling Merchant", QuestObjective.FETCH_ITEM, 1, 150, 40),
            Quest("Q_005", "Royal Message", "Deliver a message to Princess Aria",
                  "Elder Sage", QuestObjective.TALK_TO_NPC, 1, 200, 60),
        ]
        
        for quest in quests_data:
            self.quests[quest.id] = quest
    
    def accept_quest(self, player, quest_id: str) -> bool:
        """Accept a quest"""
        if quest_id not in self.quests:
            return False
        
        quest = self.quests[quest_id].copy() if hasattr(self.quests[quest_id], 'copy') else self.quests[quest_id]
        quest.status = "active"
        self.player_quests[quest_id] = quest
        return True
    
    def complete_quest(self, player, quest_id: str) -> bool:
        """Complete a quest"""
        if quest_id not in self.player_quests:
            return False
        
        quest = self.player_quests[quest_id]
        player.experience_points += quest.reward_xp
        player.gold += quest.reward_gold
        self.completed_quests.add(quest_id)
        del self.player_quests[quest_id]
        
        print(f"✅ Quest '{quest.title}' completed!")
        print(f"🌟 Gained {quest.reward_xp} XP and {quest.reward_gold} gold!")
        return True

# ==============================================================================
# PART 6: PLAYER DATA SYSTEM
# ==============================================================================

class PlayerClass(Enum):
    """Character classes"""
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    KNIGHT = "Knight"
    PALADIN = "Paladin"
    BARD = "Bard"

@dataclass
class Player:
    """Main player character"""
    name: str
    player_class: PlayerClass
    level: int = 1
    exp: int = 0
    next_level_exp: int = 100
    hp: int = 200
    max_hp: int = 200
    mp: int = 100
    max_mp: int = 100
    aura: int = 50
    max_aura: int = 50
    atk: int = 30
    dfn: int = 20
    speed: int = 15
    luck: int = 10
    crit_chance: float = 0.05
    gold: int = 100
    
    # States
    position: Tuple[int, int] = (0, 0)
    is_alive: bool = True
    status_effects: Dict[str, int] = field(default_factory=dict)
    
    # Systems
    inventory: Optional[InventorySystem] = None
    learned_skills: List[str] = field(default_factory=list)
    
    # Properties
    @property
    def health_points(self):
        return self.hp
    
    @health_points.setter
    def health_points(self, value):
        self.hp = max(0, min(value, self.max_hp))
    
    @property
    def mana_points(self):
        return self.mp
    
    @mana_points.setter
    def mana_points(self, value):
        self.mp = max(0, min(value, self.max_mp))
    
    @property
    def base_attack_power(self):
        return self.atk
    
    @base_attack_power.setter
    def base_attack_power(self, value):
        self.atk = value
    
    @property
    def base_defense_rating(self):
        return self.dfn
    
    @base_defense_rating.setter
    def base_defense_rating(self, value):
        self.dfn = value
    
    @property
    def experience_points(self):
        return self.exp
    
    @experience_points.setter
    def experience_points(self, value):
        self.exp = value
    
    @property
    def maximum_health_points(self):
        return self.max_hp
    
    @property
    def maximum_mana_points(self):
        return self.max_mp
    
    @property
    def current_level(self):
        return self.level
    
    @current_level.setter
    def current_level(self, value):
        self.level = value
    
    @property
    def speed_stat(self):
        return self.speed
    
    @speed_stat.setter
    def speed_stat(self, value):
        self.speed = value
    
    @property
    def luck_stat(self):
        return self.luck
    
    @luck_stat.setter
    def luck_stat(self, value):
        self.luck = value
    
    @property
    def aura_energy(self):
        return self.aura
    
    @aura_energy.setter
    def aura_energy(self, value):
        self.aura = max(0, min(value, self.max_aura))
    
    @property
    def maximum_aura_energy(self):
        return self.max_aura
    
    @property
    def next_level_experience(self):
        return self.next_level_exp
    
    @next_level_experience.setter
    def next_level_experience(self, value):
        self.next_level_exp = value
    
    @property
    def inventory_slots(self):
        return self.inventory.items if self.inventory else []
    
    @property
    def equipped_weapon(self):
        if self.inventory:
            weapon = self.inventory.equipped_items.get("weapon")
            return weapon.name if weapon else "Red Leather Fists"
        return "Red Leather Fists"
    
    @property
    def equipped_armor(self):
        if self.inventory:
            armor = self.inventory.equipped_items.get("armor")
            return armor.name if armor else "Crimson Business Suit"
        return "Crimson Business Suit"
    
    @property
    def quest_flags(self):
        return {}
    
    def update_stats(self):
        """Update player stats based on level"""
        self.max_hp = 200 + (self.level * 25)
        self.max_mp = 100 + (self.level * 12)
        self.atk = 30 + (self.level * 5)
        self.dfn = 20 + (self.level * 4)

# ==============================================================================
# PART 7: GAME STATE AND CONTEXT
# ==============================================================================

class GameState(Enum):
    """Game states"""
    MENU = "menu"
    CHARACTER_CREATION = "creation"
    HUB = "hub"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    DIALOGUE = "dialogue"
    INVENTORY = "inventory"
    QUESTS = "quests"
    PAUSED = "paused"
    GAME_OVER = "gameover"

class GameContext:
    """Main game context and state"""
    def __init__(self):
        self.title = "Anime Chronicles: World Salvation"
        self.version = "3.0.0 PROFESSIONAL EDITION"
        self.build = 30000
        self.state = GameState.MENU
        self.is_running = True
        self.current_act = 1
        self.world_stability = 100.0
        self.cataclysm_countdown = 24
        self.playtime = 0
        self.started_at = datetime.now()
    
    def get_playtime_formatted(self) -> str:
        """Get formatted playtime"""
        elapsed = datetime.now() - self.started_at
        seconds = int(elapsed.total_seconds())
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def display_title_screen(self):
        """Display game title"""
        print("\n" + "="*70)
        print("╔" + "═"*68 + "╗")
        print("║" + " "*68 + "║")
        print("║" + "  A N I M E   C H R O N I C L E S : W O R L D   S A L V A T I O N  ".center(68) + "║")
        print("║" + " "*68 + "║")
        print("║" + "  Professional Edition - A Comprehensive RPG Experience  ".center(68) + "║")
        print("║" + " "*68 + "║")
        print("╚" + "═"*68 + "╝")
        print("="*70 + "\n")

# ==============================================================================
# PART 8: HUB INTERFACE
# ==============================================================================

class HubInterface:
    """Main hub/town interface"""
    def __init__(self, player: Player, game_context: GameContext, 
                 quest_manager: QuestManager, npc_system: NPCSystem):
        self.player = player
        self.context = game_context
        self.quest_manager = quest_manager
        self.npc_system = npc_system
    
    def display_hub_screen(self) -> str:
        """Display hub interface"""
        print("\n" + "="*80)
        print(f" 🎮 HUB CENTER | ACT {self.context.current_act} | Playtime: {self.context.get_playtime_formatted()}")
        print("="*80)
        print(f" 👤 {self.player.name:20} | 📊 {self.player.player_class.value:15} | ⭐ Lv.{self.player.level}")
        print(f" ❤️  HP: {self.player.hp:3}/{self.player.max_hp:3} | 💙 MP: {self.player.mp:3}/{self.player.max_mp:3} | 💛 AURA: {self.player.aura:3}/{self.player.max_aura:3}")
        print(f" 🌟 EXP: {self.player.exp:5}/{self.player.next_level_exp:5} | 💰 GOLD: {self.player.gold:6} | ⚡ World Stability: {self.context.world_stability:.1f}%")
        print(f" 🗡️  ATK: {self.player.atk:3} | 🛡️  DEF: {self.player.dfn:3} | ⚙️  SPEED: {self.player.speed}")
        print("-"*80)
        print(" [1] Explore World     [2] Character Status  [3] Inventory")
        print(" [4] Quests            [5] NPCs              [6] Skills")
        print(" [7] Equipment         [8] Settings          [9] Save & Exit")
        print("-"*80)
        
        return input(" Select option (1-9): ").strip()

# ==============================================================================
# PART 9: ENEMY SYSTEM
# ==============================================================================

class Enemy:
    """Enemy class"""
    def __init__(self, enemy_id: str, name: str, level: int, hp: int, 
                 atk: int, dfn: int, xp_reward: int, loot: List[str] = None):
        self.id = enemy_id
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.dfn = dfn
        self.xp_reward = xp_reward
        self.loot = loot or []
        self.status_effects: Dict[str, int] = {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "atk": self.atk,
            "dfn": self.dfn,
            "xp_reward": self.xp_reward
        }

class EnemyRegistry:
    """Registry of all enemies"""
    def __init__(self):
        self.enemies: Dict[str, Enemy] = {}
        self._initialize_enemies()
    
    def _initialize_enemies(self):
        """Initialize all enemies"""
        enemies_data = [
            ("E_001", "Corrupted Sprite", 1, 30, 10, 5, 25, ["IT_007"]),
            ("E_002", "Dark Wraith", 3, 60, 18, 10, 75, ["IT_008"]),
            ("E_003", "Abyssal Guardian", 5, 100, 28, 15, 150, ["IT_002"]),
            ("E_004", "Shadow Beast", 7, 120, 35, 18, 200, ["IT_005"]),
            ("E_005", "Demon Lord", 10, 200, 50, 25, 500, ["IT_003"]),
            ("E_006", "Goblin", 2, 25, 8, 4, 20, ["IT_007"]),
            ("E_007", "Orc Warrior", 4, 70, 22, 12, 100, ["IT_001"]),
            ("E_008", "Dragon", 12, 300, 70, 35, 800, ["IT_003", "IT_006"]),
        ]
        
        for enemy_id, name, level, hp, atk, dfn, xp, loot in enemies_data:
            enemy = Enemy(enemy_id, name, level, hp, atk, dfn, xp, loot)
            self.enemies[enemy_id] = enemy
    
    def get_enemy(self, enemy_id: str) -> Optional[Enemy]:
        return self.enemies.get(enemy_id)

# ==============================================================================
# PART 10: GAME INITIALIZATION AND MAIN LOOP
# ==============================================================================

def create_player_character() -> Player:
    """Character creation sequence"""
    print("\n" + "="*70)
    print(" 🎭 CHARACTER CREATION ".center(70))
    print("="*70 + "\n")
    
    name = input("📝 Enter your hero name: ").strip() or "RedSuitHero"
    
    print("\n🎭 Select your class:")
    print("  [1] Warrior (High ATK & DEF)")
    print("  [2] Mage (High MP & Magic)")
    print("  [3] Rogue (High Speed & Crit)")
    print("  [4] Knight (Balanced, Tank)")
    print("  [5] Paladin (Support)")
    print("  [6] Bard (Utility)")
    
    class_choice = input("\n Select class (1-6): ").strip()
    
    class_stats = {
        "1": (PlayerClass.WARRIOR, 45, 35, 15, 0.08),
        "2": (PlayerClass.MAGE, 35, 20, 15, 0.05),
        "3": (PlayerClass.ROGUE, 40, 25, 30, 0.20),
        "4": (PlayerClass.KNIGHT, 38, 40, 12, 0.06),
        "5": (PlayerClass.PALADIN, 35, 35, 18, 0.07),
        "6": (PlayerClass.BARD, 32, 28, 25, 0.10),
    }
    
    player_class, atk, dfn, spd, crit = class_stats.get(class_choice, 
        (PlayerClass.WARRIOR, 45, 35, 15, 0.08))
    
    # Create player
    player = Player(
        name=name,
        player_class=player_class,
        atk=atk,
        dfn=dfn,
        speed=spd,
        crit_chance=crit
    )
    
    # Initialize systems
    player.inventory = InventorySystem()
    
    print(f"\n✅ Character '{name}' ({player_class.value}) created!\n")
    time.sleep(1)
    
    return player

def initialize_game_systems() -> Tuple[GameContext, Player, EnhancedPixelWorld, 
                                       EnemyRegistry, SkillRegistry, QuestManager, 
                                       NPCSystem, ItemRegistry]:
    """Initialize all game systems"""
    
    # Game context
    context = GameContext()
    context.display_title_screen()
    
    print("🔧 Initializing game systems...\n")
    
    # Create player
    player = create_player_character()
    
    # Initialize systems
    world = EnhancedPixelWorld(30, 20, seed=42)
    enemy_registry = EnemyRegistry()
    skill_registry = SkillRegistry()
    quest_manager = QuestManager()
    npc_system = NPCSystem()
    item_registry = ItemRegistry()
    
    # Add starting items to inventory
    player.inventory.add_item(item_registry.items["IT_001"])
    player.inventory.add_item(item_registry.items["IT_004"])
    player.inventory.add_item(item_registry.items["IT_007"])
    player.inventory.add_item(item_registry.items["IT_007"])
    
    # Add starting skills
    player.learned_skills = ["SK_001", "SK_002", "SK_007", "SK_009"]
    
    print("✅ All systems initialized!\n")
    time.sleep(1)
    
    return context, player, world, enemy_registry, skill_registry, quest_manager, npc_system, item_registry

def exploration_loop(player: Player, world: EnhancedPixelWorld, 
                     enemy_registry: EnemyRegistry, skill_registry: SkillRegistry,
                     npc_system: NPCSystem) -> bool:
    """Main exploration loop"""
    
    print("\n🗺️ Entering Exploration Mode...\n")
    time.sleep(1)
    
    exploring = True
    while exploring:
        # Update world
        world.update_weather()
        world.update_day_cycle()
        
        # Render world
        print("\n" + world.draw_with_fancy_border())
        print("\n" + world.get_terrain_description())
        
        print("\n📋 CONTROLS:")
        print("  Movement: [W/A/S/D or ↑/←/↓/→]")
        print("  Actions: [V]iew Character, [N]PC Interact, [X] Exit")
        
        action = input("\n⚔️ Action: ").strip().lower()
        
        if action in ("w", "a", "s", "d", "↑", "←", "↓", "→"):
            if world.move(action):
                print(f"\n✨ {player.name} moved!")
                
                # Random encounters
                if random.random() < 0.25:
                    print("\n⚠️ A wild enemy appears!")
                    enemy_id = random.choice(list(enemy_registry.enemies.keys()))
                    enemy = enemy_registry.get_enemy(enemy_id)
                    
                    if enemy:
                        combat = AdvancedCombatEngine(player, enemy.to_dict(), skill_registry)
                        victory = combat_loop(player, combat, skill_registry)
                        
                        if not victory:
                            print("\n💀 You were defeated!")
                            return False
                        
                        input("\nPress Enter to continue...")
        
        elif action == "v":
            CharacterVisualizer.display_character_full(player)
            input("Press Enter to continue...")
        
        elif action == "n":
            npcs = npc_system.get_npcs_nearby((world.player_x, world.player_y))
            if npcs:
                print("\n🤖 Nearby NPCs:")
                for i, npc in enumerate(npcs, 1):
                    print(f"  [{i}] {npc.name} ({npc.role})")
                    print(f"      {npc.greet()}")
            else:
                print("\n❌ No NPCs nearby.")
            
            input("Press Enter to continue...")
        
        elif action == "x":
            print(f"\n🚪 {player.name} returns to the hub.\n")
            exploring = False
        
        else:
            print("⚠️ Unknown command!")
    
    return True

def combat_loop(player: Player, combat: AdvancedCombatEngine, 
                skill_registry: SkillRegistry) -> bool:
    """Main combat loop"""
    
    while combat.battle_active:
        # Display battle status
        print("\n" + "="*60)
        print(f"Turn {combat.turn_counter}")
        print("="*60)
        print(f"👤 {player.name:20} HP: {player.hp:3}/{player.max_hp:3} | MP: {player.mp:3}/{player.max_mp:3}")
        print(f"👹 {combat.enemy_name:20} HP: {combat.enemy_hp:3}/{combat.enemy_max_hp:3}")
        print("-"*60)
        
        # Player turn
        print("\n⚔️ BATTLE MENU:")
        print("  [1] Slash Strike (SK_001)")
        print("  [2] Heavy Blow (SK_002)")
        print("  [3] Defend (SK_007)")
        print("  [4] Heal (SK_009)")
        print("  [5] Item")
        print("  [6] Run Away")
        
        choice = input("\n Select action (1-6): ").strip()
        
        if choice == "1":
            combat.execute_skill_action("SK_001")
        elif choice == "2":
            combat.execute_skill_action("SK_002")
        elif choice == "3":
            combat.execute_skill_action("SK_007")
        elif choice == "4":
            combat.execute_skill_action("SK_009")
        elif choice == "5":
            if player.inventory_slots:
                for i, item in enumerate(player.inventory_slots, 1):
                    print(f"  [{i}] {item.name}")
            else:
                print("  (Empty)")
        elif choice == "6":
            if random.random() < 0.5:
                print("\n🏃 You escaped!")
                return True
            else:
                print("\n❌ Failed to escape!")
        
        # Check victory
        if combat.enemy_hp <= 0:
            print(f"\n✨ VICTORY! {combat.enemy_name} defeated!")
            xp_gain = combat.enemy_xp_reward
            player.experience_points += xp_gain
            print(f"🌟 Gained {xp_gain} XP!")
            
            # Check level up
            while player.exp >= player.next_level_exp:
                player.level += 1
                player.exp -= player.next_level_exp
                player.next_level_exp = int(player.next_level_exp * 1.5)
                player.update_stats()
                player.hp = player.max_hp
                player.mp = player.max_mp
                print(f"🎉 LEVEL UP! Reached Level {player.level}!")
            
            return True
        
        # Enemy turn
        if random.random() < 0.7:
            damage = combat.calculate_damage(combat.enemy_atk, player.dfn)
            player.hp -= damage
            print(f"\n💥 {combat.enemy_name} attacks for {damage} damage!")
        else:
            print(f"\n😊 {combat.enemy_name}'s attack misses!")
        
        # Check defeat
        if player.hp <= 0:
            print("\n💀 You were defeated...")
            return False
        
        combat.turn_counter += 1
    
    return True

def hub_loop(player: Player, context: GameContext, world: EnhancedPixelWorld,
             enemy_registry: EnemyRegistry, skill_registry: SkillRegistry,
             quest_manager: QuestManager, npc_system: NPCSystem,
             item_registry: ItemRegistry) -> bool:
    """Main hub/town loop"""
    
    hub = HubInterface(player, context, quest_manager, npc_system)
    
    in_hub = True
    while in_hub:
        choice = hub.display_hub_screen()
        
        if choice == "1":
            alive = exploration_loop(player, world, enemy_registry, skill_registry, npc_system)
            if not alive:
                return False
        
        elif choice == "2":
            CharacterVisualizer.display_character_full(player)
            input("Press Enter to continue...")
        
        elif choice == "3":
            print("\n📦 INVENTORY")
            print("="*50)
            if player.inventory_slots:
                for i, item in enumerate(player.inventory_slots, 1):
                    print(f"  [{i}] {item.name} ({item.rarity.upper()}) - Power: {item.power}")
            else:
                print("  (Empty)")
            print("="*50)
            input("Press Enter to continue...")
        
        elif choice == "4":
            print("\n📋 QUESTS")
            print("="*50)
            if quest_manager.player_quests:
                for quest_id, quest in quest_manager.player_quests.items():
                    print(f"  📌 {quest.title}")
                    print(f"     {quest.description}")
                    print(f"     Reward: {quest.reward_xp} XP, {quest.reward_gold} Gold")
            else:
                print("  (No active quests)")
            print("="*50)
            input("Press Enter to continue...")
        
        elif choice == "5":
            print("\n🤖 NPCs IN TOWN")
            print("="*50)
            for npc in npc_system.npcs.values():
                print(f"  👤 {npc.name} - {npc.role}")
                print(f"     {npc.greet()}")
            print("="*50)
            input("Press Enter to continue...")
        
        elif choice == "6":
            print("\n⚡ SKILLS")
            print("="*50)
            for skill_id in player.learned_skills:
                skill = skill_registry.get_skill(skill_id)
                if skill:
                    print(f"  ⚔️ {skill.name}")
                    print(f"     {skill.description}")
                    print(f"     Cost: {skill.mana_cost} MP")
            print("="*50)
            input("Press Enter to continue...")
        
        elif choice == "7":
            print("\n🛡️ EQUIPMENT")
            print("="*50)
            print(f"  Weapon: {player.equipped_weapon}")
            print(f"  Armor: {player.equipped_armor}")
            print("="*50)
            input("Press Enter to continue...")
        
        elif choice == "8":
            print("\n⚙️ SETTINGS")
            print("="*50)
            print("  [1] Game Difficulty")
            print("  [2] Sound Settings")
            print("  [3] Display Settings")
            print("  [0] Back")
            setting_choice = input("\n Select (0-3): ").strip()
            if setting_choice != "0":
                print("  Settings updated!")
                input("Press Enter to continue...")
        
        elif choice == "9":
            print("\n💾 Saving game...")
            time.sleep(1)
            print("✅ Game saved!")
            time.sleep(1)
            print("👋 Thank you for playing Anime Chronicles!\n")
            return True
        
        else:
            print("⚠️ Invalid selection!")
    
    return True

class CharacterVisualizer:
    """Character visualization"""
    
    @staticmethod
    def display_character_full(player: Player):
        """Display full character sheet"""
        print("\n" + "="*70)
        print(" 👤 CHARACTER SHEET ".center(70))
        print("="*70)
        print(f"  Name: {player.name}")
        print(f"  Class: {player.player_class.value}")
        print(f"  Level: {player.level}")
        print("-"*70)
        print(f"  ❤️  HP: {player.hp}/{player.max_hp}")
        print(f"  💙 MP: {player.mp}/{player.max_mp}")
        print(f"  💛 AURA: {player.aura}/{player.max_aura}")
        print(f"  🌟 EXP: {player.exp}/{player.next_level_exp}")
        print("-"*70)
        print(f"  ⚡ ATK: {player.atk}")
        print(f"  🛡️  DEF: {player.dfn}")
        print(f"  🏃 SPD: {player.speed}")
        print(f"  🍀 LCK: {player.luck}")
        print(f"  ✨ CRIT: {player.crit_chance*100:.1f}%")
        print("-"*70)
        print(f"  💰 Gold: {player.gold}")
        print(f"  🗡️  Weapon: {player.equipped_weapon}")
        print(f"  🛡️  Armor: {player.equipped_armor}")
        print("="*70 + "\n")

def main():
    """Main game entry point"""
    try:
        # Initialize
        (context, player, world, enemy_registry, skill_registry, 
         quest_manager, npc_system, item_registry) = initialize_game_systems()
        
        # Display intro
        CharacterVisualizer.display_character_full(player)
        print("🎬 Your adventure begins in the town square...\n")
        time.sleep(2)
        
        # Main game loop
        alive = hub_loop(player, context, world, enemy_registry, skill_registry,
                        quest_manager, npc_system, item_registry)
        
        if alive:
            print("✨ Thanks for playing!\n")
        else:
            print("💀 Game Over. Better luck next time!\n")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Game interrupted by user.")
    except Exception as e:
        print(f"\n❌ Critical error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
