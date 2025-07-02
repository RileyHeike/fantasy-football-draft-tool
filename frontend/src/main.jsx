import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';

function App() {
  const [player, setPlayer] = useState('');
  const [data, setData] = useState(null);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    setSearching(true);
    setError('');
    setData(null);
    try {
      const res = await axios.get(`http://localhost:5002/player-props-summary/${player}`);
      setData(res.data);
    } catch (err) {
      setError('Player not found or API error.');
    }
    setSearching(false);
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Fantasy Draft Assistant</h1>
      <form onSubmit={handleSearch} style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Enter player slug (e.g. jalen-hurts)"
          value={player}
          onChange={e => setPlayer(e.target.value)}
          style={{ padding: '0.5rem', width: '250px' }}
        />
        <button type="submit" style={{ marginLeft: '1rem', padding: '0.5rem 1rem' }} disabled={searching}>
          {searching ? 'Searching...' : 'Search'}
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data && data.summary && (
        <div>
          <p><strong>Player:</strong> {data.player}</p>
          <p><strong>Team:</strong> {data.team || 'N/A'}</p>
          <p><strong>Position:</strong> {data.position || 'N/A'}</p>
          <h3>Average Prop Lines</h3>
          <table border="1" cellPadding="8" style={{ borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Category</th>
                <th>Average Line</th>
                <th>Sample Size</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.summary).map(([cat, val]) => (
                <tr key={cat}>
                  <td>{cat}</td>
                  <td>{val.average}</td>
                  <td>{val.sample_size}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
