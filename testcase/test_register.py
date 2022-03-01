import unittest
import json
from unittestreport import ddt, list_data

import setting
from common.data_handler import get_data_from_excel,generate_no_use_phone
from common.make_requests import send_http_request
from common import logger,db

# 读取测试用例数据
cases = get_data_from_excel(setting.TEST_DATA_FILE,sheet_name='register')


@ddt
class RegisterTestcase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info("-------------注册接口开始测试-------------")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("-------------注册接口结束测试-------------")

    @list_data(cases)
    def test_register(self, item):
        logger.info(">>>>>>>>>用例{}>>>>>>>".format(item['title']))
        # 是否有动态生成手机号码
        item = json.dumps(item)
        if '$phone_number$' in item:
            phone = generate_no_use_phone()
            item = item.replace('$phone_number$',phone)
        item = json.loads(item)
        # request_data、expect_data是json字符串，需要转换为python对象
        request_data = json.loads(item['request_data'])
        expect_data = json.loads(item['expect_data'])
        # 处理url
        if item['url'].startswith('http'):
            pass
        elif item['url'].startswith('/'):
            item['url'] = setting.PROJECT_HOST + item['url']
        else:
            item['url'] = setting.INTERRACES[item['url']]
        # 发送请求
        response = send_http_request(url=item['url'], method=item['method'], **request_data)
        # 断言响应状态码
        try:
            self.assertEqual(item['status_code'], response.status_code)
        except AssertionError as e:
            logger.warning('用例{}响应状态码断言异常'.format(item['title']))
            raise e
        else:
            logger.info('用例{}响应状态码断言成功'.format(item['title']))
        # 断言响应数据
        if item['res_type'].lower() == 'json':
            res = response.json()
        elif item['res_type'].lower() == 'html':
            res = response.text
        try:
            self.assertEqual(expect_data, {'code': res['code'], 'msg': res['msg']})
        except AssertionError as e:
            logger.warning('用例{}响应数据断言异常'.format(item['title']))
            logger.warning('用例{}期望结果为:{}'.format(item['title'], expect_data))
            logger.warning('用例{}响应结果为:{}'.format(item['title'], res))
        else:
            logger.info('用例{}响应数据断言成功'.format(item['title']))

        # 数据库断言
        if item.get('sql'):
            try:
                self.assertTrue(db.exist(item['sql']))
            except Exception as e:
                logger.warning('用例{}数据库断言异常,执行的sql为{}'.format(item['title'],item['sql']))
                raise e
        logger.info('用例{}数据库响应数据断言成功'.format(item['title']))


