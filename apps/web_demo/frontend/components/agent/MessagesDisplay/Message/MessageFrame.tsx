import { Message } from "@/stores/TypeAgentChat";
import classes from './MessageFrame.module.css';
import { Flex, Text } from "@mantine/core";
import AvatarBlock from "./AvatarBlock/AvatarBlock";
import MarkdownBlock from "./MarkdownBlock/MarkdownBlock";
import MessageBlock from "./MessageBlock/MessageBlock";

type FlexDirection = 'row' | 'row-reverse';

type MessageBlockProps = {
    message: Message;
}

export default function MessageFrame(props: MessageBlockProps) {
    const role = props.message.role

    let direction = "row"
    if (role == "user") {
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
            <AvatarBlock role={role}></AvatarBlock>
            <MessageBlock role={props.message.role} name={props.message.agent_name} content={props.message.content}></MessageBlock>
        </Flex>
    )
}