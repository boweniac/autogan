import { localStore } from "./LocalStore";
import { AgentConversation, Message } from "./TypeAgentChat";

const get = localStore.getState;
const set = localStore.setState;

export const updateActivePage = (page: string) => {
    set(() => ({ activePage: page }));
}

export const addAgentConversation = (id: string) => {
    set((state) => ({
        agentConversations: [
            ...state.agentConversations,
            {
                id: id,
                title: undefined,
                messages: [],
                orgStructure: undefined,
                model: undefined
            },
        ],
    }));
};

export const deleteAgentConversation = (id: string) => {
    set((state) => ({
        agentConversations: state.agentConversations.filter((c) => c.id !== id),
    }));
}

export const updateAgentConversationTitle = (id: string, conversation: Partial<AgentConversation>) => {
    set((state) => ({
        agentConversations: state.agentConversations.map((c) => {
            if (c.id === id) {
                return {...c, ...conversation}
            }
            return c;
        }),
    }));
};

export const addAgentConversationMessage = (conversationID: string, localID: string, content: string | undefined) => {
    set((state) => ({
        agentConversations: state.agentConversations.map((c) => {
            if (c.id === conversationID) {
                c.messages = [
                    ...c.messages,
                    {
                        localID: localID,
                        content: content
                    },
                ];
            }
            return c;
        }),
    }));
};

export const updateAgentConversationMessage = (conversationID: string, localID: string, message: Partial<Message>) => {
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

export const getAgentConversationMessageLastRemoteID = (conversationID: string) => {
    const conversation = get().agentConversations.find(c => c.id === conversationID);
    if (conversation == undefined) {
        return undefined
    }
    const messages = conversation.messages
    const len = messages.length
    if (len == 0) {
        return undefined
    }
    return messages[len-1].remoteID
};