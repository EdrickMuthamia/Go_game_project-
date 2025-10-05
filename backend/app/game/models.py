from app import db
from datetime import datetime
import json


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    board_state = db.Column(db.Text, nullable=False)
    current_player = db.Column(db.String(10), nullable=False, default='black')
    game_status = db.Column(db.String(20), nullable=False, default='active')
    winner = db.Column(db.String(10), nullable=True)  # 'black', 'white', or 'draw'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    board_size = db.Column(db.Integer, nullable=False, default=9)
    captured_black = db.Column(db.Integer, default=0)
    captured_white = db.Column(db.Integer, default=0)
    
    # Relationship
    player = db.relationship('User', backref='games')

    def __init__(self, player_id, board_size=9):
        self.player_id = player_id
        self.board_size = board_size
        self.board_state = self.create_empty_board()
        self.current_player = 'black'
        self.game_status = 'active'

    def create_empty_board(self):
        """Create an empty board represented as a 2D array"""
        board = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                row.append(None)
            board.append(row)
        return json.dumps(board)

    def get_board(self):
        """Get board as Python object"""
        return json.loads(self.board_state)

    def set_board(self, board):
        """Set board from Python object"""
        self.board_state = json.dumps(board)

    def to_dict(self):
        return {
            'id': self.id,
            'player_id': self.player_id,
            'human_player': self.player.username,
            'ai_player': 'AI',
            'human_color': 'black',  # Human always plays black
            'ai_color': 'white',  # AI always plays white
            'board': self.get_board(),
            'current_player': self.current_player,
            'game_status': self.game_status,
            'winner': self.winner,
            'created_at': self.created_at.isoformat(),
            'board_size': self.board_size,
            'captured_by_human': self.captured_white,  # Stones human captured from AI
            'captured_by_ai': self.captured_black  # Stones AI captured from human
        }