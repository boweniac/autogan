import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI } from "./request_open";
import { IntroductionMessage, IntroductionMessageBlock } from "@/stores/TypeIntroduction";

export const getIntroductionAPI = async (caseID: string) => {
    const res = await getOpenRequestAPI(`/open/agent/get_introduction?case_id=${caseID}`)
    if (Object.keys(res).length === 0) {
      return false
    } else {
      return res as IntroductionMessage[]
    }
  };
function uuidv4(): string | undefined {
  throw new Error("Function not implemented.");
}

