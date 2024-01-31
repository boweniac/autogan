import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AgentConversation, Message } from "./TypeAgentChat";

export const excludeFromState = [
    "appName",
    "activePage",
    "gateWayProtocol",
    "gateWayHost",
    "gateWayPort",
];

export interface LocalState {
    appName: string;
    activePage: string;
    gateWayProtocol: string;
    gateWayHost: string;
    gateWayPort: string;

    userToken:string;
    userPhone:string;
    userState:number;

    helloStart: boolean;

    initConversationRequest: string;
    agentConversations: AgentConversation[];
    introductionConversations: Message[];

    agentAvatarMapping: { [key: string]: string };
}

export const initialState = {
    appName: "AI 博闻",
    activePage: "/",
    gateWayProtocol: "http://",
    gateWayHost: "localhost",
    gateWayPort: "60607",

    userToken: "",
    userPhone: "",
    userState: 0,

    helloStart: false,
    
    initConversationRequest: "",
    agentConversations: [],
    introductionConversations: [],

    agentAvatarMapping: {
        "CustomerManager": "boy"
    }
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