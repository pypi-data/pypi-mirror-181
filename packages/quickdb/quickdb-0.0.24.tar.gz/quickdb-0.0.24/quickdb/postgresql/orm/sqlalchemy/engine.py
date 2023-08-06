"""
    pg 连接类

    engine = PostgreSQLAlchemyEngine(host='localhost', port=5432, user='postgres', pwd='1234', db='postgres')
"""
import re
from typing import List
from sqlalchemy.engine import Result
from sqlalchemy.dialects.postgresql import insert
from quickdb.orm.sqlalchemy.engine import SQLAlchemyEngineBase, BaseModel


class PostgreSQLAlchemyEngine(SQLAlchemyEngineBase):
    def __init__(self, host: str = '127.0.0.1', port: int = 5432, user: str = 'postgres', pwd: str = None,
                 db: str = 'postgres', **kwargs):
        """

        :param host: ip
        :param port: port
        :param user: 账号
        :param pwd: 密码
        :param db: 对应的数据库
        :param kwargs: 其余 SQLAlchemy 参数
        """
        super().__init__('postgresql+psycopg2', host, port, user, pwd, db, **kwargs)

    def upsert_one(
            self,
            instance: BaseModel,
            constraint: str = None,
            index_elements: List[str] = None,
            index_where=None,
            update_keys: List[str] = None,
            exclude_keys: List[str] = None
    ) -> Result:
        """
        做 更新或插入 操作
        详情见：https://docs.sqlalchemy.org/en/20/dialects/postgresql.html

        index_where=my_table.c.user_email.like('%@gmail.com')

        :param instance: 数据
        :param constraint: 表上唯一或排除约束的名称，或者约束对象本身
        :param index_elements: 由字符串列名、列对象或其他列表达式对象组成的序列
        :param index_where: 可用于推断条件目标索引的附加 WHERE 条件
        :param update_keys: 需要更新的字段（无则全更）
        :param exclude_keys: 需要排除的字段（无则全更）
        :return:
        """
        instance_dict = self._get_dict(instance)  # 获取实例的字典
        update_dict = self._get_update_data(instance_dict, update_keys, exclude_keys)  # 获取需要更新的字典

        # 构造 sql 语句
        upsert_sql = insert(instance.__table__).values(instance_dict).on_conflict_do_update(
            constraint=constraint,
            index_elements=index_elements,
            index_where=index_where,
            set_=update_dict
        )

        return self.execute(upsert_sql)

    def upsert_many(
            self,
            instance: List[BaseModel],
            constraint: str = None,
            index_elements: List[str] = None,
            index_where: str = None,
            update_keys: List[str] = None,
            exclude_keys: List[str] = None
    ) -> Result:
        """
        做 更新或插入 操作（这里使用原生 sql）

        :param instance: 数据
        :param constraint: 表上唯一或排除约束的名称，或者约束对象本身
        :param index_elements: 由字符串列名、列对象或其他列表达式对象组成的序列
        :param index_where: 可用于推断条件目标索引的附加 WHERE 条件
        :param update_keys: 需要更新的字段（无则全更）
        :param exclude_keys: 需要排除的字段（无则全更）
        :return:
        """
        instance_dict = self._get_dict(instance[0])  # 获取实例的字典
        update_dict = self._get_update_data(instance_dict, update_keys, exclude_keys)  # 获取需要更新的字典

        # 构造 sql 语句（只是利用其构造语句）
        sql = str(insert(instance[0].__table__).values(instance_dict).on_conflict_do_update(
            constraint=constraint,
            index_elements=index_elements,
            index_where=index_where,
            set_=update_dict
        ))

        # 使用原生的连接执行，否则会无法执行
        with self.connection() as conn, conn.begin():
            replace_str = 'SET ' + ', '.join([f'{i} = excluded.{i}' for i in list(update_dict.keys())]) + ' RETURNING'
            sql = re.sub(r'SET (.+) RETURNING', replace_str, sql)

            return conn.execute(sql, [self._get_dict(i) for i in instance])
