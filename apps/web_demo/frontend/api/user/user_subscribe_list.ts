import { Dispatch, SetStateAction } from "react";
import { getOpenRequestAPI } from "../request_open";
import { notifications } from "@mantine/notifications";
import { updateUserPhoneState, updateUserStateState } from "@/stores/LocalStoreActions";
import { getRequestAPI } from "../request";

export const subscribeListAPI = async () => {
    const res = await getRequestAPI(`/user/subscribe-list`)
    if (res) {
      return res
    }
    return false
  };