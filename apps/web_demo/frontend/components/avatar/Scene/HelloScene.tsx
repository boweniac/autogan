import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, extend, useFrame, useLoader, useThree } from '@react-three/fiber';
import { useGLTF, PerspectiveCamera, useFBX, useAnimations, OrbitControls } from '@react-three/drei';
import { AudioAndLip, MouthCues } from '@/stores/TypeAudioAndLip';
import * as THREE from 'three';
import { Position } from '../Avatar/AvatarUtil';
import { animationGroup } from '../Avatar/AnimationConfig';
import GLBModel from '../Avatar/AvatarChatAnimation';
import GLBLoopModel from '../Avatar/AvatarLoopAnimation';
import { Slider, Space, rem, Text, NumberInput } from '@mantine/core';

// extend({ OrbitControls });
type HelloSceneProps = {
  avatarName: string; // 模型文件的路径
  test?: boolean
};

type CameraControllerProps = {
  fov: number;
  cameraPositionX: number;
  cameraPositionY: number;
  cameraPositionZ: number;
  lookAtPositionX: number;
  lookAtPositionY: number;
  lookAtPositionZ: number;
  targetX: number;
  targetY: number;
  targetZ: number;
}

const CameraController = (props: CameraControllerProps) => {
  const { camera, gl } = useThree();

  useEffect(() => {
      camera.position.set(props.cameraPositionX, props.cameraPositionY, props.cameraPositionZ); // 设置摄像机的初始位置
      camera.near = 0.1; // 调整近裁剪面
      camera.far = 30; // 调整远裁剪面
      camera.updateProjectionMatrix(); // 更新摄像机的投影矩阵
      camera.lookAt(props.lookAtPositionX, props.lookAtPositionY, props.lookAtPositionZ); // 设置摄像机的初始朝向
  }, [camera, props]);

  return <OrbitControls args={[camera, gl.domElement]} target={[props.targetX, props.targetY, props.targetZ]} />;
};

// const CameraController = (props: CameraControllerProps) => {
//   const { gl, size } = useThree();
//   const [camera] = useState(() => new THREE.OrthographicCamera(
//     size.width / -2, 
//     size.width / 2, 
//     size.height / 2, 
//     size.height / -2, 
//     1, 
    
//   ));

//   useEffect(() => {
//     camera.position.set(props.cameraPositionX, props.cameraPositionY, props.cameraPositionZ);
//     camera.lookAt(props.lookAtPositionX, props.lookAtPositionY, props.lookAtPositionZ);
//     camera.updateProjectionMatrix();
//   }, [camera, size, props]);

//   return <OrbitControls args={[camera, gl.domElement]} target={[props.targetX, props.targetY, props.targetZ]}/>;
// };

// const CameraController = (props: CameraControllerProps) => {
//   const { gl, size } = useThree();
//   const [camera] = useState(() => new THREE.PerspectiveCamera(80, 0, 0.1, 100));

//   useEffect(() => {
//     camera.fov = props.fov
//     camera.aspect = size.width / size.height;
//     camera.position.set(props.cameraPositionX, props.cameraPositionY, props.cameraPositionZ)
//     camera.lookAt(props.lookAtPositionX, props.lookAtPositionY, props.lookAtPositionZ);
//     camera.updateProjectionMatrix();
//   }, [camera, size, props]);

//   return <OrbitControls args={[camera, gl.domElement]} target={[props.targetX, props.targetY, props.targetZ]}/>;
// };

const HelloScene: React.FC<HelloSceneProps> = ({ avatarName, test }) => {
  const [positionX, setPositionX] = useState<string | number>(0);
  const [positionY, setPositionY] = useState<string | number>(0);
  const [positionZ, setPositionZ] = useState<string | number>(0);
  const [positionRotation, setPositionRotation] = useState<string | number>(0);
  const [ambientLightIntensity, setAmbientLightIntensity] = useState<string | number>(5);
  const [pointLightX, setPointLightX] = useState<string | number>(0);
  const [pointLightY, setPointLightY] = useState<string | number>(1);
  const [pointLightZ, setPointLightZ] = useState<string | number>(1);
  const [pointLightIntensity, setPointLightIntensity] = useState<string | number>(4);
  const [fov, setFov] = useState<string | number>(0);
  const [cameraPositionX, setCameraPositionX] = useState<string | number>(0);
  const [cameraPositionY, setCameraPositionY] = useState<string | number>(1.5);
  const [cameraPositionZ, setCameraPositionZ] = useState<string | number>(0.8);
  const [lookAtPositionX, setLookAtPositionX] = useState<string | number>(0);
  const [lookAtPositionY, setLookAtPositionY] = useState<string | number>(0);
  const [lookAtPositionZ, setLookAtPositionZ] = useState<string | number>(0);
  const [targetX, setTargetX] = useState<string | number>(0);
  const [targetY, setTargetY] = useState<string | number>(1.5);
  const [targetZ, setTargetZ] = useState<string | number>(0);
  const [morphValue, setMorphValue] = useState<string>("");
  const position = {
    "x": Number(positionX),
    "y": Number(positionY),
    "z": Number(positionZ),
    "rotation": Number(positionRotation)
  }
  return (
    <div style={{height: "100%", width: "100%"}}>
      {test && <div style={{width: rem(200), position: 'fixed', zIndex: 2}}>
        <Space h="xl" />
        {/* <Text size="sm">positionX</Text>
        <Slider value={positionX} onChange={setPositionX} /> */}
        <NumberInput size="xs" label="positionX" value={positionX} onChange={setPositionX}/>
        <NumberInput size="xs" label="positionY" value={positionY} onChange={setPositionY}/>
        <NumberInput size="xs" label="positionZ" value={positionZ} onChange={setPositionZ}/>
        <NumberInput size="xs" label="positionRotation" value={positionRotation} onChange={setPositionRotation}/>
        <NumberInput size="xs" label="ambientLightIntensity" value={ambientLightIntensity} onChange={setAmbientLightIntensity}/>
        <NumberInput size="xs" label="pointLightX" value={pointLightX} onChange={setPointLightX}/>
        <NumberInput size="xs" label="pointLightY" value={pointLightY} onChange={setPointLightY}/>
        <NumberInput size="xs" label="pointLightZ" value={pointLightZ} onChange={setPointLightZ}/>
        <NumberInput size="xs" label="pointLightIntensity" value={pointLightIntensity} onChange={setPointLightIntensity}/>
        <NumberInput size="xs" label="fov" value={fov} onChange={setFov}/>
        <NumberInput size="xs" label="cameraPositionX" value={cameraPositionX} onChange={setCameraPositionX}/>
        <NumberInput size="xs" label="cameraPositionY" value={cameraPositionY} onChange={setCameraPositionY}/>
        <NumberInput size="xs" label="cameraPositionZ" value={cameraPositionZ} onChange={setCameraPositionZ}/>
        <NumberInput size="xs" label="lookAtPositionX" value={lookAtPositionX} onChange={setLookAtPositionX}/>
        <NumberInput size="xs" label="lookAtPositionY" value={lookAtPositionY} onChange={setLookAtPositionY}/>
        <NumberInput size="xs" label="lookAtPositionZ" value={lookAtPositionZ} onChange={setLookAtPositionZ}/>
        <NumberInput size="xs" label="targetX" value={targetX} onChange={setTargetX}/>
        <NumberInput size="xs" label="targetY" value={targetY} onChange={setTargetY}/>
        <NumberInput size="xs" label="targetZ" value={targetZ} onChange={setTargetZ}/>
        </div>}
      <Canvas gl={{ alpha: true }}>
        <ambientLight  intensity={Number(ambientLightIntensity)}/>
        <pointLight position={[Number(pointLightX), Number(pointLightY), Number(pointLightZ)]} intensity={Number(pointLightIntensity)} />
        <GLBLoopModel avatarName={avatarName} animations={animationGroup["hello"]} position={position} />
        <CameraController 
            fov={Number(fov)} 
            cameraPositionX={Number(cameraPositionX)} 
            cameraPositionY={Number(cameraPositionY)} 
            cameraPositionZ={Number(cameraPositionZ)} 
            lookAtPositionX={Number(lookAtPositionX)} 
            lookAtPositionY={Number(lookAtPositionY)} 
            lookAtPositionZ={Number(lookAtPositionZ)} 
            targetX={Number(targetX)} 
            targetY={Number(targetY)} 
            targetZ={Number(targetZ)} />
      </Canvas>
    </div>
  );
};

export default HelloScene;