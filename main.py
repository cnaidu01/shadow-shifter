import pygame
import sys
import random
from enum import Enum
from player import Player
from monster import Monster
from level import Level
from ui import UI
from arrow import Arrow
from platform import Platform
from shop import Shop

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow Shifter - Pixel Dungeon")
clock = pygame.time.Clock()
fps = 60

BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
DARK_GRAY = (40, 40, 50)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
BLUE = (80, 150, 255)
PURPLE = (200, 100, 255)
GOLD = (255, 200, 50)

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    LEVEL_COMPLETE = 2
    GAME_OVER = 3

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.player = None
        self.level = None
        self.platforms = []
        self.monsters = []
        self.arrows = []
        self.ui = UI()
        self.shop = Shop()
        self.level_num = 1
        self.score = 0
        self.gravity = 0.6
        self.selected_character = None
        
    def show_menu(self):
        font_large = pygame.font.Font(None, 54)
        font_small = pygame.font.Font(None, 28)
        
        characters = [
            {"name": "Archer", "desc": "Shoot arrows", "cost": 0},
            {"name": "Mage", "desc": "Cast spells & potions", "cost": 200},
            {"name": "Knight", "desc": "Heavy armor & shield", "cost": 300},
            {"name": "Rogue", "desc": "Fast & sneaky", "cost": 250},
        ]
        
        while self.state == GameState.MENU:
            screen.fill(DARK_GRAY)
            
            title = font_large.render("SHADOW SHIFTER", True, GOLD)
            screen.blit(title, (SCREEN_WIDTH // 2 - 200, 50))
            
            subtitle = font_small.render("Select Your Character", True, WHITE)
            screen.blit(subtitle, (SCREEN_WIDTH // 2 - 100, 120))
            
            gold_text = font_small.render(f"Gold: {self.shop.gold}", True, GOLD)
            screen.blit(gold_text, (SCREEN_WIDTH // 2 - 50, 170))
            
            for i, char in enumerate(characters):
                y = 250 + i * 120
                unlocked = self.shop.gold >= char["cost"] or char["cost"] == 0
                box_color = BLUE if unlocked else (80, 80, 80)
                pygame.draw.rect(screen, box_color, (100, y, 1000, 100))
                pygame.draw.rect(screen, WHITE, (100, y, 1000, 100), 3)
                
                name_text = font_small.render(char["name"], True, WHITE)
                screen.blit(name_text, (120, y + 10))
                
                desc_text = font_small.render(char["desc"], True, (200, 200, 200))
                screen.blit(desc_text, (120, y + 40))
                
                if unlocked:
                    status_text = font_small.render("OWNED", True, GREEN)
                else:
                    status_text = font_small.render(f"COST: {char['cost']}", True, RED)
                screen.blit(status_text, (900, y + 40))
            
            inst_text = font_small.render("Press 1-4 to select | SPACE to start", True, (150, 150, 150))
            screen.blit(inst_text, (SCREEN_WIDTH // 2 - 200, 750))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.selected_character = "archer"
                        self.start_game()
                        break
                    elif event.key == pygame.K_2 and self.shop.gold >= 200:
                        self.selected_character = "mage"
                        self.start_game()
                        break
                    elif event.key == pygame.K_3 and self.shop.gold >= 300:
                        self.selected_character = "knight"
                        self.start_game()
                        break
                    elif event.key == pygame.K_4 and self.shop.gold >= 250:
                        self.selected_character = "rogue"
                        self.start_game()
                        break
        return True
    
    def start_game(self):
        self.state = GameState.PLAYING
        self.player = Player(100, SCREEN_HEIGHT - 150, self.selected_character)
        self.level = Level(self.level_num)
        self.platforms = self.level.create_platforms(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.monsters = self.level.spawn_monsters(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.arrows = []
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move(-6, 0, self.platforms)
        if keys[pygame.K_d]:
            self.player.move(6, 0, self.platforms)
        if keys[pygame.K_w] and self.player.on_ground:
            self.player.jump()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.player.toggle_form()
                if event.key == pygame.K_SPACE:
                    self.player.use_ability(self.arrows, self.monsters)
        return True
    
    def update(self):
        self.player.apply_gravity(self.gravity, self.platforms, SCREEN_HEIGHT)
        
        for monster in self.monsters[:]:
            if monster.health <= 0:
                self.monsters.remove(monster)
                self.score += monster.reward
                self.shop.gold += monster.reward
            else:
                monster.update(self.platforms, SCREEN_HEIGHT)
                if self.player.form == "warrior" and abs(self.player.x - monster.x) < 30:
                    self.player.take_damage(0.5)
        
        for arrow in self.arrows[:]:
            arrow.update()
            hit = False
            for monster in self.monsters:
                if arrow.collides_with(monster):
                    monster.take_damage(arrow.damage)
                    hit = True
                    break
            if arrow.x < 0 or arrow.x > SCREEN_WIDTH or arrow.y < 0 or arrow.y > SCREEN_HEIGHT or hit:
                if arrow in self.arrows:
                    self.arrows.remove(arrow)
        
        if len(self.monsters) == 0:
            self.state = GameState.LEVEL_COMPLETE
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER
    
    def draw(self):
        screen.fill(DARK_GRAY)
        tile_size = 40
        for x in range(0, SCREEN_WIDTH, tile_size):
            for y in range(0, SCREEN_HEIGHT, tile_size):
                if (x // tile_size + y // tile_size) % 2 == 0:
                    pygame.draw.rect(screen, (35, 35, 45), (x, y, tile_size, tile_size))
        
        for platform in self.platforms:
            platform.draw(screen)
        self.player.draw(screen)
        for arrow in self.arrows:
            arrow.draw(screen)
        for monster in self.monsters:
            monster.draw(screen)
        self.ui.draw(screen, self.player, self.score, self.level_num, len(self.monsters), self.shop.gold)
        pygame.display.flip()
    
    def run(self):
        running = True
        if not self.show_menu():
            running = False
        
        while running and self.state != GameState.MENU:
            running = self.handle_input()
            
            if self.state == GameState.PLAYING:
                self.update()
            elif self.state == GameState.LEVEL_COMPLETE:
                if not self.level_complete_screen():
                    running = False
            elif self.state == GameState.GAME_OVER:
                if not self.game_over_screen():
                    running = False
            
            self.draw()
            clock.tick(fps)
        
        pygame.quit()
        sys.exit()
    
    def level_complete_screen(self):
        font = pygame.font.Font(None, 48)
        text = font.render(f"Level {self.level_num} Complete!", True, GREEN)
        screen.blit(text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 100))
        
        font_small = pygame.font.Font(None, 32)
        reward = 100 * self.level_num
        text2 = font_small.render(f"Reward: +{reward} Gold", True, GOLD)
        screen.blit(text2, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
        
        text3 = font_small.render("Press SPACE to continue...", True, WHITE)
        screen.blit(text3, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 40))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.shop.gold += 100 * self.level_num
                self.level_num += 1
                self.level = Level(self.level_num)
                self.platforms = self.level.create_platforms(SCREEN_WIDTH, SCREEN_HEIGHT)
                self.monsters = self.level.spawn_monsters(SCREEN_WIDTH, SCREEN_HEIGHT)
                self.player = Player(100, SCREEN_HEIGHT - 150, self.selected_character)
                self.arrows = []
                self.state = GameState.PLAYING
                return True
        return True
    
    def game_over_screen(self):
        font = pygame.font.Font(None, 48)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        
        font_small = pygame.font.Font(None, 32)
        text2 = font_small.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(text2, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 20))
        
        text3 = font_small.render("Press SPACE to return to menu...", True, WHITE)
        screen.blit(text3, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 70))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.state = GameState.MENU
                return True
        return True

if __name__ == "__main__":
    game = Game()
    game.run()
