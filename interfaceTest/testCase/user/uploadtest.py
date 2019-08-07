#-*- coding: UTF-8 -*-
import unittest
import paramunittest
import readConfig as readConfig
from common import common
from common import configHttp
from common.Log import MyLog
from common import businessCommon

localReadConfig = readConfig.ReadConfig()
configHttp = configHttp.ConfigHttp()
localrealface_xls = common.get_xls("userCase.xlsx", "realface")

@paramunittest.parametrized(*localrealface_xls)
class Realphone(unittest.TestCase):

    def setParameters(self, case_name, method, token, realname, idcard, photo, code, message, incorrect):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param realname:
        :param idcard:
        :param code:
        :param photo:
        :param message:
        :param incorrect:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.realname = str(realname)
        self.idcard = str(idcard)
        self.photo = str(photo)
        self.code = str(code)
        self.msg = str(message)
        self.incorrect = str(incorrect)
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
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        # self.login_token = businessCommon.login()
        print("测试开始前准备")

    def testupload(self):
        """
        test body
        :return:
        """
        # set url
        # self.url = "/api/front/real-name-test"
        self.url = common.get_url_from_xml('upload')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)
        # get visitor token

        if self.token == '0':
            token = localReadConfig.get_headers("Authorization")

        else:
            token = None
        print("第二步：设置header(token等)")

        # set file
        print("%%%%" + self.photo)
        configHttp.set_files(self.photo)

        print("第三步：设置发送请求的参数")
        # test interface
        self.return_json = configHttp.postOnlyFile()
        print(self.return_json)  # 返回<Response [200]>
        print(self.return_json.text)  # <PreparedRequest [POST]>
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        print("第五步：检查结果")

    def tearDown(self):
        """

        :return:
        """
        # businessCommon.logout(self.login_token)
        # self.log.build_case_line(self.case_name, self.info['code'], self.info['message'])
        print("测试结束，输出log完结\n\n")

