from conf import Conf
from utils.YamlUtil import YamlReader


def get_keyword(name):
    # 读取配置文件，文件路径：绝对路径
    keywords_file = Conf.keywords_path
    # 使用YamlReader的data()方法读取文件，是字典格式
    reader = YamlReader(keywords_file).data()
    # 根据字典的key(name)获取值
    value = reader[name]
    return value


# getattr()
class A:
    name = "test"
    def get_name(self):
        print(self.name)


if __name__ == '__main__':
    # print(get_keyword("click"))

    a = A()
    print(getattr(a,"name"))    # 输出name属性值
    fun = getattr(a,"get_name")
    print(fun)