import autogan
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider


# 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
aliyun_oss = autogan.dict_from_json("ALIYUN_OSS")
auth = oss2.Auth(aliyun_oss["access_key_id"], aliyun_oss["access_key_secret"])

# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
endpoint = 'oss-cn-beijing.aliyuncs.com'

# 填写Bucket名称。
bucket = oss2.Bucket(auth, endpoint, 'aibowen-base')