import { addAgentConversationAPI } from "@/api/conversation/add_conversation"
import { audioAndLipAPI } from "@/api/audio/audio_and_lip"
import { getConversationsAPI } from "@/api/conversation/get_conversations"
import { getLastMsgIdAPI } from "@/api/message/get_last_msg_id"
import { addAgentConversationMessageBlockState, addAgentMessageState, addAgentConversationListState, getAgentConversationMessageLastRemoteIDState, updateAgentConversationMessageBlockState, updateAgentConversationMessageState, updateAgentConversationState, updateInitConversationRequestState } from "@/stores/LocalStoreActions"
import { Message, MessageBlock } from "@/stores/TypeAgentChat"
import { NextRouter } from "next/router"
import { useState } from "react"
import { v4 as uuidv4 } from "uuid";
import { streamAPI } from "@/api/request"

export const addAgentConversation = async (value: string, router: NextRouter) => {
    addAgentConversationAPI().then((conversation_id: string) => {
        if (conversation_id) {
            addAgentConversationListState(conversation_id, undefined)
            updateInitConversationRequestState(value)
            router.push(`/agent/${conversation_id}`).then()
        }
    })
}

// export const syncConversations = async () => {
//     let deletedConversations: string[] = []
//     const conversations = await getConversationsAPI()
//     if (conversations) {
//         let conversationIDList: string[] = []
//         conversations.map((conversation)=>{
//             conversationIDList = [...conversationIDList, conversation.id]
//             const localConversation = getAgentConversationState(conversation.id)
//             if (localConversation) {
//                 if (localConversation.title != conversation.title) {
//                     updateAgentConversationState(conversation.id, conversation)
//                 }
//             } else {
//                 addAgentConversationState(conversation.id, conversation.title)
//             }
//         })
//         // deletedConversations = clearConversationState(conversationIDList)
//     }
//     return deletedConversations
// }

// export const syncMessages = async (conversation_id: string) => {
//     getLastMsgIdAPI(conversation_id).then((lastMsgId)=>{
//         if (lastMsgId && lastMsgId != getAgentConversationMessageLastRemoteIDState(conversation_id)) {
//             getMessagesAPI(conversation_id).then((messages)=>{
//                 updateAgentConversationState(conversation_id, {"messages": messages})
//             })
//         }
//     })
// }

export const AgentConversationSend = async (conversationID: string, value: string, signal: AbortSignal, sliceCallback: (src: string)=> void, endCallback?: (() => void) | undefined, errorCallback?: (() => void) | undefined ) => {
    // const currentAbortController = new AbortController();
    // updateCurrentAbortController(currentAbortController)
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
    await streamAPI(
        value, 
        conversationID,
        signal,
        (res) => {
            if (res) {
                if (res.content == "[DONE]") {
                    // 一个消息块的结束
                    if (textSlice) {
                        sliceCallback(textSlice)
                    }
                    text = ""
                    // agent_name = ""
                    // messageLocalID = ""
                    hold = true
                    sliceLength = 0
                    textSlice = ""
                } else {
                    if (res.index == 0) {
                        text = ""
                        console.log(`第一个块`);
                        messageBlockLocalID = uuidv4()
                        text += res.content
                        content_type = res.contentType
                        agent_name = res.agentName
                        task_id = res.taskId
                        if (messageID != res.msgId) {
                            messageID = res.msgId
                            // 一个角色消息的开始
                            console.log(`一个角色消息的开始`);
                            console.log(`messages:`+JSON.stringify(res));
                            messageLocalID = uuidv4()
                            addAgentMessageState(conversationID, {
                                task_id: task_id,
                                localID: messageLocalID,
                                msg_id:res.msgId,
                                agent_name: agent_name,
                                message_blocks: []
                            })
                            addAgentConversationMessageBlockState(conversationID, messageLocalID, {
                                taskId: task_id,
                                localID: messageBlockLocalID,
                                msgId:res.msgId,
                                agentName: agent_name,
                                contentType: content_type,
                                contentTag: res.contentTag,
                                content: res.content,
                                tokens: res.tokens
                            })
                        } else {
                            // 同一角色新的消息块
                            console.log(`同一角色新的消息块`);
                            console.log(`messages:`+JSON.stringify(res));
                            addAgentConversationMessageBlockState(conversationID, messageLocalID, {
                                taskId: task_id,
                                localID: messageBlockLocalID,
                                msgId:res.msgId,
                                agentName: agent_name,
                                contentType: content_type,
                                contentTag: res.contentTag,
                                content: res.content,
                                tokens: res.tokens
                            })
                        }
                    } else {
                        // 角色消息接收中
                        text += res.content

                        if (res.content.includes('```')) {
                            // 识别代码块的开始和结束
                            coding = !coding
                            if (coding) {
                                sliceCallback(textSlice)
                                hold = true
                                sliceLength = 0
                                textSlice = ""
                            }
                        }
                        if (!coding) {
                            // 跳过代码块
                            textSlice += res.content
                            sliceLength++
                            // console.log(`textSlice:`+JSON.stringify(textSlice));
                            // console.log(`sliceLength:`+JSON.stringify(sliceLength));
                            // console.log(`hold:`+JSON.stringify(hold));
                            if (regex.test(res.content)) {
                                console.log(`regex.test(res.content):`+JSON.stringify(regex.test(res.content)));
                                if (sliceLength > 15) {
                                    hold = false
                                }
    
                            }
                            // console.log(`hold:`+JSON.stringify(hold));
                            if (sliceLength > 15 && !hold && !coding) {
                                sliceCallback(textSlice)
                                hold = true
                                sliceLength = 0
                                textSlice = ""
                            }
                        }
                        updateAgentConversationMessageBlockState(conversationID, messageLocalID, messageBlockLocalID, {content: text})
                    }
                }
            }
        },
        endCallback
        ).then();
}