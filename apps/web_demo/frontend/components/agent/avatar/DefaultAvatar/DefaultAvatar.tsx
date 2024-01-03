import React, { useEffect, useRef, useState } from 'react';
import { Canvas, extend, useFrame, useLoader, useThree } from '@react-three/fiber';
import { useGLTF, PerspectiveCamera, useFBX, useAnimations, OrbitControls } from '@react-three/drei';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js'
import * as THREE from 'three';
// import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

// extend({ OrbitControls });

type GLBModelProps = {
  modelPath: string; // 模型文件的路径
  animationPath: string; // FBX 动画文件路径
  morphTargetName: string; // 添加形态目标名称作为一个属性
};

const GLBModel: React.FC<GLBModelProps> = ({ modelPath, animationPath, morphTargetName }) => {
    const gltf = useLoader(GLTFLoader, modelPath);
    const fbx = useLoader(FBXLoader, animationPath);
    const mixer = useRef<THREE.AnimationMixer>();
    // const [morphTargetInfluence, setMorphTargetInfluence] = useState(0); // 使用 state 来控制形态目标影响

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

        const node = gltf.scene.getObjectByName('Wolf3D_Head');
        if (node instanceof THREE.Mesh && node.morphTargetDictionary && node.morphTargetInfluences) {
          const targetIndex = node.morphTargetDictionary[morphTargetName];
          if (typeof targetIndex === 'number') {
            node.morphTargetInfluences[targetIndex] = 0;
          }
        }
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

const DefaultAvatar: React.FC = () => {
  return (
    <Canvas gl={{ alpha: true }}>
      {/* <PerspectiveCamera makeDefault position={[0, 3, 2]} fov={30} near={0.1} far={1000} /> */}
      <ambientLight  intensity={4}/>
      <pointLight position={[0, 2, 3]} intensity={20} />
      <GLBModel modelPath="/avatar/default.glb" animationPath="/animations/default.fbx" morphTargetName="viseme_O" />
      <CameraController  />
      {/* <PerspectiveCamera makeDefault fov={20} position={[0, 1.5, 3]} /> */}
    </Canvas>
  );
};

export default DefaultAvatar;