import { Message } from "@/stores/TypeAgentChat";
import { Avatar, Box, Card, Flex, Group, Loader, Stack, Text, rem } from "@mantine/core";
import MarkdownBlock from "../MarkdownBlock/MarkdownBlock";
import classes from './MessageBlock.module.css';
import AvatarBlock from "../AvatarBlock/AvatarBlock";


type UserMessageBlockProps = {
    role: string | undefined;
    name: string | undefined;
    content: string | undefined;
}

export default function MessageBlock(props: UserMessageBlockProps) {

    return (
            <Stack
                align={`${props.role == "user" ? "flex-end" : "flex-start"}`}
                justify="flex-start"
                gap="0"
            >
                <Text className={classes.agentName} fw={700}>{props.name}</Text>
                <Card
                    padding="sm"
                    radius="md"
                    className={ `${classes.messageBlock} ${props.role == "user" ? classes.messageRight : classes.messageLeft}` }
                >
                    {
                        props.content == undefined ? <Loader color="blue" size={rem(14)} type="bars" /> : <MarkdownBlock content={props.content!}></MarkdownBlock>
                    }
                </Card>
            </Stack>
    )
}