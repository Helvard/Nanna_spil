import pygame
import random
import sys

# Initialize
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
LETTER_SIZE = 120
BUTTON_SIZE = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 150, 255)
YELLOW = (255, 255, 100)
PURPLE = (200, 100, 255)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE]

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bogstavjagt! 🎈")
clock = pygame.time.Clock()

# Fonts
big_font = pygame.font.Font(None, LETTER_SIZE)
medium_font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 60)

# Game state
score = 0
target_letter = 'A'
letters = []

class Letter:
    def __init__(self, char, is_target):
        self.char = char
        self.is_target = is_target
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(150, HEIGHT - 150)
        self.color = random.choice(COLORS)
        self.scale = 1.0
        self.alive = True
        
    def draw(self):
        if not self.alive:
            return
        text = big_font.render(self.char, True, self.color)
        text_rect = text.get_rect(center=(self.x, self.y))
        
        # Pulsing effect
        self.scale = 1.0 + 0.1 * abs(pygame.time.get_ticks() % 1000 - 500) / 500
        scaled_text = pygame.transform.scale(text, 
                                             (int(text_rect.width * self.scale),
                                              int(text_rect.height * self.scale)))
        scaled_rect = scaled_text.get_rect(center=(self.x, self.y))
        screen.blit(scaled_text, scaled_rect)
        
    def is_clicked(self, pos):
        distance = ((pos[0] - self.x)**2 + (pos[1] - self.y)**2)**0.5
        return distance < LETTER_SIZE / 2

def spawn_letters():
    global letters, target_letter
    letters = []
    
    # Pick random target letter
    target_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    # Spawn 2-4 target letters
    num_targets = random.randint(2, 4)
    for _ in range(num_targets):
        letters.append(Letter(target_letter, True))
    
    # Spawn 4-6 other letters
    num_others = random.randint(4, 6)
    other_letters = [c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if c != target_letter]
    for _ in range(num_others):
        letters.append(Letter(random.choice(other_letters), False))

def play_sound(sound_type):
    """Simple sound feedback"""
    if sound_type == 'correct':
        # Høj tone for rigtigt
        sound = pygame.mixer.Sound(buffer=bytes([128 + int(50 * (i % 100) / 100) for i in range(1000)]))
        sound.play()
    elif sound_type == 'wrong':
        # Lav tone for forkert
        sound = pygame.mixer.Sound(buffer=bytes([128 - int(30 * (i % 50) / 50) for i in range(800)]))
        sound.play()

# Initialize first round
spawn_letters()

# Game loop
running = True
feedback_text = ""
feedback_timer = 0

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            for letter in letters:
                if letter.alive and letter.is_clicked(pos):
                    letter.alive = False
                    
                    if letter.is_target:
                        score += 10
                        feedback_text = "SUPER! ⭐"
                        play_sound('correct')
                    else:
                        score = max(0, score - 5)
                        feedback_text = "Prøv igen! 🎈"
                        play_sound('wrong')
                    
                    feedback_timer = 60  # 1 second at 60 FPS
                    break
            
            # Check if all targets are found
            if all(not letter.alive for letter in letters if letter.is_target):
                feedback_text = "ALLE FUNDET! 🎉"
                feedback_timer = 120
                pygame.time.wait(1000)
                spawn_letters()
    
    # Draw everything
    screen.fill(WHITE)
    
    # Draw instruction
    instruction = medium_font.render(f"Find alle: {target_letter}", True, BLACK)
    screen.blit(instruction, (50, 30))
    
    # Draw score
    score_text = small_font.render(f"Point: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 250, 30))
    
    # Draw letters
    for letter in letters:
        letter.draw()
    
    # Draw feedback
    if feedback_timer > 0:
        feedback_surf = medium_font.render(feedback_text, True, GREEN if "SUPER" in feedback_text or "ALLE" in feedback_text else RED)
        feedback_rect = feedback_surf.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        screen.blit(feedback_surf, feedback_rect)
        feedback_timer -= 1
    
    pygame.display.flip()

pygame.quit()
sys.exit()