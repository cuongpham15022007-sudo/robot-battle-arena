import pygame
import json
import os

class Equipment:
    """Equipment class for robot upgrades"""
    def __init__(self, name, type_eq, attack_bonus=0, armor_bonus=0, hp_bonus=0, cost=0):
        self.name = name
        self.type = type_eq  # "weapon", "armor", "accessory"
        self.attack_bonus = attack_bonus
        self.armor_bonus = armor_bonus
        self.hp_bonus = hp_bonus
        self.cost = cost

class EquipmentManager:
    """Manages all equipment in the game"""
    def __init__(self):
        self.weapons = {
            "rusty_sword": Equipment("Rusty Sword", "weapon", attack_bonus=5, cost=100),
            "iron_sword": Equipment("Iron Sword", "weapon", attack_bonus=10, cost=250),
            "steel_sword": Equipment("Steel Sword", "weapon", attack_bonus=15, cost=500),
            "energy_sword": Equipment("Energy Sword", "weapon", attack_bonus=25, cost=1000),
        }
        
        self.armors = {
            "leather_armor": Equipment("Leather Armor", "armor", armor_bonus=10, cost=100),
            "iron_armor": Equipment("Iron Armor", "armor", armor_bonus=20, cost=250),
            "steel_armor": Equipment("Steel Armor", "armor", armor_bonus=30, cost=500),
            "legendary_armor": Equipment("Legendary Armor", "armor", armor_bonus=50, cost=1000),
        }
        
        self.accessories = {
            "health_ring": Equipment("Health Ring", "accessory", hp_bonus=50, cost=200),
            "power_ring": Equipment("Power Ring", "accessory", attack_bonus=8, cost=200),
            "defense_ring": Equipment("Defense Ring", "accessory", armor_bonus=15, cost=200),
            "crystal_orb": Equipment("Crystal Orb", "accessory", hp_bonus=100, attack_bonus=10, armor_bonus=10, cost=800),
        }
        
    def get_all_equipment(self):
        """Return all equipment"""
        return {**self.weapons, **self.armors, **self.accessories}
    
    def get_equipment_by_id(self, eq_id):
        """Get equipment by ID"""
        all_eq = self.get_all_equipment()
        return all_eq.get(eq_id)

class PlayerStats:
    """Player statistics and progression"""
    def __init__(self, name="Player"):
        self.name = name
        self.level = 1
        self.experience = 0
        self.exp_to_next_level = 100
        self.gold = 500  # Starting currency
        
        # Equipment slots
        self.equipped_weapon = None
        self.equipped_armor = None
        self.equipped_accessory = None
        
        # Inventory
        self.inventory = []
        self.unlocked_abilities = {
            "warrior": True,
            "assassin": False,
            "tank": False,
            "mage": False,
        }
        
    def add_experience(self, amount):
        """Add experience and handle leveling up"""
        self.experience += amount
        level_up = False
        
        while self.experience >= self.exp_to_next_level:
            self.experience -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = int(self.exp_to_next_level * 1.15)
            level_up = True
            
        return level_up
    
    def add_gold(self, amount):
        """Add gold to player"""
        self.gold += amount
    
    def spend_gold(self, amount):
        """Spend gold, return True if successful"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def equip_item(self, equipment, slot):
        """Equip an item"""
        if slot == "weapon":
            self.equipped_weapon = equipment
        elif slot == "armor":
            self.equipped_armor = equipment
        elif slot == "accessory":
            self.equipped_accessory = equipment
    
    def get_total_bonuses(self):
        """Get total stat bonuses from equipment"""
        attack = 0
        armor = 0
        hp = 0
        
        if self.equipped_weapon:
            attack += self.equipped_weapon.attack_bonus
            armor += self.equipped_weapon.armor_bonus
            hp += self.equipped_weapon.hp_bonus
            
        if self.equipped_armor:
            attack += self.equipped_armor.attack_bonus
            armor += self.equipped_armor.armor_bonus
            hp += self.equipped_armor.hp_bonus
            
        if self.equipped_accessory:
            attack += self.equipped_accessory.attack_bonus
            armor += self.equipped_accessory.armor_bonus
            hp += self.equipped_accessory.hp_bonus
            
        return {"attack": attack, "armor": armor, "hp": hp}
    
    def save_to_file(self, filename="player_stats.json"):
        """Save player stats to file"""
        data = {
            "name": self.name,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "equipped_weapon": self.equipped_weapon.name if self.equipped_weapon else None,
            "equipped_armor": self.equipped_armor.name if self.equipped_armor else None,
            "equipped_accessory": self.equipped_accessory.name if self.equipped_accessory else None,
            "unlocked_abilities": self.unlocked_abilities,
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filename="player_stats.json"):
        """Load player stats from file"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.name = data.get("name", "Player")
                self.level = data.get("level", 1)
                self.experience = data.get("experience", 0)
                self.gold = data.get("gold", 500)
                self.unlocked_abilities = data.get("unlocked_abilities", self.unlocked_abilities)
                return True
        return False
