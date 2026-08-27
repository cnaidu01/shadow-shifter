import random
from monster import Monster

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.difficulty = 1 + (level_number - 1) * 0.5
    
    def spawn_monsters(self):
        """Spawn monsters based on level"""
        monsters = []
        num_monsters = 3 + int(self.level_number * 2)
        
        for i in range(num_monsters):
            x = random.randint(100, 900)
            y = random.randint(100, 600)
            
            # Vary monster types by level
            if self.level_number < 3:
                monster_type = "goblin"
            elif self.level_number < 6:
                monster_type = random.choice(["goblin", "orc"])
            else:
                monster_type = random.choice(["goblin", "orc", "skeleton"])
            
            monsters.append(Monster(x, y, monster_type))
        
        return monsters
