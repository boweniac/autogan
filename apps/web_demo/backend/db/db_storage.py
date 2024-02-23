import json
from typing import Optional
import redis

import autogan
import mysql.connector
from mysql.connector import Error
from DBUtils.PooledDB import PooledDB

from autogan.protocol.storage_protocol import StorageProtocol


class DBStorage(StorageProtocol):
    def __init__(self):
        """外部存储类，用于持久化存储会话数据，以便在服务重启或迁移后可衔接历史会话

        SQL表：
            agent_conversation：用于存储会话信息（不包括对话内容）
                - main_field：id, user_id, title
            agent_task：用于存储任务信息（不包括对话内容）
                - main_field：conversation_id, par_task_id, par_agent_name, par_agent_type, task_id, agent_name, agent_type, content
            agent_message：存储会话消息记录（完整会话消息，用于前端展示，不根据任务进行分割）
                - main_field：msg_id, conversation_id, task_id, content_type, content_tag, agent_name, content, tokens
            agent_task_message：缓存任务消息记录
                - main_field：id, task_id, role, name, tokens, content

        REDIS键：
            convs_list（哈希）：用于缓存用户会话列表（不包括对话内容）
                - key：用户 id
                - value：用户的会话列表
            convs_user_perms（哈希）：用户缓存会话鉴权信息
                - key：会话 id
                - value：用户 id
            task_get_par_id（哈希）：用于通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
                - key：下级任务id_上级 agent 名称
                - value：上级任务 id
            task_get_id（哈希）: 用于通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。
                - key：上级任务id_下级 agent 名称
                - value：下级任务 id
            task_info（哈希）：用于缓存任务信息。
                - key：任务 id
                - value：上级 agent 名称, 上级 agent 类型, 任务内容
            conv_last_task_id（哈希）：用于缓存会话中 agent 执行的最后一个任务 id
                - key：会话 id_agent 名称
                - value：最后一个任务的 id
            conv_last_msg_id（哈希）：用于缓存会话最后一条消息 id 的缓存。
                - key：会话 id
                - value：最后一条消息的 id
            task_comp_messages（哈希）：用于缓存任务的消息记录
                - key：任务 id
                - value：消息列表
        """
        redis_config_dict = autogan.dict_from_json("REDIS_CONFIG")
        mysql_config_dict = autogan.dict_from_json("MYSQL_CONFIG")

        self._redis = redis.Redis(
            host=redis_config_dict["host"],
            port=redis_config_dict["port"],
            password=redis_config_dict["password"],
            db=0,
            decode_responses=True)
        self._mysql = PooledDB(
            creator=mysql.connector,  # 使用链接数据库的模块
            maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的
            # threadsafety都为1，所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。如：0 = None = never, 1 = default = whenever it is requested,
            # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=mysql_config_dict["host"],
            port=mysql_config_dict["port"],
            user=mysql_config_dict["user"],
            password=mysql_config_dict["password"],
            database=mysql_config_dict["database"],
            charset='utf8'
        )

    def add_conversation(self, user_id: int, conversation_id: int):
        """添加会话
        SQL操作：
            - agent_conversation：插入新记录

        REDIS操作：
            - convs_list：删除用户会话列表缓存
            - convs_user_perms: 新增会话/用户鉴权缓存"""
        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """INSERT INTO `agent_conversation` (`id`, `user_id`) VALUES (%s, %s)"""
            record_tuple = (conversation_id, user_id)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)

            conn.commit()

            # REDIS 操作
            self._redis.hdel('convs_list', *[str(user_id)])
            self._redis.hset('convs_user_perms', str(conversation_id), str(user_id))
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def update_conversation_title(self, user_id: int, conversation_id: int, title: str):
        """更新会话标题
        SQL操作：
            - agent_conversation：更新 title 字段

        REDIS操作：
            - convs_list：删除用户会话列表缓存"""
        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """UPDATE agent_conversation SET title = %s WHERE id = %s AND user_id = %s"""
            record_tuple = (title, conversation_id, user_id)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)

            conn.commit()

            # REDIS 操作
            self._redis.hdel('convs_list', *[str(user_id)])
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def delete_conversation(self, user_id: int, conversation_id: int):
        """删除会话
        SQL操作：
            - agent_conversation：删除指定 id 记录

        REDIS操作：
            - convs_list：删除用户会话列表缓存
            - convs_user_perms: 删除会话/用户鉴权缓存"""
        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """UPDATE agent_conversation SET is_delete = 1 WHERE id = %s AND user_id = %s"""
            # sql_query = """DELETE FROM agent_conversation WHERE id = %s AND user_id = %s"""
            record_tuple = (conversation_id, user_id)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)

            conn.commit()

            # REDIS 操作
            self._redis.hdel('convs_list', *[str(user_id)])
            self._redis.hdel('convs_user_perms', *[str(conversation_id)])
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_conversations(self, user_id: int) -> Optional[list]:
        """获取会话列表
        REDIS操作：
            - convs_list：获取用户会话列表缓存

        失败后执行操作：
        SQL：
            - agent_conversation：查询符合特定 用户 id 值的所有记录

        REDIS：
            - convs_list：新增用户会话列表缓存"""
        convs_list = self._redis.hget('convs_list', str(user_id))
        if convs_list:
            return json.loads(convs_list)

        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """SELECT id, title FROM agent_conversation WHERE user_id = %s AND is_delete = 0 ORDER BY gmt_create DESC"""
            record_tuple = (user_id,)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)
                records = cursor.fetchall()

                if records:
                    self._redis.hset('convs_list', str(user_id), json.dumps(records))
                    return records
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def user_conversation_permissions(self, user_id: int, conversation_id: int) -> bool:
        """获取会话列表
        REDIS操作：
            - convs_user_perms：查询会话/用户鉴权缓存

        失败后执行操作：
        SQL：
            - agent_conversation：查询符合特定 会话 id 和 用户 id 值的记录

        REDIS：
            - convs_user_perms：添加会话/用户鉴权缓存"""
        user_id_str = self._redis.hget('convs_user_perms', str(conversation_id))
        if user_id_str is not None:
            if user_id_str == str(user_id):
                return True
            else:
                return False
        else:
            conn = self._mysql.connection()
            try:
                # SQL 操作
                sql_query = """SELECT id FROM agent_conversation WHERE id = %s AND user_id = %s AND is_delete = 0"""
                record_tuple = (conversation_id, user_id)

                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(sql_query, record_tuple)
                    records = cursor.fetchone()

                    if records:
                        self._redis.hset('convs_user_perms', str(conversation_id), str(user_id))
                        return True
            except Error as e:
                print(f"Error while connecting to MySQL: {e}")
                conn.rollback()
            finally:
                conn.close()
            return False

    def add_task(self, conversation_id: int, par_task_id: int, par_agent_name: str, par_agent_type: str, task_id: int,
                 agent_name: str, agent_type: str, content: str):
        """添加任务
        SQL操作：
            - agent_task：插入新记录

        REDIS操作：
            - task_get_par_id：新增通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
            - task_get_id: 新增通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。
            - task_info：新增任务信息缓存。
            - conv_last_task_id：新增会话中 agent 执行的最后一个任务 id 的缓存。"""
        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """INSERT INTO `agent_task` (`conversation_id`, `par_task_id`, `par_agent_name`, `par_agent_type`, `task_id`, `agent_name`, `agent_type`, `content`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            record_tuple = (
                conversation_id, par_task_id, par_agent_name, par_agent_type, task_id, agent_name, agent_type, content)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)

            conn.commit()

            # REDIS 操作
            self._redis.hset('task_get_par_id', f"{task_id}_{par_agent_name}", str(par_task_id))
            self._redis.hset('task_get_id', f"{par_task_id}_{agent_name}", str(task_id))
            self._redis.hset('task_info', str(task_id), json.dumps(
                {"par_agent_name": par_agent_name, "par_agent_type": par_agent_type, "content": content}))
            self._redis.hset('conv_last_task_id', f"{conversation_id}_{agent_name}", str(task_id))
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_task_info(self, task_id: int) -> Optional[dict]:
        """获取任务信息
        REDIS操作：
            - task_info：获取任务信息缓存

        失败后执行操作：
        SQL：
            - agent_conversation：查询符合特定 用户 id 值的所有记录

        REDIS：
            - task_get_par_id：新增通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
            - task_get_id: 新增通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。
            - task_info：新增任务信息缓存。"""
        task_info = self._redis.hget('task_info', str(task_id))
        if task_info:
            return json.loads(task_info)

        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """SELECT par_task_id, par_agent_name, par_agent_type, agent_name, content FROM agent_task WHERE task_id = %s"""
            record_tuple = (task_id,)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)
                records = cursor.fetchone()

                if records:
                    # REDIS 操作
                    self._redis.hset('task_get_par_id', f"{task_id}_{records['par_agent_name']}",
                                     str(records["par_task_id"]))
                    self._redis.hset('task_info', str(task_id), json.dumps(
                        {"par_agent_name": records["par_agent_name"], "par_agent_type": records["par_agent_type"],
                         "content": records["content"]}))
                    self._redis.hset('task_get_id', f"{records['par_task_id']}_{records['agent_name']}", str(task_id))
                return records
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def convert_main_or_sub_task_id(self, task_id: int, receiver_name: str) -> tuple[Optional[int], Optional[int]]:
        """转换任务 id：将下级任务 id 转换为上级任务 id，或是将上级任务 id 转换为下级任务 id
        REDIS操作：
            - task_get_par_id：通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
            - task_get_id: 通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。

        失败后执行操作：
        SQL：
            - agent_task：通过下级任务 di 和上级 agent 名称，查找上级任务 id。
            - agent_task: 通过上级任务 di 和下级 agent 名称，查找下级任务 id。

        REDIS：
            - task_get_par_id：新增通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
            - task_get_id: 新增通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。
            - task_info：新增任务信息缓存。"""
        par_task_id_str = self._redis.hget('task_get_par_id', f"{task_id}_{receiver_name}")
        par_task_id = int(par_task_id_str) if par_task_id_str else None
        task_id_str = self._redis.hget('task_get_id', f"{task_id}_{receiver_name}")
        task_id = int(task_id_str) if task_id_str else None

        if par_task_id is None and task_id is None:
            conn = self._mysql.connection()
            try:
                # SQL 操作
                sql_query = """SELECT par_task_id, par_agent_type, agent_name, content FROM agent_task WHERE task_id = %s AND par_agent_name = %s"""
                record_tuple = (task_id, receiver_name)

                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(sql_query, record_tuple)
                    records = cursor.fetchone()

                    if records:
                        # REDIS 操作
                        self._redis.hset('task_get_par_id', f"{task_id}_{receiver_name}", str(records["par_task_id"]))
                        self._redis.hset('task_info', str(task_id), json.dumps(
                            {"par_agent_name": receiver_name, "par_agent_type": records["par_agent_type"],
                             "content": records["content"]}))
                        self._redis.hset('task_get_id', f"{records['par_task_id']}_{records['agent_name']}",
                                         str(task_id))
                        par_task_id = records["par_task_id"]

                sql_query = """SELECT par_agent_name, par_agent_type, task_id, content FROM agent_task WHERE par_task_id = %s AND agent_name = %s"""
                record_tuple = (task_id, receiver_name)

                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(sql_query, record_tuple)
                    records = cursor.fetchone()

                    if records:
                        # REDIS 操作
                        self._redis.hset('task_get_par_id', f"{records['task_id']}_{records['par_agent_name']}",
                                         str(task_id))
                        self._redis.hset('task_info', str(records["task_id"]), json.dumps(
                            {"par_agent_name": records["par_agent_name"], "par_agent_type": records["par_agent_type"],
                             "content": records["content"]}))
                        self._redis.hset('task_get_id', f"{task_id}_{receiver_name}", str(records["task_id"]))
                        task_id = records["task_id"]
            except Error as e:
                print(f"Error while connecting to MySQL: {e}")
                conn.rollback()
            finally:
                conn.close()

        return par_task_id, task_id

    def get_conversation_latest_task(self, conversation_id: int, agent_name: str) -> Optional[int]:
        """获取会话中 agent 执行的最后一个任务 id
        REDIS操作：
            - conv_last_task_id：获取会话中 agent 执行的最后一个任务 id 的缓存。

        失败后执行操作：
        SQL：
            - agent_task：查询会话中 agent 执行的最后一个任务 id

        REDIS：
            - conv_last_task_id：缓存会话中 agent 执行的最后一个任务 id"""
        task_id = self._redis.hget(f'conv_last_task_id', f"{conversation_id}_{agent_name}")
        if task_id:
            return int(task_id)

        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """SELECT task_id FROM agent_task WHERE conversation_id = %s AND agent_name = %s ORDER BY gmt_create DESC LIMIT 1"""
            record_tuple = (conversation_id, agent_name)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)
                records = cursor.fetchone()

                if records:
                    # REDIS 操作
                    self._redis.hset('conv_last_task_id', f"{conversation_id}_{agent_name}", str(records["task_id"]))
                    return records["task_id"]
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def add_message(self, conversation_id: int, message: dict) -> None:
        """添加会话消息记录（完整会话消息，用于前端展示，不根据任务进行分割）
        SQL操作：
            - agent_message：插入新记录

        REDIS操作：
            - conv_last_msg_id：新增会话最后一条消息 id 的缓存。"""
        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """INSERT INTO `agent_message` (`msg_id`, `conversation_id`, `task_id`, `content_type`, `content_tag`, `agent_name`, `agent_type`, `content`, `tokens`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            record_tuple = (
                message["msg_id"], conversation_id, message["task_id"], message["content_type"], message["content_tag"],
                message["agent_name"], message["agent_type"], message["content"], message["tokens"])

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)

            conn.commit()

            # REDIS 操作
            self._redis.hset('conv_last_msg_id', str(conversation_id), str(message["msg_id"]))
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_last_msg_id(self, conversation_id: int) -> Optional[int]:
        """获取会话中最后一条消息的 id
        REDIS操作：
            - conv_last_msg_id：获取会话最后一条消息 id 的缓存。

        失败后执行操作：
        SQL：
            - agent_task：查询会话最后一条消息的 id

        REDIS：
            - conv_last_msg_id：缓存会话最后一条消息的 id"""
        msg_id = self._redis.hget(f'conv_last_msg_id', str(conversation_id))
        if msg_id:
            return int(msg_id)

        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """SELECT msg_id FROM agent_message WHERE conversation_id = %s AND is_delete = 0 ORDER BY gmt_create DESC LIMIT 1"""
            record_tuple = (conversation_id,)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)
                records = cursor.fetchone()

                if records:
                    # REDIS 操作
                    self._redis.hset('conv_last_msg_id', str(conversation_id), str(records["msg_id"]))
                    return records["msg_id"]
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_messages_when_changed(self, conversation_id: int, last_msg_id: int) -> Optional[list]:
        """如会话的最后一条消息 id 与传入参数的 last_msg_id 不符，则返回会话的所有消息记录
        REDIS操作：
            - conv_last_msg_id：获取会话最后一条消息 id 的缓存。

        失败后执行操作：
        SQL：
            - agent_message：查询会话最后一条消息 id

        REDIS：
            - conv_last_msg_id：缓存会话最后一条消息的 id

        如不符则执行操作：
        SQL：
            - agent_message：获取会话的所有消息记录"""
        msg_id = self._redis.hget(f'conv_last_msg_id', str(conversation_id))
        if msg_id and int(msg_id) == last_msg_id:
            return None

        conn = self._mysql.connection()
        try:
            if msg_id is None:
                # SQL 操作
                sql_query = """SELECT msg_id FROM agent_message WHERE conversation_id = %s AND is_delete = 0 ORDER BY gmt_create DESC LIMIT 1"""
                record_tuple = (conversation_id,)

                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(sql_query, record_tuple)
                    records = cursor.fetchone()

                    if records:
                        # REDIS 操作
                        self._redis.hset('conv_last_msg_id', str(conversation_id), str(records["msg_id"]))
                        msg_id = records["msg_id"]

            if msg_id is None:
                return []

            if int(msg_id) == last_msg_id:
                return None

            # SQL 操作
            sql_query = """SELECT msg_id, task_id, content_type, content_tag, agent_name, agent_type, content, tokens FROM agent_message WHERE conversation_id = %s AND is_delete = 0 ORDER BY gmt_create ASC"""
            record_tuple = (conversation_id,)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)
                records = cursor.fetchall()
                return records
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_messages(self, conversation_id: int) -> Optional[list]:
        """获取会话所有消息记录（完整会话消息，用于前端展示，不根据任务进行分割）
        SQL操作：
            - agent_message：获取会话的所有消息记录"""
        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """SELECT msg_id, task_id, content_type, content_tag, agent_name, agent_type, content, tokens FROM agent_message WHERE conversation_id = %s AND is_delete = 0 ORDER BY gmt_create ASC"""
            record_tuple = (conversation_id,)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)
                records = cursor.fetchall()

                return records
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def save_compressed_messages(self, task_id: int, messages: list) -> None:
        """缓存压缩后的任务消息记录
        REDIS操作：
            - task_comp_messages：缓存任务消息记录"""
        self._redis.hset('task_comp_messages', str(task_id), json.dumps(messages))

    def add_compressed_message(self, task_id: int, message: dict) -> None:
        """添加任务消息记录
        SQL操作：
            - agent_task_message：插入新记录

        REDIS操作：
            - task_comp_messages：获取任务消息记录缓存
            - task_comp_messages：更新任务消息记录缓存"""
        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """INSERT INTO `agent_task_message` (`task_id`, `role`, `name`, `tokens`, `content`) VALUES (%s, %s, %s, %s, %s)"""
            record_tuple = (task_id, message["role"], message["name"], message["tokens"], message["content"])

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)

            conn.commit()

            # REDIS 操作
            messages = self._redis.hget(f'task_comp_messages', str(task_id))
            if messages:
                decoded = json.loads(messages)
                decoded.append(message)
                self._redis.hset('task_comp_messages', str(task_id), json.dumps(decoded))
            else:
                self._redis.hset('task_comp_messages', str(task_id), json.dumps([message]))
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_compressed_messages(self, task_id: int) -> Optional[list]:
        """获取任务消息记录
        REDIS操作：
            - task_comp_messages：获取任务消息记录缓存。

        失败后执行操作：
        SQL：
            - agent_task_message：查询任务的所有消息记录

        REDIS：
            - task_comp_messages：更新任务消息记录缓存"""
        messages = self._redis.hget('task_comp_messages', str(task_id))
        if messages:
            return json.loads(messages)

        conn = self._mysql.connection()
        try:
            # SQL 操作
            sql_query = """SELECT role, name, tokens, content FROM agent_task_message WHERE task_id = %s AND is_delete = 0 ORDER BY gmt_create DESC"""
            record_tuple = (task_id,)

            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, record_tuple)
                records = cursor.fetchall()

                if records:
                    self._redis.hset('task_comp_messages', str(task_id), json.dumps(records))

                return records
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            conn.rollback()
        finally:
            conn.close()
