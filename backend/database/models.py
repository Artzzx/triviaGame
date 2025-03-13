import datetime
from typing import List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Text, Table, JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """User account information and game statistics."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    last_login = Column(DateTime, nullable=True)
    
    # Game statistics
    total_games = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    
    # Relationships
    game_participations = relationship("GameParticipant", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"

class Category(Base):
    """Question categories from Open Trivia DB."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    api_id = Column(Integer, nullable=True)  # ID in Open Trivia DB
    
    # Relationships
    questions = relationship("Question", back_populates="category")
    
    def __repr__(self):
        return f"<Category {self.name}>"

class Question(Base):
    """Cached questions from Open Trivia DB."""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(100), unique=True, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    question_text = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    incorrect_answers = Column(JSON, nullable=False)  # JSON array of incorrect answers
    created_at = Column(DateTime, default=datetime.datetime.now)
    times_used = Column(Integer, default=0)
    
    # Relationships
    category = relationship("Category", back_populates="questions")
    game_questions = relationship("GameQuestion", back_populates="question")
    
    def __repr__(self):
        return f"<Question {self.id}: {self.question_text[:30]}...>"

class GameRoom(Base):
    """Game room information."""
    __tablename__ = "game_rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))
    game_mode = Column(String(50), nullable=False, default="standard")
    max_players = Column(Integer, default=8)
    is_private = Column(Boolean, default=False)
    password_hash = Column(String(255), nullable=True)  # For private rooms
    status = Column(String(20), nullable=False, default="waiting")  # waiting, in_progress, completed
    created_at = Column(DateTime, default=datetime.datetime.now)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    
    # Relationships
    creator = relationship("User")
    participants = relationship("GameParticipant", back_populates="game_room")
    questions = relationship("GameQuestion", back_populates="game_room")
    
    def __repr__(self):
        return f"<GameRoom {self.room_code}: {self.name}>"

class GameParticipant(Base):
    """Player in a game room."""
    __tablename__ = "game_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    game_room_id = Column(Integer, ForeignKey("game_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.datetime.now)
    is_active = Column(Boolean, default=True)  # To track disconnections
    score = Column(Integer, default=0)
    rank = Column(Integer, nullable=True)  # Final rank in the game
    
    # Relationships
    game_room = relationship("GameRoom", back_populates="participants")
    user = relationship("User", back_populates="game_participations")
    answers = relationship("PlayerAnswer", back_populates="participant")
    
    def __repr__(self):
        return f"<GameParticipant: {self.user_id} in room {self.game_room_id}>"

class GameQuestion(Base):
    """Question used in a specific game."""
    __tablename__ = "game_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    game_room_id = Column(Integer, ForeignKey("game_rooms.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    sequence_number = Column(Integer, nullable=False)  # Order in the game
    start_time = Column(DateTime, nullable=True)  # When question was presented
    end_time = Column(DateTime, nullable=True)  # When question timed out
    
    # Relationships
    game_room = relationship("GameRoom", back_populates="questions")
    question = relationship("Question", back_populates="game_questions")
    player_answers = relationship("PlayerAnswer", back_populates="game_question")
    
    def __repr__(self):
        return f"<GameQuestion {self.id}: seq={self.sequence_number}>"

class PlayerAnswer(Base):
    """Player's answer to a question."""
    __tablename__ = "player_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    game_question_id = Column(Integer, ForeignKey("game_questions.id"), nullable=False)
    participant_id = Column(Integer, ForeignKey("game_participants.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answer_time_ms = Column(Integer, nullable=False)  # Response time in milliseconds
    points_earned = Column(Integer, nullable=False, default=0)
    
    # Relationships
    game_question = relationship("GameQuestion", back_populates="player_answers")
    participant = relationship("GameParticipant", back_populates="answers")
    
    def __repr__(self):
        return f"<PlayerAnswer {self.id}: correct={self.is_correct}, points={self.points_earned}>"

class Leaderboard(Base):
    """Global leaderboard statistics."""
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    total_points = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    total_answers = Column(Integer, default=0)
    fastest_answer_ms = Column(Integer, nullable=True)  # Fastest correct answer time
    average_time_ms = Column(Integer, nullable=True)  # Average answer time
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<Leaderboard entry for user {self.user_id}: points={self.total_points}>"