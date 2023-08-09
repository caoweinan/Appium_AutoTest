from utils.LogUtil import my_log
from utils.ExcelUtil import ExcelReader
from data.ExcelConfig import ExcelSheet
from data.ExcelConfig import TestCases,TestSteps,CaseData,Elements


"""
数据处理：获取运行测试用例列表，根据列表去执行测试内容、测试步骤、操作(Action)
1、初始化测试用例文档，分别初始化4个sheet对象
2、分别定义读取4个sheet数据的方法
3、获取全部真实有效的测试用例方法（没有TC_ID就可以忽略，因为通过TC_ID关联其他sheet表）
4、根据TC_ID获取相应的列表数据，定义三个方法(根据TC_ID获取其他sheet页相同TC_ID的数据，定义三个方法：data/step/elemnet)
5、判断是否运行列，y获取执行测试用例
5、获取运行测试用例列表
"""

# 一、初始化测试用例文档，分别初始化4个sheet对象
# 1、创建类，初始化测试用例文档
class Data:
    # 初始化一般都放在__init__下面，加一个参数case_file这个文件
    def __init__(self,case_file):
        # 加个日志
        self.log = my_log()     # 通过self接收，从utils工具包导入：from utils.LogUtil import my_log
        # 2、分别初始化(实例化)4个sheet对象
        self.reader_cases = ExcelReader(case_file,"TestCases")     # 通过self接收，第一个是cases,ExcelReader(case_file,"")引号里面放sheet的名称，，从utils工具包导入：from utils.ExcelUtil import ExcelReader
        self.reader_data = ExcelReader(case_file, "CaseData")
        self.reader_steps = ExcelReader(case_file, "TestSteps")
        self.reader_elements = ExcelReader(case_file, "Elements")

        self.reader_cases = ExcelReader(case_file, ExcelSheet.TEST_CASE)  # 通过self接收，第一个是cases,ExcelReader(case_file,"")引号里面放sheet的名称，，从utils工具包导入：from utils.ExcelUtil import ExcelReader
        self.reader_data = ExcelReader(case_file, ExcelSheet.TEST_DATA)
        self.reader_steps = ExcelReader(case_file, ExcelSheet.TEST_STEP)
        self.reader_elements = ExcelReader(case_file, ExcelSheet.TEST_ELEMENTS)

# 二、分别定义读取4个sheet数据的方法
    # 1、读取reader_cases方法(测试用例)
    def get_cases_sheet(self):
        """
        获取测试用例TestCases这个sheet的数据
        :return:
        """
        return self.reader_cases.data()       # 使用的是reader_cases这个对象，reader_cases调用是data方法（data方法是编写工具类ExcelUtil时自己定义的）,加个return返回
    # 2、读取reader_data方法(数据)
    def get_data_sheet(self):
        """
        获取测试用例数据CaseData这个sheet的数据
        :return:
        """
        return self.reader_data.data()      # 使用的是reader_data这个对象，reader_data调用是data方法（data方法是编写工具类ExcelUtil时自己定义的）,加个return返回
    # 3、读取reader_steps方法(步骤)
    def get_steps_sheet(self):
        """
        获取测试用例步骤TestSteps这个sheet的数据
        :return:
        """
        return self.reader_steps.data()     # 使用的是reader_steps这个对象，reader_steps调用是data方法（data方法是编写工具类ExcelUtil时自己定义的）,加个return返回
    # 4、读取reader_elements方法(元素)
    def get_elements_sheet(self):
        """
        获取元素对象Elements这个sheet的数据
        :return:
        """
        return self.reader_elements.data()      # 使用的是reader_elements这个对象，reader_elements调用是data方法（data方法是编写工具类ExcelUtil时自己定义的）,加个return返回

# 三、获取全部真实有效的测试用例方法（没有TC_ID就可以忽略，因为通过TC_ID关联其他sheet表）
    # 1、获取测试用例sheet，TestCases有效的数据内容
    def get_cases_all(self):
        """
        获取全部的测试用例，过滤空的内容
        :return:
        """
        # 按条件TC_ID判断从全部的数据列表中过滤，来获得非空数据
        data_list = self.get_cases_sheet()      # get_cases_sheet()是获取全部测试用例的方法，并且是以列表list存储的
        # res = []
        # for data in data_list:   # 循环打印这个列表list
        #     if data["TC_ID"] !="":  # 这里面要判断一个条件，假如这个数据(字典格式)TC_ID不为空的情况下，放在一个新的列表里面，新的列表list要定义一下res = []
        #         res.append(data)        # 把非空的数据添加到新列表list中，这里就是把data放在新列表中
        res = self.get_no_empyt(data_list, TestCases.CASES_TC_ID)  # 调用获取非空数据这个方法get_no_empyt(第1个参数是data_list，第2个是个条件condition就是TC_ID)
        return res      # 再把值返回一下

    # 2、获取测试数据sheet，CaseData有效的数据内容
    def get_data_all(self):
        """
        获取全部的测试数据，过滤空的内容
        :return:
        """
        # 按条件TC_ID判断从全部的数据列表中过滤，来获得非空数据
        data_list = self.get_data_sheet()      # get_data_sheet()是获取全部测试用例的方法，并且是以列表list存储的
        # res = []
        # for data in data_list:   # 循环打印这个列表list
        #     if data["TC_ID"] !="":  # 这里面要判断一个条件，假如这个数据(字典格式)TC_ID不为空的情况下，放在一个新的列表里面，新的列表list要定义一下res = []
        #         res.append(data)        # 把非空的数据添加到新列表list中，这里就是把data放在新列表中
        res = self.get_no_empyt(data_list,CaseData.DATA_TC_ID)       # 调用获取非空数据这个方法get_no_empyt(第1个参数是data_list，第2个是个条件condition就是TC_ID)
        return res      # 再把值返回一下


    # 3、获取测试步骤sheet，TestSteps有效的数据内容
    def get_steps_all(self):
        """
        获取全部的测试步骤，过滤空的内容
        :return:
        """
        data_list = self.get_steps_sheet()  # get_steps_sheet()是获取全部测试用例的方法，并且是以列表list存储的
        res = self.get_no_empyt(data_list, TestSteps.STEP_TC_ID)  # 调用获取非空数据这个方法get_no_empyt(第1个参数是data_list，第2个是个条件condition就是TC_ID)
        return res  # 再把值返回一下

    # 4、获取元素对象sheet，Elements有效的数据内容
    def get_elements_all(self):
        """
        获取全部的元素对象，过滤空的内容
        :return:
        """
        data_list = self.get_elements_sheet()  # get_elements_sheet()是获取全部测试用例的方法，并且是以列表list存储的
        res = self.get_no_empyt(data_list, Elements.ELE_TC_ID)  # 调用获取非空数据这个方法get_no_empyt(第1个参数是data_list，第2个是个条件condition就是TC_ID)
        return res  # 再把值返回一下


# 四、根据TC_ID获取相应的列表数据，定义三个方法(根据TC_ID获取其他sheet页相同TC_ID的数据，定义三个方法：data/step/elemnet)
    # 1、data
    def get_data_by_tc_id(self,tc_id):        # 加一个参数，tc_id这个参数
        """
        根据tc_id来获取data数据
        :param tc_id:
        :return:
        """
        # ①获取全部的列表数据，可以使用之前编写过的get_data_all()这个方法，给它赋个值接收一下data_all，返回结果data_all是个列表
        data_all = self.get_data_all()
        # ②根据tc_id获取一下数据，要循环data_all这个列表，针对每一个数据进行比对，最后把结果存在一个新的列表list里面
        # data_all_tc = []        # 新的列表
        # for data in data_all:       # 做个循环
        #     if data["TC_ID"] == tc_id:   #加个判断，data["TC_ID"]恒等于我们传过来的变量tc_id
        #         data_all_tc.append(data)        # 这个时候，把内容添加到新的列表里面
        data_all_tc = self.get_by_tc_id(data_all,tc_id)       # 调用get_by_tc_id()方法，里面的参数是data_all和tc_id
        return data_all_tc      # 把结果返回一下，这样就返回了根据TC_ID获取相应的列表数据

    # 2、step
    def get_steps_by_tc_id(self, tc_id):  # 加一个参数，tc_id这个参数
        """
        根据tc_id来回去步骤数据
        :param tc_id:
        :return:
        """
        # ①获取全部的列表数据，可以使用之前编写过的get_steps_all()这个方法，给它赋个值接收一下data_all，返回结果data_all是个列表
        data_all = self.get_steps_all()
        # ②根据tc_id获取一下数据，要循环data_all这个列表，针对每一个数据进行比对，最后把结果存在一个新的列表list里面
        data_all_tc = self.get_by_tc_id(data_all, tc_id)  # 调用get_by_tc_id()方法，里面的参数是data_all和tc_id
        return data_all_tc  # 把结果返回一下，这样就返回了根据TC_ID获取相应的列表数据

    # 3、element
    def get_elements_by_tc_id(self, tc_id):  # 加一个参数，tc_id这个参数
        """
        根据tc_id来获取元素对象数据
        :param tc_id:
        :return:
        """
        # ①获取全部的列表数据，可以使用之前编写过的get_elements_all()这个方法，给它赋个值接收一下data_all，返回结果data_all是个列表
        data_all = self.get_elements_all()
        # ②根据tc_id获取一下数据，要循环data_all这个列表，针对每一个数据进行比对，最后把结果存在一个新的列表list里面
        data_all_tc = self.get_by_tc_id(data_all, tc_id)  # 调用get_by_tc_id()方法，里面的参数是data_all和tc_id
        return data_all_tc  # 把结果返回一下，这样就返回了根据TC_ID获取相应的列表数据

    # 4、element 通过元素
    def get_elements_by_element(self,tc_id,element_name):
        """
        根据步骤sheet中的元素名称和tc_id 获取相应的数据
        :param tc_id:
        :param element_name:
        :return:
        """
        elements = self.get_elements_by_tc_id(tc_id)
        res = None
        for ele in elements:
            if str(ele[Elements.ELE_NAME]) == str(element_name):
                res = ele
        return res

# 五、判断是否运行列，y获取执行测试用例，针对TestCases编写一个方法，针对CaseData编写一个方法
    # 1、是否运行，针对TestCases的方法
    def get_run_cases(self):
        """
        按条件是否运行，y，获取TestCases里执行的测试用例
        :return:
        """
        # 根据是否运行这一列判断它恒等于 == y/Y，获取执行测试用例
        # 先获取全部的测试用例
        run_list = self.get_cases_all()
        # 定义一个新的列表list
        run_cases_list = []
        # 对应列"是否运行" == y/Y，生成一个新的执行测试用例
        for line in run_list:       # 循环打印每一行数据
            if str(line[TestCases.CASES_IS_RUN]).lower() == "y":     # 进行判断与小写y进行对比，每一行当中取到列的内容("是否运行")，然后把信息做字符串格式化(str)，使用lower()方法：无论是大写还是小写都转换为小写
                run_cases_list.append(line)     # 如果是y就放在新的列表list里面
        return run_cases_list       # 最后返回

    # 2、是否运行，针对CaseData的方法
    def get_run_data(self,tc_id):
        """
        按条件是否运行，y，获取CaseData里执行的测试用例
        :return:
        """
        # 根据是否运行这一列判断它恒等于 == y/Y，获取执行测试用例
        # 先获取全部的测试用例
        run_list = self.get_data_all()
        # 定义一个新的列表list
        run_cases_list = []
        # 对应列"是否运行" == y/Y，生成一个新的执行测试用例
        for line in run_list:       # 循环打印每一行数据，加一个判断and "TC_ID" in line["TC_ID"]，针对TC_ID进行验证做关联，假如有TC_ID并且在line这个数据里面，需要TC_ID增加一个变量(def get_run_data(self,tc_id):)
            if str(line[CaseData.DATA_IS_RUN]).lower() == "y" and tc_id in line[CaseData.DATA_TC_ID]:     # 进行判断与小写y进行对比，每一行当中取到列的内容("是否运行")，然后把信息做字符串格式化(str)，使用lower()方法：无论是大写还是小写都转换为小写
                run_cases_list.append(line)     # 如果是y就放在新的列表list里面
        return run_cases_list       # 最后返回结果

# 六、获取运行测试用例列表
    def run_list(self):     # 定义个方法
        # 1、获取TestCases执行测试用例列表
        cases = self.get_run_cases()        # 获取当前所运行的数据
        self.log.debug("获取TestCases表测试个数{}，数据内容{}".format(len(cases),cases))        # 打印日志,通过format()格式化一下，第一个len()个数，第二个数据内容cases

        # 2、根据这个列表中的TC_ID来获取对应的CaseData数据，还是生成一个新的列表list
        data_list = list()      # 列表用list()和[]，都可以是一样的
        # 做个循环，循环的时候获取一个tc_id，通过tc_id调用get_run_data()方法，获取对应的测试用例
        for case in cases:
            tc_id = case[TestCases.CASES_TC_ID]
            tmp_data_list = self.get_run_data(tc_id)    # tmp_data_list相当于方法ttt()里的a
            desc = case[TestCases.CASE_DESC]    # desc相当于方法ttt()里的b
            note = case[TestCases.CASE_NOTE]    # note相当于方法ttt()里的c
            for data in tmp_data_list:
                # 1、增加备注，生成allure报告中用
                data.update({TestCases.CASE_NOTE:note}) # 内容是个字典，key就是TestCases.CASE_NOTE，value就是note
                # 2、增加描述，生成allure报告中用
                data.update({TestCases.CASE_DESC:desc}) # 内容是个字典，key就是TestCases.CASE_DESC，value就是desc

            # get_run_data  [{}]
            # data_list.append  [[{}]]
            # data_list.append(self.get_run_data(tc_id))      # 把信息放在一个新的列表list里面

            # extend追加
            # alist = [{a},{b}]
            # alist_new = []
            # alist_new.extend(alist)   结果：alist_new  [{a},{b}]
            # data_list.extend(self.get_run_data(tc_id))  # 因为增加了备注和描述，extend方法需要修改一下
            data_list.extend(tmp_data_list)  # 因为增加了备注和描述，extend方法需要修改一下
            self.log.debug("获取CaseData表测试个数{}，数据内容{}".format(len(data_list), data_list))        # 打印日志,通过format()格式化一下，第一个len()个数，第二个数据内容data_list
        return data_list        # 最后返回结果

    # 练习
    def ttt(self):
        a = [{"a":"1","b":"2"},{"a":"3","b":"4"}]   # 用例的格式
        b = {"描述":"登录"}
        c = {"备注":"登录测试用例"}
        # 把b和c放到a里面，使用update方法，只需要对a进行个循环，分别update一下就可以
        # b.update(c)
        # print(b)
        # print(c)

        print("添加之前a:",a)
        for i in a:
            print(i)
            i.update(b)
            i.update(c)
        print("添加之后a:",a)


    """
    下面的内容都是相同的，为了避免代码冗余，可以把它定义成一个方法get_no_empyt获取非空数据，这个方法加些参数(第1个参数是data_list，第2个是个条件condition就是TC_ID，用condition替换一下TC_ID)，直接调用就可以了
        res = []
            for data in data_list:   # 循环打印这个列表list
                if data["TC_ID"] !="":  # 这里面要判断一个条件，假如这个数据(字典格式)TC_ID不为空的情况下，放在一个新的列表里面，新的列表list要定义一下res = []
                    res.append(data)        # 把非空的数据添加到新列表list中，这里就是把data放在新列表中
            return res      # 再把值返回一下
    """
    def get_no_empyt(self,data_list,condition):     # 获取非空数据方法，需要传一个参数(第1个参数是data_list，第2个是个条件condition就是TC_ID，用condition替换一下TC_ID)
        """
        按条件condition来回去数据，过滤非空的数据
        :param data_list:
        :param condition:
        :return:
        """
        res = []
        for data in data_list:  # 循环打印这个列表list
            if data[condition] != "":  # 这里面要判断一个条件，假如这个数据(字典格式)TC_ID不为空的情况下，放在一个新的列表里面，新的列表list要定义一下res = []
                res.append(data)  # 把非空的数据添加到新列表list中，这里就是把data放在新列表中
        return res  # 再把值返回一下

    """
    下面的内容都是相同的，为了避免代码冗余，可以把它定义成一个方法get_by_tc_id，这个方法加些参数(第1个参数是data_list，第2个是参数tc_id，用data_list替换一下data_all)，直接调用就可以了
    data_all_tc = []        # 新的列表
        for data in data_all:       # 做个循环
            if data["TC_ID"] == tc_id:   #加个判断，data["TC_ID"]恒等于我们传过来的变量tc_id
                data_all_tc.append(data)        # 这个时候，把内容添加到新的列表里面
        return data_all_tc      # 把结果返回一下，这样就返回了根据TC_ID获取相应的列表数据
    """
    def get_by_tc_id(self,data_list,tc_id):
        """
        根据tc_id来获取数据，生产一个新的列表list
        :param data_list:
        :param tc_id:
        :return:
        """
        data_all_tc = []  # 新的列表
        for data in data_list:  # 做个循环
            if data["TC_ID"] == tc_id:  # 加个判断，data["TC_ID"]恒等于我们传过来的变量tc_id
                data_all_tc.append(data)  # 这个时候，把内容添加到新的列表里面
        return data_all_tc  # 把结果返回一下，这样就返回了根据TC_ID获取相应的列表数据

if __name__ == '__main__':
    # 初始化一下类，类的名字是Data
    res_data = Data("../data/data.xls")      # 类的参数是一个测试用例的名称，放在了Appium_AutoTest/data/下面，结果给它赋个值接收一下res_data
    # # 调用一下get_cases_all这个方法，print打印查看
    # print(res_data.get_cases_all())
    # # 调用一下get_data_all这个方法，print打印查看
    # print(res_data.get_data_all())
    # # 调用一下get_steps_all这个方法，print打印查看
    # print(res_data.get_steps_all())
    # # 调用一下get_steps_all这个方法，print打印查看
    # print(res_data.get_elements_all())

    # # 调用一下get_data_by_tc_id和get_data_all这个两个方法，print打印查看，根据TC_ID对数据进行一下对比
    # print(res_data.get_data_by_tc_id("TC_Login"))       # 引号里面内容写TC_ID
    # print(res_data.get_data_all())

    # 调用一下get_steps_by_tc_id和get_steps_all这个两个方法，print打印查看，根据TC_ID对数据进行一下对比
    # print(res_data.get_steps_by_tc_id("TC_Login"))  # 引号里面内容写TC_ID
    # print(res_data.get_steps_all())

    # 调用一下get_elements_by_tc_id和get_elements_all这个两个方法，print打印查看，根据TC_ID对数据进行一下对比
    # print(res_data.get_elements_by_tc_id("TC_Login"))  # 引号里面内容写TC_ID
    # print(res_data.get_elements_all())

    # 调用一下get_run_cases和get_cases_all这个两个方法，print打印查看，根据是否运行对数据进行一下对比
    # print(res_data.get_run_cases())
    # print(res_data.get_cases_all())

    # 调用一下get_run_data和get_data_all这个两个方法，print打印查看，根据是否运行对数据进行一下对比
    # print(res_data.get_run_data("TC_Login"))      # 增加tc_id参数"TC_Login"
    # print(res_data.get_data_all())

    # 调用run_list方法，print打印查看，可以运行测试用例列表
    print(res_data.run_list())

    # 调用ttt方法，print打印查看，因为没有返回值所以有个None
    # print(res_data.ttt())
