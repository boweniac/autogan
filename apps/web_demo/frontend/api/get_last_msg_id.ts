import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI } from "./request_open";

export const getLastMsgIdAPI = async (conversation_id: string) => {
    const res = await getOpenRequestAPI(`/open/agent/get_last_msg_id?conversation_id=${conversation_id}`)
    if (res) {
        notifications.show({
          message: "成功创建新会话🎉",
          color: "green",
        });
      }
      
      return res.msgId
  };