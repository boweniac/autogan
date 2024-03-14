import { useEffect, useRef, useState } from "react";
import { useRouter } from 'next/router';
import { Box, Card, Drawer, Stack, rem } from "@mantine/core";
import CustTextarea from "@/components/agent/CustTextarea/CustTextarea";
import { HeaderMegaMenu } from "@/components/agent/HeaderMegaMenu/HeaderMegaMenu";
import { LeftTableOfContents } from "@/components/agent/LeftTableOfContents/LeftTableOfContents";
import RoleDisplay from "@/components/agent/RoleDisplay/RoleDisplay";
import MessagesDisplay from "@/components/agent/messages_display/MessagesDisplay";
import { burnAfterGetInitConversationRequestState, getAgentConversationInfoState, getAgentConversationMessageState, updateActivePageState } from "@/stores/LocalStoreActions";
import classes from './AgentFrame.module.css';
import { useDisclosure } from "@mantine/hooks";
import { AgentConversationSend, AutoTitle, addAgentConversation } from "./AgentFrameUtil";
import {LocalState, localStore} from "@/stores/LocalStore";
import { audioAndLipAPI } from "@/api/audio/audio_and_lip";
import { AudioAndLip } from "@/stores/TypeAudioAndLip";
import { avatarConfig } from "../avatar/Avatar/AvatarConfig";
import { getConversationsAPI } from "@/api/conversation/get_conversations";
import { getMessagesWhenChangedAPI } from "@/api/message/get_messages";
import SpeakButton from "./CustTextarea/AudioToText/SpeakToText";
import MarkdownBlock from "../message/MarkdownBlock/MarkdownBlock";


export default function AgentFrame() {
    // const roleWidth = rem(400)
    const router = useRouter();
    const queryConversationID = router.query.conversation_id as string | undefined;
    const agentAvatarMapping = localStore((state: LocalState) => state.agentAvatarMapping);
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);

    const [audioAndLip, setAudioAndLip] = useState<AudioAndLip | undefined>();
    const [agentRole, setAgentRole] = useState<string>("CustomerManager");
    const [avatarName, setAvatarName] = useState<string>(agentAvatarMapping["CustomerManager"]);
    const [textStack, setTextStack] = useState<AudioAndLip[]>([]);
    const [audioStack, setAudioStack] = useState<AudioAndLip[]>([]);
    const [speakText, setSpeakText] = useState<string>("");
    const muteState = localStore((state: LocalState) => state.muteState);

    const isGeting = useRef(false);
    const isPlaying = useRef(false);
    const isGetingAudio = useRef(false);
    // const avatarName = useRef(agentAvatarMapping["CustomerManager"]);
    const avatarVoice = useRef("");
    const lastMsgId = useRef("");
    const abortControllerRef = useRef<AbortController | null>(null);
    const avatarState = localStore((state: LocalState) => state.avatarState);

    // const messages = getAgentConversationMessageState(queryConversationID)

    // const messagesDisplayHeight = avatarState ? 
    const classConversationFrame = avatarState ? classes.conversationFrameAvatarOn : classes.conversationFrameAvatarOff;
    const classSpeakButton = avatarState ? classes.speakButtonAvatarOn : classes.speakButtonAvatarOff;

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
    // useEffect(() => {
    //     if (agentRole == "CustomerManager") {
    //         setAvatarName(agentAvatarMapping["CustomerManager"]);
    //     }
    // }, [avatarState]);

    useEffect(() => {
        if (agentRole == "CustomerManager") {
            setAvatarName(agentAvatarMapping["CustomerManager"]);
            setAudioAndLip({avatarName: agentAvatarMapping["CustomerManager"]})
        }
    }, [agentAvatarMapping]);

    const syncMessages = () => {
        if (queryConversationID) {
            getMessagesWhenChangedAPI(queryConversationID, lastMsgId.current)
        }
    }

    const getNextAudio = () => {
        setTextStack(prevTextStack => {
            if (prevTextStack && prevTextStack.length > 0) {
                isGeting.current = true
                const [nextText, ...textRest] = prevTextStack;
                getAudio(nextText);
                return textRest
            } else {
                isGeting.current = false
                return []
            }
          });
      }

      const getAudio = (audioLink: AudioAndLip) => {
        if (audioLink.text) {
            isGetingAudio.current = true
            audioAndLipAPI(audioLink.text, avatarConfig[agentAvatarMapping[audioLink.agentName || ""]].voice || "", 0.8).then((res)=>{
                isGetingAudio.current = false
                isGeting.current = false
                getNextAudio()
                setAudioStack(prevStack => [...prevStack, {...audioLink, ...res, avatarName: agentAvatarMapping[audioLink?.agentName || ""]}]);
                if (!isPlaying.current) {
                    playNextAudio();
                }
            }).catch(()=>{
                isGetingAudio.current = false
            })
        }
      }

    const playNextAudio = () => {
        setAudioStack(prevStack => {
            if (prevStack && prevStack.length > 0) {
                const [nextAudio, ...rest] = prevStack;
                isPlaying.current = true
                if (nextAudio.agentName && nextAudio.agentName != "Customer") {
                    setAgentRole(nextAudio.agentName)
                }
                setSpeakText(nextAudio.text || "")
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
        loadingEnd()
        handleCancel()
        setTextStack([])
        setAudioStack([])
        if (!value.startsWith("@")) {
            value = "@CustomerManager " + value
        }
        // 并非新对话
        if (queryConversationID == undefined) {
            addAgentConversation(value, router)
        } else {
            abortControllerRef.current = new AbortController();
            const signal = abortControllerRef.current.signal;
            loadingStart()
            AgentConversationSend(queryConversationID, value, signal, (text)=>{
                if (text) {
                    setTextStack(prevTextStack => {
                        return [...prevTextStack, text]
                    })
                    if (!isGeting.current && !muteState) {
                        getNextAudio();
                    }
                }
            }, () => {
                loadingEnd()
                if (!getAgentConversationInfoState(queryConversationID)?.title) {
                    const s = new AbortController().signal;
                    AutoTitle(queryConversationID, s, ()=>{})
                }
            }, () => loadingEnd())
        }
      };
      const handleCancel = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort(); // 取消请求
        }
    };

    useEffect(() => {
        updateActivePageState("/agent")
        getConversationsAPI().then((res: string[])=>{
            if (queryConversationID && !res.includes(queryConversationID)) {
                router.push("/agent").then()
            }
        })
    }, []);

    useEffect(() => {
        setTextStack([])
        setAudioStack([])
    }, [muteState]);

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
            h={`calc(${viewportHeight}px)`}
            w="100%"
            className={classes.agentFrame}
        >
            <Box
            className={classes.breakpointMd}
            >
            <LeftTableOfContents conversationID={queryConversationID} ></LeftTableOfContents>
            </Box>

            <Stack
                // h="100%"
                h={`calc(${viewportHeight}px)`}
                // h={viewportHeight}
                w="100%"
                gap={0}
            >
                <HeaderMegaMenu isLoading={isPlaying.current || isGetingAudio.current || isLoading} conversationID={queryConversationID} selectAvatarCallback={(v)=>{}} muteCallback={(v)=>{}}></HeaderMegaMenu>
                <Stack
                    h={`calc(${viewportHeight}px - ${rem(50)})`}
                    justify="flex-end"
                    gap={0}
                    className={classConversationFrame}
                >
                    <MessagesDisplay conversationID={queryConversationID} setLastMsgIdCallback={(value)=>{lastMsgId.current = value}} syncMessagesCallback={syncMessages}></MessagesDisplay>
                    {/* <CustTextarea conversationID={queryConversationID} isLoading={isLoading} callback={doSubmit} stopCallback={()=>{
                        loadingEnd()
                        handleCancel()
                        }} syncMessagesCallback={syncMessages}></CustTextarea>
                    <SpeakButton callback={doSubmit}></SpeakButton> */}
                </Stack>
            </Stack>
            <CustTextarea conversationID={queryConversationID} isLoading={isPlaying.current || isGetingAudio.current || isLoading} callback={doSubmit} stopCallback={()=>{
                        loadingEnd()
                        handleCancel()
                        setTextStack([])
                        setAudioStack([])
                        }} syncMessagesCallback={syncMessages}></CustTextarea>
                    <SpeakButton callback={doSubmit}></SpeakButton>
            
            <RoleDisplay audioAndLip={audioAndLip} audioEndCallback={()=>{
                playNextAudio()
            }}/>
        </Box>
    );
}