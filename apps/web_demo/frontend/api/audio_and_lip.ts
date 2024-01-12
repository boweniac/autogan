import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "./test";
import { AudioAndLip, LipsData, MouthCues } from "@/stores/TypeAudioAndLip";



export const audioAndLipAPI = async (text: string, voice: string, speed: number) => {
    const res = await postOpenRequestAPI(`/open/agent/audio_and_lip`, {"text": text, "voice": voice, "speed": speed})
    if (res) {
        notifications.show({
          message: "成功创建新会话🎉",
          color: "green",
        });
      }
      const audioAndLip: AudioAndLip = res;
      const lipsData = JSON.parse(audioAndLip.lipsData as string) as LipsData;
      audioAndLip.lipsData = lipsData.mouthCues;
      return audioAndLip
  };