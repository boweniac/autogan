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

// extend({ OrbitControls });
type HelloSceneConfigProps = {
  avatarName: string; // 模型文件的路径
  setAvatarNamecallback: (value: string)=>void;
  setAvatarcallback: (avatar: AvatarObject)=>void;
}

const HelloSceneConfig: React.FC<HelloSceneConfigProps> = ({ avatarName, setAvatarNamecallback, setAvatarcallback}) => {
  const avatarObject = avatarConfig[avatarName]
  const [avatar, setAvatar] = useState<AvatarObject>(avatarObject);
  const [positionX, setPositionX] = useState<string | number>(avatar.positionX || 0);
  const [positionY, setPositionY] = useState<string | number>(avatar.positionY || 0);
  const [positionZ, setPositionZ] = useState<string | number>(avatar.positionZ || 0);
  const [positionRotation, setPositionRotation] = useState<string | number>(avatar.positionRotation || 0);
  const [ambientLightIntensity, setAmbientLightIntensity] = useState<string | number>(avatar.ambientLightIntensity || 0);
  const [pointLightX, setPointLightX] = useState<string | number>(avatar.pointLightX || 0);
  const [pointLightY, setPointLightY] = useState<string | number>(avatar.pointLightY || 0);
  const [pointLightZ, setPointLightZ] = useState<string | number>(avatar.pointLightZ || 0);
  const [pointLightIntensity, setPointLightIntensity] = useState<string | number>(avatar.pointLightIntensity || 0);
  const [fov, setFov] = useState<string | number>(avatar.fov || 0);
  const [cameraPositionX, setCameraPositionX] = useState<string | number>(avatar.cameraPositionX || 0);
  const [cameraPositionY, setCameraPositionY] = useState<string | number>(avatar.cameraPositionY || 0);
  const [cameraPositionZ, setCameraPositionZ] = useState<string | number>(avatar.cameraPositionZ || 0);
  const [lookAtPositionX, setLookAtPositionX] = useState<string | number>(avatar.lookAtPositionX || 0);
  const [lookAtPositionY, setLookAtPositionY] = useState<string | number>(avatar.lookAtPositionY || 0);
  const [lookAtPositionZ, setLookAtPositionZ] = useState<string | number>(avatar.lookAtPositionZ || 0);
  const [targetX, setTargetX] = useState<string | number>(avatar.targetX || 0);
  const [targetY, setTargetY] = useState<string | number>(avatar.targetY || 0);
  const [targetZ, setTargetZ] = useState<string | number>(avatar.targetZ || 0);
  const [name, setName] = useState<string>(avatarName);

  useEffect(() => {
    setName(avatarName)
    setAvatar(avatarConfig[name])
}, [avatarName]);

  const updateAvatar = (value: AvatarObject)=>{
    const data: AvatarObject = {
      ...avatar,
      ...value
    }
    setAvatar(data)
    setAvatarcallback(data)
    return data
  }

  // useEffect(() => {
  //   setAvatarNamecallback(avatarName)
  // }, [avatarName]);

  // useEffect(() => {
  //   setAvatarcallback(avatarObject)
  // }, [avatarObject]);

  return (
    <ScrollArea h={`calc(100vh)`} style={{width: rem(200), position: 'fixed', zIndex: 2}}>
        <SegmentedControl orientation="vertical" defaultValue={avatarName} value={name} data={['customerManagerBoy', 'customerManagerGirl', 'coder', 'documentExp', 'searchExpert', 'secretary', 'tester']} onChange={(v)=>{
          setAvatarNamecallback(v)
          setName(v)
          }} />
        <NumberInput size="xs" label="positionX" value={avatar.positionX} onChange={(v)=>{updateAvatar({"positionX": v})}}/>
        <NumberInput size="xs" label="positionY" value={avatar.positionY} onChange={(v)=>{updateAvatar({"positionY": v})}}/>
        <NumberInput size="xs" label="positionZ" value={avatar.positionZ} onChange={(v)=>{updateAvatar({"positionZ": v})}}/>
        <NumberInput size="xs" label="positionRotation" value={avatar.positionRotation} onChange={(v)=>{updateAvatar({"positionRotation": v})}}/>
        <NumberInput size="xs" label="ambientLightIntensity" value={avatar.ambientLightIntensity} onChange={(v)=>{updateAvatar({"ambientLightIntensity": v})}}/>
        <NumberInput size="xs" label="pointLightX" value={avatar.pointLightX} onChange={(v)=>{updateAvatar({"pointLightX": v})}}/>
        <NumberInput size="xs" label="pointLightY" value={avatar.pointLightY} onChange={(v)=>{updateAvatar({"pointLightY": v})}}/>
        <NumberInput size="xs" label="pointLightZ" value={avatar.pointLightZ} onChange={(v)=>{updateAvatar({"pointLightZ": v})}}/>
        <NumberInput size="xs" label="pointLightIntensity" value={avatar.pointLightIntensity} onChange={(v)=>{updateAvatar({"pointLightIntensity": v})}}/>
        <NumberInput size="xs" label="fov" value={avatar.fov} onChange={(v)=>{updateAvatar({"fov": v})}}/>
        <NumberInput size="xs" label="cameraPositionX" value={avatar.cameraPositionX} onChange={(v)=>{updateAvatar({"cameraPositionX": v})}}/>
        <NumberInput size="xs" label="cameraPositionY" value={avatar.cameraPositionY} onChange={(v)=>{updateAvatar({"cameraPositionY": v})}}/>
        <NumberInput size="xs" label="cameraPositionZ" value={avatar.cameraPositionZ} onChange={(v)=>{updateAvatar({"cameraPositionZ": v})}}/>
        <NumberInput size="xs" label="lookAtPositionX" value={avatar.lookAtPositionX} onChange={(v)=>{updateAvatar({"lookAtPositionX": v})}}/>
        <NumberInput size="xs" label="lookAtPositionY" value={avatar.lookAtPositionY} onChange={(v)=>{updateAvatar({"lookAtPositionY": v})}}/>
        <NumberInput size="xs" label="lookAtPositionZ" value={avatar.lookAtPositionZ} onChange={(v)=>{updateAvatar({"lookAtPositionZ": v})}}/>
        <NumberInput size="xs" label="targetX" value={avatar.targetX} onChange={(v)=>{updateAvatar({"targetX": v})}}/>
        <NumberInput size="xs" label="targetY" value={avatar.targetY} onChange={(v)=>{updateAvatar({"targetY": v})}}/>
        <NumberInput size="xs" label="targetZ" value={avatar.targetZ} onChange={(v)=>{updateAvatar({"targetZ": v})}}/>
        </ScrollArea>
  );
};

export default HelloSceneConfig;