import React, { useState } from 'react';
import './App.css';

function App() {
  const [enrollNo, setEnrollNo] = useState('');
  const [grid, setGrid] = useState(null);
  const [highlight, setHighlight] = useState('');
  const [className, setClassName] = useState('');

  const handleGenerateGrid = async () => {
    if (!enrollNo) {
      alert('Please enter an enrollment number');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/generate-grid', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ enrollNo }),
      });

      if (response.ok) {
        const data = await response.json();
        setGrid(data.grid); // Update grid from the backend
        setHighlight(data.highlight); // Highlight the specific enrollment
        setClassName(data.class_name); // Update the class name
      } else {
        const errorData = await response.json();
        alert(errorData.error || 'Failed to fetch grid');
      }
    } catch (error) {
      console.error('Error fetching grid:', error);
      alert('Error generating the grid.');
    }
  };

  const renderGrid = (grid) => {
    return (
      <div className="grid-container">
        <h3>{className}</h3>
        <div className="grid">
          {grid.map((row, rowIndex) => (
            <div key={rowIndex} className="grid-row">
              {row.map((cell, colIndex) => (
                <div
                  key={colIndex}
                  className={`grid-cell ${cell === highlight ? 'highlight' : ''}`}
                >
                  {cell || ''}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="App">
      <h1>Seat Position Calculator</h1>
      <div className="input-section">
        <input
          type="text"
          placeholder="Enter Enrollment Number"
          value={enrollNo}
          onChange={(e) => setEnrollNo(e.target.value)}
        />
        <button onClick={handleGenerateGrid}>Generate Grid</button>
      </div>
      <div className="grids-section">
        {grid ? renderGrid(grid) : <p>No grid to display. Please generate a grid.</p>}
      </div>
    </div>
  );
}

export default App;
