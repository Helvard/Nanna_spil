import pygame
import random
import sys

# Initialize
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
GRAY = (150, 150, 150)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
BLUE = (100, 150, 255)
YELLOW = (255, 230, 100)
PURPLE = (200, 100, 255)

LETTER_COLORS = [BLUE, PURPLE, (255, 150, 100), (100, 200, 255)]

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stav Navne! 📝")
clock = pygame.time.Clock()

# Fonts
huge_font = pygame.font.Font(None, 140)
big_font = pygame.font.Font(None, 100)
medium_font = pygame.font.Font(None, 70)
box_font = pygame.font.Font(None, 90)

# Names list
NAMES = [
    "ERIK", "URSULA", "BERTIL", "OSKAR", "NANNA", 
    "LARS", "MATHILDE", "TILDE", "WILMA", "SILJE",
    "ALFRED", "PETER", "MARIE", "MORFAR", "MORMOR",
    "IBEN", "JONATHAN", "EVA"
]

# Game state
current_name = ""
typed_letters = []
available_letters = []
score = 0
feedback_text = ""
feedback_timer = 0
celebration_particles = []

class LetterButton:
    def __init__(self, letter, x, y):
        self.letter = letter
        self.x = x
        self.y = y
        self.size = 90
        self.color = random.choice(LETTER_COLORS)
        self.used = False
        
    def draw(self):
        if self.used:
            return
            
        # Draw button background
        rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, 
                          self.size, self.size)
        pygame.draw.rect(screen, self.color, rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, rect, 3, border_radius=15)
        
        # Draw letter
        text = big_font.render(self.letter, True, WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
        
    def is_clicked(self, pos):
        if self.used:
            return False
        distance = ((pos[0] - self.x)**2 + (pos[1] - self.y)**2)**0.5
        return distance < self.size / 2

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-8, -3)
        self.color = random.choice([YELLOW, GREEN, BLUE, PURPLE, RED])
        self.life = 60
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # Gravity
        self.life -= 1
        
    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

def new_name():
    global current_name, typed_letters, available_letters, celebration_particles
    
    current_name = random.choice(NAMES)
    typed_letters = []
    celebration_particles = []
    
    # Create letter buttons
    letters_needed = list(current_name)
    
    # Add some extra random letters to make it challenging
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    extra_letters = random.sample([l for l in alphabet if l not in current_name], 
                                   min(5, 26 - len(set(current_name))))
    
    all_letters = letters_needed + extra_letters
    random.shuffle(all_letters)
    
    # Position buttons in a grid at bottom
    available_letters = []
    buttons_per_row = 8
    start_x = 150
    start_y = 550
    spacing = 120
    
    for i, letter in enumerate(all_letters):
        row = i // buttons_per_row
        col = i % buttons_per_row
        x = start_x + col * spacing
        y = start_y + row * spacing
        available_letters.append(LetterButton(letter, x, y))

def play_sound(sound_type):
    if sound_type == 'correct':
        sound = pygame.mixer.Sound(buffer=bytes([128 + int(50 * (i % 100) / 100) for i in range(1000)]))
        sound.play()
    elif sound_type == 'wrong':
        sound = pygame.mixer.Sound(buffer=bytes([128 - int(30 * (i % 50) / 50) for i in range(800)]))
        sound.play()
    elif sound_type == 'complete':
        # Celebration sound
        sound = pygame.mixer.Sound(buffer=bytes([128 + int(80 * ((i * 3) % 200) / 200) for i in range(2000)]))
        sound.play()

# Initialize first name
new_name()

# Game loop
running = True

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Check if a letter button was clicked
            for button in available_letters:
                if button.is_clicked(pos):
                    # Check if it's the correct next letter
                    expected_letter = current_name[len(typed_letters)]
                    
                    if button.letter == expected_letter:
                        typed_letters.append(button.letter)
                        button.used = True
                        play_sound('correct')
                        
                        # Check if name is complete
                        if len(typed_letters) == len(current_name):
                            score += 20
                            feedback_text = "PERFEKT! 🎉"
                            feedback_timer = 120
                            play_sound('complete')
                            
                            # Create celebration particles
                            for _ in range(30):
                                celebration_particles.append(
                                    Particle(WIDTH // 2, 250)
                                )
                            
                            # Wait then new name
                            pygame.time.set_timer(pygame.USEREVENT, 2000, True)
                        else:
                            feedback_text = "Godt! ⭐"
                            feedback_timer = 30
                    else:
                        score = max(0, score - 2)
                        feedback_text = "Prøv det næste bogstav 🎈"
                        feedback_timer = 60
                        play_sound('wrong')
                    
                    break
        
        if event.type == pygame.USEREVENT:
            new_name()
    
    # Update particles
    for particle in celebration_particles[:]:
        particle.update()
        if particle.life <= 0:
            celebration_particles.remove(particle)
    
    # Draw everything
    screen.fill(WHITE)
    
    # Draw instruction
    instruction = medium_font.render("Stav navnet:", True, BLACK)
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 30))
    
    # Draw target name (reference) - grayed out
    target_text = huge_font.render(current_name, True, LIGHT_GRAY)
    screen.blit(target_text, (WIDTH // 2 - target_text.get_width() // 2, 120))
    
    # Draw boxes with filled-in letters
    box_size = 80
    box_spacing = 90
    start_x = WIDTH // 2 - (len(current_name) * box_spacing) // 2
    box_y = 250
    
    for i in range(len(current_name)):
        box_x = start_x + i * box_spacing
        
        # Draw box
        if i < len(typed_letters):
            # Filled box - green
            pygame.draw.rect(screen, GREEN, 
                            (box_x, box_y, box_size, box_size), 
                            border_radius=10)
        else:
            # Empty box - gray
            pygame.draw.rect(screen, LIGHT_GRAY, 
                            (box_x, box_y, box_size, box_size), 
                            border_radius=10)
        
        pygame.draw.rect(screen, BLACK, 
                        (box_x, box_y, box_size, box_size), 3,
                        border_radius=10)
        
        # Draw letter inside box if typed
        if i < len(typed_letters):
            letter_text = box_font.render(typed_letters[i], True, WHITE)
            letter_rect = letter_text.get_rect(center=(box_x + box_size//2, box_y + box_size//2))
            screen.blit(letter_text, letter_rect)
    
    # Draw score
    score_text = medium_font.render(f"Point: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 250, 30))
    
    # Draw letter buttons
    for button in available_letters:
        button.draw()
    
    # Draw particles
    for particle in celebration_particles:
        particle.draw()
    
    # Draw feedback
    if feedback_timer > 0:
        color = GREEN if "PERFEKT" in feedback_text or "Godt" in feedback_text else RED
        feedback_surf = medium_font.render(feedback_text, True, color)
        feedback_rect = feedback_surf.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        screen.blit(feedback_surf, feedback_rect)
        feedback_timer -= 1
    
    pygame.display.flip()

pygame.quit()
sys.exit()