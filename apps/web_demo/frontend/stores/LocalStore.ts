import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AgentConversation, AgentConversationMessage, Message } from "./TypeAgentChat";
import { BlobOptions } from "buffer";

export const excludeFromState = [
    "activePage",
];

export interface LocalState {
    activePage: string;

    userToken:string;
    userPhone:string;
    userState:number;
    openedLogInModal:boolean;

    avatarState: boolean;
    muteState: boolean;
    initConversationRequest: string;
    agentConversationList: AgentConversation[] | undefined;
    agentConversationMessage: AgentConversationMessage[];
    introductionConversations: Message[];

    audio: HTMLAudioElement | undefined

    agentAvatarMapping: { [key: string]: string };
}

export const initialState = {
    activePage: "/",

    userToken: "",
    userPhone: "",
    userState: 0,
    openedLogInModal: false,
    
    avatarState: true,
    muteState: false,
    initConversationRequest: "",
    agentConversationList: [],
    agentConversationMessage: [],
    introductionConversations: [],

    audio: undefined,

    agentAvatarMapping: {
        "CustomerManager": "customerManagerGirl",
        "Coder": "coder",
        "DocumentExp": "documentExp",
        "SearchExpert": "searchExpert",
        "Secretary": "secretary",
        "Tester": "tester",
        "system": "tester" 
    }
}

const store = () => ({ ...initialState } as LocalState);

export const localStore = create<LocalState>()(
    persist(store, {
        name: "local-store-v2",
        partialize: (state) =>
            Object.fromEntries(
                Object.entries(state).filter(([key]) => !excludeFromState.includes(key))
            ),
    })
);