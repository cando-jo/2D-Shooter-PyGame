# @Date:   2021-12-10T16:20:21+03:00
# @Last modified time: 2021-12-12T20:21:36+03:00



#NOTES:
'''
-Coordinates system for pygame: 0,0 is top left, not the middle of the window.
'''
import pygame #Pygame is a 2D Game Module
import os #operating system to help us find hte path for the images (spaceships)
from random import *
import threading

pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 1300, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # <-- This is a tuple, Capital letters means its CAPITAL letter.

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

WHITE = (255,255,255) #RGB
BLACK = (0, 0, 0) #BLACK
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CANDO_COLOUR = (45,33,200)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'BULLET_HIT_SOUND.mp3' ))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'BULLET_FIRE_SOUND2.mp3'))
MAIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'ST_Main.mp3'))
EMPTY_BULLET_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'empty_bullet2.mp3'))
BORDER = pygame.Rect(WIDTH // 2 - 2, 0, 10, HEIGHT)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 140, 140
BULLET_WIDTH, BULLET_HEIGHT = 40, 40
DROP_WIDTH, DROP_HEIGHT = 100, 100
SWORD_WIDTH, SWORD_HEIGHT = 100, 100
pygame.display.set_caption("Cando's Game")

YELLOW_WAS_HIT = pygame.USEREVENT + 1 #Custom user eventQ
RED_WAS_HIT = pygame.USEREVENT + 2 #Custom user event


FPS = 60 #To make sure all the machines run this smoothly and at the same frames per second
VELOCITY = 3 #We can play with that around. -> This is the speed of the spaceships or faces that we want them to move in
BULLET_VELOCITY = 10
DROP_VELOCITY = 4
MAX_BULLETS = 2

DROP_IMAGE = pygame.image.load(os.path.join('Assets', 'drop_fire2.png'))
#SWORD_IMAGE = pygame.image.load(os.path.join('Assets', 'sword.png'))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'soldier_yellow.png')) #Loading the image of the yellow spaceship
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'soldier_red6.png')) #Loading the image of the red spaceship
BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'bullet1.png'))

RED_BULLET = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE, (BULLET_WIDTH, BULLET_HEIGHT)), 135)
YELLOW_BULLET = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE, (BULLET_WIDTH, BULLET_HEIGHT)), 315)
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),360) #Width, height
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),360) #Width, height
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space2.jpg')), (WIDTH, HEIGHT))
DROP = pygame.transform.scale(DROP_IMAGE, (DROP_WIDTH, DROP_HEIGHT))
#YELLOW_SWORD = pygame.transform.rotate(pygame.transform.scale(SWORD_IMAGE,(SWORD_WIDTH, SWORD_HEIGHT)), 300)
#RED_SWORD = pygame.transform.rotate(pygame.transform.scale(SWORD_IMAGE, (SWORD_WIDTH, SWORD_HEIGHT)), 50)


def draw_window(red, yellow, red_bullets, yellow_bullets, bullet_hit, red_health, yellow_health, drop_array, red_sword, yellow_sword):
    WIN.blit(SPACE, (0, 0)) #It fills the colour, we make a tuple of 3 args (R,G,B). We have to fill the screen first before drawing the images (with blit() function)
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Steve's HP: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Cando's HP: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #When we want to draw a surface on the screen! (SURFACES ARE IMAGES LIKE SPACESHIPS...)
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    #WIN.blit(YELLOW_SWORD, (yellow_sword.x, yellow_sword.y))
    #WIN.blit(RED_SWORD, (red_sword.x, red_sword.y))

    for new_drop in drop_array:
        WIN.blit(DROP, (new_drop.x, new_drop.y))

    for bullet in red_bullets:
        WIN.blit(RED_BULLET, (bullet.x, bullet.y))

    for bullet in yellow_bullets:
        WIN.blit(YELLOW_BULLET, (bullet.x, bullet.y))

    pygame.display.update() #We need to update the colour to see it.


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() /2, HEIGHT/2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)



def yellow_handle_movement(keys_pressed, yellow, yellow_sword):
    if (keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0): #LEFT
        yellow.x -= VELOCITY
        yellow_sword.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VELOCITY < BORDER.x: #RIGHT
        yellow.x += VELOCITY
        yellow_sword.x += VELOCITY
    if (keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0): #LEFT
        yellow.y -= VELOCITY
        yellow_sword.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + 10 + VELOCITY < HEIGHT: #RIGHT
        yellow.y += VELOCITY
        yellow_sword.y += VELOCITY





def red_handle_movement(keys_pressed, red, red_sword):
    if (keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width): #LEFT
        red.x -= VELOCITY
        red_sword.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VELOCITY < WIDTH: #RIGHT
        red.x += VELOCITY
        red_sword.x += VELOCITY
    if (keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0): #LEFT
        red.y -= VELOCITY
        red_sword.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + 10 + VELOCITY < HEIGHT: #RIGHT
        red.y += VELOCITY
        red_sword.y += VELOCITY

def handle_movement_drop(drop, drop_array, start, red, yellow):
    for new_drop in drop_array:
        new_drop.y += DROP_VELOCITY
        if red.colliderect(new_drop):
            pygame.event.post(pygame.event.Event(RED_WAS_HIT))
            drop_array.remove(new_drop)

        if yellow.colliderect(new_drop):
            pygame.event.post(pygame.event.Event(YELLOW_WAS_HIT))
            drop_array.remove(new_drop)

        elif new_drop.y > HEIGHT:
            drop_array.remove(new_drop)





def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_WAS_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_WAS_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)





def main():#Main loop for the game
    RANDOM_WIDTH = randint(0, WIDTH)
    yellow = pygame.Rect(100, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(750, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) #Rectangle represents red and yellow spaceships (Kevin hart and the rock in this case :D)
    drop = pygame.Rect(RANDOM_WIDTH, 10, DROP_WIDTH, DROP_HEIGHT)
    yellow_sword = pygame.Rect(yellow.x + 20, yellow.y + 5, SWORD_WIDTH, SWORD_HEIGHT)
    red_sword = pygame.Rect(red.x - 90, red.y + 5, SWORD_WIDTH, SWORD_HEIGHT)
    MAIN_SOUND.play()

    red_bullets = []
    yellow_bullets = []
    drop_array = []

    red_health = 10
    yellow_health = 10

    bullet_hit = pygame.Rect(0, 0, BULLET_WIDTH, BULLET_HEIGHT)
    clock = pygame.time.Clock()
    run = True

    start = pygame.time.get_ticks()

    while(run):
        clock.tick(FPS) #Makes sure we run the while loop 60 times per second
        for event in pygame.event.get():
            RANDOM_WIDTH = randint(0, WIDTH-DROP_WIDTH)
            now = pygame.time.get_ticks()
            temp_now = now
            if now - start > 1000:
                start = now
                new_drop = pygame.Rect(RANDOM_WIDTH, 0 , 10, 5) #10 and 5 are the width and the height of the bullet
                drop_array.append(new_drop)

            if event.type == pygame.QUIT: #Clicking on the 'x' button is the pygame.QUIT
                run = False


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    if len(yellow_bullets) > MAX_BULLETS:
                        EMPTY_BULLET_SOUND.play()
                    else:
                        bullet_hit = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5) #10 and 5 are the width and the height of the bullet
                        yellow_bullets.append(bullet_hit)
                        BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL:
                    if len(red_bullets) > MAX_BULLETS:
                        EMPTY_BULLET_SOUND.play()
                    else:
                        bullet_hit = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                        red_bullets.append(bullet_hit)
                        BULLET_FIRE_SOUND.play()

            if event.type == RED_WAS_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_WAS_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if red_health <= 0:
            winner_text = "Cando Wins!"

        if yellow_health <= 0 :
            winner_text = "Steve Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed() #Gives us the keys which are being pressed 60 times in a seconds! and if they are the keys we want,
                                           #Then with if statements we can responde to they keys that are being pressed (for ex: W->Move up)

        handle_movement_drop(drop, drop_array, start, red, yellow)
        yellow_handle_movement(keys_pressed, yellow, yellow_sword)
        red_handle_movement(keys_pressed, red, red_sword)
        handle_bullets(yellow_bullets, red_bullets, yellow, red ) #yellow.x += 1 -> This will move 60 seconds per second
        draw_window(red, yellow, red_bullets, yellow_bullets, bullet_hit, red_health, yellow_health,drop_array, red_sword, yellow_sword)

    pygame.quit()

if __name__ == '__main__': #Making sure that it will only run here, not if we import the main into other file and run it there.
    main()
