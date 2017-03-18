# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 14:17:58 2017

@author: chenw
"""

from util.search_pubmed  import get_papers_list
from util.send_email import send_mail
import pickle

task_list = list()
with open("PubMed_Alerts.conf", "r") as conf:
    for line in conf:
        line = line.strip()
        print(line)
        task_id, keyword, mail_address = line.split()
        task_list.append([task_id, keyword, mail_address]) 

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
            content += "Abstract: " + str(Abstract) + '\n'
            content += url + "\n\n"
        mail_to_list = [mail_address]
        subject = "PubMed Alerts"
        send_mail(mail_to_list, subject, content)

for task in task_list:
    run(task)  