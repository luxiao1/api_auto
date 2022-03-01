import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 项目的域名
PROJECT_HOST = 'http://api.lemonban.com/futureloan'
# 接口地址
INTERRACES = {
    'register': PROJECT_HOST+'/member/register',
    'login': PROJECT_HOST+'/member/login',
    'recharge': PROJECT_HOST+'/member/recharge',
    'add': PROJECT_HOST+'/loan/add',
    'audit': PROJECT_HOST+'/loan/audit'
}

# 日志配置
LOG_CONFIG = {
    'name': 'py45',
    'filename': os.path.join(BASE_DIR,'logs','test.log'),
    'debug': 'false',
}

# 测试用例目录
TEST_CASE_DIR = os.path.join(BASE_DIR,'testcase')

# 测试数据
TEST_DATA_FILE = os.path.join(BASE_DIR, 'testdata', 'data.xlsx')

# 测试报告
REPORT_CONFIG = {
    'report_dir': os.path.join(BASE_DIR, 'reports'),
    'title': '测试报告',
    'desc': 'web自动化测试报告',
    'tester': '测试name',
    'templates': '2'
}

# 数据库配置
DB_CONFIG = {
        'engine': 'mysql',
        'host': 'api.lemonban.com',
        'user': 'future',
        'password': '123456',
        'port': 3306,
        'db': 'futureloan',
        'charset': 'utf8',
        'autocommit': True  # 设置默认每次查询都提交事务，解决重复读的问题
  }