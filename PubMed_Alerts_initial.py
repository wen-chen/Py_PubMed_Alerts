# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 14:17:58 2017

@author: chenw
"""

import pickle
import smtplib
from email.mime.text import MIMEText
from util.search_pubmed  import get_papers_list

mail_from = "BioChen.com<admin@biochen.com>"
mail_host = "smtp.ym.163.com"
mail_usr = "admin@biochen.com"
mail_pwd = "www.biochen.com"

server = smtplib.SMTP(mail_host)
server.login(mail_usr,mail_pwd) 

def send_mail(mail_to_list, subject, content):
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = ";".join(mail_to_list)
    server.sendmail(mail_from, mail_to_list, msg.as_string())    


task_list = list()
with open("PubMed_Alerts.conf", "r") as conf:
    for line in conf:
        line = line.strip()
        task_id, keyword, mail_address = line.split(',')
        task_list.append([task_id, keyword, mail_address]) 

first_email_content = '''Dear friend,
    Welcome to subscribe to the PubMed Alerts service. At the first time, this service will send you most recently 100 papers according to the keywords you give. In the next day, it will search on PubMed at 9 a.m. and 3 p.m. If there are new relevant literature, You will receive an email.
    This service is still in the beta version, If you have any comments and suggestions or want to unsubscribe it, please feel free to contact me.
Best Wishes
                                                                       Wen Chen'''

def run(task):    
    task_id, keyword, mail_address = task
    papers_list = get_papers_list(keyword, retmax = "100")    
    papers_set = set([item[0] for item in papers_list])
    with open(task_id, "wb") as task_dump:
        pickle.dump(papers_set, task_dump)
    if len(papers_list) > 0:
        content = str()
        for i, paper in enumerate(papers_list):
            PMID, Title, Journal, IF, Month, Year, Abstract = paper
            url = "https://www.ncbi.nlm.nih.gov/pubmed/" + PMID
            content += str(i + 1) + ". " + Title + '\n'
            content += Journal + "  " + "IF: " + IF + "  " + Month + '/' + Year + '\n'
            if Abstract != "NA":
                content += Abstract
            content += url + "\n\n"
        mail_to_list = [mail_address]
        send_mail(mail_to_list, "Welcome to subscribe to the PubMed Alerts service", first_email_content)
        send_mail(mail_to_list, "PubMed Alerts: " + keyword, content)

for task in task_list:
    run(task) 

server.close()