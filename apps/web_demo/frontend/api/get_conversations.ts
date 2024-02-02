import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "./request_open";
import { AgentConversation } from "@/stores/TypeAgentChat";
// import { reviver } from "./test"

export const getConversationsAPI = async () => {
    const res = await getOpenRequestAPI(`/open/agent/get_conversations`)
    if (res) {
        notifications.show({
          message: "成功创建新会话🎉",
          color: "green",
        });
      }
      if (Object.keys(res).length === 0) {
        return []
      } else {
        // const conversations: AgentConversation[] = res.conversations.map((jsonString: string) => JSON.parse(jsonString) as AgentConversation);
        return res as AgentConversation[]
      }
  };