from redis import Redis,StrictRedis

if __name__ == '__main__':
    #连接redis两种写法
    # url="redis://:密码@IP:端口/数据库编号"
    # redis=Redis.from_url(url="redis://:@127.0.0.1:6379/0")

    redis = Redis(host="127.0.0.1", port=6379, password="", db=0)

    # # 字符串
    # # set name xiaoming
    # redis.set("name", "xiaoming")

    # # setex sms_13312345678 30 500021
    # mobile = 13728504162
    # redis.setex(f"sms_{mobile}", 30, "500021")

    # ret=redis.get(f"sms_{mobile}")
    # # redis中最基本的数据类型是字符串，但是这种字符串是bytes，所以对于python而言，读取出来的字符串数据还要decode才能使用
    # print(ret,ret.decode())

    #提取数据 如果不存在则返回none
    # code_types=redis.get(f"sms_{mobile}")
    # print(code_types)
    # if code_types:
    #     #判断code_types时才解码
    #     print(code_types.decode())


    ##设置字典 单个成员
    # hset user name org
    # redis.hset("user", "name", "org")

    #多个成员
    # data={# # 获取当前仓库的所有的key
    #     "name": "org",
    #     "age": 12,
    #     "sex": 1
    # }
    # redis.hset("user",mapping=data)

    # # 获取字典所有成员，字典的所有成员都是键值对，而键值对也是bytes类型，所以需要推导式进行转换
    # ret=redis.hgetall("user")
    # print(ret)
    # data={key.decode():value.decode() for (key,value) in ret.items()}
    # print(data)

    # # 获取当前仓库的所有的key
    # ret=redis.keys("*")
    # print(ret)
    # 
    # # 删除key
    # if len(ret) > 0:
    #     redis.delete(ret[0])