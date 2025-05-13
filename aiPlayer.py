import copy
import math

DEPTH = 2
DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]
N = 17
HUMAN = 'W'
AI = 'B'


def get_available_moves(grid):
    moves = []
    for i in range(2, N):
        for j in range(2, N):
            if grid[i][j] == ' ':
                for dx, dy in DIRECTIONS:
                    for d in [-1, 1]:
                        ni, nj = i + dx * d, j + dy * d
                        if 2 <= ni < N and 2 <= nj < N and grid[ni][nj] != ' ':
                            moves.append((i, j))
                            break
                    else:
                        continue
                    break
    if not moves:
        for i in range(2, N):
            for j in range(2, N):
                if grid[i][j] == ' ':
                    moves.append((i, j))
    return moves


def evaluate_line(line, player):
    score = 0
    opponent = 'B' if player == 'W' else 'W'
    if line.count(player) == 5:
        score += 100000
    elif line.count(player) == 4 and line.count(' ') == 1:
        score += 9000
    elif line.count(player) == 3 and line.count(' ') == 2:
        score += 1000
    elif line.count(player) == 2 and line.count(' ') == 3:
        score += 100
    elif line.count(opponent) == 4 and line.count(' ') == 1:
        score -= 10000
    return score


def evaluate_board(grid, player):
    total_score = 0

    # Horizontal, vertical, and diagonal
    for i in range(2, N):
        for j in range(2, N):
            for dx, dy in DIRECTIONS:
                line = []
                for k in range(5):
                    ni, nj = i + dx * k, j + dy * k
                    if 2 <= ni <= N and 2 <= nj <= N:
                        line.append(grid[ni][nj])
                if len(line) == 5:
                    total_score += evaluate_line(line, player)
    return total_score


def minimax(grid, depth, is_maximizing, player):
    opponent = 'B' if player == 'W' else 'W'
    best_score = float('-inf') if is_maximizing else float('inf')
    best_move = None

    for move in get_available_moves(grid):
        i, j = move
        new_grid = copy.deepcopy(grid)
        new_grid[i][j] = player if is_maximizing else opponent

        if depth == 1:
            score = evaluate_board(new_grid, player)
        else:
            score, _ = minimax(new_grid, depth - 1, not is_maximizing, player)

        if is_maximizing:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    return best_score, best_move


def minimax_move(grid, is_white=True):
    player = 'W' if is_white else 'B'
    _, move = minimax(grid, DEPTH, True, player)
    if move is None:
        for m in get_available_moves(grid):
            move = m
            break
    return move


def alphaBetaPruning(grid, depth, alpha, beta, isMaximizing, player):
    if depth == 0:
        return evaluate_board(grid, player), None

    best_move = None
    moves = get_available_moves(grid)

    if not moves:
        return 0, None

    opponent = 'W' if player == 'B' else 'B'

    if isMaximizing:
        finalResult = -math.inf

        for move in moves:
            i, j = move
            new_grid = copy.deepcopy(grid)  # Create a copy to avoid modifying the original
            new_grid[i][j] = player

            result, _ = alphaBetaPruning(new_grid, depth - 1, alpha, beta, False, player)

            if result > finalResult:
                finalResult = result
                best_move = move

            alpha = max(alpha, finalResult)
            if beta <= alpha:
                break

    else:
        finalResult = math.inf

        for move in moves:
            i, j = move
            new_grid = copy.deepcopy(grid)  # Create a copy to avoid modifying the original
            new_grid[i][j] = opponent

            result, _ = alphaBetaPruning(new_grid, depth - 1, alpha, beta, True, player)

            if result < finalResult:
                finalResult = result
                best_move = move

            beta = min(beta, finalResult)
            if beta <= alpha:
                break

    return finalResult, best_move


def getAlphaBetaMove(grid, is_white):
    player = 'W' if is_white else 'B'
    _, move = alphaBetaPruning(grid, DEPTH, -math.inf, math.inf, True, player)
    if move is None:
        moves = get_available_moves(grid)
        if moves:
            move = moves[0]
    return move
