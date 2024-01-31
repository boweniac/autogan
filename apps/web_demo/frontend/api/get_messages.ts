import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI, postOpenRequestAPI } from "./request_open";
import { AgentConversation, Message, MessageBlock } from "@/stores/TypeAgentChat";
// import { reviver } from "./test"
import { v4 as uuidv4 } from "uuid";

export const getMessagesAPI = async (conversation_id: string) => {
    const res = await getOpenRequestAPI(`/open/agent/get_messages?conversation_id=${conversation_id}`)
      if (Object.keys(res).length === 0) {
        return []
      } else {
        let msg_id = ""
        let messages: Message[] = []
        res.messages.map((jsonString: string) => {
          const message_block = JSON.parse(jsonString) as MessageBlock
          message_block.localID = uuidv4()
          if (message_block.msg_id != msg_id) {
            messages = [
              ...messages,
              {
                task_id: message_block.task_id,
                localID: uuidv4(),
                msg_id: message_block.msg_id,
                agent_name: message_block.agent_name,
                message_blocks: [{
                  task_id: message_block.task_id,
                  localID: message_block.localID,
                  msg_id: message_block.msg_id,
                  agent_name: message_block.agent_name,
                  content_type: message_block.content_type,
                  content_tag: message_block.content_tag,
                  content: message_block.content,
                  tokens: message_block.tokens,
                }]
              }
            ]
          } else {
            messages = messages.map((m) => {
              if (m.msg_id === msg_id) {
                  m.message_blocks = [
                    ...m.message_blocks,
                    {
                      task_id: message_block.task_id,
                      localID: message_block.localID,
                      msg_id: message_block.msg_id,
                      agent_name: message_block.agent_name,
                      content_type: message_block.content_type,
                      content_tag: message_block.content_tag,
                      content: message_block.content,
                      tokens: message_block.tokens,
                    }
                  ]
                  return m
              }
              return m;
            });
          }
        });
        return messages
      }
  };