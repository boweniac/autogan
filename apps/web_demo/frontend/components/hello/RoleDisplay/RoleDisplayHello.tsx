import { Button, SegmentedControl, Stack } from "@mantine/core";

import classes from './RoleDisplayHello.module.css';
// import { DefaultAvatar } from "../avatar/DefaultAvatar/DefaultAvatar2";

import dynamic from 'next/dynamic'
import { FunctionComponent, useEffect, useRef, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { AudioAndLip } from "@/stores/TypeAudioAndLip";
import DefaultScene from "../../avatar/Scene/DefaultScene";
import HelloScene from "@/components/avatar/Scene/HelloScene";

// type RoleDisplayHelloProps = {
//     avatarName: string; // 模型文件的路径
//   }


export default function RoleDisplayHello() {
    const avatarList = ["customerManagerBoy", "customerManagerGirl", "coder", "documentExp", "searchExpert", "secretary", "tester"]
    const [avatarName, setAvatarName] = useState<string>("customerManagerBoy");
    // console.log(`props.avatarName:`+props.avatarName);
    const currentAvatarIndex = useRef(0);

    const [viewportHeight, setViewportHeight] = useState(0); // 初始值设置为0或合理的默认值

  useEffect(() => {
    // 这确保了window.innerHeight只在客户端获取
    setViewportHeight(window.innerHeight);

    const handleResize = () => {
      setViewportHeight(window.innerHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

    return (
        <Stack
            className={classes.roleDisplay}
            // bg="var(--mantine-color-body)"
            justify="space-between"
            style={{
                position: 'fixed',
                // zIndex: -1
                zIndex: 1,
                top: `calc(${-0.70*viewportHeight}px)`
                // 其他样式以调整内容位置和外观
            }}
        >
            {/* <Canvas>
                <DefaultAvatar />
            </Canvas> */}
            
            <HelloScene avatarName={avatarName} animation="hello" test={false} animationPlayEndCallback={()=>{
                if (currentAvatarIndex.current == avatarList.length-1) {
                    currentAvatarIndex.current = 0
                  } else {
                    currentAvatarIndex.current += 1
                  }
                  setAvatarName(avatarList[currentAvatarIndex.current])
            }
                
            }/>
        </Stack>
    );
}