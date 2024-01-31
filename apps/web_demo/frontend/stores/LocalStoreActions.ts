import { localStore } from "./LocalStore";
import { AgentConversation, Message, MessageBlock } from "./TypeAgentChat";

const get = localStore.getState;
const set = localStore.setState;

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

export const updateHelloStartState = (value: boolean) => {
    set(() => ({ helloStart: value }));
}

export const updateInitConversationRequestState = (value: string) => {
    set(() => ({ initConversationRequest: value }));
}

export const burnAfterGetInitConversationRequestState = () => {
    const initConversationRequest = get().initConversationRequest
    set(() => ({ initConversationRequest: "" }));
    return initConversationRequest
}

export const addAgentConversationState = (id: string, title: string | undefined) => {
    set((state) => ({
        agentConversations: [
            ...state.agentConversations,
            {
                id: id,
                title: title,
                messages: [],
                orgStructure: undefined,
                model: undefined
            },
        ],
    }));
};

export const deleteAgentConversationState = (id: string) => {
    set((state) => ({
        agentConversations: state.agentConversations.filter((c) => c.id !== id),
    }));
}

export const updateAgentConversationState = (id: string, conversation: Partial<AgentConversation>) => {
    set((state) => ({
        agentConversations: state.agentConversations.map((c) => {
            if (c.id === id) {
                return {...c, ...conversation}
            }
            return c;
        }),
    }));
};

export const getAgentConversationState = (conversationID: string) => {
    return get().agentConversations.find(c => c.id === conversationID);
};

export const resetAgentConversationsState = () => {
    set(() => ({ agentConversations: [] }));
};

export const clearConversationState = (conversationIDList: string[]) => {
    let deletedConversations: string[] = []
    set((state) => ({
        agentConversations: state.agentConversations.filter(
            (c) => {
                if (conversationIDList.includes(c.id)) {
                    return true
                } else {
                    deletedConversations = [...deletedConversations, c.id]
                    return false
                }
            }
          ),
    }));
    return deletedConversations
};

export const addAgentConversationMessageState = (conversationID: string, message: Message) => {
    set((state) => ({
        agentConversations: state.agentConversations.map((c) => {
            if (c.id === conversationID) {
                c.messages = [
                    ...c.messages,
                    message,
                ];
            }
            return c;
        }),
    }));
};

export const updateAgentConversationMessageState = (conversationID: string, messageLocalID: string, message: Message) => {
    set((state) => ({
        agentConversations: state.agentConversations.map((c) => {
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
        agentConversations: state.agentConversations.map((c) => {
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
        agentConversations: state.agentConversations.map((c) => {
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
    const conversation = get().agentConversations.find(c => c.id === conversationID);
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
    console.log(`messageLocalID:`+messageLocalID);
    console.log(`agent_name:`+agent_name);
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