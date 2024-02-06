import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "../request_open";
import { getRequestAPI } from "../request";

export const deleteConversationAPI = async (conversation_id: string) => {
    await getRequestAPI(`/agent/delete_conversation?conversation_id=${conversation_id}`)
  };