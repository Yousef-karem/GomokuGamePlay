import pygame
import sys
from game import GomokuGame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku Game - Main Menu")
font_large = pygame.font.Font(None, 60)
font = pygame.font.Font(None, 40)

#  settings
board_size = 15  # Default board size
ai_algorithm = "alpha-beta"  # Default AI algorithm
ai_depth = 2  # Default AI depth
current_screen = "main_menu"
try:
    background = pygame.image.load("wood_background.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except pygame.error:
    background = None

# Button config
button_color = (210, 180, 140)
hover_color = (188, 143, 143)
text_color = (0, 0, 0)

main_menu_buttons = [
    {"label": "Human vs AI", "rect": pygame.Rect(WIDTH // 2 - 150, 250, 300, 60), "action": "human_vs_ai"},
    {"label": "AI vs AI", "rect": pygame.Rect(WIDTH // 2 - 150, 330, 300, 60), "action": "ai_vs_ai"},
    {"label": "Settings", "rect": pygame.Rect(WIDTH // 2 - 150, 410, 300, 60), "action": "settings"},
    {"label": "Exit", "rect": pygame.Rect(WIDTH // 2 - 150, 490, 300, 60), "action": "exit"}
]

 #Settings  buttons

board_size_buttons = [
    {"label": "13", "rect": pygame.Rect(WIDTH // 4 - 25, 250, 50, 50), "value": 15},
    {"label": "15", "rect": pygame.Rect(3 * WIDTH // 4 - 25, 250, 50, 50), "value": 17}
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
        screen.fill((210, 180, 140))  # Tan color as fallback


def draw_button(button):
    mouse_pos = pygame.mouse.get_pos()
    color = hover_color if button["rect"].collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, color, button["rect"], border_radius=5)
    pygame.draw.rect(screen, (0, 0, 0), button["rect"], 2, border_radius=5)  # Black border

    text_render = font.render(button["label"], True, text_color)
    text_rect = text_render.get_rect(center=button["rect"].center)
    screen.blit(text_render, text_rect)


def draw_main_menu():
    draw_background()

    # Draw title
    title = font_large.render("Gomoku Game with AI", True, (0, 0, 0))
    title_rect = title.get_rect(center=(WIDTH // 2, 120))
    screen.blit(title, title_rect)

    # Draw buttons
    for button in main_menu_buttons:
        draw_button(button)

    pygame.display.flip()


def draw_settings():
    draw_background()

    # Draw title
    title = font_large.render("Settings", True, (0, 0, 0))
    title_rect = title.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title, title_rect)

    # Draw board size section
    board_size_text = font.render("Board Size:", True, (0, 0, 0))
    screen.blit(board_size_text, (WIDTH // 2 - 100, 180))

    for button in board_size_buttons:
        # Highlight selected size
        selected = button["value"] == board_size
        highlight_color = (144, 238, 144) if selected else (
            hover_color if button["rect"].collidepoint(pygame.mouse.get_pos()) else button_color)
        pygame.draw.rect(screen, highlight_color, button["rect"], border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), button["rect"], 2, border_radius=5)  # Black border

        text_render = font.render(button["label"], True, text_color)
        text_rect = text_render.get_rect(center=button["rect"].center)
        screen.blit(text_render, text_rect)

    # Draw AI algorithm section
    algorithm_text = font.render("AI Algorithm:", True, (0, 0, 0))
    screen.blit(algorithm_text, (WIDTH // 2 - 100, 300))

    for button in algorithm_buttons:
        # Highlight selected algorithm
        selected = button["value"] == ai_algorithm
        highlight_color = (144, 238, 144) if selected else (
            hover_color if button["rect"].collidepoint(pygame.mouse.get_pos()) else button_color)
        pygame.draw.rect(screen, highlight_color, button["rect"], border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), button["rect"], 2, border_radius=5)  # Black border

        text_render = font.render(button["label"], True, text_color)
        text_rect = text_render.get_rect(center=button["rect"].center)
        screen.blit(text_render, text_rect)

    # Draw AI depth section
    depth_text = font.render("AI Depth:", True, (0, 0, 0))
    screen.blit(depth_text, (WIDTH // 2 - 100, 400))

    for button in depth_buttons:
        # Highlight selected depth
        selected = button["value"] == ai_depth
        highlight_color = (144, 238, 144) if selected else (
            hover_color if button["rect"].collidepoint(pygame.mouse.get_pos()) else button_color)
        pygame.draw.rect(screen, highlight_color, button["rect"], border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), button["rect"], 2, border_radius=5)  # Black border

        text_render = font.render(button["label"], True, text_color)
        text_rect = text_render.get_rect(center=button["rect"].center)
        screen.blit(text_render, text_rect)

    # Draw back button
    draw_button(back_button)

    pygame.display.flip()


def handle_main_menu_events(event):
    global current_screen, screen

    if event.type == pygame.MOUSEBUTTONDOWN:
        for button in main_menu_buttons:
            if button["rect"].collidepoint(event.pos):
                if button["action"] == "exit":
                    return False
                elif button["action"] == "settings":
                    current_screen = "settings"
                elif button["action"] in ["human_vs_ai", "ai_vs_ai"]:
                    game = GomokuGame(
                        mode=button["action"],
                        board_size=board_size,
                        ai_algorithm=ai_algorithm,
                        ai_depth=ai_depth
                    )
                    return_to_menu = game.run()
                    if return_to_menu:
                        # Ensure we reset the screen size properly
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        current_screen = "main_menu"
                        return True  # Continue the main loop to show the menu
                    else:
                        return False  # Exit the main loop (game was closed)
    return True


def handle_settings_events(event):
    global current_screen, board_size, ai_algorithm, ai_depth

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Handle board size selection
        for button in board_size_buttons:
            if button["rect"].collidepoint(event.pos):
                board_size = button["value"]
                return True

        # Handle algorithm selection
        for button in algorithm_buttons:
            if button["rect"].collidepoint(event.pos):
                ai_algorithm = button["value"]
                return True

        # Handle depth selection
        for button in depth_buttons:
            if button["rect"].collidepoint(event.pos):
                ai_depth = button["value"]
                return True

        # Handle back button
        if back_button["rect"].collidepoint(event.pos):
            current_screen = "main_menu"
            return True
    return True


# Main game loop
running = True
while running:
    if current_screen == "main_menu":
        draw_main_menu()
    elif current_screen == "settings":
        draw_settings()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "main_menu":
            running = handle_main_menu_events(event)
        elif current_screen == "settings":
            handle_settings_events(event)

    pygame.display.update()

pygame.quit()
sys.exit()