import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

# 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
auth = oss2.Auth("LTAI5tNit1NuR8R3nSyBKU38", "hN3eGaL7NyDtsP9VP9S1MTE7x8bDqy")

# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
endpoint = 'oss-cn-beijing.aliyuncs.com'

# 填写Bucket名称。
bucket = oss2.Bucket(auth, endpoint, 'aibowen-base')