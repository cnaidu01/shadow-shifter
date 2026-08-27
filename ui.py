import pygame

class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def draw(self, screen, player, score, level, enemies_remaining):
        # Form indicator
        form_text = f"Form: {player.form.upper()}"
        form_color = (100, 0, 150) if player.form == "shadow" else (0, 100, 200)
        text = self.font_small.render(form_text, True, form_color)
        screen.blit(text, (10, 10))
        
        # Controls hint
        controls = "WASD: Move | E: Shift Form | Click: Attack"
        text = self.font_small.render(controls, True, (200, 200, 200))
        screen.blit(text, (10, 40))
        
        # Health display
        health_text = f"Health: {int(player.health)}/{player.max_health}"
        text = self.font_small.render(health_text, True, (200, 0, 0))
        screen.blit(text, (10, 70))
        
        # Score
        score_text = f"Score: {score}"
        text = self.font_small.render(score_text, True, (0, 200, 0))
        screen.blit(text, (800, 10))
        
        # Level
        level_text = f"Level: {level}"
        text = self.font_small.render(level_text, True, (0, 200, 0))
        screen.blit(text, (800, 40))
        
        # Enemies remaining
        enemies_text = f"Enemies: {enemies_remaining}"
        text = self.font_small.render(enemies_text, True, (200, 0, 0))
        screen.blit(text, (800, 70))
