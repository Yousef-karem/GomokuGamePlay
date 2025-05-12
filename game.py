import pygame

class GomokuGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 660, 660
        self.blockSize = 60
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.n = (self.height // self.blockSize) - 2
        self.grid = [[' ' for _ in range(self.n + 1)] for _ in range(self.n + 1)]
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.turn = True  # True for white, False for black
        self.won = False
        self.wood_background = pygame.image.load("wood_background.jpg")
        self.wood_background = pygame.transform.scale(self.wood_background, (self.width, self.height))

    def draw_grid(self):
        for i in range(self.blockSize, self.width - self.blockSize + 1, self.blockSize):
            pygame.draw.line(self.screen, (0, 0, 0), (i, self.blockSize), (i, self.width - self.blockSize))
            pygame.draw.line(self.screen, (0, 0, 0), (self.blockSize, i), (self.width - self.blockSize, i))

    def check_five(self, x, y):
        c = self.grid[x][y]
        dx = [1, -1, 0, 0, 1, 1, -1, -1]
        dy = [0, 0, 1, -1, 1, -1, 1, -1]

        for i in range(8):
            count = 1
            nx, ny = x + dx[i], y + dy[i]
            while 1 <= nx <= self.n and 1 <= ny <= self.n and self.grid[nx][ny] == c:
                count += 1
                if count == 5:
                    return True
                nx += dx[i]
                ny += dy[i]
        return False

    def evaluate(self, c):
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if self.grid[i][j] != ' ' and self.check_five(i, j):
                    return 1 if self.grid[i][j] == c else -1
        return 0

    def handle_click(self, x, y):
        X, Y = x % self.blockSize, y % self.blockSize
        if (X <= 10 or X >= self.blockSize - 10) and (Y <= 10 or Y >= self.blockSize - 10):
            i, j = round(x / self.blockSize), round(y / self.blockSize)
            if i <= 1 or i > self.n or j <= 1 or j > self.n or self.grid[i][j] != ' ':
                return
            color = (255, 255, 255) if self.turn else (0, 0, 0)
            c = 'W' if self.turn else 'B'
            self.grid[i][j] = c

            pygame.draw.circle(self.screen, (100, 100, 100), (i * self.blockSize, j * self.blockSize), (self.blockSize // 2) - 2)
            pygame.draw.circle(self.screen, color, (i * self.blockSize, j * self.blockSize), (self.blockSize // 2) - 4)

            if self.evaluate(c) == 1:
                winner = "White" if self.turn else "Black"
                text_surface = self.font.render(winner + " has won!", True, (0, 0, 0))
                self.screen.blit(text_surface, ((self.width // 2.5), (self.blockSize // 2)))
                self.won = True

            self.turn = not self.turn

    def run(self):
        self.screen.blit(self.wood_background, (0, 0))
        self.draw_grid()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.won:
                    x, y = pygame.mouse.get_pos()
                    self.handle_click(x, y)

            pygame.display.flip()

        pygame.quit()
