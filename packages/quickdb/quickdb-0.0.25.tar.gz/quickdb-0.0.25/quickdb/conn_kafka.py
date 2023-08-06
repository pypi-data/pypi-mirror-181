"""
    向 kafka 发送数据

    注意：
        有时需要通过判断 future 状态，确认是否成功
        这里结束一定要 flush 不然可能会丢数据！
"""
import json
from typing import Union, List
from kafka import KafkaProducer
from kafka.future import Future


class KafkaMsgProducer:

    def __init__(self, server: Union[str, List[str]], **kwargs):
        """

        :param server: 连接配置 ['ip:port'] 形式
        """

        if not kwargs.get('acks'):
            kwargs['acks'] = -1

        self.producer = KafkaProducer(bootstrap_servers=server, **kwargs)

    def send(self, topic: str, msg: Union[str, dict], flush_now: bool = False) -> Future:
        """

        :param topic: topic
        :param msg: 字符串或者字典
        :param flush_now: 是否每次都立即刷新缓存
        :return:
        """
        if isinstance(msg, dict):
            msg = json.dumps(msg, ensure_ascii=False)

        future = self.producer.send(topic=topic, value=msg.encode())

        if flush_now:
            self.producer.flush()

        return future

    def close(self):
        """
        关闭并刷新缓存

        :return:
        """
        self.producer.flush()
        self.producer.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
