import numpy as np
import pygame, sys
import time
from pygame.locals import *
from maze import Maze
import random as r

def get_info():
    show_minimap = False
    while True:
        try:
            seed = input("Seed: ")
            if "cheatcode999" == seed:
                show_minimap = True
                print("permanent minimap aktiviert!")
                seed = input("Seed: ")
            if seed != "":
                r.seed(int(seed))
            size = int(input("Größe: "))
            print("Generating Maze...")
            break
        except:
            print("Invalid Input Format. Versuchs nochmal!")
    if size > 101:
        print("Zu großes Labyerynth - Größe wurde auf 101 gestellt!")
        size = 101
    elif size < 21:
        print("Zu kleines Laberynth - Größe wurde auf 21 gesetzt!")
        size = 21
    if size % 2 == 0:
        size -= 1
    return show_minimap, size

def minimap(): 
    x_step = (pygame.display.get_surface().get_width() // len(maze[0])) // 5
    y_step = x_step
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            color = (255,255,255)
            if maze[i][j] == 1:
                color = (0,0,0)
            elif maze[i][j] == 2:
                color = (0,255,00)
            if i == int(posx) and j == int(posy):
                color = (0,0,255)
            pygame.draw.rect(display,color,(x_step * j, y_step * i, x_step, y_step))
    pygame.display.update()

def handle_inputs(fov, posx, posy, rot):
    start_time = 0
    keys=pygame.key.get_pressed()
    if keys[K_LEFT]:
        rot -= np.pi / 100
    if keys[K_RIGHT]:
        rot += np.pi / 100
    if keys[K_UP]:
        posx += 0.02 * np.cos(rot)
        posy += 0.02 * np.sin(rot)
    if keys[K_DOWN]:
        posx -= 0.02 * np.cos(rot)
        posy -= 0.02 * np.sin(rot)
    if keys[K_w]:
        fov += 1
    if keys[K_s]:
        fov -= 1
    if keys[K_q]:
        posx, posy = (1,1)
        rot = np.pi / 4
        fov = 125
        print("minimap visible for 10 sec")
        minimap()
        time.sleep(10)
    return fov, posx, posy, rot

def draw(fov, posx, posy, rot, c_m):
    for i in range(fov):
        rot_i = rot + (np.pi * (i - (fov / 2))) / 180
        sin, cos = (0.02 * np.sin(rot_i), 0.02 * np.cos(rot_i))
        x, y = (posx, posy)
        print(maze[int(x)][int(y)])
        n = 0
        while maze[int(x)][int(y)] == 0:
            x, y = (x + cos, y + sin)
            n += 1
        try:
            h = 1 / (0.02 * n)
        except ZeroDivisionError:
            display.fill((255,0,0))
            posx, posy = (1,1)
            rot = np.pi / 4
            fov = 125
            break
        x_coord = (pygame.display.get_surface().get_width() / fov)
        height = pygame.display.get_surface().get_height() * h
        y_coord = (pygame.display.get_surface().get_height() / 2) - height / 2
        color = c_m[int(x)][int(y)]
        if maze[int(x)][int(y)] == 2:
            color = (0,255,0)
        pygame.draw.rect(display,color,(x_coord * i, y_coord, x_coord, height))
    return posx, posy, rot, fov

def make_colors(maze):
    color_maze = list()
    for line in maze:
        new_line = []
        for i in line:
            value = []
            for c in range(3):
                value.append(r.randint(50,100))
            new_line.append(value)
        color_maze.append(new_line)
    return color_maze

show_minimap = False
maze_object = Maze()
show_minimap, size = True, 21
maze_layout = [[0 for i in range(size)] for k in range(size)]
maze = maze_object.gen(maze_layout)
maze[-2][-2] = 2
clock = pygame.time.Clock()
start_time = time.time()
color_maze = make_colors(maze)
print("GO!")
posx, posy = (1,1)
rot = np.pi / 4
fov = 125
moved = False

pygame.init()
display = pygame.display.set_mode((1500, 800), 0, 32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display.fill((255,255,255))
    posx, posy, rot, fov = draw(fov, posx, posy, rot, color_maze)
    fov, posx, posy, rot = handle_inputs(fov, posx, posy, rot)
    if show_minimap:
        minimap()
    pygame.display.update()

    if posx > size - 2.5 and posy > size - 2.5:
        end_time = time.time() - start_time
        print("GESCHAFFT! In " + str(round(end_time,3)) + "s")
        pygame.quit()
        sys.exit()
    
    clock.tick(60)

    
