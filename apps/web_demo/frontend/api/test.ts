import { Stream } from 'stream';
import http from "http";
import {notifications} from "@mantine/notifications";
import axios, {AxiosProgressEvent, AxiosRequestConfig} from "axios";
import {localStore} from "@/stores/LocalStore";

const get = localStore.getState;

export async function streamTestAPI(content: string, abortController?: AbortController | undefined, callback?: ((res: any) => void) | undefined, endCallback?: (() => void) | undefined, errorCallback?: (() => void) | undefined): Promise<void>{
    try {
        const payload = JSON.stringify({
            user_id: 1,
            conversation_id: 1,
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
                    console.log("res", res)
                    // callback?.(res);
                    res.on("data", (chunk) => {
                        // console.log("res.on(\"data\", (chunk) => {")
                        if (abortController?.signal.aborted) {
                            res.destroy();
                            endCallback?.();
                            return;
                        }

                        // 将响应拆分成单独的消息
                        const allMessages = chunk.toString().split("\n");
                        for (const message of allMessages) {
                            // 切掉响应数据前缀
                            const cleaned = message.toString().match(/(?<=data:).*$/s);
                            if (!cleaned || cleaned === " [DONE]") {
                                return;
                            }
                            console.log(`cleaned:`+JSON.stringify(cleaned));
                            // 序列化
                            let parsed;
                            try {
                                parsed = JSON.parse(cleaned);
                            } catch (e) {
                                console.error(e);
                                return;
                            }
                            console.log(`parsed:`+JSON.stringify(parsed));
                            callback?.(parsed);
                        }
                    });
                    res.on("end", () => {
                        console.log("res.on(\"end\", () => {")
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
