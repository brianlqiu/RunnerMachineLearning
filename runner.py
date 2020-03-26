import pygame
import math
import random
pygame.init()


WIN_WIDTH = 1280
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Runner")

slide = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-slide-0{frame}.png"), (200, 148)) for frame in range(0, 2)]
jump = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-jump-0{frame}.png"), (200, 148)) for frame in range(2, 6)]
run = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-run-0{frame}.png"), (200, 148)) for frame in range(0, 6)]
bg = pygame.transform.scale(pygame.image.load('assets/Background.png'), (1280, 720))
axe = pygame.transform.scale(pygame.image.load("assets/groundaxe.png"), (60, 59))
sign = pygame.transform.scale(pygame.image.load("assets/sign.png"), (100, 157))
bg_x = 0
bg_x2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_jump = False
        self.jump_count = 8
        self.is_run = True
        self.is_slide = False
        self.distance = 0
        self.run_frame = 0
        self.jump_frame = 0
        self.slide_frame = 0
        self.hitbox = (self.x + 80, self.y + 30, 90, 115)

    def draw(self, win):
        if self.is_run: 
            self.hitbox = (self.x + 80, self.y + 30, 70, 115)
            if self.run_frame + 1 >= 18:
                self.run_frame = 0
            win.blit(run[self.run_frame // 3], (self.x, self.y))
            self.run_frame += 1
        if self.is_jump:
            self.hitbox = (self.x + 80, self.y + 30, 70, 100)
            if self.jump_frame + 1 >= 18:
                self.jump_frame = 0
            win.blit(jump[self.jump_frame // 5], (self.x, self.y))
            self.jump_frame += 1
            self.run_frame = 0
        if self.is_slide:
            self.hitbox = (self.x + 50, self.y + 80, 95, 60)
            if self.slide_frame + 1 >= 6:
                self.slide_frame = 0
            win.blit(slide[self.slide_frame // 3], (self.x, self.y))
            self.slide_frame += 1
            self.run_frame = 0

class obstacle(object):
    def __init__(self, x, y, width, height, obst):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.obst = obst

    def draw(self, win):
        win.blit(self.obst, (self.x, self.y))


def redraw_game_window():
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x2, 0))
    char.draw(win)
    for obst in obstacles:
        obst.draw(win)
    pygame.display.update()


running = True
char = player(300, WIN_HEIGHT - 228, 200, 148)
obstacles = []
pygame.time.set_timer(pygame.USEREVENT+2, random.randrange(610, 1000))
while running:
    #frame rate
    clock.tick(30)

    #rules for obstacle generation
    #8 frames to reach peak jump
    #9 frames to return to ground
    #0 frames to start sliding
    #ground -> ground = distance of at least 17 frames
    #ground -> air = distance of at least 9 frames
    #air -> ground = distance of at least 8 frames
    #air -> air = distance of at least 0 frames

    #scrolling screen
    bg_x -= 10
    bg_x2 -= 10
    if bg_x < bg.get_width() * -1:
        bg_x = bg.get_width()
    if bg_x2 < bg.get_width() * -1:
        bg_x2 = bg.get_width()
    char.distance += 1

    #exit & slide end listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP and char.is_slide:
            char.is_slide = False
            char.is_run = True
        elif event.type == pygame.USEREVENT+2:
            rand = random.randint(0, 1)
            if rand == 0:
                obstacles.append(obstacle(WIN_WIDTH, WIN_HEIGHT - 139, 60, 59, axe))
            else:
                obstacles.append(obstacle(WIN_WIDTH, WIN_HEIGHT - 239, 60, 59, sign))


    for obst in obstacles:
        obst.x -= 10

    #player input
    keys = pygame.key.get_pressed()
    if not(char.is_jump) and keys[pygame.K_SPACE]:
        char.is_jump = True
        char.is_run = False
        char.is_slide = False
    elif char.is_jump:
        if char.jump_count >= -8:
            neg = 1
            if(char.jump_count < 0):
                neg = -1
            char.y -= (char.jump_count ** 2) * neg * 0.5
            char.jump_count -= 1
        else:
            char.is_jump = False
            char.is_run = True
            char.jump_count = 8
    if not(char.is_slide) and not(char.is_jump) and keys[pygame.K_DOWN]:
        char.is_slide = True
        char.is_jump = False   
        char.is_run = False
    

    #redraw function
    redraw_game_window()

pygame.quit()