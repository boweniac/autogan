import { Message } from "@/stores/TypeAgentChat";
import { ScrollArea, Text, rem } from "@mantine/core";
import MessageFrame from "./Message/MessageFrame";
import classes from './MessagesDisplay.module.css';

type MessagesDisplayProps = {
    messages: Message[] | undefined;
}

export default function MessagesDisplay(props: MessagesDisplayProps) {
    // const [messages, setMessages] = useState<Message[]>([]);
    
    return (
        
        <ScrollArea className={classes.scrollArea} type="never" >
            {props.messages?.map((message) => (
                <MessageFrame key={message.localID} message={message} />
            ))}
            {/* <MessageFrame message={{localID:"1", content:'undefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefinedundefined', role:"user", agentName:"用户"}}/> */}
            {/* <MessageFrame message={{localID:"1", content:'hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...}', role:"user", agentName:"用户"}}/>
            <MessageFrame message={{localID:"2", content:'使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...}', role:"main", agentName:"客户经理"}}/>
            <MessageFrame message={{localID:"2", role:"main", agentName:"客户经理"}}/>
            <MessageFrame message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", agentName:"客户经理"}}/>
            <MessageFrame message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", agentName:"客户经理"}}/>
            <MessageFrame message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", agentName:"客户经理"}}/>
            <MessageFrame message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", agentName:"客户经理"}}/>
            <MessageFrame message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", agentName:"客户经理"}}/> */}
        </ScrollArea>
    );
}