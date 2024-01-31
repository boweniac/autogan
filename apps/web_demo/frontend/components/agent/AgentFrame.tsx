import { useEffect, useRef, useState } from "react";
import { useRouter } from 'next/router';
import { Box, Button, ScrollArea, SegmentedControl, Stack, rem } from "@mantine/core";
import CustTextarea from "@/components/agent/CustTextarea/CustTextarea";
import { HeaderMegaMenu } from "@/components/agent/HeaderMegaMenu/HeaderMegaMenu";
import { LeftTableOfContents } from "@/components/agent/LeftTableOfContents/LeftTableOfContents";
import RoleDisplay from "@/components/agent/RoleDisplay/RoleDisplay";
import MessagesDisplay from "@/components/agent/messages_display/MessagesDisplay";
import { addAgentConversationState, burnAfterGetInitConversationRequestState, getAgentConversationState, updateActivePageState } from "@/stores/LocalStoreActions";
import classes from './AgentFrame.module.css';
import { useDisclosure } from "@mantine/hooks";
import { addAgentConversationAPI } from "@/api/add_conversation";
import { streamTestAPI } from "@/api/request_open";
import { AgentConversationSend, addAgentConversation, syncConversations, syncMessages } from "./AgentFrameUtil";
import { Message } from "@/stores/TypeAgentChat";
import { v4 as uuidv4 } from "uuid";
import MessageFrame from "../message/MessageFrame";
import {LocalState, localStore} from "@/stores/LocalStore";
import { audioAndLipAPI } from "@/api/audio_and_lip";
import { AudioAndLip, MouthCues } from "@/stores/TypeAudioAndLip";
import { notifications } from "@mantine/notifications";
import { avatarConfig } from "../avatar/Avatar/AvatarConfig";


export default function AgentFrame() {
    const router = useRouter();
    const queryConversationID = router.query.conversation_id as string | undefined;
    // getConversations()
    const roleWidth = rem(400)
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);
    // const [test, setTest] = useState<string>("");
    const [message, setMessage] = useState<Message | undefined>(undefined);
    const [messages, setMessages] = useState<Message[]>([]);
    const [speakText, setSpeakText] = useState<string>("");
    const [audioAndLip, setAudioAndLip] = useState<AudioAndLip>();
    // const [lipValue, setLipValue] = useState<string>();
    const agentAvatarMapping = localStore((state: LocalState) => state.agentAvatarMapping);
    const [agentRole, setAgentRole] = useState<string>("CustomerManager");
    const avatarName = useRef("boy");
    const avatarVoice = useRef("");
    // const agentConversations = localStore((state: LocalState) => state.agentConversations);
    // const agentConversation = agentConversations.find((agentConversations) => agentConversations.id == queryConversationID);
    const [morphTargetName, setMorphTargetName] = useState<string>("viseme_O");
    const [textStack, setTextStack] = useState<string[]>([]);
    const [audioStack, setAudioStack] = useState<AudioAndLip[]>([]);
    const isGeting = useRef(false);
    const isPlaying = useRef(false);
    const abortControllerRef = useRef<AbortController | null>(null);
    // const [currentMorphTargetHolder, setSpeakText] = useState<string>("");
    // new Audio()
    // const currentAbortController = new AbortController();
    // updateCurrentAbortController(currentAbortController)


    const getNextAudio = () => {
        setTextStack(prevTextStack => {
            // console.log(`prevTextStack2:`+JSON.stringify(prevTextStack));
            if (prevTextStack && prevTextStack.length > 0) {
                isGeting.current = true
                const [nextText, ...textRest] = prevTextStack;
                // console.log(`nextText:`+JSON.stringify(nextText));
                getAudio(nextText);
                // console.log(`textRest:`+JSON.stringify(textRest));
                return textRest
            } else {
                isGeting.current = false
                return []
            }
          });
      }

      const getAudio = (audioLink: string) => {
        audioAndLipAPI(audioLink, avatarVoice.current, 1).then((res)=>{
            isGeting.current = false
            getNextAudio()
            setAudioStack(prevStack => [...prevStack, res]);
            if (!isPlaying.current) {
                playNextAudio();
            }
        })
      }

    const playNextAudio = () => {
        setAudioStack(prevStack => {
            if (prevStack && prevStack.length > 0) {
                // console.log(`prevStack:`+JSON.stringify(prevStack));
                const [nextAudio, ...rest] = prevStack;
                // console.log(`nextAudio:`+JSON.stringify(nextAudio));
                // console.log(`rest:`+JSON.stringify(rest));
                isPlaying.current = true
                setAudioAndLip(nextAudio)
                // playAudio(nextAudio); // 播放下一个音频
                return rest
            } else {
                isPlaying.current = false
                return []
            }
          });
      }

    // useEffect(() => {
    //     if (router.isReady) {
    //         if (queryConversationID != undefined && agentConversation == undefined) {
    //             router.push("/agent").then()
    //         } else {
    //             updateActivePageState("/agent")
    //             syncConversations().then((deletedConversations)=>{
    //                 if (queryConversationID != undefined && deletedConversations.includes(queryConversationID)) {
    //                     router.push("/agent").then()
    //                 }
    //             })
    //             if (queryConversationID != undefined) {
    //                 const initConversationRequest = burnAfterGetInitConversationRequestState()
    //                 if (initConversationRequest != "") {
    //                     doSubmit(initConversationRequest)
    //                 } else {
    //                     syncMessages(queryConversationID)
    //                 }
    //             }
    //         }
    //         // getConversations()
    //     }
    // }, [router.isReady]);

    useEffect(() => {
        avatarName.current = agentAvatarMapping[agentRole]
        avatarVoice.current = avatarConfig[avatarName.current].voice
    }, [agentRole]);


    const doSubmit = async (value: string) => {
        // 并非新对话
        if (queryConversationID == undefined) {
            addAgentConversation(value, router)
        } else {
            abortControllerRef.current = new AbortController();
            const signal = abortControllerRef.current.signal;
            loadingStart()
            AgentConversationSend(queryConversationID, value, signal, (text)=>{
                if (text) {
                    // console.log(`speakText:`+JSON.stringify(text));
                    setTextStack(prevTextStack => {
                        // console.log(`prevTextStack:`+JSON.stringify(prevTextStack));
                        return [...prevTextStack, text]
                    })
                    if (!isGeting.current) {
                        getNextAudio();
                    }
                }
            }, () => loadingEnd(), () => loadingEnd())
        }
      };
      const handleCancel = () => {
        console.log(`点击 1:`);
        if (abortControllerRef.current) {
            console.log(`点击 2:`);
            abortControllerRef.current.abort(); // 取消请求
        }
    };

    return (
        <Box
            h={`calc(100vh)`}
            w="100%"
            className={classes.agentFrame}
        >
            <LeftTableOfContents conversationID={queryConversationID} ></LeftTableOfContents>

            <Stack
                h="100%"
                w="100%"
                gap={0}
            >
                <HeaderMegaMenu></HeaderMegaMenu>
                <Stack
                    // h="100%"
                    h={`calc(100vh - ${rem(50)})`}
                    justify="space-between"
                    gap={0}
                    className={classes.conversationFrame}
                    style={{ marginRight: roleWidth}}
                >
                    <MessagesDisplay queryConversationID={queryConversationID} doSubmit={doSubmit} ></MessagesDisplay>
                    <CustTextarea conversationID={queryConversationID} isLoading={isLoading} callback={doSubmit} stopCallback={()=>{
                        loadingEnd()
                        handleCancel()
                        }} ></CustTextarea>
                </Stack>
            </Stack>
            
            <RoleDisplay avatarName={avatarName.current} audioAndLip={audioAndLip} audioEndCallback={()=>{
                playNextAudio()
            }}/>
        </Box>
    );
}