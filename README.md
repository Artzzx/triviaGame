# Multiplayer Real-Time Quiz Game

A fast-paced, real-time multiplayer quiz game that utilizes WebSockets for live gameplay and fetches diverse questions from the Open Trivia Database.

## Features

- **Real-time Multiplayer**: Create and join game rooms instantly
- **Diverse Question Categories**: Questions from the Open Trivia Database covering numerous topics
- **Dynamic Scoring**: Points awarded based on speed and accuracy
- **Live Leaderboard**: Track rankings in real-time
- **Multiple Game Modes**: Quick Match, Tournament, and more
- **User Authentication**: Create accounts and track your stats

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL (optional, SQLite for development)

### Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/quiz-game.git
   cd quiz-game
   ```
2. Create and activate a virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Configure environment variables
    ```bash
    cp .env.example .env
    # Edit .env with your configuration
    ```
5. Initialize the database   
    ```bash
    python -m backend.database.db_handler --init
    ```
## Running the Application

### Development Mode

```bash
 python -m backend.database.db_handler --init
```
### Production Mode

```bash
 python run.py
```
## Project Structure

```
    quiz_game/
    ├── backend/        # Server-side code
    ├── frontend/       # Client-side interface
    ├── tests/          # Test suites
    └── docs/           # Documentation
```
## Game Modes

- Quick Match: 10 random questions with 15-second time limit
- Tournament: Multiple rounds with increasing difficulty
- Custom Game: Create games with specific categories and settings

## API Integration
This project uses the Open Trivia Database API. See API Documentation for details.

## License
Distributed under the MIT License. See LICENSE for more information.
