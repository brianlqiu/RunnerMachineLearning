import pygame
pygame.init()


WIN_WIDTH = 1280
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Runner")

slide = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-slide-0{frame}.png"), (100, 74)) for frame in range(0, 2)]
jump = [pygame.image.load(f"assets/adventurer-jump-0{frame}.png") for frame in range(0, 6)]
run = [pygame.transform.scale(pygame.image.load(f"assets/adventurer-run-0{frame}.png"), (200, 148)) for frame in range(0, 6)]
bg = pygame.image.load('assets/Background.png')
bg = pygame.transform.scale(bg, (1280, 720))

clock = pygame.time.Clock()

width = 200
height = 148
x = 300
y = WIN_HEIGHT - height - 80
vel = 20

is_jump = False
jump_count = 8

distance = 0

is_slide = False

run_count = 0

def redraw_game_window():
    global run_count
    win.blit(bg, (0,0))
    if run_count + 1 >= 18:
        run_count = 0
    win.blit(run[run_count//3], (x,y))
    run_count += 1
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
    elif is_jump:
        if jump_count >= -8:
            neg = 1
            if(jump_count < 0):
                neg = -1
            y -= (jump_count ** 2) * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 8
    redraw_game_window()

pygame.quit()