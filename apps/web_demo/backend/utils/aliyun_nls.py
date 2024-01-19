import time
import threading
import nls

URL = "wss://nls-gateway-cn-beijing.aliyuncs.com/ws/v1"
TOKEN = "c7fa8c7b0cb64812859b7e6ae0896c27"  # 参考https://help.aliyun.com/document_detail/450255.html获取token
APPKEY = "hQ0ZUxRpHidDh1ve"  # 获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist


# 以下代码会根据音频文件内容反复进行一句话识别
class TestSr:
    def __init__(self, tid, test_file):
        self.__th = threading.Thread(target=self.__test_run)
        self.__id = tid
        self.__test_file = test_file

    def loadfile(self, filename):
        with open(filename, "rb") as f:
            self.__data = f.read()

    def start(self):
        self.loadfile(self.__test_file)
        self.__th.start()

    def test_on_start(self, message, *args):
        print("test_on_start:{}".format(message))

    def test_on_error(self, message, *args):
        print("on_error args=>{}".format(args))

    def test_on_close(self, *args):
        print("on_close: args=>{}".format(args))

    def test_on_result_chg(self, message, *args):
        print("test_on_chg:{}".format(message))

    def test_on_completed(self, message, *args):
        print("on_completed:args=>{} message=>{}".format(args, message))

    def __test_run(self):
        print("thread:{} start..".format(self.__id))

        sr = nls.NlsSpeechRecognizer(
            url=URL,
            token=TOKEN,
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

        self.__slices = zip(*(iter(self.__data),) * 640)
        for i in self.__slices:
            sr.send_audio(bytes(i))
            time.sleep(0.01)

        r = sr.stop()
        print("{}: sr stopped:{}".format(self.__id, r))
        time.sleep(1)

