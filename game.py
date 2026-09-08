import pygame
import sys
import math
from robot import Robot
from ai_robot import AIRobot
from progression import PlayerStats, EquipmentManager
from ui_menu import MainMenu, ShopMenu, StatsMenu, RobotSelectMenu
from vfx import VFXManager, TextManager

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GOLD = (255, 215, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robot Battle Arena")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Game state
        self.state = "main_menu"  # main_menu, shop, stats, robot_select, battle, game_over
        self.game_mode = None  # pvp or pve
        self.ai_difficulty = "normal"
        
        # Menus
        self.main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.equipment_manager = EquipmentManager()
        self.player_stats = PlayerStats("Hero")
        self.player_stats.load_from_file()
        
        self.shop_menu = ShopMenu(SCREEN_WIDTH, SCREEN_HEIGHT, self.equipment_manager, self.player_stats)
        self.stats_menu = StatsMenu(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_stats)
        self.robot_select_menu = RobotSelectMenu(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_stats)
        
        # Battle variables
        self.robot1 = None
        self.robot2 = None
        self.is_ai = False
        self.game_over = False
        self.winner = None
        self.round_timer = 0
        self.battle_reward = 0
        
        # VFX
        self.vfx_manager = VFXManager()
        self.text_manager = TextManager()
        
    def reset_game(self, robot1_type, robot2_type, is_ai=False):
        """Initialize or reset the game"""
        # Create robots with player stats bonuses
        bonuses = self.player_stats.get_total_bonuses()
        
        self.robot1 = Robot(150, SCREEN_HEIGHT//2 - 25, robot_type=robot1_type, team=1)
        # Apply equipment bonuses to player robot
        self.robot1.attack_power += bonuses["attack"]
        self.robot1.armor += bonuses["armor"]
        self.robot1.max_hp += bonuses["hp"]
        self.robot1.current_hp = self.robot1.max_hp
        
        if is_ai:
            self.robot2 = AIRobot(SCREEN_WIDTH - 200, SCREEN_HEIGHT//2 - 25, robot_type=robot2_type, team=2, difficulty=self.ai_difficulty)
            self.is_ai = True
        else:
            self.robot2 = Robot(SCREEN_WIDTH - 200, SCREEN_HEIGHT//2 - 25, robot_type=robot2_type, team=2)
            self.is_ai = False
        
        self.game_over = False
        self.winner = None
        self.round_timer = 0
        self.battle_reward = 0
        
    def handle_input(self):
        """Handle player input"""
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                return False
                
        # Handle different game states
        if self.state == "main_menu":
            action = self.main_menu.handle_input(events, mouse_pos)
            if action == "Start PvE":
                self.state = "robot_select"
                self.game_mode = "pve"
            elif action == "Start PvP":
                self.state = "robot_select"
                self.game_mode = "pvp"
            elif action == "Shop":
                self.state = "shop"
            elif action == "Stats":
                self.state = "stats"
            elif action == "Quit":
                return False
                
        elif self.state == "shop":
            action = self.shop_menu.handle_input(events)
            if action == "back":
                self.state = "main_menu"
                
        elif self.state == "stats":
            action = self.stats_menu.handle_input(events)
            if action == "back":
                self.state = "main_menu"
                
        elif self.state == "robot_select":
            action = self.robot_select_menu.handle_input(events)
            if action == "back":
                self.state = "main_menu"
            elif action and action in ["warrior", "assassin", "tank", "mage"]:
                self.reset_game(action, "assassin" if self.game_mode == "pve" else "warrior", self.game_mode == "pve")
                self.state = "battle"
                
        elif self.state == "battle":
            # Battle input
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.state = "main_menu"
                        
            # Player 1 controls (WASD + Space + Shift)
            keys = pygame.key.get_pressed()
            dx1, dy1 = 0, 0
            
            if keys[pygame.K_w]:
                dy1 = -1
            if keys[pygame.K_s]:
                dy1 = 1
            if keys[pygame.K_a]:
                dx1 = -1
            if keys[pygame.K_d]:
                dx1 = 1
                
            if dx1 != 0 or dy1 != 0:
                self.robot1.move(dx1, dy1, SCREEN_WIDTH, SCREEN_HEIGHT)
                
            if keys[pygame.K_SPACE]:
                if self.robot1.basic_attack(self.robot2):
                    self.vfx_manager.create_hit_effect(self.robot2.x + self.robot2.width//2, 
                                                       self.robot2.y + self.robot2.height//2, 
                                                       self.robot1.attack_power)
                    self.text_manager.add_damage_text(self.robot2.x, self.robot2.y, self.robot1.attack_power)
                    
            if keys[pygame.K_LSHIFT]:
                if self.robot1.special_ability(self.robot2):
                    self.vfx_manager.create_ability_effect(self.robot1.x + self.robot1.width//2,
                                                          self.robot1.y + self.robot1.height//2)
                    
            # Player 2 controls (only for PvP)
            if not self.is_ai:
                dx2, dy2 = 0, 0
                
                if keys[pygame.K_UP]:
                    dy2 = -1
                if keys[pygame.K_DOWN]:
                    dy2 = 1
                if keys[pygame.K_LEFT]:
                    dx2 = -1
                if keys[pygame.K_RIGHT]:
                    dx2 = 1
                    
                if dx2 != 0 or dy2 != 0:
                    self.robot2.move(dx2, dy2, SCREEN_WIDTH, SCREEN_HEIGHT)
                    
                if keys[pygame.K_RETURN]:
                    if self.robot2.basic_attack(self.robot1):
                        self.vfx_manager.create_hit_effect(self.robot1.x + self.robot1.width//2,
                                                          self.robot1.y + self.robot1.height//2,
                                                          self.robot2.attack_power)
                        self.text_manager.add_damage_text(self.robot1.x, self.robot1.y, self.robot2.attack_power)
                        
                if keys[pygame.K_RCTRL]:
                    if self.robot2.special_ability(self.robot1):
                        self.vfx_manager.create_ability_effect(self.robot2.x + self.robot2.width//2,
                                                              self.robot2.y + self.robot2.height//2)
        
        return True
    
    def update(self):
        """Update game state"""
        if self.state == "battle" and not self.game_over:
            # Update robots
            self.robot1.update([self.robot2])
            
            if self.is_ai:
                self.robot2.update(self.robot1, SCREEN_WIDTH, SCREEN_HEIGHT)
            else:
                self.robot2.update([self.robot1])
            
            # Check if anyone is dead
            if not self.robot1.is_alive():
                self.game_over = True
                self.winner = 2
                self.battle_reward = 0
            elif not self.robot2.is_alive():
                self.game_over = True
                self.winner = 1
                self.battle_reward = 200 + (self.player_stats.level * 50)
                
                # Award experience and gold
                leveled_up = self.player_stats.add_experience(self.battle_reward)
                self.player_stats.add_gold(int(self.battle_reward * 0.5))
                
                if leveled_up:
                    self.vfx_manager.create_level_up_effect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                    self.text_manager.add_level_up_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                    # Unlock new robots at certain levels
                    if self.player_stats.level >= 5:
                        self.player_stats.unlocked_abilities["assassin"] = True
                    if self.player_stats.level >= 10:
                        self.player_stats.unlocked_abilities["tank"] = True
                    if self.player_stats.level >= 15:
                        self.player_stats.unlocked_abilities["mage"] = True
                
                self.player_stats.save_to_file()
            
            self.round_timer += 1
        
        # Update VFX
        self.vfx_manager.update()
        self.text_manager.update()
    
    def draw(self):
        """Draw game state"""
        if self.state == "main_menu":
            self.main_menu.draw(self.screen)
        elif self.state == "shop":
            self.shop_menu.draw(self.screen)
        elif self.state == "stats":
            self.stats_menu.draw(self.screen)
        elif self.state == "robot_select":
            self.robot_select_menu.draw(self.screen)
        elif self.state == "battle":
            self.draw_battle()
        
        pygame.display.flip()
    
    def draw_battle(self):
        """Draw battle screen"""
        self.screen.fill(BLACK)
        
        # Draw arena border
        pygame.draw.rect(self.screen, GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 3)
        
        # Draw center line
        pygame.draw.line(self.screen, GRAY, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 1)
        
        # Draw robots
        self.robot1.draw(self.screen)
        self.robot2.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw VFX
        self.vfx_manager.draw(self.screen)
        self.text_manager.draw(self.screen)
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
    
    def draw_ui(self):
        """Draw user interface"""
        # Game mode indicator
        mode_text = f"Mode: {'PvE' if self.is_ai else 'PvP'} | Level: {self.player_stats.level} | Gold: {self.player_stats.gold}"
        mode_surface = self.font_tiny.render(mode_text, True, GOLD)
        self.screen.blit(mode_surface, (SCREEN_WIDTH//2 - 150, 10))
        
        # Player 1 stats (left side)
        p1_text = f"Player 1 - {self.robot1.robot_type.upper()}"
        p1_surface = self.font_medium.render(p1_text, True, (255, 100, 100))
        self.screen.blit(p1_surface, (20, 20))
        
        # Robot 1 HP
        hp_text = f"HP: {int(self.robot1.current_hp)}/{int(self.robot1.max_hp)}"
        hp_surface = self.font_small.render(hp_text, True, WHITE)
        self.screen.blit(hp_surface, (20, 60))
        
        # Robot 1 Armor
        armor_text = f"Armor: {int(self.robot1.armor)}"
        armor_surface = self.font_small.render(armor_text, True, WHITE)
        self.screen.blit(armor_surface, (20, 85))
        
        # Robot 1 Attack
        attack_text = f"Attack: {int(self.robot1.attack_power)}"
        attack_surface = self.font_small.render(attack_text, True, WHITE)
        self.screen.blit(attack_surface, (20, 110))
        
        # Robot 1 Attack Cooldown
        if self.robot1.attack_cooldown > 0:
            cooldown_text = f"Attack: {self.robot1.attack_cooldown}"
            cooldown_surface = self.font_small.render(cooldown_text, True, RED)
            self.screen.blit(cooldown_surface, (20, 135))
            
        # Robot 1 Ability Cooldown
        if self.robot1.ability_cooldown > 0:
            ability_text = f"Ability: {self.robot1.ability_cooldown}"
            ability_surface = self.font_small.render(ability_text, True, RED)
            self.screen.blit(ability_surface, (20, 160))
            
        # Player 2 stats (right side)
        player2_label = "AI" if self.is_ai else "Player 2"
        p2_text = f"{player2_label} - {self.robot2.robot_type.upper()}"
        p2_surface = self.font_medium.render(p2_text, True, (100, 100, 255))
        self.screen.blit(p2_surface, (SCREEN_WIDTH - 400, 20))
        
        # Robot 2 HP
        hp_text = f"HP: {int(self.robot2.current_hp)}/{int(self.robot2.max_hp)}"
        hp_surface = self.font_small.render(hp_text, True, WHITE)
        self.screen.blit(hp_surface, (SCREEN_WIDTH - 400, 60))
        
        # Robot 2 Armor
        armor_text = f"Armor: {int(self.robot2.armor)}"
        armor_surface = self.font_small.render(armor_text, True, WHITE)
        self.screen.blit(armor_surface, (SCREEN_WIDTH - 400, 85))
        
        # Robot 2 Attack
        attack_text = f"Attack: {int(self.robot2.attack_power)}"
        attack_surface = self.font_small.render(attack_text, True, WHITE)
        self.screen.blit(attack_surface, (SCREEN_WIDTH - 400, 110))
        
        # Robot 2 Attack Cooldown
        if self.robot2.attack_cooldown > 0:
            cooldown_text = f"Attack: {self.robot2.attack_cooldown}"
            cooldown_surface = self.font_small.render(cooldown_text, True, RED)
            self.screen.blit(cooldown_surface, (SCREEN_WIDTH - 400, 135))
            
        # Robot 2 Ability Cooldown
        if self.robot2.ability_cooldown > 0:
            ability_text = f"Ability: {self.robot2.ability_cooldown}"
            ability_surface = self.font_small.render(ability_text, True, RED)
            self.screen.blit(ability_surface, (SCREEN_WIDTH - 400, 160))
            
        # Controls info
        if self.is_ai:
            controls_text = "P1: WASD+SPACE/SHIFT"
        else:
            controls_text = "P1: WASD+SPACE/SHIFT | P2: ARROW+ENTER/RCTRL"
        controls_surface = self.font_small.render(controls_text, True, GRAY)
        self.screen.blit(controls_surface, (SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT - 30))
    
    def draw_game_over(self):
        """Draw game over screen"""
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Winner text
        if self.winner == 1:
            winner_text = f"YOU WIN! | Reward: {self.battle_reward} EXP + {int(self.battle_reward * 0.5)} Gold"
            color = GREEN
        else:
            winner_text = "AI WINS!" if self.is_ai else "Player 2 Wins!"
            color = RED
            
        winner_surface = self.font_large.render(winner_text, True, color)
        text_rect = winner_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(winner_surface, text_rect)
        
        # Restart text
        restart_text = "Press R to return to menu"
        restart_surface = self.font_small.render(restart_text, True, WHITE)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_surface, restart_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
