/**
 * CinematicIntro.tsx
 * "Clarity from Chaos" – 3-Act cinematic sequence
 * Built with React Three Fiber + GSAP
 * NO @react-three/postprocessing (crashes R3F v8 with applyProps)
 * Bokeh simulated via multi-layer opacity/size rendering
 */
import React, { useRef, useMemo, useEffect, useState, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
import gsap from 'gsap';

// ─── Constants ─────────────────────────────────────────────────────────────
const PARTICLE_COUNT = 1200;
const PARTICLE_COLOR = new THREE.Color('#FFFFFF');

const ACTS = {
  VOID: 0,
  CONVERGENCE: 1,
  INSIGHT: 2,
} as const;
type Act = (typeof ACTS)[keyof typeof ACTS];

// ─── Generate Grid Positions (The Monument) ─────────────────────────────────
function buildGridPositions(count: number) {
  const side = Math.ceil(Math.cbrt(count));
  const spacing = 0.22;
  const positions: [number, number, number][] = [];
  for (let i = 0; i < count; i++) {
    const ix = (i % side) - side / 2;
    const iy = (Math.floor(i / side) % side) - side / 2;
    const iz = Math.floor(i / (side * side)) - side / 2;
    positions.push([ix * spacing, iy * spacing, iz * spacing]);
  }
  return positions;
}

function buildVoidPositions(count: number) {
  return Array.from({ length: count }, () => {
    const r = 3.5 + Math.random() * 1.5;
    const theta = Math.random() * 2 * Math.PI;
    const phi = Math.acos(2 * Math.random() - 1);
    return [
      r * Math.sin(phi) * Math.cos(theta),
      r * Math.sin(phi) * Math.sin(theta),
      r * Math.cos(phi),
    ] as [number, number, number];
  });
}

// ─── Swarm Mesh ─────────────────────────────────────────────────────────────
interface SwarmProps {
  currentAct: Act;
  onConvergenceComplete: () => void;
}

const Swarm: React.FC<SwarmProps> = ({ currentAct, onConvergenceComplete }) => {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const clock = useRef(0);
  const actRef = useRef<Act>(ACTS.VOID);

  // Particle "live" positions that GSAP interpolates
  const livePos = useRef<Float32Array>(new Float32Array(PARTICLE_COUNT * 3));

  const voidPos = useMemo(() => buildVoidPositions(PARTICLE_COUNT), []);
  const gridPos = useMemo(() => buildGridPositions(PARTICLE_COUNT), []);

  // Noise offsets per particle for Act 1 drift
  const noise = useMemo(() => Array.from({ length: PARTICLE_COUNT }, () => ({
    speed: 0.3 + Math.random() * 0.4,
    phase: Math.random() * Math.PI * 2,
  })), []);

  // Opacity that we manage imperatively
  const material = useMemo(() => new THREE.MeshBasicMaterial({
    color: PARTICLE_COLOR,
    transparent: true,
    opacity: 0.55,
  }), []);

  const geometry = useMemo(() => new THREE.IcosahedronGeometry(0.014, 0), []);

  // Initialize positions
  useEffect(() => {
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const [x, y, z] = voidPos[i];
      livePos.current[i * 3] = x;
      livePos.current[i * 3 + 1] = y;
      livePos.current[i * 3 + 2] = z;

      dummy.position.set(x, y, z);
      dummy.scale.setScalar(1);
      dummy.updateMatrix();
      meshRef.current?.setMatrixAt(i, dummy.matrix);
    }
    if (meshRef.current) meshRef.current.instanceMatrix.needsUpdate = true;
  }, [dummy, voidPos]);

  // Act transitions
  useEffect(() => {
    actRef.current = currentAct;

    if (currentAct === ACTS.CONVERGENCE) {
      // Stagger particles to grid using Power4.inOut
      let maxDuration = 0;
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        const delay = (i / PARTICLE_COUNT) * 1.8; // sweep effect
        const duration = 2.2 + Math.random() * 0.8;
        maxDuration = Math.max(maxDuration, delay + duration);
        const [tx, ty, tz] = gridPos[i];
        const proxy = { x: livePos.current[i * 3], y: livePos.current[i * 3 + 1], z: livePos.current[i * 3 + 2] };
        gsap.to(proxy, {
          x: tx, y: ty, z: tz,
          duration,
          delay,
          ease: 'power4.inOut',
          onUpdate: () => {
            livePos.current[i * 3] = proxy.x;
            livePos.current[i * 3 + 1] = proxy.y;
            livePos.current[i * 3 + 2] = proxy.z;
          }
        });
      }
      // Opacity surge during convergence
      gsap.to(material, { opacity: 0.9, duration: 2.5, delay: 0.5, ease: 'power2.inOut' });

      setTimeout(onConvergenceComplete, (maxDuration + 0.3) * 1000);
    }

    if (currentAct === ACTS.INSIGHT) {
      // Ripple flash
      gsap.to(material, {
        opacity: 1,
        duration: 0.15,
        yoyo: true,
        repeat: 1,
        ease: 'expo.out',
      });
      // Then settle to a bright steady
      gsap.to(material, { opacity: 0.9, duration: 0.8, delay: 0.4, ease: 'expo.out' });
    }
  }, [currentAct, gridPos, material, onConvergenceComplete]);

  // Frame loop
  useFrame((_, delta) => {
    if (!meshRef.current) return;
    clock.current += delta;
    const t = clock.current;
    const act = actRef.current;

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const px = livePos.current[i * 3];
      const py = livePos.current[i * 3 + 1];
      const pz = livePos.current[i * 3 + 2];

      if (act === ACTS.VOID) {
        const { speed, phase } = noise[i];
        dummy.position.set(
          px + Math.sin(t * speed + phase) * 0.12,
          py + Math.cos(t * speed * 0.9 + phase) * 0.10,
          pz + Math.sin(t * 0.4 + phase) * 0.06
        );
        dummy.scale.setScalar(0.8 + Math.sin(t * speed + phase) * 0.2);
      } else {
        dummy.position.set(px, py, pz);
        dummy.scale.setScalar(1);
      }

      dummy.updateMatrix();
      meshRef.current.setMatrixAt(i, dummy.matrix);
    }
    meshRef.current.instanceMatrix.needsUpdate = true;

    // Group rotation
    if (act === ACTS.VOID) {
      meshRef.current.rotation.y = t * 0.018;
      meshRef.current.rotation.x = Math.sin(t * 0.007) * 0.15;
    } else if (act === ACTS.CONVERGENCE) {
      meshRef.current.rotation.y += 0.035 * delta * 60;
      meshRef.current.rotation.x += 0.008 * delta * 60;
    } else {
      // Smooth halt via lerp
      meshRef.current.rotation.y = THREE.MathUtils.lerp(meshRef.current.rotation.y, Math.PI / 6, 0.04);
      meshRef.current.rotation.x = THREE.MathUtils.lerp(meshRef.current.rotation.x, Math.PI / 12, 0.04);
    }
  });

  return <instancedMesh ref={meshRef} args={[geometry, material, PARTICLE_COUNT]} frustumCulled={false} />;
};

// ─── Camera Rig ─────────────────────────────────────────────────────────────
interface CameraRigProps {
  currentAct: Act;
}

const CameraRig: React.FC<CameraRigProps> = ({ currentAct }) => {
  const { camera } = useThree();

  useEffect(() => {
    if (currentAct === ACTS.VOID) {
      camera.position.set(0, 0, 9);
      gsap.to(camera.position, { z: 6.5, duration: 14, ease: 'none' });
    } else if (currentAct === ACTS.CONVERGENCE) {
      gsap.killTweensOf(camera.position);
      gsap.to(camera.position, { x: 2.5, y: 1.2, z: 5, duration: 4.5, ease: 'power4.inOut' });
    } else if (currentAct === ACTS.INSIGHT) {
      gsap.killTweensOf(camera.position);
      // Snap zoom — hard and precise
      gsap.to(camera.position, { x: 0, y: 0, z: 2.5, duration: 1.1, ease: 'expo.out' });
    }
  }, [currentAct, camera]);

  useFrame(() => {
    if (currentAct !== ACTS.INSIGHT) {
      camera.lookAt(0, 0, 0);
    } else {
      camera.lookAt(0, 0, 0);
    }
  });

  return null;
};

// ─── Main Component ─────────────────────────────────────────────────────────
interface CinematicIntroProps {
  onSequenceComplete: () => void;
}

export default function CinematicIntro({ onSequenceComplete }: CinematicIntroProps) {
  const [currentAct, setCurrentAct] = useState<Act>(ACTS.VOID);

  const handleConvergenceComplete = useCallback(() => {
    setCurrentAct(ACTS.INSIGHT);
    // Signal HeroSection text to appear shortly after the snap-zoom lands
    setTimeout(onSequenceComplete, 400);
  }, [onSequenceComplete]);

  useEffect(() => {
    // Begin Act 2 after void ambient phase
    const t = setTimeout(() => setCurrentAct(ACTS.CONVERGENCE), 2800);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="absolute inset-0 -z-10 h-full w-full overflow-hidden pointer-events-none"
      style={{ background: '#2B2B2B' }}>
      <Canvas
        camera={{ fov: 60, near: 0.1, far: 100 }}
        gl={{ antialias: true, alpha: false }}
        dpr={Math.min(window.devicePixelRatio, 2)}
      >
        <CameraRig currentAct={currentAct} />
        <Swarm currentAct={currentAct} onConvergenceComplete={handleConvergenceComplete} />
      </Canvas>
    </div>
  );
}
