import json
from unittest import TestCase

from unittestreport import ddt,list_data

import setting
from common import logger, db
from common.data_handler import (
    get_data_from_excel,
    generate_no_use_phone,
    replace_args_by_re)
from common.fixture import register,login,add_loan
from common.make_requests import send_http_request

cases = get_data_from_excel(setting.TEST_DATA_FILE, 'audit')


@ddt
class TestAudit(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info("-------------项目审核口开始测试-------------")
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

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("-------------项目审核接口结束测试-------------")

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
        # 替换依赖参数
        item = json.dumps(item)

        # item = item.replace('#loan_id#', str(self.loan_id))
        # item = item.replace('#token#', self.__class__.token)
        item = replace_args_by_re(item, self)
        item = json.loads(item)

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
                    logger.warning('用例{}数据库断言异常,执行的sql为{}'.format(item['title'], item['sql']))
                    raise e
            logger.info('用例{}数据库响应数据断言成功'.format(item['title']))