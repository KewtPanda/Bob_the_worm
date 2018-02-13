import pygame, random, sys
from pygame.locals import *

# sprite setup for a block
class Block(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, color):
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        #self.rect.center = pos
        self.rect.topleft = pos
        self.width = width
        self.height = height

# define what happens when the update runs
def update_position(bob_list, direction):
    for i in range(len(bob_list)-1, 0, -1):
        bob_list[i].rect.x = bob_list[i-1].rect.x
        bob_list[i].rect.y = bob_list[i-1].rect.y
        
    if direction == 'left':
        bob_list[0].rect.x = bob_list[0].rect.x - bob_list[0].width
    elif direction == 'right':
        bob_list[0].rect.x = bob_list[0].rect.x + bob_list[0].width
    elif direction == 'up':
        bob_list[0].rect.y = bob_list[0].rect.y - bob_list[0].height
    elif direction == 'down':
        bob_list[0].rect.y = bob_list[0].rect.y + bob_list[0].height
            

# set name
def set_name(SCREEN, bgc, txtc):
    global name
    name = 'noname'
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # check what key is pressed
            elif event.type == KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif event.key == K_RETURN:
                    return name
        SCREEN.fill(bgc)
        block = font.render(name, True, txtc)
        rect = block.get_rect()
        rect.center = SCREEN.get_rect().center
        SCREEN.blit(block, rect)
        pygame.display.update()

# get high score from file and return it
def get_high_score():
    # Default high score
    high_score = 0
    high_score_name = ''
 
    # Try to read the high score from a file
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        high_score_name_file = open("high_score_name.txt", "r")
        high_score_name = high_score_name_file.read()
        high_score_name_file.close()
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")
 
    return high_score, high_score_name
 
# save high score to file
def save_high_score(new_high_score, new_high_score_name):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
        high_score_name_file = open("high_score_name.txt", "w")
        high_score_name_file.write(new_high_score_name)
        high_score_name_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")

# check Bob collision
def collide(x1, x2, y1, y2, w1, w2, h1, h2):
    if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
        return True
    else:
        return False

# display score and text when Bob die
def die(SCREEN, bob_score, bgc, txtc):
    while True:
        # check events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # check what key is pressed
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    main()
                elif event.key == K_ESCAPE:
                    global name
                    name = set_name(SCREEN, (255, 255, 255), (0, 0, 0))
                    main()

        # get highscore
        high_score, high_score_name = get_high_score()

        # save highscore
        if bob_score > high_score:
            save_high_score(bob_score, name)
            tnhs = font.render('NEW HIGHSCORE!!!', True, txtc)
            SCREEN.blit(tnhs, (10, 10))

        # get highscore again, if it's a new one
        high_score, high_score_name = get_high_score()
            
        # display score and information
        t = font.render('Your score was: '+str(bob_score), True, txtc)
        tn = font.render('Press Return (Enter) for new game or ESC for new name ', True, txtc)
        ths = font.render('HIGHSCORE: '+high_score_name+' - '+str(high_score), True, txtc)
        SCREEN.blit(t, (10, 100))
        SCREEN.blit(tn, (10, 150))
        SCREEN.blit(ths, (10, 250))
        
        pygame.display.update()


# get apple position
def get_apple(WINDOWWIDTH, WINDOWHEIGHT, bob_group, size, color):
    collision = True
    while(collision):
        pos_x = random.randint(0, WINDOWWIDTH-size)
        offset = pos_x%10
        pos_x -= offset
        pos_y = random.randint(0, WINDOWHEIGHT-size)
        offset = pos_y%10
        pos_y -= offset
        apple = Block([pos_x, pos_y],size, size, color) # position, width, height, color
        collision = pygame.sprite.spritecollide(apple, bob_group, True)
    return apple


def main():
    # init pygame
    pygame.init()
    # first run vairable
    global first_run
    
    # setup fps
    FPS = 10
    # used to manage how fast the screen updates
    fpsClock = pygame.time.Clock()

    # setup the screen
    WINDOWWIDTH = 1280
    WINDOWHEIGHT = 720
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    # name of the app
    pygame.display.set_caption('Bob the worm')

    # colors (standard)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    # colors (other)
    AQUA = (0, 255, 255)
    GRAY = (128, 128, 128)
    LIME = ( 0, 128, 0)
    OLIVE = (128, 128, 0)
    PURPLE = (128, 0, 128)
    SILVER = (192, 192, 192)
    TEAL = (0, 128, 128)
    YELLOW = (255, 255, 0)

    # setup font
    global font
    font = pygame.font.SysFont('Arial', 30)

    # setup music
    if first_run == 1:
        try:
            soundObj = pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(0.9)
        except:
            print('Loading of music failed!')
             
    # setup Bob the worm
    bob_score = 0
    bob_speed = 0.8 # speed(FPS) = Original_FPS(10) + bob_score * bob_speed
    bob_color = BLUE
    bob_size = 10
    direction = 'up'
    bob_group = pygame.sprite.Group()
    bob_list = []
    for i in range(0, 3, 1):
        if i == 0:
            bob = Block([(int)(WINDOWWIDTH/2), (int)(WINDOWHEIGHT/2)], bob_size, bob_size, bob_color) # position, width, height, color
        else:
            bob = Block([bob_list[i-1].rect.x, bob_list[i-1].rect.y+bob_size], bob_size, bob_size, bob_color) # position, width, height, color
        bob_list.append(bob) # list of every block in bob in order
        bob_group.add(bob) # sprite with every block in bob, used for collision

    # setup apple
    apple_size = 10
    apple_color = RED
    #apple_x = random.randint(0, WINDOWWIDTH-apple_size)
    #apple_y = random.randint(0, WINDOWHEIGHT-apple_size)
    apple_group = pygame.sprite.Group()
    apple = get_apple(WINDOWWIDTH, WINDOWHEIGHT, bob_group, apple_size, apple_color)
    apple_group.add(apple)

    # setup name
    global name
    if first_run == 1:    
        name = set_name(SCREEN, WHITE, BLACK)

    # set first_run variable to 0 to stop music from restarting
    first_run = 0
    
    # main game loop
    while True:
        # check events
        dir_block = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # check what key is pressed
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and direction != 'right' and dir_block == False:
                    direction = 'left'
                    dir_block = True
                elif event.key == K_RIGHT and direction != 'left' and dir_block == False:
                    direction = 'right'
                    dir_block = True
                elif event.key == K_UP and direction != 'down' and dir_block == False:
                    direction = 'up'
                    dir_block = True
                elif event.key == K_DOWN and direction != 'up' and dir_block == False:
                    direction = 'down'
                    dir_block = True
                elif event.key == K_s:
                    direction = 'none'
                elif event.key == K_ESCAPE:
                    name = set_name(SCREEN, WHITE, BLACK)
                    main()

        # clear the screen
        SCREEN.fill(WHITE)
        
        # move Bob based on user input
        if direction != 'none':
            update_position(bob_list, direction)

        # check if Bob eats an apple
        consume = pygame.sprite.spritecollide(apple, bob_group, False)
        if consume:
            bob_score += 1
            bob = Block([bob_list[2].rect.x, bob_list[2].rect.y], bob_size, bob_size, bob_color)
            bob_list.append(bob)
            bob_group.add(bob)
            apple_group.remove(apple)
            apple = get_apple(WINDOWWIDTH, WINDOWHEIGHT, bob_group, apple_size, apple_color)
            apple_group.add(apple)
            
        # check if Bob collide with a wall
        if (bob_list[0].rect.x < 0 or
            bob_list[0].rect.x+bob_size > WINDOWWIDTH or
            bob_list[0].rect.y < 0 or
            bob_list[0].rect.y+bob_size > WINDOWHEIGHT):
            die(SCREEN, bob_score, WHITE, BLACK)       
        
        # check if Bob collide with himself
        for i in range(len(bob_list)-1, 1, -1):
            if collide(bob_list[0].rect.x, bob_list[i].rect.x, bob_list[0].rect.y, bob_list[i].rect.y, bob_size, bob_size, bob_size, bob_size):
                die(SCREEN, bob_score, WHITE, BLACK)
        
        # draw score
        t = font.render(str(bob_score), True, (0, 0, 0))
        SCREEN.blit(t, (10, 10))
        
        # draw sprites
        bob_group.draw(SCREEN)
        apple_group.draw(SCREEN)
      
        # update screen
        pygame.display.update()
        # wait before next run
        new_fps = FPS + bob_score*bob_speed
        fpsClock.tick(new_fps)


# call the main function 
if __name__ == '__main__':
    global first_run
    first_run = 1

    main()
