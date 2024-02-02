#! /usr/bin/env python
# coding=utf-8
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from alibabacloud_sts20150401.models import AssumeRoleResponseBodyCredentials
import autogan
import oss2
from alibabacloud_sts20150401.client import Client as Sts20150401Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_sts20150401 import models as sts_20150401_models
from alibabacloud_tea_util import models as util_models

# 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
aliyun_oss = autogan.dict_from_json("ALIYUN_OSS")
auth = oss2.Auth(aliyun_oss["access_key_id"], aliyun_oss["access_key_secret"])

# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
endpoint = 'oss-cn-beijing.aliyuncs.com'

# 填写Bucket名称。
bucket = oss2.Bucket(auth, endpoint, 'aibowen-base')


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Sts20150401Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Sts
        config.endpoint = f'sts.cn-beijing.aliyuncs.com'
        return Sts20150401Client(config)

    @staticmethod
    def main() -> AssumeRoleResponseBodyCredentials:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，
        # 仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client(aliyun_oss["access_key_id"], aliyun_oss["access_key_secret"])
        assume_role_request = sts_20150401_models.AssumeRoleRequest(
            role_arn='acs:ram::1641649638081567:role/oss',
            role_session_name='ali'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            assumeRoleResponse = client.assume_role_with_options(assume_role_request, runtime)
            return assumeRoleResponse.body.credentials
        except Exception as error:
            # 错误 message
            print(error)
            # 诊断地址
            # print(error.data.get("Recommend"))
            # UtilClient.assert_as_string(error.message)
