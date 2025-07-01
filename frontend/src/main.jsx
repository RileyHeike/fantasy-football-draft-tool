import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:5002/projected-points")
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Fantasy Draft Assistant</h1>
      {data ? (
        <div>
          <p><strong>Player:</strong> {data.player}</p>
          <p><strong>Team:</strong> {data.team}</p>
          <p><strong>Projected Fantasy Points:</strong> {data.projected_fantasy_points.toFixed(2)}</p>
        </div>
      ) : <p>Loading...</p>}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
