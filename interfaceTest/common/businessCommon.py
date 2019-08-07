#-*- coding: UTF-8 -*-

from common import common
from common import configHttp
import readConfig as readConfig

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = common.get_xls("userCase.xlsx", "login")
localrealname_xls = common.get_xls("userCase.xlsx", "realname")
localAddAddress_xls = common.get_xls("userCase.xlsx", "addAddress")
localrealface_xls = common.get_xls("userCase.xlsx", "realface")

# 单独从某个接口中获取token
# login
def login():
    """
    login
    :return: token
    """
    # set url
    url = common.get_url_from_xml('login')
    localConfigHttp.set_url(url)

    # set header
    """
    token = localReadConfig.get_headers("Authorization")
    header = {"Authorization": token}
    localConfigHttp.set_headers(header)
    """
    header = {"Content-Type": "application/json"}
    localConfigHttp.set_headers(header)
    # set param
    data = {"username": localLogin_xls[0][3],
            "password": localLogin_xls[0][4]}
    localConfigHttp.set_data(data)

    # login
    response = localConfigHttp.postWithJson().json()
    token = common.get_value_from_return_json(response, "data", "token")
    return token

def upload(length):
    """
    login
    :return: token
    """
    # set url
    url = common.get_url_from_xml('upload')
    print(url)
    localConfigHttp.set_url(url)
    localConfigHttp.set_files(localrealface_xls[length][5])
    print("------" + localrealface_xls[length][5])
    response = localConfigHttp.postOnlyFile()
    photoId = response.text
    return photoId


# logout
def logout(token):
    """
    logout
    :param token: login token
    :return:
    """
    # set url
    url = common.get_url_from_xml('logout')
    localConfigHttp.set_url(url)

    # set header
    header = {'token': token}
    localConfigHttp.set_headers(header)

    # logout
    localConfigHttp.get()


