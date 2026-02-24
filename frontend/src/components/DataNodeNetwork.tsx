import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Points, PointMaterial } from '@react-three/drei';
import * as THREE from 'three';

const ParticleSwarm = () => {
  const pointsRef = useRef<THREE.Points>(null);

  // Generate random points in a sphere
  const [positions, floatSpeeds] = useMemo(() => {
    const count = 3000;
    const pos = new Float32Array(count * 3);
    const speeds = new Float32Array(count);

    for (let i = 0; i < count; i++) {
      // Use spherical coordinates for better distribution
      const u = Math.random();
      const v = Math.random();
      const theta = u * 2.0 * Math.PI;
      const phi = Math.acos(2.0 * v - 1.0);
      const r = Math.cbrt(Math.random()) * 2.5; // Radius 2.5

      const sinPhi = Math.sin(phi);
      pos[i * 3] = r * sinPhi * Math.cos(theta);     // x
      pos[i * 3 + 1] = r * sinPhi * Math.sin(theta); // y
      pos[i * 3 + 2] = r * Math.cos(phi);            // z
      
      speeds[i] = (Math.random() - 0.5) * 0.2; // Float speed
    }

    return [pos, speeds];
  }, []);

  useFrame((state) => {
    if (!pointsRef.current) return;
    const time = state.clock.getElapsedTime();
    // Soothing, slow rotation
    pointsRef.current.rotation.y = time * 0.02;
    pointsRef.current.rotation.x = time * 0.01;
    
    // Add subtle waving motion
    const positions = pointsRef.current.geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < positions.length; i += 3) {
      const speed = floatSpeeds[i / 3];
      positions[i + 1] += Math.sin(time * 0.5 + speed * 100) * 0.001;
    }
    pointsRef.current.geometry.attributes.position.needsUpdate = true;
  });

  return (
    <Points ref={pointsRef} positions={positions} stride={3} frustumCulled={false}>
      <PointMaterial
        transparent
        color="#FFFFFF" // Inverted to white for dark background
        size={0.018}
        sizeAttenuation={true}
        depthWrite={false}
        opacity={0.15} // Even more subtle against dark bg
        blending={THREE.AdditiveBlending} // Additive works beautifully on dark backgrounds
      />
    </Points>
  );
};

export default function DataNodeNetwork() {
  return (
    <div className="absolute inset-0 -z-10 h-[100%] w-full overflow-hidden pointer-events-none bg-background">
      <Canvas camera={{ position: [0, 0, 4.5], fov: 60 }} dpr={[1, 2]}>
        <ParticleSwarm />
      </Canvas>
    </div>
  );
}
