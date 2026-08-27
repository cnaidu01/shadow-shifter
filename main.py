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

pygame.init()

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow Shifter - Platformer")
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
GRAY = (100, 100, 100)

class GameState(Enum):
    PLAYING = 1
    LEVEL_COMPLETE = 2
    GAME_OVER = 3

class Game:
    def __init__(self):
        self.state = GameState.PLAYING
        self.player = Player(100, SCREEN_HEIGHT - 150)
        self.level = Level(1)
        self.platforms = self.level.create_platforms(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.monsters = self.level.spawn_monsters(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.arrows = []
        self.ui = UI()
        self.level_num = 1
        self.score = 0
        self.gravity = 0.6
        self.enemies_defeated = 0
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Movement
        if keys[pygame.K_a]:
            self.player.move(-6, 0, self.platforms)
        if keys[pygame.K_d]:
            self.player.move(6, 0, self.platforms)
        
        # Jump
        if keys[pygame.K_w] and self.player.on_ground:
            self.player.jump()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                # Shift form (E key)
                if event.key == pygame.K_e:
                    self.player.toggle_form()
                # Shoot arrow (Space or mouse click)
                if event.key == pygame.K_SPACE:
                    self.shoot_arrow()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot_arrow()
        
        return True
    
    def shoot_arrow(self):
        """Shoot an arrow from player position"""
        if self.player.form == "warrior":
            arrow = self.player.shoot_arrow()
            if arrow:
                self.arrows.append(arrow)
    
    def update(self):
        # Apply gravity
        self.player.apply_gravity(self.gravity, self.platforms, SCREEN_HEIGHT)
        
        # Update monsters
        for monster in self.monsters[:]:
            if monster.health <= 0:
                self.monsters.remove(monster)
                self.score += monster.reward
                self.enemies_defeated += 1
            else:
                monster.update(self.platforms, SCREEN_HEIGHT)
        
        # Update arrows
        for arrow in self.arrows[:]:
            arrow.update()
            
            # Check collision with monsters
            hit = False
            for monster in self.monsters:
                if arrow.collides_with(monster):
                    monster.take_damage(arrow.damage)
                    hit = True
                    break
            
            # Remove arrow if off screen or hit
            if arrow.x < 0 or arrow.x > SCREEN_WIDTH or arrow.y < 0 or arrow.y > SCREEN_HEIGHT or hit:
                if arrow in self.arrows:
                    self.arrows.remove(arrow)
        
        # Check win condition
        if len(self.monsters) == 0:
            self.state = GameState.LEVEL_COMPLETE
        
        # Check lose condition
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER
    
    def draw(self):
        # Background
        if self.player.form == "shadow":
            screen.fill((10, 10, 20))  # Dark background in shadow form
        else:
            screen.fill((20, 20, 40))  # Dark blue dungeon
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(screen)
        
        # Draw player
        self.player.draw(screen)
        
        # Draw arrows
        for arrow in self.arrows:
            arrow.draw(screen)
        
        # Draw monsters
        for monster in self.monsters:
            monster.draw(screen)
        
        # Draw UI
        self.ui.draw(screen, self.player, self.score, self.level_num, len(self.monsters))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
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
        screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
        
        font_small = pygame.font.Font(None, 32)
        text2 = font_small.render("Press SPACE to continue...", True, WHITE)
        screen.blit(text2, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.level_num += 1
                self.level = Level(self.level_num)
                self.platforms = self.level.create_platforms(SCREEN_WIDTH, SCREEN_HEIGHT)
                self.monsters = self.level.spawn_monsters(SCREEN_WIDTH, SCREEN_HEIGHT)
                self.player = Player(100, SCREEN_HEIGHT - 150)
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
        screen.blit(text2, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return False
        return True

if __name__ == "__main__":
    game = Game()
    game.run()
