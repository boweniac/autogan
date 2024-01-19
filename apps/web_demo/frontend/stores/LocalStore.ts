import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AgentConversation } from "./TypeAgentChat";

export const excludeFromState = [
    "appName",
    "activePage",

    "currentAbortController",
];

export interface LocalState {
    appName: string;
    activePage: string;
    gateWayProtocol: string;
    gateWayHost: string;
    gateWayPort: string;

    initConversationRequest: string;
    agentConversations: AgentConversation[];

    currentAbortController: AbortController | undefined;
}

export const initialState = {
    appName: "AI 博闻",
    activePage: "/",
    gateWayProtocol: "http://",
    gateWayHost: "localhost",
    gateWayPort: "60507",
    
    initConversationRequest: "",
    agentConversations: [],

    currentAbortController: undefined,
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