import random

class GoAI:
    def __init__(self, board_size=9):
        self.board_size = board_size

    def make_move(self, board):
        empty_spots = [(r, c) for r in range(self.board_size) 
                      for c in range(self.board_size) if board[r][c] is None]
        
        if not empty_spots:
            return None

        # Try captures first
        for row, col in empty_spots:
            if self.can_capture_here(board, row, col):
                return (row, col)

        # Try defense
        for row, col in empty_spots:
            if self.can_save_stones_here(board, row, col):
                return (row, col)

        # Play near stones or random
        good_spots = [pos for pos in empty_spots if self.is_near_stones(board, *pos)]
        return random.choice(good_spots if good_spots else empty_spots)

    def can_capture_here(self, board, row, col):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < self.board_size and 0 <= nc < self.board_size and
                    board[nr][nc] == 'black' and self.count_liberties(board, nr, nc) == 1):
                return True
        return False

    def can_save_stones_here(self, board, row, col):
        board[row][col] = 'white'
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < self.board_size and 0 <= nc < self.board_size and
                    board[nr][nc] == 'white' and self.count_liberties(board, nr, nc) > 1):
                board[row][col] = None
                return True
        board[row][col] = None
        return False

    def is_near_stones(self, board, row, col):
        for r in range(max(0, row - 2), min(self.board_size, row + 3)):
            for c in range(max(0, col - 2), min(self.board_size, col + 3)):
                if (r != row or c != col) and board[r][c] is not None:
                    return True
        return False

    def count_liberties(self, board, row, col):
        """Count empty spots next to stone group"""
        if board[row][col] is None:
            return 0

        stone_color = board[row][col]
        visited = set()
        liberties = set()
        to_check = [(row, col)]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while to_check:
            cr, cc = to_check.pop()
            if (cr, cc) in visited:
                continue
            visited.add((cr, cc))

            for dr, dc in directions:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                    if board[nr][nc] is None:
                        liberties.add((nr, nc))
                    elif board[nr][nc] == stone_color and (nr, nc) not in visited:
                        to_check.append((nr, nc))

        return len(liberties)
