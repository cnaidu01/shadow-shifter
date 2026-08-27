import pygame

class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 22)
    
    def draw(self, screen, player, score, level, enemies_remaining):
        # Form indicator
        form_text = f"Form: {player.form.upper()}"
        form_color = (150, 50, 200) if player.form == "shadow" else (0, 150, 255)
        text = self.font_small.render(form_text, True, form_color)
        screen.blit(text, (10, 10))
        
        # Controls hint
        controls = "A/D: Move | W: Jump | E: Shadow Form | SPACE/CLICK: Shoot"
        text = self.font_small.render(controls, True, (200, 200, 200))
        screen.blit(text, (10, 35))
        
        # Health display
        health_text = f"Health: {int(player.health)}/{player.max_health}"
        text = self.font_small.render(health_text, True, (200, 0, 0))
        screen.blit(text, (10, 60))
        
        # Score
        score_text = f"Score: {score}"
        text = self.font_small.render(score_text, True, (0, 200, 0))
        screen.blit(text, (1000, 10))
        
        # Level
        level_text = f"Level: {level}"
        text = self.font_small.render(level_text, True, (0, 200, 0))
        screen.blit(text, (1000, 35))
        
        # Enemies remaining
        enemies_text = f"Enemies: {enemies_remaining}"
        text = self.font_small.render(enemies_text, True, (200, 0, 0))
        screen.blit(text, (1000, 60))
