
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.auth import bp
from app.auth.models import User
from app import db
from datetime import timedelta


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Username, email, and password are required'}), 400

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Create new user
    user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()

    # Create access token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': user.to_dict()
    }), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    # Validate required fields
    if not all(field in data for field in [
        'username',
        'password'
    ]):
        return jsonify({'message': 'Username and password are required'}), 400

    # Find user and validate password
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Create access token with user ID as integer
    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=6)
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    # Get user ID from JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'user': user.to_dict()}), 200