import React, { useRef, useMemo, useEffect, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { EffectComposer, DepthOfField } from '@react-three/postprocessing';
import * as THREE from 'three';
import gsap from 'gsap';

// ==========================================
// Act Structure & State Management
// ==========================================
const ACTS = {
  VOID: 0,
  CONVERGENCE: 1,
  INSIGHT: 2,
};

// ==========================================
// Geometry & Particle Management
// ==========================================
const PARTICLE_COUNT = 1500;

const ChoreographedSwarm = ({ currentAct, onActComplete }: { currentAct: number, onActComplete: () => void }) => {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const targetPositions = useRef<Float32Array>(new Float32Array(PARTICLE_COUNT * 3));
  const time = useRef(0);
  
  // Base Geometry (Tiny Shards)
  const geometry = useMemo(() => new THREE.IcosahedronGeometry(0.015, 0), []);
  const material = useMemo(() => new THREE.MeshBasicMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.4 }), []);

  // Initial Void State (Chaos)
  const [dummy] = useState(() => new THREE.Object3D());
  const initialData = useMemo(() => {
    const data = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      // Act 1: Random Sphere Volume (Void)
      const r = 4 * Math.cbrt(Math.random());
      const theta = Math.random() * 2 * Math.PI;
      const phi = Math.acos(2 * Math.random() - 1);
      
      const x = r * Math.sin(phi) * Math.cos(theta);
      const y = r * Math.sin(phi) * Math.sin(theta);
      const z = r * Math.cos(phi);

      // Act 3: The Structured Grid/Monument (Target)
      // Arrange into a sharp, geometric block (10x15x10 grid approximation)
      const side = Math.ceil(Math.cbrt(PARTICLE_COUNT));
      const spacing = 0.15;
      const gx = ((i % side) - side/2) * spacing;
      const gy = (Math.floor((i / side) % side) - side/2) * spacing;
      const gz = (Math.floor(i / (side * side)) - side/2) * spacing;

      data.push({
        x, y, z, // Void pos
        tx: gx, ty: gy, tz: gz, // Target Matrix pos
        speed: Math.random() * 0.5 + 0.1,
        axis: new THREE.Vector3(Math.random(), Math.random(), Math.random()).normalize(),
        progress: 0 // GSAP will animate this
      });
      targetPositions.current[i*3] = x;
      targetPositions.current[i*3+1] = y;
      targetPositions.current[i*3+2] = z;
    }
    return data;
  }, []);

  // Set initial instance matrices
  useEffect(() => {
    if (!meshRef.current) return;
    initialData.forEach((d, i) => {
      dummy.position.set(d.x, d.y, d.z);
      dummy.rotation.set(Math.random()*Math.PI, Math.random()*Math.PI, Math.random()*Math.PI);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  }, [dummy, initialData]);

  // Choreography Core
  useEffect(() => {
    if (currentAct === ACTS.CONVERGENCE) {
      // Act 2: Convergence (Snap fragments to grid)
      // GSAP aggressively interpolates progress from 0 -> 1
      initialData.forEach((d, i) => {
        gsap.to(d, {
          progress: 1,
          duration: 3 + Math.random() * 1.5, // Sweep effect
          ease: "power4.inOut",
          onUpdate: () => {
            // Interpolate position based on progress
            targetPositions.current[i*3] = THREE.MathUtils.lerp(d.x, d.tx, d.progress);
            targetPositions.current[i*3+1] = THREE.MathUtils.lerp(d.y, d.ty, d.progress);
            targetPositions.current[i*3+2] = THREE.MathUtils.lerp(d.z, d.tz, d.progress);
          }
        });
      });

      // Signal completion after longest animation
      setTimeout(() => {
        onActComplete();
      }, 4500);
    }
    
    if (currentAct === ACTS.INSIGHT) {
      // Act 3: Insight (Structure formed, ripple sent)
      // Material flash hack via opacity bump
      gsap.to(material, {
        opacity: 0.9,
        duration: 0.2,
        yoyo: true,
        repeat: 1,
        ease: "expo.out"
      });
    }
  }, [currentAct, initialData, material, onActComplete]);

  // Frame Loop
  useFrame((state, delta) => {
    if (!meshRef.current) return;
    time.current += delta;

    initialData.forEach((d, i) => {
      // Read target positions (either void static, or interpolating to grid)
      const px = targetPositions.current[i*3];
      const py = targetPositions.current[i*3+1];
      const pz = targetPositions.current[i*3+2];

      if (currentAct === ACTS.VOID) {
        // Act 1: Subtle floating drift
        dummy.position.set(
          px + Math.sin(time.current * d.speed + i) * 0.1,
          py + Math.cos(time.current * d.speed * 0.8 + i) * 0.1,
          pz + Math.sin(time.current * 0.5) * 0.05
        );
        dummy.rotation.x += 0.005;
        dummy.rotation.y += 0.005;
      } else if (currentAct === ACTS.CONVERGENCE) {
        // Act 2: Snapping into place (driven by GSAP lerping targetPositions)
        dummy.position.set(px, py, pz);
        // Align rotation aggressively
        dummy.quaternion.slerp(new THREE.Quaternion(), d.progress * 0.1); 
      } else {
        // Act 3: Locked Monument (Zero drift)
        dummy.position.set(px, py, pz);
        dummy.rotation.set(0,0,0);
      }

      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });

    meshRef.current.instanceMatrix.needsUpdate = true;
    
    // Group Rotation (Orbital effect)
    if (currentAct === ACTS.VOID) {
       meshRef.current.rotation.y = time.current * 0.02; // Very slow drift
    } else if (currentAct === ACTS.CONVERGENCE) {
       // Spin up during convergence
       meshRef.current.rotation.y += 0.04;
       meshRef.current.rotation.x += 0.01;
    } else {
       // Sharp halt onInsight, perfectly aligned
       gsap.to(meshRef.current.rotation, {
         x: Math.PI / 8, 
         y: Math.PI / 4, 
         z: 0, 
         duration: 1, 
         ease: "expo.out" 
       });
    }
  });

  return (
    <instancedMesh ref={meshRef} args={[geometry, material, PARTICLE_COUNT]} frustumCulled={false} />
  );
};

// ==========================================
// Camera & PostProcessing Rig
// ==========================================
const CameraRig = ({ currentAct }: { currentAct: number }) => {
  const { camera } = useThree();
  const dofRef = useRef<any>(null);

  useEffect(() => {
    if (!dofRef.current) return;
    
    if (currentAct === ACTS.VOID) {
      // Act 1: Macro Dolly-in, Heavy Bokeh
      camera.position.set(0, 0, 8);
      dofRef.current.focusDistance = 0.05;
      dofRef.current.focalLength = 0.1;
      dofRef.current.bokehScale = 12;

      // Slow dolly in
      gsap.to(camera.position, {
        z: 6,
        duration: 12, // Let it drift 
        ease: "none"
      });
    } 
    else if (currentAct === ACTS.CONVERGENCE) {
      // Act 2: Orbital Track & Rack focus
      gsap.killTweensOf(camera.position);
      
      // Pull focus sharply to center
      gsap.to(dofRef.current, {
        focusDistance: 0.1, // Center
        focalLength: 0.05,
        bokehScale: 2,
        duration: 3,
        ease: "power2.inOut"
      });

      // Pushing in while group spins creates orbital feel
      gsap.to(camera.position, {
        x: 2,
        y: 1,
        z: 4,
        duration: 4,
        ease: "power4.inOut"
      });
    }
    else if (currentAct === ACTS.INSIGHT) {
      // Act 3: Snap Zoom & Infinite DoF
      gsap.killTweensOf(camera.position);
      
      // Infinite DoF (Remove Bokeh)
      gsap.to(dofRef.current, {
        bokehScale: 0,
        duration: 0.5,
        ease: "expo.out"
      });

      // Hard Snap Zoom millimeters away
      gsap.to(camera.position, {
        x: 0,
        y: 0,
        z: 2.2, // Extremely tight
        duration: 1.2,
        ease: "expo.out"
      });
      
      // Look dead center perfectly aligned
      gsap.to(camera.rotation, {
        x: 0, y: 0, z: 0,
        duration: 0.5,
        ease: "expo.out"
      });
    }
  }, [currentAct, camera]);

  return (
    <EffectComposer>
      <DepthOfField 
        ref={dofRef} 
        focusDistance={0.05} 
        focalLength={0.1} 
        bokehScale={12} 
        height={480} 
      />
    </EffectComposer>
  );
};

// ==========================================
// Main Orchestrator Component
// ==========================================
export default function CinematicIntro({ onSequenceComplete }: { onSequenceComplete: () => void }) {
  const [currentAct, setCurrentAct] = useState(ACTS.VOID);

  useEffect(() => {
    // Orchestrate timeline
    // Act 1 (Void) starts immediately
    
    // Trigger Act 2 (Convergence) after ambient void phase
    const t1 = setTimeout(() => {
      setCurrentAct(ACTS.CONVERGENCE);
    }, 2500);

    return () => {
      clearTimeout(t1);
    };
  }, []);

  const handleConvergenceComplete = () => {
    // When Grid snaps together, enter Act 3
    setCurrentAct(ACTS.INSIGHT);
    
    // Signal UI to trigger Framer Motion text reveals
    setTimeout(() => {
      onSequenceComplete();
    }, 200); // Tiny delay for impact
  };

  return (
    <div className="absolute inset-0 -z-10 h-full w-full overflow-hidden pointer-events-none bg-[#2B2B2B]">
      <Canvas dpr={[1, 2]}>
        <CameraRig currentAct={currentAct} />
        <ChoreographedSwarm currentAct={currentAct} onActComplete={handleConvergenceComplete} />
      </Canvas>
    </div>
  );
}
