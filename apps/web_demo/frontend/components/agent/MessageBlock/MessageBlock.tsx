import { Message } from "@/stores/TypeAgentChat";
import UserMessageBlock from "./MessageType/UserMessageBlock";
import AgentMessageBlock from "./MessageType/AgentMessageBlock";
import classes from './MessageBlock.module.css';

type MessageBlockProps = {
    message: Message;
}

export default function MessageBlock(props: MessageBlockProps) {
    const role = props.message.role
    return role == "user" ? (
        <UserMessageBlock message={props.message} />
      ) : role == "main" ? (
        <AgentMessageBlock message={props.message} />
      ) : (
        <p>条件 A 和 B 都不满足。</p>
      )
}