import CustTextarea from "@/components/agent/CustTextarea/CustTextarea";
import { HeaderMegaMenu } from "@/components/appshell/HeaderMegaMenu/HeaderMegaMenu";
import { updateActivePage } from "@/stores/LocalStoreActions";
import { Box, Button, Center, Container, Flex, Group, ScrollArea, Stack, Textarea, rem, Text } from "@mantine/core";
import { useEffect, useState } from "react";
import { useRouter } from 'next/router';
import { NavbarSegmented } from "@/components/agent/LeftNavbarMenu/LeftNavbarMenu";
import RoleDisplay from "@/components/agent/RoleDisplay/RoleDisplay";
import DefaultAvatar from "@/components/agent/avatar/DefaultAvatar/DefaultAvatar2";

export default function Agent() {
    const router = useRouter();
    const [test, setTest] = useState<string | undefined>();

    useEffect(() => {
        if (router.isReady) {
            updateActivePage("/agent")
        }
    }, [router.isReady]);


    return (
        <Stack
            w="100%"
            h="100%"
            bg="var(--mantine-color-gray-3)"
            justify="flex-start"
            gap={0}
        >
            <HeaderMegaMenu></HeaderMegaMenu>
            <Group 
                h={`calc(100vh - ${rem(50)})`}
                bg="var(--mantine-color-gray-3)"
                gap={0} 
                style={{ width: '100%', alignItems: 'stretch' }}
            >
                <NavbarSegmented ></NavbarSegmented>
                {/* <Stack
                    h={`calc(100vh - ${rem(50)})`}
                    bg="var(--mantine-color-body)"
                    justify="space-between"
                    gap={0}
                    style={{ flexGrow: 1 }}
                >
                    <ScrollArea type="never" w="100%" >
                        <Text style={{wrap: "wrap"}}>{test}</Text>
                    </ScrollArea>
                    <CustTextarea setTest={setTest}></CustTextarea>
                </Stack> */}
                <DefaultAvatar></DefaultAvatar>
            </Group>
        </Stack>
    );
}