# encoding=utf-8
from utils.YamlUtil import YamlReader
from conf import Conf
from appium import webdriver


# 通过yaml读取caps.yml
reader = YamlReader(Conf.conf_caps)
data = reader.data()
# 结果，字典转换


def appium_desired_caps(host,port,systemPort="8200"):
    # 创建desired字典
    desired_caps = dict()
    # platformName
    desired_caps['platformName'] = data['platformName']
    # platformVersion
    desired_caps['platformVersion'] = data['platformVersion']
    # deviceName
    desired_caps['deviceName'] = data['deviceName']
    # 包名
    desired_caps['appPackage'] = data['appPackage']
    # 界面名
    desired_caps['appActivity'] = data['appActivity']
    # 解决中文
    desired_caps['unicodeKeyboard'] = data['unicodeKeyboard']
    desired_caps['resetKeyboard'] = data['resetKeyboard']
    # 获取toast
    desired_caps['automationName'] = data['automationName']
    # 不清除app里的原有数据
    # desired_caps["noReset"] = data["noReset"]
    # 解决并发测试
    desired_caps["systemPort"] = systemPort
    # 连接appium服务器
    driver = webdriver.Remote('http://%s:%s/wd/hub'%(host,port), desired_caps)
    driver.implicitly_wait(20)
    return driver
