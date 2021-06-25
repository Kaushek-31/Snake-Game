import pygame
import sys
import time
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = 'kaushek-VivoBook-Flip-14-TP410UF'
port = 9999
IP = '127.0.0.2'

bound = 50
b_x = bound
b_y = int(bound * (480/640))
bound_fact_x = float(640/(640-(2*b_x)))
bound_fact_y = float(480/(480-(2*b_y)))

s.connect((IP, port))


pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

#initialize variables
display_x = 800
display_y = 600

block_size = 100

gameDisplay = pygame.display.set_mode((display_x, display_y))
pygame.display.set_caption("Block Game")
gameDisplay.fill(white)

#to update display
pygame.display.update()

pygame.font.init()
score_font =  pygame.font.SysFont("times new roman", 25)
win_font = pygame.font.SysFont("arial", 50)
title_font = pygame.font.SysFont("comic sans ms", 68)

#introduction to the game
def intro_screen():
    intro_exit = False
    while not intro_exit:
        gameDisplay.fill(white)
        screen_text = win_font.render("You have to map every block", True, black)
        screen_rect = screen_text.get_rect()
        screen_rect.center = (int(display_x/2), int(display_y/2))
        gameDisplay.blit(screen_text, screen_rect)
        screen_text = score_font.render("Right click mouse to move block", True, black)
        screen_rect = screen_text.get_rect()
        screen_rect.center = (int(display_x/2), int(display_y/2)+65)
        gameDisplay.blit(screen_text, screen_rect)
        screen_text = score_font.render("Press Enter to continue", True, black)
        screen_rect = screen_text.get_rect()
        screen_rect.center = (int(display_x/2), int(display_y/2)+100)
        gameDisplay.blit(screen_text, screen_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro_exit = True

#thank_you function
def thank_you():
    gameDisplay.fill([255, 255, 180])
    title = title_font.render("Thanks!!", True, black)
    title_rect = title.get_rect()
    title_rect.center = (display_x/2), (display_y/2)
    gameDisplay.blit(title, title_rect)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

def intersect_block(block_pos, click_block):
    #code
    click_block -= (click_block % 2)
    if abs(block_pos[click_block][0] - block_pos[click_block+1][0]) < (block_size/2):
        if abs(block_pos[click_block][1] - block_pos[click_block+1][1]) < (block_size/2):
            return True
        else:
            return False
    else:
        return False
            
def end_check(block_pos):
    count = 0
    for i in range(int(len(block_pos)/2)):
        if block_pos[2*i][:] == block_pos[(2*i)+1][:]:
            count += 2
    if count == len(block_pos):
        return True
    else:
        return False

def game_function():
    gameDisplay.fill(white)
    pygame.display.update()
    mouse_pos = [0, 0]
    game_run = True
    cursor = pygame.image.load('cursor_3.png')
    cursor = pygame.transform.scale(cursor, (26, 40))
    #block initialization
    block_a1 = [0, 0, red]
    block_a2 = [800-block_size, 600-block_size, red]
    block_b1 = [800-block_size, 0, blue]
    block_b2 = [0, 600-block_size, blue]
    
    block_pos = [block_a1, block_a2, block_b1, block_b2]
    
    #mouse_click on block
    click = False
    click_block = 4
    while game_run:
        
        message = s.recv(100).decode('utf-8')
        print(message)
        
        if message == 'n/d, n/d':
            print("Place your index finger in front of the camera")
        else:
            cur_pos = message[:-1]
            pick = True if message[-1] == 'p' else False
            scale = [640, 480]
            mouse_pos = cur_pos.split(', ')
            mouse_pos[0] = int((float(mouse_pos[0]) - b_x) * (display_x/scale[0])*bound_fact_x) 
            mouse_pos[1] = int((float(mouse_pos[1]) - b_y) * (display_y/scale[1])*bound_fact_y)
            
            for i in range(len(block_pos)):
                mouse_x, mouse_y = mouse_pos
                if pick == True:
                    if mouse_x >= block_pos[i][0] and mouse_x <= block_pos[i][0]+block_size:
                        if mouse_y >= block_pos[i][1] and mouse_y <= block_pos[i][1]+block_size:
                            click_block = i
                            click = True
                else:
                    click_block = 4
                    click = False
            
        if click == True:
            mouse_x, mouse_y = mouse_pos
            if not intersect_block(block_pos, click_block):
                block_pos[click_block][0] = max(0, mouse_x - (block_size/2))
                block_pos[click_block][1] = max(0, mouse_y - (block_size/2))
                block_pos[click_block][0] = min(block_pos[click_block][0], display_x-(block_size))
                block_pos[click_block][1] = min(block_pos[click_block][1], display_y-(block_size))
            else:
                if click_block % 2 == 0:
                    block_pos[click_block] = block_pos[click_block+1][:]
                else:
                    block_pos[click_block] = block_pos[click_block-1][:]
                

        gameDisplay.fill(white)
        
        cursor_rect = cursor.get_rect()
        cursor_rect.center = mouse_pos
        
        for b in block_pos:
            pygame.draw.rect(gameDisplay, b[2], [b[0], b[1], block_size, block_size])
        
        gameDisplay.blit(cursor, cursor_rect)
        pygame.display.update()
        
        if end_check(block_pos):
            game_run = False
            screen_text = win_font.render("You have mapped every block", True, black)
            screen_rect = screen_text.get_rect()
            screen_rect.center = (int(display_x/2), int(display_y/2))
            gameDisplay.blit(screen_text, screen_rect)
            pygame.display.update()
            time.sleep(2)

intro_screen()
game_function()
thank_you()