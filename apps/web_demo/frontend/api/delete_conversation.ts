import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "./request_open";

export const deleteConversationAPI = async (conversation_id: string) => {
    const res = await getOpenRequestAPI(`/open/agent/delete_conversation?conversation_id=${conversation_id}`)
    if (res) {
        notifications.show({
          message: "成功创建新会话🎉",
          color: "green",
        });
      }
  };