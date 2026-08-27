import pygame

class Platform:
    def __init__(self, x, y, width, height, platform_type="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platform_type = platform_type
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        if self.platform_type == "normal":
            pygame.draw.rect(screen, (100, 100, 150), self.rect)
            pygame.draw.rect(screen, (150, 150, 200), self.rect, 2)  # Border
        elif self.platform_type == "moving":
            pygame.draw.rect(screen, (150, 100, 50), self.rect)
            pygame.draw.rect(screen, (200, 150, 100), self.rect, 2)
        elif self.platform_type == "spike":
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
            for i in range(0, self.width, 10):
                pygame.draw.polygon(screen, (255, 100, 100), [(self.x + i, self.y), (self.x + i + 5, self.y - 5), (self.x + i + 10, self.y)])
