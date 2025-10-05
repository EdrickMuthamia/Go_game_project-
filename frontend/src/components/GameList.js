import React, { useState, useEffect } from 'react';
import axios from 'axios';

function GameList({ token, onGameSelect }) {
  // Simple state variables
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Get games when component loads
  useEffect(() => {
    // Get all games from server
    axios.get('http://localhost:5000/api/game/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(function(response) {
      setGames(response.data.games);
      setLoading(false);
    })
    .catch(function(error) {
      setError('Could not get games');
      setLoading(false);
    });
  }, [token]);

  // Get all games from server
  const getGames = () => {
    axios.get('http://localhost:5000/api/game/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(function(response) {
      setGames(response.data.games);
      setLoading(false);
    })
    .catch(function(error) {
      setError('Could not get games');
      setLoading(false);
    });
  };

  // Create a new game
  const makeNewGame = () => {
    axios.post('http://localhost:5000/api/game/new', {
      board_size: 9
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(function(response) {
      getGames();
    })
    .catch(function(error) {
      setError('Could not create game');
    });
  };

  if (loading) return <div>Loading games...</div>;

  return (
    <div className="game-list">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Your Games</h2>
        <button onClick={makeNewGame} className="btn btn-success">
          New Game
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {games.length === 0 && <div>No games yet. Create your first game!</div>}
      
      {games.map(function(game) {
        return (
          <div 
            key={game.id} 
            className="game-item"
            onClick={() => onGameSelect(game)}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3>Game #{game.id}</h3>
                <p>Board Size: {game.board_size}x{game.board_size}</p>
                <p>Current Player: {game.current_player}</p>
                <p>Created: {new Date(game.created_at).toLocaleDateString()}</p>
              </div>
              <div>
                <span className={`game-status ${game.game_status}`}>
                  {game.game_status.toUpperCase()}
                </span>
                {game.winner && <div>Winner: {game.winner}</div>}
              </div>
            </div>
          </div>
        );
      })
    }
    </div>
  );
}

export default GameList;