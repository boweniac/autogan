import { Message, MessageBlock } from "@/stores/TypeAgentChat";
import { Avatar, Box, Card, Flex, Group, Loader, Stack, Text, rem } from "@mantine/core";

import classes from './MessageBlocks.module.css';
import FileBlock from "../FileBlock/FileBlock";
import MarkdownBlock from "../MarkdownBlock/MarkdownBlock";


type UserMessageBlockProps = {
    conversationID?: string | undefined
    mainAgent: string;
    name: string | undefined;
    message_blocks: MessageBlock[];
}

export default function MessageBlocks(props: UserMessageBlockProps) {

    return (
            <Stack
                align={`${props.name == props.mainAgent ? "flex-end" : "flex-start"}`}
                justify="flex-start"
                gap="0"
            >
                <Text className={classes.agentName} fw={700}>{props.name}</Text>
                <Card
                    padding="sm"
                    radius="md"
                    // maw={`calc(100vw - ${rem(400)} - ${rem(364)})`}
                    className={ `${classes.messageBlock} ${props.name == props.mainAgent ? classes.messageRight : classes.messageLeft}` }
                >
                    {
                        props.message_blocks.map((mb) => 
                            {
                                return mb.contentType == "file" ? <FileBlock conversationID={props.conversationID} content_tag={mb.contentTag}></FileBlock> : <MarkdownBlock key={mb.localID} content_type={mb.contentType} content_tag={mb.contentTag} content={mb.content!}></MarkdownBlock>
                            }
                            // <MarkdownBlock key={mb.localID} content_type={mb.content_type} content_tag={mb.content_tag} content={mb.content!}></MarkdownBlock>
                        )
                        // <MarkdownBlock content_type={"mb.content_type"} content={"mb.content!"}></MarkdownBlock>

                    }
                </Card>
            </Stack>
    )
}