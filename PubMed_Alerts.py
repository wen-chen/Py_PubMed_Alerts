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
    papers_list = get_papers_list(keyword)    
    papers_set = set([item[0] for item in papers_list])
    task_dump = open(task_id, 'rb')
    papers_set = pickle.load(task_dump)
    task_dump.close()
    kown_papers = list()
    for paper in papers_list:
        if paper[0] in papers_set:
            kown_papers.append(paper)
    for paper in kown_papers:
        papers_list.remove(paper)
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
        subject = "PubMed Alerts: " + keyword
        send_mail(mail_to_list, subject, content)     

for task in task_list:
    run(task) 