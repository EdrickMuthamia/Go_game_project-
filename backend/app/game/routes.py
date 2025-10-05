from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.game import bp
from app.game.models import Game
from app.game.ai import GoAI
from app import db


@bp.route('/new', methods=['POST'])
@jwt_required()
def new_game():
    user_id, data = int(get_jwt_identity()), request.get_json()
    board_size = data.get('board_size', 9) if data and data.get('board_size') in [9, 13] else 9

    game = Game(player_id=user_id, board_size=board_size)
    db.session.add(game)
    db.session.commit()

    return jsonify({
        'message': 'Game created - You are Black, AI is White',
        'game': game.to_dict()
    }), 201


@bp.route('/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game(game_id):
    
    user_id, game = int(get_jwt_identity()), Game.query.get(game_id)
    if not game or game.player_id != user_id:
        return jsonify({'message': 'Game not found'}), 404

    return jsonify({'game': game.to_dict()}), 200


@bp.route('/', methods=['GET'])
@jwt_required()
def get_user_games():

    games = Game.query.filter_by(player_id=int(get_jwt_identity())).all()

    return jsonify({
        'games': [game.to_dict() for game in games]
    }), 200


@bp.route('/<int:game_id>/move', methods=['POST'])
@jwt_required()
def make_move(game_id):
   
    user_id, game = int(get_jwt_identity()), Game.query.get(game_id)

    # Ensure game exists and belongs to user
    if not game or game.player_id != user_id:
        return jsonify({'message': 'Game not found'}), 404

    # Ensure it's user's turn (Black) and game is still active
    if game.game_status != 'active' or game.current_player != 'black':
        return jsonify({'message': 'Not your turn'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data'}), 400

    # Handle "pass" move
    if data.get('pass'):
        return handle_pass(game)

    # Ensure valid coordinates
    if 'row' not in data or 'col' not in data:
        return jsonify({'message': 'Missing row or col'}), 400

    row, col = data['row'], data['col']

    if not (0 <= row < game.board_size and 0 <= col < game.board_size):
        return jsonify({'message': 'Invalid position'}), 400

    board = game.get_board()

    if board[row][col]:
        return jsonify({'message': 'Position occupied'}), 400

    # Place player's stone
    board[row][col] = 'black'

    # Capture opponent stones (if any)
    game.captured_white += capture_stones(board, 'white', game.board_size)
    game.set_board(board)

    # AI's move
    ai_move = GoAI(game.board_size).make_move(board)
    if ai_move:
        board[ai_move[0]][ai_move[1]] = 'white'
        game.captured_black += capture_stones(board, 'black', game.board_size)
        game.set_board(board)
    else:
        # AI passed => end game and decide winner
        game.game_status, game.winner = 'finished', 'black' if game.captured_white > game.captured_black + 6.5 else 'white'

    db.session.commit()

    return jsonify({
        'message': 'Move made',
        'game': game.to_dict(),
        'ai_move': ai_move
    }), 200


@bp.route('/<int:game_id>/pass', methods=['POST'])
@jwt_required()
def pass_turn(game_id):
    
    user_id, game = int(get_jwt_identity()), Game.query.get(game_id)

    if not game or game.player_id != user_id:
        return jsonify({'message': 'Game not found'}), 404

    if game.game_status != 'active' or game.current_player != 'black':
        return jsonify({'message': 'Not your turn'}), 400

    return handle_pass(game)

def handle_pass(game):
    
    board, ai_move = game.get_board(), GoAI(game.board_size).make_move(game.get_board())

    if ai_move:
        board[ai_move[0]][ai_move[1]] = 'white'
        game.captured_black += capture_stones(board, 'black', game.board_size)
        game.set_board(board)
        message = f'You passed. AI moved at ({ai_move[0]}, {ai_move[1]})'
    else:
        # Both passed => end game
        game.game_status, game.winner = 'finished', 'black' if game.captured_white > game.captured_black + 6.5 else 'white'
        message = 'Both passed - Game ended'

    db.session.commit()

    return jsonify({
        'message': message,
        'game': game.to_dict(),
        'ai_move': ai_move
    }), 200


def capture_stones(board, color, board_size):
    
    captured = 0
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == color and has_no_liberties(board, row, col, board_size):
                captured += remove_group(board, row, col, color, board_size)
    return captured


def has_no_liberties(board, row, col, board_size):
    
    if not board[row][col]:
        return False

    color, visited, stack = board[row][col], set(), [(row, col)]

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        # Explore neighbors
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < board_size and 0 <= nc < board_size:
                if not board[nr][nc]:
                    return False  # Found a liberty
                elif board[nr][nc] == color:
                    stack.append((nr, nc))

    return True


def remove_group(board, start_row, start_col, color, board_size):
    
    removed, stack, visited = 0, [(start_row, start_col)], set()

    while stack:
        row, col = stack.pop()

        if (row, col) in visited or board[row][col] != color:
            continue

        visited.add((row, col))
        board[row][col], removed = None, removed + 1

        # Explore neighbors
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < board_size and 0 <= nc < board_size:
                stack.append((nr, nc))

    return removed