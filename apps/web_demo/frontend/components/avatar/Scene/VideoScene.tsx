import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, extend, useFrame, useLoader, useThree } from '@react-three/fiber';
import { useGLTF, PerspectiveCamera, useFBX, useAnimations, OrbitControls } from '@react-three/drei';
import { AudioAndLip, MouthCues } from '@/stores/TypeAudioAndLip';
import * as THREE from 'three';
import { Position } from '../Avatar/AvatarUtil';
import { animationGroup } from '../Avatar/AnimationConfig';
import GLBModel from '../Avatar/AvatarChatAnimation';
import GLBLoopModel from '../Avatar/AvatarLoopAnimation';
import { Slider, Space, rem, Text, NumberInput, ScrollArea, SegmentedControl } from '@mantine/core';
import { AvatarObject, avatarConfig } from '../Avatar/AvatarConfig';
import HelloSceneConfig from './HelloSceneConfig';

// extend({ OrbitControls });
type VideoSceneSceneProps = {
  avatarName?: string; // 模型文件的路径
  animation: string 
  test?: boolean;
  audioAndLip?: AudioAndLip | undefined;
  audioEndCallback?: ()=>void;
  animationPlayEndCallback?: ()=>void
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

const VideoScene: React.FC<VideoSceneSceneProps> = ({ avatarName, animation, test, audioAndLip,  audioEndCallback, animationPlayEndCallback}) => {
  const avatarObject = avatarConfig[audioAndLip?.avatarName || avatarName || "customerManagerGirl"]
  const [avatar, setAvatar] = useState<AvatarObject>(avatarObject);
  const [name, setName] = useState<string>(audioAndLip?.avatarName || avatarName || "customerManagerGirl");
  const animations = animationGroup[animation]

  useEffect(() => {
    setName(audioAndLip?.avatarName || avatarName || "customerManagerGirl")
}, [avatarName, audioAndLip]);

useEffect(() => {
  setAvatar(avatarConfig[name])
}, [name]);
  return (
    <div style={{height: "100%", width: "100%"}}>
      {test && <HelloSceneConfig avatarName={name} setAvatarNamecallback={(v)=>{setName(v)}} setAvatarcallback={setAvatar}></HelloSceneConfig>}
      <Canvas gl={{ alpha: true }}>
        <ambientLight  intensity={Number(avatar.ambientLightIntensity || 0)}/>
        <pointLight position={[Number(avatar.pointLightX || 3), Number(avatar.pointLightY || 3), Number(avatar.pointLightZ || 3)]} intensity={Number(avatar.pointLightIntensity || 3)} />
        {animations.length == 1 ? <GLBLoopModel avatarName={avatarName || ""} animations={animations} position={{"x": avatar.positionX || 0, "y": avatar.positionY || 0, "z": avatar.positionZ || 0, "rotation": avatar.positionRotation || 0}} animationPlayEndCallback={animationPlayEndCallback} /> : <GLBModel animation={animations[0]} position={{"x": avatar.positionX || 0, "y": avatar.positionY || 0, "z": avatar.positionZ || 0, "rotation": avatar.positionRotation || 0}} audioAndLip={audioAndLip} audioEndCallback={audioEndCallback} />}
        <CameraController 
            fov={Number(avatar.fov || 0)} 
            // cameraPositionX={Number(3)} 
            // cameraPositionY={Number(1.3)} 
            // cameraPositionZ={Number(2.5)} 
            cameraPositionX={Number(avatar.cameraPositionX || 0)} 
            cameraPositionY={Number(avatar.cameraPositionY || 0)} 
            cameraPositionZ={Number(avatar.cameraPositionZ || 0)} 
            lookAtPositionX={Number(avatar.lookAtPositionX || 0)} 
            lookAtPositionY={Number(avatar.lookAtPositionY || 0)} 
            lookAtPositionZ={Number(avatar.lookAtPositionZ || 0)} 
            targetX={Number(avatar.targetX || 0)} 
            targetY={Number(avatar.targetY || 0)} 
            targetZ={Number(avatar.targetZ || 0)} />
      </Canvas>
    </div>
  );
};

export default VideoScene;