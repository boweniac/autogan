import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI } from "./request_open";

export const aliyunStsAPI = async () => {
    const res = await getOpenRequestAPI(`/open/agent/aliyun_sts`)
    if (res) {
        notifications.show({
          message: "成功创建新会话🎉",
          color: "green",
        });
      }
      return res
  };