import random
from platform import Platform
from monster import Monster

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.difficulty = 1 + (level_number - 1) * 0.3
    
    def create_platforms(self, screen_width, screen_height):
        """Create platformer level layout"""
        platforms = []
        
        # Ground platform
        platforms.append(Platform(0, screen_height - 50, screen_width, 50, "normal"))
        
        # Level 1 - Simple platformer
        if self.level_number == 1:
            platforms.append(Platform(200, screen_height - 150, 150, 20, "normal"))
            platforms.append(Platform(500, screen_height - 200, 150, 20, "normal"))
            platforms.append(Platform(800, screen_height - 150, 150, 20, "normal"))
            platforms.append(Platform(1050, screen_height - 100, 150, 20, "normal"))
        
        # Level 2 - More complex
        elif self.level_number == 2:
            platforms.append(Platform(150, screen_height - 150, 100, 20, "normal"))
            platforms.append(Platform(350, screen_height - 200, 100, 20, "normal"))
            platforms.append(Platform(550, screen_height - 250, 100, 20, "normal"))
            platforms.append(Platform(750, screen_height - 200, 100, 20, "normal"))
            platforms.append(Platform(950, screen_height - 150, 100, 20, "normal"))
            platforms.append(Platform(100, screen_height - 300, 150, 20, "normal"))
        
        # Level 3+ - Crazy platforming
        else:
            for i in range(3, 10):
                x = random.randint(50, screen_width - 150)
                y = screen_height - (i * 100)
                platforms.append(Platform(x, y, random.randint(100, 150), 20, "normal"))
        
        return platforms
    
    def spawn_monsters(self, screen_width, screen_height):
        """Spawn monsters on platforms"""
        monsters = []
        num_monsters = 3 + int(self.level_number * 1.5)
        
        monster_types = ["goblin"]
        if self.level_number > 1:
            monster_types.append("orc")
        if self.level_number > 3:
            monster_types.append("skeleton")
        
        for i in range(num_monsters):
            x = random.randint(200, screen_width - 200)
            y = random.randint(100, screen_height - 150)
            monster_type = random.choice(monster_types)
            monsters.append(Monster(x, y, monster_type))
        
        return monsters
