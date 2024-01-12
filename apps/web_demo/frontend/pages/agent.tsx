
import AgentFrame from "@/components/agent/AgentFrame";

export default function Agent() {
    return <AgentFrame></AgentFrame>
}
// import CustTextarea from "@/components/agent/CustTextarea/CustTextarea";
// import { HeaderMegaMenu } from "@/components/appshell/HeaderMegaMenu/HeaderMegaMenu";
// import { updateActivePage } from "@/stores/LocalStoreActions";
// import { Box, Button, Center, Container, Flex, Group, ScrollArea, Stack, Textarea, rem, Text } from "@mantine/core";
// import { useEffect, useState } from "react";
// import { useRouter } from 'next/router';
// import { LeftNavbarMenu } from "@/components/agent/LeftNavbarMenu/LeftNavbarMenu";
// import RoleDisplay from "@/components/agent/RoleDisplay/RoleDisplay";
// import MessagesDisplay from "@/components/agent/MessagesDisplay/MessagesDisplay";

// export default function Agent() {
//     return (
//         <Stack
//             w="100%"
//             h="100%"
//             justify="flex-start"
//             gap={0}
//             style={{
//                 backgroundImage: 
//                     `linear-gradient(to left, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1)), 
//                     url(/avatar/default_avatar_background_picture.jpg)`, // 设置渐变和背景图片
//                 backgroundSize: 'cover', // 背景图片覆盖整个元素
//                 backgroundRepeat: 'no-repeat', // 背景图片不重复
//                 backgroundPosition: 'center', // 背景图片居中
//             }}
//         >
//             <HeaderMegaMenu></HeaderMegaMenu>
//             <Group 
//                 h={`calc(100vh - ${rem(50)})`}
//                 gap={0} 
//                 style={{ width: '100%', alignItems: 'stretch' }}
//                 wrap="nowrap"
//             >
//                 <LeftNavbarMenu ></LeftNavbarMenu>
//                 <Stack
//                     h={`calc(100vh - ${rem(50)})`}
//                     justify="space-between"
//                     gap={0}
//                     style={{ flexGrow: 1 }}
//                 >
//                     <MessagesDisplay></MessagesDisplay>
//                     <CustTextarea setTest={setTest}></CustTextarea>
//                 </Stack>
//                 <RoleDisplay />
//             </Group>
//         </Stack>
//     );
// }