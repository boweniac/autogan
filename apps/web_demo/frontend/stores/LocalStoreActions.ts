import { localStore } from "./LocalStore";
import { AgentConversation, Message } from "./TypeAgentChat";

const get = localStore.getState;
const set = localStore.setState;

export const updateActivePageState = (page: string) => {
    set(() => ({ activePage: page }));
}

export const updateInitConversationRequest = (value: string) => {
    set(() => ({ initConversationRequest: value }));
}

export const burnAfterGetInitConversationRequest = () => {
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

export const addAgentConversationMessageState = (conversationID: string, message: Partial<Message>) => {
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

export const updateAgentConversationMessageState = (conversationID: string, localID: string, message: Partial<Message>) => {
    set((state) => ({
        agentConversations: state.agentConversations.map((c) => {
            if (c.id === conversationID) {
                c.messages = c.messages.map((m) => {
                    if (m.localID === localID) {
                        return {...m, ...message}
                    }
                    return m;
                });
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
    return messages[len-1].id
};