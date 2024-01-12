import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "./test";
import { AgentConversation, Message } from "@/stores/TypeAgentChat";
// import { reviver } from "./test"
import { v4 as uuidv4 } from "uuid";

export const getMessagesAPI = async (conversation_id: string) => {
    const res = await getOpenRequestAPI(`/open/agent/get_messages?conversation_id=${conversation_id}`)
    if (res) {
        notifications.show({
          message: "成功创建新会话🎉",
          color: "green",
        });
      }
      if (Object.keys(res).length === 0) {
        return []
      } else {
        const messages: Message[] = res.messages.map((jsonString: string) => {
          const message = JSON.parse(jsonString) as Message
          message.localID = uuidv4()

          return message
        });
        return messages
      }
  };