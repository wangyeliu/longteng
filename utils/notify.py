"""发送邮件"""
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


class Notice(object):
    def email(self, body, subject, receivers, file_path):
        """发送邮件
        body是正文信息
        subject邮件主题
        receivers是收件人列表
        file_path是附件路径"""

        smtp_conf = os.getenv('SMTP_CONFIG')
        smtp_host, is_ssl, user, password = smtp_conf.split(',')

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        msg['From'] = user
        msg['To'] = ','.join(receivers)
        msg['Subject'] = subject

        att1 = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
        att1['Content-Type'] = 'application/octet-stream'
        att1["Content-Disposition"] = f'attachment; filename={file_path.split("/")[-1]}'
        msg.attach(att1)

        smtp = smtplib.SMTP_SSL(smtp_host)
        smtp.login(user, password)
        for person in receivers:
            smtp.sendmail(user, person, msg.as_string())


if __name__ == '__main__':
    Notice().email('正文', '主题', ['superhin@126.com'], 'report.html')
