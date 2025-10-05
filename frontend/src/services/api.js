import React, { useState, useEffect } from 'react';
import './App.css';
import Login from './components/Login';
import GameBoard from './components/GameBoard';
import GameList from './components/GameList';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [currentGame, setCurrentGame] = useState(null);
  const [view, setView] = useState('games'); // 'games' or 'game'

  useEffect(() => {
    if (token) {
      const userData = localStorage.getItem('user');
      if (userData) {
        setUser(JSON.parse(userData));
      }
    }
  }, [token]);

  const handleLogin = (token, user) => {
    setToken(token);
    setUser(user);
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    setCurrentGame(null);
    setView('games');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const handleGameSelect = (game) => {
    setCurrentGame(game);
    setView('game');
  };

  const handleBackToGames = () => {
    setCurrentGame(null);
    setView('games');
  };

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>Go Game</h1>
        <div className="user-info">
          <span>Welcome, {user?.username}</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </header>
      
      {view === 'games' ? (
        <GameList 
          token={token} 
          onGameSelect={handleGameSelect}
        />
      ) : (
        <GameBoard 
          token={token}
          game={currentGame}
          onBack={handleBackToGames}
        />
      )}
    </div>
  );
}

export default App;