import pygame
import math

class Arrow:
    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.vel_x = vel_x * 8  # Speed multiplier
        self.vel_y = vel_y * 8
        self.width = 15
        self.height = 5
        self.damage = 20
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
    
    def collides_with(self, other):
        """Check collision with monster"""
        arrow_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        monster_rect = pygame.Rect(other.x - other.width // 2, other.y - other.height // 2, other.width, other.height)
        return arrow_rect.colliderect(monster_rect)
    
    def draw(self, screen):
        # Draw arrow
        pygame.draw.line(screen, (255, 200, 0), (int(self.x - self.width // 2), int(self.y)), (int(self.x + self.width // 2), int(self.y)), 3)
        # Arrow tip
        pygame.draw.polygon(screen, (255, 200, 0), [(int(self.x + self.width // 2), int(self.y)), (int(self.x + self.width // 2 + 4), int(self.y - 3)), (int(self.x + self.width // 2 + 4), int(self.y + 3))])
