import pytest
import time
import os
from base.Allure_Report import allure_generate
from conf import Conf
import concurrent.futures
from base.SendEmail import send_mail


# 1、ProcessPoolExecutor并发，方法实现
def run_pytest(device):
    report_path = Conf.report_path + os.sep + "result" + os.sep + device["name"]
    report_html = Conf.report_path + os.sep + "html" + os.sep + device["name"]
    pytest.main([f"--cmdopt={device}","--alluredir",report_path])  # 加f表示{cmdopt}是个参数
    # time.sleep(2)
    allure_generate(report_path, report_html)
    time.sleep(3)
    send_mail(content="测试完成，请查看测试报告")

# 3、ProcessPoolExecutor并发，pool并发
def run_pool(devices):
    with concurrent.futures.ProcessPoolExecutor(len(devices)) as executor:
        executor.map(run_pytest,devices)

if __name__ == '__main__':

    # 2、ProcessPoolExecutor并发，定义参数列表
    devices_list = list()
    devices_1 = {"host": "127.0.0.1",
              "port": "4723",
              "bpport": "4724",
              "udid": "WQVNW18305004438",
                 "systemPort":8200,
                 "name":"华为真机FLA-AL10"}

    # 如果adb devices看不到mumu模拟器，输入adb connect 127.0.0.1:7555就可以直接连上mumu模拟器
    devices_2 = {"host": "127.0.0.1",
              "port": "4725",
              "bpport": "4726",
              "udid": "127.0.0.1:5555",
                 "systemPort":8201,
                 "name":"网易MuMu模拟器"}
    devices_list.append(devices_1)
    devices_list.append(devices_2)
    run_pool(devices_list)
