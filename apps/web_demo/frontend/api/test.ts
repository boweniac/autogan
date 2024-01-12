import { Stream } from 'stream';
import http from "http";
import {notifications} from "@mantine/notifications";
import axios, {AxiosProgressEvent, AxiosRequestConfig} from "axios";
import {localStore} from "@/stores/LocalStore";

const get = localStore.getState;

export async function streamTestAPI(content: string, conversationID: string, abortController?: AbortController | undefined, callback?: ((res: any) => void) | undefined, endCallback?: (() => void) | undefined, errorCallback?: (() => void) | undefined): Promise<void>{
    try {
        const payload = JSON.stringify({
            user_id: 1,
            conversation_id: conversationID,
            content: content,
        });

        const req = http.request(
            {
                hostname: get().gateWayHost,
                port: get().gateWayPort,
                path: "/open/agent/test",
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                signal: abortController?.signal,
            },
            (res) => {
                if (res.statusCode === 200) {
                    res.on("data", (chunk) => {
                        if (abortController?.signal.aborted) {
                            res.destroy();
                            endCallback?.();
                            return;
                        }
                        // 将响应拆分成单独的消息
                        let buffer = '';
                        const allMessages = chunk.toString().split("\n\n\n");
                        for (const message of allMessages) {
                            buffer += message.toString();
                            // 切掉响应数据前缀
                            const cleaned = buffer.match(/(?<=data:).*$/s)?.toString();
                            if (!cleaned || cleaned === " [DONE]") {
                                return;
                            }
                            // 序列化
                            let parsed;
                            try {
                                parsed = JSON.parse(cleaned);
                            } catch (e) {
                                buffer += "\\n\\n\\n"
                                console.error(e);
                                continue;
                            }
                            callback?.(parsed);
                            buffer = '';
                        }
                    });
                    res.on("end", () => {
                        endCallback?.();
                    });
                } else {
                    res.on("data", (chunk) => {
                        const data = JSON.parse(chunk)
                        notifications.show({
                            message: "请求错误：" + data.msg,
                            color: "red",
                        });
                    });
                    return;
                }
            }
        );
        req.write(payload);
        req.end();
    } catch (e: any) {
        if (axios.isAxiosError(e)) {
            console.error(e.response?.data);
        }
        notifications.show({
            message: "请求错误：" + e,
            color: "red",
        });
        throw e;
    }
};

export async function getOpenRequestAPI(path: string) {
    try {
        const res = await axios.get(get().gateWayProtocol + get().gateWayHost + ":" + get().gateWayPort + path);
        if (res.status === 200) {
            if (res.data) {
                return res.data;
            } else {
                return true
            }
        }
        notifications.show({
            message: "请求错误：" + res.data.msg,
            color: "red",
        });
    } catch (e: any) {
        if (axios.isAxiosError(e)) {
            console.error(e.response?.data);
        }
        notifications.show({
            message: "请求错误：" + e,
            color: "red",
        });
        throw e;
    }
}

export async function postOpenRequestAPI(path: string, payload: any) {
    try {
        const res = await axios.post(get().gateWayProtocol + get().gateWayHost + ":" + get().gateWayPort + path, payload);
        if (res.status === 200) {
            if (res.data) {
                return res.data;
            } else {
                return true
            }
        }
        notifications.show({
            message: "请求错误：" + res.data.msg,
            color: "red",
        });
    } catch (e: any) {
        if (axios.isAxiosError(e)) {
            console.error(e.response?.data);
        }
        notifications.show({
            message: "请求错误：" + e,
            color: "red",
        });
        throw e;
    }
}

// export const reviver = (key: string, value: any) => {
//     if (typeof value === 'number') {
//       return value.toString();
//     }
//     return value;
//   };