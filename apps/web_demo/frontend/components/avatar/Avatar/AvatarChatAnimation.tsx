import React, { useEffect, useRef } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js'
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { AudioAndLip, MouthCues } from '@/stores/TypeAudioAndLip';
import { Position, animateMorphTargets } from './AvatarUtil';
import { animationNameToPath } from './AnimationConfig';
import { avatarConfig, corresponding, nodeKeyToIndex } from './AvatarConfig';
import { useRouter } from 'next/router';


type GLBModelProps = {
  avatarName: string; // 模型文件的路径
  animation: string; // FBX 动画文件路径
  position: Position | undefined;
  audioAndLip: AudioAndLip | undefined;
  audioEndCallback: ()=>void
  isReadyCallback?: ()=>void
};


const GLBModel: React.FC<GLBModelProps> = ({ avatarName, animation, position, audioAndLip, audioEndCallback }) => {
  const router = useRouter();
    const gltf = useLoader(GLTFLoader, avatarConfig[avatarName].modelPath);
    const headNode = gltf.scene.getObjectByName('Wolf3D_Head');
    const teethNode = gltf.scene.getObjectByName('Wolf3D_Teeth');

    // eslint-disable-next-line react-hooks/rules-of-hooks
    const fbx = useLoader(FBXLoader, animationNameToPath[animation]);
    // const fbxs = animations.map((animation)=>useLoader(FBXLoader, animationNameToPath[animation]))
    const mixer = useRef<THREE.AnimationMixer>();
    const oldMorphTargetIndex = useRef(0);
    const currentMorphTargetIndex = useRef(0);
    const currentAnimationIndex = useRef(0);
    new Audio(``)

    useEffect(() => {
      const handleLoad = () => {
          if (typeof window !== 'undefined') {
            console.log(`1234567890987654321234567890`);
          }
      };
  
      if (router.isReady) {
          window.addEventListener('load', handleLoad);
      }
  
      return () => {
          window.removeEventListener('load', handleLoad);
      };
  }, [router.isReady]);

    useEffect(()=>{
      console.log(`audioAndLip.audioFile1:`+JSON.stringify(audioAndLip?.audioFile));
      if (audioAndLip) {
        console.log(`audioAndLip.audioFile2:`+JSON.stringify(audioAndLip.audioFile));
        const audio = new Audio(`${audioAndLip.audioFile}`)
        audio.play().catch(error => {
          audioEndCallback()
        });
        const handleTimeUpdate = () => {
          const currentTime = audio.currentTime;
          console.log(`currentTime:`+JSON.stringify(currentTime));
          for (let i = 0; i < audioAndLip.lipsData.length; i++) {
            const lipsData = audioAndLip.lipsData[i] as MouthCues;
            if (currentTime >= lipsData.start && currentTime <= lipsData.end) {
              console.log(`lipsData.value:`+JSON.stringify(lipsData.value));
              currentMorphTargetIndex.current = nodeKeyToIndex[corresponding[lipsData.value]]
              animateMorphTargets(performance.now(), updateMorphTargets)
              break
            }
          }
        };
        audio.ontimeupdate = () => {
          handleTimeUpdate();
        };
        audio.addEventListener('ended', () => {
          currentMorphTargetIndex.current = 0
          updateMorphTargets(1)
          audioEndCallback()
        });
      }
    }, [audioAndLip])
    

    const updateMorphTargets = (ratio: number) => {
      if (headNode instanceof THREE.Mesh && headNode.morphTargetInfluences) {
        headNode.morphTargetInfluences[oldMorphTargetIndex.current] = 1-ratio;
        headNode.morphTargetInfluences[currentMorphTargetIndex.current] = ratio;
      }
      
      if (teethNode instanceof THREE.Mesh && teethNode.morphTargetInfluences) {
        teethNode.morphTargetInfluences[oldMorphTargetIndex.current] = 1-ratio;
          teethNode.morphTargetInfluences[currentMorphTargetIndex.current] = ratio;
      }

      if (ratio == 1) {
        oldMorphTargetIndex.current = currentMorphTargetIndex.current
      }
    };

    const animationPlay = () => {
      if (gltf.scene && fbx.animations[0]) {
        mixer.current = new THREE.AnimationMixer(gltf.scene);
        const action = mixer.current.clipAction(fbx.animations[0]);

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
      animationPlay()
  }, [gltf, fbx]);

  useFrame((state, delta) => {
    mixer.current?.update(delta);
    // if (mixer.current) {
    //     mixer.current.update(delta);
    //     const action = mixer.current.existingAction(fbx.animations[0]);
        
    //     if (action && action.time >= action.getClip().duration-0.1) {
    //       if (currentAnimationIndex.current == fbxs.length-1) {
    //         currentAnimationIndex.current = 0
    //       } else {
    //         currentAnimationIndex.current += 1
    //       }
    //       animationPlay(currentAnimationIndex.current)
    //     }
    // }
});

    return <primitive object={gltf.scene} />;
};

export default GLBModel;