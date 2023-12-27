import { localStore } from "./LocalStore";

const set = localStore.setState;

export const updateActivePage = (page: string) => {
    set(() => ({ activePage: page }));
}