import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "../request_open";
import { AgentConversation, AgentConversationMessage } from "@/stores/TypeAgentChat";
import { getRequestAPI } from "../request";
import { clearConversationMessageState, updateAgentConversationListState } from "@/stores/LocalStoreActions";
// import { reviver } from "./test"

export const getConversationsAPI = async () => {
  let conversationIDList: string[] = []
  let conversationList = await getRequestAPI(`/agent/get_conversations`) as AgentConversation[] | undefined
  if (conversationList == undefined) {
    conversationList = []
  } else {
    conversationIDList = conversationList.map((c)=>c.id)
  }
  updateAgentConversationListState(conversationList)
  clearConversationMessageState(conversationIDList)
  return conversationIDList
};