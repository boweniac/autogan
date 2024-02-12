import { localStore } from "./LocalStore";
import { AgentConversation, AgentConversationMessage, Message, MessageBlock } from "./TypeAgentChat";

const get = localStore.getState;
const set = localStore.setState;

// user
export const updateUserTokenState = (value: string) => {
    set(() => ({ userToken: value }));
}

export const updateUserPhoneState = (value: string) => {
    set(() => ({ userPhone: value }));
}

export const updateUserStateState = (value: number) => {
    set(() => ({ userState: value }));
}

export const updateActivePageState = (page: string) => {
    set(() => ({ activePage: page }));
}

export const updateAudioState = (audio: HTMLAudioElement) => {
    set(() => ({ audio: audio }));
}

export const getAudioState = () => {
    return get().audio
}

export const openLogInModal = () => {
    set(() => ({ openedLogInModal: true }));
}

export const closeLogInModal = () => {
    set(() => ({ openedLogInModal: false }));
}

export const updateAgentAvatarMappingState = (mapping: { [key: string]: string }) => {
    set((state) => ({
        agentAvatarMapping: {
            ...state.agentAvatarMapping, ...mapping
        }
    }));
};
// export const updateHelloStartState = (value: boolean) => {
//     set(() => ({ helloStart: value }));
// }

export const updateAvatarStateState = (value: boolean) => {
    set(() => ({ avatarState: value }));
}

export const updateMuteStateState = (value: boolean) => {
    set(() => ({ muteState: value }));
}

export const updateInitConversationRequestState = (value: string) => {
    set(() => ({ initConversationRequest: value }));
}

export const burnAfterGetInitConversationRequestState = () => {
    const initConversationRequest = get().initConversationRequest
    set(() => ({ initConversationRequest: "" }));
    return initConversationRequest
}

export const addAgentConversationListState = (id: string, title: string | undefined) => {
    set((state) => ({
        agentConversationList: [
            {
                id: id,
                title: title,
                orgStructure: undefined,
                model: undefined
            },
            ...state.agentConversationList || [],
        ],
    }));
};

export const deleteAgentConversationState = (id: string) => {
    set((state) => ({
        agentConversationList: state.agentConversationList?.filter((c) => c.id !== id),
        agentConversationMessage: state.agentConversationMessage?.filter((c) => c.id !== id),
    }));
}

export const updateAgentConversationState = (id: string, conversation: Partial<AgentConversation>) => {
    set((state) => ({
        agentConversationList: state.agentConversationList?.map((c) => {
            if (c.id === id) {
                return {...c, ...conversation}
            }
            return c;
        }),
    }));
};

// AgentConversationList
export const getAgentConversationInfoState = (conversationID: string) => {
    return get().agentConversationList?.find(c => c.id === conversationID);
};

export const getAgentConversationListState = () => {
    return get().agentConversationList
};

export const updateAgentConversationListState = (value: AgentConversation[]) => {
    set(() => ({ agentConversationList: value }));
}

export const resetAgentConversationListState = () => {
    set(() => ({ agentConversationList: [] }));
};

// AgentConversationMessage
export const getAgentConversationMessageState = (conversationID: string | undefined) => {
    if (conversationID) {
        const messages = get().agentConversationMessage?.find(c => c.id === conversationID)?.messages;
        if (messages) {
            return messages
        }
        set((state) => ({
            agentConversationMessage: [
                ...state.agentConversationMessage,
                {
                    id: conversationID,
                    messages: []
                }
            ]
        }));
    }
};

export const InitAgentConversationMessageState = (conversationID: string, messages: Message[]) => {
    const conversationMessage = {
        id: conversationID,
        messages: messages
    }
    if (get().agentConversationMessage?.find(c => c.id == conversationID)) {
        set((state) => ({
            agentConversationMessage: state.agentConversationMessage?.map((c) => {
                if (c.id === conversationID) {
                    return conversationMessage
                }
                return c;
            }),
        }));
    } else {
        set((state) => ({
            agentConversationMessage: [
                ...state.agentConversationMessage,
                conversationMessage
            ]
        }));
    }
};

export const addAgentMessageState = (conversationID: string, message: Message) => {
    set((state) => ({
        agentConversationMessage: state.agentConversationMessage?.map((c) => {
            if (c.id === conversationID) {
                c.messages = [
                    ...c.messages,
                    message
                ]
                return c
            }
            return c;
        }),
    }));
};

export const deleteAgentConversationMessageState = (conversationID: string) => {
    return get().agentConversationMessage?.filter(c => c.id !== conversationID);
};

export const resetAgentConversationMessageState = () => {
    set(() => ({ agentConversationMessage: [] }));
};

export const clearConversationMessageState = (conversationIDList: string[]) => {
    set((state) => ({
        agentConversationMessage: state.agentConversationMessage?.filter((c) => conversationIDList.includes(c.id)),
    }));
};

export const updateAgentConversationMessageState = (conversationID: string, messageLocalID: string, message: Message) => {
    set((state) => ({
        agentConversationMessage: state.agentConversationMessage?.map((c) => {
            if (c.id === conversationID) {
                c.messages = c.messages.map((m) => {
                    if (m.localID === messageLocalID) {
                        return {...m, ...message}
                    }
                    return m;
                });
            }
            return c;
        }),
    }));
};

export const addAgentConversationMessageBlockState = (conversationID: string, messageLocalID: string, messageBlock: MessageBlock) => {
    set((state) => ({
        agentConversationMessage: state.agentConversationMessage?.map((c) => {
            if (c.id === conversationID) {
                c.messages.map((m)=>{
                    if (m.localID === messageLocalID) {
                        m.message_blocks = [
                            ...m.message_blocks,
                            messageBlock
                        ]
                    }
                })
            }
            return c;
        }),
    }));
};

export const updateAgentConversationMessageBlockState = (conversationID: string, messageLocalID: string, messageBlockLocalID: string, messageBlock: MessageBlock) => {
    set((state) => ({
        agentConversationMessage: state.agentConversationMessage?.map((c) => {
            if (c.id === conversationID) {
                c.messages.map((m)=>{
                    if (m.localID === messageLocalID) {
                        m.message_blocks = m.message_blocks.map((mb) => {
                            if (mb.localID === messageBlockLocalID) {
                                return {...mb, ...messageBlock}
                            }
                            return mb;
                        });
                    }
                })
            }
            return c;
        }),
    }));
};

export const getAgentConversationMessageLastRemoteIDState = (conversationID: string) => {
    const conversation = get().agentConversationMessage?.find(c => c.id === conversationID);
    if (conversation == undefined) {
        return undefined
    }
    const messages = conversation.messages
    const len = messages.length
    if (len == 0) {
        return undefined
    }
    return messages[len-1].msg_id
};

export const addIntroductionConversationMessageState = (messageLocalID: string, agent_name: string) => {
    set((state) => ({
        introductionConversations: [
            ...state.introductionConversations,
            {
                localID: messageLocalID,
                agent_name: agent_name,
                message_blocks: [],
            },
        ],
    }));
};

export const addIntroductionConversationMessageBlockState = (messageLocalID: string, messageBlock: MessageBlock) => {
    set((state) => ({
        introductionConversations: state.introductionConversations.map((m)=>{
            if (m.localID === messageLocalID) {
                m.message_blocks = [
                    ...m.message_blocks,
                    messageBlock
                ]
            }
            return m
        }),
    }));
};

export const updateIntroductionConversationMessageBlockState = (messageLocalID: string, messageBlockLocalID: string, messageBlock: MessageBlock) => {
    set((state) => ({
        introductionConversations: state.introductionConversations.map((m) => {
            if (m.localID === messageLocalID) {
                m.message_blocks.map((mb)=>{
                    if (mb.localID === messageBlockLocalID) {
                        mb.content = messageBlock.content
                        return mb
                    }
                    return mb;
                })
            }
            return m;
        }),
    }));
};

export const resetIntroductionConversationsState = () => {
    set(() => ({ introductionConversations: [] }));
};

export const resetLogOutState = () => {
    set((state) => ({ 
        userToken: "",
        userPhone: "",
        userState: 0,
        avatarState: true,
        muteState: false,
        agentAvatarMapping: {
            ...state.agentAvatarMapping, ...{"CustomerManager": "customerManagerGirl"}
        },
        agentConversationList: [],
        agentConversationMessage: [],
        introductionConversations: []
    }));
};