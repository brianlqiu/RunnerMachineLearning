import pygame
pygame.init()


WIN_WIDTH = 1280
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Runner")

slide = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-slide-0{frame}.png"), (200, 148)) for frame in range(0, 2)]
jump = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-jump-0{frame}.png"), (200, 148)) for frame in range(0, 6)]
run = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-run-0{frame}.png"), (200, 148)) for frame in range(0, 6)]
bg = pygame.image.load('assets/Background.png')
bg = pygame.transform.scale(bg, (1280, 720))

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

    def draw(self, win):
        if self.is_run: 
            if self.run_frame + 1 >= 18:
                self.run_frame = 0
            win.blit(run[self.run_frame//3], (self.x, self.y))
            self.run_frame += 1
        if self.is_jump:
            if self.jump_frame + 1 >= 18:
                self.jump_frame = 0
            win.blit(jump[self.jump_frame//3], (self.x, self.y))
            self.jump_frame += 1
        if self.is_slide:
            if self.slide_frame + 1 >= 6:
                self.slide_frame = 0
            win.blit(slide[self.slide_frame//3], (self.x, self.y))
            self.slide_frame += 1
        


def redraw_game_window():
    win.blit(bg, (0,0))
    char.draw(win)
    pygame.display.update()


running = True
char = player(300, WIN_HEIGHT - 228, 200, 148)
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP and char.is_slide:
            char.is_slide = False
            char.is_run = True
    
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
            char.y -= (char.jump_count ** 2) * neg
            char.jump_count -= 1
        else:
            char.is_jump = False
            char.is_run = True
            char.jump_count = 8
    if not(char.is_slide) and not(char.is_jump) and keys[pygame.K_DOWN]:
        char.is_slide = True
        char.is_jump = False   
        char.is_run = False

    redraw_game_window()

pygame.quit()