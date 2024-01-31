import { Message } from "@/stores/TypeAgentChat";
import { Blockquote, Container, ScrollArea, Text, Title, Transition, rem } from "@mantine/core";
import MessageFrame from "../../message/MessageFrame";
import classes from './MessagesDisplay.module.css';
import { LocalState, localStore } from "@/stores/LocalStore";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/router";
import { burnAfterGetInitConversationRequestState, resetIntroductionConversationsState, updateActivePageState } from "@/stores/LocalStoreActions";
import { helloAudioAndLip, helloTextString } from "../HelloUtil";
import { AudioAndLip, LipsData } from "@/stores/TypeAudioAndLip";
import { SelectCard } from "../select_card/SelectCard";

type MessagesDisplayProps = {
    startSayHello: boolean;
    playAudio: (audioAndLip: AudioAndLip)=>void
    selectCallback: (value: string)=>void
  }

export default function MessagesDisplay(props: MessagesDisplayProps) {
    const router = useRouter();
    const [hello, setHello] = useState<boolean>(false);
    const [helloText, setHelloText] = useState<string>("");
    const [helloSelect, setHelloSelect] = useState<boolean>(false);
    const agentConversation = localStore((state: LocalState) => state.introductionConversations);
    const selectCaseID = useRef("");

    useEffect(() => {
        if (router.isReady) {
            setHello(true)
            props.playAudio(helloAudioAndLip)
            let currentChar = 0;
            let prevText = ""
            const typeWriter = setInterval(() => {
                prevText += helloTextString[currentChar]
                setHelloText(prevText)
                currentChar++;
                if (currentChar === helloTextString.length) clearInterval(typeWriter);
            }, 200);
        }
    }, [router.isReady]);

    useEffect(() => {
        // 当 yourVariable 变化时，设置一个1秒的延时
        const timer = setTimeout(() => {
            setHelloSelect(true)
        }, 1000);
    
        // 如果 yourVariable 在1秒内再次变化，清除上一个定时器
        return () => clearTimeout(timer);
      }, [agentConversation]); // 依赖列表中包含 yourVariable



    return (
        <ScrollArea className={classes.scrollArea} type="never" >
             <Transition
                mounted={hello}
                transition="fade"
                duration={1000}
                timingFunction="ease"
                onEntered={()=>{setHelloSelect(true)}}
                >
                {(styles) => <Blockquote style={styles} cite="– 客户经理">
                        {helloText}
                    </Blockquote>}
            </Transition>
            {agentConversation?.map((message) => (
                <MessageFrame mainAgent="Customer" key={message.localID} message={message} />
            ))}
            <Transition
                mounted={helloSelect}
                transition="fade"
                duration={1000}
                timingFunction="ease"
                onExited={()=>{
                    resetIntroductionConversationsState()
                    props.selectCallback(selectCaseID.current)
                }}
                >
                {(styles) => <Container style={styles} mt={30} mb={30} size="lg">
                        <SelectCard callback={(value)=>{
                            if (value == "/agent") {
                                router.push("/agent")
                            } else {
                                selectCaseID.current = value
                                setHello(false)
                                setHelloSelect(false)
                                // props.selectCallback(value)
                            }
                        }}></SelectCard>
                    </Container>}
            </Transition>
        </ScrollArea>
    );
}