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
import { AgentIntroductionSend, convertToAudioAndLipDemo } from "./HelloUtil";
import MessagesDisplay from "./messages_display/MessagesDisplay";
import RoleDisplayHello from "./RoleDisplay/RoleDisplayHello";
import RoleDisplayHelloTitle from "./RoleDisplay/RoleDisplayHelloTitle";
import RoleDisplayHelloButton from "./RoleDisplay/RoleDisplayHelloButton";
import { resetIntroductionConversationsState, updateActivePageState } from "@/stores/LocalStoreActions";
import { HeaderMegaMenu } from "./HeaderMegaMenu/HeaderMegaMenu";
import MessagesDisplaySm from "./messages_display_sm/MessagesDisplaySm";


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
    // const avatarName = useRef("customerManagerGirl");
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
    const [avatarName, setAvatarName] = useState<string>(agentAvatarMapping["CustomerManager"]);
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
        updateActivePageState("/")
        resetIntroductionConversationsState()
    }, []);

    useEffect(() => {
        if (router.isReady && helloStart) {
            setIntroductionStart(true)
        }
    }, [router.isReady, helloStart]);

    useEffect(() => {
        if (agentRole == "CustomerManager") {
            setAvatarName(agentAvatarMapping["CustomerManager"]);
        }
    }, [agentAvatarMapping]);

    useEffect(() => {
        setAvatarName(agentAvatarMapping[agentRole])
        avatarVoice.current = avatarConfig[avatarName].voice || ""
    }, [agentRole]);
    


    const startIntroduction = async (caseID: string) => {
        AgentIntroductionSend(caseID, (value)=>{
            if (value) {
                const audioAndLip = convertToAudioAndLipDemo(value, agentAvatarMapping[value?.agentName || ""])
                setAudioStack(prevStack => [...prevStack, {...audioAndLip, avatarName: agentAvatarMapping[audioAndLip?.agentName || ""]}]);
                if (!isPlaying.current) {
                    playNextAudio();
                }
            }
        }, () => loadingEnd(), () => loadingEnd())
      };

    const handleCancel = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort(); // 取消请求
        }
    };

    return (
        <>
            {
                helloStart ? <Stack
                h={`calc(100vh)`}
                w="100%"
                className={classes.agentFrame}
            >
                <HeaderMegaMenu selectAvatarCallback={(v)=>{}} muteCallback={(v)=>{}}></HeaderMegaMenu>
                <Stack
                        w="100%"
                        h={`calc(100vh - ${rem(100)})`}
                        justify="space-between"
                        gap={0}
                        className={classes.conversationFrame}
                        style={{ marginRight: roleWidth}}
                    >
                        <Transition mounted={introductionStart} transition="fade" duration={1000} timingFunction="ease">
                            {(styles) => <Title className={classes.title} style={styles} mb="lg" size={80} order={1}> 人人都是 CEO </Title>}
                        </Transition>
                        <MessagesDisplay startSayHello={introductionStart} playAudio={(value)=>{
                            const audioAndLip = convertToAudioAndLipDemo(value, agentAvatarMapping[value?.agentName || ""])
                            setAudioStack(prevStack => [...prevStack, audioAndLip]);
                            if (!isPlaying.current) {
                                playNextAudio();
                            }
                        }} selectCallback={(value)=>{
                            startIntroduction(value)
                        }}></MessagesDisplay>
                    </Stack>
                <RoleDisplay avatarName={avatarName} audioAndLip={audioAndLip} audioEndCallback={()=>{
                    playNextAudio()
                }}/>
            </Stack> : <Box
                h={`calc(100vh)`}
                w="100%"
                className={classes.agentFrame}
            >
    
                {/* <Transition mounted={!helloStart} transition="fade" duration={600} timingFunction="ease">
                            {(styles) => <div style={styles}>Fade In Content</div>}
                        </Transition> */}
                <RoleDisplayHelloTitle></RoleDisplayHelloTitle>
                <RoleDisplayHello  />
                <RoleDisplayHelloButton clickIntroductionCallback={()=>setHelloStart(true)} clickAgentCallback={()=>{
                    router.push("/agent")
                }}></RoleDisplayHelloButton>
            </Box>
            }
        </>
    );
}