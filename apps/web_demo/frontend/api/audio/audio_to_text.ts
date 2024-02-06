import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "../request_open";
import { AudioAndLip, LipsData, MouthCues } from "@/stores/TypeAudioAndLip";
import { postRequestAPI } from "../request";



export const audioToTextAPI = async (formData: FormData) => {
    const res = await postRequestAPI(`/agent/audio_to_text`, formData)
    return res.text
  };