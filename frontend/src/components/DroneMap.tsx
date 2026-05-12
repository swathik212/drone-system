import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Box, Sphere, Line } from '@react-three/drei';
import * as THREE from 'three';

const Scene = ({ bounds, start, goal, obstacles, noFlyZones, path }: any) => {
  const droneRef = useRef<THREE.Mesh>(null);
  
  // Animate drone along path
  useFrame(({ clock }) => {
    if (path.length > 0 && droneRef.current) {
      const time = clock.getElapsedTime();
      const speed = 2; // cells per second
      const progress = (time * speed) % path.length;
      const index = Math.floor(progress);
      const nextIndex = Math.min(index + 1, path.length - 1);
      const fraction = progress - index;
      
      const p1 = path[index];
      const p2 = path[nextIndex];
      
      droneRef.current.position.set(
        p1.x + (p2.x - p1.x) * fraction,
        p1.z + (p2.z - p1.z) * fraction, // map z to threejs y
        p1.y + (p2.y - p1.y) * fraction  // map y to threejs z
      );
    }
  });

  const pathPoints = path.map((p: any) => new THREE.Vector3(p.x, p.z, p.y));

  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 20, 10]} intensity={1} />
      
      {/* Grid Helper */}
      <gridHelper args={[Math.max(bounds[0], bounds[1]) * 2, Math.max(bounds[0], bounds[1]) * 2]} position={[bounds[0]/2, -0.5, bounds[1]/2]} />

      {/* Start and Goal */}
      <Sphere args={[0.3]} position={[start.x, start.z, start.y]}>
        <meshStandardMaterial color="green" />
      </Sphere>
      <Sphere args={[0.3]} position={[goal.x, goal.z, goal.y]}>
        <meshStandardMaterial color="blue" />
      </Sphere>

      {/* Obstacles (Buildings) */}
      {obstacles.map((obs: any, i: number) => (
        <Box key={i} args={[1, 1, 1]} position={[obs.x, obs.z, obs.y]}>
          <meshStandardMaterial color="gray" opacity={0.8} transparent />
        </Box>
      ))}

      {/* No Fly Zones */}
      {noFlyZones.map((nfz: any, i: number) => (
        <Box key={`nfz-${i}`} args={[1, 1, 1]} position={[nfz.x, nfz.z, nfz.y]}>
          <meshStandardMaterial color="red" opacity={0.3} transparent />
        </Box>
      ))}

      {/* Path Line */}
      {pathPoints.length > 1 && (
        <Line points={pathPoints} color="yellow" lineWidth={3} />
      )}

      {/* Drone */}
      {path.length > 0 && (
        <Sphere ref={droneRef} args={[0.2]}>
          <meshStandardMaterial color="red" />
        </Sphere>
      )}

      <OrbitControls target={[bounds[0]/2, bounds[2]/2, bounds[1]/2]} />
    </>
  );
};

const DroneMap = (props: any) => {
  return (
    <Canvas camera={{ position: [15, 15, 15], fov: 50 }}>
      {/* Add a black background */}
      <color attach="background" args={['#000']} />
      <Scene {...props} />
    </Canvas>
  );
};

export default DroneMap;
