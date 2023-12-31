import logging
from conf import Conf
import datetime
import os


# 定义日志级别映射
log_l = {
    "info":logging.INFO,
    "debug":logging.DEBUG,
    "warning":logging.WARNING,
    "error":logging.ERROR
}
# 创建类
class Logger:
    # 定义参数：写入日志文件的名称test.log，logger名称，日志级别总开关
    def __init__(self,log_file,log_name,log_level):
        # 设置logger名称
        self.logger = logging.getLogger(log_name)
        # 设置日志级别
        self.logger.setLevel(log_l[log_level])
        # 编写输出控制台handler
        # 判断handler是否存在
        if not self.logger.handlers:
            fh_stream = logging.StreamHandler()
            fh_stream.setLevel(log_l[log_level])
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh_stream.setFormatter(formatter)
            self.logger.addHandler(fh_stream)
            # 编写输出日志文件handler
            fh_file = logging.FileHandler(log_file)
            fh_file.setLevel(log_l[log_level])
            fh_file.setFormatter(formatter)
            self.logger.addHandler(fh_file)

# 定义一个外部调用方法
# log_file,log_name,log_level
# 初始化参数数据
# 日文件的名称 = logs目录 +文件名 （当前时间+扩展名.log）
# 目录
log_path = Conf.log_path
# 当前时间
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
# 扩展名
log_extension = ".log"
# 生成
logfile = os.path.join(log_path,current_date + log_extension)
print(logfile)
# 日志级别，log_level
loglevel = "debug"
# 对外方法，初始log工具类，提供给其它类使用
def my_log(log_name= __file__):
    return Logger(logfile,log_name,loglevel).logger

if __name__ == "__main__":
    # my_log("这里可以设置名称")
    log = my_log()
    # log = my_log("测试一下")
    log.info("这是一个info信息")