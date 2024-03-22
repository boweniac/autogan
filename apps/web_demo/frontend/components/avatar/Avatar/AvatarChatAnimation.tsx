import React, { useCallback, useEffect, useRef } from 'react';
import { ObjectMap, useFrame, useLoader } from '@react-three/fiber';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js'
import * as THREE from 'three';
import { GLTF, GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { AudioAndLip, MouthCues } from '@/stores/TypeAudioAndLip';
import { Position, animateMorphTargets } from './AvatarUtil';
import { animationNameToPath } from './AnimationConfig';
import { avatarConfig, corresponding, nodeKeyToIndex } from './AvatarConfig';
import { useRouter } from 'next/router';
import { getAudioState } from '@/stores/LocalStoreActions';
import { LocalState, localStore } from '@/stores/LocalStore';


type GLBModelProps = {
  animation: string; // FBX 动画文件路径
  position: Position | undefined;
  audioAndLip: AudioAndLip | undefined;
  audioEndCallback?: ()=>void
  isReadyCallback?: ()=>void
};


const GLBModel: React.FC<GLBModelProps> = ({ animation, position, audioAndLip, audioEndCallback }) => {
  const router = useRouter();
  const agentAvatarMapping = localStore((state: LocalState) => state.agentAvatarMapping);
  const avatarName = agentAvatarMapping["CustomerManager"]
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
    // const headNode = gltfs[avatarName].scene.getObjectByName('Wolf3D_Head');
    // const teethNode = gltfs[avatarName].scene.getObjectByName('Wolf3D_Teeth');

    const headNodes:{[key: string]: THREE.Object3D<THREE.Object3DEventMap> | THREE.Mesh<any, any, any> | undefined} = {
      "customerManagerBoy": gltfs["customerManagerBoy"].scene.getObjectByName('Wolf3D_Head'),
      "customerManagerGirl": gltfs["customerManagerGirl"].scene.getObjectByName('Wolf3D_Head'),
      "coder": gltfs["coder"].scene.getObjectByName('Wolf3D_Head'),
      "documentExp": gltfs["documentExp"].scene.getObjectByName('Wolf3D_Head'),
      "searchExpert": gltfs["searchExpert"].scene.getObjectByName('Wolf3D_Head'),
      "secretary": gltfs["secretary"].scene.getObjectByName('Wolf3D_Head'),
      "tester": gltfs["tester"].scene.getObjectByName('Wolf3D_Head'),
    }

    const teethNodes:{[key: string]: THREE.Object3D<THREE.Object3DEventMap> | THREE.Mesh<any, any, any> | undefined} = {
      "customerManagerBoy": gltfs["customerManagerBoy"].scene.getObjectByName('Wolf3D_Teeth'),
      "customerManagerGirl": gltfs["customerManagerGirl"].scene.getObjectByName('Wolf3D_Teeth'),
      "coder": gltfs["coder"].scene.getObjectByName('Wolf3D_Teeth'),
      "documentExp": gltfs["documentExp"].scene.getObjectByName('Wolf3D_Teeth'),
      "searchExpert": gltfs["searchExpert"].scene.getObjectByName('Wolf3D_Teeth'),
      "secretary": gltfs["secretary"].scene.getObjectByName('Wolf3D_Teeth'),
      "tester": gltfs["tester"].scene.getObjectByName('Wolf3D_Teeth'),
    }

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
          }
      };
  
      if (router.isReady) {
          window.addEventListener('load', handleLoad);
      }
  
      return () => {
          window.removeEventListener('load', handleLoad);
      };
  }, [router.isReady]);

  const onAudioEnded = useCallback(() => {
    if (audioEndCallback) {
      audioEndCallback();
    }
  }, [audioEndCallback]); 

    useEffect(()=>{
      const audio = getAudioState()
      if (audioAndLip?.audioFile && audio) {
        // const audio = new Audio()
        // const audio = new Audio(`${audioAndLip.audioFile}`)
        audio.src = `${audioAndLip.audioFile}`;
        audio.load();
        audio.play().catch(error => {
          console.log(`play.error:`+JSON.stringify(error));
          if (audioEndCallback) {
            onAudioEnded()
          }
        });
        const handleTimeUpdate = () => {
          if (audio.readyState >= 2) {
            const currentTime = audio.currentTime;
            if (audioAndLip.lipsData) {
              for (let i = 0; i < audioAndLip.lipsData.length; i++) {
                const lipsData = audioAndLip.lipsData[i] as MouthCues;
                if (currentTime >= lipsData.start && currentTime <= lipsData.end) {
                  currentMorphTargetIndex.current = nodeKeyToIndex[corresponding[lipsData.value]]
                  animateMorphTargets(performance.now(), updateMorphTargets)
                  const headNode = headNodes[audioAndLip.avatarName || avatarName]
                  if (headNode instanceof THREE.Mesh && headNode.morphTargetInfluences) {
                    headNode.morphTargetInfluences[currentMorphTargetIndex.current] = 0;
                  }
                  const teethNode = teethNodes[audioAndLip?.avatarName || avatarName]
                  if (teethNode instanceof THREE.Mesh && teethNode.morphTargetInfluences) {
                    teethNode.morphTargetInfluences[11] = 0;
                  }
                  break
                }
                const headNode = headNodes[audioAndLip.avatarName || avatarName]
                if (headNode instanceof THREE.Mesh && headNode.morphTargetInfluences) {
                  headNode.morphTargetInfluences[currentMorphTargetIndex.current] = 0;
                }
                const teethNode = teethNodes[audioAndLip?.avatarName || agentAvatarMapping["customerManagerGirl"]]
                if (teethNode instanceof THREE.Mesh && teethNode.morphTargetInfluences) {
                  teethNode.morphTargetInfluences[11] = 0;
                }
              }
            }
          }
        };
        audio.ontimeupdate = () => {
          handleTimeUpdate();
        };

        // 由于现在 `onAudioEnded` 是稳定的，我们可以正确移除之前添加的监听器
        audio.removeEventListener('ended', onAudioEnded);
        audio.addEventListener('ended', onAudioEnded);

        // 返回一个清理函数来移除监听器，以防组件卸载
        return () => {
          audio.removeEventListener('ended', onAudioEnded);
        };
        
      }
    }, [audioAndLip])
    

    const updateMorphTargets = (ratio: number) => {
      ratio = ratio * 2
      const headNode = headNodes[audioAndLip?.avatarName || avatarName]
      if (headNode instanceof THREE.Mesh && headNode.morphTargetInfluences) {
        if (ratio <=1) {
          headNode.morphTargetInfluences[currentMorphTargetIndex.current] = ratio;
        } else {
          headNode.morphTargetInfluences[currentMorphTargetIndex.current] = 2-ratio;
        }
      }
      
      const teethNode = teethNodes[audioAndLip?.avatarName || avatarName]
      if (teethNode instanceof THREE.Mesh && teethNode.morphTargetInfluences) {
        if (ratio <=1) {
          teethNode.morphTargetInfluences[currentMorphTargetIndex.current] = ratio;
        } else {
          teethNode.morphTargetInfluences[currentMorphTargetIndex.current] = 2-ratio;
        }
      }
    };

    const animationPlay = () => {
      if (gltfs[audioAndLip?.avatarName || avatarName].scene && fbx.animations[0]) {
        mixer.current = new THREE.AnimationMixer(gltfs[audioAndLip?.avatarName || avatarName].scene);
        const action = mixer.current.clipAction(fbx.animations[0]);

        // action.setLoop(THREE.LoopOnce, 1);
        
        action.play();
    }
    }

    useEffect(() => {
      if (gltfs[audioAndLip?.avatarName || avatarName].scene) {
          if (position) {
            gltfs[audioAndLip?.avatarName || avatarName].scene.position.set(Number(position.x), Number(position.y), Number(position.z));
            gltfs[audioAndLip?.avatarName || avatarName].scene.rotation.y = Number(position.rotation);
          }
      }
      animationPlay()
  }, [gltfs[audioAndLip?.avatarName || avatarName], fbx]);

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

    return <primitive object={gltfs[audioAndLip?.avatarName || avatarName].scene} />;
};

export default GLBModel;