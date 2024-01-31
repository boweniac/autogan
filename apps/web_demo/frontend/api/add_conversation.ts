import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI } from "./request_open";

export const addAgentConversationAPI = async () => {
    const res = await getOpenRequestAPI(`/open/agent/add_conversation`)
    if (res) {
        notifications.show({
          message: "成功创建新会话🎉",
          color: "green",
        });
      }
      return res.conversationId
  };