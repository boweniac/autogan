import { Stream } from 'stream';
import http from "http";
import {notifications} from "@mantine/notifications";
import axios, {AxiosProgressEvent, AxiosRequestConfig} from "axios";
import {localStore} from "@/stores/LocalStore";
import { openLogInModal } from '@/stores/LocalStoreActions';
// import { getCurrentAbortController } from '@/stores/LocalStoreActions';

const get = localStore.getState;
const gateWayProtocol = "https://"
const gateWayHost = "nas.boweniac.top"
const gateWayPort = "44403"

export async function streamAPI(path: string, payloadData: {[key: string]: string}, signal: AbortSignal, callback?: ((res: any) => void) | undefined, endCallback?: (() => void) | undefined, errorCallback?: (() => void) | undefined): Promise<void>{
    if (!get().userToken) {
        openLogInModal()
        notifications.show({
            message: "请先完成登陆",
            color: "red",
        });
        return
    }
    try {
        // abortController = getCurrentAbortController()
        const payload = JSON.stringify(payloadData);

        const req = http.request(
            {
                hostname: gateWayHost,
                port: gateWayPort,
                path: path,
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": get().userToken,
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
                            // 切掉响应数据前缀
                            const cleaned = buffer.match(/(?<=data:).*$/s)?.toString();
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
                    req.on('error', (e) => {
                        if (e.name === 'AbortError') {
                        } else {
                          console.error(`请求出现问题: ${e.message}`);
                        }
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

export async function getRequestAPI(path: string) {
    if (!get().userToken) {
        openLogInModal()
        notifications.show({
            message: "请先完成登陆",
            color: "red",
        });
        return
    }
    try {
        const res = await axios.get(gateWayProtocol + gateWayHost + ":" + gateWayPort + path, {
            headers: {
                "Authorization": get().userToken,
            }
        });
        if (res.status === 200) {
            if (res.data.code === 200) {
                if (res.data.data) {
                    return res.data.data;
                }
            } else {
                notifications.show({
                    title: '请求失败',
                    message: res.data.msg,
                    color: "red",
                });
            }
        } else {
            throw new Error(`Request failed with status code ${res.status} ${res.statusText}`);
        }
    } catch (e: any) {
        if (axios.isAxiosError(e)) {
            notifications.show({
                title: '服务错误',
                message: e.message,
                color: "red",
            });
        }
    }
}

export async function postRequestAPI(path: string, payload: any) {
    if (!get().userToken) {
        openLogInModal()
        notifications.show({
            message: "请先完成登陆",
            color: "red",
        });
        return
    }
    try {
        const res = await axios.post(gateWayProtocol + gateWayHost + ":" + gateWayPort + path, payload, {
            headers: {
                'Authorization': get().userToken
            }
        });
        if (res.status === 200) {
            if (res.data.code === 200) {
                if (res.data.data) {
                    return res.data.data;
                }
            } else {
                notifications.show({
                    message: "请求失败：" + res.data.msg,
                    color: "red",
                });
            }
            
        } else {
            throw new Error(`Request failed with status code ${res.status} ${res.statusText}`);
        }
    } catch (e: any) {
        if (axios.isAxiosError(e)) {
            notifications.show({
                title: '服务错误',
                message: e.message,
                color: "red",
            });
        }
    }
}