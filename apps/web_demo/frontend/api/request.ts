import { Stream } from 'stream';
import http from "http";
import {notifications} from "@mantine/notifications";
import axios, {AxiosProgressEvent, AxiosRequestConfig} from "axios";
import {localStore} from "@/stores/LocalStore";
// import { getCurrentAbortController } from '@/stores/LocalStoreActions';

const get = localStore.getState;

export async function streamTestAPI(content: string, conversationID: string, signal: AbortSignal, callback?: ((res: any) => void) | undefined, endCallback?: (() => void) | undefined, errorCallback?: (() => void) | undefined): Promise<void>{
    try {
        // abortController = getCurrentAbortController()
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
                signal: signal,
            },
            (res) => {
                if (res.statusCode === 200) {
                    res.on("data", (chunk) => {
                        if (signal.aborted) {
                            req.abort();
                            res.destroy();
                            endCallback?.();
                            return;
                        }
                        // 将响应拆分成单独的消息
                        let buffer = '';
                        const allMessages = chunk.toString().split("\n\n");
                        for (const message of allMessages) {
                            buffer += message.toString();
                            // console.log(`buffer2.toString():`+buffer.toString());
                            // 切掉响应数据前缀
                            const cleaned = buffer.match(/(?<=data:).*$/s)?.toString();
                            // console.log(`cleaned:`+cleaned);
                            if (!cleaned || cleaned === " [DONE]") {
                                return;
                            }
                            // 序列化
                            let parsed;
                            try {
                                // const cleanedString = cleaned.replace(/\n|\r/g, "\\n");
                                // parsed = JSON.parse(cleanedString);
                                parsed = JSON.parse(cleaned);
                            } catch (e) {
                                buffer += "\n\n\n"
                                // console.log(`buffer1.toString():`+buffer.toString());
                                console.error(e);
                                continue;
                            }
                            callback?.(parsed);
                            buffer = '';
                        }
                    });
                    res.on("end", () => {
                        console.log('请求结束');
                        endCallback?.();
                    });
                    req.on('error', (e) => {
                        if (e.name === 'AbortError') {
                          console.log('请求被中断');
                        } else {
                          console.error(`请求出现问题: ${e.message}`);
                        }
                      });
                    //   req.on('abort', () => {
                    //     console.log('请求被中断事件触发');
                    //   });
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

export async function getRequestAPI(path: string) {
    try {
        const res = await axios.get(get().gateWayProtocol + get().gateWayHost + ":" + get().gateWayPort + path, {
            headers: {
                "Authorization": get().userToken,
            }
        });
        if (res.status === 200) {
            if (res.data.code === 200) {
                if (res.data.data) {
                    return res.data.data;
                } else {
                    return true
                }
            } else {
                notifications.show({
                    title: '请求失败',
                    message: res.data.msg,
                    color: "red",
                });
            }
            
        } else {
            notifications.show({
                title: '服务错误',
                message: "未知错误",
                color: "red",
            });
        }
    } catch (e: any) {
        if (axios.isAxiosError(e)) {
            console.error(e.response?.data);
        }
        notifications.show({
            title: '服务错误',
            message: e,
            color: "red",
        });
        throw e;
    }
}

export async function postRequestAPI(path: string, payload: any) {
    try {
        const res = await axios.post(get().gateWayProtocol + get().gateWayHost + ":" + get().gateWayPort + path, payload, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': get().userToken
            }
        });
        if (res.status === 200) {
            if (res.data.code === 200) {
                if (res.data.data) {
                    return res.data.data;
                } else {
                    return true
                }
            } else {
                notifications.show({
                    message: "请求失败：" + res.data.msg,
                    color: "red",
                });
            }
            
        } else {
            notifications.show({
                message: "服务错误",
                color: "red",
            });
        }
    } catch (e: any) {
        if (axios.isAxiosError(e)) {
            console.error(e.response?.data);
        }
        notifications.show({
            message: "服务错误：" + e,
            color: "red",
        });
        throw e;
    }
}