import { useEffect, useRef, useState } from "react";
import { useRouter } from 'next/router';
import { Box, Stack, rem } from "@mantine/core";
import CustTextarea from "@/components/agent/CustTextarea/CustTextarea";
import { HeaderMegaMenu } from "@/components/agent/HeaderMegaMenu/HeaderMegaMenu";
import { LeftTableOfContents } from "@/components/agent/LeftTableOfContents/LeftTableOfContents";
import RoleDisplay from "@/components/agent/RoleDisplay/RoleDisplay";
import MessagesDisplay from "@/components/agent/messages_display/MessagesDisplay";
import { burnAfterGetInitConversationRequestState, getAgentConversationMessageState, updateActivePageState } from "@/stores/LocalStoreActions";
import classes from './AgentFrame.module.css';
import { useDisclosure } from "@mantine/hooks";
import { AgentConversationSend, addAgentConversation } from "./AgentFrameUtil";
import {LocalState, localStore} from "@/stores/LocalStore";
import { audioAndLipAPI } from "@/api/audio/audio_and_lip";
import { AudioAndLip } from "@/stores/TypeAudioAndLip";
import { avatarConfig } from "../avatar/Avatar/AvatarConfig";
import { getConversationsAPI } from "@/api/conversation/get_conversations";
import { getMessagesWhenChangedAPI } from "@/api/message/get_messages";


export default function AgentFrame() {
    const roleWidth = rem(400)
    const router = useRouter();
    const queryConversationID = router.query.conversation_id as string | undefined;
    const agentAvatarMapping = localStore((state: LocalState) => state.agentAvatarMapping);
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);

    const [audioAndLip, setAudioAndLip] = useState<AudioAndLip>();
    const [agentRole, setAgentRole] = useState<string>("CustomerManager");
    const [avatarName, setAvatarName] = useState<string>(agentAvatarMapping["CustomerManager"]);
    const [textStack, setTextStack] = useState<string[]>([]);
    const [audioStack, setAudioStack] = useState<AudioAndLip[]>([]);

    const isGeting = useRef(false);
    const isPlaying = useRef(false);
    // const avatarName = useRef(agentAvatarMapping["CustomerManager"]);
    const avatarVoice = useRef("");
    const lastMsgId = useRef("");
    const abortControllerRef = useRef<AbortController | null>(null);

    // const messages = getAgentConversationMessageState(queryConversationID)

    useEffect(() => {
        if (agentRole == "CustomerManager") {
            setAvatarName(agentAvatarMapping["CustomerManager"]);
        }
    }, [agentAvatarMapping]);

    const syncMessages = () => {
        if (queryConversationID) {
            getMessagesWhenChangedAPI(queryConversationID, lastMsgId.current)
        }
    }

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
                        // getNextAudio();
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

    useEffect(() => {
        updateActivePageState("/agent")
        getConversationsAPI().then((res: string[])=>{
            console.log(`res:`+JSON.stringify(res));
            if (queryConversationID && !res.includes(queryConversationID)) {
                router.push("/agent").then()
            }
        })
    }, []);

    useEffect(() => {
        if (router.isReady && queryConversationID) {
            const initConversationRequest = burnAfterGetInitConversationRequestState()
            if (initConversationRequest) {
                doSubmit(initConversationRequest)
            }
        }
    }, [router.isReady]);

    useEffect(() => {
        setAvatarName(agentAvatarMapping[agentRole])
        avatarVoice.current = avatarConfig[avatarName].voice || ""
    }, [agentRole]);

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
                <HeaderMegaMenu selectAvatarCallback={(v)=>{}} muteCallback={(v)=>{}}></HeaderMegaMenu>
                <Stack
                    // h="100%"
                    h={`calc(100vh - ${rem(50)})`}
                    justify="space-between"
                    gap={0}
                    className={classes.conversationFrame}
                    style={{ marginRight: roleWidth}}
                >
                    <MessagesDisplay conversationID={queryConversationID} setLastMsgIdCallback={(value)=>{lastMsgId.current = value}} syncMessagesCallback={syncMessages}></MessagesDisplay>
                    <CustTextarea conversationID={queryConversationID} isLoading={isLoading} callback={doSubmit} stopCallback={()=>{
                        loadingEnd()
                        handleCancel()
                        }} syncMessagesCallback={syncMessages}></CustTextarea>
                </Stack>
            </Stack>
            
            <RoleDisplay avatarName={avatarName} audioAndLip={audioAndLip} audioEndCallback={()=>{
                playNextAudio()
            }}/>
        </Box>
    );
}