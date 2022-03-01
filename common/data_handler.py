import random
import re
from common import db
from openpyxl import load_workbook


def get_data_from_excel(file,sheet_name=None):
    """

    :param file: excel文件名
    :param sheet_name: 表格名称
    :return:
    """
    # 读取excel文件
    wb = load_workbook(file)
    # 读取对应的表
    if sheet_name is None:
        # 如果不传sheet_name，默认使用第一张表
        ws = wb.active
    else:
        ws = wb[sheet_name]
    # 创建一个列表容器存放数据
    data = []
    # 组织数据
    # 获取表头，作为字典的key
    row_list = list(ws.rows)

    # title = []
    # # 拿到第一行，然后迭代
    # for key in row_list[0]:
    #     title.append(key.value)

    #title = row_list[0]
    title = [item.value for item in row_list[0]]
    # 获取其他数据
    for row in row_list[1:]:
        # 获取每一行的数据
        temp = [i.value for i in row]
        # 将表头与这一行数据打包，换成字典
        data.append(dict(zip(title,temp)))
    return data

def generate_phone():
    """
    随机生成手机号码
    :return:
    """
    # 前面的2位数
    # phone = ['1',str(random.randint(3,9))]
    # # 后面的9位数
    # for i in range(9):
    #     phone.append(str(random.randint(0,9)))
    # return ''.join(phone)

    phone = ['158']
    for i in range(8):
        phone.append(random.choice('0123456789'))
    return ''.join(phone)

def generate_no_use_phone(sql='select id from member where mobile_phone={}'):
    """
    生成一个没有注册的手机号码
    :param sql:
    :return:
    """
    for i in range(10):
        phone = generate_phone()
        sql = sql.format(phone)
        if not db.exist(sql):
            return phone
    else:
        raise ValueError('数据已存在')


def replace_args_by_re(json_str, obj):
    """
    通过正则表达式动态的替换参数
    :param json_str: 需要被替换的json字符串
    :param obj: 提供数据的对象
    :return: 替换后的字符串
    """
    # 先找出字符串中的槽位名
    args = re.findall('#(.*?)#', json_str)
    # 再去数据对象中获取对应名字的参数的值
    for arg in args:
        # 获取obj中对应参数名的属性值
        value = getattr(obj, arg, None)
        # 如果有属性替换
        if value is not None:
            json_str = json_str.replace('#{}#'.format(arg), str(value))
    return json_str


if __name__ == '__main__':

     print(generate_phone())
     print(generate_no_use_phone())
    # res = get_data_from_excel('../testdata/data.xlsx')
    # print(res)