import pygame
import random
import sys

pygame.init()

# Dimensions et fenêtre
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump Light")
clock = pygame.time.Clock()

# Couleurs
DARK_BG = (15, 15, 25)
PLAYER_COLOR = (0, 255, 157)    # Vert néon
PLATFORM_COLOR = (0, 162, 255)  # Bleu
WHITE = (255, 255, 255)
RED = (255, 75, 75)
GRAY = (150, 150, 150)

# Physique & Paramètres
GRAVITY = 0.4
JUMP_STRENGTH = -11
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 12

# Polices
font_large = pygame.font.SysFont("Arial", 40, bold=True)
font_medium = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

def generate_initial_platforms():
    platforms = [
        pygame.Rect(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 50, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    ]
    for i in range(7):
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        y = HEIGHT - 100 - (i * 75)
        platforms.append(pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    return platforms

def reset_game():
    return {
        "player": pygame.Rect(WIDTH // 2 - 15, HEIGHT - 120, 30, 30),
        "dy": JUMP_STRENGTH,
        "platforms": generate_initial_platforms(),
        "score": 0,
        "game_over": False
    }

game = reset_game()
high_score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game["game_over"]:
                game = reset_game()

    screen.fill(DARK_BG)

    if not game["game_over"]:
        # 1. Déplacements horizontaux + effet "wrap" (traverser les bords)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game["player"].x -= 6
        if keys[pygame.K_RIGHT]:
            game["player"].x += 6

        if game["player"].right < 0:
            game["player"].left = WIDTH
        elif game["player"].left > WIDTH:
            game["player"].right = 0

        # 2. Gravité et mouvement vertical
        game["dy"] += GRAVITY
        game["player"].y += int(game["dy"])

        # 3. Collision avec les plateformes (uniquement en descendant)
        if game["dy"] > 0:
            for plat in game["platforms"]:
                if game["player"].colliderect(plat) and game["player"].bottom <= plat.bottom + 10:
                    game["dy"] = JUMP_STRENGTH
                    break

        # 4. Caméra : Défilement vers le haut quand le joueur dépasse le milieu
        if game["player"].y < HEIGHT // 2:
            scroll = HEIGHT // 2 - game["player"].y
            game["player"].y = HEIGHT // 2
            game["score"] += int(scroll)

            # Faire descendre toutes les plateformes
            for plat in game["platforms"]:
                plat.y += scroll

        # Supprimer les plateformes sous l'écran et en récréer en haut
        new_platforms = []
        for plat in game["platforms"]:
            if plat.top < HEIGHT:
                new_platforms.append(plat)
            else:
                # Nouvelle plateforme en haut
                x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                y = random.randint(-30, 0)
                new_platforms.append(pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
        game["platforms"] = new_platforms

        # 5. Condition de défaite (chute sous l'écran)
        if game["player"].top > HEIGHT:
            game["game_over"] = True

        if game["score"] > high_score:
            high_score = game["score"]

        # Dessin des plateformes
        for plat in game["platforms"]:
            pygame.draw.rect(screen, PLATFORM_COLOR, plat, border_radius=5)

        # Dessin du joueur
        pygame.draw.ellipse(screen, PLAYER_COLOR, game["player"])

        # Affichage du score
        score_txt = font_medium.render(f"Score: {game['score']}", True, WHITE)
        screen.blit(score_txt, (20, 20))

    else:
        # Écran Game Over
        go_txt = font_large.render("GAME OVER", True, RED)
        final_score_txt = font_medium.render(f"Hauteur: {game['score']}", True, WHITE)
        best_score_txt = font_medium.render(f"Meilleur score: {high_score}", True, PLAYER_COLOR)
        replay_txt = font_small.render("Appuie sur ESPACE pour rejouer", True, GRAY)

        screen.blit(go_txt, (WIDTH // 2 - go_txt.get_width() // 2, 180))
        screen.blit(final_score_txt, (WIDTH // 2 - final_score_txt.get_width() // 2, 250))
        screen.blit(best_score_txt, (WIDTH // 2 - best_score_txt.get_width() // 2, 290))
        screen.blit(replay_txt, (WIDTH // 2 - replay_txt.get_width() // 2, 370))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()