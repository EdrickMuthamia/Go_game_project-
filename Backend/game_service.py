from sqlalchemy.orm import Session
from models import Game, User
from go_engine import GoEngine, Stone
import json
from datetime import datetime

class GameService:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_game(self, black_player_id: int, white_player_id: int, board_size: int = 9) -> Game:
        """Create a new game"""
        engine = GoEngine(board_size)
        
        game = Game(
            black_player_id=black_player_id,
            white_player_id=white_player_id,
            board_state=engine.serialize(),
            current_turn='black',
            board_size=board_size
        )
        
        self.db.add(game)
        self.db.commit()
        return game
    
    def get_game(self, game_id: int) -> Game:
        """Get game by ID"""
        return self.db.query(Game).filter(Game.id == game_id).first()
    
    def load_engine(self, game: Game) -> GoEngine:
        """Load Go engine from game state"""
        return GoEngine.deserialize(game.board_state)
    
    def save_engine(self, game: Game, engine: GoEngine):
        """Save Go engine state to game"""
        game.board_state = engine.serialize()
        game.current_turn = 'black' if engine.current_player == Stone.BLACK else 'white'
        game.updated_at = datetime.utcnow()
        self.db.commit()
    
    def make_move(self, game_id: int, player_id: int, row: int, col: int) -> dict:
        """Make a move in the game"""
        game = self.get_game(game_id)
        if not game:
            return {'success': False, 'error': 'Game not found'}
        
        if game.game_status != 'active':
            return {'success': False, 'error': 'Game is not active'}
        
        # Check if it's player's turn
        current_player_id = game.black_player_id if game.current_turn == 'black' else game.white_player_id
        if player_id != current_player_id:
            return {'success': False, 'error': 'Not your turn'}
        
        # Load engine and make move
        engine = self.load_engine(game)
        
        if engine.make_move(row, col):
            self.save_engine(game, engine)
            return {
                'success': True,
                'board_state': engine.get_board_state(),
                'current_player': 'black' if engine.current_player == Stone.BLACK else 'white',
                'captured': {
                    'black': engine.captured[Stone.WHITE],
                    'white': engine.captured[Stone.BLACK]
                }
            }
        else:
            return {'success': False, 'error': 'Invalid move'}
    
    def pass_turn(self, game_id: int, player_id: int) -> dict:
        """Pass turn in the game"""
        game = self.get_game(game_id)
        if not game:
            return {'success': False, 'error': 'Game not found'}
        
        if game.game_status != 'active':
            return {'success': False, 'error': 'Game is not active'}
        
        # Check if it's player's turn
        current_player_id = game.black_player_id if game.current_turn == 'black' else game.white_player_id
        if player_id != current_player_id:
            return {'success': False, 'error': 'Not your turn'}
        
        engine = self.load_engine(game)
        engine.pass_turn()
        
        # Check for consecutive passes (game end)
        if (len(engine.move_history) >= 2 and 
            engine.move_history[-1].get('pass') and 
            engine.move_history[-2].get('pass')):
            game.game_status = 'finished'
            
            # Calculate winner
            score = engine.get_score()
            if score['black'] > score['white']:
                game.winner_id = game.black_player_id
            elif score['white'] > score['black']:
                game.winner_id = game.white_player_id
        
        self.save_engine(game, engine)
        
        return {
            'success': True,
            'current_player': 'black' if engine.current_player == Stone.BLACK else 'white',
            'game_status': game.game_status
        }
    
    def get_game_state(self, game_id: int) -> dict:
        """Get current game state"""
        game = self.get_game(game_id)
        if not game:
            return {'error': 'Game not found'}
        
        engine = self.load_engine(game)
        score = engine.get_score()
        
        return {
            'game_id': game.id,
            'board_state': engine.get_board_state(),
            'board_size': engine.size,
            'current_player': 'black' if engine.current_player == Stone.BLACK else 'white',
            'game_status': game.game_status,
            'black_player_id': game.black_player_id,
            'white_player_id': game.white_player_id,
            'captured': {
                'black': engine.captured[Stone.WHITE],
                'white': engine.captured[Stone.BLACK]
            },
            'score': score,
            'move_history': engine.move_history
        }
    
    def resign_game(self, game_id: int, player_id: int) -> dict:
        """Resign from game"""
        game = self.get_game(game_id)
        if not game:
            return {'success': False, 'error': 'Game not found'}
        
        if game.game_status != 'active':
            return {'success': False, 'error': 'Game is not active'}
        
        # Set winner as opponent
        if player_id == game.black_player_id:
            game.winner_id = game.white_player_id
        elif player_id == game.white_player_id:
            game.winner_id = game.black_player_id
        else:
            return {'success': False, 'error': 'Player not in this game'}
        
        game.game_status = 'finished'
        self.db.commit()
        
        return {'success': True, 'winner_id': game.winner_id}