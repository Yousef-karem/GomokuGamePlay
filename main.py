import pygame
from game import GomokuGame

pygame.init()
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku - Main Menu")
font = pygame.font.Font(None, 40)

# Button config
button_color = (200, 200, 200)
hover_color = (170, 170, 170)
text_color = (0, 0, 0)
buttons = [
    {"label": "Human vs AI", "rect": pygame.Rect(100, 80, 200, 50), "mode": "human_vs_ai"},
    {"label": "AI vs AI", "rect": pygame.Rect(100, 160, 200, 50), "mode": "ai_vs_ai"},
]


def draw_menu():
    screen.fill((245, 245, 245))
    for button in buttons:
        mouse_pos = pygame.mouse.get_pos()
        color = hover_color if button["rect"].collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, color, button["rect"])
        text = font.render(button["label"], True, text_color)
        text_rect = text.get_rect(center=button["rect"].center)
        screen.blit(text, text_rect)
    pygame.display.flip()


running = True
while running:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button["rect"].collidepoint(event.pos):
                    game = GomokuGame(mode=button["mode"])
                    game.run()
                    running = False

pygame.quit()
