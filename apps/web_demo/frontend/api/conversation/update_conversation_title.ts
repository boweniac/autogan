import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "../request_open";
import { getRequestAPI } from "../request";

export const updateConversationTitleAPI = async (conversation_id: string, title: string | undefined) => {
  if (title == undefined) {
    title = ""
  }
    await getRequestAPI(`/agent/update_conversation_title?conversation_id=${conversation_id}&title=${title}`)
  };