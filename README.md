# Go Game Project

A web-based Go game with AI opponent, user authentication, and game persistence.

## Features

- **Interactive Go Board** - Play Go on 9x9, 13x13, or 19x19 boards
- **AI Opponent** - Strategic AI with capture, defense, and tactical play
- **User Authentication** - Secure login and registration system
- **Game Persistence** - Save and resume games
- **Real-time Gameplay** - Responsive web interface

## Tech Stack

### Backend
- **Python Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database
- **Alembic** - Database migrations

### Frontend
- **React** - UI framework
- **JavaScript** - Client-side logic
- **CSS** - Styling

## Quick Start

### Backend Setup
```bash
cd backend
pip install pipenv
pipenv install
pipenv shell
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Database Setup
```bash
cd backend
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

## Project Structure

```
Go_game_project-/
├── backend/
│   ├── app/
│   │   ├── auth/          # Authentication routes
│   │   ├── game/          # Game logic and AI
│   │   └── config.py      # Configuration
│   ├── migrations/        # Database migrations
│   └── main.py           # Application entry point
└── frontend/
    ├── src/
    │   ├── components/    # React components
    │   └── services/      # API services
    └── public/           # Static assets
```

## API Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /games` - List user games
- `POST /games` - Create new game
- `POST /games/{id}/move` - Make move
- `GET /games/{id}` - Get game state

## Game Rules

- Standard Go rules apply
- Capture stones by surrounding them
- AI plays as white, human as black
- Pass when no moves available

## Development

### Run Tests
```bash
cd backend && python -m pytest
cd frontend && npm test
```

### Database Migration
```bash
cd backend
flask db migrate -m "description"
flask db upgrade
```

## Contributors

- Bettson Kiptoo
- Jane Kimei
- Feysal Abdii
- Edrick Muthamia 

## License

MIT License

 