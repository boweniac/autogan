import { Stream } from 'stream';
import http from "http";
import {notifications} from "@mantine/notifications";
import axios, {AxiosProgressEvent, AxiosRequestConfig} from "axios";
import {localStore} from "@/stores/LocalStore";
import { openLogInModal, resetLogOutState } from '@/stores/LocalStoreActions';
// import { getCurrentAbortController } from '@/stores/LocalStoreActions';

const get = localStore.getState;
const gateWayProtocol = process.env.GATE_WAY_PROTOCOL || ""
const gateWayHost = process.env.GATE_WAY_HOST || ""
const gateWayPort = process.env.GATE_WAY_PORT || ""

export async function uploadFileStreamAPI(files: any[], apiType: string, baseId: string | undefined, conversationId: string | undefined, callback?: ((res: any) => void) | undefined, endCallback?: (() => void) | undefined, errorCallback?: (() => void) | undefined): Promise<void>{
    if (!get().userToken) {
        openLogInModal()
        notifications.show({
            message: "请先完成登陆",
            color: "red",
        });
        return
    }
    const uploaders = files.map((file) => {
        // abortController = getCurrentAbortController()
        let formData = new FormData();
        formData.append('file', file);
        formData.append('api_type', apiType);
        formData.append('base_id', baseId ? baseId : "0");
        formData.append('conversation_id', conversationId ? conversationId : "0");
        formData.append('file_name', file.name);
        fetch(gateWayProtocol + gateWayHost + ":" + gateWayPort + "/agent/add_file", {
            method: 'POST',
            headers: {
                'Authorization': get().userToken
            },
            body: formData,
        })
            .then(response => {
                if (response.ok) {
                    return response.body;
                } else {
                    // resetLogOutState()
                    openLogInModal()
                    throw new Error('Network response was not ok.');
                }
            })
            .then(stream => {
                const reader = stream?.getReader();
                reader?.read().then(function processText({ done, value }): Promise<any> {
                    if (done) {
                        return Promise.resolve();
                    }
                    const str = new TextDecoder("utf-8").decode(value);
                    let buffer = '';
                    const allMessages = str.split("\n\n");
                    for (const message of allMessages) {
                        buffer += message.toString();
                        // 切掉响应数据前缀
                        const cleaned = buffer.match(/(?<=data:).*$/s)?.toString();
                        // 序列化
                        let parsed;
                        try {
                            // const cleanedString = cleaned.replace(/\n|\r/g, "\\n");
                            // parsed = JSON.parse(cleanedString);
                            if (cleaned != undefined) {
                                parsed = JSON.parse(cleaned);
                            }
                        } catch (e) {
                            buffer += "\n\n\n"
                            console.error(e);
                            continue;
                        }
                        callback?.(parsed);
                        buffer = '';
                    }
                    return reader.read().then(processText);
                });
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            })
            .then(body => {
                console.log(`response:`+JSON.stringify(body));
              });
    });
    try {
        await Promise.all(uploaders);
    } catch (e: any) {
        if (axios.isAxiosError(e)) {
            notifications.show({
                message: "请求错误：" + e,
                color: "red",
            });
        }
    }
};
