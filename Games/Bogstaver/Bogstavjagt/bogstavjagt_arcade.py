"""
Bogstavjagt! 🎈 - Arcade Version
Letter hunting game with improved graphics and animations
"""

import arcade
import random
import math

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Bogstavjagt! 🎈"

# Colors
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK
RED = arcade.color.RED
GREEN = arcade.color.GREEN
BLUE = arcade.color.BLUE
YELLOW = arcade.color.YELLOW
PURPLE = arcade.color.PURPLE
LIGHT_BLUE = arcade.color.LIGHT_BLUE
LIGHT_GREEN = arcade.color.LIGHT_GREEN

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE]

# Game settings
LETTER_SIZE = 80
SPAWN_ANIMATION_SPEED = 0.1
FLOAT_SPEED = 0.5
PULSE_SPEED = 2.0

class Letter:
    """Animated letter with floating and pulsing effects"""
    
    def __init__(self, char: str, is_target: bool, center_x: float, center_y: float):
        self.char = char
        self.is_target = is_target
        self.original_x = center_x
        self.original_y = center_y
        self.center_x = center_x
        self.center_y = center_y
        
        # Animation properties
        self.float_offset = random.uniform(0, math.pi * 2)
        self.pulse_phase = 0
        self.scale = 1.0
        self.target_scale = 1.0
        
        # Visual properties
        self.color = random.choice(COLORS)
        self.glow_amount = 0
        self.size = LETTER_SIZE
        
    def on_update(self, delta_time: float):
        """Update animations"""
        
        # Floating animation
        self.float_offset += FLOAT_SPEED * delta_time
        float_y = math.sin(self.float_offset) * 20
        self.center_y = self.original_y + float_y
        
        # Pulsing effect for target letters
        if self.is_target:
            self.pulse_phase += PULSE_SPEED * delta_time
            pulse = 1.0 + 0.1 * math.sin(self.pulse_phase)
            self.scale = self.target_scale * pulse
            
            # Glow effect
            self.glow_amount = abs(math.sin(self.pulse_phase)) * 0.3
    
    def draw(self):
        """Draw the letter with effects"""
        current_size = self.size * self.scale
        
        # Draw glow for target letters
        if self.is_target and self.glow_amount > 0:
            glow_size = current_size * (1 + self.glow_amount)
            glow_alpha = int(50 * self.glow_amount)
            
            # Draw glow circles
            for i in range(3):
                glow_scale = 1 + (i + 1) * 0.2 * self.glow_amount
                arcade.draw_circle_filled(
                    self.center_x, 
                    self.center_y,
                    glow_size * glow_scale / 2,
                    (*YELLOW[:3], glow_alpha // (i + 1))
                )
        
        # Draw the letter background circle
        arcade.draw_circle_filled(
            self.center_x, 
            self.center_y,
            current_size / 2,
            self.color
        )
        
        # Draw the letter text on top
        arcade.draw_text(
            self.char,
            self.center_x,
            self.center_y,
            WHITE,
            font_size=int(current_size * 0.8),
            font_name="Arial",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )
    
    def is_clicked(self, x: float, y: float) -> bool:
        """Check if this letter was clicked"""
        distance = math.sqrt((x - self.center_x)**2 + (y - self.center_y)**2)
        return distance < (self.size * self.scale) / 2

class ParticleEffect:
    """Celebration particle effect"""
    
    def __init__(self, x: float, y: float, color):
        self.center_x = x
        self.center_y = y
        self.color = color
        self.velocity_x = random.uniform(-200, 200)
        self.velocity_y = random.uniform(100, 400)
        self.lifetime = 1.0
        self.radius = random.uniform(5, 15)
        
    def on_update(self, delta_time: float):
        """Update particle physics"""
        self.center_x += self.velocity_x * delta_time
        self.center_y += self.velocity_y * delta_time
        self.velocity_y -= 500 * delta_time  # Gravity
        self.lifetime -= delta_time
        return self.lifetime > 0
        
    def draw(self):
        """Draw particle"""
        alpha = int(255 * self.lifetime)
        arcade.draw_circle_filled(
            self.center_x, 
            self.center_y, 
            self.radius * self.lifetime,
            (*self.color[:3], alpha)
        )

class BogstavjagtGame(arcade.Window):
    """Main game window"""
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Game state
        self.letters = []
        self.particles = []
        self.score = 0
        self.target_letter = 'A'
        self.feedback_text = ""
        self.feedback_timer = 0
        self.round_complete = False
        self.round_timer = 0
        
        # Visual settings
        arcade.set_background_color(LIGHT_BLUE)
        
        # Start first round
        self.setup_round()
        
    def setup_round(self):
        """Setup a new round of letters"""
        self.letters.clear()
        self.particles.clear()
        self.round_complete = False
        self.round_timer = 0
        
        # Pick random target letter
        self.target_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        # Spawn 2-4 target letters
        num_targets = random.randint(2, 4)
        for _ in range(num_targets):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(150, SCREEN_HEIGHT - 150)
            letter = Letter(self.target_letter, True, x, y)
            self.letters.append(letter)
        
        # Spawn 4-6 other letters
        num_others = random.randint(4, 6)
        other_letters = [c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if c != self.target_letter]
        for _ in range(num_others):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(150, SCREEN_HEIGHT - 150)
            char = random.choice(other_letters)
            letter = Letter(char, False, x, y)
            self.letters.append(letter)
    
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse clicks"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Check if any letter was clicked
            for letter in self.letters[:]:  # Copy list to avoid modification during iteration
                if letter.is_clicked(x, y):
                    self.letters.remove(letter)
                    
                    if letter.is_target:
                        # Correct letter!
                        self.score += 10
                        self.feedback_text = "SUPER! ⭐"
                        self.feedback_timer = 60
                        self.create_celebration(letter.center_x, letter.center_y, GREEN)
                    else:
                        # Wrong letter
                        self.score = max(0, self.score - 5)
                        self.feedback_text = "Prøv igen! 🎈"
                        self.feedback_timer = 60
                        self.create_celebration(letter.center_x, letter.center_y, RED)
                    
                    break
            
            # Check if round is complete
            target_letters = [l for l in self.letters if l.is_target]
            if len(target_letters) == 0:
                self.feedback_text = "ALLE FUNDET! 🎉"
                self.feedback_timer = 120
                self.round_complete = True
                self.round_timer = 120  # 2 seconds before next round
    
    def create_celebration(self, x: float, y: float, color):
        """Create particle celebration effect"""
        for _ in range(20):
            particle = ParticleEffect(x, y, color)
            self.particles.append(particle)
    
    def on_update(self, delta_time: float):
        """Update game logic"""
        # Update letters
        for letter in self.letters:
            letter.on_update(delta_time)
        
        # Update particles
        particles_to_remove = []
        for particle in self.particles:
            if not particle.on_update(delta_time):
                particles_to_remove.append(particle)
        
        for particle in particles_to_remove:
            self.particles.remove(particle)
        
        # Update feedback timer
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
        
        # Handle round completion
        if self.round_complete:
            self.round_timer -= 1
            if self.round_timer <= 0:
                self.setup_round()
    
    def on_draw(self):
        """Draw everything"""
        self.clear()
        
        # Draw instruction
        instruction_text = f"Find alle: {self.target_letter}"
        arcade.draw_text(
            instruction_text,
            50, 30,
            BLACK,
            font_size=60,
            font_name="Arial",
            bold=True
        )
        
        # Draw score
        score_text = f"Point: {self.score}"
        arcade.draw_text(
            score_text,
            SCREEN_WIDTH - 250, 30,
            BLACK,
            font_size=45,
            font_name="Arial",
            bold=True
        )
        
        # Draw letters
        for letter in self.letters:
            letter.draw()
        
        # Draw particles
        for particle in self.particles:
            particle.draw()
        
        # Draw feedback
        if self.feedback_timer > 0:
            feedback_color = GREEN if "SUPER" in self.feedback_text or "ALLE" in self.feedback_text else RED
            arcade.draw_text(
                self.feedback_text,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 100,
                feedback_color,
                font_size=50,
                font_name="Arial",
                bold=True,
                anchor_x="center"
            )

def main():
    """Main function"""
    game = BogstavjagtGame()
    arcade.run()

if __name__ == "__main__":
    main()
