import { addAgentConversationAPI } from "@/api/add_conversation"
import { audioAndLipAPI } from "@/api/audio_and_lip"
import { getConversationsAPI } from "@/api/get_conversations"
import { getLastMsgIdAPI } from "@/api/get_last_msg_id"
import { getMessagesAPI } from "@/api/get_messages"
import { streamTestAPI } from "@/api/test"
import { addAgentConversationMessageState, addAgentConversationState, clearConversationState, getAgentConversationMessageLastRemoteIDState, getAgentConversationState, updateAgentConversationMessageState, updateAgentConversationState, updateCurrentAbortController, updateInitConversationRequest } from "@/stores/LocalStoreActions"
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
    const currentAbortController = new AbortController();
    updateCurrentAbortController(currentAbortController)
    const regex = /[.,，。；\/#!$%\^&\*;:{}=\-_`~()|\n\r]/g;
    let text = ""
    let textSlice = ""
    let hold = true
    let coding = false
    let sliceLength = 0
    let agent_name = ""
    let role = ""
    let uuid = ""
    await streamTestAPI(
        value, 
        conversationID,
        currentAbortController,
        (res) => {
            if (res) {
                if (res.content == "[DONE]") {
                    if (textSlice) {
                        speakText(textSlice)
                    }
                    text = ""
                    agent_name = ""
                    uuid = ""
                    hold = true
                    sliceLength = 0
                    textSlice = ""
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

                        if (res.content.includes('```')) {
                            coding = !coding
                            if (coding) {
                                speakText(textSlice)
                                hold = true
                                sliceLength = 0
                                textSlice = ""
                            }
                        }
                        if (!coding) {
                            textSlice += res.content
                            sliceLength++
                            console.log(`textSlice:`+JSON.stringify(textSlice));
                            console.log(`sliceLength:`+JSON.stringify(sliceLength));
                            console.log(`hold:`+JSON.stringify(hold));
                            if (regex.test(res.content)) {
                                console.log(`regex.test(res.content):`+JSON.stringify(regex.test(res.content)));
                                if (sliceLength > 15) {
                                    hold = false
                                }
    
                            }
                            console.log(`hold:`+JSON.stringify(hold));
                            if (sliceLength > 15 && !hold && !coding) {
                                speakText(textSlice)
                                hold = true
                                sliceLength = 0
                                textSlice = ""
                            }
                        }
                        updateAgentConversationMessageState(conversationID, uuid, {content: text})
                    }
                }
            }
        },
        undefined
        ).then();
}