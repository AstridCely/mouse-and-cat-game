import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ENEMY_SPEED = 1.2  # Velocidad de los enemigos (gatos)
PLAYER_SPEED = 5  # Velocidad del jugador (ratón)
GAME_SPEED = 60   # Velocidad del juego (FPS)

# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mouse and Cat Game🐱‍👓🐭')

# Cargar imágenes
background = pygame.image.load('assets/background.png').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
mouse_img = pygame.image.load('assets/mouse.png').convert_alpha()
mouse_img = pygame.transform.scale(mouse_img, (50, 50))
cat_img = pygame.image.load('assets/cat.png').convert_alpha()
cat_img = pygame.transform.scale(cat_img, (50, 50))
cheese_img = pygame.image.load('assets/cheese.png').convert_alpha()
cheese_img = pygame.transform.scale(cheese_img, (50, 50))

# Fuentes
font = pygame.font.Font(None, 36)

# Función para dibujar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Función para mostrar el menú de inicio
def show_start_screen():
    screen.blit(background, (0, 0))
    draw_text("Mouse and Cat Game", font, BLACK, screen, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100)
    draw_text("Press any key to start ", font, WHITE, screen, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Función para mostrar el menú de fin de juego
def show_game_over_screen():
    screen.blit(background, (0, 0))
    draw_text("Game Over!", font, RED, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
    draw_text("Press R to play again or ESC to quit", font, WHITE, screen, SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
    return False

# Función para mostrar el menú de victoria
def show_win_screen():
    screen.blit(background, (0, 0))
    draw_text("You Won! Has alcanzado el queso!", font, GREEN, screen, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50)
    draw_text("Press C to continue or ESC to quit", font, WHITE, screen, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_c:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
    return False

# Configuración del juego
start_game = True
game_over = False
win_game = False
score = 0
player_rect = pygame.Rect(50, 50, 50, 50)
player_speed_x = 0
player_speed_y = 0
cheese_rect = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 50, 50)
enemies = []
for _ in range(3):  # Agregar 3 enemigos adicionales
    enemy = pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50), 50, 50)
    enemies.append(enemy)

# Bucle principal
clock = pygame.time.Clock()
while True:
    if start_game:
        show_start_screen()
        start_game = False

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Lógica del juego
    if not game_over and not win_game:
        keys = pygame.key.get_pressed()
        player_speed_x = 0
        player_speed_y = 0
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_speed_x = PLAYER_SPEED
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_speed_y = -PLAYER_SPEED
        if keys[pygame.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
            player_speed_y = PLAYER_SPEED

        player_rect.x += player_speed_x
        player_rect.y += player_speed_y

        # Mover a los enemigos (gatos) hacia el jugador (ratón)
        for enemy in enemies:
            if not win_game:  # Solo persiguen al ratón si no ha ganado
                if enemy.x < player_rect.x:
                    enemy.x += ENEMY_SPEED
                elif enemy.x > player_rect.x:
                    enemy.x -= ENEMY_SPEED

                if enemy.y < player_rect.y:
                    enemy.y += ENEMY_SPEED
                elif enemy.y > player_rect.y:
                    enemy.y -= ENEMY_SPEED

                # Colisión entre el jugador (ratón) y los enemigos (gatos)
                if player_rect.colliderect(enemy):
                    game_over = True

        # Colisión entre el jugador (ratón) y el queso
        if player_rect.colliderect(cheese_rect):
            win_game = True
            score = 1000  # Aumentar el puntaje al alcanzar el queso

        # Dibujar elementos en la pantalla
        screen.blit(background, (0, 0))
        screen.blit(cheese_img, cheese_rect)
        screen.blit(mouse_img, player_rect.topleft)
        for enemy in enemies:
            screen.blit(cat_img, enemy)

        # Mostrar puntuación
        draw_text(f"Score: {score}", font, WHITE, screen, 10, 10)

        # Mensajes de estado
        if win_game:
            draw_text("Has alcanzado el queso!", font, GREEN, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
            
        if game_over:
            draw_text("Game Over!", font, RED, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            draw_text("Press R to play again or ESC to quit", font, WHITE, screen, SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 50)

        # Actualizar pantalla
        pygame.display.flip()

        # Controlar la velocidad de actualización del juego
        clock.tick(GAME_SPEED)

    # Si el juego termina
    elif game_over:
        if show_game_over_screen():
            # Reiniciar juego
            player_rect.x = 50
            player_rect.y = 50
            game_over = False
            win_game = False
            score = 0
            for enemy in enemies:
                enemy.x = random.randint(50, SCREEN_WIDTH - 50)
                enemy.y = random.randint(50, SCREEN_HEIGHT - 50)
        else:
            pygame.quit()
            sys.exit()
    
    # Si el jugador gana
    elif win_game:
        if show_win_screen():
            # Continuar juego (resetear posición del ratón)
            player_rect.x = 50
            player_rect.y = 50
            win_game = False
            score = 0
            for enemy in enemies:
                enemy.x = random.randint(50, SCREEN_WIDTH - 50)
                enemy.y = random.randint(50, SCREEN_HEIGHT - 50)
        else:
            pygame.quit()
            sys.exit()

