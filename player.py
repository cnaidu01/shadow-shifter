import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.form = "warrior"  # warrior or shadow
        self.health = 100
        self.max_health = 100
        self.form_cooldown = 0
        self.attack_cooldown = 0
        self.level = 1
        self.exp = 0
        self.characters_unlocked = ["warrior"]  # Start with warrior
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def toggle_form(self):
        """Switch between warrior and shadow form"""
        if self.form_cooldown <= 0:
            self.form = "shadow" if self.form == "warrior" else "warrior"
            self.form_cooldown = 30  # 0.5 seconds at 60 FPS
    
    def attack(self, monsters):
        """Attack nearby monsters in warrior form"""
        if self.attack_cooldown <= 0 and self.form == "warrior":
            for monster in monsters:
                if self.distance_to(monster) < 60:  # Attack range
                    damage = 15
                    monster.take_damage(damage)
                    self.attack_cooldown = 20  # Attack speed
    
    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    
    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)
    
    def update(self):
        self.form_cooldown = max(0, self.form_cooldown - 1)
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
    
    def draw(self, screen):
        self.update()
        
        if self.form == "warrior":
            # Blue warrior
            pygame.draw.rect(screen, (0, 100, 200), (self.x - 15, self.y - 20, self.width, self.height))
            # Head
            pygame.draw.circle(screen, (200, 180, 150), (int(self.x), int(self.y - 25)), 8)
        else:
            # Purple/dark shadow
            pygame.draw.rect(screen, (100, 0, 150), (self.x - 15, self.y - 20, self.width, self.height))
            pygame.draw.circle(screen, (100, 0, 150), (int(self.x), int(self.y - 25)), 8)
            # Shadow effect
            pygame.draw.ellipse(screen, (50, 0, 100), (self.x - 20, self.y + 15, 40, 8))
        
        # Health bar
        bar_width = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (200, 0, 0), (self.x - bar_width // 2, self.y - 35, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (self.x - bar_width // 2, self.y - 35, bar_width * health_ratio, bar_height))
