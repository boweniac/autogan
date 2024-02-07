import { Message } from "@/stores/TypeAgentChat";
import classes from './MessageFrame.module.css';
import { Flex, Text } from "@mantine/core";
import AvatarBlock from "./AvatarBlock/AvatarBlock";
import MessageBlocks from "./MessageBlock/MessageBlocks";
import { LocalState, localStore } from "@/stores/LocalStore";

type FlexDirection = 'row' | 'row-reverse';

type MessageBlockProps = {
    mainAgent: string;
    message: Message;
}

export default function MessageFrame(props: MessageBlockProps) {
    const agentAvatarMapping = localStore((state: LocalState) => state.agentAvatarMapping);
    const name = props.message.agent_name || ""

    let direction = "row"
    if (name == props.mainAgent) {
      direction = "row-reverse"
    }

    // console.log(`props.message.content:`+JSON.stringify(props.message.content));

    return (
      <Flex
            justify="flex-start"
            align="flex-start"
            direction={direction as FlexDirection}
            wrap="nowrap"
            gap="0"
            className={classes.messageFrame}
        >
            <AvatarBlock avatarName={agentAvatarMapping[name]}></AvatarBlock>
            <MessageBlocks mainAgent={props.mainAgent} name={props.message.agent_name} message_blocks={props.message.message_blocks}></MessageBlocks>
        </Flex>
    )
}