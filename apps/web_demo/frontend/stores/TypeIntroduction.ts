import { AudioAndLip } from "./TypeAudioAndLip";

export interface IntroductionMessage {
    agentName: string;
    messageBlocks: IntroductionMessageBlock[];
}

export interface IntroductionMessageBlock {
    contentType?: string | undefined;
    contentTag?: string | undefined;
    content?: string | undefined;
    audioAndLip?: AudioAndLip | undefined
}