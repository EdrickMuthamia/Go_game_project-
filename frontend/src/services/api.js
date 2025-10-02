import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE,
});

// Auth endpoints
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getProfile: (token) => api.get('/auth/profile', {
    headers: { Authorization: `Bearer ${token}` }
  })
};

// Game endpoints
export const gameAPI = {
  getGames: (token) => api.get('/game/', {
    headers: { Authorization: `Bearer ${token}` }
  }),
  
  createGame: (token, boardSize = 9) => api.post('/game/new', 
    { board_size: boardSize }, 
    { headers: { Authorization: `Bearer ${token}` } }
  ),
  
  getGame: (token, gameId) => api.get(`/game/${gameId}`, {
    headers: { Authorization: `Bearer ${token}` }
  }),
  
  makeMove: (token, gameId, row, col) => api.post(`/game/${gameId}/move`, 
    { row, col }, 
    { headers: { Authorization: `Bearer ${token}` } }
  ),
  
  passMove: (token, gameId) => api.post(`/game/${gameId}/pass`, 
    {}, 
    { headers: { Authorization: `Bearer ${token}` } }
  )
};

export default api;