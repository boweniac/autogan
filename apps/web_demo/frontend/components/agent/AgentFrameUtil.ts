import { addAgentConversationAPI } from "@/api/add_conversation"
import { audioAndLipAPI } from "@/api/audio_and_lip"
import { getConversationsAPI } from "@/api/get_conversations"
import { getLastMsgIdAPI } from "@/api/get_last_msg_id"
import { getMessagesAPI } from "@/api/get_messages"
import { streamTestAPI } from "@/api/test"
import { addAgentConversationMessageState, addAgentConversationState, clearConversationState, getAgentConversationMessageLastRemoteIDState, getAgentConversationState, updateAgentConversationMessageState, updateAgentConversationState, updateInitConversationRequest } from "@/stores/LocalStoreActions"
import { Message } from "@/stores/TypeAgentChat"
import { NextRouter } from "next/router"
import { useState } from "react"
import { v4 as uuidv4 } from "uuid";

export const addAgentConversation = async (value: string, router: NextRouter) => {
    addAgentConversationAPI().then((conversation_id: string) => {
        if (conversation_id) {
            addAgentConversationState(conversation_id, undefined)
            updateInitConversationRequest(value)
            router.push(`/agent/${conversation_id}`).then()
        }
    })
}

export const syncConversations = async () => {
    let deletedConversations: string[] = []
    const conversations = await getConversationsAPI()
    if (conversations) {
        let conversationIDList: string[] = []
        conversations.map((conversation)=>{
            conversationIDList = [...conversationIDList, conversation.id]
            const localConversation = getAgentConversationState(conversation.id)
            if (localConversation) {
                if (localConversation.title != conversation.title) {

                    updateAgentConversationState(conversation.id, conversation)
                }
            } else {
                addAgentConversationState(conversation.id, conversation.title)
            }
        })
        deletedConversations = clearConversationState(conversationIDList)
    }
    return deletedConversations
}

export const syncMessages = async (conversation_id: string) => {
    getLastMsgIdAPI(conversation_id).then((lastMsgId)=>{
        if (lastMsgId && lastMsgId != getAgentConversationMessageLastRemoteIDState(conversation_id)) {
            getMessagesAPI(conversation_id).then((messages)=>{
                updateAgentConversationState(conversation_id, {"messages": messages})
            })
        }
    })
}

export const AgentConversationSend = async (conversationID: string, value: string, speakText: (src: string)=> void) => {
    let text = ""
    let agent_name = ""
    let role = ""
    let uuid = ""
    await streamTestAPI(
        value, 
        conversationID,
        undefined,
        (res) => {
            if (res) {
                if (res.content == "[DONE]") {
                    speakText(text)
                    text = ""
                    agent_name = ""
                    uuid = ""
                } else {
                    if (text == "") {
                        uuid = uuidv4()
                        text += res.content
                        role = res.role
                        agent_name = res.agent_name
                        addAgentConversationMessageState(conversationID, {
                            localID: uuid,
                            agent_name: agent_name,
                            role: role,
                            content: text
                        })
                    } else {
                        text += res.content
                        updateAgentConversationMessageState(conversationID, uuid, {content: text})
                    }
                }
            }
        },
        undefined
        ).then();
}