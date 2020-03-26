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

width = 200
height = 148
x = 300
y = WIN_HEIGHT - height - 80
vel = 20

is_run = True
is_jump = False
jump_count = 8

distance = 0

is_slide = False

run_frame = 0
jump_frame = 0

def redraw_game_window():
    global run_frame
    global jump_frame
    win.blit(bg, (0,0))
    if is_run: 
        if run_frame + 1 >= 18:
            run_frame = 0
        win.blit(run[run_frame//3], (x,y))
        run_frame += 1
    if is_jump:
        if jump_frame + 1 >= 18:
            jump_frame = 0
        win.blit(jump[jump_frame//3], (x,y))
        jump_frame += 1
    pygame.display.update()


running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if not(is_jump) and keys[pygame.K_SPACE]:
        is_jump = True
        is_run = False
    elif is_jump:
        if jump_count >= -8:
            neg = 1
            if(jump_count < 0):
                neg = -1
            y -= (jump_count ** 2) * neg
            jump_count -= 1
        else:
            is_jump = False
            is_run = True
            jump_count = 8
    redraw_game_window()

pygame.quit()