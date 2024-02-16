import { ScrollArea, rem } from "@mantine/core";
import MessageFrame from "../../message/MessageFrame";
import classes from './MessagesDisplay.module.css';
import { LocalState, localStore } from "@/stores/LocalStore";
import { useEffect, useRef, useState } from "react";

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

    const avatarState = localStore((state: LocalState) => state.avatarState);
    const classScrollArea = avatarState ? classes.scrollAreaAvatarOn : classes.scrollAreaAvatarOff;

    const [viewportHeight, setViewportHeight] = useState(0); // 初始值设置为0或合理的默认值

  useEffect(() => {
    // 这确保了window.innerHeight只在客户端获取
    setViewportHeight(window.innerHeight);

    const handleResize = () => {
      setViewportHeight(window.innerHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

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
        <ScrollArea
        // h={`calc(${viewportHeight}px - ${rem(130)})`}
        // h={`${viewportHeight} - ${rem(130)}px`}
        // style={{ height: `${viewportHeight} - ${rem(130)}` }}
         className={classScrollArea} 
         type="never" viewportRef={viewport}>
            {agentConversation?.messages?.map((message) => (
                <MessageFrame conversationID={props.conversationID} mainAgent="Customer" key={message.localID} message={message} />
            ))}
        </ScrollArea>
    );
}