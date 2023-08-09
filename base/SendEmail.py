from conf import Conf
from utils.EmailUtil import SendEmail


# 1、邮件配置conf配置conf.yml
# 2、send_mail()发送邮件操作
def send_mail(title="测试", content="", report_file=""):
    email_info = Conf.config["EMAIL"]
    smtp_addr = email_info["smtpsever"]
    username = email_info["username"]
    password = email_info["password"]
    recv = email_info["receiver"]
    email = SendEmail(smtp_addr=smtp_addr,
              username=username,
              password=password,
              recv=recv,
              title=title,
              content=content,
              file=report_file)
    email.send_mail()
