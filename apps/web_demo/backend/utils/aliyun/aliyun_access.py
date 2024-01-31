import json
import time

import autogan
import oss2
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
aliyun_oss_conf = autogan.dict_from_json("ALIYUN_OSS")
aliyun_nls_conf = autogan.dict_from_json("ALIYUN_NLS")


class AliyunAccess:
    def __init__(self, aliyun_oss_conf: dict, aliyun_nls_conf: dict):
        self.aliyun_oss_conf = aliyun_oss_conf
        self.aliyun_nls_conf = aliyun_nls_conf
        self._auth = oss2.Auth(aliyun_oss_conf["access_key_id"], aliyun_oss_conf["access_key_secret"])
        self._nls_expire_time = 0
        self._nls_token = ""

    @property
    def nls_token(self) -> str:
        print("nls_token")
        if self._nls_expire_time < time.time():
            client = AcsClient(
                self.aliyun_oss_conf["access_key_id"],
                self.aliyun_oss_conf["access_key_secret"],
                "cn-shanghai"
            )
            # 创建request，并设置参数。
            request = CommonRequest()
            request.set_method('POST')
            request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
            request.set_version('2019-02-28')
            request.set_action_name('CreateToken')

            try:
                response = client.do_action_with_exception(request)
                print(response)

                jss = json.loads(response)
                if 'Token' in jss and 'Id' in jss['Token']:
                    token = jss['Token']['Id']
                    expire_time = jss['Token']['ExpireTime']
                    self._nls_token = token
                    self._nls_expire_time = expire_time
                    print(token)
                    return token
            except Exception as e:
                print(e)
                return ""
        else:
            return self._nls_token


aliyun_access = AliyunAccess(aliyun_oss_conf, aliyun_nls_conf)
