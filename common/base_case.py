from unittest import TestCase
import json
import setting
from common.make_requests import send_http_request
from common import db,logger
from common.data_handler import (
    replace_args_by_re,
    generate_no_use_phone
)


class BaseCase(TestCase):
    """
    用例基类
    """
    db = db
    logger = logger
    setting = setting

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info("-------------{}项目审核接口开始测试-------------".format(cls.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.logger.info("-------------{}接口结束测试-------------".format(cls.name))

    def flow(self,item):
        """
        执行流程
        :param item:
        :return:
        """
        # 把测试数据绑定到 _case上
        self._case = item
        self.process_test_data()
        self.send_request()
        self.assert_all()

    def process_test_data(self):
        """
        测试数据的处理
        :return:
        """
        self.generate_test_data()
        self.replace_args()
        self.process_url()

    def replace_args(self):
        """
        替换参数
        :return:
        """
        # 替换依赖参数
        self._case = json.dumps(self._case)
        # item = item.replace('#loan_id#', str(self.loan_id))
        # item = item.replace('#token#', self.__class__.token)
        self._case = replace_args_by_re(self._case, self)
        self._case = json.loads(self._case)
        try:
            self._case['request_data'] = json.loads(self._case['request_data'])
            self._case['expect_data'] = json.loads(self._case['expect_data'])
        except Exception as e:
            self.logger.error('{}用例的测试数据格式不正确'.format(self._case['title']))
            raise e

    def process_url(self):
        """
        处理url
        :return:
        """
        if self._case['url'].startswith('http'):
            # 是否是全地址
            pass
        elif self._case['url'].startswith('/'):
            # 是否是短地址
            self._case['url'] = self.setting.PROJECT_HOST + self._case['url']
        else:
            # 接口名称
            try:
                self._case['url'] = self.setting.INTERRACES[self._case['url']]
            except Exception as e:
                self.logger.error('接口名称：{}不存在'.format(self._case['url']))

    def generate_test_data(self):
       """
       生成测试数据，不是固定流程，有不同可以复写
       :return:
       """
       self._case = json.dumps(self._case)
       if '$phone_number$' in self._case:
           phone = generate_no_use_phone()
           self._case = self._case.replace('$phone_number$', phone)
       self._case = json.loads(self._case)


    def send_request(self):
        # 发送请求
        self._response = send_http_request(url=self._case['url'],
                                          method=self._case['method'],
                                          **self._case['request_data'])

    def assert_all(self):
        """
        断言
        :return:
        """
        try:
            self.assert_status_code()
            self.assert_response()
            self.assert_sql()
        except AssertionError as e:
            self.logger.error('<<<<<<<<<<用例{}测试失败<<<<<<<<'.format(self._case['title']))
            raise e
        else:
            self.logger.info('用例{}数据库响应数据断言成功'.format(self._case['title']))



    def assert_status_code(self):
        """
        断言响应状态码
        :return:
        """
        try:
            self.assertEqual(self._case['status_code'], self._response.status_code)
        except AssertionError as e:
            self.logger.warning('用例{}响应状态码断言异常'.format(self._case['title']))
            raise e
        else:
            self.logger.info('用例{}响应状态码断言成功'.format(self._case['title']))

    def assert_response(self):
        """
        断言响应数据
        :return:
        """
        if self._case['res_type'].lower() == 'json':
            res = self._response.json()
        elif self._case['res_type'].lower() == 'html':
            res = self._response.text
        try:
            self.assertEqual(self._case['expect_data'], {'code': res['code'], 'msg': res['msg']})
        except AssertionError as e:
            self.logger.warning('用例{}响应数据断言异常'.format(self._case['title']))
            self.logger.warning('用例{}期望结果为:{}'.format(self._case['title'], self._case['expect_data']))
            self.logger.warning('用例{}响应结果为:{}'.format(self._case['title'], res))
        else:
            self.logger.info('用例{}响应数据断言成功'.format(self._case['title']))

    def assert_sql(self):
        """
        断言数据库
        :return:
        """
        if self._case.get('sql'):
            try:
                self.assertTrue(self.db.exist(self._case['sql']))
            except Exception as e:
                self.logger.warning('用例{}数据库断言异常,执行的sql为{}'.format(self._case['title'], self._case['sql']))
                raise e
