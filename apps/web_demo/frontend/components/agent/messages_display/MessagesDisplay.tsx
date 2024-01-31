import { Message } from "@/stores/TypeAgentChat";
import { ScrollArea, Text, rem } from "@mantine/core";
import MessageFrame from "../../message/MessageFrame";
import classes from './MessagesDisplay.module.css';
import { LocalState, localStore } from "@/stores/LocalStore";
import { useEffect } from "react";
import { useRouter } from "next/router";
import { burnAfterGetInitConversationRequestState, updateActivePageState } from "@/stores/LocalStoreActions";
import { syncConversations, syncMessages } from "../AgentFrameUtil";

type MessagesDisplayProps = {
    queryConversationID: string | undefined;
    doSubmit: (value: string) => void
}

export default function MessagesDisplay(props: MessagesDisplayProps) {
    const router = useRouter();
    const agentConversations = localStore((state: LocalState) => state.agentConversations);
    const agentConversation = agentConversations.find((agentConversations) => agentConversations.id == props.queryConversationID);

    useEffect(() => {
        if (router.isReady) {
            if (props.queryConversationID != undefined && agentConversation == undefined) {
                router.push("/agent").then()
            } else {
                updateActivePageState("/agent")
                syncConversations().then((deletedConversations)=>{
                    if (props.queryConversationID != undefined && deletedConversations.includes(props.queryConversationID)) {
                        router.push("/agent").then()
                    }
                })
                if (props.queryConversationID != undefined) {
                    const initConversationRequest = burnAfterGetInitConversationRequestState()
                    if (initConversationRequest != "") {
                        props.doSubmit(initConversationRequest)
                    } else {
                        syncMessages(props.queryConversationID)
                    }
                }
            }
            // getConversations()
        }
    }, [router.isReady]);
    
    return (
        
        <ScrollArea className={classes.scrollArea} type="never" >
            {agentConversation?.messages?.map((message) => (
                <MessageFrame mainAgent="Customer" key={message.localID} message={message} />
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