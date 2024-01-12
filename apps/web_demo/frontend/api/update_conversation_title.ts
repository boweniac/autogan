import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "./test";

export const updateConversationTitleAPI = async (conversation_id: string, title: string | undefined) => {
  if (title == undefined) {
    title = ""
  }
    const res = await getOpenRequestAPI(`/open/agent/update_conversation_title?conversation_id=${conversation_id}&title=${title}`)
    if (res) {
        notifications.show({
          message: "成功创建新会话🎉",
          color: "green",
        });
      }
  };