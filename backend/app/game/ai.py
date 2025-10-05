import random

class GoAI:
    def __init__(self, board_size=9):
        self.board_size = board_size

    def make_move(self, board):
        """ AI decides where to play next move Returns: (row, col) position or None to pass """
        print("AI is thinking...")

        # Find all empty spots
        empty_spots = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] is None:
                    empty_spots.append((row, col))

        if not empty_spots:
            print("AI passes - no moves available")
            return None

        # Try to capture human's stones
        print("AI checking for captures...")
        for row, col in empty_spots:
            if self.can_capture_here(board, row, col):
                print(f"AI captures at ({row}, {col})!")
                return (row, col)

        # Try to save own stones
        print("AI checking if own stones need saving...")
        for row, col in empty_spots:
            if self.can_save_stones_here(board, row, col):
                print(f"AI saves stones at ({row}, {col})")
                return (row, col)

        # Play near existing stones
        print("AI looking for good spots near other stones...")
        good_spots = []
        for row, col in empty_spots:
            if self.is_near_stones(board, row, col):
                good_spots.append((row, col))

        # Choose move
        if good_spots:
            chosen = random.choice(good_spots)
            print(f"AI plays near stones at {chosen}")
        else:
            chosen = random.choice(empty_spots)
            print(f"AI plays randomly at {chosen}")
        return chosen

    def can_capture_here(self, board, row, col):
        """Check if playing here captures black stones"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < self.board_size and 0 <= nc < self.board_size and
                    board[nr][nc] == 'black'):
                if self.count_liberties(board, nr, nc) == 1:
                    return True
        return False

    def can_save_stones_here(self, board, row, col):
        """Check if playing here saves white stones"""
        board[row][col] = 'white'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        can_save = False
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < self.board_size and 0 <= nc < self.board_size and
                    board[nr][nc] == 'white'):
                if self.count_liberties(board, nr, nc) > 1:
                    can_save = True
                    break

        board[row][col] = None
        return can_save

    def is_near_stones(self, board, row, col):
        """Check if spot is near other stones"""
        for r in range(max(0, row - 2), min(self.board_size, row + 3)):
            for c in range(max(0, col - 2), min(self.board_size, col + 3)):
                if r == row and c == col:
                    continue
                if board[r][c] is not None:
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