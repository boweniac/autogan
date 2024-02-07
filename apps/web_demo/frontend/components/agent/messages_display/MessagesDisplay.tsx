import { ScrollArea, rem } from "@mantine/core";
import MessageFrame from "../../message/MessageFrame";
import classes from './MessagesDisplay.module.css';
import { LocalState, localStore } from "@/stores/LocalStore";
import { useEffect, useRef } from "react";

type MessagesDisplayProps = {
    conversationID: string | undefined
    setLastMsgIdCallback: (value: string) => void;
    syncMessagesCallback: () => void
}

export default function MessagesDisplay(props: MessagesDisplayProps) {
    const agentConversationMessage = localStore((state: LocalState) => state.agentConversationMessage);
    const agentConversation = agentConversationMessage?.find((message) => message.id == props.conversationID);
    const viewport = useRef<HTMLDivElement>(null);
    const lastMessage = agentConversation?.messages[agentConversation?.messages.length - 1];
    const lastMessageBlock = lastMessage?.message_blocks[lastMessage.message_blocks.length - 1];

    const scrollToBottom = () =>
      viewport.current!.scrollTo({ top: viewport.current!.scrollHeight});

    useEffect(() => {
        if (lastMessageBlock?.content) {
            scrollToBottom()
        }
    }, [lastMessageBlock?.content]);

    useEffect(() => {
        if (props.conversationID) {
            let lastMsgId = ""
            if (agentConversation && agentConversation.messages.length > 0) {
                lastMsgId = agentConversation.messages[agentConversation.messages.length-1].msg_id ?? ""
            }
            props.setLastMsgIdCallback(lastMsgId)
            props.syncMessagesCallback()
        }
    }, [props.conversationID]);
    
    return (
        <ScrollArea className={classes.scrollArea} type="never" viewportRef={viewport}>
            {agentConversation?.messages?.map((message) => (
                <MessageFrame mainAgent="Customer" key={message.localID} message={message} />
            ))}
        </ScrollArea>
    );
}