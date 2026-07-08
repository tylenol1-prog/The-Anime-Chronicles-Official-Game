#!/usr/bin/env python3
# ==============================================================================
# ANIME CHRONICLES: WORLD SALVATION SYSTEM
# MAIN GAME ENGINE WITH CHARACTER VISUALIZATION
# ==============================================================================

import sys
import os
import random
import time

# ============================================================================
# PART 0: CHARACTER VISUALIZATION SYSTEM
# ============================================================================

class CharacterVisualizer:
    """Renders the player character as ASCII art"""
    
    RED_SUIT_CHARACTER = [
        "    🧑    ",
        "   ╱█╲   ",
        "   █ █   ",
        "   ╲█╱   ",
        "    ║    ",
        "   ╱ ╲   ",
    ]
    
    RED_SUIT_CHARACTER_SPRITE = [
        "   ╔═╗   ",
        "   ║O║   ",
        "  ╔╩█╩╗  ",
        "  ║ █ ║  ",
        "  ╚═╪═╝  ",
        "   ╱ ╲   ",
    ]
    
    DETAILED_CHARACTER = [
        "    ◉     ",
        "   ╱▓╲    ",
        "   ▓▓▓▓   ",
        "  ╱▓███╲  ",
        "  ║ ▓▓▓ ║ ",
        "  ╚═╪═╪═╝ ",
        "   ╱ ╲    ",
        "  ▓   ▓   ",
    ]
    
    @staticmethod
    def render_character():
        """Return ASCII art of red-suited character"""
        return CharacterVisualizer.RED_SUIT_CHARACTER_SPRITE
    
    @staticmethod
    def display_character_full(player):
        """Display full character status with visual"""
        print("\n" + "="*50)
        print("            YOUR CHARACTER")
        print("="*50)
        
        for line in CharacterVisualizer.render_character():
            print(line)
        
        print("-"*50)
        print(f"  Name: {player.player_name}")
        print(f"  Class: {player.chosen_class}")
        print(f"  Weapon: {player.equipped_weapon}")
        print(f"  Armor: {player.equipped_armor}")
        print("="*50 + "\n")

# ============================================================================
# PART 1: WORLD MAP AND MOVEMENT SYSTEM
# ============================================================================

class PixelWorld:
    """2D tile-based world with character movement"""
    
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.player_x = width // 2
        self.player_y = height // 2
        self.tiles = {}
        self.generate_world()
        self.visited_zones = set()
    
    def generate_world(self):
        """Generate random world terrain"""
        for y in range(self.height):
            for x in range(self.width):
                rand = random.random()
                if rand < 0.1:
                    self.tiles[(x, y)] = "🌲"  # Forest
                elif rand < 0.15:
                    self.tiles[(x, y)] = "🏔"   # Mountain
                elif rand < 0.2:
                    self.tiles[(x, y)] = "💧"   # Water
                elif rand < 0.25:
                    self.tiles[(x, y)] = "🏛"   # Ruins
                else:
                    self.tiles[(x, y)] = "·"    # Grass
    
    def draw(self):
        """Render the game world with player character"""
        print("\n" + "╔" + "═" * (self.width * 2 - 1) + "╗")
        
        for y in range(self.height):
            print("║", end="")
            for x in range(self.width):
                if x == self.player_x and y == self.player_y:
                    print("🔴", end="")  # Red character/suit indicator
                else:
                    tile = self.tiles.get((x, y), "·")
                    print(tile, end="")
            print("║")
        
        print("╚" + "═" * (self.width * 2 - 1) + "╝")
        print(f"Position: ({self.player_x}, {self.player_y}) | Map: {self.width}x{self.height}")
    
    def move(self, direction):
        """Move player in specified direction"""
        old_x, old_y = self.player_x, self.player_y
        
        if direction == "w" or direction == "↑":
            self.player_y = max(0, self.player_y - 1)
        elif direction == "s" or direction == "↓":
            self.player_y = min(self.height - 1, self.player_y + 1)
        elif direction == "a" or direction == "←":
            self.player_x = max(0, self.player_x - 1)
        elif direction == "d" or direction == "→":
            self.player_x = min(self.width - 1, self.player_x + 1)
        
        moved = (old_x != self.player_x or old_y != self.player_y)
        return moved
    
    def get_terrain_description(self):
        """Get description of current terrain"""
        terrain = self.tiles.get((self.player_x, self.player_y), "·")
        descriptions = {
            "🌲": "You stand in a dense forest. Shadows dance between the trees.",
            "🏔": "Towering mountains loom overhead. A cold wind blows through.",
            "💧": "You wade through water. Something moves beneath the surface...",
            "🏛": "Ancient ruins surround you. A sense of history fills the air.",
            "·": "Grassland stretches endlessly. The path ahead is clear."
        }
        return descriptions.get(terrain, "You are in an unknown location.")

# ============================================================================
# PART 2: GAME CORE AND REGISTRATION SYSTEMS
# ============================================================================

class GameContext:
    def __init__(self):
        self.game_title = "Anime Chronicles: World Salvation"
        self.version = "2.5.0 CHARACTER EDITION"
        self.build_number = 10250
        self.max_lines_target = 10000
        self.is_running = True
        self.system_ready = False
        self.current_act = 1
        self.world_stability_index = 100.0
        self.cataclysm_countdown_hours = 24
        
    def display_boot_logo(self):
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║     A N I M E   C H R O N I C L E S : W O R L D   S A L V A T I O N  ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║ System Version: {self.version:<30} Build: {self.build_number:<6} ║")
        print("║ Loading character visualization systems...                     ║")
        print("╚════════════════════════════════════════════════════════════════╝")

class SystemLogger:
    def __init__(self, context):
        self.context = context
        self.logs = []
        
    def log_info(self, message):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [INFO] {message}"
        self.logs.append(log_entry)
        print(log_entry)
        
    def log_warning(self, message):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [WARN] {message}"
        self.logs.append(log_entry)
        print(log_entry)
        
    def log_critical(self, message):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [CRIT] {message}"
        self.logs.append(log_entry)
        print(log_entry)

class PlayerDataStructure:
    def __init__(self):
        self.player_name = "DefaultHero"
        self.chosen_class = "None"
        self.current_level = 1
        self.experience_points = 0
        self.next_level_experience = 100
        self.health_points = 200
        self.maximum_health_points = 200
        self.mana_points = 100
        self.maximum_mana_points = 100
        self.aura_energy = 50
        self.maximum_aura_energy = 50
        self.base_attack_power = 30
        self.base_defense_rating = 20
        self.speed_stat = 15
        self.luck_stat = 10
        self.crit_chance = 0.05
        self.equipped_weapon = "Red Leather Fists"
        self.equipped_armor = "Crimson Business Suit"
        self.inventory_slots = []
        self.unlocked_skills = []
        self.quest_flags = {}
        
    def update_stats(self):
        self.maximum_health_points = 200 + (self.current_level * 25)
        self.maximum_mana_points = 100 + (self.current_level * 12)
        self.base_attack_power = 30 + (self.current_level * 5)
        self.base_defense_rating = 20 + (self.current_level * 4)

class ItemRegistry:
    def __init__(self):
        self.items = {}
        
    def register_item(self, item_id, name, item_type, power, value, description):
        self.items[item_id] = {
            "name": name,
            "type": item_type,
            "power": power,
            "value": value,
            "description": description
        }

class EnemyRegistry:
    def __init__(self):
        self.enemies = {}
        
    def register_enemy(self, enemy_id, name, level, hp, atk, dfn, xp_reward):
        self.enemies[enemy_id] = {
            "name": name,
            "level": level,
            "hp": hp,
            "max_hp": hp,
            "atk": atk,
            "dfn": dfn,
            "xp_reward": xp_reward
        }

class ZoneRegistry:
    def __init__(self):
        self.zones = {}
        
    def register_zone(self, zone_id, name, danger_rating, primary_element, narrative_intro):
        self.zones[zone_id] = {
            "name": name,
            "danger": danger_rating,
            "element": primary_element,
            "intro": narrative_intro,
            "cleared": False
        }

# ============================================================================
# PART 3: COMBAT ENGINE
# ============================================================================

class CombatEngine:
    def __init__(self, player, active_enemy_data):
        self.player = player
        self.enemy_name = active_enemy_data["name"]
        self.enemy_level = active_enemy_data["level"]
        self.enemy_hp = active_enemy_data["hp"]
        self.enemy_max_hp = active_enemy_data["max_hp"]
        self.enemy_atk = active_enemy_data["atk"]
        self.enemy_dfn = active_enemy_data["dfn"]
        self.enemy_xp_reward = active_enemy_data["xp_reward"]
        self.turn_counter = 1
        self.battle_active = True
        self.player_defense_buff = False

    def calculate_damage_output(self, raw_atk, target_dfn, is_critical=False):
        base_damage = max(1, raw_atk - (target_dfn // 2))
        variance = random.randint(-3, 5)
        total_damage = max(1, base_damage + variance)
        if is_critical:
            total_damage = int(total_damage * 1.5)
            print("✨ CRITICAL HIT! The cosmic alignment shatters the enemy defenses!")
        return total_damage

    def execute_player_turn(self):
        print(f"\n--- TURN {self.turn_counter} : {self.player.player_name}'s Action Phase ---")
        print(f"[{self.player.player_name}] HP: {self.player.health_points}/{self.player.maximum_health_points} | MP: {self.player.mana_points}/{self.player.maximum_mana_points}")
        print(f"[{self.enemy_name}] HP: {self.enemy_hp}/{self.enemy_max_hp} (Lv.{self.enemy_level})")
        print("\nBattle Menu:")
        print("1) Slash Strike      - Standard physical blow")
        print("2) Special Technique - High-potency attack")
        print("3) Tactical Guard    - Reduce incoming damage")
        print("4) Use Item          - Access inventory")
        
        choice = input("Select action (1-4): ").strip()
        self.player_defense_buff = False

        if choice == "1":
            is_crit = random.random() < self.player.crit_chance
            dmg = self.calculate_damage_output(self.player.base_attack_power, self.enemy_dfn, is_crit)
            self.enemy_hp -= dmg
            self.player.aura_energy = min(self.player.maximum_aura_energy, self.player.aura_energy + 5)
            print(f"⚔️ You strike {self.enemy_name} for {dmg} damage!")
        
        elif choice == "2":
            if self.player.mana_points >= 20:
                self.player.mana_points -= 20
                dmg = self.calculate_damage_output(self.player.base_attack_power * 2, self.enemy_dfn, True)
                self.enemy_hp -= dmg
                print(f"💥 You unleash a devastating technique for {dmg} damage!")
            else:
                print("❌ Not enough mana! Defending instead.")
                self.player_defense_buff = True

        elif choice == "3":
            self.player_defense_buff = True
            print(f"🛡️ {self.player.player_name} takes a defensive stance.")

        elif choice == "4":
            if not self.player.inventory_slots:
                print("❌ No items in inventory!")
                dmg = self.calculate_damage_output(self.player.base_attack_power // 2, self.enemy_dfn)
                self.enemy_hp -= dmg
            else:
                print("\nInventory:")
                for index, item in enumerate(self.player.inventory_slots):
                    print(f"{index + 1}) {item}")
                item_choice = input("Select item (number): ").strip()
                
                try:
                    chosen_idx = int(item_choice) - 1
                    if 0 <= chosen_idx < len(self.player.inventory_slots):
                        consumed_item = self.player.inventory_slots.pop(chosen_idx)
                        self.player.health_points = min(self.player.maximum_health_points, self.player.health_points + 60)
                        print(f"🧪 Used {consumed_item}. Recovered 60 HP!")
                except:
                    print("⚠️ Invalid selection.")

    def execute_enemy_turn(self):
        if self.enemy_hp <= 0:
            return

        print(f"\n--- {self.enemy_name}'s Counter Phase ---")
        dmg = self.calculate_damage_output(self.enemy_atk, self.player.base_defense_rating)
        
        if self.player_defense_buff:
            dmg = dmg // 2
            print("🛡️ Your defensive stance blocks half the damage!")

        self.player.health_points -= dmg
        print(f"💥 {self.enemy_name} attacks for {dmg} damage!")

    def process_battle_loop(self):
        while self.battle_active:
            self.execute_player_turn()
            if self.enemy_hp <= 0:
                print(f"\n✨ VICTORY! {self.enemy_name} has been defeated!")
                self.player.experience_points += self.enemy_xp_reward
                print(f"🌟 Gained {self.enemy_xp_reward} experience points!")
                self.check_level_up_parameters()
                self.battle_active = False
                return True

            self.execute_enemy_turn()
            if self.player.health_points <= 0:
                print("\n💀 You were defeated...")
                self.battle_active = False
                return False
                
            self.turn_counter += 1

    def check_level_up_parameters(self):
        if self.player.experience_points >= self.player.next_level_experience:
            self.player.current_level += 1
            self.player.experience_points -= self.player.next_level_experience
            self.player.next_level_experience = int(self.player.next_level_experience * 1.5)
            self.player.update_stats()
            self.player.health_points = self.player.maximum_health_points
            self.player.mana_points = self.player.maximum_mana_points
            print(f"🎉 LEVEL UP! {self.player.player_name} reached Level {self.player.current_level}!")

class HubInterface:
    def __init__(self, player, world_context):
        self.player = player
        self.context = world_context

    def show_dashboard(self):
        print("\n" + "="*70)
        print(f" MASTER HUB | ACT: {self.context.current_act} | WORLD STABILITY: {self.context.world_stability_index:.1f}%")
        print(f" ⏱️  CATACLYSM COUNTDOWN: {self.context.cataclysm_countdown_hours} HOURS")
        print("="*70)
        print(f" 🧑 Hero: {self.player.player_name} | 📊 Class: {self.player.chosen_class}")
        print(f" 📈 Level: {self.player.current_level} | ⚡ EXP: {self.player.experience_points}/{self.player.next_level_experience}")
        print(f" ❤️  HP: {self.player.health_points}/{self.player.maximum_health_points} | 💙 MP: {self.player.mana_points}/{self.player.maximum_mana_points}")
        print(f" 🗡️  Weapon: {self.player.equipped_weapon} | 🛡️  Armor: {self.player.equipped_armor}")
        print("-"*70)
        print("1) Explore World Map")
        print("2) View Character")
        print("3) Inventory")
        print("4) System Status")
        print("5) Exit Game")
        
        return input("Select option (1-5): ").strip()

# ============================================================================
# PART 4: QUEST AND NARRATIVE SYSTEMS
# ============================================================================

class QuestManager:
    def __init__(self):
        self.quests = {}
        self.active_quests = []
        self.completed_quests = []
        self.quest_chains = {}
        self.current_chapter = 1
        self.story_flags = {}
    
    def register_quest(self, quest_id, title, description, objective_type, reward_xp, reward_gold, quest_giver):
        self.quests[quest_id] = {
            "id": quest_id,
            "title": title,
            "description": description,
            "objective": objective_type,
            "reward_xp": reward_xp,
            "reward_gold": reward_gold,
            "giver": quest_giver,
            "status": "available",
            "progress": 0,
            "completion_requirement": 100
        }
    
    def accept_quest(self, player, quest_id):
        if quest_id not in self.quests:
            return False
        
        quest = self.quests[quest_id]
        if quest_id not in player.quest_flags:
            player.quest_flags[quest_id] = {"status": "active", "progress": 0}
            self.active_quests.append(quest_id)
            return True
        return False

class NPCSystem:
    def __init__(self):
        self.npcs = {}
        self.npc_relationships = {}
    
    def register_npc(self, npc_id, name, role, personality, location_zone):
        self.npcs[npc_id] = {
            "id": npc_id,
            "name": name,
            "role": role,
            "personality": personality,
            "location": location_zone,
            "relationship_level": 0
        }
        self.npc_relationships[npc_id] = {"favor": 0, "interactions": 0}

class CataclysmSystem:
    def __init__(self, game_context):
        self.game_context = game_context
        self.cataclysm_stages = [
            {"stage": 1, "hours": 24, "corruption": 0.0, "description": "Peaceful Era"},
            {"stage": 2, "hours": 18, "corruption": 0.2, "description": "Rifts Begin to Open"},
            {"stage": 3, "hours": 12, "corruption": 0.4, "description": "Zones Under Threat"},
            {"stage": 4, "hours": 6, "corruption": 0.7, "description": "World Falling"},
            {"stage": 5, "hours": 0, "corruption": 1.0, "description": "Apocalypse"}
        ]
        self.current_stage = 1
        self.time_remaining = 24
    
    def update_cataclysm_countdown(self, hours_passed):
        self.time_remaining -= hours_passed
        self.game_context.cataclysm_countdown_hours = max(self.time_remaining, 0)

# ============================================================================
# MAIN GAME INITIALIZATION AND LOOP
# ============================================================================

def initialize_game():
    """Initialize all game systems"""
    game_context = GameContext()
    game_context.display_boot_logo()
    
    logger = SystemLogger(game_context)
    logger.log_info("Initializing player data structure...")
    
    player = PlayerDataStructure()
    player.player_name = input("\n🎭 Enter your hero name: ").strip() or "RedSuitHero"
    
    print("\n[CLASS SELECTION]")
    print("1) Warrior (High ATK, High DEF)")
    print("2) Mage (High MP, High ATK)")
    print("3) Rogue (High Speed, High Crit)")
    class_choice = input("Select class (1-3): ").strip()
    
    if class_choice == "1":
        player.chosen_class = "Warrior"
        player.base_attack_power = 45
        player.base_defense_rating = 35
    elif class_choice == "2":
        player.chosen_class = "Mage"
        player.maximum_mana_points = 200
        player.mana_points = 200
        player.base_attack_power = 35
    elif class_choice == "3":
        player.chosen_class = "Rogue"
        player.speed_stat = 30
        player.crit_chance = 0.15
    else:
        player.chosen_class = "Warrior"
    
    player.update_stats()
    logger.log_info(f"Hero {player.player_name} ({player.chosen_class}) registered!")
    
    # Initialize all game systems
    pixel_world = PixelWorld(20, 15)
    enemy_registry = EnemyRegistry()
    zone_registry = ZoneRegistry()
    quest_manager = QuestManager()
    npc_system = NPCSystem()
    cataclysm = CataclysmSystem(game_context)
    hub = HubInterface(player, game_context)
    
    # Register enemies
    enemy_registry.register_enemy("ENM_001", "Corrupted Sprite", 1, 30, 10, 5, 25)
    enemy_registry.register_enemy("ENM_002", "Dark Wraith", 3, 60, 18, 10, 75)
    enemy_registry.register_enemy("ENM_003", "Abyssal Guardian", 5, 100, 28, 15, 150)
    
    game_context.system_ready = True
    logger.log_info("Game systems initialized. Ready for adventure!")
    
    return game_context, player, logger, pixel_world, enemy_registry, hub, cataclysm

def exploration_mode(player, pixel_world, enemy_registry, hub):
    """Interactive exploration and movement mode"""
    exploring = True
    
    while exploring:
        pixel_world.draw()
        print(pixel_world.get_terrain_description())
        print("\nMovement Controls:")
        print("  W/↑ = Up    |  S/↓ = Down  |  A/← = Left  |  D/→ = Right")
        print("  V = View Character  |  L = Look Around  |  X = Exit Exploration")
        
        action = input("\nAction: ").strip().lower()
        
        if action in ("w", "s", "a", "d", "↑", "↓", "←", "→"):
            if pixel_world.move(action):
                print(f"\n✨ {player.player_name} moved in the {action} direction!")
                print(pixel_world.get_terrain_description())
                
                # Random encounter
                if random.random() < 0.3:
                    print("\n⚠️ A wild enemy appears!")
                    enemy_id = random.choice(list(enemy_registry.enemies.keys()))
                    enemy_data = enemy_registry.enemies[enemy_id].copy()
                    combat = CombatEngine(player, enemy_data)
                    victory = combat.process_battle_loop()
                    
                    if not victory:
                        return False
                    
                    input("\nPress Enter to continue exploring...")
        
        elif action == "v":
            CharacterVisualizer.display_character_full(player)
            input("Press Enter to continue...")
        
        elif action == "l":
            print(f"\n👀 {player.player_name} looks around carefully...")
            print(pixel_world.get_terrain_description())
        
        elif action == "x":
            print(f"🚪 {player.player_name} returns to the hub.")
            exploring = False
        
        else:
            print("⚠️ Unknown command. Use W/A/S/D to move, V to view character, or X to exit.")
    
    return True

def main_game_loop(game_context, player, logger, pixel_world, enemy_registry, hub, cataclysm):
    """Main game loop"""
    
    while game_context.is_running:
        if not game_context.system_ready:
            break
        
        choice = hub.show_dashboard()
        
        if choice == "1":
            print("\n🗺️  Entering Exploration Mode...")
            time.sleep(1)
            alive = exploration_mode(player, pixel_world, enemy_registry, hub)
            
            if not alive:
                print("\n[GAME OVER] Your adventure has ended...")
                game_context.is_running = False
        
        elif choice == "2":
            CharacterVisualizer.display_character_full(player)
            input("Press Enter to continue...")
        
        elif choice == "3":
            print("\n📦 INVENTORY")
            print("="*40)
            if player.inventory_slots:
                for i, item in enumerate(player.inventory_slots, 1):
                    print(f"  {i}) {item}")
            else:
                print("  (Empty)")
            print("="*40)
            input("Press Enter to continue...")
        
        elif choice == "4":
            print("\n🔧 SYSTEM STATUS")
            print("="*40)
            print(f"Hero Status: {player.player_name} Lv.{player.current_level}")
            print(f"Health: {player.health_points}/{player.maximum_health_points}")
            print(f"Cataclysm Stage: Stage {cataclysm.current_stage}")
            print(f"Time Remaining: {game_context.cataclysm_countdown_hours} hours")
            print("="*40)
            input("Press Enter to continue...")
        
        elif choice == "5":
            print("\n👋 Thank you for playing Anime Chronicles!")
            print("Saving game data...")
            time.sleep(1)
            game_context.is_running = False
        
        else:
            print("⚠️ Invalid selection.")

def main():
    """Main entry point"""
    try:
        game_context, player, logger, pixel_world, enemy_registry, hub, cataclysm = initialize_game()
        
        CharacterVisualizer.display_character_full(player)
        print("🎬 Your adventure begins...\n")
        time.sleep(2)
        
        main_game_loop(game_context, player, logger, pixel_world, enemy_registry, hub, cataclysm)
    
    except KeyboardInterrupt:
        print("\n\n[SYSTEM] Game interrupted. Shutting down...")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
