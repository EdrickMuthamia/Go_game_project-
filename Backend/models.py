from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    games_as_black = relationship("Game", foreign_keys="Game.black_player_id", back_populates="black_player")
    games_as_white = relationship("Game", foreign_keys="Game.white_player_id", back_populates="white_player")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Game(Base):
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True)
    black_player_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    white_player_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    board_state = Column(Text, nullable=False, default='{}')  # JSON string of board state
    current_turn = Column(String(5), nullable=False, default='black')  # 'black' or 'white'
    game_status = Column(String(20), nullable=False, default='active')  # 'active', 'finished', 'abandoned'
    winner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    board_size = Column(Integer, nullable=False, default=19)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    black_player = relationship("User", foreign_keys=[black_player_id], back_populates="games_as_black")
    white_player = relationship("User", foreign_keys=[white_player_id], back_populates="games_as_white")
    winner = relationship("User", foreign_keys=[winner_id])