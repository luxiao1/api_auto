import json

from unittestreport import ddt,list_data

from common.data_handler import (
    get_data_from_excel,
    generate_no_use_phone,)
from common.fixture import register,login,add_loan

from common.base_case import BaseCase

cases = get_data_from_excel(BaseCase.setting.TEST_DATA_FILE, 'audit')




@ddt
class TestAudit(BaseCase):
    name = '项目审核'
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        # 1.注册借钱用户
        mobile_phone = generate_no_use_phone()
        pwd = '12345678'
        register(mobile_phone, pwd)
        # 2.登录借钱用户
        data = login(mobile_phone, pwd)
        # 保存投资用户的数据用来创建标
        # 要保存借钱用户的id和token
        cls.normal_member_id = data['id']
        cls.normal_token = data['token_info']['token']
        # 3.注册管理员用户
        mobile_phone = generate_no_use_phone()
        register(mobile_phone, pwd, _type=0)
        # 4.登录管理员用户
        data = login(mobile_phone, pwd)
        # 保存管理员用户的token
        cls.token = data['token_info']['token']



    def setUp(self) -> None:
        """

        :return:
        """
        # 创建项目
        res = add_loan(member_id=self.__class__.normal_member_id,
                       token=self.__class__.normal_token)

        # 将创建好的项目id传递到测试用例中
        # 通过对象属性
        self.loan_id = res['id']

    @list_data(cases)
    def test_audit(self,item):
        """
        审核项目
        :param item:
        :return:
        """
        self.flow(item)



