import pygame
import math
import random
import neat
import os

pygame.init()


WIN_WIDTH = 1280
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Runner")
font_64 = pygame.font.Font("assets/8-BITWONDER.TTF", 64)
font_48 = pygame.font.Font("assets/8-BITWONDER.TTF", 48)
font_24 = pygame.font.Font("assets/8-BITWONDER.TTF", 24)

gamename = font_64.render('RUNNER', True, (255, 255, 255))
gamename_rect = gamename.get_rect()
gamename_rect.center = (1280 // 2, 720 // 2)
gamestart = font_24.render('PRESS ANY BUTTON TO START', True, (255, 255, 255))
gamestart_rect = gamestart.get_rect()
gamestart_rect.center = (1280 // 2, 720 * 2 // 3)

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
        self.run_frame = 0
        self.jump_frame = 0
        self.slide_frame = 0
        self.distance = 0
        self.hitbox = pygame.Rect(self.x + 80, self.y + 30, 70, 115)

    def toggle_jump(self):
        self.is_jump = True
        self.is_run = False
        self.is_slide = False

    def jump(self):
        if self.jump_count >= -8:
            neg = 1
            if(self.jump_count < 0):
                neg = -1
            self.y -= (self.jump_count ** 2) * neg * 0.5
            self.jump_count -= 1
        else:
            self.is_jump = False
            self.is_run = True
            self.jump_count = 8

    def toggle_slide(self):
        self.is_slide = True
        self.is_jump = False   
        self.is_run = False

    def stop_slide(self):
        self.is_slide = False
        self.is_run = True
    
    def increment_distance(self):
        self.distance += 1

    def draw(self, win):
        if self.is_run: 
            self.hitbox = pygame.Rect(self.x + 80, self.y + 30, 70, 115)
            if self.run_frame + 1 >= 18:
                self.run_frame = 0
            win.blit(run[self.run_frame // 3], (self.x, self.y))
            self.run_frame += 1
        if self.is_jump:
            self.hitbox = pygame.Rect(self.x + 80, self.y + 30, 70, 100)
            if self.jump_frame + 1 >= 18:
                self.jump_frame = 0
            win.blit(jump[self.jump_frame // 5], (self.x, self.y))
            self.jump_frame += 1
            self.run_frame = 0
        if self.is_slide:
            self.hitbox = pygame.Rect(self.x + 80, self.y + 80, 65, 60)
            if self.slide_frame + 1 >= 6:
                self.slide_frame = 0
            win.blit(slide[self.slide_frame // 3], (self.x, self.y))
            self.slide_frame += 1
            self.run_frame = 0
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

class obstacle(object):
    def __init__(self, x, y, width, height, name, obst):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.obst = obst
        if self.name == "axe":
            self.hitbox = pygame.Rect(self.x + 10, self.y + 10, 45, 45)
        else:
            self.hitbox = pygame.Rect(self.x, self.y, 75, 75)

    def draw(self, win):
        if self.name == "axe":
            self.hitbox = pygame.Rect(self.x + 10, self.y + 10, 45, 45)
        else:
            self.hitbox = pygame.Rect(self.x, self.y, 75, 75)
        win.blit(self.obst, (self.x, self.y))
        return self.hitbox
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

def redraw_game_window(char, obstacles, obstacle_hitboxes):
    score = font_24.render("SCORE  " + str(char.distance), True, (255,255,255))
    score_rect = score.get_rect()
    score_rect.center = (1100, 100)
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x2, 0))
    win.blit(score, score_rect)
    char.draw(win)
    for obst in obstacles:
        obstacle_hitboxes.append(obst.draw(win))
    pygame.display.update()

def game_loop():
    running = True
    pygame.time.set_timer(pygame.USEREVENT, random.randrange(1000, 1200))
    pygame.time.set_timer(pygame.USEREVENT+1, random.randrange(900, 1100))
    pygame.time.set_timer(pygame.USEREVENT+2, random.randrange(800, 1000))
    pygame.time.set_timer(pygame.USEREVENT+3, random.randrange(700, 900))
    pygame.time.set_timer(pygame.USEREVENT+4, random.randrange(650, 800))
    pygame.time.set_timer(pygame.USEREVENT+5, random.randrange(650, 700))
    difficulty = 0
    char = player(300, WIN_HEIGHT - 228, 200, 148)
    obstacles = []
    obstacle_hitboxes = []
    while running:
        #frame rate
        clock.tick(30)

        #scrolling screen
        global bg_x
        global bg_x2
        bg_x -= 10
        bg_x2 -= 10
        if bg_x < bg.get_width() * -1:
            bg_x = bg.get_width()
        if bg_x2 < bg.get_width() * -1:
            bg_x2 = bg.get_width()
        char.increment_distance()
        
        difficulty = char.distance // 500

        #exit & slide end listeners
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYUP and char.is_slide:
                char.stop_slide()
            elif event.type == pygame.USEREVENT + difficulty:
                rand = random.randint(0, 1)
                if rand == 0:
                    obstacles.append(obstacle(WIN_WIDTH, WIN_HEIGHT - 139, 60, 59, "axe", axe))
                else:
                    obstacles.append(obstacle(WIN_WIDTH, WIN_HEIGHT - 239, 100, 157, "sign", sign))

        if(char.hitbox.collidelist(obstacle_hitboxes) != -1):
            running = False

        obstacle_hitboxes.clear()

        for obst in obstacles:
            obst.x -= 10
            if obst.x < 0:
                obstacles.remove(obst)

        #player input
        keys = pygame.key.get_pressed()
        if not(char.is_jump) and keys[pygame.K_SPACE]:
            char.toggle_jump()
        elif char.is_jump:
            char.jump()
        if not(char.is_slide) and not(char.is_jump) and keys[pygame.K_DOWN]:
            char.toggle_slide()
        

        #redraw function
        redraw_game_window(char, obstacles, obstacle_hitboxes)

game_loop()
pygame.quit()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(game_loop(), 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)