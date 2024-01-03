import { Message } from "@/stores/TypeAgentChat";
import { ScrollArea, Text, rem } from "@mantine/core";
import MessageBlock from "../MessageBlock/MessageBlock";
import classes from './MessagesDisplay.module.css';

// type MessagesDisplayProps = {
//     messages: Message[];
// }

export default function MessagesDisplay() {
    return (
        <ScrollArea className={classes.scrollArea} type="never" >
            <MessageBlock message={{localID:"1", content:"你好", role:"user", name:"用户"}}/>
            <MessageBlock message={{localID:"2", content:'hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", name:"客户经理"}}/>
            <MessageBlock message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", name:"客户经理"}}/>
            <MessageBlock message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", name:"客户经理"}}/>
            <MessageBlock message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", name:"客户经理"}}/>
            <MessageBlock message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", name:"客户经理"}}/>
            <MessageBlock message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", name:"客户经理"}}/>
            <MessageBlock message={{localID:"2", content:'## hello \n不，使用 <>{...}</>（即 React Fragment）来封装 {conditionA ? ... : ...} 这种条件渲染表达式并不是必需的。React Fragment 主要用于在不添加额外 DOM 节点的情况下，将多个元素组合在一起。如果你的条件渲染表达式是组件返回的唯一元素，你不需要使用 Fragment。\n```python\nimport { Message } from "@/stores/TypeAgentChat";\n```', role:"main", name:"客户经理"}}/>

        </ScrollArea>
    );
}