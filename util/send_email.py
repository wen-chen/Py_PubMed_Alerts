import smtplib
from email.mime.text import MIMEText

def send_mail(mail_to_list,                                       #收件人列表
              subject,                                            #邮件主题
              content,                                            #邮件内容
              mail_from = "BioChen.com<admin@biochen.com>",       #发件人信息
              mail_host = "smtp.ym.163.com",                      #SMTP服务器地址
              mail_usr = "admin@biochen.com",                     #用户名
              mail_pwd = "www.biochen.com",                       #密码
              ):    
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = ";".join(mail_to_list)                            #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP(mail_host)                          #连接服务器
        server.login(mail_usr,mail_pwd)                           #登录操作
        server.sendmail(mail_from, mail_to_list, msg.as_string()) #发送邮件
        server.close()
        return True
    except Exception:
        print(Exception)
        return False


if __name__ == "__main__":
    mail_to_list = ["admin@biochen.com"]          
    subject = "Automatically send mail successfully"
    content = "This is an automatic mail from Biochen.com!"    
    if send_mail(mail_to_list, subject, content):  
        print("Automatically send mail successfully")
    else:
        print("Automatically send mail failed")