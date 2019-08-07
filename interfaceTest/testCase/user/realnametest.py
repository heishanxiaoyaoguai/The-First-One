import unittest
import paramunittest
import readConfig as readConfig
from common import common
from common import configHttp
from common.Log import MyLog
from common import businessCommon

localReadConfig = readConfig.ReadConfig()
configHttp = configHttp.ConfigHttp()
localLogin_xls = common.get_xls("userCase.xlsx", "login")
localrealname_xls = common.get_xls("userCase.xlsx", "realname")

@paramunittest.parametrized(*localrealname_xls)
class Realname(unittest.TestCase):

    def setParameters(self, case_name, method, token, realname, idcard, code, message, incorrect):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param realname:
        :param idcard:
        :param code:
        :param message:
        :param incorrect:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.realname = str(realname)
        self.idcard = str(idcard)
        self.code = str(code)
        self.msg = str(message)
        self.incorrect = str(incorrect)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")

    def testrealname(self):
        """
        test body
        :return:
        """
        # set url
        # self.url = "/api/front/real-name-test"
        self.url = common.get_url_from_xml('realname')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)

        # get visitor token

        if self.token == '1':
            token = None

        else:
            token = localReadConfig.get_headers("Authorization")
        # header = {'Authorization': "Bearer " + str(token)}
        # configHttp.set_headers(header)
        token1 = "Bearer" + str(token)
        print("当前token**：" + token1)
        # set headers

        header = {"Content-Type": "application/json", "Authorization": str(token1)}
        configHttp.set_headers(header)
        print("第二步：设置header(token等)")

        # set params
        data = {"realname": self.realname, "idcard": self.idcard}
        configHttp.set_data(data)
        print("第三步：设置发送请求的参数")

        # test interface
        self.return_json = configHttp.postWithJson()
        print(self.return_json)  # 返回<Response [200]>
        print(self.return_json.request)  # <PreparedRequest [POST]>
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查结果")

    def tearDown(self):
        """

        :return:
        """
        # businessCommon.logout(self.login_token)
        self.log.build_case_line(self.case_name, self.info['code'], self.info['message'])
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        print(self.info)
        info1 = self.info
        info2 = info1['data']
        info3 = info2['data']
        print(info3)
        # print(self.info)  # {'code': 0, 'message': 'success', 'data': {'resultcode': '101'}}
        # show return message
        common.show_return_msg(self.return_json)
        if info3['incorrect'] == '100':
            # email = common.get_value_from_return_json(self.info, 'member', 'email')
            self.assertEqual(str(self.info['code']), self.code)
            self.assertEqual(str(info3['message']), self.msg)
            # self.assertEqual(email, self.email)

        if info3['incorrect'] != '100':
            self.assertEqual(str(self.info['code']), self.code)
            self.assertEqual(str(info3['message']), self.msg)
