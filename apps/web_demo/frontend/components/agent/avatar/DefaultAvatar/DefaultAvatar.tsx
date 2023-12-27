import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

type GLBViewerProps = {
  modelUrl: string;
};

const GLBViewer: React.FC<GLBViewerProps> = ({ modelUrl }) => {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const mount = mountRef.current;

    if (mount) {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, mount.clientWidth / mount.clientHeight, 0.1, 1000);
      camera.position.z = 1;
      camera.position.y = 1.5;

      const renderer = new THREE.WebGLRenderer();
      renderer.setSize(mount.clientWidth, mount.clientHeight);
      renderer.setClearColor(0xffffff, 0); // 设置背景色为白色
      mount.appendChild(renderer.domElement);

      // const light = new THREE.HemisphereLight(0xffffbb, 0x080820, 1);
      // scene.add(light);

      const ambientLight = new THREE.AmbientLight(0xffffff, 2); // 环境光
      scene.add(ambientLight);

      const loader = new GLTFLoader();
      loader.load(
        modelUrl,
        (gltf) => {
          scene.add(gltf.scene);
        },
        undefined,
        (error) => {
          console.error('An error happened', error);
        }
      );

      const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
      };
      animate();

      return () => {
        mount.removeChild(renderer.domElement);
      };
    }
  }, [modelUrl]);

  return <div ref={mountRef} style={{ width: '100%', height: '100%' }} />;
};

export default GLBViewer;