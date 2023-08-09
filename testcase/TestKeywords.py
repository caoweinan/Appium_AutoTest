import pytest
from base.ExcelData import Data
from utils.LogUtil import my_log
from conf import Conf
from testcase.operate.KeywordOperatePytest import Operate
from base.DesireCaps import appium_desired_caps


log = my_log("TestKeywords")
data = Data(Conf.testcase_file)
# 执行测试用例的列表
run_list = data.run_list()

# 1、创建一个测试用例方法
# 2、根据这个方法重构代码
# 3、增加一个运行，类似setup、teardown、set_class、teardown_class
class TestKeyword:

    # def setup_class(self):
    #     self.driver = appium_desired_caps()
    #
    # def setup(self):
    #     self.driver.launch_app()

    @pytest.mark.parametrize("run_case",run_list)
    def test_run(self,start_appium_desired,run_case):
        self.driver = start_appium_desired
        self.driver.launch_app()
        log.info("执行用例内容：{}".format(run_case))
        Operate(self.driver).step(data,run_case)

    def teardown(self):
        self.driver.close_app()

    # def teardown_class(self):
    #     self.driver.quit()

