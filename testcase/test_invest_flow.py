from common.base_case import BaseCase


class TestInvestFlow(BaseCase):
    name = '投资业务流程'

    def test_01register_normal_user(self):
        """
        1.注册普通融资用户
        :return:
        """
        item = {
                'title':'注册融资用户',
                'url':'register',
                'method':'post',
                'request_data':'{"headers": {"X-Lemonban-Media-Type": "lemonban.v1"},"json": {"mobile_phone":$phone_number$,"pwd": 12345678}}',
                'status_code':200,
                'res_type':'json',
                'expect_data':'{"code": 0,"msg": "OK"}',
                'sql':'select id from member where mobile_phone=$phone_number$'
        }
        self.flow(item)
        # 绑定下一个测试需要的数据，在响应中拿到数据,并绑定到类属性 normal_mobile_phone 中
        self.__class__.normal_mobile_phone = self._response.json()['data']['mobile_phone']

    def test_02login_normal_user(self):
        """
        2.登录普通的融资用户
        :return:
        """
        item = {'title':'登录融资用户',
                'url':'login',
                'method':'post',
                'request_data':'{"headers": {"X-Lemonban-Media-Type": "lemonban.v2"},"json": {"mobile_phone":#normal_mobile_phone#,"pwd": 12345678}}',
                'status_code':200,
                'res_type':'json',
                'expect_data':'{"code": 0,"msg": "OK"}'
               }
        self.flow(item)
        # 在响应中提取下一个接口需要的数据然后绑定到属性上
        self.__class__normal_token = self._response.json()['data']['token_info']['token']
        self.__class__normal_member_id = self._response.json()['data']['id']

    def test_03_loan(self):
        """
        3.创建融资项目
        :return:
        """
        item = {'title': '创建融资项目',
                'url': 'add',
                'method': 'post',
                'request_data': '''{"headers": {"X-Lemonban-Media-Type": "lemonban.v2","Authorization":"Bearer #normal_token#"},
                                    "json": {"member_id":#normal_member_id#,
                                    "title": "借钱实现财富自由",
                                    "amount":5000,
                                    "loan_rate":18.0,
                                    "loan_term":6,
                                    "loan_date_type":1,
                                    "bidding_days":10
                                    }}''',
                'status_code': 200,
                'res_type': 'json',
                'expect_data': '{"code": 0,"msg": "OK"}'
                }
        self.flow(item)

    def test_04register_admin_user(self):
        """
        4.创建管理员用户
        :return:
        """
        item = {}
        self.flow(item)
        # 绑定下一个测试需要的数据

    def test_05login_admin_user(self):
        """
        5.登录管理员用户
        :return:
        """
        item = {}
        self.flow(item)

    def test_06audit_loan(self):
        """
        6.审核融资项目
        :return:
        """
        item = {}
        self.flow(item)

    def test_07register_invest_user(self):
        """
        7.注册普通投资用户
        :return:
        """
        item = {}
        self.flow(item)

    def tets_08login_invest_user(self):
        """
        8.登录普通投资用户
        :return:
        """
        item = {}
        self.flow(item)

    def tets_09invest_user(self):
        """
        9.普通投资用户充值
        :return:
        """
        item = {}
        self.flow(item)

    def test_09invest(self):
        """
        10.投资
        :return:
        """
        item = {}
        self.flow(item)
