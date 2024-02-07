export interface AudioAndLip {
    audioFile?: string;
    lipsData?: string | MouthCues[]
    text?: string | undefined
    agentName?: string | undefined
    avatarName?: string | undefined
}

export interface LipsData {
    metadata: Metadata;
    mouthCues: MouthCues[];
  }

  export interface Metadata {
    soundFile: string;
    duration: number;
  }

export interface MouthCues {
    start: number;
    end: number;
    value: string;
  }

export interface AudioAndLipDemo {
  audioFile?: { [key: string]: string };
  lipsData?: string | MouthCues[]
  text?: string | undefined
  agentName?: string | undefined
  avatarName?: string | undefined
  messageLocalID?: string | undefined
  messageBlockLocalID?: string | undefined
}
