import CustTextarea from "@/components/agent/CustTextarea/CustTextarea";
import { HeaderMegaMenu } from "@/components/appshell/HeaderMegaMenu/HeaderMegaMenu";
import { updateActivePage } from "@/stores/LocalStoreActions";
import { Box, Button, Center, Container, Flex, Group, ScrollArea, Stack, Textarea, rem, Text } from "@mantine/core";
import { useEffect, useState } from "react";
import { useRouter } from 'next/router';
import { LeftNavbarMenu } from "@/components/agent/LeftNavbarMenu/LeftNavbarMenu";
import RoleDisplay from "@/components/agent/RoleDisplay/RoleDisplay";
import MessagesDisplay from "@/components/agent/MessagesDisplay/MessagesDisplay";

export default function AgentFrame() {
    const router = useRouter();
    const [text, setText] = useState<string | undefined>();

    useEffect(() => {
        if (router.isReady) {
            updateActivePage("/agent")
        }
    }, [router.isReady]);


    return (
        <Stack
            w="100%"
            h="100%"
            justify="flex-start"
            gap={0}
            // style={{
            //     backgroundImage: 
            //         `linear-gradient(to left, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1)), 
            //         url(/avatar/default_avatar_background_picture.jpg)`, // 设置渐变和背景图片
            //     backgroundSize: 'cover', // 背景图片覆盖整个元素
            //     backgroundRepeat: 'no-repeat', // 背景图片不重复
            //     backgroundPosition: 'center', // 背景图片居中
            // }}
        >
            <Box
                style={{ position: 'relative', zIndex: 2 }}
            >
                <Group 
                    h={`calc(100vh)`}
                    gap={0} 
                    style={{ width: '100%', alignItems: 'stretch' }}
                    wrap="nowrap"
                >
                    <LeftNavbarMenu ></LeftNavbarMenu>
                    <Stack
                        h="100%"
                        w="100%"
                        justify="space-between"
                        gap={0}
                        // style={{ backgroundColor: 'transparent', marginRight: rem(440) }}
                    >
                        <HeaderMegaMenu></HeaderMegaMenu>
                        <Group 
                            h={`calc(100vh - ${rem(50)})`}
                            gap={0} 
                            style={{ alignItems: 'stretch' }}
                            wrap="nowrap"
                        >
                            <Stack
                                // h={`calc(100vh - ${rem(50)})`}
                                // w={`calc(100% - ${rem(440)})`}
                                justify="space-between"
                                gap={0}
                                style={{ flexGrow: 1, marginRight: rem(440)}}
                            >
                                <MessagesDisplay></MessagesDisplay>
                                <CustTextarea setTest={setText}></CustTextarea>
                            </Stack>
                            {/* <RoleDisplay /> */}
                        </Group>
                    </Stack>
                </Group>
            </Box>
            <RoleDisplay />
        </Stack>
    );
}