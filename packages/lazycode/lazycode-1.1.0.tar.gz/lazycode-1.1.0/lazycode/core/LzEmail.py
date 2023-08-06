import smtplib
import ssl
from email.message import EmailMessage
import os


class LzEmailImp(object):
    def send_email(self, email_title: str,
                   body: str,
                   to_email_list: list,
                   enclosure_file_list: list = None,
                   is_html_body: bool = False,
                   from_email_address: str = "ttw5656@163.com",
                   email_authorization_code: str = "YWFLDCNRLGSMSHCE"):
        # 使用ssl模块的context加载系统允许的证书，在登录时进行验证
        context = ssl.create_default_context()
        # 邮件实例对象
        msg = EmailMessage()
        # 邮件发送者
        msg["From"] = from_email_address
        # 邮件标题
        msg['subject'] = email_title

        # 两种只能选一种
        if is_html_body:
            html_body = body
            msg.add_alternative(html_body, subtype='html')
        else:
            text_body = body
            msg.set_content(text_body)

        if enclosure_file_list is not None:
            for file_dic in enclosure_file_list:
                # 附件文件路径
                filename = file_dic["file_path"]
                # 可选, 文件类型
                file_type = file_dic.get("file_type", os.path.splitext(filename)[1].split(".")[1].lower())
                # 可选, 附件文件名
                email_filename = file_dic.get("email_filename", os.path.basename(filename))
                file_data = None
                with open(filename, 'rb') as f:
                    file_data = f.read()
                msg.add_attachment(file_data, maintype=file_type, subtype=file_type,
                                   filename=email_filename)

        # 使用网易邮箱smtp服务, 为了防止忘记关闭连接也可以使用with语句
        with smtplib.SMTP_SSL("smtp.163.com", 465, context=context) as smtp:  # 完成加密通讯

            # 连接成功后使用login方法登录自己的邮箱
            smtp.login(from_email_address, email_authorization_code)

            for to_email_address in to_email_list:
                msg["To"] = to_email_address

                # # 抄送
                # msg["Cc"] = to_email_address

                # 使用send_message方法发送邮件信息
                smtp.send_message(msg)


# LzEmailImp() \
#     .send_email(email_title="测试邮件",
#                 body="邮件主体",
#                 enclosure_file_list=[
#                     {
#                         "file_path": r"C:\TEMP\Rolan桌面整理.zip",
#                     }
#                 ],
#                 to_email_list=["ttw5656@163.com"]
#                 )
