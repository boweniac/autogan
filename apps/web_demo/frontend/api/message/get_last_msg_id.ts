import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI } from "../request_open";
import { getRequestAPI } from "../request";

export const getLastMsgIdAPI = async (conversation_id: string) => {
    const res = await getRequestAPI(`/agent/get_last_msg_id?conversation_id=${conversation_id}`)
    return res?.msgId
  };