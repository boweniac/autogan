import React, { useEffect, useRef } from 'react';
import { ObjectMap, useFrame, useLoader } from '@react-three/fiber';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js'
import * as THREE from 'three';
import { GLTF, GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
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
  audioEndCallback?: ()=>void
  isReadyCallback?: ()=>void
};


const GLBModel: React.FC<GLBModelProps> = ({ avatarName, animation, position, audioAndLip, audioEndCallback }) => {
  console.log(`position:`+JSON.stringify(position));
  const router = useRouter();
  const gltfs:{[key: string]: GLTF & ObjectMap} = {
    "customerManagerBoy": useLoader(GLTFLoader, avatarConfig["customerManagerBoy"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "customerManagerGirl": useLoader(GLTFLoader, avatarConfig["customerManagerGirl"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "coder": useLoader(GLTFLoader, avatarConfig["coder"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "documentExp": useLoader(GLTFLoader, avatarConfig["documentExp"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "searchExpert": useLoader(GLTFLoader, avatarConfig["searchExpert"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "secretary": useLoader(GLTFLoader, avatarConfig["secretary"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
    "tester": useLoader(GLTFLoader, avatarConfig["tester"]["modelPath"] || "/avatars/CustomerManagerBoy.glb"),
  }
    // const gltf = useLoader(GLTFLoader, avatarConfig[avatarName].modelPath);
    const headNode = gltfs[avatarName].scene.getObjectByName('Wolf3D_Head');
    const teethNode = gltfs[avatarName].scene.getObjectByName('Wolf3D_Teeth');

    // eslint-disable-next-line react-hooks/rules-of-hooks
    const fbx = useLoader(FBXLoader, animationNameToPath[animation]);
    // const fbxs = animations.map((animation)=>useLoader(FBXLoader, animationNameToPath[animation]))
    const mixer = useRef<THREE.AnimationMixer>();
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
          if (audioEndCallback) {
            audioEndCallback()
          }
        });
        const handleTimeUpdate = () => {
          const currentTime = audio.currentTime;
          console.log(`currentTime:`+JSON.stringify(currentTime));
          for (let i = 0; i < audioAndLip.lipsData.length; i++) {
            const lipsData = audioAndLip.lipsData[i] as MouthCues;
            if (currentTime >= lipsData.start && currentTime <= lipsData.end) {
              currentMorphTargetIndex.current = nodeKeyToIndex[corresponding[lipsData.value]]
              animateMorphTargets(performance.now(), updateMorphTargets)
              if (headNode instanceof THREE.Mesh && headNode.morphTargetInfluences) {
                headNode.morphTargetInfluences[currentMorphTargetIndex.current] = 0;
              }
              break
            }
          }
        };
        audio.ontimeupdate = () => {
          handleTimeUpdate();
        };
        audio.addEventListener('ended', () => {
          // currentMorphTargetIndex.current = 0
          // updateMorphTargets(1)
          if (audioEndCallback) {
            audioEndCallback()
          }
        });
      }
    }, [audioAndLip])
    

    const updateMorphTargets = (ratio: number) => {
      ratio = ratio * 2
      if (headNode instanceof THREE.Mesh && headNode.morphTargetInfluences) {
        if (ratio <=1) {
          headNode.morphTargetInfluences[currentMorphTargetIndex.current] = ratio;
        } else {
          headNode.morphTargetInfluences[currentMorphTargetIndex.current] = 2-ratio;
        }
      }
      
      if (teethNode instanceof THREE.Mesh && teethNode.morphTargetInfluences) {
        if (ratio <=1) {
          teethNode.morphTargetInfluences[currentMorphTargetIndex.current] = ratio;
        } else {
          teethNode.morphTargetInfluences[currentMorphTargetIndex.current] = 2-ratio;
        }
      }
    };

    const animationPlay = () => {
      if (gltfs[avatarName].scene && fbx.animations[0]) {
        mixer.current = new THREE.AnimationMixer(gltfs[avatarName].scene);
        const action = mixer.current.clipAction(fbx.animations[0]);

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
      animationPlay()
  }, [gltfs[avatarName], fbx]);

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

    return <primitive object={gltfs[avatarName].scene} />;
};

export default GLBModel;