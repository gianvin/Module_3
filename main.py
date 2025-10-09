import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Load Sound
flip_sound = pygame.mixer.Sound("sounds/flip.ogg")


# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animal Kingdom")

# Font setup
font = pygame.font.Font(None, 24)

# Load and resize images
def load_image(path):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (100,100))
    except Exception as e:
        print(f"Warning: couldn't load '{path}': {e} - using placeholder")
        surf = pygame.Surface((100, 100))
        surf.fill((200, 200, 200))
        label = font.render(path.split('/')[-1].split('.')[0], True, (0, 0, 0))
        surf.blit(label, label.get_rect(center=(50,50)))
        return surf
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
        self.rect = pygame.Rect(x, y, 100, 100)
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
start_x, start_y = 100, 120
gap = 20
cols = 4

for i, (name, img) in enumerate(all_cards):
    x = start_x + (i % cols) * (100 + gap)
    y = start_y + (i // cols) * (100 + gap)
    cards.append(Card(img, name, x, y, back))

# Game variables
clock = pygame.time.Clock()
flipped_cards = []
flip_time = 0
awaiting_flip = False

def handle_click(pos):
   # ignore clicks while waiting for flip-back to complete
   if awaiting_flip:
       return
   #prevent clicking more than 2 cards
   if len(flipped_cards) >= 2:
       return

   
   for card in cards:
        if card.rect.collidepoint(pos) and not card.flipped and not card.matched:
            card.flipped = True
            flipped_cards.append(card)
            flip_sound.play()
            break

def check_match():
        global flip_time, awaiting_flip, flipped_cards, current_player 

        if len(flipped_cards) == 2 and not awaiting_flip:
            c1, c2 = flipped_cards
            if c1.name.lower() == c2.name.lower():
                #Matched!
                c1.matched = True
                c2.matched = True
                current_player.score += 1
                flipped_cards.clear() 
            else:

                # wait 1 second before flipping back
                awaiting_flip = True
                flip_time = pygame.time.get_ticks() + 1000

#Function for Flip back and switch
def flip_back_and_switch():
    global flip_time, awaiting_flip, flipped_cards, current_player
    
    #flip back the two cards and switch turn
    for c in flipped_cards:
        c.flipped = False
    flipped_cards.clear()
    awaiting_flip = False
    flip_time = 0
    current_player = player2 if current_player == player1 else player1

#Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())
        
    check_match()

     # If waiting and timer expired, flip back and switch players
    if awaiting_flip and pygame.time.get_ticks() >= flip_time:
        flip_back_and_switch()
    
    #Fill the screen with a color white
    screen.fill((255, 255, 255))

    # Drawing all cards
    for card in cards:
        card.draw(screen)
    #Displaying the scores of the players
    text1 = font.render(f"{player1.name}: {player1.score}", True, (0, 0, 0))
    text2 = font.render(f"{player2.name}: {player2.score}", True, (0, 0, 0))
    turn_text = font.render(f"Turn: {current_player.name}", True, (200, 0, 0))
    
    #Draw text on screen
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))
    screen.blit(turn_text, (10, 70))
    
    #Function to check all cards matched, and which player win

    if all(card.matched for card in cards):
        if player1.score > player2.score:
            winner_text = f"{player1.name} Wins!"
        elif player2.score > player1.score:
            winner_text = f"{player2.name} Wins!"
        else: winner_text = "It's a Tie"

        winner_display = font.render(winner_text, True, (0, 128, 0))
        screen.blit(winner_display, (300, 50))
    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(30)

pygame.quit()
sys.exit()


