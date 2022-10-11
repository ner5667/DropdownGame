#TO DOs:
#the score starts as -1 - this is a workaround and NOT optimal
#implement a count in system before game starts

#change the background and the corner to different things -> otherwise really weird to see the barriers

import pygame
from pygame.locals import *
import sys

#test
left_hold = 0
right_hold = 0

#DEFINE EVERYTHING WITH PYGAME AND etc.

#initiate clock for FPS later
clock = pygame.time.Clock()

#initiate pygame
pygame.init()

#name the window
pygame.display.set_caption("Window (very fockin` uwu)")

#define every tile as 16*16=256 pixels
tile_x = 16
tile_y = 16

#define the framerate
#later used by pygame.clock
framerate = 30

#initiate and set the screen as 400*400
screen = pygame.display.set_mode((400, 400), 0, 32)


def collision_test(rect, tiles):
    # zero-initialize hit_list, a list used to output which items collide
    hit_list = []
    for tile in tiles:

        # check if items from the first list collide with the second list
        if rect.colliderect(tile):
            # if the collision happens, add the things that collide to hit_list
            hit_list.append(tile)

    # in this list all items of the 2nd list that collide with the first list/item
    # get returned
    return hit_list


# the function quits the program when called
# used when pressing esc/the funny little x in the top corner
def quit_out():
    pygame.quit()
    sys.exit()


def adjust_for_framerate(original_number, adjusted_number):
    return original_number*(30/adjusted_number)


#LOAD ALL NECESSARY IMAGE FILES (and fonts)

block_dirt = pygame.image.load("ImageFiles/Dirt.png")

#this is the "enemy" tile where you die when you touch it
block_baddie = pygame.image.load("ImageFiles/Baddie.png")

#theoretically for the sides, now used as the background with no way to see the barriers at the side
#, that sound **corner** the playing field
block_corner = pygame.image.load("ImageFiles/corner.png")

#the very good background for when you die
#basically just says "You died: this is your score"
death_screen = pygame.image.load("ImageFiles/DeathScreen.png")

#the neutral form for the player, it doesn't have any other stats rn
character_animation_neutral = pygame.image.load("ImageFiles/Character.png")

#fonts for score, first one for the score display when you died, second one for score display in game
font_score = pygame.font.SysFont("Comic Sans MS", 100)
font_score1 = pygame.font.SysFont("Comic Sans MS", 24)


#gamemap
# every 2 is a cornerblock (barrier to not cross into ouf bounds area)
# every 1 is a baddie, an enemy block
# every 0 is ... well nothing
screen_map = [
    [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2],
    [2, 2, 2, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 2, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 2, 2, 2], ]

#the characters stats/statistics
class CharacterStats:
    score = -1

    # define movement options
    # if the movement option is True, then the direction changes
    # controlled by "A" and "D" keys
    #used in the pygame event loop
    movement_left = False
    movement_right = False

    #spawnlovation is at 200/350 (middle bottom of screen)
    character_location_spawn = [200, 350]

    #here the character_location is defined and displays the characters current location
    character_location_current = character_location_spawn

    # fallspeed of player, increases with the score by 0.2 by score point
    character_fallspeed = adjust_for_framerate(4.5, framerate)
    #render the players
    character_hitbox = pygame.Rect(character_location_current[0],
                                   character_location_current[1],
                                   character_animation_neutral.get_width(),
                                   character_animation_neutral.get_height())


check_for_highscore = True

#0 is normal game state, 1 is the death screen
Menu_Screen = 0

#please just rework this whole system thanks
#also please if this stays in find an exploit where this never gets set to false so you get infinite points
#if you find one explain it to me and dm me on dc at "ner♡#2707" (with the heart), I won't fix it then
character_invincible = True

#list of all enemies (1s in the game map)
tile_baddies = []

#the game map, but a different one ig(?)
tile_rects = []

#pygame game loop, ends quit_out() is called
while True:

    #gamestate: if 0: normal game state, if 1: deathscreen
    if Menu_Screen == 0:

        #this is basically just me trying to implement a count in but really lazily
        #the player starts with -1 score and invincible, then gets "vincible" when having 0 score
        #if you want to exploit this, find a way to instantly get 1 score (somehow)
        if CharacterStats.score == 0:
            character_invincible = False
        if collision_test(CharacterStats.character_hitbox, tile_baddies):
            if not character_invincible:
                Menu_Screen = 1
        screen.fill((30, 100, 150))
        tile_rects = []  # Setting the game map
        y = 0
        for row in screen_map:
            x = 0
            for tile in row:
                if tile == 1:
                    screen.blit(block_baddie, (x * tile_x, y * tile_y))
                    tile_baddies.append(pygame.Rect(x * tile_x, y * tile_y, tile_x, tile_y))
                if tile == 2:
                    screen.blit(block_corner, (x * tile_x, y * tile_y))
                if tile != 0:
                    tile_rects.append(pygame.Rect(x * tile_x, y * tile_y, tile_x, tile_y))
                x += 1
            y += 1
        if CharacterStats.movement_left:  # Character movement
            if CharacterStats.character_location_current[0] >= 52:
                CharacterStats.character_location_current[0] -= adjust_for_framerate(6, framerate)
                left_hold += 1
        if CharacterStats.movement_right:
            if CharacterStats.character_location_current[0] + character_animation_neutral.get_width() <= 347:
                CharacterStats.character_location_current[0] += adjust_for_framerate(6, framerate)
                right_hold += 1
        if CharacterStats.character_location_current[1] >= 380:
            CharacterStats.character_location_current[1] = 0
            CharacterStats.score += 1

        #Gravity
        #First, we check if the characters location is at the bottom, then put him back uo
        #then we increment the score by (0.2 * the score) + fallspeed (= 4.5)
        if CharacterStats.character_location_current[1] <= 380:
            CharacterStats.character_location_current[1] += \
                CharacterStats.character_fallspeed + (0.2 * CharacterStats.score)

        #draw the character
        screen.blit(character_animation_neutral, (CharacterStats.character_location_current[0],
                                                  CharacterStats.character_location_current[1]))

        #have the hitbox of the character as the current characters location
        #the hitbox is always the same as the chars location (not like Celeste wink wink)
        CharacterStats.character_hitbox.x = CharacterStats.character_location_current[0]
        CharacterStats.character_hitbox.y = CharacterStats.character_location_current[1]

        #render the score at with colour white (255,255,255) with font size = 24
        textsurface2 = font_score1.render(str(CharacterStats.score), False, (255, 255, 255))

        #update the score render
        if CharacterStats.score >= 0:
            screen.blit(textsurface2, (15, 10))

        #Event loop
        for event in pygame.event.get():

            #define what happens when you quit by pressing the x in the corner
            if event.type == pygame.QUIT:

                #end the program
                quit_out()

            #what happens when you press any key down
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:

                    #when you press esc, the game quits out
                    quit_out()

                #just sets the movement value of the according direction as true which moves
                #moves the character in the corresponding direction
                if event.key == K_a:
                    CharacterStats.movement_left = True
                if event.key == K_d:
                    CharacterStats.movement_right = True

            #what happens when you release a key
            if event.type == KEYUP:

                #when you release "a", you stop moving the char to the left
                if event.key == K_a:
                    CharacterStats.movement_left = False
                    print("You moved " + str(left_hold) + " frames to the left")
                    left_hold = 0

                #when you release "d", you stop moving the char to the right
                if event.key == K_d:
                    CharacterStats.movement_right = False
                    print("You moved " + str(right_hold) + " frames to the right")
                    right_hold = 0

    #initiate the death screen
    #Menu_Screen is set to 1 when you die and set to 0 when you start/respawn
    if Menu_Screen == 1:

        if check_for_highscore:

            #open the highscore file
            opened_file = open("ImageFiles/Highscore.txt")

            #read the contents of the file
            high_score = opened_file.read()
            opened_file.close()
            try:
                opened_file = open("ImageFiles/Highscore.txt")
                file_content = opened_file.read()
                opened_file.close()
                if int(file_content) < CharacterStats.score:
                    opened_file = open("ImageFiles/Highscore.txt", "w")
                    opened_file.write(str(CharacterStats.score))
            except TypeError:
                opened_file = open("ImageFiles/Highscore.txt", "w")
                opened_file.write(str(CharacterStats.score))

            check_for_highscore = False

        #have the deathscreen as defined above as the background (probably poorly too)
        screen.blit(death_screen, (0, 0))

        #define and render the final score
        textsurface2 = font_score.render(str(CharacterStats.score), False, (30, 10, 10))
        screen.blit(textsurface2, (190, 250))

        #eventloop for deathscreen
        for event in pygame.event.get():

            #define what happens when pressing the nice x
            #run gets set to false and in turn the main loop and therefore the program stops
            if event.type == pygame.QUIT:
                run = False

            #define what happens when pressing Esc
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit_out()

            #check if space is pressed, restart the game
                if event.key == K_SPACE:

                    #reset all stats to default
                    Menu_Screen = 0
                    character_invincible = True
                    CharacterStats.movement_left = False
                    CharacterStats.movement_right = False
                    character_location_current = [200, 350]
                    CharacterStats.score = -1
                    check_for_highscore = True

    #draw everything that happened in the frame
    pygame.display.update()

    #clock here is used for framerate (as name implies :D)
    #framerate is normally at 30
    clock.tick(framerate)

    
