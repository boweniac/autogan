import { Dispatch, SetStateAction } from "react";
import { getOpenRequestAPI } from "../request_open";
import { notifications } from "@mantine/notifications";

export const sendSmsAPI = async (phone: string, type: number) => {
    const res = await getOpenRequestAPI(`/open/user/send-sms?phone=${phone}&sms_type=${type}`)
    if (res) {
      notifications.show({
        message: "发送成功🎉",
        color: "green",
      });
      return true
    }
    return false
  };