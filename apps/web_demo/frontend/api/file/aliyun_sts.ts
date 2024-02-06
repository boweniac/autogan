import { notifications } from "@mantine/notifications";
import { getOpenRequestAPI } from "../request_open";
import { getRequestAPI } from "../request";

export const aliyunStsAPI = async () => {
    const res = await getRequestAPI(`/agent/aliyun_sts`)
    return res
  };