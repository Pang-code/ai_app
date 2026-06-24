from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough


def test1(x: int):
    return x + 10

# 节点：封装为标准 Runnable 组件
r1 = RunnableLambda(test1)  # 把函数封装成 Runnable 可链式组件

# 1调用示例
print(r1.invoke(5))   # 输出 15


# 2批量调用
print(r1.batch([1, 2, 3]))





# 3、流式调用
def test2(prompt: str):
    for item in prompt.split(' '):
        yield item

r1 = RunnableLambda(test2)
for item in r1.stream('hello world'):
    print(item)





# 4、组合链
r1 = RunnableLambda(test1)
r2 = RunnableLambda(lambda x: x * 2)

# 用管道 | 拼接成链式流程：先执行 r1，结果传给 r2
chain1 = r1 | r2   # 串行

# 调用示例
res = chain1.invoke(5)
print(res)   # 计算逻辑：(5+10)*2 = 30



# 5、并行运行 RunnableParallel
chain = RunnableParallel(r1=r1, r2=r2)

# 调用测试
result = chain.invoke(input=2, config={"max_concurrency": 2}) # 最大并发数
print(result)


## 组合多个 Runnable 组件


new_chain = chain1 | chain

new_chain.get_graph().print_ascii() # grandalf
print( new_chain.invoke(2) )




# 6、合并输入，并处理中间数据
# RunnablePassthrough：允许传递输入数据，可以保持不变或添加额外的键。必须传入一个字典数据，还可过滤

r1 = RunnableLambda(lambda x: {"key1": x})
r2 = RunnableLambda(lambda x: x["key1"] + 10)

# chain = r1 |  r2
# chain = r1 | RunnablePassthrough.assign(new_key=r2)
# chain = r1 | RunnablePassthrough.assign(new_key=r2)
chain = r1 | RunnablePassthrough()|RunnablePassthrough.assign(new_key=r2)
print(chain.invoke(2))

chain = r1 | RunnableParallel(
    foo=RunnablePassthrough(),
    new_key=RunnablePassthrough.assign(key2=r2)
) | RunnablePassthrough()

chain = r1 | RunnableParallel(
    foo=RunnablePassthrough(),
    new_key=RunnablePassthrough.assign(key2=r2)
) | RunnablePassthrough().pick(['new_key'])  # 过滤只要new_key

r3 = RunnableLambda(lambda x: x["new_key"]["key2"])
chain = r1 | RunnableParallel(
    foo=RunnablePassthrough(),
    new_key=RunnablePassthrough.assign(key2=r2)
) | RunnablePassthrough().pick(['new_key']) |r3  # 过滤只要new_key


print(chain.invoke(2))


# 7、后备选项：后备选项是一种可以在紧急情况下使用的替代方案。
r1 = RunnableLambda(test1)
r2 = RunnableLambda(lambda x: int(x) + 10)

# chain = r1.with_fallbacks([备选方案1, 备选方案2, 最终兜底方案])
chain = r1.with_fallbacks([r2])
print(chain.invoke('2'))





# 8、重试策略 重复多次执行某个节点

from langchain_core.runnables import RunnableLambda

# 全局计数器
counter = 0

def test3(x):
    global counter
    counter += 1
    print(f'执行了 {counter} 次')
    return x / counter

# # 绑定重试策略：最多尝试4次
# r1 = RunnableLambda(test3).with_retry(stop_after_attempt=4)
# print(r1.invoke(2))


# 根据条件，动态的构建链
r1 = RunnableLambda(test1)
r2 = RunnableLambda(lambda x: [x] * 2)


# 根据r1的输出结果，判断，是否要执行r2，（判断本身也是一个节点）
# chain = r1 | RunnableLambda(lambda x: r2 if x>12 else RunnablePassthrough().assign(res=x))
chain = r1 | RunnableLambda(lambda x: r2 if x > 12 else RunnableLambda(lambda x: x))

print(chain.invoke(2))



# 9. 周期管理

import time
from langchain_core.runnables import RunnableLambda
from datetime import datetime

import pytz

# 东八区时区
tz_cn = pytz.timezone("Asia/Shanghai")

def test4(n: int):
    time.sleep(n)
    return n * 2

r1 = RunnableLambda(test4)

from langchain_core.tracers import Run

def on_start(run_obj: Run):
    """ 当r1节点启动的时候，自动调用 """
    print('r1启动的时间：', run_obj.start_time.astimezone(tz_cn))
from langchain_core.tracers import Run

def on_end(run_obj: Run):
    """ 当r1节点已经运行结束的时候，自动调用 """
    print('r1结束的时间：', run_obj.end_time.astimezone(tz_cn))

chain = r1.with_listeners(on_start=on_start, on_end=on_end)
print(chain.invoke(2))
