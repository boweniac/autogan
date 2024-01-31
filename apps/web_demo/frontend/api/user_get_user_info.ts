import { Dispatch, SetStateAction } from "react";
import { getOpenRequestAPI } from "./request_open";
import { notifications } from "@mantine/notifications";
import { updateUserPhoneState, updateUserStateState } from "@/stores/LocalStoreActions";
import { getRequestAPI } from "./request";

export const getUserInfoAPI = async () => {
    const res = await getRequestAPI(`/user/user-info`)
    if (res) {
      updateUserPhoneState(res.phone)
      updateUserStateState(res.state)
      return true
    }
    return false
  };