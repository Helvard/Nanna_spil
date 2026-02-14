import pygame
import random
import sys
import math

# Initialize
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1400, 800
FPS = 60
CELL_SIZE = 100  # Bigger cells for more detail

# Colors
SKY_BLUE = (135, 206, 250)
FOREST_GREEN = (34, 139, 34)
DARK_GREEN = (25, 80, 25)
PATH_BROWN = (139, 90, 43)
LIGHT_BROWN = (180, 140, 100)
GRASS_GREEN = (107, 142, 35)
PINK = (255, 182, 193)
DARK_PINK = (255, 105, 180)
HOT_PINK = (255, 20, 147)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)
GOLD = (255, 215, 0)
WOOD_BROWN = (101, 67, 33)
DARK_WOOD = (70, 40, 20)
LEAF_GREEN = (50, 205, 50)
RED = (220, 20, 60)
ORANGE = (255, 140, 0)

# Shape colors
SHAPE_COLORS = [(255, 100, 100), (100, 150, 255), (255, 230, 100), 
                (200, 100, 255), (255, 180, 100), (255, 150, 200)]

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bamse finder vej! 🧸")
clock = pygame.time.Clock()

# Fonts
huge_font = pygame.font.Font(None, 90)
big_font = pygame.font.Font(None, 70)
medium_font = pygame.font.Font(None, 55)
small_font = pygame.font.Font(None, 45)

# Small mazes (4-5 junctions)
SMALL_MAZES = [
    [
        ['1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', '0', 'J', '0', '1'],
        ['1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', '1', '1', '0', '1', '1'],
        ['1', '0', 'J', '0', '0', '1', '1'],
        ['1', '0', '1', '1', '1', '1', '1'],
        ['1', 'E', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1'],
    ],
    [
        ['1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', 'J', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1'],
        ['1', '1', '1', '0', 'J', '0', '1'],
        ['1', '1', '1', '1', '1', '0', '1'],
        ['1', '0', 'J', '0', '0', '0', '1'],
        ['1', 'E', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1'],
    ],
    [
        ['1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', '0', '0', 'J', '1', '1'],
        ['1', '1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', 'J', '0', '0', '0', '1', '1'],
        ['1', '1', '0', '1', '1', '1', '1', '1'],
        ['1', '1', 'E', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1'],
    ],
    [
        ['1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', 'J', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1'],
        ['1', '1', 'J', '0', '1', '1', '1'],
        ['1', '1', '0', '1', '1', '1', '1'],
        ['1', '1', '0', 'J', '0', '0', '1'],
        ['1', '1', '1', '1', '1', 'E', '1'],
        ['1', '1', '1', '1', '1', '1', '1'],
    ],
]

# Medium mazes (6-8 junctions)
MEDIUM_MAZES = [
    [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', '0', 'J', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '0', '1', '1', '1', '1'],
        ['1', '1', 'J', '0', '0', '1', '1', '1', '1'],
        ['1', '1', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '0', 'J', '0', '0', 'J', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', '0', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1'],
        ['1', '1', '1', 'E', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ],
    [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', '0', '0', '0', 'J', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', 'J', '0', '0', '0', '0', '1', '1'],
        ['1', '1', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '0', '0', 'J', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '0', '1', '1', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', 'J', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', '1', '1', '1', '1', 'E', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ],
    [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', 'J', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '0', 'J', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
        ['1', '1', 'J', '0', '0', '0', '1', '1', '1', '1'],
        ['1', '1', '0', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '0', 'J', '0', '0', '0', 'J', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', 'E', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ],
    [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', '0', '0', '0', 'J', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', '0', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1'],
        ['1', 'J', '0', '0', '1', '1', '1', '1', '1'],
        ['1', '0', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '0', '0', '0', 'J', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '0', '1', '1', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', '0', 'E', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ],
]

# Large mazes (9-12 junctions)
LARGE_MAZES = [
    [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', '0', 'J', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', 'J', '0', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '0', '0', 'J', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', '0', 'J', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', '0', '0', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '0', 'J', '0', '0', 'J', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', 'E', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ],
    [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', '0', '0', 'J', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'J', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '0', '0', 'J', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', 'J', '0', '0', '0', 'J', '1', '1', '1', '1', '1'],
        ['1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '1'],
        ['1', '1', '0', '0', 'J', '0', '0', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '0', '0', '0', '0', 'E', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ],
    [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', 'J', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '0', '0', 'J', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', '0', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'J', '0', '0', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '0', '0', 'J', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', 'J', '0', '0', '0', 'J', '1', '1', '1', '1'],
        ['1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1'],
        ['1', '1', '0', '0', 'J', '0', '0', '0', 'E', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ],
    [
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', 'S', '0', '0', '0', 'J', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', 'J', '0', '0', '0', 'J', '1', '1', '1', '1', '1'],
        ['1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '1'],
        ['1', '1', '0', '0', 'J', '0', '0', '1', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '1', 'J', '0', '0', '0', 'J', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
        ['1', '1', 'J', '0', '0', 'J', '0', '0', '1', '1', '1', '1'],
        ['1', '1', '0', '1', '1', '0', '1', '1', '1', '1', '1', '1'],
        ['1', '1', '0', '0', '0', '0', '0', '0', 'E', '1', '1', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ],
]

ALL_MAZES = SMALL_MAZES + MEDIUM_MAZES + LARGE_MAZES

def draw_tree(surface, x, y, size):
    """Draw a detailed tree"""
    # Trunk
    trunk_width = size // 4
    trunk_height = size // 2
    pygame.draw.rect(surface, WOOD_BROWN, 
                    (x - trunk_width // 2, y, trunk_width, trunk_height))
    pygame.draw.rect(surface, DARK_WOOD, 
                    (x - trunk_width // 2, y, trunk_width, trunk_height), 2)
    
    # Leaves - multiple layers
    leaf_colors = [FOREST_GREEN, LEAF_GREEN, DARK_GREEN]
    for i, color in enumerate(leaf_colors):
        offset = i * 8
        pygame.draw.circle(surface, color, (x, y - offset), size // 2)
    
    # Highlight
    pygame.draw.circle(surface, LEAF_GREEN, (x - size // 6, y - size // 3), size // 6)

def draw_flower(surface, x, y):
    """Draw a small flower"""
    # Petals
    petal_colors = [RED, YELLOW, PINK, ORANGE]
    color = random.choice(petal_colors)
    for angle in range(0, 360, 72):
        petal_x = x + math.cos(math.radians(angle)) * 5
        petal_y = y + math.sin(math.radians(angle)) * 5
        pygame.draw.circle(surface, color, (int(petal_x), int(petal_y)), 4)
    # Center
    pygame.draw.circle(surface, GOLD, (x, y), 3)

def draw_bear(surface, x, y, hop_offset, direction):
    """Draw a cute pink bear"""
    draw_y = y - hop_offset
    size = 35
    
    # Shadow
    pygame.draw.ellipse(surface, (0, 0, 0, 50), 
                       (x - size, y + size - 5, size * 2, 15))
    
    # Body
    pygame.draw.circle(surface, PINK, (int(x), int(draw_y)), size)
    pygame.draw.circle(surface, DARK_PINK, (int(x), int(draw_y)), size, 3)
    
    # Ears
    ear_size = size // 2
    pygame.draw.circle(surface, PINK, (int(x - size * 0.6), int(draw_y - size * 0.6)), ear_size)
    pygame.draw.circle(surface, PINK, (int(x + size * 0.6), int(draw_y - size * 0.6)), ear_size)
    pygame.draw.circle(surface, HOT_PINK, (int(x - size * 0.6), int(draw_y - size * 0.6)), ear_size // 2)
    pygame.draw.circle(surface, HOT_PINK, (int(x + size * 0.6), int(draw_y - size * 0.6)), ear_size // 2)
    
    # Face
    # Eyes
    eye_y = draw_y - 8
    pygame.draw.circle(surface, BLACK, (int(x - 12), int(eye_y)), 5)
    pygame.draw.circle(surface, BLACK, (int(x + 12), int(eye_y)), 5)
    pygame.draw.circle(surface, WHITE, (int(x - 10), int(eye_y - 2)), 2)
    pygame.draw.circle(surface, WHITE, (int(x + 14), int(eye_y - 2)), 2)
    
    # Nose
    pygame.draw.circle(surface, DARK_PINK, (int(x), int(draw_y + 5)), 6)
    
    # Smile
    pygame.draw.arc(surface, BLACK, (x - 10, draw_y, 20, 15), 0, math.pi, 2)
    
    # Direction indicator (small arrow/triangle)
    if direction == 'right':
        points = [(x + size + 5, draw_y), (x + size - 5, draw_y - 8), (x + size - 5, draw_y + 8)]
    elif direction == 'left':
        points = [(x - size - 5, draw_y), (x - size + 5, draw_y - 8), (x - size + 5, draw_y + 8)]
    elif direction == 'up':
        points = [(x, draw_y - size - 5), (x - 8, draw_y - size + 5), (x + 8, draw_y - size + 5)]
    else:  # down
        points = [(x, draw_y + size + 5), (x - 8, draw_y + size - 5), (x + 8, draw_y + size - 5)]
    pygame.draw.polygon(surface, DARK_PINK, points)

def draw_house(surface, x, y):
    """Draw a cute house"""
    house_w = 60
    house_h = 50
    
    # House body
    pygame.draw.rect(surface, (255, 200, 150), (x - house_w // 2, y - house_h, house_w, house_h))
    pygame.draw.rect(surface, DARK_WOOD, (x - house_w // 2, y - house_h, house_w, house_h), 3)
    
    # Roof
    roof_points = [(x - house_w // 2 - 10, y - house_h), 
                   (x + house_w // 2 + 10, y - house_h), 
                   (x, y - house_h - 30)]
    pygame.draw.polygon(surface, RED, roof_points)
    pygame.draw.polygon(surface, DARK_WOOD, roof_points, 3)
    
    # Door
    pygame.draw.rect(surface, WOOD_BROWN, (x - 10, y - 30, 20, 30))
    pygame.draw.circle(surface, GOLD, (x + 5, y - 15), 2)
    
    # Windows
    pygame.draw.rect(surface, SKY_BLUE, (x - 25, y - 35, 12, 12))
    pygame.draw.rect(surface, SKY_BLUE, (x + 13, y - 35, 12, 12))

def draw_girl(surface, x, y):
    """Draw a simple girl waving"""
    # Body
    pygame.draw.circle(surface, (255, 220, 180), (x, y - 20), 12)  # Head
    pygame.draw.rect(surface, (255, 100, 150), (x - 10, y - 8, 20, 25))  # Dress
    
    # Arms (one raised - waving)
    pygame.draw.line(surface, (255, 220, 180), (x - 10, y - 5), (x - 20, y - 15), 4)  # Left arm raised
    pygame.draw.line(surface, (255, 220, 180), (x + 10, y - 5), (x + 15, y + 5), 4)  # Right arm
    
    # Legs
    pygame.draw.line(surface, (255, 220, 180), (x - 5, y + 17), (x - 5, y + 30), 4)
    pygame.draw.line(surface, (255, 220, 180), (x + 5, y + 17), (x + 5, y + 30), 4)
    
    # Face
    pygame.draw.circle(surface, BLACK, (x - 4, y - 22), 2)  # Eyes
    pygame.draw.circle(surface, BLACK, (x + 4, y - 22), 2)
    pygame.draw.arc(surface, BLACK, (x - 5, y - 18, 10, 8), 0, math.pi, 2)  # Smile

class Shape:
    def __init__(self, shape_type, x, y, color, size=22, dimmed=False):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.dimmed = dimmed
        
    def draw(self, surface):
        draw_color = (100, 100, 100) if self.dimmed else self.color
        
        if self.shape_type == 'circle':
            pygame.draw.circle(surface, draw_color, (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.size, 2)
        elif self.shape_type == 'square':
            rect = pygame.Rect(int(self.x - self.size), int(self.y - self.size), 
                             self.size * 2, self.size * 2)
            pygame.draw.rect(surface, draw_color, rect, border_radius=3)
            pygame.draw.rect(surface, BLACK, rect, 2, border_radius=3)
        elif self.shape_type == 'star':
            points = []
            for i in range(10):
                angle = math.pi * 2 * i / 10 - math.pi / 2
                r = self.size if i % 2 == 0 else self.size * 0.4
                px = self.x + r * math.cos(angle)
                py = self.y + r * math.sin(angle)
                points.append((px, py))
            pygame.draw.polygon(surface, draw_color, points)
            pygame.draw.polygon(surface, BLACK, points, 2)
        elif self.shape_type == 'heart':
            pygame.draw.circle(surface, draw_color, (int(self.x - self.size//3), int(self.y - self.size//4)), self.size//2)
            pygame.draw.circle(surface, draw_color, (int(self.x + self.size//3), int(self.y - self.size//4)), self.size//2)
            points = [(self.x - self.size//1.5, self.y), (self.x + self.size//1.5, self.y), (self.x, self.y + self.size)]
            pygame.draw.polygon(surface, draw_color, points)

class MathQuestion:
    def __init__(self):
        self.type = random.choice(['count', 'plus', 'minus'])
        self.shape_type = random.choice(['circle', 'star', 'heart', 'square'])
        self.color = random.choice(SHAPE_COLORS)
        self.shapes = []
        
        if self.type == 'count':
            self.answer = random.randint(3, 8)
            self.text = "Hvor mange?"
            self.create_shapes(self.answer, 130)
        elif self.type == 'plus':
            self.num1 = random.randint(2, 4)
            self.num2 = random.randint(1, 3)
            self.answer = self.num1 + self.num2
            self.text = f"{self.num1} + {self.num2} = ?"
            self.create_shapes(self.num1, 110)
            self.create_shapes(self.num2, 110, x_offset=120)
        else:
            self.num1 = random.randint(5, 8)
            self.num2 = random.randint(1, min(3, self.num1 - 1))
            self.answer = self.num1 - self.num2
            self.text = f"{self.num1} - {self.num2} = ?"
            self.create_shapes(self.num1, 130)
            for i in range(self.num1 - self.num2, self.num1):
                self.shapes[i].dimmed = True
        
        self.options = [self.answer]
        possible = list(range(max(0, self.answer - 3), self.answer + 4))
        if self.answer in possible:
            possible.remove(self.answer)
        self.options.extend(random.sample(possible, min(3, len(possible))))
        random.shuffle(self.options)
    
    def create_shapes(self, count, y_center, x_offset=0):
        shapes_per_row = 4
        spacing = 50
        start_x = 130 + x_offset
        
        for i in range(count):
            row = i // shapes_per_row
            col = i % shapes_per_row
            x = start_x + col * spacing
            y = y_center + row * spacing
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)
            self.shapes.append(Shape(self.shape_type, x, y, self.color, size=20))

class AnswerButton:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y
        self.size = 45
        
    def draw(self, surface):
        pygame.draw.circle(surface, GOLD, (self.x, self.y), self.size)
        pygame.draw.circle(surface, BLACK, (self.x, self.y), self.size, 3)
        text = big_font.render(str(self.number), True, BLACK)
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)
    
    def is_clicked(self, pos, camera_x, camera_y):
        # Adjust for camera offset
        adjusted_pos = (pos[0] + camera_x, pos[1] + camera_y)
        dist = math.sqrt((adjusted_pos[0] - self.x)**2 + (adjusted_pos[1] - self.y)**2)
        return dist < self.size

class Bear:
    def __init__(self, grid_x, grid_y, maze):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.maze = maze
        self.x = grid_x * CELL_SIZE + CELL_SIZE // 2
        self.y = grid_y * CELL_SIZE + CELL_SIZE // 2
        self.direction = 'right'
        self.target_x = self.x
        self.target_y = self.y
        self.moving = False
        self.speed = 0
        self.max_speed = 3.0
        self.acceleration = 0.12
        self.deceleration = 0.2
        self.hop_offset = 0
        
    def start_moving_forward(self):
        self.moving = True
        dx, dy = self.get_direction_delta()
        
        steps = 1
        while True:
            next_x = self.grid_x + dx * steps
            next_y = self.grid_y + dy * steps
            
            if (next_y < 0 or next_y >= len(self.maze) or 
                next_x < 0 or next_x >= len(self.maze[0]) or
                self.maze[next_y][next_x] == '1'):
                steps -= 1
                break
            
            if self.maze[next_y][next_x] == 'J' or self.maze[next_y][next_x] == 'E':
                break
                
            steps += 1
        
        if steps > 0:
            self.target_x = (self.grid_x + dx * steps) * CELL_SIZE + CELL_SIZE // 2
            self.target_y = (self.grid_y + dy * steps) * CELL_SIZE + CELL_SIZE // 2
    
    def get_direction_delta(self):
        return {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}[self.direction]
    
    def turn(self, new_direction):
        self.direction = new_direction
    
    def update(self):
        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist < 50:
                self.speed = max(0, self.speed - self.deceleration)
            else:
                self.speed = min(self.max_speed, self.speed + self.acceleration)
            
            if dist < 1 or self.speed == 0:
                self.x = self.target_x
                self.y = self.target_y
                self.moving = False
                self.speed = 0
                self.grid_x = round(self.x / CELL_SIZE - 0.5)
                self.grid_y = round(self.y / CELL_SIZE - 0.5)
            else:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
                self.hop_offset = abs(math.sin(pygame.time.get_ticks() * 0.008)) * 12
        else:
            self.hop_offset = 0
    
    def draw(self, surface, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        draw_bear(surface, draw_x, draw_y, self.hop_offset, self.direction)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-8, -2)
        self.color = random.choice(SHAPE_COLORS)
        self.life = 50
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.35
        self.life -= 1
        
    def draw(self, surface, camera_x, camera_y):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x - camera_x), int(self.y - camera_y)), 5)

def find_positions(maze):
    start = junctions = end = None
    junctions = []
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            cell = maze[row][col]
            if cell == 'S':
                start = (col, row)
            elif cell == 'J':
                junctions.append((col, row))
            elif cell == 'E':
                end = (col, row)
    return start, junctions, end

def get_valid_directions(maze, grid_x, grid_y, current_direction):
    directions = []
    moves = [('up', 0, -1), ('down', 0, 1), ('left', -1, 0), ('right', 1, 0)]
    opposite = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    
    for direction, dx, dy in moves:
        if direction == opposite.get(current_direction):
            continue
        new_x, new_y = grid_x + dx, grid_y + dy
        if (0 <= new_y < len(maze) and 0 <= new_x < len(maze[0]) and maze[new_y][new_x] != '1'):
            directions.append(direction)
    return directions

def draw_sign(surface, question, answer_buttons, camera_x, camera_y):
    """Draw wooden sign with math problem"""
    # Position sign near bear but in view
    sign_x = 400 - camera_x
    sign_y = 200 - camera_y
    sign_width = 400
    sign_height = 380
    
    # Post
    pygame.draw.rect(surface, WOOD_BROWN, (sign_x + sign_width // 2 - 12, sign_y + sign_height, 24, 120))
    
    # Board
    pygame.draw.rect(surface, WOOD_BROWN, (sign_x, sign_y, sign_width, sign_height), border_radius=15)
    pygame.draw.rect(surface, DARK_WOOD, (sign_x, sign_y, sign_width, sign_height), 5, border_radius=15)
    
    # Decorative corners
    corner_size = 20
    for cx, cy in [(sign_x + 10, sign_y + 10), (sign_x + sign_width - 30, sign_y + 10),
                   (sign_x + 10, sign_y + sign_height - 30), (sign_x + sign_width - 30, sign_y + sign_height - 30)]:
        pygame.draw.rect(surface, DARK_WOOD, (cx, cy, corner_size, corner_size), border_radius=3)
    
    # Question text
    q_text = medium_font.render(question.text, True, WHITE)
    surface.blit(q_text, (sign_x + sign_width // 2 - q_text.get_width() // 2, sign_y + 25))
    
    # Shapes - offset for camera
    for shape in question.shapes:
        shape_surface_x = shape.x - camera_x
        shape_surface_y = shape.y - camera_y
        temp_shape = Shape(shape.shape_type, shape_surface_x, shape_surface_y, shape.color, shape.size, shape.dimmed)
        temp_shape.draw(surface)
    
    # Buttons
    for button in answer_buttons:
        button_surface_x = button.x - camera_x
        button_surface_y = button.y - camera_y
        temp_button = AnswerButton(button.number, button_surface_x, button_surface_y)
        temp_button.draw(surface)

def play_sound(sound_type):
    if sound_type == 'correct':
        sound = pygame.mixer.Sound(buffer=bytes([128 + int(50 * (i % 100) / 100) for i in range(1200)]))
        sound.play()
    elif sound_type == 'wrong':
        sound = pygame.mixer.Sound(buffer=bytes([128 - int(30 * (i % 50) / 50) for i in range(900)]))
        sound.play()
    elif sound_type == 'complete':
        sound = pygame.mixer.Sound(buffer=bytes([128 + int(80 * ((i * 3) % 200) / 200) for i in range(3000)]))
        sound.play()

# Initialize
chosen_maze = random.choice(ALL_MAZES)
start_pos, junction_positions, end_pos = find_positions(chosen_maze)
bear = Bear(start_pos[0], start_pos[1], chosen_maze)

# Game state
score = 0
visited_junctions = set()
showing_question = False
waiting_for_direction = False
direction_timer = 0
current_question = None
answer_buttons = []
correct_direction = None
particles = []
feedback_text = ""
feedback_timer = 0
game_won = False

# Camera
camera_x = 0
camera_y = 0

bear.start_moving_forward()

running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and showing_question:
            pos = pygame.mouse.get_pos()
            for button in answer_buttons:
                if button.is_clicked(pos, camera_x, camera_y):
                    if button.number == current_question.answer:
                        score += 10
                        play_sound('correct')
                        showing_question = False
                        waiting_for_direction = True
                        direction_timer = 90
                        for _ in range(20):
                            particles.append(Particle(button.x, button.y))
                    else:
                        score = max(0, score - 2)
                        feedback_text = "Prøv igen! 💭"
                        feedback_timer = 50
                        play_sound('wrong')
                    break
    
    bear.update()
    
    # Camera follows bear smoothly
    target_camera_x = bear.x - WIDTH // 2
    target_camera_y = bear.y - HEIGHT // 2
    camera_x += (target_camera_x - camera_x) * 0.1
    camera_y += (target_camera_y - camera_y) * 0.1
    
    # Clamp camera to maze bounds
    maze_pixel_width = len(chosen_maze[0]) * CELL_SIZE
    maze_pixel_height = len(chosen_maze) * CELL_SIZE
    camera_x = max(0, min(camera_x, maze_pixel_width - WIDTH))
    camera_y = max(0, min(camera_y, maze_pixel_height - HEIGHT))
    
    if not bear.moving and not showing_question and not waiting_for_direction and not game_won:
        current_pos = (bear.grid_x, bear.grid_y)
        
        if current_pos == end_pos:
            game_won = True
            play_sound('complete')
            for _ in range(50):
                particles.append(Particle(bear.x, bear.y))
        elif current_pos in junction_positions and current_pos not in visited_junctions:
            visited_junctions.add(current_pos)
            showing_question = True
            current_question = MathQuestion()
            
            valid_dirs = get_valid_directions(chosen_maze, bear.grid_x, bear.grid_y, bear.direction)
            if valid_dirs:
                correct_direction = random.choice(valid_dirs)
            
            # Position question near bear
            sign_world_x = bear.x - 200
            sign_world_y = bear.y - 150
            
            answer_buttons = []
            for i, num in enumerate(current_question.options):
                x = sign_world_x + 120 + (i % 2) * 90
                y = sign_world_y + 270 + (i // 2) * 90
                answer_buttons.append(AnswerButton(num, x, y))
    
    if waiting_for_direction:
        direction_timer -= 1
        if direction_timer <= 0:
            waiting_for_direction = False
            bear.turn(correct_direction)
            bear.start_moving_forward()
    
    for particle in particles[:]:
        particle.update()
        if particle.life <= 0:
            particles.remove(particle)
    
    if feedback_timer > 0:
        feedback_timer -= 1
    
    # Draw
    screen.fill(GRASS_GREEN)
    
    # Draw maze
    for row in range(len(chosen_maze)):
        for col in range(len(chosen_maze[0])):
            x = col * CELL_SIZE - camera_x
            y = row * CELL_SIZE - camera_y
            cell = chosen_maze[row][col]
            
            if cell == '1':
                draw_tree(screen, x + CELL_SIZE // 2, y + CELL_SIZE // 2, CELL_SIZE - 10)
            else:
                # Path
                pygame.draw.rect(screen, PATH_BROWN, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, LIGHT_BROWN, (x, y, CELL_SIZE, CELL_SIZE), 2)
                
                # Add flowers
                if random.random() < 0.1:
                    draw_flower(screen, x + random.randint(10, CELL_SIZE - 10), 
                               y + random.randint(10, CELL_SIZE - 10))
            
            if cell == 'E':
                draw_house(screen, x + CELL_SIZE // 2, y + CELL_SIZE)
                draw_girl(screen, x + CELL_SIZE // 2 - 40, y + CELL_SIZE // 2 + 10)
    
    bear.draw(screen, camera_x, camera_y)
    
    if showing_question:
        draw_sign(screen, current_question, answer_buttons, camera_x, camera_y)
    
    for particle in particles:
        particle.draw(screen, camera_x, camera_y)
    
    # UI Overlay
    if waiting_for_direction:
        dir_text = {'up': 'Kør OPAD! ⬆️', 'down': 'Kør NEDAD! ⬇️', 
                   'left': 'Kør VENSTRE! ⬅️', 'right': 'Kør HØJRE! ➡️'}
        direction_surf = big_font.render(dir_text.get(correct_direction, ''), True, WHITE)
        bg_rect = direction_surf.get_rect(center=(WIDTH // 2, 50))
        bg_rect.inflate_ip(40, 20)
        pygame.draw.rect(screen, FOREST_GREEN, bg_rect, border_radius=15)
        pygame.draw.rect(screen, GOLD, bg_rect, 4, border_radius=15)
        screen.blit(direction_surf, direction_surf.get_rect(center=(WIDTH // 2, 50)))
    
    # Score
    score_text = medium_font.render(f"Point: {score}", True, WHITE)
    score_bg = score_text.get_rect(topleft=(15, 15))
    score_bg.inflate_ip(20, 15)
    pygame.draw.rect(screen, FOREST_GREEN, score_bg, border_radius=10)
    pygame.draw.rect(screen, GOLD, score_bg, 3, border_radius=10)
    screen.blit(score_text, (25, 20))
    
    if feedback_timer > 0:
        feedback_surf = big_font.render(feedback_text, True, RED)
        feedback_bg = feedback_surf.get_rect(center=(WIDTH // 2, 120))
        feedback_bg.inflate_ip(30, 20)
        pygame.draw.rect(screen, WHITE, feedback_bg, border_radius=12)
        screen.blit(feedback_surf, feedback_surf.get_rect(center=(WIDTH // 2, 120)))
    
    if game_won:
        win_text = huge_font.render("BAMSEN FANDT PIGEN! 🎉🧸", True, GOLD)
        win_bg = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win_bg.inflate_ip(50, 40)
        pygame.draw.rect(screen, FOREST_GREEN, win_bg, border_radius=20)
        pygame.draw.rect(screen, GOLD, win_bg, 6, border_radius=20)
        screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    
    pygame.display.flip()

pygame.quit()
sys.exit()