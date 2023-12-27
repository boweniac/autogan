import uuid
import time
import threading


def create_time_based_uuid() -> str:
    # 获取当前时间的时间戳
    timestamp = time.time()

    # 创建一个基于时间戳的UUID
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(timestamp)))


class SnowflakeIdGenerator:
    def __init__(self, datacenter_id, worker_id):
        # 时间戳部分所占长度
        self.timestamp_bits = 41
        # 数据中心标识所占长度
        self.datacenter_id_bits = 5
        # 机器标识所占长度
        self.worker_id_bits = 5
        # 序列号所占长度
        self.sequence_bits = 12

        # 最大取值计算
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

        # 时间戳的偏移量
        self.twepoch = 1288834974657

        # 数据中心标识和机器标识
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id

        # 序列号和最后一次时间戳初始值
        self.sequence = 0
        self.last_timestamp = -1

        # 锁
        self.lock = threading.Lock()

        # 校验数据中心ID和机器ID的范围
        if self.datacenter_id > self.max_datacenter_id or self.datacenter_id < 0:
            raise ValueError("datacenter_id should be between 0 and {}".format(self.max_datacenter_id))
        if self.worker_id > self.max_worker_id or self.worker_id < 0:
            raise ValueError("worker_id should be between 0 and {}".format(self.max_worker_id))

    @staticmethod
    def _next_millis(last_timestamp):
        timestamp = int(time.time() * 1000)
        while timestamp <= last_timestamp:
            timestamp = int(time.time() * 1000)
        return timestamp

    @staticmethod
    def _til_next_millis(last_timestamp):
        timestamp = int(time.time() * 1000)
        while timestamp <= last_timestamp:
            time.sleep(0.001)
        return timestamp

    def next_id(self):
        with self.lock:
            timestamp = int(time.time() * 1000)
            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards. Refusing to generate id for {} milliseconds".format(
                    self.last_timestamp - timestamp))

            if self.last_timestamp == timestamp:
                self.sequence = (self.sequence + 1) & self.sequence_mask
                if self.sequence == 0:
                    timestamp = self._til_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            return ((timestamp - self.twepoch) << (
                        self.datacenter_id_bits + self.worker_id_bits + self.sequence_bits)) | \
                (self.datacenter_id << (self.worker_id_bits + self.sequence_bits)) | \
                (self.worker_id << self.sequence_bits) | \
                self.sequence
