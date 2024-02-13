import HelloScene from "@/components/avatar/Scene/HelloScene";
import Hello from "@/components/hello/Hello";
import { Box } from "@mantine/core";

export default function Home() {
    return <Box
    h={`calc(100vh)`}
    w="100%"
    // className={classes.agentFrame}
>
<HelloScene avatarName="customerManagerGirl" animation="config" test={true}/>
</Box>
}
