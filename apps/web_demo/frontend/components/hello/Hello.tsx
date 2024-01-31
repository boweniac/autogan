import { useEffect, useRef, useState } from "react";
import { useRouter } from 'next/router';
import { Box, Button, ScrollArea, SegmentedControl, Stack, Title, Transition, rem } from "@mantine/core";
import RoleDisplay from "@/components/hello/RoleDisplay/RoleDisplay";
import classes from './Hello.module.css';
import { useDisclosure } from "@mantine/hooks";
import { Message } from "@/stores/TypeAgentChat";
import {LocalState, localStore} from "@/stores/LocalStore";
import { AudioAndLip, MouthCues } from "@/stores/TypeAudioAndLip";
import { avatarConfig } from "../avatar/Avatar/AvatarConfig";
import { AgentIntroductionSend } from "./HelloUtil";
import MessagesDisplay from "./messages_display/MessagesDisplay";
import RoleDisplayHello from "./RoleDisplay/RoleDisplayHello";
import RoleDisplayHelloTitle from "./RoleDisplay/RoleDisplayHelloTitle";
import RoleDisplayHelloButton from "./RoleDisplay/RoleDisplayHelloButton";
import { resetIntroductionConversationsState, updateHelloStartState } from "@/stores/LocalStoreActions";


export default function Hello() {
    const router = useRouter();
    // getConversations()
    const roleWidth = rem(400)
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);
    // const [test, setTest] = useState<string>("");
    const [message, setMessage] = useState<Message | undefined>(undefined);
    const [messages, setMessages] = useState<Message[]>([]);
    const [speakText, setSpeakText] = useState<string>("");
    const [audioAndLip, setAudioAndLip] = useState<AudioAndLip>();
    const [lipValue, setLipValue] = useState<string>();
    const agentAvatarMapping = localStore((state: LocalState) => state.agentAvatarMapping);
    const [agentRole, setAgentRole] = useState<string>("CustomerManager");
    const avatarName = useRef("boy");
    const avatarVoice = useRef("");
    // const agentConversation = localStore((state: LocalState) => state.introductionConversations);
    // const agentConversation = agentConversations.find((agentConversations) => agentConversations.id == queryConversationID);
    const [morphTargetName, setMorphTargetName] = useState<string>("viseme_O");
    const [textStack, setTextStack] = useState<string[]>([]);
    const [audioStack, setAudioStack] = useState<AudioAndLip[]>([]);
    const isGeting = useRef(false);
    const isPlaying = useRef(false);
    const abortControllerRef = useRef<AbortController | null>(null);
    // const helloStart = localStore((state: LocalState) => state.helloStart);
    const [helloStart, setHelloStart] = useState<boolean>(false);
    const [introductionStart, setIntroductionStart] = useState<boolean>(false);
    // const [currentMorphTargetHolder, setSpeakText] = useState<string>("");
    // new Audio()
    // const currentAbortController = new AbortController();
    // updateCurrentAbortController(currentAbortController)


    // const getNextAudio = () => {
    //     setTextStack(prevTextStack => {
    //         // console.log(`prevTextStack2:`+JSON.stringify(prevTextStack));
    //         if (prevTextStack && prevTextStack.length > 0) {
    //             isGeting.current = true
    //             const [nextText, ...textRest] = prevTextStack;
    //             // console.log(`nextText:`+JSON.stringify(nextText));
    //             getAudio(nextText);
    //             // console.log(`textRest:`+JSON.stringify(textRest));
    //             return textRest
    //         } else {
    //             isGeting.current = false
    //             return []
    //         }
    //       });
    //   }

    //   const getAudio = (audioLink: string) => {
    //     audioAndLipAPI(audioLink, avatarVoice.current, 1).then((res)=>{
    //         isGeting.current = false
    //         getNextAudio()
    //         setAudioStack(prevStack => [...prevStack, res]);
    //         if (!isPlaying.current) {
    //             playNextAudio();
    //         }
    //     })
    //   }

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
    //     startIntroduction("introduction")
    // }, []);

    // useEffect(() => {
    //     if (router.isReady) {
    //         updateHelloStartState(false)
    //     }
    // }, [router.isReady]);
    useEffect(() => {
        resetIntroductionConversationsState()
    }, []);

    useEffect(() => {
        if (router.isReady && helloStart) {
            setIntroductionStart(true)
        }
    }, [router.isReady, helloStart]);

    useEffect(() => {
        avatarName.current = agentAvatarMapping[agentRole]
        avatarVoice.current = avatarConfig[avatarName.current].voice
        // startIntroduction("introduction")
    }, [agentRole]);
    


    const startIntroduction = async (caseID: string) => {
        AgentIntroductionSend(caseID, (value)=>{
            if (value) {
                setAudioStack(prevStack => [...prevStack, value]);
                if (!isPlaying.current) {
                    playNextAudio();
                }
            }
        }, () => loadingEnd(), () => loadingEnd())
      };

    const handleCancel = () => {
        console.log(`点击 1:`);
        if (abortControllerRef.current) {
            console.log(`点击 2:`);
            abortControllerRef.current.abort(); // 取消请求
        }
    };

    return (
        <>
            {
                helloStart ? <Box
                h={`calc(100vh)`}
                w="100%"
                className={classes.agentFrame}
            >
    
                <Stack
                        w="100%"
                        h={`calc(100vh - ${rem(50)})`}
                        justify="space-between"
                        gap={0}
                        className={classes.conversationFrame}
                        style={{ marginRight: roleWidth}}
                    >
                        <Transition mounted={introductionStart} transition="fade" duration={1000} timingFunction="ease">
                            {(styles) => <Title style={styles} mb="lg" mt={100} size={80} order={1}> 数字员工 </Title>}
                        </Transition>
                        <MessagesDisplay startSayHello={introductionStart} playAudio={(audioAndLip)=>{
                            setAudioStack(prevStack => [...prevStack, audioAndLip]);
                            if (!isPlaying.current) {
                                playNextAudio();
                            }
                        }} selectCallback={(value)=>{
                            startIntroduction(value)
                        }}></MessagesDisplay>
                    </Stack>
                <RoleDisplay avatarName={avatarName.current} audioAndLip={audioAndLip} audioEndCallback={()=>{
                    playNextAudio()
                }}/>
            </Box> : <Box
                h={`calc(100vh)`}
                w="100%"
                className={classes.agentFrame}
            >
    
                {/* <Transition mounted={!helloStart} transition="fade" duration={600} timingFunction="ease">
                            {(styles) => <div style={styles}>Fade In Content</div>}
                        </Transition> */}
                <RoleDisplayHelloTitle></RoleDisplayHelloTitle>
                <RoleDisplayHello avatarName={avatarName.current}  />
                <RoleDisplayHelloButton clickIntroductionCallback={()=>setHelloStart(true)} clickAgentCallback={()=>{
                    router.push("/agent")
                }}></RoleDisplayHelloButton>
            </Box>
            }
        </>
    );
}