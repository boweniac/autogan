import json
from typing import Optional
from sqlalchemy import create_engine, text
import redis

import autogan
import mysql.connector
from mysql.connector import Error


from autogan.protocol.storage_protocol import StorageProtocol


class DBStorage(StorageProtocol):
    def __init__(self):
        redis_config_dict = autogan.dict_from_json("REDIS_CONFIG")
        mysql_config_dict = autogan.dict_from_json("MYSQL_CONFIG")

        self._redis = redis.Redis(
            host=redis_config_dict["host"],
            port=redis_config_dict["port"],
            db=0,
            decode_responses=True)

        self._mysql = create_engine(f'mysql+mysqlconnector://{mysql_config_dict["user"]}:{mysql_config_dict["password"]}@{mysql_config_dict["host"]}:{mysql_config_dict["port"]}/{mysql_config_dict["database"]}')

        # self._mysql = mysql.connector.connect(
        #     host=mysql_config_dict["host"],
        #     port=mysql_config_dict["port"],
        #     user=mysql_config_dict["user"],
        #     password=mysql_config_dict["password"],
        #     database=mysql_config_dict["database"],
        # )

    def add_conversation(self, user_id: int, conversation_id: int):
        sql_query = text("INSERT INTO agent_conversation (id, user_id) VALUES (:id, :user_id)")
        record_tuple = {"id": conversation_id, "user_id": user_id}
        with self._mysql.connect() as conn:
            conn.execute(sql_query, record_tuple)
            conn.commit()  # 确保提交事务

        # REDIS 操作
        self._redis.hdel('convs_list', *[str(user_id)])
        self._redis.hset('convs_user_perms', str(conversation_id), str(user_id))

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """INSERT INTO `agent_conversation` (`id`, `user_id`) VALUES (%s, %s)"""
        #         record_tuple = (conversation_id, user_id)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         self._mysql.commit()
        #
        #         # REDIS 操作
        #         self._redis.hdel('convs_list', *[str(user_id)])
        #         self._redis.hset('convs_user_perms', str(conversation_id), str(user_id))
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    def update_conversation_title(self, user_id: int, conversation_id: int, title: str):
        sql_query = text("UPDATE agent_conversation SET title = :title WHERE id = :id AND user_id = :user_id")
        record_tuple = {"title": title, "id": conversation_id, "user_id": user_id}
        with self._mysql.connect() as conn:
            conn.execute(sql_query, record_tuple)
            conn.commit()  # 确保提交事务

        # REDIS 操作
        self._redis.hdel('convs_list', *[str(user_id)])

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """UPDATE agent_conversation SET title = %s WHERE id = %s AND user_id = %s"""
        #         record_tuple = (title, conversation_id, user_id)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         self._mysql.commit()
        #
        #         # REDIS 操作
        #         self._redis.hdel('convs_list', *[str(user_id)])
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    def delete_conversation(self, user_id: int, conversation_id: int):
        sql_query = text("UPDATE agent_conversation SET is_delete = 1 WHERE id = :id AND user_id = :user_id")
        record_tuple = {"id": conversation_id, "user_id": user_id}
        with self._mysql.connect() as conn:
            conn.execute(sql_query, record_tuple)
            conn.commit()  # 确保提交事务

        # REDIS 操作
        self._redis.hdel('convs_list', *[str(user_id)])
        self._redis.hdel('convs_user_perms', *[str(conversation_id)])

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """UPDATE agent_conversation SET is_delete = 1 WHERE id = %s AND user_id = %s"""
        #         # sql_query = """DELETE FROM agent_conversation WHERE id = %s AND user_id = %s"""
        #         record_tuple = (conversation_id, user_id)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         self._mysql.commit()
        #
        #         # REDIS 操作
        #         self._redis.hdel('convs_list', *[str(user_id)])
        #         self._redis.hdel('convs_user_perms', *[str(conversation_id)])
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    def get_conversations(self, user_id: int) -> Optional[list]:
        convs_list = self._redis.hget('convs_list', str(user_id))
        if convs_list:
            return json.loads(convs_list)

        sql_query = text("SELECT id, title FROM agent_conversation WHERE user_id = :user_id AND is_delete = 0 ORDER BY gmt_create DESC")
        record_tuple = {"user_id": user_id}
        with self._mysql.connect() as conn:
            result = conn.execute(sql_query, record_tuple)
            records = result.fetchall()

            print(f"get_conversations: {records}")
            if records:
                self._redis.hset('convs_list', str(user_id), json.dumps(records))
                return records

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """SELECT id, title FROM agent_conversation WHERE user_id = %s AND is_delete = 0 ORDER BY gmt_create DESC"""
        #         record_tuple = (user_id, )
        #
        #         cursor.execute(sql_query, record_tuple)
        #         records = cursor.fetchall()
        #
        #         if records:
        #             self._redis.hset('convs_list', str(user_id), json.dumps(records))
        #             return records
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    def user_conversation_permissions(self, user_id: int, conversation_id: int) -> bool:
        user_id_str = self._redis.hget('convs_user_perms', str(conversation_id))
        if user_id_str is not None:
            if user_id_str == str(user_id):
                return True
            else:
                return False
        else:
            sql_query = text("SELECT id FROM agent_conversation WHERE id = :id AND user_id = :user_id AND is_delete = 0")
            record_tuple = {"id": conversation_id, "user_id": user_id}
            with self._mysql.connect() as conn:
                result = conn.execute(sql_query, record_tuple)
                records = result.fetchone()
            if records:
                self._redis.hset('convs_user_perms', str(conversation_id), str(user_id))
                return True
            # if self._mysql.is_connected():
            #     cursor = self._mysql.cursor(dictionary=True)
            #     try:
            #         # SQL 操作
            #         sql_query = """SELECT id FROM agent_conversation WHERE id = %s AND user_id = %s AND is_delete = 0"""
            #         record_tuple = (conversation_id, user_id)
            #
            #         cursor.execute(sql_query, record_tuple)
            #         records = cursor.fetchone()
            #
            #         if records:
            #             self._redis.hset('convs_user_perms', str(conversation_id), str(user_id))
            #             return True
            #     except Error as e:
            #         print(f"Error while connecting to MySQL: {e}")
            #     finally:
            #         cursor.close()
            return False

    def add_task(self, conversation_id: int, par_task_id: int, par_agent_name: str, par_agent_type: str, task_id: int, agent_name: str, agent_type: str, content: str):
        sql_query = text("INSERT INTO agent_task (conversation_id, par_task_id, par_agent_name, par_agent_type, task_id, agent_name, agent_type, content) VALUES (:conversation_id, :par_task_id, :par_agent_name, :par_agent_type, :task_id, :agent_name, :agent_type, :content)")
        record_tuple = {"conversation_id": conversation_id, "par_task_id": par_task_id, "par_agent_name": par_agent_name, "par_agent_type": par_agent_type, "task_id": task_id, "agent_name": agent_name, "agent_type": agent_type, "content": content}
        with self._mysql.connect() as conn:
            conn.execute(sql_query, record_tuple)
            conn.commit()  # 确保提交事务

        # REDIS 操作
        self._redis.hset('task_get_par_id', f"{task_id}_{par_agent_name}", str(par_task_id))
        self._redis.hset('task_info', str(task_id), json.dumps(
            {"par_agent_name": par_agent_name, "par_agent_type": par_agent_type, "content": content}))
        self._redis.hset('task_get_id', f"{par_task_id}_{agent_name}", str(task_id))
        self._redis.hset('conv_last_task_id', f"{conversation_id}_{agent_name}", str(task_id))

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """INSERT INTO `agent_task` (`conversation_id`, `par_task_id`, `par_agent_name`, `par_agent_type`, `task_id`, `agent_name`, `agent_type`, `content`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        #         record_tuple = (conversation_id, par_task_id, par_agent_name, par_agent_type, task_id, agent_name, agent_type, content)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         self._mysql.commit()
        #
        #         # REDIS 操作
        #         self._redis.hset('task_get_par_id', f"{task_id}_{par_agent_name}", str(par_task_id))
        #         self._redis.hset('task_info', str(task_id), json.dumps({"par_agent_name": par_agent_name, "par_agent_type": par_agent_type, "content": content}))
        #         self._redis.hset('task_get_id', f"{par_task_id}_{agent_name}", str(task_id))
        #         self._redis.hset('conv_last_task_id', f"{conversation_id}_{agent_name}", str(task_id))
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    # def save_task_info(self, task_id: int, task_info: dict):
    #     self._redis.hset('task_info', str(task_id), json.dumps(task_info))

    def get_task_info(self, task_id: int) -> Optional[dict]:
        task_info = self._redis.hget('task_info', str(task_id))
        if task_info:
            return json.loads(task_info)

        sql_query = text("SELECT par_task_id, par_agent_name, par_agent_type, agent_name, content FROM agent_task WHERE task_id = :task_id")
        record_tuple = {"task_id": task_id}
        with self._mysql.connect() as conn:
            result = conn.execute(sql_query, record_tuple)
            records = result.fetchone()
            if records:
                # REDIS 操作
                self._redis.hset('task_get_par_id', f"{task_id}_{records['par_agent_name']}",
                                 str(records["par_task_id"]))
                self._redis.hset('task_info', str(task_id), json.dumps(
                    {"par_agent_name": records["par_agent_name"], "par_agent_type": records["par_agent_type"],
                     "content": records["content"]}))
                self._redis.hset('task_get_id', f"{records['par_task_id']}_{records['agent_name']}", str(task_id))
            return records

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """SELECT par_task_id, par_agent_name, par_agent_type, agent_name, content FROM agent_task WHERE task_id = %s"""
        #         record_tuple = (task_id,)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         records = cursor.fetchone()
        #
        #         if records:
        #             # REDIS 操作
        #             self._redis.hset('task_get_par_id', f"{task_id}_{records['par_agent_name']}", str(records["par_task_id"]))
        #             self._redis.hset('task_info', str(task_id), json.dumps({"par_agent_name": records["par_agent_name"], "par_agent_type": records["par_agent_type"], "content": records["content"]}))
        #             self._redis.hset('task_get_id', f"{records['par_task_id']}_{records['agent_name']}", str(task_id))
        #         return records
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    # def save_main_to_sub_task_id(self, main_task_id: int, sub_task_id: int) -> None:
    #     self._redis.hset('main_to_sub_task_id', str(main_task_id), str(sub_task_id))

    # def save_sub_to_main_task_id(self, main_task_id: int, sub_task_id: int) -> None:
    #     self._redis.hset('sub_to_main_task_id', str(sub_task_id), str(main_task_id))

    def convert_main_or_sub_task_id(self, task_id: int, receiver_name: str) -> tuple[Optional[int], Optional[int]]:
        par_task_id_str = self._redis.hget('task_get_par_id', f"{task_id}_{receiver_name}")
        par_task_id = int(par_task_id_str) if par_task_id_str else None
        task_id_str = self._redis.hget('task_get_id', f"{task_id}_{receiver_name}")
        task_id = int(task_id_str) if task_id_str else None

        if par_task_id is None and task_id is None:
            sql_query = text("SELECT par_task_id, par_agent_type, agent_name, content FROM agent_task WHERE task_id = :task_id AND par_agent_name = :par_agent_name")
            record_tuple = {"task_id": task_id, "par_agent_name": receiver_name}
            with self._mysql.connect() as conn:
                result = conn.execute(sql_query, record_tuple)
                records = result.fetchone()
                if records:
                    # REDIS 操作
                    self._redis.hset('task_get_par_id', f"{task_id}_{receiver_name}", str(records["par_task_id"]))
                    self._redis.hset('task_info', str(task_id), json.dumps({"par_agent_name": receiver_name, "par_agent_type": records["par_agent_type"], "content": records["content"]}))
                    self._redis.hset('task_get_id', f"{records['par_task_id']}_{records['agent_name']}", str(task_id))
                    par_task_id = records["par_task_id"]

            sql_query = text("SELECT par_agent_name, par_agent_type, task_id, content FROM agent_task WHERE par_task_id = :par_task_id AND agent_name = :agent_name")
            record_tuple = {"par_task_id": task_id, "agent_name": receiver_name}
            with self._mysql.connect() as conn:
                result = conn.execute(sql_query, record_tuple)
                records = result.fetchone()
                if records:
                    # REDIS 操作
                    self._redis.hset('task_get_par_id', f"{records['task_id']}_{records['par_agent_name']}", str(task_id))
                    self._redis.hset('task_info', str(records["task_id"]), json.dumps({"par_agent_name": records["par_agent_name"], "par_agent_type": records["par_agent_type"],"content": records["content"]}))
                    self._redis.hset('task_get_id', f"{task_id}_{receiver_name}", str(records["task_id"]))
                    task_id = records["task_id"]

        # if par_task_id is None and task_id is None and self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """SELECT par_task_id, par_agent_type, agent_name, content FROM agent_task WHERE task_id = %s AND par_agent_name = %s"""
        #         record_tuple = (task_id, receiver_name)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         records = cursor.fetchone()
        #
        #         if records:
        #             # REDIS 操作
        #             self._redis.hset('task_get_par_id', f"{task_id}_{receiver_name}", str(records["par_task_id"]))
        #             self._redis.hset('task_info', str(task_id), json.dumps({"par_agent_name": receiver_name, "par_agent_type": records["par_agent_type"], "content": records["content"]}))
        #             self._redis.hset('task_get_id', f"{records['par_task_id']}_{records['agent_name']}", str(task_id))
        #             par_task_id = records["par_task_id"]
        #
        #         sql_query = """SELECT par_agent_name, par_agent_type, task_id, content FROM agent_task WHERE par_task_id = %s AND agent_name = %s"""
        #         record_tuple = (task_id, receiver_name)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         records = cursor.fetchone()
        #
        #         if records:
        #             # REDIS 操作
        #             self._redis.hset('task_get_par_id', f"{records['task_id']}_{records['par_agent_name']}", str(task_id))
        #             self._redis.hset('task_info', str(records["task_id"]), json.dumps({"par_agent_name": records["par_agent_name"], "par_agent_type": records["par_agent_type"],"content": records["content"]}))
        #             self._redis.hset('task_get_id', f"{task_id}_{receiver_name}", str(records["task_id"]))
        #             task_id = records["task_id"]
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

        return par_task_id, task_id

    # def save_conversation_latest_task(self, conversation_id: int, agent_name: str, task_id: int) -> None:
    #     self._redis.hset('conv_last_task', f"{conversation_id}_{agent_name}", str(task_id))

    def get_conversation_latest_task(self, conversation_id: int, agent_name: str) -> Optional[int]:
        task_id = self._redis.hget(f'conv_last_task_id', f"{conversation_id}_{agent_name}")
        if task_id:
            return int(task_id)

        sql_query = text("SELECT task_id FROM agent_task WHERE conversation_id = :conversation_id AND agent_name = :agent_name ORDER BY gmt_create DESC LIMIT 1")
        record_tuple = {"conversation_id": conversation_id, "agent_name": agent_name}
        with self._mysql.connect() as conn:
            result = conn.execute(sql_query, record_tuple)
            records = result.fetchone()
            if records:
                # REDIS 操作
                self._redis.hset('conv_last_task_id', f"{conversation_id}_{agent_name}", str(records["task_id"]))
                return records["task_id"]

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """SELECT task_id FROM agent_task WHERE conversation_id = %s AND agent_name = %s ORDER BY gmt_create DESC LIMIT 1"""
        #         record_tuple = (conversation_id, agent_name)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         records = cursor.fetchone()
        #
        #         if records:
        #             # REDIS 操作
        #             self._redis.hset('conv_last_task_id', f"{conversation_id}_{agent_name}", str(records["task_id"]))
        #             return records["task_id"]
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    # def convert_main_to_sub_task_id(self, task_id: int) -> Optional[int]:
    #     task_id = self._redis.hget(f'main_to_sub_task_id', str(task_id))
    #     if task_id:
    #         return int(task_id)
    #     else:
    #         return None

    # def convert_sub_to_main_task_id(self, task_id: int) -> Optional[int]:
    #     task_id = self._redis.hget(f'sub_to_main_task_id', str(task_id))
    #     if task_id:
    #         return int(task_id)
    #     else:
    #         return None

    def add_message(self, conversation_id: int, message: dict) -> None:
        sql_query = text("INSERT INTO agent_message (msg_id, conversation_id, task_id, content_type, content_tag, agent_name, content, tokens) VALUES (:msg_id, :conversation_id, :task_id, :content_type, :content_tag, :agent_name, :content, :tokens)")
        record_tuple = {"msg_id": message["msg_id"], "conversation_id": conversation_id, "task_id": message["task_id"], "content_type": message["content_type"], "content_tag": message["content_tag"], "agent_name": message["agent_name"], "content": message["content"], "tokens": message["tokens"]}
        with self._mysql.connect() as conn:
            conn.execute(sql_query, record_tuple)
            conn.commit()  # 确保提交事务
        # REDIS 操作
        self._redis.hset('conv_last_msg_id', str(conversation_id), str(message["msg_id"]))

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """INSERT INTO `agent_message` (`msg_id`, `conversation_id`, `task_id`, `content_type`, `content_tag`, `agent_name`, `content`, `tokens`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        #         record_tuple = (message["msg_id"], conversation_id, message["task_id"], message["content_type"], message["content_tag"], message["agent_name"], message["content"], message["tokens"])
        #
        #         cursor.execute(sql_query, record_tuple)
        #         self._mysql.commit()
        #
        #         # REDIS 操作
        #         self._redis.hset('conv_last_msg_id', str(conversation_id), str(message["msg_id"]))
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    def get_last_msg_id(self, conversation_id: int) -> Optional[int]:
        msg_id = self._redis.hget(f'conv_last_msg_id', str(conversation_id))
        if msg_id:
            return int(msg_id)

        sql_query = text("SELECT msg_id FROM agent_message WHERE conversation_id = :conversation_id AND is_delete = 0 ORDER BY gmt_create DESC LIMIT 1")
        record_tuple = {"conversation_id": conversation_id}
        with self._mysql.connect() as conn:
            result = conn.execute(sql_query, record_tuple)
            records = result.fetchone()
        if records:
            # REDIS 操作
            self._redis.hset('conv_last_msg_id', str(conversation_id), str(records["msg_id"]))
            return records["msg_id"]

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """SELECT msg_id FROM agent_message WHERE conversation_id = %s AND is_delete = 0 ORDER BY gmt_create DESC LIMIT 1"""
        #         record_tuple = (conversation_id, )
        #
        #         cursor.execute(sql_query, record_tuple)
        #         records = cursor.fetchone()
        #
        #         if records:
        #             # REDIS 操作
        #             self._redis.hset('conv_last_msg_id', str(conversation_id), str(records["msg_id"]))
        #             return records["msg_id"]
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()
    def get_messages_when_changed(self, conversation_id: int, last_msg_id: int) -> Optional[list]:
        msg_id = self._redis.hget(f'conv_last_msg_id', str(conversation_id))
        if msg_id and int(msg_id) == last_msg_id:
            return None
        if msg_id is None:
            sql_query = text("SELECT msg_id FROM agent_message WHERE conversation_id = :conversation_id AND is_delete = 0 ORDER BY gmt_create DESC LIMIT 1")
            record_tuple = {"conversation_id": conversation_id}
            with self._mysql.connect() as conn:
                result = conn.execute(sql_query, record_tuple)
                records = result.fetchone()
                if records:
                    # REDIS 操作
                    self._redis.hset('conv_last_msg_id', str(conversation_id), str(records["msg_id"]))
                    msg_id = records["msg_id"]

        if msg_id is None:
            return []

        if int(msg_id) == last_msg_id:
            return None

        sql_query = text("SELECT msg_id, task_id, content_type, content_tag, agent_name, content, tokens FROM agent_message WHERE conversation_id = :conversation_id AND is_delete = 0 ORDER BY gmt_create ASC")
        record_tuple = {"conversation_id": conversation_id}
        with self._mysql.connect() as conn:
            return conn.execute(sql_query, record_tuple)

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         if msg_id is None:
        #             # SQL 操作
        #             sql_query = """SELECT msg_id FROM agent_message WHERE conversation_id = %s AND is_delete = 0 ORDER BY gmt_create DESC LIMIT 1"""
        #             record_tuple = (conversation_id,)
        #
        #             cursor.execute(sql_query, record_tuple)
        #             records = cursor.fetchone()
        #
        #             if records:
        #                 # REDIS 操作
        #                 self._redis.hset('conv_last_msg_id', str(conversation_id), str(records["msg_id"]))
        #                 msg_id = records["msg_id"]
        #
        #         if msg_id is None:
        #             return []
        #
        #         if int(msg_id) == last_msg_id:
        #             return None
        #
        #         # SQL 操作
        #         sql_query = """SELECT msg_id, task_id, content_type, content_tag, agent_name, content, tokens FROM agent_message WHERE conversation_id = %s AND is_delete = 0 ORDER BY gmt_create ASC"""
        #         record_tuple = (conversation_id,)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         records = cursor.fetchall()
        #
        #         return records
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    def get_messages(self, conversation_id: int) -> Optional[list]:
        sql_query = text("SELECT msg_id, task_id, content_type, content_tag, agent_name, content, tokens FROM agent_message WHERE conversation_id = :conversation_id AND is_delete = 0 ORDER BY gmt_create ASC")
        record_tuple = {"conversation_id": conversation_id}
        with self._mysql.connect() as conn:
            return conn.execute(sql_query, record_tuple)

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """SELECT msg_id, task_id, content_type, content_tag, agent_name, content, tokens FROM agent_message WHERE conversation_id = %s AND is_delete = 0 ORDER BY gmt_create ASC"""
        #         record_tuple = (conversation_id,)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         records = cursor.fetchall()
        #
        #         return records
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()

    def save_compressed_messages(self, task_id: int, messages: list) -> None:
        self._redis.hset('task_comp_messages', str(task_id), json.dumps(messages))

    def add_compressed_message(self, task_id: int, message: dict) -> None:
        sql_query = text("INSERT INTO agent_task_message (task_id, role, name, tokens, content) VALUES (:task_id, :role, :name, :tokens, :content)")
        record_tuple = {"task_id": task_id, "role": message["role"], "name": message["name"], "tokens": message["tokens"], "content": message["content"]}
        with self._mysql.connect() as conn:
            conn.execute(sql_query, record_tuple)
            conn.commit()  # 确保提交事务

        # REDIS 操作
        messages = self._redis.hget(f'task_comp_messages', str(task_id))
        if messages:
            decoded = json.loads(messages)
            decoded.append(message)
            self._redis.hset('task_comp_messages', str(task_id), json.dumps(decoded))
        else:
            self._redis.hset('task_comp_messages', str(task_id), json.dumps([message]))

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """INSERT INTO `agent_task_message` (`task_id`, `role`, `name`, `tokens`, `content`) VALUES (%s, %s, %s, %s, %s)"""
        #         record_tuple = (task_id, message["role"], message["name"], message["tokens"], message["content"])
        #
        #         cursor.execute(sql_query, record_tuple)
        #         self._mysql.commit()
        #
        #         # REDIS 操作
        #         messages = self._redis.hget(f'task_comp_messages', str(task_id))
        #         if messages:
        #             decoded = json.loads(messages)
        #             decoded.append(message)
        #             self._redis.hset('task_comp_messages', str(task_id), json.dumps(decoded))
        #         else:
        #             self._redis.hset('task_comp_messages', str(task_id), json.dumps([message]))
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()


    def get_compressed_messages(self, task_id: int) -> Optional[list]:
        messages = self._redis.hget('task_comp_messages', str(task_id))
        if messages:
            return json.loads(messages)

        sql_query = text("SELECT role, name, tokens, content FROM agent_task_message WHERE task_id = :task_id AND is_delete = 0 ORDER BY gmt_create DESC")
        record_tuple = {"task_id": task_id}
        with self._mysql.connect() as conn:
            result = conn.execute(sql_query, record_tuple)
            records = result.fetchall()
            if records:
                self._redis.hset('task_comp_messages', str(task_id), json.dumps(records))

            return records

        # if self._mysql.is_connected():
        #     cursor = self._mysql.cursor(dictionary=True)
        #     try:
        #         # SQL 操作
        #         sql_query = """SELECT role, name, tokens, content FROM agent_task_message WHERE task_id = %s AND is_delete = 0 ORDER BY gmt_create DESC"""
        #         record_tuple = (task_id,)
        #
        #         cursor.execute(sql_query, record_tuple)
        #         records = cursor.fetchall()
        #
        #         if records:
        #             self._redis.hset('task_comp_messages', str(task_id), json.dumps(records))
        #
        #         return records
        #     except Error as e:
        #         print(f"Error while connecting to MySQL: {e}")
        #     finally:
        #         cursor.close()