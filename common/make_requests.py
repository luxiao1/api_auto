import requests


# def send_http_request(url,method='GET',**kwargs):
#     """
#     发送http请求
#     :param url: 接口url
#     :param method: http请求方法
#     :param kwargs: requests原生请求的关键字参数
#     :return:
#     """
#     method = method.lower()
#     if method == 'get':
#         res = requests.get(url,**kwargs)
#     elif method == 'post':
#         res = requests.post(url, **kwargs)
#     elif method == 'put':
#         res = requests.put(url, **kwargs)
#     elif method == 'delete':
#         res = requests.delete(url, **kwargs)
#     else:
#         raise ValueError('请输入正确的请求方法')
#     return res

def send_http_request(url,method='GET',**kwargs):
    """
    发送http请求
    :param url: 接口url
    :param method: http请求方法
    :param kwargs: requests原生请求的关键字参数
    :return:
    """
    method = method.lower()
    #return getattr(requests,method)(url,**kwargs)
    return requests.request(method,url,**kwargs)

if __name__ == '__main__':
    url = 'http://api.lemonban.com/futureloan/member/register'
    method = 'post'
    data = {
        "headers":{"X-Lemonban-Media-Type":"lemonban.v1"},
        "json":{"mobile_phone": 17634728220,
        "pwd": 12345678,
        "reg_name": "最帅的心蓝",
        "type": 1}
    }

    r = send_http_request(url,method,**data)
    print(r.json())

