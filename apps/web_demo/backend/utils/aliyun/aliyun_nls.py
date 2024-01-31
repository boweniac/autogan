import json
import time
import threading
import sys
from typing import AnyStr

import nls

from apps.web_demo.backend.utils.aliyun.aliyun_access import aliyun_access

URL = aliyun_access.aliyun_nls_conf["url"]
# TOKEN = aliyun_access.nls_token  # 参考https://help.aliyun.com/document_detail/450255.html获取token
APPKEY = aliyun_access.aliyun_nls_conf["app_key"]  # 获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist


# 以下代码会根据音频文件内容反复进行一句话识别
class TestSr:
    def __init__(self, tid, test_file):
        self.__result = ""
        self.__token = aliyun_access.nls_token
        # self.__th = threading.Thread(target=self.__test_run)
        self.__id = tid
        self.__test_file = test_file
        self.__data: AnyStr = b''

    def loadfile(self):
        with open(self.__test_file, "rb") as f:
            self.__data = f.read()

    # def start(self):
    #     self.loadfile(self.__test_file)
    #     return self.__th.start()

    def test_on_start(self, message, *args):
        print("test_on_start:{}".format(message))

    def test_on_error(self, message, *args):
        print("on_error args=>{}".format(args))

    def test_on_close(self, *args):
        print("on_close: args=>{}".format(args))

    def test_on_result_chg(self, message, *args):
        print("test_on_chg:{}".format(message))

    def test_on_completed(self, message, *args):
        print(type(json.loads(message)))
        self.__result = json.loads(message)["payload"]["result"]
        print("on_completed:args=>{} message=>{}".format(args, message))

    def test_run(self):
        with open(self.__test_file, "rb") as f:
            file_content = f.read()
        print("thread:{} start..".format(self.__id))

        sr = nls.NlsSpeechRecognizer(
            url=URL,
            token=self.__token,
            appkey=APPKEY,
            on_start=self.test_on_start,
            on_result_changed=self.test_on_result_chg,
            on_completed=self.test_on_completed,
            on_error=self.test_on_error,
            on_close=self.test_on_close,
            callback_args=[self.__id]
        )
        # while True:
        print("{}: session start".format(self.__id))
        r = sr.start(aformat="pcm", ex={"hello": 123})

        self.__slices = zip(*(iter(file_content),) * 640)
        for i in self.__slices:
            sr.send_audio(bytes(i))
            time.sleep(0.01)

        r = sr.stop()
        print("{}: sr stopped:{}".format(self.__id, r))
        return self.__result
            # time.sleep(1)

#
# def multiruntest(num=500):
#     for i in range(0, num):
#         name = "thread" + str(i)
#         t = TestSr(name, "tests/test1.pcm")
#         t.start()
#
#
# # 设置打开日志输出
# nls.enableTrace(True)
# multiruntest(1)