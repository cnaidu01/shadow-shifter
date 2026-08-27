import pygame
import sys
import random
from enum import Enum
from player import Player
from monster import Monster
from level import Level
from ui import UI

pygame.init()

# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow Shifter")
clock = pygame.time.Clock()
fps = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 200)
PURPLE = (150, 0, 150)

class GameState(Enum):
    PLAYING = 1
    PAUSED = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4

class Game:
    def __init__(self):
        self.state = GameState.PLAYING
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.level = Level(1)
        self.monsters = self.level.spawn_monsters()
        self.ui = UI()
        self.wave = 1
        self.score = 0
        self.enemies_defeated = 0
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Movement
        if keys[pygame.K_w]:
            self.player.move(0, -5)
        if keys[pygame.K_s]:
            self.player.move(0, 5)
        if keys[pygame.K_a]:
            self.player.move(-5, 0)
        if keys[pygame.K_d]:
            self.player.move(5, 0)
        
        # Shift form (E key)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.player.toggle_form()
                if event.key == pygame.K_SPACE and self.player.form == "warrior":
                    # Attack
                    self.player.attack(self.monsters)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.player.form == "warrior":
                    self.player.attack(self.monsters)
        
        return True
    
    def update(self):
        # Keep player in bounds
        self.player.x = max(20, min(self.player.x, SCREEN_WIDTH - 20))
        self.player.y = max(20, min(self.player.y, SCREEN_HEIGHT - 20))
        
        # Update monsters
        for monster in self.monsters[:]:
            if monster.health <= 0:
                self.monsters.remove(monster)
                self.score += monster.reward
                self.enemies_defeated += 1
            else:
                monster.update(self.player)
                # Check collision with player (damage)
                if self.player.form == "warrior" and self.player.distance_to(monster) < 30:
                    self.player.take_damage(0.5)  # Per frame damage
        
        # Check win condition
        if len(self.monsters) == 0:
            self.state = GameState.LEVEL_COMPLETE
    
    def draw(self):
        screen.fill(DARK_GRAY)
        
        # Draw walls (dungeon layout)
        if self.player.form == "shadow":
            screen.fill((10, 10, 20))  # Darker background in shadow form
        
        # Draw player
        self.player.draw(screen)
        
        # Draw monsters
        for monster in self.monsters:
            monster.draw(screen)
        
        # Draw UI
        self.ui.draw(screen, self.player, self.score, self.wave, len(self.monsters))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            
            if self.state == GameState.PLAYING:
                self.update()
            elif self.state == GameState.LEVEL_COMPLETE:
                self.level_complete_screen()
            
            self.draw()
            clock.tick(fps)
        
        pygame.quit()
        sys.exit()
    
    def level_complete_screen(self):
        font = pygame.font.Font(None, 48)
        text = font.render(f"Level {self.wave} Complete!", True, GREEN)
        screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.wave += 1
                self.level = Level(self.wave)
                self.monsters = self.level.spawn_monsters()
                self.state = GameState.PLAYING
        return True

if __name__ == "__main__":
    game = Game()
    game.run()
