import pygame
import random
import sys
import math

# Initialize
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (20, 30, 80)  # Mørkeblå baggrund
LIGHT_GRAY = (180, 180, 180)
GRAY = (120, 120, 120)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
BLUE = (100, 150, 255)
YELLOW = (255, 230, 100)
PURPLE = (200, 100, 255)
ORANGE = (255, 180, 100)
PINK = (255, 150, 200)

SHAPE_COLORS = [RED, BLUE, YELLOW, PURPLE, ORANGE, PINK]

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tæl og Regn! 🔢")
clock = pygame.time.Clock()

# Fonts
huge_font = pygame.font.Font(None, 120)
big_font = pygame.font.Font(None, 100)
medium_font = pygame.font.Font(None, 80)

# Game state
score = 0
feedback_text = ""
feedback_timer = 0
current_question = None
celebration_particles = []

class Shape:
    def __init__(self, shape_type, x, y, color, size=40, dimmed=False):
        self.shape_type = shape_type  # 'circle', 'star', 'heart', 'square'
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.scale = 1.0
        self.dimmed = dimmed  # For shapes to subtract
        
    def draw(self):
        # Small bounce animation
        bounce = math.sin(pygame.time.get_ticks() / 200) * 0.05
        current_size = int(self.size * (self.scale + bounce))
        
        # Use gray color if dimmed (for minus operations)
        draw_color = GRAY if self.dimmed else self.color
        
        if self.shape_type == 'circle':
            pygame.draw.circle(screen, draw_color, (int(self.x), int(self.y)), current_size)
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), current_size, 3)
            
        elif self.shape_type == 'square':
            rect = pygame.Rect(int(self.x - current_size), int(self.y - current_size), 
                             current_size * 2, current_size * 2)
            pygame.draw.rect(screen, draw_color, rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, rect, 3, border_radius=5)
            
        elif self.shape_type == 'star':
            self.draw_star(self.x, self.y, current_size, draw_color)
            
        elif self.shape_type == 'heart':
            self.draw_heart(self.x, self.y, current_size, draw_color)
    
    def draw_star(self, x, y, size, color):
        points = []
        for i in range(10):
            angle = math.pi * 2 * i / 10 - math.pi / 2
            if i % 2 == 0:
                r = size
            else:
                r = size * 0.4
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 3)
    
    def draw_heart(self, x, y, size, color):
        # Simple heart shape using circles and triangle
        # Top left circle
        pygame.draw.circle(screen, color, (int(x - size//3), int(y - size//4)), size//2)
        # Top right circle
        pygame.draw.circle(screen, color, (int(x + size//3), int(y - size//4)), size//2)
        # Bottom triangle
        points = [
            (x - size//1.5, y),
            (x + size//1.5, y),
            (x, y + size)
        ]
        pygame.draw.polygon(screen, color, points)
        # Outline
        pygame.draw.circle(screen, BLACK, (int(x - size//3), int(y - size//4)), size//2, 3)
        pygame.draw.circle(screen, BLACK, (int(x + size//3), int(y - size//4)), size//2, 3)
        pygame.draw.polygon(screen, BLACK, points, 3)

class AnswerButton:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y
        self.size = 100
        self.color = BLUE
        
    def draw(self):
        # Draw button
        rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2,
                          self.size, self.size)
        pygame.draw.rect(screen, self.color, rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, rect, 4, border_radius=15)
        
        # Draw number
        text = huge_font.render(str(self.number), True, WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
    
    def is_clicked(self, pos):
        distance = ((pos[0] - self.x)**2 + (pos[1] - self.y)**2)**0.5
        return distance < self.size / 1.5

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-8, -3)
        self.color = random.choice(SHAPE_COLORS)
        self.life = 60
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.life -= 1
        
    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 6)

class Question:
    def __init__(self):
        self.question_type = random.choice(['count', 'plus', 'minus'])
        self.shape_type = random.choice(['circle', 'star', 'heart', 'square'])
        self.color = random.choice(SHAPE_COLORS)
        self.shapes = []
        self.answer_buttons = []
        
        if self.question_type == 'count':
            # Just count shapes
            self.answer = random.randint(3, 10)
            self.text = f"Hvor mange?"
            self.create_shapes(self.answer, 250)
            
        elif self.question_type == 'plus':
            # Show some, add some more
            self.num1 = random.randint(2, 5)
            self.num2 = random.randint(1, 4)
            self.answer = self.num1 + self.num2
            self.text = f"{self.num1} + {self.num2} = ?"
            # Show first group
            self.create_shapes(self.num1, 200)
            # Show second group (slightly offset)
            self.create_shapes(self.num2, 200, x_offset=400)
            
        else:  # minus
            # Show some, mark some as dimmed (to subtract)
            self.num1 = random.randint(5, 10)
            self.num2 = random.randint(1, min(4, self.num1 - 1))
            self.answer = self.num1 - self.num2
            self.text = f"{self.num1} - {self.num2} = ?"
            # Show all shapes
            self.create_shapes(self.num1, 250)
            # Mark last num2 shapes as dimmed
            for i in range(self.num1 - self.num2, self.num1):
                self.shapes[i].dimmed = True
        
        # Create answer buttons
        self.create_answer_buttons()
    
    def create_shapes(self, count, y_center, x_offset=0):
        # Arrange shapes in rows
        shapes_per_row = 5
        spacing = 80
        start_x = 250 + x_offset
        
        for i in range(count):
            row = i // shapes_per_row
            col = i % shapes_per_row
            x = start_x + col * spacing
            y = y_center + row * spacing
            # Add some randomness
            x += random.randint(-10, 10)
            y += random.randint(-10, 10)
            self.shapes.append(Shape(self.shape_type, x, y, self.color, size=35))
    
    def create_answer_buttons(self):
        # Create 4 answer options
        correct = self.answer
        options = [correct]
        
        # Add 3 wrong answers
        possible = list(range(max(0, correct - 3), correct + 4))
        possible.remove(correct)
        options.extend(random.sample(possible, min(3, len(possible))))
        
        random.shuffle(options)
        
        # Position buttons
        button_y = 550
        spacing = 150
        start_x = WIDTH // 2 - (len(options) * spacing) // 2 + spacing // 2
        
        for i, num in enumerate(options):
            x = start_x + i * spacing
            self.answer_buttons.append(AnswerButton(num, x, button_y))
    
    def draw(self):
        # Draw question text
        question_text = big_font.render(self.text, True, WHITE)
        screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 30))
        
        # Draw shapes
        for shape in self.shapes:
            shape.draw()
        
        # Draw answer buttons
        for button in self.answer_buttons:
            button.draw()

def play_sound(sound_type):
    if sound_type == 'correct':
        sound = pygame.mixer.Sound(buffer=bytes([128 + int(50 * (i % 100) / 100) for i in range(1000)]))
        sound.play()
    elif sound_type == 'wrong':
        sound = pygame.mixer.Sound(buffer=bytes([128 - int(30 * (i % 50) / 50) for i in range(800)]))
        sound.play()
    elif sound_type == 'complete':
        sound = pygame.mixer.Sound(buffer=bytes([128 + int(80 * ((i * 3) % 200) / 200) for i in range(2000)]))
        sound.play()

# Start first question
current_question = Question()

# Game loop
running = True

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Check answer buttons
            for button in current_question.answer_buttons:
                if button.is_clicked(pos):
                    if button.number == current_question.answer:
                        score += 10
                        feedback_text = "RIGTIGT! 🌟"
                        feedback_timer = 90
                        play_sound('complete')
                        
                        # Celebration particles
                        for _ in range(20):
                            celebration_particles.append(
                                Particle(WIDTH // 2, 300)
                            )
                        
                        # New question after delay
                        pygame.time.set_timer(pygame.USEREVENT, 1500, True)
                    else:
                        score = max(0, score - 3)
                        feedback_text = "Prøv igen! 💭"
                        feedback_timer = 60
                        play_sound('wrong')
                    break
        
        if event.type == pygame.USEREVENT:
            current_question = Question()
    
    # Update particles
    for particle in celebration_particles[:]:
        particle.update()
        if particle.life <= 0:
            celebration_particles.remove(particle)
    
    # Draw everything
    screen.fill(DARK_BLUE)  # Mørkeblå baggrund
    
    # Draw current question
    current_question.draw()
    
    # Draw score
    score_text = medium_font.render(f"Point: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 250, 30))
    
    # Draw particles
    for particle in celebration_particles:
        particle.draw()
    
    # Draw feedback
    if feedback_timer > 0:
        color = GREEN if "RIGTIGT" in feedback_text else RED
        feedback_surf = big_font.render(feedback_text, True, color)
        feedback_rect = feedback_surf.get_rect(center=(WIDTH // 2, 650))
        screen.blit(feedback_surf, feedback_rect)
        feedback_timer -= 1
    
    pygame.display.flip()

pygame.quit()
sys.exit()