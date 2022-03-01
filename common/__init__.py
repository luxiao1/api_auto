# python的模块就是单例模式，所有的模块只会被导入一次
import setting
from common.loghandler import get_logger
from common.db_handler import SQLdbHandler

logger = get_logger(**setting.LOG_CONFIG)
db = SQLdbHandler(db_config=setting.DB_CONFIG)