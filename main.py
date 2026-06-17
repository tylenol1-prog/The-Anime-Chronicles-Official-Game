#!/usr/bin/env python3
# ==============================================================================
# ANIME CHRONICLES: WORLD SALVATION SYSTEM
# MAIN GAME ENGINE - Orchestrates all game systems
# ==============================================================================

import sys
import os
import random
import time

# ============================================================================
# PART 1: GAME CORE AND REGISTRATION SYSTEMS
# ============================================================================

class GameContext:
    def __init__(self):
        self.game_title = "Anime Chronicles: World Salvation"
        self.version = "1.0.0"
        self.build_number = 10042
        self.max_lines_target = 10000
        self.is_running = True
        self.system_ready = False
        self.current_act = 1
        self.world_stability_index = 100.0
        self.cataclysm_countdown_hours = 24
        
    def display_boot_logo(self):
        print("======================================================================")
        print("     A N I M E   C H R O N I C L E S :   W O R L D   S A L V A T I O N")
        print("======================================================================")
        print(f" System Version: {self.version} | Build: {self.build_number} | Lines Matrix: {self.max_lines_target}")
        print(" Loading core multi-verse memory buffers...")
        print("----------------------------------------------------------------------")

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
        self.equipped_weapon = "None"
        self.equipped_armor = "None"
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
# PART 2: COMBAT ENGINE
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
        print("\nBattle Menu Mechanics:")
        print("1) Slash Strike      - Standard physical blow. Generates 5 Aura Energy.")
        print("2) Special Anime Burst - Cast unlocked specialized high-potency techniques.")
        print("3) Tactical Guard   - Half incoming enemy strike values for the next round.")
        print("4) Open Item Satchel - Access and consume restorable inventory parameters.")
        
        choice = input("Select strategic maneuver (1-4): ").strip()
        self.player_defense_buff = False

        if choice == "1":
            is_crit = random.random() < self.player.crit_chance
            dmg = self.calculate_damage_output(self.player.base_attack_power, self.enemy_dfn, is_crit)
            self.enemy_hp -= dmg
            self.player.aura_energy = min(self.player.maximum_aura_energy, self.player.aura_energy + 5)
            print(f"⚔️ You strike {self.enemy_name} for {dmg} damage points!")
        
        elif choice == "2":
            if not self.player.unlocked_skills:
                print("⚠️ System Notification: You possess no initialized dynamic skills yet. Defending instead.")
                self.player_defense_buff = True
            else:
                print("\nAvailable Special Techniques Matrix:")
                for index, skill in enumerate(self.player.unlocked_skills):
                    print(f"{index + 1}) {skill} (Cost: 20 MP / 10 Aura)")
                
                skill_choice = input("Select skill number: ").strip()
                if self.player.mana_points >= 20:
                    self.player.mana_points -= 20
                    dmg = self.calculate_damage_output(self.player.base_attack_power * 2, self.enemy_dfn, True)
                    self.enemy_hp -= dmg
                    print(f"💥 ANIME AWAKENING SCENE! You unleash {self.player.unlocked_skills[0]} dealing {dmg} obliteration damage!")
                else:
                    print("❌ Insufficient magic mana registers! Execution failed. Defending instead.")
                    self.player_defense_buff = True

        elif choice == "3":
            self.player_defense_buff = True
            print(f"🛡️ {self.player.player_name} enters a heavy defensive parry stance.")

        elif choice == "4":
            if not self.player.inventory_slots:
                print("❌ Your inventory matrix contains zero usable entities. Striking instead.")
                dmg = self.calculate_damage_output(self.player.base_attack_power // 2, self.enemy_dfn)
                self.enemy_hp -= dmg
            else:
                print("\nInventory Ingestion System:")
                for index, item in enumerate(self.player.inventory_slots):
                    print(f"{index + 1}) {item}")
                item_choice = input("Select item array index to consume: ").strip()
                
                try:
                    chosen_idx = int(item_choice) - 1
                    consumed_item = self.player.inventory_slots.pop(chosen_idx)
                    if "Shard" in consumed_item or "Potion" in consumed_item:
                        self.player.health_points = min(self.player.maximum_health_points, self.player.health_points + 60)
                        print(f"🧪 Consumed {consumed_item}. Recovered 60 Health Points framework parameters.")
                except:
                    print("⚠️ Input compilation error. Miscast item, turn forfeit.")

    def execute_enemy_turn(self):
        if self.enemy_hp <= 0:
            return

        print(f"\n--- {self.enemy_name}'s Counter Phase ---")
        dmg = self.calculate_damage_output(self.enemy_atk, self.player.base_defense_rating)
        
        if self.player_defense_buff:
            dmg = dmg // 2
            print("🛡️ Your defensive configuration matrix blocked half the oncoming kinetic values.")

        self.player.health_points -= dmg
        print(f"💥 {self.enemy_name} charges forward! Dealt {dmg} damage to your armor arrays.")

    def process_battle_loop(self):
        while self.battle_active:
            self.execute_player_turn()
            if self.enemy_hp <= 0:
                print(f"\n✨ VICTORY! {self.enemy_name} was wiped from the active matrix sector.")
                self.player.experience_points += self.enemy_xp_reward
                print(f"🌟 Gained {self.enemy_xp_reward} experience points allocation.")
                self.check_level_up_parameters()
                self.battle_active = False
                return True

            self.execute_enemy_turn()
            if self.player.health_points <= 0:
                print("\n💀 CRITICAL COGNITIVE DISCONNECT: Player health dropped to absolute zero.")
                print("The apocalyptic countdown accelerates. The timeline falls into cosmic static.")
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
            print(f"🎉 LEVEL UP MATRIX EVOLUTION! {self.player.player_name} reached Level {self.player.current_level}!")

class HubInterface:
    def __init__(self, player, world_context):
        self.player = player
        self.context = world_context

    def show_dashboard(self):
        print("\n" + "="*70)
        print(f" MASTER HUD INTERFACE | ACT: {self.context.current_act} | WORLD STABILITY: {self.context.world_stability_index}%")
        print(f" COUNTDOWN UNTIL TOTAL TIMELINE COLLAPSE: {self.context.cataclysm_countdown_hours} HOURS")
        print("="*70)
        print(f" Hero Unit: {self.player.player_name} | Archetype Vector: {self.player.chosen_class}")
        print(f" Level: {self.player.current_level} | EXP Pool: {self.player.experience_points}/{self.player.next_level_experience}")
        print(f" Structural HP: {self.player.health_points}/{self.player.maximum_health_points} | MP Capacity: {self.player.mana_points}/{self.player.maximum_mana_points}")
        print(f" Armed Core: {self.player.equipped_weapon} | Carried Shell: {self.player.equipped_armor}")
        print("-"*70)
        print("Navigation System Matrix Directives:")
        print("1) Initiate Spatial Warp to Active Danger Sectors")
        print("2) Initialize Dialogue Communications Protocol with Local NPCs")
        print("3) Access Item Satchel Manifest and Gear Allocations")
        print("4) Run Local Automated Systems Infrastructure Diagnostics")
        print("5) Terminate Connection and Exit Game Engine")
        
        return input("Select directive index sequence: ").strip()

# ============================================================================
# PART 4: QUEST AND NARRATIVE SYSTEMS
# ============================================================================

class QuestManager:
    """Manages all quests, objectives, and narrative progression"""
    
    def __init__(self):
        self.quests = {}
        self.active_quests = []
        self.completed_quests = []
        self.quest_chains = {}
        self.current_chapter = 1
        self.story_flags = {}
    
    def register_quest(self, quest_id, title, description, objective_type, reward_xp, reward_gold, quest_giver):
        """Register a new quest into the system"""
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
        """Player accepts a quest"""
        if quest_id not in self.quests:
            return False
        
        quest = self.quests[quest_id]
        if quest_id not in player.quest_flags:
            player.quest_flags[quest_id] = {"status": "active", "progress": 0}
            self.active_quests.append(quest_id)
            return True
        return False
    
    def update_quest_progress(self, quest_id, progress_amount):
        """Update progress on active quest"""
        if quest_id in self.quests:
            self.quests[quest_id]["progress"] = min(
                self.quests[quest_id]["progress"] + progress_amount,
                self.quests[quest_id]["completion_requirement"]
            )
            return self.quests[quest_id]["progress"]
        return 0
    
    def complete_quest(self, player, quest_id):
        """Mark quest as complete and grant rewards"""
        if quest_id not in self.quests:
            return None
        
        quest = self.quests[quest_id]
        if quest["progress"] >= quest["completion_requirement"]:
            player.quest_flags[quest_id]["status"] = "completed"
            self.completed_quests.append(quest_id)
            if quest_id in self.active_quests:
                self.active_quests.remove(quest_id)
            
            rewards = {
                "experience": quest["reward_xp"],
                "gold": quest["reward_gold"]
            }
            return rewards
        return None

class NPCSystem:
    """Manages NPC interactions, dialogue trees, and relationships"""
    
    def __init__(self):
        self.npcs = {}
        self.npc_relationships = {}
        self.dialogue_trees = {}
        self.npc_locations = {}
    
    def register_npc(self, npc_id, name, role, personality, location_zone):
        """Register a new NPC into the world"""
        self.npcs[npc_id] = {
            "id": npc_id,
            "name": name,
            "role": role,
            "personality": personality,
            "location": location_zone,
            "relationship_level": 0,
            "has_quest": False,
            "quest_id": None
        }
        self.npc_relationships[npc_id] = {"favor": 0, "interactions": 0}
    
    def interact_with_npc(self, npc_id, choice):
        """Execute NPC interaction and track relationship"""
        if npc_id not in self.npcs:
            return None
        
        npc = self.npcs[npc_id]
        self.npc_relationships[npc_id]["interactions"] += 1
        self.npc_relationships[npc_id]["favor"] += 1
        
        return {
            "npc": npc["name"],
            "interaction": self.npc_relationships[npc_id]["interactions"],
            "favor_level": self.npc_relationships[npc_id]["favor"]
        }

class CataclysmSystem:
    """Manages the apocalyptic countdown and world threat mechanics"""
    
    def __init__(self, game_context):
        self.game_context = game_context
        self.cataclysm_stages = [
            {"stage": 1, "hours": 24, "world_corruption": 0.2, "description": "Initial Rifts Open"},
            {"stage": 2, "hours": 18, "world_corruption": 0.35, "description": "Corrupted Zones Expand"},
            {"stage": 3, "hours": 12, "world_corruption": 0.5, "description": "Magic Destabilizes"},
            {"stage": 4, "hours": 6, "world_corruption": 0.75, "description": "Cities Fall"},
            {"stage": 5, "hours": 0, "world_corruption": 1.0, "description": "World Consumed"}
        ]
        self.current_stage = 1
        self.time_remaining = 24
    
    def update_cataclysm_countdown(self, hours_passed):
        """Advance cataclysm timer"""
        self.time_remaining -= hours_passed
        self.game_context.cataclysm_countdown_hours = max(self.time_remaining, 0)
        self._check_stage_advancement()
    
    def _check_stage_advancement(self):
        """Transition to next cataclysm stage"""
        for stage_data in self.cataclysm_stages:
            if self.time_remaining <= stage_data["hours"] and self.current_stage < stage_data["stage"]:
                self.current_stage = stage_data["stage"]
                self.game_context.world_stability_index = (1.0 - stage_data["world_corruption"]) * 100
    
    def get_stage_description(self):
        """Get current cataclysm stage narrative"""
        return self.cataclysm_stages[self.current_stage - 1]["description"]

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
    player.player_name = input("\n[SYSTEM] Enter your hero designation: ").strip() or "DefaultHero"
    
    print("\n[CLASS SELECTION MATRIX]")
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
    
    player.update_stats()
    
    logger.log_info(f"Hero {player.player_name} ({player.chosen_class}) registered successfully!")
    
    # Initialize game systems
    item_registry = ItemRegistry()
    enemy_registry = EnemyRegistry()
    zone_registry = ZoneRegistry()
    quest_manager = QuestManager()
    npc_system = NPCSystem()
    cataclysm = CataclysmSystem(game_context)
    hub = HubInterface(player, game_context)
    
    logger.log_info("Loading enemy registry templates...")
    enemy_registry.register_enemy("ENM_001", "Corrupted Sprite", 1, 30, 10, 5, 25)
    enemy_registry.register_enemy("ENM_002", "Dark Wraith", 3, 60, 18, 10, 75)
    enemy_registry.register_enemy("ENM_003", "Abyssal Guardian", 5, 100, 28, 15, 150)
    
    logger.log_info("Loading zone registry...")
    zone_registry.register_zone("ZONE_001", "Shattered Forests", 2, "Nature", "A forest twisted by corruption")
    zone_registry.register_zone("ZONE_002", "Forsaken Citadel", 4, "Darkness", "An ancient fortress has fallen")
    
    logger.log_info("Loading quest registry...")
    quest_manager.register_quest("Q001", "Save the Village", "Defeat corrupted beasts terrorizing the village", "combat", 500, 100, "Elder Sage")
    quest_manager.register_quest("Q002", "Retrieve Crystal Shards", "Find 5 crystal shards scattered across zones", "collection", 300, 50, "Mage Guild Master")
    
    logger.log_info("Loading NPC registry...")
    npc_system.register_npc("NPC_001", "Elder Sage", "Quest Giver", "Wise", "Village Center")
    npc_system.register_npc("NPC_002", "Mage Guild Master", "Trainer", "Scholarly", "Magic Tower")
    
    logger.log_info("System initialization complete! World stability at 100%")
    game_context.system_ready = True
    
    return game_context, player, logger, enemy_registry, zone_registry, quest_manager, npc_system, cataclysm, hub

def main_game_loop(game_context, player, logger, enemy_registry, zone_registry, quest_manager, npc_system, cataclysm, hub):
    """Main game loop"""
    
    while game_context.is_running:
        if not game_context.system_ready:
            break
        
        choice = hub.show_dashboard()
        
        if choice == "1":
            print("\n[SPATIAL WARP INITIATED]")
            print("Available Danger Sectors:")
            for zone_id, zone_data in zone_registry.zones.items():
                print(f"  > {zone_data['name']} (Danger: {zone_data['danger']}/5)")
            
            zone_choice = input("Select zone (or press Enter to return): ").strip()
            if zone_choice:
                # Start combat with random enemy
                enemy_id = random.choice(list(enemy_registry.enemies.keys()))
                enemy_data = enemy_registry.enemies[enemy_id].copy()
                
                print(f"\n⚠️ A wild {enemy_data['name']} (Lv.{enemy_data['level']}) appears!")
                combat = CombatEngine(player, enemy_data)
                victory = combat.process_battle_loop()
                
                if not victory:
                    print("\n[GAME OVER] Your timeline has concluded.")
                    game_context.is_running = False
                else:
                    cataclysm.update_cataclysm_countdown(1)
                    print(f"\nWorld Corruption Status: {100 - game_context.world_stability_index}%")
                    print(f"Time Remaining: {game_context.cataclysm_countdown_hours} hours")
        
        elif choice == "2":
            print("\n[DIALOGUE MATRIX ACTIVATED]")
            print("Available NPCs:")
            for npc_id, npc_data in npc_system.npcs.items():
                print(f"  > {npc_data['name']} ({npc_data['role']}) - {npc_data['location']}")
            
            npc_choice = input("Select NPC (or press Enter to return): ").strip()
            if npc_choice:
                result = npc_system.interact_with_npc(f"NPC_{int(npc_choice):03d}", "greeting")
                if result:
                    print(f"\n{result['npc']}: 'Greetings, traveler. We meet again...'")
                    print(f"Favor Level: {result['favor_level']}")
        
        elif choice == "3":
            print("\n[INVENTORY INTERFACE]")
            print(f"Current Items: {len(player.inventory_slots)}")
            if player.inventory_slots:
                for i, item in enumerate(player.inventory_slots, 1):
                    print(f"  {i}) {item}")
            else:
                print("  (Empty)")
            input("Press Enter to continue...")
        
        elif choice == "4":
            print("\n[SYSTEM DIAGNOSTICS]")
            print(f"Hero Status: {player.player_name} Lv.{player.current_level}")
            print(f"Health: {player.health_points}/{player.maximum_health_points}")
            print(f"Active Quests: {len(quest_manager.active_quests)}")
            print(f"Cataclysm Stage: {cataclysm.get_stage_description()}")
            input("Press Enter to continue...")
        
        elif choice == "5":
            print("\n[SYSTEM SHUTDOWN INITIATED]")
            print("Thank you for playing Anime Chronicles: World Salvation!")
            game_context.is_running = False
        
        else:
            print("⚠️ Invalid selection. Please try again.")

def main():
    """Main entry point"""
    try:
        game_context, player, logger, enemy_registry, zone_registry, quest_manager, npc_system, cataclysm, hub = initialize_game()
        main_game_loop(game_context, player, logger, enemy_registry, zone_registry, quest_manager, npc_system, cataclysm, hub)
    except KeyboardInterrupt:
        print("\n\n[SYSTEM] Game interrupted by user. Shutting down...")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
