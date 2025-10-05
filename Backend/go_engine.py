import json
from typing import Set, Tuple, List, Optional, Dict
from enum import Enum

class Stone(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

class GoEngine:
    def __init__(self, size: int = 9):
        self.size = size
        self.board = [[Stone.EMPTY for _ in range(size)] for _ in range(size)]
        self.current_player = Stone.BLACK
        self.captured = {Stone.BLACK: 0, Stone.WHITE: 0}
        self.ko_position = None
        self.move_history = []
        
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get valid neighboring positions"""
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                neighbors.append((nr, nc))
        return neighbors
    
    def get_group(self, row: int, col: int) -> Set[Tuple[int, int]]:
        """Get all stones in the same group (connected stones of same color)"""
        if self.board[row][col] == Stone.EMPTY:
            return set()
        
        color = self.board[row][col]
        group = set()
        stack = [(row, col)]
        
        while stack:
            r, c = stack.pop()
            if (r, c) in group:
                continue
            group.add((r, c))
            
            for nr, nc in self.get_neighbors(r, c):
                if self.board[nr][nc] == color and (nr, nc) not in group:
                    stack.append((nr, nc))
        
        return group
    
    def get_liberties(self, group: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """Get all liberties (empty adjacent positions) for a group"""
        liberties = set()
        for row, col in group:
            for nr, nc in self.get_neighbors(row, col):
                if self.board[nr][nc] == Stone.EMPTY:
                    liberties.add((nr, nc))
        return liberties
    
    def capture_group(self, group: Set[Tuple[int, int]]) -> int:
        """Remove captured group and return number of stones captured"""
        captured_count = len(group)
        for row, col in group:
            self.board[row][col] = Stone.EMPTY
        return captured_count
    
    def get_captured_groups(self, opponent_color: Stone) -> List[Set[Tuple[int, int]]]:
        """Find all groups of opponent that have no liberties"""
        captured_groups = []
        visited = set()
        
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in visited and self.board[row][col] == opponent_color:
                    group = self.get_group(row, col)
                    visited.update(group)
                    
                    if len(self.get_liberties(group)) == 0:
                        captured_groups.append(group)
        
        return captured_groups
    
    def would_be_suicide(self, row: int, col: int, color: Stone) -> bool:
        """Check if placing stone would be suicide (illegal unless it captures opponent)"""
        # Temporarily place stone
        self.board[row][col] = color
        
        # Check if this move captures any opponent groups
        opponent_color = Stone.WHITE if color == Stone.BLACK else Stone.BLACK
        captured_groups = self.get_captured_groups(opponent_color)
        
        # Check if our own group has liberties
        our_group = self.get_group(row, col)
        our_liberties = self.get_liberties(our_group)
        
        # Remove temporary stone
        self.board[row][col] = Stone.EMPTY
        
        # It's suicide if we have no liberties and capture no opponent stones
        return len(our_liberties) == 0 and len(captured_groups) == 0
    
    def would_violate_ko(self, row: int, col: int) -> bool:
        """Check if move would violate ko rule"""
        if self.ko_position is None:
            return False
        return (row, col) == self.ko_position
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if move is valid"""
        # Check bounds
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        
        # Check if position is empty
        if self.board[row][col] != Stone.EMPTY:
            return False
        
        # Check ko rule
        if self.would_violate_ko(row, col):
            return False
        
        # Check suicide rule
        if self.would_be_suicide(row, col, self.current_player):
            return False
        
        return True
    
    def make_move(self, row: int, col: int) -> bool:
        """Make a move and return True if successful"""
        if not self.is_valid_move(row, col):
            return False
        
        # Place stone
        self.board[row][col] = self.current_player
        
        # Capture opponent groups
        opponent_color = Stone.WHITE if self.current_player == Stone.BLACK else Stone.BLACK
        captured_groups = self.get_captured_groups(opponent_color)
        
        total_captured = 0
        ko_candidate = None
        
        for group in captured_groups:
            captured_count = self.capture_group(group)
            total_captured += captured_count
            
            # Check for ko: single stone capture that could be immediately recaptured
            if captured_count == 1 and len(self.get_liberties(self.get_group(row, col))) == 1:
                ko_candidate = list(group)[0]
        
        # Update captured count
        self.captured[opponent_color] += total_captured
        
        # Update ko position
        self.ko_position = ko_candidate if total_captured == 1 else None
        
        # Record move
        self.move_history.append({
            'row': row,
            'col': col,
            'player': self.current_player.value,
            'captured': total_captured
        })
        
        # Switch players
        self.current_player = Stone.WHITE if self.current_player == Stone.BLACK else Stone.BLACK
        
        return True
    
    def calculate_territory(self) -> Dict[str, int]:
        """Calculate territory using simple area scoring"""
        visited = set()
        territory = {Stone.BLACK: 0, Stone.WHITE: 0, 'neutral': 0}
        
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in visited and self.board[row][col] == Stone.EMPTY:
                    # Find connected empty region
                    region = set()
                    stack = [(row, col)]
                    
                    while stack:
                        r, c = stack.pop()
                        if (r, c) in region:
                            continue
                        region.add((r, c))
                        
                        for nr, nc in self.get_neighbors(r, c):
                            if self.board[nr][nc] == Stone.EMPTY and (nr, nc) not in region:
                                stack.append((nr, nc))
                    
                    # Determine territory owner
                    bordering_colors = set()
                    for r, c in region:
                        for nr, nc in self.get_neighbors(r, c):
                            if self.board[nr][nc] != Stone.EMPTY:
                                bordering_colors.add(self.board[nr][nc])
                    
                    # Assign territory
                    if len(bordering_colors) == 1:
                        owner = list(bordering_colors)[0]
                        territory[owner] += len(region)
                    else:
                        territory['neutral'] += len(region)
                    
                    visited.update(region)
        
        return territory
    
    def get_score(self) -> Dict[str, float]:
        """Calculate final score"""
        territory = self.calculate_territory()
        
        # Count stones on board
        stones = {Stone.BLACK: 0, Stone.WHITE: 0}
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != Stone.EMPTY:
                    stones[self.board[row][col]] += 1
        
        return {
            'black': stones[Stone.BLACK] + territory[Stone.BLACK],
            'white': stones[Stone.WHITE] + territory[Stone.WHITE] + 6.5,  # Komi
            'black_territory': territory[Stone.BLACK],
            'white_territory': territory[Stone.WHITE],
            'black_captured': self.captured[Stone.WHITE],
            'white_captured': self.captured[Stone.BLACK]
        }
    
    def serialize(self) -> str:
        """Serialize game state to JSON"""
        board_data = []
        for row in range(self.size):
            board_row = []
            for col in range(self.size):
                board_row.append(self.board[row][col].value)
            board_data.append(board_row)
        
        state = {
            'size': self.size,
            'board': board_data,
            'current_player': self.current_player.value,
            'captured': {
                'black': self.captured[Stone.WHITE],
                'white': self.captured[Stone.BLACK]
            },
            'ko_position': self.ko_position,
            'move_history': self.move_history
        }
        
        return json.dumps(state)
    
    @classmethod
    def deserialize(cls, data: str) -> 'GoEngine':
        """Deserialize game state from JSON"""
        state = json.loads(data)
        
        engine = cls(state['size'])
        
        # Restore board
        for row in range(state['size']):
            for col in range(state['size']):
                engine.board[row][col] = Stone(state['board'][row][col])
        
        # Restore game state
        engine.current_player = Stone(state['current_player'])
        engine.captured[Stone.WHITE] = state['captured']['black']
        engine.captured[Stone.BLACK] = state['captured']['white']
        engine.ko_position = tuple(state['ko_position']) if state['ko_position'] else None
        engine.move_history = state['move_history']
        
        return engine
    
    def get_board_state(self) -> List[List[int]]:
        """Get current board state as 2D list of integers"""
        return [[self.board[row][col].value for col in range(self.size)] for row in range(self.size)]
    
    def pass_turn(self):
        """Pass current turn to opponent"""
        self.move_history.append({
            'row': None,
            'col': None,
            'player': self.current_player.value,
            'captured': 0,
            'pass': True
        })
        self.current_player = Stone.WHITE if self.current_player == Stone.BLACK else Stone.BLACK
        self.ko_position = None