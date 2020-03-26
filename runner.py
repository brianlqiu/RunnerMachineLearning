import pygame
pygame.init()


WIN_WIDTH = 1280
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Runner")


width = 40
height = 60
x = 0
y = WIN_HEIGHT - height
vel = 20

is_jump = False
jump_count = 5

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
    """
    if keys[pygame.K_UP]:
        if y < vel:
            y = 0
        else:
            y -= vel
    """
    
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
    """
    if keys[pygame.K_DOWN]:
        if y > WIN_HEIGHT - height - vel:
            y = WIN_HEIGHT - height
        else:
            y += vel
    """

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

pygame.quit()