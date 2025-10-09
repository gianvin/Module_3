import pygame
import sys
import random

#Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animal Kingdom")


# Font setup
font = pygame.font.Font(None, 36)

# Load and resize images
def load_image(path):
    return pygame.transform.scale(pygame.image.load(path), (100,100))
#Animal images
bear = load_image("images/bear.png")
dog = load_image("images/dog.png")
elephant = load_image("images/elephant.png")
frog = load_image("images/frog.png")
jellyfish = load_image("images/jellyfish.png")
kangaroo = load_image("images/kangaroo.png")
lion = load_image("images/lion.png")
turtle = load_image("images/turtle.png")
back = load_image("images/back.png")
# Player Class
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

# Create 2 players
player1 = Player("Player 1")
player2 = Player("Player 2")
current_player = player1

# Function for class Card
class Card:
    def __init__(self, image, name, x, y, back_image):
        self.image = image
        self.name = name
        self.rect = self.image.get_rect(topleft=(x, y))
        self.flipped = False
        self.matched = False
        self.back_image = back_image
    
    def draw(self, surface):
        if self.flipped or self.matched:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(self.back_image, self.rect)                                                                 
# Create card pairs
animals = [
    ("Dog", dog),
    ("Elephant", elephant),
    ("frog", frog),
    ("Jellyfish", jellyfish),
    ("Kangaroo", kangaroo),
    ("Bear", bear),
    ("Lion", lion),
    ("turtle", turtle)
]

# For Pairing
all_cards = []
for name, img in animals:
    all_cards.append((name, img))
    all_cards.append((name, img))

# Shuffle the cards randomly
random.shuffle(all_cards)

# Card positions
cards = []
start_x, start_y = 100, 150
gap = 20
cols = 4

for i, (name, img) in enumerate(all_cards):
    x = start_x + (i % cols) * (100 + gap)
    y = start_y + (i // cols) * (100 + gap)
    cards.append(Card(img, name, x, y, back))

# Start with Player 1
current_player = player1

#Set the Frame Rate
clock = pygame.time.Clock()


# Step 5 Add Flip and Match
flipped_cards = []

def handle_click(pos):
    global current_player
    for card in cards:
        if card.rect.collidepoint(pos) and not card.flipped and not card.matched:
            card.flipped = True
            flipped_cards.append(card)
            break

        if len(flipped_cards) == 2:
            card1, card2 = flipped_cards
            if card1.name == card2.name:
                #Matched!
                card1.matched = True
                card2.matched = True
            else:

                #Not Matched flipped back after delay
                pygame.time.delay(800)
                card1.flipped = False
                card2.flipped = False
                flipped_cards.clear()

                #switch turn
                current_player = player2 if current_player == player1 else player1

#Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False

        # Switch Turn when mouse is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_player = player2 if current_player == player1 else player1
    
    #Fill the screen with a color white
    screen.fill((255, 255, 255))

    # Drawing all cards
    for card in cards:
        card.draw(screen)
    #Display the scores of the players
    text1 = font.render(f"{player1.name}: {player1.score}", True, (0, 0, 0))
    text2 = font.render(f"{player2.name}: {player2.score}", True, (0, 0, 0))
    turn_text = font.render(f"Turn: {current_player.name}", True, (255, 0, 0))
    
    #Draw text on screen
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 50))
    screen.blit(turn_text, (10, 100))
    
    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(30)

pygame.quit()
sys.exit()
