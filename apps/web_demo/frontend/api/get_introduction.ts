import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI } from "./request_open";
import { IntroductionMessage, IntroductionMessageBlock } from "@/stores/TypeIntroduction";

export const getIntroductionAPI = async (caseID: string) => {
    const res = await getOpenRequestAPI(`/open/agent/get_introduction?case_id=${caseID}`)
    if (Object.keys(res).length === 0) {
      return false
    } else {
      // let msg_id = ""
      // let messages: IntroductionMessage[] = []
      // res.messages.map((jsonString: string) => {
      //   const message_block = JSON.parse(jsonString) as IntroductionMessageBlock
      //   message_block.localID = uuidv4()
      //   if (message_block.msg_id != msg_id) {
      //     messages = [
      //       ...messages,
      //       {
      //         localID: uuidv4(),
      //         msg_id: message_block.msg_id,
      //         agent_name: message_block.agent_name,
      //         message_blocks: [message_block]
      //       }
      //     ]
      //   } else {
      //     messages = messages.map((m) => {
      //       if (m.msg_id === msg_id) {
      //           m.message_blocks = [
      //             ...m.message_blocks,
      //             message_block
      //           ]
      //           return m
      //       }
      //       return m;
      //     });
      //   }
      // });
      return res as IntroductionMessage[]
    }
  };
function uuidv4(): string | undefined {
  throw new Error("Function not implemented.");
}

