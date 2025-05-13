import pygame
from aiPlayer import minimax_move, getAlphaBetaMove

N = 17
DEPTH = 2
DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]


class GomokuGame:
    def __init__(self, mode="human_vs_ai"):
        pygame.init()
        self.width, self.height = 540, 540
        self.block_size = 30
        self.n = (self.height // self.block_size) - 1
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Gomoku")

        self.mode = mode
        self.grid = [[' ' for _ in range(self.n + 1)] for _ in range(self.n + 1)]
        self.font = pygame.font.Font(None, 36)

        self.wood_background = pygame.image.load("wood_background.jpg")
        self.wood_background = pygame.transform.scale(self.wood_background, (self.width, self.height))

        self.running = True
        self.turn = True  # True = White (Human or AI1), False = Black (AI or AI2)
        self.won = False

    def draw_grid(self):
        for i in range(self.block_size, self.width - self.block_size + 1, self.block_size):
            pygame.draw.line(self.screen, (0, 0, 0), (i, self.block_size), (i, self.width - self.block_size))
            pygame.draw.line(self.screen, (0, 0, 0), (self.block_size, i), (self.width - self.block_size, i))

    def check_five(self, x, y):
        c = self.grid[x][y]
        dx = [1, -1, 0, 0, 1, 1, -1, -1]
        dy = [0, 0, 1, -1, 1, -1, 1, -1]
        for i in range(0, 8):
            count = 1
            nx, ny = x + dx[i], y + dy[i]
            while 2 <= nx <= self.n and 2 <= ny <= self.n and self.grid[nx][ny] == c:
                count += 1
                if count == 5:
                    return True
                nx += dx[i]
                ny += dy[i]
        return False

    def evaluate(self, c):
        for i in range(2, self.n + 1):
            for j in range(2, self.n + 1):
                if self.grid[i][j] != ' ' and self.check_five(i, j):
                    return 1 if self.grid[i][j] == c else -1
        return 0

    def draw_board(self):
        self.screen.blit(self.wood_background, (0, 0))
        self.draw_grid()
        for i in range(2, self.n + 1):
            for j in range(2, self.n + 1):
                if self.grid[i][j] != ' ':
                    color = (255, 255, 255) if self.grid[i][j] == 'W' else (0, 0, 0)

    def ai_move(self):
        if self.turn:  # White
            i, j = getAlphaBetaMove(self.grid, is_white=True)
            self.grid[i][j] = 'W'
            pygame.draw.circle(self.screen, (100, 100, 100), (i * self.block_size, j * self.block_size),
                               (self.block_size // 2) - 2)
            pygame.draw.circle(self.screen, (255, 255, 255), (i * self.block_size, j * self.block_size),
                               (self.block_size // 2) - 4)
        else:
            if self.mode == "ai_vs_ai":
                i, j = minimax_move(self.grid, is_white=False)
            else:
                i, j = getAlphaBetaMove(self.grid, is_white=False)
            self.grid[i][j] = 'B'
            pygame.draw.circle(self.screen, (100, 100, 100), (i * self.block_size, j * self.block_size),
                               (self.block_size // 2) - 2)
            pygame.draw.circle(self.screen, (0, 0, 0), (i * self.block_size, j * self.block_size),
                               (self.block_size // 2) - 4)

        self.turn = not self.turn

    def full(self):
        for i in range(2, N):
            for j in range(2, N):
                if self.grid[i][j] == ' ':
                    return False
        return True

    def run(self):
        clock = pygame.time.Clock()
        self.draw_board()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.mode == "human_vs_ai" and event.type == pygame.MOUSEBUTTONDOWN and not self.won and self.turn:
                    x, y = pygame.mouse.get_pos()
                    X, Y = x % self.block_size, y % self.block_size
                    if (X <= 10 or X >= self.block_size - 10) and (Y <= 10 or Y >= self.block_size - 10):
                        i, j = round(x / self.block_size), round(y / self.block_size)
                        if 1 < i < self.n and 1 < j < self.n and self.grid[i][j] == ' ':
                            self.grid[i][j] = 'W'
                            pygame.draw.circle(self.screen, (100, 100, 100), (i * self.block_size, j * self.block_size),
                                               (self.block_size // 2) - 2)
                            pygame.draw.circle(self.screen, (255, 255, 255), (i * self.block_size, j * self.block_size),
                                               (self.block_size // 2) - 4)
                            if self.full() and not self.won:
                                text_surface = self.font.render("It's a Draw!", True, (255, 255, 255))
                                self.screen.blit(text_surface, ((self.width // 2.5), (self.block_size // 2)))
                                self.won = True
                            self.turn = not self.turn

                if not self.won and (self.mode == "ai_vs_ai" or (self.mode == "human_vs_ai" and not self.turn)):
                    self.ai_move()
                    if self.full() and not self.won:
                        text_surface = self.font.render("It's a Draw!", True, (255, 255, 255))
                        self.screen.blit(text_surface, ((self.width // 2.5), (self.block_size // 2)))
                        self.won = True

                winner = self.evaluate('W' if not self.turn else 'B')
                if winner == 1:
                    name = "White" if not self.turn else "Black"
                    text_surface = self.font.render(f"{name} has won!", True, (0, 0, 0))
                    self.screen.blit(text_surface, ((self.width // 2.5), (self.block_size // 2)))
                    self.won = True

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
