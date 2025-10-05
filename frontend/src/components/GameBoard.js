import React, { useState, useEffect } from 'react';
import axios from 'axios';

function GameBoard({ token, game: initialGame, onBack }) {
  const [game, setGame] = useState(initialGame);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (initialGame) {
      getGameData(initialGame.id);
    }
  });

  const getGameData = (gameId) => {
    axios.get(`http://localhost:5000/api/game/${gameId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(function(response) {
      setGame(response.data.game);
    })
    .catch(function(error) {
      setError('Could not get game data');
    });
  };

  const placeStone = (row, col) => {
    if (loading) return;
    if (game.game_status !== 'active') return;
    if (game.current_player !== 'black') return;

    setLoading(true);
    setError('');

    axios.post(`http://localhost:5000/api/game/${game.id}/move`, {
      row: row,
      col: col
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(function(response) {
      setGame(response.data.game);
      setLoading(false);
    })
    .catch(function(error) {
      setError('Could not place stone');
      setLoading(false);
    });
  };

  const skipTurn = () => {
    if (loading) return;
    if (game.game_status !== 'active') return;
    if (game.current_player !== 'black') return;

    setLoading(true);
    setError('');

    axios.post(`http://localhost:5000/api/game/${game.id}/pass`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(function(response) {
      setGame(response.data.game);
      setLoading(false);
    })
    .catch(function(error) {
      setError('Could not skip turn');
      setLoading(false);
    });
  };

  if (!game) {
    return <div>Loading...</div>;
  }

  const drawBoard = () => {
    const boardSize = game.board_size;
    const cellSize = 40;
    const totalSize = (boardSize - 1) * cellSize;
    
    const lines = [];
    for (let i = 0; i < boardSize; i++) {
      const pos = i * cellSize;
      lines.push(
        <line key={`h${i}`} x1="0" y1={pos} x2={totalSize} y2={pos} stroke="#000" strokeWidth="1" />
      );
      lines.push(
        <line key={`v${i}`} x1={pos} y1="0" x2={pos} y2={totalSize} stroke="#000" strokeWidth="1" />
      );
    }

    const intersections = [];
    for (let row = 0; row < boardSize; row++) {
      for (let col = 0; col < boardSize; col++) {
        const x = col * cellSize;
        const y = row * cellSize;
        const stone = game.board[row][col];
        
        intersections.push(
          <div
            key={`${row}-${col}`}
            className="intersection"
            style={{ left: x, top: y }}
            onClick={() => placeStone(row, col)}
          >
            {stone && (
              <div className={`stone ${stone}`}></div>
            )}
          </div>
        );
      }
    }

    return (
      <div className="board-container">
        <svg className="board-lines" width={totalSize} height={totalSize}>
          {lines}
        </svg>
        {intersections}
      </div>
    );
  };

  return (
    <div className="game-container">
      <button onClick={onBack} className="btn btn-secondary">
        ← Back to Games
      </button>

      <div className="score-panel">
        <div>Black Score: {game.captured_by_human}</div>
        <div>White Score: {game.captured_by_ai}</div>
        <div>Current Player: {game.current_player}</div>
        <div>Captured - Black: {game.captured_by_ai}, White: {game.captured_by_human}</div>
      </div>

      <div className="game-board">
        {drawBoard()}
      </div>

      <div className="game-controls">
        <button 
          onClick={skipTurn}
          className="btn btn-secondary"
        >
          Pass
        </button>
        
        {game.game_status === 'finished' && (
          <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#28a745' }}>
            Game Over! Winner: {game.winner}
          </div>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}
      {loading && <div>Processing move...</div>}
    </div>
  );
}

export default GameBoard;