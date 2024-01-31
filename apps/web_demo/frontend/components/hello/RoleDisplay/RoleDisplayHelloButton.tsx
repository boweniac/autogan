import { Button, SegmentedControl, Stack, Text, rem } from "@mantine/core";

import classes from './RoleDisplayHello.module.css';
// import { DefaultAvatar } from "../avatar/DefaultAvatar/DefaultAvatar2";

import dynamic from 'next/dynamic'
import { FunctionComponent, useEffect, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { AudioAndLip } from "@/stores/TypeAudioAndLip";
import DefaultScene from "../../avatar/Scene/DefaultScene";
import HelloScene from "@/components/avatar/Scene/HelloScene";

type RoleDisplayHelloButtonProps = {
    clickIntroductionCallback: () => void;
    clickAgentCallback: () => void;
  }

export default function RoleDisplayHelloButton(props: RoleDisplayHelloButtonProps) {
    // console.log(`props.avatarName:`+props.avatarName);
    return (
        <Stack
            className={classes.roleDisplay}
            align="center"
            // bg="var(--mantine-color-body)"
            justify="flex-end"
            style={{
                position: 'fixed',
                zIndex: 2
                // zIndex: 1,
                // 其他样式以调整内容位置和外观
            }}
        >
            <Stack
                h={300}
                // bg="var(--mantine-color-body)"
                align="center"
                justify="space-around"
                pb={rem(64)}
            >
                <Button
                    size="xl"
                    className={classes.control}
                    variant="gradient"
                    gradient={{ from: 'blue', to: 'cyan' }}
                    onClick={props.clickIntroductionCallback}
                >
                    了解数字员工
                </Button>
                <Button
                    size="xl"
                    variant="default"
                    className={classes.control}
                    onClick={props.clickAgentCallback}
                >
                    立即体验
                </Button>
            </Stack>
        </Stack>
    );
}