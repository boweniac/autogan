import { Box } from "@mantine/core";
import classes from './Hello.module.css';
import RoleDisplayHello from "./RoleDisplay/RoleDisplayHello";
import RoleDisplayHelloTitle from "./RoleDisplay/RoleDisplayHelloTitle";
import { useEffect } from "react";
import { updateActivePageState } from "@/stores/LocalStoreActions";


export default function Video() {
    useEffect(() => {
        updateActivePageState("/video")
    }, []);

    return (
        <Box
            h={`calc(100vh)`}
            w="100%"
            className={classes.agentFrame}
            style={{
                width: '100%', // 根据需要设置宽度
                height: '500px', // 根据需要设置高度
                backgroundImage: 'url(/bg13.jpg)', // 注意：如果图片在src/assets中，你可能需要使用import来引入图片
                backgroundSize: 'cover', // 覆盖整个容器
                backgroundPosition: 'center', // 图片居中显示
              }}
        >
            <RoleDisplayHelloTitle></RoleDisplayHelloTitle>
            <RoleDisplayHello  />
        </Box>
    );
}