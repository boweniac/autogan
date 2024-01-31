import React, { useEffect, useRef } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js'
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { Position, animateMorphTargets } from './AvatarUtil';
import { animationNameToPath } from './AnimationConfig';
import { avatarConfig, corresponding, nodeKeyToIndex } from './AvatarConfig';


type GLBModelProps = {
  avatarName: string; // 模型文件的路径
  animations: string[]; // FBX 动画文件路径
  position: Position | undefined;
};


const GLBLoopModel: React.FC<GLBModelProps> = ({ avatarName, animations, position }) => {
    const gltf = useLoader(GLTFLoader, avatarConfig[avatarName].modelPath);

    // eslint-disable-next-line react-hooks/rules-of-hooks
    const fbxs = animations.map((animation)=>useLoader(FBXLoader, animationNameToPath[animation]))
    const mixer = useRef<THREE.AnimationMixer>();
    const currentAnimationIndex = useRef(0);
    

    const animationPlay = (index: number) => {
      if (gltf.scene && fbxs[index].animations[0]) {
        mixer.current = new THREE.AnimationMixer(gltf.scene);
        const action = mixer.current.clipAction(fbxs[index].animations[0]);

        // action.setLoop(THREE.LoopOnce, 1);
        
        action.play();
    }
    }

    useEffect(() => {
      if (gltf.scene) {
          if (position) {
            gltf.scene.position.set(position.x, position.y, position.z);
            gltf.scene.rotation.y = position.rotation;
          }
      }
      animationPlay(currentAnimationIndex.current)
  }, [gltf, fbxs]);

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
          animationPlay(currentAnimationIndex.current)
        }
    }
});

    return <primitive object={gltf.scene} />;
};

export default GLBLoopModel;