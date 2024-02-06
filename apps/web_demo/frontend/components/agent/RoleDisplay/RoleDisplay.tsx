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

    return (
        <Stack
            className={classes.roleDisplay}
            // bg="var(--mantine-color-body)"
            justify="space-between"
            style={{
                position: 'fixed',
                zIndex: -1
                // zIndex: 1,
                // 其他样式以调整内容位置和外观
            }}
        >
            {/* <Canvas>
                <DefaultAvatar />
            </Canvas> */}
            <HelloScene avatarName={props.avatarName} animation="stay" audioAndLip={props.audioAndLip} audioEndCallback={props.audioEndCallback}/>
        </Stack>
    );
}