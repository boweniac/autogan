import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, extend, useFrame, useLoader, useThree } from '@react-three/fiber';
import { useGLTF, PerspectiveCamera, useFBX, useAnimations, OrbitControls } from '@react-three/drei';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js'
import * as THREE from 'three';
// import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import AudioPlay from '../../Audio/AudioPlay';
import { AudioAndLip, MouthCues } from '@/stores/TypeAudioAndLip';

// extend({ OrbitControls });
type DefaultAvatarProps = {
  morphTargetName: string; // 添加形态目标名称作为一个属性
  audioAndLip: AudioAndLip | undefined;
};

type GLBModelProps = {
  modelPath: string; // 模型文件的路径
  animationPath: string; // FBX 动画文件路径
  morphTargetName: string; // 添加形态目标名称作为一个属性
  audioAndLip: AudioAndLip | undefined;
};

const GLBModel: React.FC<GLBModelProps> = ({ modelPath, animationPath, morphTargetName, audioAndLip }) => {
    const gltf = useLoader(GLTFLoader, modelPath);
    const fbx = useLoader(FBXLoader, animationPath);
    const mixer = useRef<THREE.AnimationMixer>();
    const morphTargetHolder = useRef(0);
    // const [morphTargetInfluence, setMorphTargetInfluence] = useState(0); // 使用 state 来控制形态目标影响
    const audioFile = audioAndLip?.audioFile || ""
    const audio = useMemo(()=>new Audio(`${audioFile}`), [audioFile])

    useEffect(() => {
      // const audio = audioRef.current;
      if (audio) {
        audio.play()
          .then(() => {
            console.log("Audio is playing");
          })
          .catch(error => {
            console.error("Error playing audio", error);
          });
        
      //   audio.onended = () => {
      //     props.onFinishedPlaying();
      //   };

      //   audio.ontimeupdate = () => {
      //     props.onPlaying(audio.currentTime);
      // };
      const headNode = gltf.scene.getObjectByName('Wolf3D_Head');
      const teethNode = gltf.scene.getObjectByName('Wolf3D_Teeth');
      const handleTimeUpdate = () => {
        const currentTime = audio.currentTime;
        // let found = false;
        console.log(`audio.currentTime:`+JSON.stringify(audio.currentTime));
        if (audioAndLip) {
          // console.log(`audioAndLip.lipsData:`+JSON.stringify(audioAndLip.lipsData));
          for (let i = 0; i < audioAndLip.lipsData.length; i++) {
            const lipsData = audioAndLip.lipsData[i] as MouthCues;
            console.log(`i:`+JSON.stringify(i));
            if (currentTime >= lipsData.start && currentTime <= lipsData.end) {
              console.log(`i2:`+JSON.stringify(i));
              console.log(`headNode instanceof THREE.Mesh:`+JSON.stringify(headNode instanceof THREE.Mesh));
              if (headNode instanceof THREE.Mesh && headNode.morphTargetDictionary && headNode.morphTargetInfluences) {
                console.log(`i3:`+JSON.stringify(i));
                console.log(`lipsData.value2:`+JSON.stringify(lipsData.value));
                console.log(`corresponding[lipsData.value]:`+JSON.stringify(corresponding[lipsData.value]));
                const headTargetIndex = headNode.morphTargetDictionary[corresponding[lipsData.value]];
                console.log(`headTargetIndex:`+JSON.stringify(headTargetIndex));
                if (typeof headTargetIndex === 'number') {
                  headNode.morphTargetInfluences[morphTargetHolder.current] = 0;
                  headNode.morphTargetInfluences[headTargetIndex] = 1;
                  // morphTargetHolder.current = headTargetIndex;
                  // break
                }
              }
              
              if (teethNode instanceof THREE.Mesh && teethNode.morphTargetDictionary && teethNode.morphTargetInfluences) {
                const teethTargetIndex = teethNode.morphTargetDictionary[corresponding[lipsData.value]];
                if (typeof teethTargetIndex === 'number') {
                  teethNode.morphTargetInfluences[morphTargetHolder.current] = 0;
                  teethNode.morphTargetInfluences[teethTargetIndex] = 1;
                  morphTargetHolder.current = teethTargetIndex;
                }
              }
              // found = true;
              break
            }
          }
        }
      };
      audio.ontimeupdate = () => {
        handleTimeUpdate();
    };

    //   audio.addEventListener('timeupdate', handleTimeUpdate);

    // return () => {
    //   audio.removeEventListener('timeupdate', handleTimeUpdate);
    // };
      }
    }, [audioFile]);

    useEffect(() => {
        if (gltf.scene && fbx.animations[0]) {
            mixer.current = new THREE.AnimationMixer(gltf.scene);
            const action = mixer.current.clipAction(fbx.animations[0]);
            action.play();

            // gltf.scene.position.set(1, 0, 0)
        }
    }, [gltf, fbx]);


    useFrame((state, delta) => {
      mixer.current?.update(delta);
      // const headNode = gltf.scene.getObjectByName('Wolf3D_Head');
      // const teethNode = gltf.scene.getObjectByName('Wolf3D_Teeth');
      // audio.ontimeupdate = () => {
      //   if (audioAndLip) {
      //     const currentTime = audio.currentTime
      //     console.log(`audioAndLip.lipsData:`+JSON.stringify(audioAndLip.lipsData));
      //     for (let i = 0; i < audioAndLip.lipsData.length; i++) {
      //       const lipsData = audioAndLip.lipsData[i] as MouthCues;
      //       console.log(`lipsData:`+JSON.stringify(lipsData));
      //       if (currentTime >= lipsData.start && currentTime <= lipsData.end) {
      //         if (headNode instanceof THREE.Mesh && headNode.morphTargetDictionary && headNode.morphTargetInfluences) {
      //           const headTargetIndex = headNode.morphTargetDictionary[corresponding[lipsData.value]];
      //           if (typeof headTargetIndex === 'number') {
      //             headNode.morphTargetInfluences[morphTargetHolder.current] = 0;
      //             headNode.morphTargetInfluences[headTargetIndex] = 1;
      //           }
      //         }
              
      //         if (teethNode instanceof THREE.Mesh && teethNode.morphTargetDictionary && teethNode.morphTargetInfluences) {
      //           const teethTargetIndex = teethNode.morphTargetDictionary[corresponding[lipsData.value]];
      //           if (typeof teethTargetIndex === 'number') {
      //             teethNode.morphTargetInfluences[morphTargetHolder.current] = 0;
      //             teethNode.morphTargetInfluences[teethTargetIndex] = 1;
      //             morphTargetHolder.current = teethTargetIndex;
      //           }
      //         }
      //       }
      //     }
      //   }
      // };
    });

    return <primitive object={gltf.scene} />;
};

const CameraController = () => {
  const { camera, gl } = useThree();

  useEffect(() => {
      camera.position.set(0, 1.5, 1); // 设置摄像机的初始位置
      // camera.lookAt(3, 3, 3); // 设置摄像机的初始朝向
  }, [camera]);

  return <OrbitControls args={[camera, gl.domElement]} target={[0, 1.5, 0]} />;
};

const corresponding: { [key: string]: string } = {
  "A": "viseme_PP",
  "B": "viseme_kk",
  "C": "viseme_I",
  "D": "viseme_aa",
  "E": "viseme_O",
  "F": "viseme_U",
  "G": "viseme_FF",
  "H": "viseme_TH",
  "X": "viseme_PP",
};

const DefaultAvatar: React.FC<DefaultAvatarProps> = ({ morphTargetName, audioAndLip }) => {
  const [morphValue, setMorphValue] = useState<string>("");
  return (
    <div style={{height: "100%", width: "100%"}}>
      <Canvas gl={{ alpha: true }}>
        {/* <PerspectiveCamera makeDefault position={[0, 3, 2]} fov={30} near={0.1} far={1000} /> */}
        <ambientLight  intensity={4}/>
        <pointLight position={[0, 2, 3]} intensity={20} />
        <GLBModel modelPath="/avatar/default.glb" animationPath="/animations/default.fbx" morphTargetName={morphValue} audioAndLip={audioAndLip} />
        <CameraController  />
        {/* <PerspectiveCamera makeDefault fov={20} position={[0, 1.5, 3]} /> */}
      </Canvas>
    </div>
  );
};

export default DefaultAvatar;