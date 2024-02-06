import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI } from "../request_open";
import { getRequestAPI } from "../request";
import { InitAgentConversationMessageState } from "@/stores/LocalStoreActions";

export const addAgentConversationAPI = async () => {
    const res = await getRequestAPI(`/agent/add_conversation`)
    if (res) {
      InitAgentConversationMessageState(res.conversationId, [])
      return res.conversationId
    }
  };