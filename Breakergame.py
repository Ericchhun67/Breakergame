import pygame
import sys
success, fail = pygame.init()
print(f"init success: {success} fail: {fail}")

# handle screen errors
try:
    # Set up the game window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Brick Breaker Game")
    # load the game icon
except pygame.exceptions as e:
    # print out an error message and exit 
    print(f"Error initializing game window: {e}")
finally:
    # print out a success message if the game window was initialized successfully
    print("Game window initialized successfully")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
# set up the FPS counter
CLOCK = pygame.time.Clock()
FPS = 100

# initialize a game quest in a dictionary
quest_log = {
    "Brick Breaker": 0,
    "Target": 10,
    "Best Score": 10 
}

# Create a Button class with highlighting feature
class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, text_color):
        # initialize the position and size of the button
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color # set the color for the button
        self.hover_color = hover_color 
        self.text = text # set the text for the button
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen, mouse_pos):
        # if the mouse is over the button, draw the text and color for the button
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        # return True if the mouse button was clicked and the button was clicked, False otherwise
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(350, 550, 100, 10)
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(400, 300, 10, 10)
        self.speed_x = 3
        self.speed_y = -3

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off the walls
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, YELLOW, self.rect)

def display_quest(screen, quest_log):
    quest_font = pygame.font.Font(None, 30)
    y_offset = 20 # start the y position of the quest at the top of the screen
    # loop through the quest
    for quest, progress in quest_log.items():
        text = f"{quest}: {progress}"
        quest_text = quest_font.render(text, True, WHITE)
        text_rect = quest_text.get_rect(topright=(780, y_offset))
        screen.blit(quest_text, text_rect)
        y_offset += 30
    return quest_log
def display_fps(screen):
    # position the fps text on the screen
    fpsX = 10
    fpsY = 550
    font = pygame.font.Font(None, 25) # set the font size to 25
    # calculate and display Fps
    fps = int(CLOCK.get_fps())
    fps_text = font.render("Fps : " + str(fps), True, (255,255,255))
    screen.blit(fps_text, (fpsX, fpsY))
    return

def displayscore(score):
    score_font = pygame.font.Font(None, 25) # set the font size to 25
    # render the score text in white color
    score_text = score_font.render("Score : " + str(score), True, (255,255, 255))
    # blit the score text to the center of the screen at the coordinates (300, 550)
    screen.blit(score_text, (30, 20))
    return


def you_win_screen():
    running = True # if running is true then display the win screen
    # win screen loop
    while running:
        # fill the win screen with white
        screen.fill(WHITE)
        # set the game font to 50
        font = pygame.font.Font(None, 50)
        # render the win text in white color
        text = font.render("You Win!", True, BLACK)
        # blit the win text to the center of the screen at the coordinates (300, 300)
        screen.blit(text, (300, 300))
        # handle the game events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # update to game screen
        pygame.display.flip()

# Create bricks
def create_bricks():
    bricks = [] # create a list of bricks to be storted in an empty list
    # Create 4 rows of 8 bricks each, with a gap of 10 pixels between them
    for i in range(6): # loop through each break
        for j in range(8): # col of 8 
            bricks.append(pygame.Rect(100 + j * 75, 50 + i * 30, 60, 20))
    return bricks


def pauseMenu():
    # fill the menu with the color green
    screen.fill(GREEN)
    font = pygame.font.Font(None, 30)
    pause_text = font.render("Pause", True, WHITE)
    screen.blit(pause_text, (300, 300))
    
    p_text = font.render("press tab to go back to the menu", True, WHITE)
    screen.blit(p_text, (300, 350))
    pygame.display.flip()
    
    game_title = font.render("Brick Breaker", True, WHITE)
    # position at the top left of the screen
    screen.blit(game_title, (30, 10))
    pygame.display.flip()
    
    pause = True # set to True to active  the pause menu
    # start of the pause loop
    while pause:
        # handle game event
        for event in pygame.event.get():
            # handle keys events
            if event.type == pygame.KEYDOWN:
                # display that the pause menu is active
                print("Pause menu is active")
                pause = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Draw objects
        # start_button.draw(screen, mouse_pos)
        # exit_button.draw(screen, mouse_pos)

        pygame.display.flip()

def game_over():
    # to-do restart game doesn't work properly
    
    # Create a loop to keep the game over screen running until a decision is made
    while True:
        # Fill the screen with blue when the game is over
        screen.fill(("blue"))  # Blue color
        # Display the background image on the game over screen

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the game
                sys.exit()  # Exit the program

            # Check for keypresses or button clicks for restart/exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press "R" to restart the game
                    # display a that the r key is pressed
                    print ("press the R key to restart the game")
                    return  # Exiting game_over function to restart the game
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:  # Press "Q" to quit the game
                    # display that the q key is pressed
                    print ("press the Q key to quit the game")
                    pygame.quit()
                    sys.exit()
            
        # Set the font to display "Game Over" at size 64
        font = pygame.font.Font(None, 64)
        # Create a surface for the "Game Over" text and fill the text with white color
        text_surface = font.render("Game Over!", True, (255, 255, 255))  
        # Position the "Game Over" text on screen
        text_rect = text_surface.get_rect(center=(400, 300))  # Adjust according to your screen size
        # Display the "Game Over" text on screen
        screen.blit(text_surface, text_rect)

        # Add a message to instruct the player to press "R" to restart or "Q" to quit
        restart_font = pygame.font.Font(None, 32)
        restart_surface = restart_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(400, 400))  # Adjust according to your screen size
        screen.blit(restart_surface, restart_rect) # get the restart on the screen

        # Update the game screen
        pygame.display.flip()
        return



def main():
    # Main menu buttons
    start_button = Button(300, 200, 200, 50, GREEN, RED, "Start", BLACK)
    exit_button = Button(300, 300, 200, 50, RED, GREEN, "Exit", BLACK)

    # Initialize objects
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    score = 0
    # Game states
    main_menu = True
    game_running = False

    # Main game loop
    running = True
    while running:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # keyboard pause events
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                # display pause menu when tab key is pressed
                print(" Tab key is pressed")
                pauseMenu()
            
            
        
            if main_menu:
                if start_button.is_clicked(event):
                    main_menu = False
                    game_running = True
                    ball.rect.x, ball.rect.y = 400, 300  # Reset ball position
                if exit_button.is_clicked(event):
                    running = False

        # Main Menu Screen
        if main_menu:
            # fill the main menu screen with blue
            screen.fill("blue")
            start_button.draw(screen, mouse_pos)
            exit_button.draw(screen, mouse_pos)
        display_fps(screen) # display the FPS on the screen
        displayscore(score) # display the score on the screen

        # Game Screen
        if game_running:
            # handle keyboard events
            keys = pygame.key.get_pressed()
            # Move paddle
            paddle.move(keys)
            # Draw paddle, ball, and bricks
            paddle.draw(screen)
            ball.draw(screen)
            ball.move() # move the ball 
            # Move ball
            for brick in bricks:
                # draw Red bricks 
                pygame.draw.rect(screen, RED, brick)   
            
            # Check if the ball hits the paddle
            if ball.rect.colliderect(paddle.rect):
                ball.speed_y *= -1

            # Check if the ball hits a brick
            for brick in bricks:
                if ball.rect.colliderect(brick):
                    quest_log["Brick Breaker"] += 1 # increment the number of bricks
                    score += 1 # increment the score when the ball hits a brick
                    bricks.remove(brick)  # Remove the brick
                    ball.speed_y *= -1.0 # decrease the speed of the ball
                    break  # Only remove one brick per frame
                
                
                
            # Check if ball falls below the screen
            if ball.rect.bottom >= 600:
                game_running = False 
                main_menu = True
            
            
            # Check if all bricks are broken
            if len(bricks) < 5:
                game_running = False
                you_win_screen()
            # display the quest on the game screen  
            display_quest(screen, quest_log)   

            # Draw paddle, ball, and bricks
            paddle.draw(screen)
            ball.draw(screen)

            for brick in bricks:
                pygame.draw.rect(screen, RED, brick)
        # Update the display
        pygame.display.flip()
        CLOCK.tick(FPS) 
if __name__ == '__main__':
    main()