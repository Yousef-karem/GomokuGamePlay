import pygame
from aiPlayer import minimax_move, getAlphaBetaMove

DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]


class GomokuGame:
    def __init__(self, mode="human_vs_ai", board_size=17, ai_algorithm="alpha-beta", ai_depth=2):
        pygame.init()
        self.block_size = 30
        self.board_size = board_size
        self.n = board_size + 2
        self.start = 3
        self.end = board_size
        self.button_margin = 150
        self.width = (self.n * self.block_size) + self.button_margin
        self.height = self.n * self.block_size

        self.original_screen_size = pygame.display.get_surface().get_size()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Gomoku")

        self.mode = mode
        self.ai_algorithm = ai_algorithm
        self.ai_depth = ai_depth

        self.grid = [[' ' for _ in range(self.n + 1)] for _ in range(self.n + 1)]
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.wood_background = pygame.image.load("wood_background.jpg")
        self.wood_background = pygame.transform.scale(self.wood_background, (self.width, self.height))

        self.running = True
        self.turn = True  # True = White (Human or AI1), False = Black (AI or AI2)
        self.won = False
        self.return_to_menu = False

        button_x = self.n * self.block_size + 20
        button_width = 110
        button_height = 40
        button_spacing = 20
        self.common_buttons = [
            {"label": "New Game", "rect": pygame.Rect(button_x, 310, button_width, button_height),
             "action": "new_game"},
            {"label": "Menu",
             "rect": pygame.Rect(button_x, 310 + button_height + button_spacing, button_width, button_height),
             "action": "back_to_menu"}
        ]

        # AI vs AI
        self.ai_control_buttons = [
            {"label": "Start", "rect": pygame.Rect(button_x, 160, button_width, button_height), "action": "start"},
        ]
        self.ai_auto_play = False

    def draw_grid(self):

        start_pos = 2 * self.block_size
        end_pos = (self.n - 2) * self.block_size

        for i in range(start_pos, end_pos + 1, self.block_size):
            pygame.draw.line(self.screen, (0, 0, 0), (i, start_pos), (i, end_pos))
            pygame.draw.line(self.screen, (0, 0, 0), (start_pos, i), (end_pos, i))

        if self.board_size >= 13:
            star_points = []
            if self.board_size == 13:
                positions = [3, 6, 9]
            else:
                positions = [3, 7, 11]
            for x in positions:
                for y in positions:
                    star_points.append((x + 2, y + 2))

            for x, y in star_points:
                pygame.draw.circle(self.screen, (0, 0, 0), (x * self.block_size, y * self.block_size), 4)

    def check_five(self, x, y):
        c = self.grid[x][y]
        if c == ' ':
            return False

        dx = [1, -1, 0, 0, 1, 1, -1, -1]
        dy = [0, 0, 1, -1, 1, -1, 1, -1]

        for i in range(8):
            count = 1
            nx, ny = x + dx[i], y + dy[i]

            while self.start <= nx < self.end and self.start <= ny < self.end and self.grid[nx][ny] == c:
                count += 1
                if count == 5:
                    return True
                nx += dx[i]
                ny += dy[i]

        return False

    def evaluate(self, c):
        for i in range(self.start, self.end):
            for j in range(self.start, self.end):
                if self.grid[i][j] != ' ' and self.check_five(i, j):
                    return 1 if self.grid[i][j] == c else -1
        return 0

    def draw_board(self):
        if self.wood_background:
            self.screen.blit(self.wood_background, (0, 0))
        else:
            self.screen.fill((210, 180, 140))
        self.draw_grid()

        for i in range(self.start, self.end):
            for j in range(self.start, self.end):
                if self.grid[i][j] != ' ':
                    if self.grid[i][j] == 'W':

                        pygame.draw.circle(self.screen, (100, 100, 100), (i * self.block_size, j * self.block_size),
                                           (self.block_size // 2) - 2)
                        pygame.draw.circle(self.screen, (255, 255, 255), (i * self.block_size, j * self.block_size),
                                           (self.block_size // 2) - 4)
                    else:  # 'B'

                        pygame.draw.circle(self.screen, (100, 100, 100), (i * self.block_size, j * self.block_size),
                                           (self.block_size // 2) - 2)
                        pygame.draw.circle(self.screen, (0, 0, 0), (i * self.block_size, j * self.block_size),
                                           (self.block_size // 2) - 4)

        turn_text = "White's Turn" if self.turn else "Black's Turn"
        if self.won:
            winner = self.evaluate('W' if not self.turn else 'B')
            if winner == 1:
                name = "White" if not self.turn else "Black"
                turn_text = f"{name} has won!"
            elif self.is_board_full():
                turn_text = "It's a Draw!"

        text_surface = self.font.render(turn_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10)
        self.screen.blit(text_surface, text_rect)

        if self.mode == "ai_vs_ai":
            self.draw_ai_controls()

        self.draw_common_controls()

    def draw_common_controls(self):
        button_color = (210, 180, 140)
        hover_color = (188, 143, 143)
        text_color = (0, 0, 0)

        for button in self.common_buttons:
            mouse_pos = pygame.mouse.get_pos()
            color = hover_color if button["rect"].collidepoint(mouse_pos) else button_color

            pygame.draw.rect(self.screen, color, button["rect"], border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), button["rect"], 2, border_radius=5)  # Black border

            text = self.small_font.render(button["label"], True, text_color)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

    def draw_ai_controls(self):
        button_color = (210, 180, 140)
        hover_color = (188, 143, 143)
        text_color = (0, 0, 0)

        for button in self.ai_control_buttons:
            mouse_pos = pygame.mouse.get_pos()
            color = hover_color if button["rect"].collidepoint(mouse_pos) else button_color

            if button["action"] == "start" and self.ai_auto_play:
                color = (144, 238, 144)

            pygame.draw.rect(self.screen, color, button["rect"], border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), button["rect"], 2, border_radius=5)  # Black border

            text = self.small_font.render(button["label"], True, text_color)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

    def ai_move(self):
        if self.mode == "ai_vs_ai":
            if self.turn:
                i, j = getAlphaBetaMove(self.grid, is_white=True)
            else:
                i, j = minimax_move(self.grid, is_white=False)
        else:

            algo_func = getAlphaBetaMove if self.ai_algorithm == "alpha-beta" else minimax_move
            i, j = algo_func(self.grid, is_white=self.turn)

        if i is not None and j is not None and self.start <= i < self.end and self.start <= j < self.end and self.grid[i][j] == ' ':
            self.grid[i][j] = 'W' if self.turn else 'B'

            stone_color = (255, 255, 255) if self.turn else (0, 0, 0)
            pygame.draw.circle(self.screen, (100, 100, 100), (i * self.block_size, j * self.block_size),
                               (self.block_size // 2) - 2)
            pygame.draw.circle(self.screen, stone_color, (i * self.block_size, j * self.block_size),
                               (self.block_size // 2) - 4)

            if self.check_five(i, j):
                self.won = True
            elif self.is_board_full():
                self.won = True

            self.turn = not self.turn

    def is_board_full(self):
        for i in range(self.start, self.end):
            for j in range(self.start, self.end):
                if self.grid[i][j] == ' ':
                    return False
        return True

    def handle_ai_control_click(self, pos):
        for button in self.ai_control_buttons:
            if button["rect"].collidepoint(pos):
                if button["action"] == "start":
                    self.ai_auto_play = True
                return True
        return False

    def handle_common_control_click(self, pos):
        for button in self.common_buttons:
            if button["rect"].collidepoint(pos):
                if button["action"] == "new_game":

                    self.grid = [[' ' for _ in range(self.n + 1)] for _ in range(self.n + 1)]
                    self.turn = True
                    self.won = False
                    self.ai_auto_play = False
                elif button["action"] == "back_to_menu":
                    self.return_to_menu = True
                    self.running = False
                return True
        return False

    def run(self):
        clock = pygame.time.Clock()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.handle_common_control_click(event.pos):
                        pass
                    elif self.mode == "ai_vs_ai" and self.handle_ai_control_click(event.pos):
                        pass
                    elif self.mode == "human_vs_ai" and not self.won and self.turn:
                        x, y = event.pos
                        i, j = round(x / self.block_size), round(y / self.block_size)

                        if (self.start <= i < self.end and self.start <= j < self.end and
                                self.grid[i][j] == ' '):

                            self.grid[i][j] = 'W'  # Human plays as White

                            pygame.draw.circle(self.screen, (100, 100, 100), (i * self.block_size, j * self.block_size),
                                               (self.block_size // 2) - 2)
                            pygame.draw.circle(self.screen, (255, 255, 255), (i * self.block_size, j * self.block_size),
                                               (self.block_size // 2) - 4)

                            if self.check_five(i, j):
                                self.won = True
                            elif self.is_board_full():
                                self.won = True

                            self.turn = not self.turn
                            pygame.display.flip()

            if not self.won:
                if self.mode == "ai_vs_ai" and self.ai_auto_play:

                    self.ai_move()
                elif self.mode == "human_vs_ai" and not self.turn:

                    self.ai_move()

            self.draw_board()

            pygame.display.flip()
            clock.tick(30)

        # Restore original screen size when returning to menu
        if self.return_to_menu:
            pygame.display.set_mode(self.original_screen_size)

        return self.return_to_menu
