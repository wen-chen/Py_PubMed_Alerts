import time
import sys
import pickle
import smtplib
from email.mime.text import MIMEText
from util.search_pubmed  import get_papers_list

log_file = open("PubMed_Alerts.log", "a")
log_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')

mail_from = "BioChen.com<admin@biochen.com>"
mail_host = "smtp.ym.163.com"
mail_usr = "admin@biochen.com"
mail_pwd = "www.biochen.com"

try:
    server = smtplib.SMTP(mail_host)
    server.login(mail_usr,mail_pwd)
    log_file.write("The connection to the mail server was successful!" + '\n')
except:
    log_file.write("The connection to the mail server failed!" + '\n')
    log_file.close()
    sys.exit()


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

def run(task):
    task_id, keyword, mail_address = task

    task_dump = open(task_id, 'rb')
    kown_papers_set = pickle.load(task_dump)
    task_dump.close()
    
    papers_list = get_papers_list(keyword, retmax = "100") 
    new_papers_list = list()
    for paper in papers_list:
        if paper[0] not in kown_papers_set:
            new_papers_list.append(paper)  
                  
    if len(new_papers_list) > 0:
        kown_papers_set.update(set([item[0] for item in new_papers_list]))
        task_dump = open(task_id, 'wb')
        pickle.dump(kown_papers_set, task_dump)
        task_dump.close() 
        
        content = str()
        for i, paper in enumerate(new_papers_list):
            PMID, Title, Journal, IF, Month, Year, Abstract = paper
            url = "https://www.ncbi.nlm.nih.gov/pubmed/" + PMID
            content += str(i + 1) + ". " + Title + '\n'
            content += Journal + "  " + "IF: " + IF + "  " + Month + '/' + Year + '\n'
            content += "Abstract: " + str(Abstract) + '\n'
            content += url + "\n\n"
        mail_to_list = [mail_address]
        subject = "PubMed Alerts: " + keyword
        send_mail(mail_to_list, subject, content)     

for task in task_list:
    try:
        run(task) 
        log_file.write("{} is successful!\n".format(task[0]))    
    except:
        log_file.write("{} failed!\n".format(task[0])) 

try:    
    server.close()
    log_file.write("The mail server was successfully closed!\n")
except:
    log_file.write("The mail server was failed closed!\n")

log_file.close()