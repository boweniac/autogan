import { Button, SegmentedControl, Stack } from "@mantine/core";

import classes from './RoleDisplay.module.css';
// import { DefaultAvatar } from "../avatar/DefaultAvatar/DefaultAvatar2";

import dynamic from 'next/dynamic'
import { FunctionComponent, useEffect, useState } from "react";
import { Canvas } from "@react-three/fiber";
import DefaultAvatar from "../avatar/DefaultAvatar/DefaultAvatar";
import { AudioAndLip } from "@/stores/TypeAudioAndLip";

type RoleDisplayProps = {
    morphTargetName: string;
    audioAndLip: AudioAndLip | undefined;
  }


export default function RoleDisplay(props: RoleDisplayProps) {
    const [morphTargetName, setMorphTargetName] = useState<string>("viseme_O");

    useEffect(() => {
        setMorphTargetName(props.morphTargetName)
    }, [props.morphTargetName]);

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
            <DefaultAvatar morphTargetName={morphTargetName} audioAndLip={props.audioAndLip}/>
        </Stack>
    );
}