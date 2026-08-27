import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.form = "warrior"  # warrior or shadow
        self.health = 100
        self.max_health = 100
        self.form_cooldown = 0
        self.arrow_cooldown = 0
        self.on_ground = False
        self.jump_power = 15
        self.level = 1
        self.characters_unlocked = ["warrior"]
    
    def move(self, dx, dy, platforms):
        """Move with collision detection"""
        test_x = self.x + dx
        test_y = self.y + dy
        
        # Check collision with platforms
        can_move = True
        if self.form == "warrior":
            test_rect = pygame.Rect(test_x - self.width // 2, test_y - self.height // 2, self.width, self.height)
            for platform in platforms:
                if test_rect.colliderect(platform.rect):
                    can_move = False
                    break
        
        if can_move:
            self.x = test_x
            self.y = test_y
    
    def jump(self):
        """Jump (only when on ground)"""
        if self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
    
    def toggle_form(self):
        """Switch between warrior and shadow form"""
        if self.form_cooldown <= 0:
            self.form = "shadow" if self.form == "warrior" else "warrior"
            self.form_cooldown = 30
    
    def shoot_arrow(self):
        """Shoot arrow from player position"""
        if self.arrow_cooldown <= 0:
            from arrow import Arrow
            arrow = Arrow(self.x, self.y - 10, 1, 0)  # Shoot right
            self.arrow_cooldown = 15  # Arrow fire rate
            return arrow
        return None
    
    def apply_gravity(self, gravity, platforms, screen_height):
        """Apply gravity and handle collisions"""
        self.vel_y += gravity
        self.on_ground = False
        
        # Apply vertical velocity
        test_y = self.y + self.vel_y
        test_rect = pygame.Rect(self.x - self.width // 2, test_y - self.height // 2, self.width, self.height)
        
        # Check collision with platforms
        for platform in platforms:
            if test_rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.y = platform.rect.top + self.height // 2
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping
                    self.y = platform.rect.bottom - self.height // 2
                    self.vel_y = 0
        
        # No collision, apply velocity
        if not self.on_ground:
            self.y = test_y
        
        # Fall off screen = death
        if self.y > screen_height:
            self.health = 0
    
    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
    
    def update(self):
        self.form_cooldown = max(0, self.form_cooldown - 1)
        self.arrow_cooldown = max(0, self.arrow_cooldown - 1)
    
    def draw(self, screen):
        self.update()
        
        if self.form == "warrior":
            # Blue warrior
            pygame.draw.rect(screen, (0, 150, 255), (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
            # Head
            pygame.draw.circle(screen, (255, 200, 100), (int(self.x), int(self.y - 25)), 8)
            # Bow indicator
            pygame.draw.line(screen, (100, 50, 0), (int(self.x + 10), int(self.y - 10)), (int(self.x + 20), int(self.y - 10)), 3)
        else:
            # Purple shadow - can pass through walls
            pygame.draw.rect(screen, (150, 50, 200), (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
            pygame.draw.circle(screen, (150, 50, 200), (int(self.x), int(self.y - 25)), 8)
            # Shadow effect
            pygame.draw.ellipse(screen, (100, 0, 150), (self.x - 15, self.y + 15, 30, 6))
        
        # Health bar
        bar_width = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (200, 0, 0), (self.x - bar_width // 2, self.y - 35, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (self.x - bar_width // 2, self.y - 35, bar_width * health_ratio, bar_height))
