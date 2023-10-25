from utils.LogUtil import my_log
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import allure
import datetime


# 定义类
class Action:
    def __init__(self,driver):
        self.driver = driver
        self.log = my_log("Base_Page")

# 定义方法
    # 定义元素定位方法：id,xpath
    # 定义元素等待方法
    # 定义点击click方法
    # 定义send_keys方法
    # 定义toast方法

    # 元素定位：id,xpath
    def by_xpath(self,value):
        """
        xpath 元素定位
        :param value:
        :return:
        """
        return self.by_find_element(By.XPATH,value)
    def by_id(self,value):
        """
        id 元素定位
        :param value:
        :return:
        """
        return self.by_find_element(By.ID,value)

    # # send_keys
    # def send_keys(self,by,value,send_value):
    #     """
    #     发送内容
    #     :param by:
    #     :param value:
    #     :param send_value:
    #     :return:
    #     """
    #     # 加个判断：根据by类型，进行by_id还是by_xpath方法调用
    #     if by == "id":
    #         loc = self.by_id(value)
    #     elif by == "xpath":
    #         loc = self.by_xpath(value)
    #     loc.click()     # 发送内容前建议先点击一下
    #     loc.send_keys(send_value)

    # send_keys，**kwargs这种方式，by、value需要被替换
    def send_keys(self,**kwargs):
        """
        发送内容
        :param by:
        :param value:
        :param send_value:
        :return:
        """
        # 加个判断：根据by类型，进行by_id还是by_xpath方法调用
        by,value = kwargs["by"],kwargs["value"]
        if by == "id":
            loc = self.by_id(value)
        elif by == "xpath":
            loc = self.by_xpath(value)
        loc.click()  # 发送内容前建议先点击一下
        loc.send_keys(kwargs["send"])


    # 元素等待方法：WebDriverWait
    def by_find_element(self,by,value,timeout=30,poll=3):
        """
        隐式等待，寻找元素
        :param by:
        :param value:
        :param timeout:
        :param poll:
        :return:
        """
        try:
            WebDriverWait(self.driver,timeout,poll).until(lambda x:x.find_element(by,value))
            return self.driver.find_element(by,value)
        except Exception as e:
            self.log.error("没有找到该元素：{}".format(e))

    # # toast
    #     # def is_toast_exist(self,text,timeout=30,poll=3):
    #     #     # 使用by_find_element寻找元素，类型是xpath，value自定义
    #     #     # WebDriverWait获取信息，text
    #     #     # toast_loc = "//*[contains(@text,'手机号格式错误')]"
    #     #     try:
    #     #         toast_loc = "//*[contains(@text,'"+ text +"')]"
    #     #         ele = WebDriverWait(self.driver,timeout,poll).until(lambda x:x.find_element(By.XPATH,toast_loc))
    #     #         self.log.info("获取toast内容为：{}".format(ele.text))
    #     #         return True
    #     #     except Exception as e:
    #     #         self.log.error("toast获取失败，错误信息：{}".format())
    #     #         return False

    # toast
    def is_toast_exist(self, **kwargs):
        # 使用by_find_element寻找元素，类型是xpath，value自定义
        # WebDriverWait获取信息，text
        # toast_loc = "//*[contains(@text,'手机号格式错误')]"
        try:
            text = kwargs["expect"]
            toast_loc = "//*[contains(@text,'" + text + "')]"
            ele = WebDriverWait(self.driver, timeout=3, poll_frequency=0.5).until(lambda x: x.find_element(By.XPATH, toast_loc))
            self.log.info("获取toast内容为：{}".format(ele.text))
            return True
        except Exception as e:
            self.log.error("toast获取失败，错误信息：{}".format())
            return False

    # # 定义点击click方法
    # def click_btn(self,by,value):
    #     # 加个判断：根据by类型，进行by_id还是by_xpath方法调用
    #     if by == "id":
    #         loc = self.by_id(value)
    #     elif by == "xpath":
    #         loc = self.by_xpath(value)
    #     loc.click()

    # 定义点击click方法，**kwargs这种方式，by和value需要被替换
    def click_btn(self, **kwargs):
        # 加个判断：根据by类型，进行by_id还是by_xpath方法调用
        by,value = kwargs["by"],kwargs["value"]
        if by == "id":
            loc = self.by_id(value)
        elif by == "xpath":
            loc = self.by_xpath(value)
        loc.click()

    # toast错误进行拍图，并放在allure报告中，同时需要修改/conf/keywords.yml，verify_toast: "assert_toast_result"
    # def assert_toast_result(self,**kwargs):
    #     toast_result = self.is_toast_exist(**kwargs)
    #     try:
    #         assert toast_result == False
    #     except Exception as e:
    #         png = self.driver.get_screenshot_as_png()
    #         allure.attach(png,"toast错误",allure.attachment_type.PNG)
    #         raise e
    def assert_toast_result(self,**kwargs):
        toast_result = self.is_toast_exist(**kwargs)
        assert toast_result

    # 获取屏幕尺寸
    def get_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    # 显示屏幕尺寸
    # l = get_size()
    # print(l)

    # 向左水平滑动
    def swipeLift(self, t=500, n=2):
        l = self.get_size()
        x1 = int(l[0] * 0.9)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.1)
        # 向左滑动2次
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)

    # 向上滑动
    def swipeUp(self, t=500, n=1):
        l = self.get_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)

# 定义一个装饰器，其他方法错误的时候也进行拍图操作
# 1、定义装饰器2层函数
def screenshot_allure(func):
    def get_err_screenshot(self,*args,**kwargs):
    # 2、定义内部函数的时候，进行一个操作，错误处理及拍图操作
        try:
            func(self,*args,**kwargs)
        except Exception as e:
            png = self.driver.get_screenshot_as_png()
            name = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            allure.attach(png,name,allure.attachment_type.PNG)
            raise e
    # 3、返回内部函数名称
    return get_err_screenshot
    # 4、重构toast断言
    # 5、调用装饰器

# 用/Appium_AutoTest/testcase/Caps_Base.py这个文件进行调试