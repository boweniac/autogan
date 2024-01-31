import { Stream } from 'stream';
import http from "http";
import {notifications} from "@mantine/notifications";
import axios, {AxiosProgressEvent, AxiosRequestConfig} from "axios";
import {localStore} from "@/stores/LocalStore";
// import { getCurrentAbortController } from '@/stores/LocalStoreActions';

const get = localStore.getState;

export async function uploadFileStreamAPI(files: any[], apiType: string, baseId: string | undefined, conversationId: string | undefined, callback?: ((res: any) => void) | undefined, endCallback?: (() => void) | undefined, errorCallback?: (() => void) | undefined): Promise<void>{
    const uploaders = files.map((file) => {
        // abortController = getCurrentAbortController()
        let formData = new FormData();
        formData.append('file', file);
        formData.append('api_type', apiType);
        formData.append('base_id', baseId ? baseId : "0");
        formData.append('conversation_id', conversationId ? conversationId : "0");
        formData.append('file_name', file.name);

        fetch(get().gateWayProtocol + get().gateWayHost + ":" + get().gateWayPort + "/open/agent/add_file", {
            method: 'POST',
            // headers: {
            //     'Authorization': get().userToken
            // },
            body: formData,
        })
            .then(response => {
                if (response.ok) {
                    return response.body;
                } else {
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
                        // console.log(`message.toString():`+message.toString());
                        buffer += message.toString();
                        // console.log(`buffer2.toString():`+buffer.toString());
                        // 切掉响应数据前缀
                        const cleaned = buffer.match(/(?<=data:).*$/s)?.toString();
                        // 序列化
                        let parsed;
                        try {
                            console.log(`cleaned:`+cleaned);
                            // const cleanedString = cleaned.replace(/\n|\r/g, "\\n");
                            // parsed = JSON.parse(cleanedString);
                            if (cleaned != undefined) {
                                parsed = JSON.parse(cleaned);
                            }
                        } catch (e) {
                            buffer += "\n\n\n"
                            // console.log(`buffer1.toString():`+buffer.toString());
                            console.error(e);
                            continue;
                        }
                        callback?.(parsed);
                        buffer = '';
                    }
                    // const regex = /(\d+\.\d+)/; // 匹配浮点数的正则表达式
                    // const match = str.match(regex); // 使用正则表达式匹配字符串中的浮点数
                    // if (match) {
                    //     const floatValue = parseFloat(match[0]); // 将匹配到的字符串转换为浮点数
                    //     console.log(`floatValue:`+JSON.stringify(floatValue));
                    // }
                    return reader.read().then(processText);
                });
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    });
    try {
        await Promise.all(uploaders);
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
