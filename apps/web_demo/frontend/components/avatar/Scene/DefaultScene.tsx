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
  avatarName: string; // 模型文件的路径
  audioAndLip: AudioAndLip | undefined;
  audioEndCallback: ()=>void;
  isReadyCallback?: ()=>void;
};

// const CameraController = () => {
//   const { camera, gl } = useThree();

//   useEffect(() => {
//       camera.position.set(0, 1.5, 1); // 设置摄像机的初始位置
//       camera.near = 0.1; // 调整近裁剪面
//       camera.far = 1; // 调整远裁剪面
//       camera.updateProjectionMatrix(); // 更新摄像机的投影矩阵
//       // camera.lookAt(3, 3, 3); // 设置摄像机的初始朝向
//   }, [camera]);

//   return <OrbitControls args={[camera, gl.domElement]} target={[0, 1.5, 0]} />;
// };

// const CameraController = () => {
//   const { gl, size } = useThree();
//   const [camera] = useState(() => new THREE.OrthographicCamera(
//     size.width / -2, 
//     size.width / 2, 
//     size.height / 2, 
//     size.height / -2, 
//     1, 
    
//   ));

//   useEffect(() => {
//     // camera.position.set(50, 50, 10);
//     // camera.lookAt(4, -3, 1);
//     camera.updateProjectionMatrix();
//   }, [camera, size]);

//   return <OrbitControls args={[camera, gl.domElement]}/>;
// };

// const CameraController = () => {
//   const { camera, gl } = useThree();

//   useEffect(() => {
//       camera.position.set(0, 1.5, 1); // 设置摄像机的初始位置
//   }, [camera]);

//   return <OrbitControls args={[camera, gl.domElement]} target={[0, 1.5, 0]} />;
// };

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

const DefaultScene: React.FC<DefaultSceneProps> = ({ avatarName, audioAndLip, audioEndCallback, isReadyCallback }) => {
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
        <GLBModel avatarName={avatarName} animation="Idle" position={position} audioAndLip={audioAndLip} audioEndCallback={audioEndCallback} />
        <CameraController  />
      </Canvas>
    </div>
  );
};

export default DefaultScene;