import pygame
import math

# Colors
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "gray": (128, 128, 128),
    "dark_gray": (64, 64, 64),
    "gold": (255, 215, 0),
}

class Button:
    """UI Button class"""
    def __init__(self, x, y, width, height, text, font, bg_color=(100, 100, 100), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover = False
        self.clicked = False
        
    def update(self, mouse_pos, mouse_clicked):
        """Update button state"""
        self.hover = self.rect.collidepoint(mouse_pos)
        self.clicked = self.hover and mouse_clicked
        
    def draw(self, screen):
        """Draw button"""
        color = tuple(min(c + 50, 255) for c in self.bg_color) if self.hover else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLORS["white"], self.rect, 2)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Menu:
    """Base menu class"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
    def handle_input(self):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        pass

class MainMenu(Menu):
    """Main menu screen"""
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.selected_option = 0
        self.options = ["Start PvE", "Start PvP", "Shop", "Stats", "Quit"]
        
        self.buttons = [
            Button(screen_width//2 - 100, 150, 200, 50, "Start PvE", self.font_medium),
            Button(screen_width//2 - 100, 220, 200, 50, "Start PvP", self.font_medium),
            Button(screen_width//2 - 100, 290, 200, 50, "Shop", self.font_medium),
            Button(screen_width//2 - 100, 360, 200, 50, "Stats", self.font_medium),
            Button(screen_width//2 - 100, 430, 200, 50, "Quit", self.font_medium),
        ]
        
    def handle_input(self, events, mouse_pos):
        """Handle input"""
        for button in self.buttons:
            button.update(mouse_pos, False)
            
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        return self.options[i]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option]
        
        return None
    
    def draw(self, screen):
        """Draw menu"""
        screen.fill(COLORS["black"])
        
        # Title
        title = self.font_large.render("ROBOT BATTLE ARENA", True, COLORS["gold"])
        title_rect = title.get_rect(center=(self.screen_width//2, 50))
        screen.blit(title, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

class ShopMenu(Menu):
    """Shop menu for buying equipment"""
    def __init__(self, screen_width, screen_height, equipment_manager, player_stats):
        super().__init__(screen_width, screen_height)
        self.equipment_manager = equipment_manager
        self.player_stats = player_stats
        self.selected_tab = "weapons"  # weapons, armors, accessories
        
    def handle_input(self, events):
        """Handle input"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                elif event.key == pygame.K_1:
                    self.selected_tab = "weapons"
                elif event.key == pygame.K_2:
                    self.selected_tab = "armors"
                elif event.key == pygame.K_3:
                    self.selected_tab = "accessories"
        
        return None
    
    def draw(self, screen):
        """Draw shop"""
        screen.fill(COLORS["black"])
        
        # Title
        title = self.font_large.render("SHOP", True, COLORS["gold"])
        title_rect = title.get_rect(center=(self.screen_width//2, 20))
        screen.blit(title, title_rect)
        
        # Player stats
        gold_text = self.font_small.render(f"Gold: {self.player_stats.gold}", True, COLORS["gold"])
        level_text = self.font_small.render(f"Level: {self.player_stats.level}", True, COLORS["white"])
        screen.blit(gold_text, (20, 70))
        screen.blit(level_text, (self.screen_width - 200, 70))
        
        # Tabs
        tabs = ["[1] Weapons", "[2] Armors", "[3] Accessories"]
        for i, tab in enumerate(tabs):
            color = COLORS["gold"] if (i == 0 and self.selected_tab == "weapons") or \
                                      (i == 1 and self.selected_tab == "armors") or \
                                      (i == 2 and self.selected_tab == "accessories") else COLORS["white"]
            tab_text = self.font_small.render(tab, True, color)
            screen.blit(tab_text, (20 + i * 200, 120))
        
        # Display items
        y_pos = 170
        if self.selected_tab == "weapons":
            items = self.equipment_manager.weapons
        elif self.selected_tab == "armors":
            items = self.equipment_manager.armors
        else:
            items = self.equipment_manager.accessories
            
        for eq_id, equipment in items.items():
            text = f"{equipment.name} | Cost: {equipment.cost} | ATK: +{equipment.attack_bonus} ARM: +{equipment.armor_bonus} HP: +{equipment.hp_bonus}"
            eq_text = self.font_small.render(text, True, COLORS["white"])
            screen.blit(eq_text, (40, y_pos))
            y_pos += 40
        
        # Instructions
        info = self.font_small.render("Press ESC to return", True, COLORS["gray"])
        screen.blit(info, (20, self.screen_height - 40))

class StatsMenu(Menu):
    """Stats/Profile menu"""
    def __init__(self, screen_width, screen_height, player_stats):
        super().__init__(screen_width, screen_height)
        self.player_stats = player_stats
        
    def handle_input(self, events):
        """Handle input"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
        return None
    
    def draw(self, screen):
        """Draw stats"""
        screen.fill(COLORS["black"])
        
        # Title
        title = self.font_large.render("PLAYER STATS", True, COLORS["gold"])
        title_rect = title.get_rect(center=(self.screen_width//2, 20))
        screen.blit(title, title_rect)
        
        y_pos = 100
        
        # Player info
        info_texts = [
            f"Name: {self.player_stats.name}",
            f"Level: {self.player_stats.level}",
            f"Experience: {self.player_stats.experience}/{self.player_stats.exp_to_next_level}",
            f"Gold: {self.player_stats.gold}",
            "",
            "EQUIPMENT:",
            f"Weapon: {self.player_stats.equipped_weapon.name if self.player_stats.equipped_weapon else 'None'}",
            f"Armor: {self.player_stats.equipped_armor.name if self.player_stats.equipped_armor else 'None'}",
            f"Accessory: {self.player_stats.equipped_accessory.name if self.player_stats.equipped_accessory else 'None'}",
            "",
            "UNLOCKED ROBOTS:",
        ]
        
        for text in info_texts:
            text_surface = self.font_small.render(text, True, COLORS["white"])
            screen.blit(text_surface, (40, y_pos))
            y_pos += 35
        
        # Unlocked robots
        for robot_type, unlocked in self.player_stats.unlocked_abilities.items():
            status = "Unlocked" if unlocked else "Locked"
            color = COLORS["green"] if unlocked else COLORS["red"]
            text_surface = self.font_small.render(f"  {robot_type.upper()}: {status}", True, color)
            screen.blit(text_surface, (60, y_pos))
            y_pos += 35
        
        # Instructions
        info = self.font_small.render("Press ESC to return", True, COLORS["gray"])
        screen.blit(info, (20, self.screen_height - 40))

class RobotSelectMenu(Menu):
    """Menu to select robot type"""
    def __init__(self, screen_width, screen_height, player_stats):
        super().__init__(screen_width, screen_height)
        self.player_stats = player_stats
        self.robot_types = ["warrior", "assassin", "tank", "mage"]
        self.selected_index = 0
        
        self.robot_descriptions = {
            "warrior": "Balanced - Good for beginners",
            "assassin": "Fast & High Damage - Risky",
            "tank": "Tanky - Defensive playstyle",
            "mage": "High Attack - Long range",
        }
        
    def handle_input(self, events):
        """Handle input"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.selected_index = (self.selected_index - 1) % len(self.robot_types)
                elif event.key == pygame.K_RIGHT:
                    self.selected_index = (self.selected_index + 1) % len(self.robot_types)
                elif event.key == pygame.K_RETURN:
                    selected_robot = self.robot_types[self.selected_index]
                    if self.player_stats.unlocked_abilities.get(selected_robot, False):
                        return selected_robot
                elif event.key == pygame.K_ESCAPE:
                    return "back"
        return None
    
    def draw(self, screen):
        """Draw menu"""
        screen.fill(COLORS["black"])
        
        # Title
        title = self.font_large.render("SELECT ROBOT", True, COLORS["gold"])
        title_rect = title.get_rect(center=(self.screen_width//2, 50))
        screen.blit(title, title_rect)
        
        # Draw robot options
        y_pos = 150
        for i, robot_type in enumerate(self.robot_types):
            is_selected = i == self.selected_index
            is_unlocked = self.player_stats.unlocked_abilities.get(robot_type, False)
            
            if not is_unlocked:
                color = COLORS["gray"]
                status = " [LOCKED]"
            elif is_selected:
                color = COLORS["gold"]
                status = " <- SELECTED"
            else:
                color = COLORS["white"]
                status = ""
            
            text = self.font_medium.render(f"{robot_type.upper()}{status}", True, color)
            screen.blit(text, (self.screen_width//2 - 100, y_pos))
            
            # Description
            desc = self.font_small.render(self.robot_descriptions[robot_type], True, COLORS["gray"])
            screen.blit(desc, (self.screen_width//2 - 100, y_pos + 40))
            
            y_pos += 120
        
        # Instructions
        info = self.font_small.render("Use arrow keys to select | ENTER to confirm | ESC to go back", True, COLORS["gray"])
        screen.blit(info, (self.screen_width//2 - 300, self.screen_height - 40))
