from unittestreport import ddt, list_data

from common.data_handler import get_data_from_excel

from common.base_case import BaseCase

# 读取测试用例数据
cases = get_data_from_excel(BaseCase.setting.TEST_DATA_FILE,sheet_name='register')


@ddt
class RegisterTestcase(BaseCase):
    name = '注册'

    @list_data(cases)
    def test_register(self, item):
        self.flow(item)



