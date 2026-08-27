import pygame
import math
import random

class Monster:
    def __init__(self, x, y, monster_type="goblin"):
        self.x = x
        self.y = y
        self.monster_type = monster_type
        self.width = 25
        self.height = 30
        self.vel_x = 0
        self.vel_y = 0
        self.health = 30
        self.max_health = 30
        self.reward = 50
        self.on_ground = False
        self.direction = random.choice([-1, 1])  # Left or right
        
        # Different monster types
        if monster_type == "goblin":
            self.health = 30
            self.max_health = 30
            self.speed = 1.5
            self.color = (0, 180, 0)
            self.reward = 50
        elif monster_type == "orc":
            self.health = 60
            self.max_health = 60
            self.speed = 1.0
            self.color = (150, 100, 0)
            self.reward = 100
        elif monster_type == "skeleton":
            self.health = 40
            self.max_health = 40
            self.speed = 1.8
            self.color = (200, 200, 200)
            self.reward = 75
    
    def update(self, platforms, screen_height):
        """Update monster position with gravity and platforming"""
        # Move horizontally
        self.x += self.speed * self.direction
        
        # Apply gravity
        self.vel_y += 0.6
        self.on_ground = False
        
        # Check platform collisions
        test_rect = pygame.Rect(self.x - self.width // 2, self.y + self.vel_y - self.height // 2, self.width, self.height)
        for platform in platforms:
            if test_rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.y = platform.rect.top + self.height // 2
                    self.vel_y = 0
                    self.on_ground = True
                    # Random jump
                    if random.random() > 0.95:
                        self.vel_y = -10
        
        # Apply vertical velocity
        if not self.on_ground:
            self.y += self.vel_y
        
        # Fall off screen
        if self.y > screen_height:
            self.health = 0
        
        # Change direction randomly or at edges
        if random.random() > 0.98:
            self.direction *= -1
    
    def take_damage(self, amount):
        self.health -= amount
    
    def draw(self, screen):
        # Draw body
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
        
        # Draw eyes
        eye_color = (255, 0, 0) if self.monster_type != "skeleton" else (0, 0, 0)
        pygame.draw.circle(screen, eye_color, (int(self.x - 7), int(self.y - 5)), 2)
        pygame.draw.circle(screen, eye_color, (int(self.x + 7), int(self.y - 5)), 2)
        
        # Health bar
        bar_width = 30
        bar_height = 4
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (200, 0, 0), (self.x - bar_width // 2, self.y - 25, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (self.x - bar_width // 2, self.y - 25, bar_width * health_ratio, bar_height))
