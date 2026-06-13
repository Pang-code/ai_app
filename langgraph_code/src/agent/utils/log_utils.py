import sys, os
from loguru import logger

# 获得当前项目的绝对路径
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, "logs")  # 存放项目日志目录的绝对路径

if not os.path.exists(log_dir):  # 如果日志目录不存在，则创建
    os.mkdir(log_dir)

# LOG_FILE = "translation.log"  # 存储日志的文件

# Trace < Debug < Info < Success < Warning < Error < Critical
class MyLogger:
    def __init__(self):
        # log_file_path = os.path.join(log_dir, LOG_FILE)
        self.logger = logger  # 写日志的对象
        # 清空所有设置
        self.logger.remove()

        # 添加控制台输出的格式, sys.stdout为输出到屏幕
        self.logger.add(sys.stdout, level='DEBUG',
                        format="<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 线程名
                               "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                               ":<cyan>{line}</cyan> | "  # 行号
                               "<level>{level}</level>: "  # 等级
                               "<level>{message}</level>",  # 日志内容
                        )

        # 输出到文件的格式（注释状态）
        # self.logger.add(log_file_path, level='DEBUG', encoding='UTF-8',
        #                 format='{time:YYYYMMDD HH:mm:ss} - '  # 时间
        #                        '{process.name} | '  # 进程名
        #                        '{thread.name} | '  # 线程名
        #                        '{module}.{function}:{line} | '  # 模块名.方法名:行号
        #                        '{level}: {message}',  # 日志内容
        #                 rotation="10 MB",  # 日志文件轮转
        #                 retention="10 days",  # 日志保留天数
        #                 enqueue=True)  # 多线程安全

    def get_logger(self):
        return self.logger

# 初始化日志实例
log = MyLogger().get_logger()

if __name__ == '__main__':
    # 日志级别测试
    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning('这是一个警告')
    log.trace('xxxx')

    # 测试字符串后缀提取
    print('str.pdf'['str.pdf'.rindex('.'):])  # 输出: .pdf


    # @log.catch  # 整个函数自动加上try，catch。自动捕获异常，并且通过日志打印
    def test():
        try:
            print(3 / 0)
        except ZeroDivisionError as e:
            # log.error(e)  # 仅记录错误信息，无堆栈
            log.exception(e)  # 推荐：记录错误信息+完整堆栈