import { useState } from 'react';
import { findPath } from '../api';

const Controls = ({ bounds, start, goal, obstacles, noFlyZones, setStart, setGoal, setObstacles, onPathFound }: any) => {
  const [algorithm, setAlgorithm] = useState('ucs');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const result = await findPath({
        bounds,
        start,
        goal,
        obstacles,
        no_fly_zones: noFlyZones,
        algorithm
      });
      if (result.path.length === 0) {
        alert("No path found");
      }
      onPathFound(result.path, {
        cost: result.cost,
        nodes_expanded: result.nodes_expanded,
        runtime: result.runtime
      });
    } catch (err) {
      alert("Error finding path");
      console.error(err);
    }
    setLoading(false);
  };

  const updateCoordinate = (setter: any, current: any, field: string, value: string) => {
    const num = parseInt(value, 10);
    if (!isNaN(num)) {
      setter({ ...current, [field]: num });
    }
  };

  const generateRandomObstacles = () => {
    const newObstacles = [];
    for (let i = 0; i < 15; i++) {
      const x = Math.floor(Math.random() * bounds[0]);
      const y = Math.floor(Math.random() * bounds[1]);
      const maxZ = Math.floor(Math.random() * (bounds[2] - 2)) + 1;
      
      for (let z = 0; z < maxZ; z++) {
         if (!(x === start.x && y === start.y && z === start.z) && 
             !(x === goal.x && y === goal.y && z === goal.z)) {
            newObstacles.push({x, y, z});
         }
      }
    }
    setObstacles(newObstacles);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
      <h2>Drone Navigation Settings</h2>
      
      <div>
        <label>Algorithm:</label>
        <select 
          value={algorithm} 
          onChange={e => setAlgorithm(e.target.value)}
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        >
          <option value="ucs">Uniform Cost Search (UCS)</option>
          <option value="astar_manhattan">A* (Manhattan)</option>
          <option value="astar_euclidean">A* (Euclidean)</option>
          <option value="astar_building">A* (Building-Aware)</option>
        </select>
      </div>

      <div>
        <h3>Edit Coordinates</h3>
        <p style={{fontSize: '0.8em', color: '#ccc'}}>Format: [X, Y, Altitude]</p>
        <div style={{display:'flex', gap:'10px', alignItems:'center'}}>
          <label style={{width: '60px'}}>Start:</label>
          <input type="number" value={start.x} onChange={e => updateCoordinate(setStart, start, 'x', e.target.value)} style={{width: '50px'}} title="X position" />
          <input type="number" value={start.y} onChange={e => updateCoordinate(setStart, start, 'y', e.target.value)} style={{width: '50px'}} title="Y position" />
          <input type="number" value={start.z} onChange={e => updateCoordinate(setStart, start, 'z', e.target.value)} style={{width: '50px'}} title="Altitude (Z)" />
        </div>
        <div style={{display:'flex', gap:'10px', alignItems:'center', marginTop: '10px'}}>
          <label style={{width: '60px'}}>Goal:</label>
          <input type="number" value={goal.x} onChange={e => updateCoordinate(setGoal, goal, 'x', e.target.value)} style={{width: '50px'}} title="X position" />
          <input type="number" value={goal.y} onChange={e => updateCoordinate(setGoal, goal, 'y', e.target.value)} style={{width: '50px'}} title="Y position" />
          <input type="number" value={goal.z} onChange={e => updateCoordinate(setGoal, goal, 'z', e.target.value)} style={{width: '50px'}} title="Altitude (Z)" />
        </div>
      </div>

      <div>
        <h3>Obstacles: {obstacles.length} blocks</h3>
        <button onClick={generateRandomObstacles} style={{ marginRight: '10px', padding: '5px', cursor: 'pointer' }}>Generate Random City</button>
        <button onClick={() => setObstacles([])} style={{ padding: '5px', cursor: 'pointer' }}>Clear Obstacles</button>
      </div>

      <button 
        onClick={handleSearch} 
        disabled={loading}
        style={{
          padding: '10px',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer',
          marginTop: '10px'
        }}
      >
        {loading ? 'Searching...' : 'Find Path'}
      </button>

    </div>
  );
};

export default Controls;
