export const avatarConfig: { [key: string]: AvatarObject } = {
    "boy": {
        "modelPath": "/avatars/boy.glb",
        "voice": "onyx",
    },
    "girl": {
        "modelPath": "/avatars/girl.glb",
        "voice": "nova",
    }
};

export interface AvatarObject {
    modelPath: string;
    voice: string;
}

export const corresponding: { [key: string]: string } = {
    "A": "viseme_PP",
    "B": "viseme_kk",
    "C": "viseme_I",
    "D": "viseme_aa",
    "E": "viseme_O",
    "F": "viseme_U",
    "G": "viseme_FF",
    "H": "viseme_TH",
    "X": "viseme_PP",
  };
  
  export const nodeKeyToIndex: { [key: string]: number } = {
    "viseme_sil": 0,
    "viseme_PP": 1,
    "viseme_FF": 2,
    "viseme_TH": 3,
    "viseme_DD": 4,
    "viseme_kk": 5,
    "viseme_CH": 6,
    "viseme_SS": 7,
    "viseme_nn": 8,
    "viseme_RR": 9,
    "viseme_aa": 10,
    "viseme_E": 11,
    "viseme_I": 12,
    "viseme_O": 13,
    "viseme_U": 14
  };