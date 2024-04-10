import { Button, SegmentedControl, Stack } from "@mantine/core";

import classes from './RoleDisplay.module.css';
// import { DefaultAvatar } from "../avatar/DefaultAvatar/DefaultAvatar2";

import dynamic from 'next/dynamic'
import { FunctionComponent, useEffect, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { AudioAndLip } from "@/stores/TypeAudioAndLip";
import DefaultScene from "../../avatar/Scene/DefaultScene";
import HelloScene from "@/components/avatar/Scene/HelloScene";

type RoleDisplayProps = {
    avatarName: string; // 模型文件的路径
    audioAndLip: AudioAndLip | undefined;
    audioEndCallback: ()=>void
  }


export default function RoleDisplay(props: RoleDisplayProps) {
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
    // console.log(`props.avatarName:`+props.avatarName);
    return (
        <Stack
            className={classes.roleDisplay}
            // bg="var(--mantine-color-body)"
            justify="space-between"
            style={{
                position: 'fixed',
                zIndex: -1,
                top: `calc(${-0.70*viewportHeight}px)`
                // zIndex: 1,
                // 其他样式以调整内容位置和外观
            }}
        >
            {/* <Canvas>
                <DefaultAvatar />
            </Canvas> */}
            <HelloScene avatarName={props.avatarName} animation="stay" audioAndLip={props.audioAndLip} audioEndCallback={props.audioEndCallback} test={false}/>
        </Stack>
    );
}