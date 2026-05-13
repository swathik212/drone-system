import { useState } from 'react';
import DroneMap from './components/DroneMap';
import Controls from './components/Controls';
import type { Coordinate } from './api';

function App() {
  const [bounds] = useState<[number, number, number]>([10, 10, 10]);
  const [start, setStart] = useState<Coordinate>({ x: 0, y: 0, z: 0 });
  const [goal, setGoal] = useState<Coordinate>({ x: 9, y: 9, z: 9 });
  const [obstacles, setObstacles] = useState<Coordinate[]>([
    {x: 5, y: 5, z: 0}, {x: 5, y: 5, z: 1}, {x: 5, y: 5, z: 2},
    {x: 5, y: 5, z: 3}, {x: 5, y: 5, z: 4}, {x: 5, y: 5, z: 5}
  ]);
  const [noFlyZones, setNoFlyZones] = useState<Coordinate[]>([]);
  const [path, setPath] = useState<Coordinate[]>([]);
  const [metrics, setMetrics] = useState<any>(null);

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw' }}>
      <div style={{ flex: 1, position: 'relative' }}>
        <DroneMap 
          bounds={bounds} 
          start={start} 
          goal={goal} 
          obstacles={obstacles} 
          noFlyZones={noFlyZones}
          path={path} 
        />
      </div>
      <div style={{ width: '400px', backgroundColor: '#1e1e1e', color: 'white', padding: '20px', overflowY: 'auto' }}>
        <Controls 
          bounds={bounds}
          start={start}
          goal={goal}
          obstacles={obstacles}
          noFlyZones={noFlyZones}
          setStart={setStart}
          setGoal={setGoal}
          setObstacles={setObstacles}
          setNoFlyZones={setNoFlyZones}
          onPathFound={(pathData: any, metricsData: any) => {
            setPath(pathData);
            setMetrics(metricsData);
          }}
        />
        {metrics && (
          <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#2d2d2d', borderRadius: '8px' }}>
            <h3>Results</h3>
            <p><strong>Cost:</strong> {metrics.cost}</p>
            <p><strong>Nodes Expanded:</strong> {metrics.nodes_expanded}</p>
            <p><strong>Runtime:</strong> {(metrics.runtime * 1000).toFixed(2)} ms</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
