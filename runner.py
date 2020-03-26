import pygame
pygame.init()


WIN_WIDTH = 1280
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Runner")

run = []
slide = []
jump = []
bg = pygame.image.load('assets/Background.png')
bg = pygame.transform.scale(bg, (1280, 720))

for i in range(0, 5):
    run.append(pygame.image.load('assets/adventurer-run-0' + str(i) + '.png'))
    jump.append(pygame.image.load('assets/adventurer-jump-0' + str(i) + '.png'))
    if i < 2:
        slide.append(pygame.image.load('assets/adventurer-slide-0' + str(i) + '.png'))



width = 50
height = 37
x = 0
y = WIN_HEIGHT - height
vel = 20

is_jump = False
jump_count = 5

walk_count = 0

is_slide = False

def redraw_game_window():
    global walk_count
    win.blit(bg, (0,0))
    pygame.display.update()


run = True
while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if x < vel:
            x = 0
        else:
            x -= vel
    if keys[pygame.K_RIGHT]:
        if x > WIN_WIDTH - width - vel:
            x = WIN_WIDTH - width
        else: 
            x += vel
    if not(is_jump) and keys[pygame.K_SPACE]:
        is_jump = True
    elif is_jump:
        if jump_count >= -5:
            neg = 1
            if(jump_count < 0):
                neg = -1
            y -= (jump_count ** 2) * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 5
    redraw_game_window()

pygame.quit()