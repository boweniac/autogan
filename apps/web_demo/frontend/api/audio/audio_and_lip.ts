import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "../request_open";
import { AudioAndLip, LipsData, MouthCues } from "@/stores/TypeAudioAndLip";
import { postRequestAPI } from "../request";



export const audioAndLipAPI = async (text: string, voice: string, speed: number) => {
    const res = await postRequestAPI(`/agent/audio_and_lip`, {"text": text, "voice": voice, "speed": speed})
      const audioAndLip: AudioAndLip = res;
      const lipsData = JSON.parse(audioAndLip.lipsData as string) as LipsData;
      audioAndLip.lipsData = lipsData.mouthCues;
    
      return audioAndLip
  };