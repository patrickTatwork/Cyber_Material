import pygame
import sys
import random

WIDTH, HEIGHT = 800, 400
GROUND_Y = 300
GRAVITY = 1
JUMP_VELOCITY = -15
OBSTACLE_INTERVAL = 1500


def create_character(name: str) -> pygame.Surface:
    """Return a simple surface representing the chosen character."""
    if name == "Trecek":
        height = 80
    else:
        height = 60

    surf = pygame.Surface((40, height), pygame.SRCALPHA)
    body_color = (255, 224, 189)
    # body
    pygame.draw.rect(surf, body_color, pygame.Rect(10, height - 40, 20, 40))
    # head
    pygame.draw.circle(surf, body_color, (20, height - 50), 10)

    if name == "Parijs":
        # hair
        pygame.draw.rect(surf, (139, 69, 19), pygame.Rect(10, height - 60, 20, 10))
        # beard
        pygame.draw.rect(surf, (139, 69, 19), pygame.Rect(10, height - 45, 20, 5))
    elif name == "Szeto":
        # glasses
        pygame.draw.rect(surf, (0, 0, 0), pygame.Rect(12, height - 54, 16, 8), 1)
        # beard
        pygame.draw.rect(surf, (80, 50, 20), pygame.Rect(10, height - 45, 20, 5))
    return surf


def character_select_screen(screen: pygame.Surface, font: pygame.font.Font) -> str:
    """Display a character select screen and return the chosen character."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "Trecek"
                if event.key == pygame.K_2:
                    return "Parijs"
                if event.key == pygame.K_3:
                    return "Szeto"

        screen.fill((255, 255, 255))
        title = font.render("Kessler Run", True, (0, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        instructions = font.render("Select your runner: 1) Trecek 2) Parijs 3) Szeto", True, (0, 0, 0))
        screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 150))
        pygame.display.flip()


def game_loop(screen: pygame.Surface, font: pygame.font.Font, character: str) -> None:
    player_surf = create_character(character)
    player_rect = player_surf.get_rect(midbottom=(80, GROUND_Y))
    obstacle_surf = pygame.Surface((20, 40))
    obstacle_surf.fill((255, 0, 0))

    obstacle_rects: list[pygame.Rect] = []
    OBSTACLE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(OBSTACLE_EVENT, OBSTACLE_INTERVAL)

    player_gravity = 0
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= GROUND_Y:
                    player_gravity = JUMP_VELOCITY
            if event.type == OBSTACLE_EVENT:
                obstacle_rects.append(obstacle_surf.get_rect(midbottom=(WIDTH + 20, GROUND_Y)))

        player_gravity += GRAVITY
        player_rect.y += player_gravity
        if player_rect.bottom >= GROUND_Y:
            player_rect.bottom = GROUND_Y

        obstacle_rects = [obstacle.move(-5, 0) for obstacle in obstacle_rects if obstacle.x > -20]
        for obstacle in obstacle_rects:
            if player_rect.colliderect(obstacle):
                return

        # Draw background
        screen.fill((135, 206, 235))
        pygame.draw.rect(screen, (238, 214, 175), pygame.Rect(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        for obstacle in obstacle_rects:
            screen.blit(obstacle_surf, obstacle)
        screen.blit(player_surf, player_rect)

        score = (pygame.time.get_ticks() - start_time) // 1000
        score_surf = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()
        clock.tick(60)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kessler Run")
    font = pygame.font.Font(None, 36)
    character = character_select_screen(screen, font)
    game_loop(screen, font, character)


if __name__ == "__main__":
    main()
