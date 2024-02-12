import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, extend, useFrame, useLoader, useThree } from '@react-three/fiber';
import { useGLTF, PerspectiveCamera, useFBX, useAnimations, OrbitControls } from '@react-three/drei';
import { AudioAndLip, MouthCues } from '@/stores/TypeAudioAndLip';
import * as THREE from 'three';
import { Position } from '../Avatar/AvatarUtil';
import { animationGroup } from '../Avatar/AnimationConfig';
import GLBModel from '../Avatar/AvatarChatAnimation';

// extend({ OrbitControls });
type DefaultSceneProps = {
  audioAndLip: AudioAndLip | undefined;
  audioEndCallback: ()=>void;
  isReadyCallback?: ()=>void;
};


const CameraController = () => {
  const { gl, size } = useThree();
  const [camera] = useState(() => new THREE.PerspectiveCamera(80, 0, 0.1, 3));

  useEffect(() => {
    camera.fov = 180
    camera.aspect = size.width / size.height;
    // camera.lookAt(4, -3, 1);
    camera.updateProjectionMatrix();
  }, [camera, size]);

  return <OrbitControls args={[camera, gl.domElement]}/>;
};

const DefaultScene: React.FC<DefaultSceneProps> = ({ audioAndLip, audioEndCallback, isReadyCallback }) => {
  const [morphValue, setMorphValue] = useState<string>("");
  const position = {
    "x": 0,
    "y": -1.3,
    "z": 4.2,
    "rotation": -0.3
  }
  return (
    <div style={{height: "100%", width: "100%"}}>
      <Canvas gl={{ alpha: true }}>
        <ambientLight  intensity={4}/>
        <pointLight position={[0, 2, 3]} intensity={20} />
        <GLBModel animation="Idle" position={position} audioAndLip={audioAndLip} audioEndCallback={audioEndCallback} />
        <CameraController  />
      </Canvas>
    </div>
  );
};

export default DefaultScene;