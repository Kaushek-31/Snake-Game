import pygame
import sys
import random
import time
import csv
import math

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

gameDisplay = pygame.display.set_mode((display_x, display_y))
pygame.display.set_caption("Snake game")
gameDisplay.fill(white)

pygame.display.update()

filename = 'movement_data.csv'

time_list = []
co_ord = []
with open(filename, 'r') as f:
    csv_reader = csv.DictReader(f)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        #time_list.append(row['0.8409717082977295'])
        time_list.append(row['Time'])
        #co_ord.append(row['n/d'])
        co_ord.append(row['Co-ordinate'])
        line_count += 1

block_size = 5
for i in range(len(time_list)-1):
    if co_ord[i] != 'n/d':
        co_or = co_ord[i].split(', ')
        x_co = co_or[0][1:]
        y_co = co_or[1][:-1]
        pygame.draw.rect(gameDisplay, red, [int(float(x_co)*(800/640)), int(float(y_co)*600/480), block_size, block_size])
        pygame.display.update()
    time.sleep(max(0, float(time_list[i+1])-float(time_list[i])))
    print(float(time_list[i+1])-float(time_list[i]))

time.sleep(5)
pygame.quit()
sys.exit()