import { create } from "zustand";
import { persist } from "zustand/middleware";

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
}

export const initialState = {
    appName: "AI 博闻",
    gateWayProtocol: "http://",
    gateWayHost: "localhost",
    gateWayPort: "60507",
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
