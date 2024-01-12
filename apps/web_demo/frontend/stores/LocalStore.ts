import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AgentConversation } from "./TypeAgentChat";

export const excludeFromState = [
    "appName",
    "activePage",
];

export interface LocalState {
    appName: string;
    activePage: string;
    gateWayProtocol: string;
    gateWayHost: string;
    gateWayPort: string;

    initConversationRequest: string;
    agentConversations: AgentConversation[];
}

export const initialState = {
    appName: "AI 博闻",
    activePage: "/",
    gateWayProtocol: "http://",
    gateWayHost: "localhost",
    gateWayPort: "60507",
    
    initConversationRequest: "",
    agentConversations: [],
}

const store = () => ({ ...initialState } as LocalState);

export const localStore = create<LocalState>()(
    persist(store, {
        name: "local-store-v1",
        partialize: (state) =>
            Object.fromEntries(
                Object.entries(state).filter(([key]) => !excludeFromState.includes(key))
            ),
    })
);