from email.mime.text import MIMEText
import smtplib

from config.config import get_settings

setting = get_settings()


def init_message(msg_title, msg_content, receive_email_list, sender):
  # 设置email信息
    # 邮件内容设置
    # message = MIMEText('邮件发送内容', 'plain', 'utf-8')
    message = MIMEText(f'{msg_content}', 'plain', 'utf-8')
    # 邮件主题
    # message['Subject'] = '测试发送邮件'
    message['Subject'] = f'{msg_title}'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    # message['To'] = receive_email_list[0]
    print(message)
    return message


def send_message(receive_email_list, message, sender, mail_host, mail_user, mail_pass):
    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receive_email_list, message.as_string())
        # 退出
        smtpObj.quit()
        return 'success'
    except smtplib.SMTPException as e:
        return f'error,{e}'  # 打印错误



def send_email(msg_title, msg_content, receive_email_list):
    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = setting.mail_host
    # 163用户名
    mail_user = setting.mail_user
    # 密码(部分邮箱为授权码)
    mail_pass = setting.mail_pass
    # 邮件发送方邮箱地址
    sender = setting.sender

    message = init_message(msg_title, msg_content, receive_email_list, sender=sender)
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    # receivers = json.loads(email_setting.get('receivers'))
    return send_message(receive_email_list, message=message, mail_host=mail_host, mail_user=mail_user, mail_pass=mail_pass, sender=sender)

