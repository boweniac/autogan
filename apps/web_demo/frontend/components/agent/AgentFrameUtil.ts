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
import { AudioAndLip } from "@/stores/TypeAudioAndLip"

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

export const AgentConversationSend = async (conversationID: string, value: string, signal: AbortSignal, sliceCallback: (src: AudioAndLip)=> void, endCallback?: (() => void) | undefined, errorCallback?: (() => void) | undefined ) => {
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
        "/agent/test",
        {
            conversation_id: conversationID,
            content: value,
        },
        signal,
        (res) => {
            if (res) {
                if (res.content == "[DONE]") {
                    if (res.contentType == "tool") {
                        updateAgentConversationMessageBlockState(conversationID, messageLocalID, messageBlockLocalID, {contentTag: res.contentTag})
                    }
                    // 一个消息块的结束
                    if (textSlice && agent_name != "PainterExp") {
                        sliceCallback({"text": textSlice, "agentName": agent_name})
                    }
                    text = ""
                    // agent_name = ""
                    // messageLocalID = ""
                    hold = true
                    coding = false
                    sliceLength = 0
                    textSlice = ""
                } else {
                    if (res.index == 0) {
                        text = ""
                        messageBlockLocalID = uuidv4()
                        text += res.content
                        content_type = res.contentType
                        agent_name = res.agentName
                        task_id = res.taskId
                        if (messageID != res.msgId) {
                            messageID = res.msgId
                            // 一个角色消息的开始
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
                        if (agent_name != "Customer") {
                            if (res.content.includes('```')) {
                                // 识别代码块的开始和结束
                                coding = !coding
                                if (coding && textSlice && agent_name != "PainterExp") {
                                    sliceCallback({"text": textSlice, "agentName": agent_name})
                                    hold = true
                                    sliceLength = 0
                                    textSlice = ""
                                }
                            }
                            if (!coding) {
                                // 跳过代码块
                                textSlice += res.content
                                sliceLength++
                                if (textSlice.length > 10 && !coding &&  agent_name != "PainterExp") {
                                    sliceCallback({"text": textSlice, "agentName": agent_name})
                                    hold = true
                                    sliceLength = 0
                                    textSlice = ""
                                }
                            }
                        }
                    } else {
                        // 角色消息接收中
                        text += res.content

                        if (res.content.includes('```')) {
                            // 识别代码块的开始和结束
                            coding = !coding
                            if (coding && textSlice &&  agent_name != "PainterExp") {
                                sliceCallback({"text": textSlice, "agentName": agent_name})
                                hold = true
                                sliceLength = 0
                                textSlice = ""
                            }
                        } else if (!coding) {
                            // 跳过代码块
                            textSlice += res.content
                            sliceLength++
                            if (regex.test(res.content)) {
                                if (sliceLength > 15) {
                                    hold = false
                                }

                            }
                            if (sliceLength > 15 && !hold && !coding &&  agent_name != "PainterExp") {
                                sliceCallback({"text": textSlice, "agentName": agent_name})
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

export const AutoTitle = async (conversationID: string, signal: AbortSignal, sliceCallback: (src: AudioAndLip)=> void) => {
    let title = ""
    await streamAPI(
        "/agent/auto_title",
        {
            conversation_id: conversationID,
        },
        signal,
        (res) => {
            if (res) {
                if (res.content != "[DONE]") {
                    title += res.content
                    updateAgentConversationState(conversationID, {title: title})
                }
            }
        }
        ).then();
}