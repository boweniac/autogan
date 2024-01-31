import { Button, Group, SegmentedControl, Stack, Text, Transition } from "@mantine/core";

import classes from './RoleDisplayHello.module.css';
// import { DefaultAvatar } from "../avatar/DefaultAvatar/DefaultAvatar2";

import dynamic from 'next/dynamic'
import { FunctionComponent, useEffect, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { AudioAndLip } from "@/stores/TypeAudioAndLip";
import DefaultScene from "../../avatar/Scene/DefaultScene";
import HelloScene from "@/components/avatar/Scene/HelloScene";
import { useRouter } from "next/router";


export default function RoleDisplayHelloTitle() {
  const router = useRouter();
  const [start, setStart] = useState<boolean>(false);
    
  useEffect(() => {
      if (router.isReady) {
        setStart(true)
      }
  }, [router.isReady]);
    // console.log(`props.avatarName:`+props.avatarName);
    return (
        <Stack
            className={classes.roleDisplay}
            // align="center"
            // bg="var(--mantine-color-body)"
            justify="space-between"
            style={{
                position: 'fixed',
                zIndex: -1
                // zIndex: 1,
                // 其他样式以调整内容位置和外观
            }}
        >
          <Transition mounted={start} transition="fade" duration={1500} timingFunction="ease">
              {(styles) => <Group style={styles} justify="center" gap="xl">
            <h1 className={classes.title}>
          欢迎来到
        </h1>
        <h1 className={classes.title}>
          <Text component="span" variant="gradient" gradient={{ from: 'blue', to: 'cyan' }} inherit>
            爱博闻科技
          </Text>
        </h1>
    </Group>}
          </Transition>
        </Stack>
    );
}