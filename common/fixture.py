import setting
from common.make_requests import send_http_request
from common import logger


def register(mobile_phone,pwd,reg_name=None,_type=None):
    """
    注册用户
    :param mobile_phone:
    :param pwd:
    :param reg_name:
    :param _type:
    :return:
    """
    # 构造发送注册请求的参数
    data = {
        'mobile_phone': mobile_phone,
        'pwd': pwd
    }
    if reg_name:
        data['reg_name'] = reg_name
    if _type is not None:
        data['type'] = _type

    # 构造请求头
    headers = {"X-Lemonban-Media-Type": "lemonban.v1"}
    url = setting.INTERRACES['register']
    # 发送请求
    try:
        res = send_http_request(url,'post',json=data,headers=headers)
        if res.status_code == 200:
            if res.json()['code'] ==0:
                return True
        raise ValueError(res.text)
    except Exception as e:
        logger.warning('用户注册失败')
        raise e


def login(mobile_phone,pwd):
    """
    登录用户
    :param mobile_phone:
    :param pwd:

    :return:
    """
    # 构造发送注册请求的参数
    data = {
        'mobile_phone': mobile_phone,
        'pwd': pwd
    }

    # 构造请求头
    headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
    url = setting.INTERRACES['login']
    # 发送请求
    try:
        res = send_http_request(url,'post',json=data,headers=headers)
        if res.status_code == 200:
            if res.json()['code'] ==0:
                return res.json()['data']
        raise ValueError(res.text)
    except Exception as e:
        logger.warning('用户登录失败')
        raise e


def add_loan(member_id, token, title='借钱实现财富自由',amount=50000,
             loan_rate=12, loan_term=10, loan_date_type=2, bidding_days=5):
    """
    添加一个项目
    :param member_id:
    :param token:
    :param title:
    :param amount:
    :param loan_rate:
    :param loan_term:
    :param loan_date_type:
    :param bidding_days:
    :return:
    """
    # 构造数据
    data = {
        'member_id':member_id,
        'title':title,
        'amount':amount,
        'loan_rate':loan_rate,
        'loan_term':loan_term,
        'loan_date_type':loan_date_type,
        'bidding_days':bidding_days
    }
    # 构造请求头
    headers = {"X-Lemonban-Media-Type": "lemonban.v2","Authorization": "Bearer {}".format(token)}
    url = setting.INTERRACES['add']
    # 发送请求
    try:
        res = send_http_request(url, 'post', json=data, headers=headers)
        if res.status_code == 200:
            if res.json()['code'] == 0:
                return res.json()['data']
        raise ValueError(res.text)
    except Exception as e:
        logger.warning('创建项目失败')
        raise e


if __name__ == '__main__':
    from common.data_handler import generate_no_use_phone
    phone = generate_no_use_phone()
    res = register(phone,'12345678')
    if res:
        token = login(phone,'12345678')
    print(token)

    lo = login(15870961865,'12345678')
    print(lo)

    a = add_loan('34213082', 'eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjM0MjEzMDgyLCJleHAiOjE2NDYwNjE3MTB9.OZ2as1FXoMPtATZ-mZNMEoBBFGAqxOEWb_lFeR-gLe6yyl5hXrgmOTDlCQYQV3a7Vnc3V5rvrve82XSx9OQhlw')
    print(a)
