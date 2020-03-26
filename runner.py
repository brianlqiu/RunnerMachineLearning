import pygame
import math
import random
import neat
import os

pygame.init()

GEN = 0

WIN_WIDTH = 1280
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Runner")
font_64 = pygame.font.Font("assets/8-BITWONDER.TTF", 64)
font_48 = pygame.font.Font("assets/8-BITWONDER.TTF", 48)
font_24 = pygame.font.Font("assets/8-BITWONDER.TTF", 24)

slide = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-slide-0{frame}.png"), (200, 148)) for frame in range(0, 2)]
jump = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-jump-0{frame}.png"), (200, 148)) for frame in range(2, 6)]
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
        self.is_slide = True
        self.jump_frame = 0
        self.slide_frame = 0
        self.hitbox = pygame.Rect(self.x + 80, self.y + 30, 70, 115)

    def jump(self):
        self.is_jump = True
        self.is_slide = False

    def move(self):
        if self.is_jump:
            if self.jump_count >= -8:
                neg = 1
                if(self.jump_count < 0):
                    neg = -1
                self.y -= (self.jump_count ** 2) * neg * 0.5
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.is_slide = True
                self.jump_count = 8

    def draw(self, win):
        if self.is_jump:
            self.hitbox = pygame.Rect(self.x + 80, self.y + 30, 70, 100)
            if self.jump_frame + 1 >= 18:
                self.jump_frame = 0
            win.blit(jump[self.jump_frame // 5], (self.x, self.y))
            self.jump_frame += 1
        if self.is_slide:
            self.hitbox = pygame.Rect(self.x + 80, self.y + 80, 65, 60)
            if self.slide_frame + 1 >= 6:
                self.slide_frame = 0
            win.blit(slide[self.slide_frame // 3], (self.x, self.y))
            self.slide_frame += 1
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

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

def redraw_game_window(chars, obstacles, obstacle_hitboxes, distance):
    global GEN
    score = font_24.render("SCORE  " + str(distance), True, (255,255,255))
    score_rect = score.get_rect()
    score_rect.center = (1100, 100)
    gen_num = font_24.render("GEN " + str(GEN), True, (255,255,255))
    gen_num_rect = gen_num.get_rect()
    gen_num_rect.center = (100, 100)
    alive = font_24.render("ALIVE " + str(len(chars)), True, (255,255,255))
    alive_rect = alive.get_rect()
    alive_rect.center = (100, 200)
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x2, 0))
    win.blit(score, score_rect)
    win.blit(gen_num, gen_num_rect)
    win.blit(alive, alive_rect)
    for char in chars:
        char.draw(win)
    for obst in obstacles:
        obstacle_hitboxes.append(obst.draw(win))
    pygame.display.update()



def eval_genomes(genomes, config):
    global GEN
    GEN += 1
    running = True
    pygame.time.set_timer(pygame.USEREVENT, random.randrange(1000, 1200))
    distance = 0

    chars = []
    nets = []
    ge = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        chars.append(player(300, WIN_HEIGHT - 228, 200, 148))
        genome.fitness = 0
        ge.append(genome)

    obstacles = []
    obstacle_hitboxes = []
    while running and len(chars) > 0:
        #frame rate
        clock.tick(60)

        #scrolling screen
        global bg_x
        global bg_x2
        bg_x -= 10
        bg_x2 -= 10
        if bg_x < bg.get_width() * -1:
            bg_x = bg.get_width()
        if bg_x2 < bg.get_width() * -1:
            bg_x2 = bg.get_width()

        nearest_obstacle_ind = 0
        distance += 1

        if len(chars) > 0 and len(obstacles) > 0:
            for i, obst in enumerate(obstacles):
                if(obst.x > 360):
                    nearest_obstacle_ind = i
                    break
            pygame.draw.rect(win, (255,0,0), obstacles[nearest_obstacle_ind].hitbox, 2)
            pygame.display.update()
            for i, char in enumerate(chars):
                if char.is_jump and abs(obstacles[nearest_obstacle_ind].hitbox.centerx - char.hitbox.centerx) >= 150:
                    ge[i].fitness -= 1
                elif char.is_jump and abs(obstacles[nearest_obstacle_ind].hitbox.centerx - char.hitbox.centerx) <= 150:
                    ge[i].fitness += 2
                else:
                    ge[i].fitness += 0.1

                char.move()
                output = nets[i].activate((obstacles[nearest_obstacle_ind].hitbox.centerx - char.hitbox.centerx, abs(obstacles[nearest_obstacle_ind].hitbox.centery - char.hitbox.centery)))
                if output[0] > 0.5:
                    char.jump()

        #exit & slide end listeners
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.USEREVENT:
                rand = random.randint(0, 1)
                """
                if rand == 0:
                    obstacles.append(obstacle(WIN_WIDTH - 300, WIN_HEIGHT - 239, 75, 75, "sign", sign))
                else:
                    obstacles.append(obstacle(WIN_WIDTH - 300, WIN_HEIGHT - 139, 45, 45, "axe", axe))
                """
                obstacles.append(obstacle(WIN_WIDTH - 300, WIN_HEIGHT - 139, 45, 45, "axe", axe))

        for i, char in enumerate(chars):
            if(char.hitbox.collidelist(obstacle_hitboxes) != -1):
                ge[i].fitness -= 1
                chars.pop(i)
                nets.pop(i)
                ge.pop(i)

        obstacle_hitboxes.clear()

        for obst in obstacles:
            obst.x -= 10
            if obst.x < 300:
                obstacles.remove(obst)

        #redraw function
        redraw_game_window(chars, obstacles, obstacle_hitboxes, distance)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, 200)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)