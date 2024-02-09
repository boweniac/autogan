import { getIntroductionAPI } from "@/api/get_introduction";
import { addIntroductionConversationMessageBlockState, addIntroductionConversationMessageState, updateIntroductionConversationMessageBlockState } from "@/stores/LocalStoreActions";
import { AudioAndLip, AudioAndLipDemo, LipsData } from "@/stores/TypeAudioAndLip";
import { IntroductionMessage } from "@/stores/TypeIntroduction";
import { v4 as uuidv4 } from "uuid";
import { avatarConfig } from "../avatar/Avatar/AvatarConfig";

export const AgentIntroductionSend = async (caseID: string, sliceCallback: (src: AudioAndLipDemo)=> void, endCallback?: (() => void) | undefined, errorCallback?: (() => void) | undefined ) => {
    const regex = /[.,，。；\/#!$%\^&\*;:{}=\-_`~()|\n\r]/g;
    let text = ""
    let textSlice = ""
    let hold = true
    let coding = false
    let sliceLength = 0
    let agent_name = ""
    let content_type = ""
    let messageLocalID = ""
    let messageBlockLocalID = ""
    let messageID = ""
    let task_id = ""
    getIntroductionAPI(caseID).then((messages)=>{
        if (messages) {
            const processMessage = (messageIndex: number) => {
                if (messageIndex < messages.length) {
                    const message = messages[messageIndex];
                    const messageLocalID = uuidv4()
                    addIntroductionConversationMessageState(messageLocalID, message.agentName)

                    const processMessageBlocks = (blockIndex: number) => {
                        if (blockIndex < message.messageBlocks.length) {
                            const message_block = message.messageBlocks[blockIndex];
                            const messageBlockLocalID = uuidv4()
                            addIntroductionConversationMessageBlockState(messageLocalID, {
                                localID: messageBlockLocalID,
                                contentType: message_block.contentType,
                                contentTag: message_block.contentTag,
                                content: "",
                            })
                            if (message_block.audioAndLip?.lipsData) {
                                const lipsData = JSON.parse(message_block.audioAndLip.lipsData as string) as LipsData;
                                message_block.audioAndLip.lipsData = lipsData.mouthCues;
                                const data: AudioAndLipDemo = {
                                    audioFile: message_block.audioAndLip.audioFile,
                                    lipsData: message_block.audioAndLip.lipsData,
                                    text: message_block.content,
                                    agentName: message.agentName,
                                    messageLocalID: messageLocalID,
                                    messageBlockLocalID: messageBlockLocalID
                                }
                                sliceCallback(data)
                            }

                            let currentChar = 0;
                            let prevText = ""
                            const typeWriter = setInterval(() => {
                                if (message_block.content) {
                                    prevText += message_block.content[currentChar]
                                    updateIntroductionConversationMessageBlockState(messageLocalID, messageBlockLocalID, {content: prevText})
                                    currentChar++;
                                    if (currentChar === message_block.content.length) {
                                        clearInterval(typeWriter)
                                        processMessageBlocks(blockIndex + 1);
                                    };
                                }
                            }, 200);

                            // return () => clearInterval(typeWriter);
                        } else {
                            // 当所有消息块处理完成后，递归处理下一个消息
                            processMessage(messageIndex + 1);
                        }
                    }
                    processMessageBlocks(0);
                }
            }
            processMessage(0);
        }
    })
}

export const convertToAudioAndLipDemo = (audioAndLipDemo: AudioAndLipDemo, avatarName: string) => {
    const audioFile = audioAndLipDemo.audioFile ? audioAndLipDemo.audioFile[avatarName] : ""
    const data = {
        "audioFile": audioFile,
        "lipsData": audioAndLipDemo.lipsData,
        "text": audioAndLipDemo.text,
        "agentName": audioAndLipDemo.agentName,
    }
    return data
}

export const helloTextString: string = "您好，欢迎来到“爱博闻科技”！我是这里的数字员工。您可以在下面的菜单中选择想要了解的内容或是亲自体验。";
  
export const helloAudioAndLip: AudioAndLipDemo = {
    audioFile: {
        "customerManagerBoy": "https://aibowen-base.boweniac.top/9475afe9-49c7-533a-b7d4-7316dfe7c69f.mp3",
        "customerManagerGirl": "https://aibowen-base.boweniac.top/6206f179-0bbb-5265-89b8-ec742b5cfbcb.mp3"
    },
    agentName: "CustomerManager",
    lipsData: [
        {
            "start": 0.00,
            "end": 0.03,
            "value": "X"
        },
        {
            "start": 0.03,
            "end": 0.08,
            "value": "B"
        },
        {
            "start": 0.08,
            "end": 0.20,
            "value": "F"
        },
        {
            "start": 0.20,
            "end": 0.34,
            "value": "C"
        },
        {
            "start": 0.34,
            "end": 0.48,
            "value": "E"
        },
        {
            "start": 0.48,
            "end": 1.08,
            "value": "X"
        },
        {
            "start": 1.08,
            "end": 1.13,
            "value": "B"
        },
        {
            "start": 1.13,
            "end": 1.24,
            "value": "E"
        },
        {
            "start": 1.24,
            "end": 1.31,
            "value": "B"
        },
        {
            "start": 1.31,
            "end": 1.38,
            "value": "F"
        },
        {
            "start": 1.38,
            "end": 1.45,
            "value": "C"
        },
        {
            "start": 1.45,
            "end": 1.52,
            "value": "B"
        },
        {
            "start": 1.52,
            "end": 1.59,
            "value": "D"
        },
        {
            "start": 1.59,
            "end": 1.67,
            "value": "A"
        },
        {
            "start": 1.67,
            "end": 1.76,
            "value": "C"
        },
        {
            "start": 1.76,
            "end": 1.83,
            "value": "B"
        },
        {
            "start": 1.83,
            "end": 1.91,
            "value": "A"
        },
        {
            "start": 1.91,
            "end": 2.09,
            "value": "E"
        },
        {
            "start": 2.09,
            "end": 2.16,
            "value": "B"
        },
        {
            "start": 2.16,
            "end": 2.44,
            "value": "F"
        },
        {
            "start": 2.44,
            "end": 3.07,
            "value": "B"
        },
        {
            "start": 3.07,
            "end": 3.27,
            "value": "F"
        },
        {
            "start": 3.27,
            "end": 3.34,
            "value": "B"
        },
        {
            "start": 3.34,
            "end": 3.41,
            "value": "F"
        },
        {
            "start": 3.41,
            "end": 3.69,
            "value": "B"
        },
        {
            "start": 3.69,
            "end": 3.97,
            "value": "F"
        },
        {
            "start": 3.97,
            "end": 4.04,
            "value": "B"
        },
        {
            "start": 4.04,
            "end": 4.25,
            "value": "C"
        },
        {
            "start": 4.25,
            "end": 4.53,
            "value": "E"
        },
        {
            "start": 4.53,
            "end": 4.60,
            "value": "F"
        },
        {
            "start": 4.60,
            "end": 4.67,
            "value": "B"
        },
        {
            "start": 4.67,
            "end": 5.53,
            "value": "X"
        },
        {
            "start": 5.53,
            "end": 5.97,
            "value": "B"
        },
        {
            "start": 5.97,
            "end": 6.04,
            "value": "C"
        },
        {
            "start": 6.04,
            "end": 6.18,
            "value": "B"
        },
        {
            "start": 6.18,
            "end": 6.25,
            "value": "C"
        },
        {
            "start": 6.25,
            "end": 6.33,
            "value": "A"
        },
        {
            "start": 6.33,
            "end": 6.58,
            "value": "B"
        },
        {
            "start": 6.58,
            "end": 6.86,
            "value": "C"
        },
        {
            "start": 6.86,
            "end": 7.14,
            "value": "E"
        },
        {
            "start": 7.14,
            "end": 7.42,
            "value": "B"
        },
        {
            "start": 7.42,
            "end": 7.70,
            "value": "F"
        },
        {
            "start": 7.70,
            "end": 7.77,
            "value": "B"
        },
        {
            "start": 7.77,
            "end": 7.91,
            "value": "C"
        },
        {
            "start": 7.91,
            "end": 8.05,
            "value": "E"
        },
        {
            "start": 8.05,
            "end": 8.12,
            "value": "F"
        },
        {
            "start": 8.12,
            "end": 8.47,
            "value": "B"
        },
        {
            "start": 8.47,
            "end": 8.54,
            "value": "C"
        },
        {
            "start": 8.54,
            "end": 8.61,
            "value": "B"
        },
        {
            "start": 8.61,
            "end": 8.75,
            "value": "E"
        },
        {
            "start": 8.75,
            "end": 8.82,
            "value": "F"
        },
        {
            "start": 8.82,
            "end": 9.06,
            "value": "B"
        },
        {
            "start": 9.06,
            "end": 9.18,
            "value": "E"
        },
        {
            "start": 9.18,
            "end": 9.46,
            "value": "B"
        },
        {
            "start": 9.46,
            "end": 9.67,
            "value": "F"
        },
        {
            "start": 9.67,
            "end": 9.81,
            "value": "B"
        },
        {
            "start": 9.81,
            "end": 10.09,
            "value": "C"
        },
        {
            "start": 10.09,
            "end": 10.15,
            "value": "A"
        },
        {
            "start": 10.15,
            "end": 10.23,
            "value": "B"
        },
        {
            "start": 10.23,
            "end": 10.29,
            "value": "X"
        }
    ]
};