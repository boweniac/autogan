import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AgentConversation, AgentConversationMessage, Message } from "./TypeAgentChat";
import { BlobOptions } from "buffer";

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
    openedLogInModal:boolean;

    helloStart: boolean;

    avatarState: boolean;
    muteState: boolean;
    initConversationRequest: string;
    agentConversationList: AgentConversation[] | undefined;
    agentConversationMessage: AgentConversationMessage[];
    introductionConversations: Message[];

    agentAvatarMapping: { [key: string]: string };
}

export const initialState = {
    appName: "AI 博闻",
    activePage: "/",
    gateWayProtocol: "https://",
    gateWayHost: "nas.boweniac.top",
    gateWayPort: "44403",

    userToken: "",
    userPhone: "",
    userState: 0,
    openedLogInModal: false,

    helloStart: false,
    
    avatarState: true,
    muteState: false,
    initConversationRequest: "",
    agentConversationList: [],
    agentConversationMessage: [],
    introductionConversations: [],

    agentAvatarMapping: {
        "CustomerManager": "customerManagerGirl",
        "Coder": "coder",
        "DocumentExp": "documentExp",
        "SearchExpert": "searchExpert",
        "Secretary": "secretary",
        "Tester": "tester"
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