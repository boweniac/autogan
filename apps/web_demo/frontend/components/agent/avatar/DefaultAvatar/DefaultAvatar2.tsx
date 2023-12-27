import React from 'react';
import { Canvas } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';

type GLBModelProps = {
  path: string; // 模型文件的路径
};

const GLBModel: React.FC<GLBModelProps> = ({ path }) => {
  const { scene } = useGLTF(path) as any;

  return <primitive object={scene} />;
};

const DefaultAvatar: React.FC = () => {
  return (
    <Canvas>
      <ambientLight />
      <pointLight position={[10, 10, 10]} />
      <GLBModel path="/avatar/default.glb" />
    </Canvas>
  );
};

export default DefaultAvatar;