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
        self.speed = 1.5
        self.health = 30
        self.max_health = 30
        self.reward = 50
        self.attack_cooldown = 0
        
        # Different monster types
        if monster_type == "goblin":
            self.health = 30
            self.max_health = 30
            self.speed = 2
            self.color = (0, 150, 0)
            self.reward = 50
        elif monster_type == "orc":
            self.health = 60
            self.max_health = 60
            self.speed = 1.2
            self.color = (100, 100, 0)
            self.reward = 100
        elif monster_type == "skeleton":
            self.health = 40
            self.max_health = 40
            self.speed = 1.8
            self.color = (200, 200, 200)
            self.reward = 75
    
    def update(self, player):
        """Move towards player"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
    
    def take_damage(self, amount):
        self.health -= amount
    
    def draw(self, screen):
        # Draw body
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
        
        # Draw eyes
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x - 7), int(self.y - 5)), 3)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x + 7), int(self.y - 5)), 3)
        
        # Health bar
        bar_width = 30
        bar_height = 4
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (200, 0, 0), (self.x - bar_width // 2, self.y - 25, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (self.x - bar_width // 2, self.y - 25, bar_width * health_ratio, bar_height))
