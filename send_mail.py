import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# 第三方 SMTP 服务
# 设置服务器
mail_host = os.getenv("EMAIL_FROM_SMTP")
# 25, 587, 465, 2525
# https://www.poftut.com/what-is-smtp-port-number-25-587-465-2525
# 使用telnet命令来检测端口是否开放
mail_port = 465
sender = os.getenv("EMAIL_FROM")
# 用户名
mail_user = os.getenv("EMAIL_FROM_USERNAME")
# 口令
mail_pass = os.getenv("EMAIL_FROM_PASSWORD")
# 接收邮件
receivers = [os.getenv("EMAIL_TO")]


def send_mail_from_txt(sub: str):
    # 从文件中获取正文
    context = ''
    with open(file="mail_content.txt", mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            context = context + line
    if context != '':
        send_mail(sub, context)


def send_message(message, subject):
    message['From'] = formataddr((mail_user, sender))
    message['To'] = ','.join(receivers)
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")


def send_mail(sub: str, content: str):
    # 主题
    subject = 'GitHub Action - ' + sub
    message = MIMEText(content, 'plain', 'utf-8')
    send_message(message, subject)


def send_mail_html(sub: str, content: str):
    # 主题
    subject = 'GitHub Action - ' + sub
    message = MIMEText(content, 'html', 'utf-8')
    send_message(message, subject)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        send_mail_from_txt(sys.argv[1])
    elif len(sys.argv) == 3:
        send_mail(sys.argv[1], sys.argv[2])
    else:
        print('未指定主题或正文')
