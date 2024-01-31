import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "./request_open";
import { AudioAndLip, LipsData, MouthCues } from "@/stores/TypeAudioAndLip";



export const audioToTextAPI = async (formData: FormData) => {
    const res = await postOpenRequestAPI(`/open/agent/audio_to_text`, formData)
    if (res) {
        notifications.show({
          message: "成功创建新会话🎉",
          color: "green",
        });
      }
      // console.log(`audioToTextAPI.res:`+JSON.stringify(res.text));
      return res.text
  };