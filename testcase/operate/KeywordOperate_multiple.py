import unittest
import ddt
import os
from base.ExcelData import Data
from data.ExcelConfig import TestSteps,Elements,CaseData
from base.BaseAction import Action      # Action有个初始化参数driver，需要setup或者setupclass
from base.DesireCaps import appium_desired_caps
from utils.LogUtil import my_log
from conf import Conf
from utils.YamlUtil import YamlReader
from utils.HTMLTestRunner3 import HTMLTestRunner


# 多个用例的编写及运行
"""
多个用例参数化可以使用ddt方式，支持file_data,data的方法
data方法支持，元组、列表、字典，拆分参数使用unpack方式
1、删除无用的代码
2、获取测试用例的列表ExcelData.py，之前是[[{}],[{}]]这种类型，但ddt方式不支持这种多层嵌套，需要列表转换成[{},{}]这种类型，就要修改ExcelData.py里run_list方法
3、增加新的用例test_run进行参数化运行，调用单条步骤执行方法不做修改
4、编写ddt相关代码，ddt.ddt再使用ddt.data，不是使用unpack方式
5、增加输出测试报告
6、运行及调试
"""


log = my_log("operate")
data = Data(Conf.testcase_file)
# 执行测试用例的列表
run_list = data.run_list()

@ddt.ddt
class Operate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = appium_desired_caps()
        # pass
    def setUp(self):
        self.driver.launch_app()

# 4、调试运行
    def get_keyword(self,name):
        # 读取配置文件，文件路径：绝对路径
        keywords_file = Conf.keywords_path
        # 使用YamlReader的data()方法读取文件，是字典格式
        reader = YamlReader(keywords_file).data()
        # 根据字典的key(name)获取值
        value = reader[name]
        return value

    # 字符串转换为字典方法
    def str_to_dict(self,content):
        # 字符串转换成字典
        # 通过,分割得到username=13718418220   password=123456
        res = {}  # 首先定义一个字典
        # 通过=分割
        for i in str(content).split(","):
            c = i.split("=")
            res[c[0]] = c[1]
        return res

    @ddt.data(*run_list)
    def test_run(self,run_case):    # 定义这个参数用于获取用例字典内容
        log.info("执行用例内容：{}".format(run_case))
        self.step(run_case)

    def step(self,run_case):
        tc_id = run_case[TestSteps.STEP_TC_ID]
        # 获取步骤
        steps = data.get_steps_by_tc_id(tc_id)
        for step in steps:
            log.debug("执行步骤{}".format(step))
            # 获取元素信息
            elements = step[TestSteps.STEP_ELEMENT_NAME]
            element = data.get_elements_by_element(step[TestSteps.STEP_TC_ID], elements)
            log.debug("元素信息{}".format(element))
            # 操作步骤 click_btn、send_keys、is_toast_exist
            operate = self.get_keyword(step[TestSteps.STEP_OPERATE])

            # 判断操作，是否存在，存在运行，不存在不执行步骤
            if operate:
                # 定义方法参数：字典by、value、send、expect(期望结果)
                param_value = dict()

                # 根据getattr判断去执行哪个方法
                action_method = getattr(Action(self.driver),operate)
                log.debug("该关键字是{}".format(operate))

                # 定义具体参数by、value、send、expect
                by = element[Elements.ELE_BY]
                value = element[Elements.ELE_VALUE]
                # 获取by,value,send_value内容
                send_value = step[TestSteps.STEP_DATA]
                expect = run_case[CaseData.DATA_EXPECT_RESULT]
                # 把by、value、send、expect放到字典里
                param_value["by"] = by
                param_value["value"] = value
                param_value["expect"] = expect

                # 假如有输入内容，需要做字符转换
                if send_value:
                    # send_value内容转换，通过case data 获取数据内容，是字符串类型
                    data_input = run_case[CaseData.DATA_INPUT]  # 数据内容是字符串型
                    send = self.str_to_dict(data_input)  # 返回的是一个字典
                    param_value["send"] = send[send_value]  # 返回的是一个字典，它的值就是send_value

                action_method(**param_value)
            else:
                log.error("没有operate信息：{}".format(operate))

    def tearDown(self):
        self.driver.close_app()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Operate)
    report = Conf.report_path + os.sep + "测试报告.html"
    with open(report,"wb+") as report:
        runner = HTMLTestRunner(stream=report,
                                verbosity=2,
                                title="移动端自动化测试报告",
                                description="关键字驱动测试"
                                )
        runner.run(suite)
