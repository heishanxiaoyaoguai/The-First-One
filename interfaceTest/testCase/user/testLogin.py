import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp

login_xls = common.get_xls("userCase.xlsx", "login")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, token, username, password, resultcode, code, message):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param username:
        :param password:
        :param resultcode:
        :param code:
        :param message:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.username = str(username)
        self.password = str(password)
        self.resultcode = str(resultcode)
        self.code = str(code)
        self.msg = str(message)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        # self.url = "/api/login/name"
        self.url = common.get_url_from_xml('login')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)

        # get visitor token

        if self.token == '0':
            self.token = localReadConfig.get_headers("token_v")
        elif self.token == '1':
            self.token = None

        # set headers
        header = {"Content-Type": "application/json"}
        configHttp.set_headers(header)
        print("第二步：设置header(token等)")

        # set params
        data = {"username": self.username, "password": self.password}
        configHttp.set_data(data)
        print("第三步：设置发送请求的参数")

        # test interface
        self.return_json = configHttp.postWithJson()
        print(self.return_json)  # 返回<Response [200]>
        print(self.return_json.request)  # <PreparedRequest [POST]>
        method = str(self.return_json.request)[int(str(self.return_json.request).find
                                                   ('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查结果")

    def tearDown(self):
        """

        :return:
        """
        global token1
        info = self.info
        # print(info)  # {'code': 0, 'message': 'success', 'data': {'resultcode': '101'}}
        info1 = info['data']
        print(info1)
        if 'resultcode' in info1 and info1['resultcode'] == '100':
            # get uer token
            token_u = common.get_value_from_return_json(info, 'data', 'token')
            # set user token to config file
            localReadConfig.set_headers("Authorization", token_u)  # 往config.ini 插入一条数据，用来方便其他用例读取
            print(token_u)
        else:
            pass
        # print(self.case_name)
        # print(self.info['code'])
        # print(self.info['message'])
        token1 = localReadConfig.get_headers("Authorization")  # 往config.ini 读取对应的数据
        print("当前token1：" + token1)
        self.log.build_case_line(self.case_name, self.info['code'], self.info['message'])
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # print(self.info)  # {'code': 0, 'message': 'success', 'data': {'resultcode': '101'}}
        # show return message
        common.show_return_msg(self.return_json)
        if self.resultcode == '100':
            # email = common.get_value_from_return_json(self.info, 'member', 'email')
            self.assertEqual(str(self.info['code']), self.code)
            self.assertEqual(self.info['message'], self.msg)
            # self.assertEqual(email, self.email)

        if self.resultcode != '100':
            self.assertEqual(str(self.info['code']), self.code)
            self.assertEqual(self.info['message'], self.msg)

