import React, { useEffect, useRef } from 'react';
import { ObjectMap, useFrame, useLoader } from '@react-three/fiber';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js'
import * as THREE from 'three';
import { GLTF, GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { Position, animateMorphTargets } from './AvatarUtil';
import { animationNameToPath } from './AnimationConfig';
import { avatarConfig, corresponding, nodeKeyToIndex } from './AvatarConfig';


type GLBModelProps = {
  avatarName: string; // 模型文件的路径
  animations: string[]; // FBX 动画文件路径
  position: Position | undefined;
  animationPlayEndCallback?: ()=>void
};


const GLBLoopModel: React.FC<GLBModelProps> = ({ avatarName, animations, position, animationPlayEndCallback }) => {
  const gltfs:{[key: string]: GLTF & ObjectMap} = {
    "customerManagerBoy": useLoader(GLTFLoader, avatarConfig["customerManagerBoy"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "customerManagerGirl": useLoader(GLTFLoader, avatarConfig["customerManagerGirl"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "coder": useLoader(GLTFLoader, avatarConfig["coder"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "documentExp": useLoader(GLTFLoader, avatarConfig["documentExp"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "searchExpert": useLoader(GLTFLoader, avatarConfig["searchExpert"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "secretary": useLoader(GLTFLoader, avatarConfig["secretary"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "tester": useLoader(GLTFLoader, avatarConfig["tester"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
  }
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const fbxs = animations.map((animation)=>useLoader(FBXLoader, animationNameToPath[animation]))
    const mixer = useRef<THREE.AnimationMixer>();
    const currentAnimationIndex = useRef(0);
    

    const animationPlay = (index: number) => {
      if (gltfs[avatarName].scene && fbxs[index].animations[0]) {
        mixer.current = new THREE.AnimationMixer(gltfs[avatarName].scene);
        const action = mixer.current.clipAction(fbxs[index].animations[0]);

        // action.setLoop(THREE.LoopOnce, 1);
        
        action.play();
    }
    }

    useEffect(() => {
      if (gltfs[avatarName].scene) {
          if (position) {
            gltfs[avatarName].scene.position.set(Number(position.x), Number(position.y), Number(position.z));
            gltfs[avatarName].scene.rotation.y = Number(position.rotation);
          }
      }
      animationPlay(currentAnimationIndex.current)
  }, [gltfs[avatarName], fbxs]);

  useFrame((state, delta) => {
    if (mixer.current) {
        mixer.current.update(delta);
        const action = mixer.current.existingAction(fbxs[currentAnimationIndex.current].animations[0]);
        
        if (action && action.time >= action.getClip().duration-0.1) {
          if (currentAnimationIndex.current == fbxs.length-1) {
            currentAnimationIndex.current = 0
          } else {
            currentAnimationIndex.current += 1
          }
          if (animationPlayEndCallback) {
            animationPlayEndCallback()
          }
          animationPlay(currentAnimationIndex.current)
        }
    }
});

    return <primitive object={gltfs[avatarName].scene} />;
};

export default GLBLoopModel;