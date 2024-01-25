# Example file showing a circle moving on screen
import pygame
import numpy as np


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
STEP_SIZE = 300
BORDER_WIDTH = 15
grav = 1000
player_pos = pygame.Vector2(screen.get_width() / 2, 0)#screen.get_height() / 2)
player_vel = pygame.Vector2(0, 0)
player_accel = pygame.Vector2(0, grav)
fixed = True
won = False
level = 1

paddle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - BORDER_WIDTH)
paddle_width = 100
paddle_direction = 1
paddle_speed = 700

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    if fixed:
        player_accel.x = player_accel.y = 0
        player_vel.x = player_vel.y = 0
    else: 
        player_accel.y = grav
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")     
    #pygame.draw.circle(screen, "black", player_pos, 10)
    pygame.draw.rect(screen, "blue", pygame.Rect(player_pos, (10, 10)))
    pygame.draw.line(screen, "black", (paddle_pos.x - paddle_width / 2, paddle_pos.y), (paddle_pos.x + paddle_width / 2,paddle_pos.y), width=50)
    keys = pygame.key.get_pressed()

    player_vel.x = (player_vel.x + player_accel.x * dt)
    player_vel.y = (player_vel.y + player_accel.y * dt)
    
    player_pos.x = np.clip(player_pos.x + player_vel.x * dt, 0 + BORDER_WIDTH, screen.get_width() - BORDER_WIDTH)
    player_pos.y = np.clip(player_pos.y + player_vel.y * dt, 0 + BORDER_WIDTH, screen.get_height() - BORDER_WIDTH)
    
    if (
        np.abs(player_pos.x - paddle_pos.x) < paddle_width / 4 
        and np.abs(player_pos.y - paddle_pos.y) < paddle_width / 4 
        and (not player_pos.y == screen.get_height() - BORDER_WIDTH)
    ):
        player_vel.x = player_vel.y = 0
        won = True
        paddle_direction = 0
    
    new_pos = paddle_pos.x + paddle_direction * paddle_speed * (1 + (level - 1)*.2) * dt
    if new_pos > screen.get_width() - BORDER_WIDTH:
        paddle_direction = -1 * paddle_direction
        new_pos = screen.get_width() - BORDER_WIDTH
    elif new_pos < BORDER_WIDTH:
        paddle_direction = -1 * paddle_direction
        new_pos = BORDER_WIDTH
    paddle_pos.x = new_pos
    
    if keys[pygame.K_r]:
        player_pos.y = BORDER_WIDTH
        if won:
            won = False
            paddle_direction = 1
            level += 1
            print(f'You won, new level - {level}')
        fixed = True
    
    if keys[pygame.K_SPACE]:
        fixed = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    # if keys[pygame.K_w]:
    #     player_pos.y -= STEP_SIZE * dt if player_pos.y - STEP_SIZE * dt > BORDER_WIDTH else 0
    # if keys[pygame.K_s]:
    #     player_pos.y += STEP_SIZE * dt if player_pos.y - STEP_SIZE * dt < screen.get_height() - BORDER_WIDTH else 0#screen.get_height() - 1
    # if keys[pygame.K_a]:
    #     player_pos.x -= STEP_SIZE * dt if player_pos.x - STEP_SIZE * dt > BORDER_WIDTH else 0
    # if keys[pygame.K_d]:
    #     player_pos.x += STEP_SIZE * dt if player_pos.x - STEP_SIZE * dt < screen.get_width() - BORDER_WIDTH else 0#screen.get_width() - 1

pygame.quit()