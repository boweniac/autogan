import { Message } from "@/stores/TypeAgentChat";
import { Avatar, Box, Card, Flex, Group, Text } from "@mantine/core";
import MarkdownBlock from "../MarkdownBlock/MarkdownBlock";
import classes from './MessageBlock.module.css';


type UserMessageBlockProps = {
    message: Message;
}

export default function AgentMessageBlock(props: UserMessageBlockProps) {
    const message = props.message

    return <div>
        <Flex
            justify="flex-start"
            align="flex-start"
            direction="row"
            wrap="nowrap"
            gap="xs"
            // className={classes.group}
        >
            <Avatar
            // className={classes.avatar}
            src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png"
            alt={message.name}
            radius="xl"
            size="sm"
            />
            <div>
                <Text className={classes.agentName} size="sm">{message.name}</Text>
                {/* <p>{message.content}</p> */}
                <div
                    className={classes.agentMessage}
                >
                    {/* <p>fdsfafad</p> */}
                    <MarkdownBlock content={message.content!}></MarkdownBlock>
                </div>
            </div>
        </Flex>
    </div>
}