import pygame
import sys
import random
import time

#initializing pygame
pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

#initialize variables
display_x = 800
display_y = 700
window_x = 800
window_y = 600
block_size = 20 # you can vary block size among the given options (10, 20)

#setting display
gameDisplay = pygame.display.set_mode((display_x, display_y))
pygame.display.set_caption("Snake game")
gameDisplay.fill(white)
excess_y = display_y - window_y

#to update display
pygame.display.update()

pygame.font.init()
score_font =  pygame.font.SysFont("times new roman", 25)
lost_font = pygame.font.SysFont("arial", 50)
title_font = pygame.font.SysFont("comic sans ms", 68)
instruction_font = pygame.font.SysFont("courier new", 11)
rules_font = pygame.font.SysFont("courier new", 20)

if block_size == 20:
    img = pygame.image.load('head_20.png')
if block_size == 10:
    img = pygame.image.load('head_10.png')

#normal display functions used for better interface
def score_display(msg):
    screen_text = score_font.render("Score: " + str(msg), True, black)
    screen_rect = screen_text.get_rect()
    screen_rect.center = 50, 650
    gameDisplay.blit(screen_text, screen_rect)
def lost_display():
    screen_text = lost_font.render("YOU LOST!!!", True, red)
    screen_rect = screen_text.get_rect()
    screen_rect.center = (window_x/2), (window_y/2)
    gameDisplay.blit(screen_text, screen_rect)
    screen_text = score_font.render("Press SPACE to continue or ESC to quit", True, black)
    screen_rect = screen_text.get_rect()
    screen_rect.center = (window_x/2), (window_y/2)+100
    gameDisplay.blit(screen_text, screen_rect)
    pygame.display.update()
def title_display():
    screen_text = title_font.render("Snake Game", True, green)
    screen_rect = screen_text.get_rect()
    screen_rect.center = 275 , 650
    gameDisplay.blit(screen_text, screen_rect)
def instruction_display():
    screen_text = score_font.render("RULES", True, red)
    screen_rect = screen_text.get_rect()
    screen_rect.center = 625, 615
    gameDisplay.blit(screen_text, screen_rect)
    screen_text = instruction_font.render("1. You can cross the blue borders!", True, black)
    screen_rect = screen_text.get_rect()
    screen_rect.center = 625, 640
    gameDisplay.blit(screen_text, screen_rect)
    screen_text = instruction_font.render("2. Eat as many red balls as you can.", True, black)
    screen_rect = screen_text.get_rect()
    screen_rect.center = 625, 660
    gameDisplay.blit(screen_text, screen_rect)
    screen_text = instruction_font.render("3. If you touch yourself, the game will be over!", True, black)
    screen_rect = screen_text.get_rect()
    screen_rect.center = 625, 680
    gameDisplay.blit(screen_text, screen_rect)

#drawing boundary 
def boundary_draw():
    pygame.draw.rect(gameDisplay, blue, [0, window_y, window_x, 2])
    pygame.draw.rect(gameDisplay, blue, [0, 0, window_x, 2])
    pygame.draw.rect(gameDisplay, blue, [window_x - 2, 0, 2, window_y])
    pygame.draw.rect(gameDisplay, blue, [0, 0, 2, window_y])
    pygame.draw.rect(gameDisplay, blue, [100, window_y, 2, excess_y])
    pygame.draw.rect(gameDisplay, [100, 25, 175], [0, window_y, 100, excess_y])
    pygame.draw.rect(gameDisplay, [33, 66, 99], [102, window_y, 348, excess_y])
    pygame.draw.rect(gameDisplay, [50, 150, 100], [452, window_y, 348, excess_y])
    pygame.draw.rect(gameDisplay, blue, [450, window_y, 2, excess_y])

#introduction to the game
def intro_screen():
    intro_exit = False
    while not intro_exit:
        gameDisplay.fill(black)
        title = pygame.image.load('snake_game.png')
        title_rect = title.get_rect()
        title_rect.center = 400, 175
        gameDisplay.blit(title, title_rect)
        screen_text = score_font.render("Welcome to the game! Use arrow keys to move around. Have fun :)", True, white)
        screen_rect = screen_text.get_rect()
        screen_rect.center = 400, 350
        gameDisplay.blit(screen_text, screen_rect)
        screen_text = rules_font.render("Eat as many red and yellow balls as possible!", True, yellow)
        screen_rect = screen_text.get_rect()
        screen_rect.center = 400, 420
        gameDisplay.blit(screen_text, screen_rect)
        screen_text = rules_font.render("If the snake touches itself, the game will be over!", True, yellow)
        screen_rect = screen_text.get_rect()
        screen_rect.center = 400, 450
        gameDisplay.blit(screen_text, screen_rect)
        screen_text = rules_font.render("Yellow ball will boost your score and length", True, yellow)
        screen_rect = screen_text.get_rect()
        screen_rect.center = 400, 480
        gameDisplay.blit(screen_text, screen_rect)
        screen_text = rules_font.render("You can cross the border and it will appear on the other side ", True, yellow)
        screen_rect = screen_text.get_rect()
        screen_rect.center = 400, 510
        gameDisplay.blit(screen_text, screen_rect)
        screen_text = score_font.render("Press ENTER to start the game ", True, green)
        screen_rect = screen_text.get_rect()
        screen_rect.center = 400, 550
        gameDisplay.blit(screen_text, screen_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro_exit = True
    
#thank_you function
def thank_you():
    gameDisplay.fill([255, 255, 180])
    title = pygame.image.load('thank_you.jpeg')
    title_rect = title.get_rect()
    title_rect.center = (display_x/2), (display_y/2)
    gameDisplay.blit(title, title_rect)
    pygame.display.update()
    time.sleep(2)

#to rotate the head image
def head_rot(direction):
    if direction == 'left':
        head_rot = pygame.transform.rotate(img, 90)
    if direction == 'right':
        head_rot = pygame.transform.rotate(img, 270)
    if direction == 'down':
        head_rot = pygame.transform.rotate(img, 180)
    if direction == 'up':
        head_rot = img
    return head_rot

#game function... The whole game block
def game_function():
    # initializing variables used
    direction = 'right'
    game_exit = True
    lead_x = window_x/2
    lead_y = window_y/2
    clock = pygame.time.Clock()
    key_up = 2
    key_right = 2
    score = 1
    fps = 15
    big_ball = 0
    pace = block_size
    body = [[lead_x, lead_y], [lead_x-block_size, lead_y], [lead_x-(2*block_size), lead_y]]
    red_pos = [random.randint(1, ((window_x/pace)-1))*pace, random.randint(1, ((window_y/pace)-1))*pace]
    lead_x_change = pace
    lead_y_change = 0
    game_over = False
    head = img
    
    #function of games
    while game_exit:
        # to restart the game over and over (making user-friendly)
        while game_over:
            #displaying "lost" text/home/kaushek/activity_detection/
            lost_display()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_function()
                    if event.key == pygame.K_ESCAPE:
                        game_over = False
                        game_exit = False
        
        #key control functions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = False
            if event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_LEFT:
                    if key_right != 1:
                        lead_x_change = -1*pace
                        lead_y_change = 0
                        key_right = 0
                        key_up = 2
                        direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    if key_right != 0:
                        lead_x_change = pace
                        lead_y_change = 0
                        key_right = 1
                        key_up = 2
                        direction = 'right'
                elif event.key == pygame.K_DOWN:
                    if key_up != 1:
                        lead_x_change = 0
                        lead_y_change = pace
                        key_up = 0
                        key_right = 2
                        direction = 'down'
                elif event.key == pygame.K_UP:
                    if key_up != 0:
                        lead_x_change = 0
                        lead_y_change = -1*pace
                        key_right = 2
                        key_up = 1
                        direction = 'up'
        #updating the current lead position
        lead_x += lead_x_change
        lead_y += lead_y_change
        
        #To make the snake pass boundary and appear on the other side
        if lead_x > (window_x - pace):
            lead_x = 0
        elif lead_y > (window_y - pace):
            lead_y = 0
        elif lead_x < 0:
            lead_x = window_x - pace
        elif lead_y < 0:
            lead_y = window_y - pace
        new = [lead_x, lead_y]        
        
        #game over if the snake bi[]tes its own body
        for element in body:
            if lead_x == element[0] and lead_y == element[1]:
                game_over = True
        body.insert(0, new)
        temp = body.pop(len(body)-1)
        
        #big ball function (just an extras to make game better)
        if big_ball == 0:
            if lead_x == red_pos[0] and lead_y == red_pos[1]:
                red_pos.clear()
                red_pos.append(random.randint(1, ((window_x/pace)-1))*pace)
                red_pos.append(random.randint(1, ((window_y/pace)-1))*pace)
                score += 1
                body.append(temp)
        else:
            if (lead_x == red_pos[0]-(block_size) or lead_x == red_pos[0]) and (lead_y == red_pos[1]-(block_size) or lead_y == red_pos[1]):
                red_pos.clear()
                red_pos.append(random.randint(1, ((window_x/pace)-1))*pace)
                red_pos.append(random.randint(1, ((window_y/pace)-1))*pace)
                score += 12
                #increases the body size by 5 blocks after capturing the big ball
                tm = body[len(body)-1]
                x_pos = tm[0] - temp[0]
                y_pos = tm[1] - temp[1]
                if x_pos == 0:
                    if y_pos > 0:
                        o = -1
                    else:
                        o = 1
                    for q in range(0, 5, 1):
                        new_element = (temp[0], temp[1]+(o*q*(block_size)))
                        body.append(new_element)
                else:
                    if x_pos > 0:
                        o = -1
                    else:
                        o = 1
                    for q in range(0, 5, 1):
                        new_element = (temp[0]+(o*q*(block_size)), temp[1])
                        body.append(new_element)
                big_ball = 0
        
        gameDisplay.fill(white)
        
        #making another ball to appear
        if (score % 11 == 0):
            pygame.draw.rect(gameDisplay, yellow, [red_pos[0]-block_size, red_pos[1]-block_size, 2*block_size, 2*block_size])
            big_ball = 1
        else:
            pygame.draw.circle(gameDisplay, red, (red_pos[0] + (block_size/2), red_pos[1] + (block_size/2)), (block_size/2), 100)
        #drawing the boundary
        boundary_draw()
        
        #body alignment for the snake
        head =  0
        for box in body:
            #head part
            if head == 0:
                head_rotate = head_rot(direction)
                gameDisplay.blit(head_rotate, (box[0], box[1]))
            #body part
            elif head < (len(body)-1):
                pygame.draw.rect(gameDisplay, black, [box[0], box[1], block_size, block_size])
            #tail part
            else:
                x_pos = box[0] - temp[0]
                y_pos = box[1] - temp[1]
                if x_pos == 0 and y_pos == 0:
                    x_pos = body[len(body)-2][0] - temp[0]
                    y_pos = body[len(body)-2][1] - temp[1]
                if x_pos == 0:
                    if y_pos > 0:
                        pygame.draw.polygon(gameDisplay, black, [(box[0]+(block_size/2), box[1]), (box[0]+block_size, box[1]+block_size), (box[0], box[1]+block_size)])
                    else:
                        pygame.draw.polygon(gameDisplay, black, [(box[0], box[1]), (box[0]+block_size, box[1]), (box[0]+(block_size/2), box[1]+block_size)])
                else:
                    if x_pos > 0:
                        pygame.draw.polygon(gameDisplay, black, [(box[0]+block_size, box[1]), (box[0]+block_size, box[1]+block_size), (box[0], box[1]+(block_size/2))])
                    else:
                        pygame.draw.polygon(gameDisplay, black, [(box[0], box[1]), (box[0], box[1]+block_size), (box[0]+block_size, box[1]+(block_size/2))])
            head += 1
        
        #displays in the screen
        score_display(score-1)
        title_display()
        instruction_display()
        pygame.display.update()
        clock.tick(fps)
        
    thank_you()
    #uninitializing pygame
    pygame.quit()
    sys.exit()

intro_screen()
game_function()
