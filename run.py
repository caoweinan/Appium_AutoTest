import pytest
import time
import os
from base.Allure_Report import allure_generate
from conf import Conf
from base.SendEmail import send_mail


report_path = Conf.report_path + os.sep + "result"
report_html= Conf.report_path + os.sep + "html"


if __name__ == '__main__':
    # pytest.main()
    # time.sleep(2)
    # allure_generate(report_path,report_html)
    # time.sleep(3)
    # send_mail(content="测试完成，请查看测试报告")

    # 自定义参数
    # 启动appium需要信息，--cmdopt字典
    cmdopt = {"host": "127.0.0.1",
              "port": "4723",
              "bpport": "4724",
              "udid": "WQVNW18305004438",
              "systemPort":8200}
    pytest.main([f"--cmdopt={cmdopt}"])     #加f表示{cmdopt}是个参数
    time.sleep(2)
    allure_generate(report_path, report_html)
    # time.sleep(3)
    # send_mail(content="测试完成，请查看测试报告")

