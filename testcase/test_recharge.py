from unittestreport import ddt, list_data
from common.data_handler import (
    get_data_from_excel,
    generate_no_use_phone,
)
from common.fixture import register,login

from common.base_case import BaseCase
cases = get_data_from_excel(BaseCase.setting.TEST_DATA_FILE,sheet_name='recharge')


@ddt
class TestRecharge(BaseCase):
    name = '充值'
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.logger.info('注册用户并登录用户')
        # 注册一个用户
        mobile_phone = generate_no_use_phone()
        pwd = '12345678'
        register(mobile_phone,pwd)
        # 登录
        data = login(mobile_phone,pwd)
        # 保存需要传递到测试函数中的数据到类属性
        # 依赖 member_id
        cls.member_id = str(data['id'])
        # 依赖token
        cls.token = data['token_info']['token']

    @list_data(cases)
    def test_recharge(self,item):
        self.flow(item)