# 一、模块介绍

quickdb 是一个操作合集

* mysql
* postgresql
* kafka
* mongo
* redis

## 二 mysql

使用 sqlalchemy 为其定义了一个类

* MysqlSQLAlchemyEngine

### 2.1、MysqlSQLAlchemyEngine

该类继承自 SQLAlchemyEngineBase 用来定义连接 \
可接收 sqlalchemy create_engine 的参数

    engine = MysqlSQLAlchemyEngine(host='localhost', port=3306, user='root', pwd='1234', db='test')
    
    with engine.session() as session, session.begin:
        pass

    with engine.connection() as conn, conn.begin:
        pass

### 2.2、MysqlSQLAlchemyEngine 方法

其含有以下方法：

* reverse_table_model：逆向表模型
* insert_one
* insert_many
* upsert_one
* upsert_many
* delete
* execute
* merge

主要说一下 reverse_table_model
该方法含有三个参数：

* path：生成的 model 路径，需含文件名
* tables：需要的表，可不指定
* commands：额外的命令

      method = MysqlSQLAlchemyMethods(engine=engine)
      method.reverse_table_model(path='./modules.py')

## 三、postgresql

同 mysql

## 四、kafka

主要是使用了 with 和方便的 send，会帮助你将 msg 转化为 bytes，也可以同时 flush

    p = KafkaMsgProducer(server=xxx)
    p.send(topic, msg)

    with KafkaMsgProducer(server=xxx) as p:
        p.send()

## 五、mongo

通过 get_collection 返回的是修改过的 Collection 对象，其有两个新方法

- iter: 快速迭代数据库
- upsert_one：插入或更新的便捷写法

```
conn = MongoConn(host, port)
col = conn.get_collection(db, col)

for i in col.iter():
    print(i)
```

其使用了 with，可以自动回收连接

    conn = MongoConn(host, port)
    col = conn.get_collection(db, col)
    conn.close()

    with MongoConn(host, port) as conn:
        col = conn.get_collection(db, col)

## 六、redis

### 1、redisConn

    with RedisConn() as conn:
        pass

### 2、RedisLock

这是一个阻塞的 redis 事务锁

    with RedisLock(lock_name=""):
        pass

### 3、RedisLockNoWait

这是一个非阻塞的 redis 事务锁，只有获取到锁的人才执行，获取不到就不会继续等待锁，但是需要使用 lock_success 判断

    with RedisLockNoWait(lock_name=") as lock:
        if lock.lock_success:
            ...