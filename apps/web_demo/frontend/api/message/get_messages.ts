import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "../request_open";
import { AgentConversationMessage, Message, MessageBlock } from "@/stores/TypeAgentChat";
// import { reviver } from "./test"
import { v4 as uuidv4 } from "uuid";
import { getRequestAPI } from "../request";
import { InitAgentConversationMessageState } from "@/stores/LocalStoreActions";

export const convertMessages = (messagesList: MessageBlock[]) => {
  let msg_id = ""
  let messages: Message[] = []
  messagesList.map((messageBlock) => {
    messageBlock.localID = uuidv4()
    if (messageBlock.msgId != msg_id) {
      messages = [
        ...messages,
        {
          task_id: messageBlock.taskId,
          localID: uuidv4(),
          msg_id: messageBlock.msgId,
          agent_name: messageBlock.agentName,
          message_blocks: [{
            taskId: messageBlock.taskId,
            localID: messageBlock.localID,
            msgId: messageBlock.msgId,
            agentName: messageBlock.agentName,
            contentType: messageBlock.contentType,
            contentTag: messageBlock.contentTag,
            content: messageBlock.content,
            tokens: messageBlock.tokens,
          }]
        }
      ]
      console.log(`messageBlock.msg_id:`+JSON.stringify(messageBlock.msgId));
    } else {
      messages = messages.map((m) => {
        if (m.msg_id === msg_id) {
            m.message_blocks = [
              ...m.message_blocks,
              {
                taskId: messageBlock.taskId,
                localID: messageBlock.localID,
                msgId: messageBlock.msgId,
                agentName: messageBlock.agentName,
                contentType: messageBlock.contentType,
                contentTag: messageBlock.contentTag,
                content: messageBlock.content,
                tokens: messageBlock.tokens,
              }
            ]
        }
        return m;
      });
    }
  });
  return messages
}

export const getMessagesWhenChangedAPI = async (conversation_id: string, last_msg_id: string | undefined) => {
  let path = `/agent/get_messages_when_changed?conversation_id=${conversation_id}`
  if (last_msg_id) {
    path += "&last_msg_id="+last_msg_id
  }
  const messagesList = await getRequestAPI(path) as MessageBlock[] | undefined
  let messages: Message[] = []

  if (messagesList && messagesList.length > 0) {
    messages = convertMessages(messagesList)
    InitAgentConversationMessageState(conversation_id, messages)
  }
};