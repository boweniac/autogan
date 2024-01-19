import { useEffect, useRef, useState } from "react";
import { useRouter } from 'next/router';
import { Box, Button, ScrollArea, SegmentedControl, Stack, rem } from "@mantine/core";
import CustTextarea from "@/components/agent/CustTextarea/CustTextarea";
import { HeaderMegaMenu } from "@/components/agent/HeaderMegaMenu/HeaderMegaMenu";
import { LeftTableOfContents } from "@/components/agent/LeftTableOfContents/LeftTableOfContents";
import RoleDisplay from "@/components/agent/RoleDisplay/RoleDisplay";
import MessagesDisplay from "@/components/agent/MessagesDisplay/MessagesDisplay";
import { abortCurrentRequest, addAgentConversationState, burnAfterGetInitConversationRequest, getAgentConversationState, updateActivePageState, updateCurrentAbortController } from "@/stores/LocalStoreActions";
import classes from './AgentFrame.module.css';
import { useDisclosure } from "@mantine/hooks";
import { addAgentConversationAPI } from "@/api/add_conversation";
import { streamTestAPI } from "@/api/test";
import { AgentConversationSend, addAgentConversation, syncConversations, syncMessages } from "./AgentFrameUtil";
import { Message } from "@/stores/TypeAgentChat";
import { v4 as uuidv4 } from "uuid";
import MessageFrame from "./MessagesDisplay/Message/MessageFrame";
import {LocalState, localStore} from "@/stores/LocalStore";
import { audioAndLipAPI } from "@/api/audio_and_lip";
import AudioPlay from "./Audio/AudioPlay";
import { AudioAndLip, MouthCues } from "@/stores/TypeAudioAndLip";


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
    const [lipValue, setLipValue] = useState<string>();
    const agentConversations = localStore((state: LocalState) => state.agentConversations);
    const agentConversation = agentConversations.find((agentConversations) => agentConversations.id == queryConversationID);
    const [morphTargetName, setMorphTargetName] = useState<string>("viseme_O");
    const [textStack, setTextStack] = useState<string[]>([]);
    const [audioStack, setAudioStack] = useState<AudioAndLip[]>([]);
    const isGeting = useRef(false);
    const isPlaying = useRef(false);
    // const currentAbortController = new AbortController();
    // updateCurrentAbortController(currentAbortController)

    const getNextAudio = () => {
        setTextStack(prevTextStack => {
            console.log(`prevTextStack2:`+JSON.stringify(prevTextStack));
            if (prevTextStack && prevTextStack.length > 0) {
                isGeting.current = true
                const [nextText, ...textRest] = prevTextStack;
                console.log(`nextText:`+JSON.stringify(nextText));
                getAudio(nextText);
                console.log(`textRest:`+JSON.stringify(textRest));
                return textRest
            } else {
                isGeting.current = false
                return []
            }
          });
      }

      const getAudio = (audioLink: string) => {
        audioAndLipAPI(audioLink, "onyx", 1).then((res)=>{
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
                console.log(`prevStack:`+JSON.stringify(prevStack));
                const [nextAudio, ...rest] = prevStack;
                console.log(`nextAudio:`+JSON.stringify(nextAudio));
                console.log(`rest:`+JSON.stringify(rest));
                playAudio(nextAudio); // 播放下一个音频
                return rest
            } else {
                isPlaying.current = false
                return []
            }
          });
      }

      const playAudio = (audioLink: AudioAndLip) => {
        const audio = new Audio(`${audioLink.audioFile}`)
            audio.play()
                .then(() => {
                    isPlaying.current = true
                    console.log("Audio is playing");
                })
                .catch(error => {
                    isPlaying.current = false
                    console.error("Error playing audio", error);
                });
                const handleTimeUpdate = () => {
                    const currentTime = audio.currentTime;
                    for (let i = 0; i < audioLink.lipsData.length; i++) {
                        const lipsData = audioLink.lipsData[i] as MouthCues;
                        if (currentTime >= lipsData.start && currentTime <= lipsData.end) {
                            setLipValue(lipsData.value)
                          break
                        }
                      }
                };
              audio.ontimeupdate = () => {
                handleTimeUpdate();
            };
            audio.addEventListener('ended', () => {
                console.log('音频播放结束');
                playNextAudio();
                // 在这里执行你需要的操作，比如播放下一个音频
              });
      }
    useEffect(() => {
        if (router.isReady) {
            if (queryConversationID != undefined && agentConversation == undefined) {
                router.push("/agent").then()
            } else {
                updateActivePageState("/agent")
                syncConversations().then((deletedConversations)=>{
                    if (queryConversationID != undefined && deletedConversations.includes(queryConversationID)) {
                        router.push("/agent").then()
                    }
                })
                if (queryConversationID != undefined) {
                    const initConversationRequest = burnAfterGetInitConversationRequest()
                    if (initConversationRequest != "") {
                        doSubmit(initConversationRequest)
                    } else {
                        syncMessages(queryConversationID)
                    }
                }
            }
            // getConversations()
        }
    }, [router.isReady]);
    

    // useEffect(() => {
    //     if (speakText) {
    //         console.log(`speakText:`+JSON.stringify(speakText));
    //         setTextStack(prevTextStack => [...prevTextStack, speakText])
    //         if (!isGeting.current) {
    //             getNextAudio();
    //         }
    //     }
    // }, [speakText]);


    const doSubmit = async (value: string) => {
        // 并非新对话
        if (queryConversationID == undefined) {
            addAgentConversation(value, router)
        } else {
            AgentConversationSend(queryConversationID, value, (text)=>{
                if (text) {
                    console.log(`speakText:`+JSON.stringify(text));
                    setTextStack(prevTextStack => {
                        console.log(`prevTextStack:`+JSON.stringify(prevTextStack));
                        return [...prevTextStack, text]
                    })
                    if (!isGeting.current) {
                        getNextAudio();
                    }
                }
            })
        }
      };

    return (
        <Box
            h={`calc(100vh)`}
            w="100%"
            className={classes.agentFrame}
        >
            <LeftTableOfContents conversationID={queryConversationID} ></LeftTableOfContents>
            {/* <SegmentedControl
                value={morphTargetName}
                onChange={setMorphTargetName}
                data={[
                    { label: 'viseme_RR', value: 'viseme_RR' },
                    { label: 'viseme_aa', value: 'viseme_aa' },
                    { label: 'viseme_E', value: 'viseme_E' },
                    { label: 'viseme_I', value: 'viseme_I' },
                    { label: 'viseme_O', value: 'viseme_O' },
                ]}
                /> */}
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
                    <MessagesDisplay messages={agentConversation?.messages} ></MessagesDisplay>
                    <CustTextarea conversationID={queryConversationID} isLoading={isLoading} callback={doSubmit} ></CustTextarea>
                </Stack>
            </Stack>
            <Button 
                onClick={()=>{abortCurrentRequest()}} 
            >
            停止链接
            </Button>
            <RoleDisplay morphTargetName={morphTargetName} audioAndLip={audioAndLip} lipValue={lipValue}/>
            {/* <AudioPlay src={audioAndLip?.audioFile} onFinishedPlaying={()=>console.log(`播放完成`)} onPlaying={()=>{}}></AudioPlay> */}
            {/* <AudioPlay src={audioSrc} onFinishedPlaying={()=>console.log(`播放完成`)}></AudioPlay> */}
        </Box>
    );
}