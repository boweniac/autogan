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

    const [audioAndLip, setAudioAndLip] = useState<AudioAndLip>();
    const [agentRole, setAgentRole] = useState<string>("CustomerManager");
    const [avatarName, setAvatarName] = useState<string>(agentAvatarMapping["CustomerManager"]);
    const [textStack, setTextStack] = useState<AudioAndLip[]>([]);
    const [audioStack, setAudioStack] = useState<AudioAndLip[]>([]);
    const [speakText, setSpeakText] = useState<string>("");
    const muteState = localStore((state: LocalState) => state.muteState);

    const isGeting = useRef(false);
    const isPlaying = useRef(false);
    // const avatarName = useRef(agentAvatarMapping["CustomerManager"]);
    const avatarVoice = useRef("");
    const lastMsgId = useRef("");
    const abortControllerRef = useRef<AbortController | null>(null);
    const avatarState = localStore((state: LocalState) => state.avatarState);

    // const messages = getAgentConversationMessageState(queryConversationID)

    const classConversationFrame = avatarState ? classes.conversationFrameAvatarOn : classes.conversationFrameAvatarOff;
    const classSpeakButton = avatarState ? classes.speakButtonAvatarOn : classes.speakButtonAvatarOff;
    const [height, setHeight] = useState(window.innerHeight + 'px');
    // useEffect(() => {
    //     if (agentRole == "CustomerManager") {
    //         setAvatarName(agentAvatarMapping["CustomerManager"]);
    //     }
    // }, [avatarState]);

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
            audioAndLipAPI(audioLink.text, avatarConfig[agentAvatarMapping[audioLink.agentName || ""]].voice || "", 1).then((res)=>{
                isGeting.current = false
                getNextAudio()
                setAudioStack(prevStack => [...prevStack, {...audioLink, ...res, avatarName: agentAvatarMapping[audioLink?.agentName || ""]}]);
                if (!isPlaying.current) {
                    playNextAudio();
                }
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
                console.log(`getAgentConversationInfoState(queryConversationID):`+JSON.stringify(getAgentConversationInfoState(queryConversationID)));
                console.log(`getAgentConversationInfoState(queryConversationID)?.title:`+JSON.stringify(getAgentConversationInfoState(queryConversationID)?.title));
                if (!getAgentConversationInfoState(queryConversationID)?.title) {
                    console.log(`lslslslsl:`);
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

        // 定义一个函数来更新高度
        const updateHeight = () => {
            setHeight(window.innerHeight + 'px');
        };
    
        // 在组件挂载时设置高度
        updateHeight();
    
        // 监听窗口大小变化事件，以便更新高度
        window.addEventListener('resize', updateHeight);
    
        // 组件卸载时移除事件监听器
        return () => window.removeEventListener('resize', updateHeight);
    }, []);

    useEffect(() => {
        setTextStack(prevTextStack => {
            return []
        })
        setAudioStack(prevTextStack => {
            return []
        })
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
            h={`calc(100vh)`}
            w="100%"
            className={classes.agentFrame}
        >
            <Box
            className={classes.breakpointMd}
            >
            <LeftTableOfContents conversationID={queryConversationID} ></LeftTableOfContents>
            </Box>

            <Stack
                h="100%"
                w="100%"
                gap={0}
            >
                <HeaderMegaMenu conversationID={queryConversationID} selectAvatarCallback={(v)=>{}} muteCallback={(v)=>{}}></HeaderMegaMenu>
                <Stack
                    // h="100%"
                    h={`calc(${height} - ${rem(50)})`}
                    justify="flex-end"
                    gap={0}
                    className={classConversationFrame}
                >
                    <MessagesDisplay conversationID={queryConversationID} setLastMsgIdCallback={(value)=>{lastMsgId.current = value}} syncMessagesCallback={syncMessages}></MessagesDisplay>
                    <CustTextarea conversationID={queryConversationID} isLoading={isLoading} callback={doSubmit} stopCallback={()=>{
                        loadingEnd()
                        handleCancel()
                        }} syncMessagesCallback={syncMessages}></CustTextarea>
                    <SpeakButton callback={doSubmit}></SpeakButton>
                </Stack>
                {/* <Stack
                    h={`calc(100vh - ${rem(50)})`}
                    w="100%"
                    align="center"
                    justify="flex-end"
                    // className={classSpeakButton}
                >
                    {
                        speakText && <Card
                        padding="sm"
                        radius="md"
                        // maw={`calc(100vw - ${rem(400)} - ${rem(364)})`}
                        className={ `${classes.messageBlock} ${classes.messageLeft}` }
                        >
                            <MarkdownBlock content_type="main" content_tag="" content={speakText}></MarkdownBlock>
                        </Card>
                    }
                    <SpeakButton callback={doSubmit}></SpeakButton>
                </Stack> */}
            </Stack>
            
            <RoleDisplay avatarName={avatarName} audioAndLip={audioAndLip} audioEndCallback={()=>{
                playNextAudio()
            }}/>
        </Box>
    );
}