export interface AudioAndLip {
    audioFile: string;
    lipsData: string | MouthCues[]
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