export const avatarConfig: { [key: string]: AvatarObject } = {
    "customerManagerBoy": {
        "modelPath": "/avatars/CustomerManagerBoy.glb",
        "voice": "onyx",
        "ambientLightIntensity": 4,
        "pointLightY": 1,
        "pointLightZ": 1,
        "pointLightIntensity": 4,
        "cameraPositionY": 1.7,
        "cameraPositionZ": 1.4,
        "targetY": 1.7,
    },
    "customerManagerGirl": {
        "modelPath": "/avatars/CustomerManagerGirl.glb",
        "voice": "nova",
        "ambientLightIntensity": 4,
        "pointLightY": 1,
        "pointLightZ": 1,
        "pointLightIntensity": 4,
        "cameraPositionY": 1.6,
        "cameraPositionZ": 1.4,
        "targetY": 1.6,
    },
    "coder": {
        "modelPath": "/avatars/Coder.glb",
        "voice": "echo",
        "ambientLightIntensity": 4,
        "pointLightY": 1,
        "pointLightZ": 1,
        "pointLightIntensity": 4,
        "cameraPositionY": 1.7,
        "cameraPositionZ": 1.4,
        "targetY": 1.7,
    },
    "documentExp": {
        "modelPath": "/avatars/DocumentExp.glb",
        "voice": "shimmer",
        "ambientLightIntensity": 4,
        "pointLightY": 1,
        "pointLightZ": 1,
        "pointLightIntensity": 4,
        "cameraPositionY": 1.6,
        "cameraPositionZ": 1.4,
        "targetY": 1.6,
    },
    "searchExpert": {
        "modelPath": "/avatars/SearchExpert.glb",
        "voice": "alloy",
        "ambientLightIntensity": 4,
        "pointLightY": 1,
        "pointLightZ": 1,
        "pointLightIntensity": 4,
        "cameraPositionY": 1.7,
        "cameraPositionZ": 1.4,
        "targetY": 1.7,
    },
    "secretary": {
        "modelPath": "/avatars/Secretary.glb",
        "voice": "shimmer",
        "ambientLightIntensity": 4,
        "pointLightY": 1,
        "pointLightZ": 1,
        "pointLightIntensity": 4,
        "cameraPositionY": 1.6,
        "cameraPositionZ": 1.4,
        "targetY": 1.6,
    },
    "tester": {
        "modelPath": "/avatars/Tester.glb",
        "voice": "fable",
        "ambientLightIntensity": 4,
        "pointLightY": 1,
        "pointLightZ": 1,
        "pointLightIntensity": 4,
        "cameraPositionY": 1.7,
        "cameraPositionZ": 1.4,
        "targetY": 1.7,
    },
    "painterExp": {
        "modelPath": "/avatars/Tester.glb",
        "voice": "fable",
        "ambientLightIntensity": 4,
        "pointLightY": 1,
        "pointLightZ": 1,
        "pointLightIntensity": 4,
        "cameraPositionY": 1.7,
        "cameraPositionZ": 1.4,
        "targetY": 1.7,
    }
};

export interface AvatarObject {
    modelPath?: string;
    voice?: string;
    positionX?: string | number;
    positionY?: string | number;
    positionZ?: string | number;
    positionRotation?: string | number;
    ambientLightIntensity?: string | number;
    pointLightX?: string | number;
    pointLightY?: string | number;
    pointLightZ?: string | number;
    pointLightIntensity?: string | number;
    fov?: string | number;
    cameraPositionX?: string | number;
    cameraPositionY?: string | number;
    cameraPositionZ?: string | number;
    lookAtPositionX?: string | number;
    lookAtPositionY?: string | number;
    lookAtPositionZ?: string | number;
    targetX?: string | number;
    targetY?: string | number;
    targetZ?: string | number;
}

export const corresponding: { [key: string]: string } = {
    "A": "viseme_PP",
    "B": "viseme_SS",
    "C": "viseme_E",
    "D": "viseme_aa",
    "E": "viseme_O",
    "F": "viseme_U",
    "G": "viseme_FF",
    "H": "viseme_CH",
    "X": "viseme_sil",
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
