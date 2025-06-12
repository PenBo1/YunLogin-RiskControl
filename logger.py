import logging
import os
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import sys
from datetime import datetime

# 日志目录
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 当前日期（用于日志文件名）
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

# 基础日志配置
def setup_logger(name="YunLogin谷歌风控"):
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别

    # 防止重复添加handler
    if logger.handlers:
        return logger

    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # 控制台只输出INFO及以上级别
    console_handler.setFormatter(formatter)

    # 文件handler - 按日期分割
    file_handler = TimedRotatingFileHandler(
        filename=f"{LOG_DIR}/app_{CURRENT_DATE}.log",
        when="midnight",  # 每天午夜轮换
        interval=1,
        backupCount=7,  # 保留7天的日志
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)  # 文件记录所有级别
    file_handler.setFormatter(formatter)

    # 错误日志单独记录 - 按文件大小轮换
    error_handler = RotatingFileHandler(
        filename=f"{LOG_DIR}/error.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.WARNING)  # 只记录WARNING及以上级别
    error_handler.setFormatter(formatter)

    # 添加handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    return logger

# 使用示例
logger = setup_logger()

# 封装的日志方法
def log_debug(message):
    logger.debug(message)

def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_error(message):
    logger.error(message, exc_info=True)  # 自动记录异常堆栈

def log_critical(message):
    logger.critical(message, exc_info=True)

# 异常捕获装饰器
def log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {str(e)}", exc_info=True)
            raise  # 可以选择重新抛出异常
    return wrapper

# 使用示例
if __name__ == "__main__":
    log_info("Application started")
    log_debug("This is a debug message")
    log_warning("This is a warning")
