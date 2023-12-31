import pytest
from base.DesireCaps import appium_desired_caps
from base.StartAppium import get_devices, appium_start, check_port
import time


# 定义命令选项
def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default="run", help=None)


# 接收命令
@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--cmdopt")

"""
本地运行
"""
# 调用命令使用
@pytest.fixture(scope="session")
def start_appium_desired(cmdopt):
    opt = eval(cmdopt)
    # {'host': '127.0.0.1', 'port': '4723', 'bpport': '4724', 'udid': None}
    host = opt["host"]
    port = opt["port"]
    bpport = opt["bpport"]
    udid = opt["udid"]
    systemPort = opt["systemPort"]
    # print(opt)
    driver = None
    if udid in get_devices():
        appium_start(host, port, bpport, udid)
        time.sleep(5)
        if not check_port():
            driver = appium_desired_caps(host, port,systemPort)
    # return driver
    yield driver
    driver.quit()


"""
Jenkins运行start_appium_desired
"""
# 调用命令使用
# @pytest.fixture(scope="session")
# def start_appium_desired(cmdopt):
#     opt = eval(cmdopt)
#     # {'host': '127.0.0.1', 'port': '4723', 'bpport': '4724', 'udid': None}
#     host = opt["host"]
#     port = opt["port"]
#     bpport = opt["bpport"]
#     udid = opt["udid"]
#     systemPort = opt["systemPort"]
#     # print(opt)
#     driver = None
#     # if udid in get_devices():
#     #     appium_start(host, port, bpport, udid)
#     #     time.sleep(5)
#     #     if not check_port():
#     #         driver = appium_desired_caps(host, port,systemPort)
#     if not check_port(host,port):
#         driver = appium_desired_caps(host, port,systemPort)
#     # return driver
#     yield driver
#     driver.quit()