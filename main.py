import pygame
import sys

from game import GomokuGame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku Game - Main Menu")
font_large = pygame.font.Font(None, 60)
font = pygame.font.Font(None, 40)

background = pygame.image.load("wood_background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Button config
button_color = (210, 180, 140)
hover_color = (188, 143, 143)
text_color = (0, 0, 0)
current_screen = "main_menu"

main_menu_buttons = [
    {"label": "Human vs AI", "rect": pygame.Rect(WIDTH // 2 - 150, 250, 300, 60), "action": "human_vs_ai"},
    {"label": "AI vs AI", "rect": pygame.Rect(WIDTH // 2 - 150, 330, 300, 60), "action": "ai_vs_ai"},
    {"label": "Exit", "rect": pygame.Rect(WIDTH // 2 - 150, 415, 300, 60), "action": "exit"}
]

# AI  buttons
algorithm_buttons = [
    {"label": "Minimax", "rect": pygame.Rect(WIDTH // 3 - 75, 350, 150, 50), "value": "minimax"},
    {"label": "Alpha-Beta", "rect": pygame.Rect(2 * WIDTH // 3 - 75, 350, 150, 50), "value": "alpha-beta"}
]

# depth buttons
depth_buttons = [
    {"label": "1", "rect": pygame.Rect(WIDTH // 5 - 25, 450, 50, 50), "value": 1},
    {"label": "2", "rect": pygame.Rect(2 * WIDTH // 5 - 25, 450, 50, 50), "value": 2},
    {"label": "3", "rect": pygame.Rect(3 * WIDTH // 5 - 25, 450, 50, 50), "value": 3},
    {"label": "4", "rect": pygame.Rect(4 * WIDTH // 5 - 25, 450, 50, 50), "value": 4}
]
back_button = {"label": "Back to Menu", "rect": pygame.Rect(WIDTH // 2 - 150, 520, 300, 60), "action": "main_menu"}


def draw_background():
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((210, 180, 140))


def draw_button(button):
    mouse_pos = pygame.mouse.get_pos()
    color = hover_color if button["rect"].collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, color, button["rect"], border_radius=5)
    pygame.draw.rect(screen, (0, 0, 0), button["rect"], 2, border_radius=5)

    text_render = font.render(button["label"], True, text_color)
    text_rect = text_render.get_rect(center=button["rect"].center)
    screen.blit(text_render, text_rect)


def draw_main_menu():
    draw_background()

    title = font_large.render("Gomoku Game with AI", True, (0, 0, 0))
    title_rect = title.get_rect(center=(WIDTH // 2, 120))
    screen.blit(title, title_rect)

    for button in main_menu_buttons:
        draw_button(button)

    pygame.display.flip()


def handle_main_menu_events(event):
    global current_screen, screen

    if event.type == pygame.MOUSEBUTTONDOWN:
        for button in main_menu_buttons:
            if button["rect"].collidepoint(event.pos):
                if button["action"] == "exit":
                    return False
                game = GomokuGame(
                    mode=button["action"],
                    board_size=17,
                    ai_algorithm="alpha-beta",
                    ai_depth=2
                )
                return_to_menu = game.run()
                if return_to_menu:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    current_screen = "main_menu"
                    return True
                else:
                    return False
    return True


running = True
while running:
    if current_screen == "main_menu":
        draw_main_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "main_menu":
            running = handle_main_menu_events(event)

    pygame.display.update()

pygame.quit()
sys.exit()
