import random
import pygame

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

player_width = 100
player_height = 10
player_x = (WIDTH - player_width) //2
player_y = HEIGHT - player_height - 10
player_speed = 10000000

ai_width = 100
ai_height = 10
ai_x = (WIDTH - player_width) //2
ai_y = 10
ai_speed = 10000000

ball_radius = 15
ball_x = WIDTH / 2
ball_y = HEIGHT / 2
ball_speed_x = random.choice([-3,3])
ball_speed_y = 3

score_player = 0
score_ai = 0
game_over = False
game_started = False

def game_over_screen(winner):
    font = pygame.font.SysFont(None, 72)
    text = font.render(f'{winner} Wins!', True,
                       (0, 0, 0))
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 3, HEIGHT //3))
    pygame.display.update()
    pygame.time.wait(3000)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_started:
            game_started = True

    if game_started:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x >0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        if ai_x + ai_width / 10 < ball_x:
            ai_x += ai_speed
        elif ai_x + ai_width / 10 > ball_x:
            ai_x -= ai_speed

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_x <= 0 or ball_x >= WIDTH - ball_radius:
            ball_speed_x = -ball_speed_x

        if player_y <= ball_y + ball_radius <= player_y + player_height and player_x <= ball_x <= player_x + player_width:
            ball_speed_y = -ball_speed_y

        if ai_y <= ball_y - ball_radius <= ai_y + ai_height and ai_x <= ball_x <= ai_x + ai_width:
            ball_speed_y = -ball_speed_y

        if ball_y - ball_radius < ai_y + ai_height:
            ball_y = ai_y + ai_height + ball_radius

        if ball_y > HEIGHT:
            game_over = True
            game_over_screen('AI')

        if ball_y < 0:
            game_over = True
            game_over_screen('PLAYER')

        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
        pygame.draw.rect(screen, RED, (ai_x, ai_y, ai_width, ai_height))
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Player: {score_player} AI: {score_ai}',
                             True, (0, 0, 0))
        screen.blit(score_text, (10,10))

    else:
        font = pygame.font.SysFont(None, 72)
        text = font.render("Press Space to Start", True, (0,0,0))
        screen.fill(WHITE)
        screen.blit(text, (WIDTH // 4, HEIGHT // 3))

    pygame.display.update()
    clock.tick(60)

pygame.quit()


