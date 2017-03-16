from util.search_pubmed  import search, fetch_details
from util.send_email import send_mail


results = search('lncRNA')
id_list = results['IdList']
papers = fetch_details(id_list)
content = str()
for i, paper in enumerate(papers['PubmedArticle']):        
    Title = paper['MedlineCitation']['Article']['ArticleTitle']
    Abstract = paper['MedlineCitation']['Article']['Abstract']["AbstractText"]
    PMID = paper['MedlineCitation']["PMID"].split(',')[0]
    url = "https://www.ncbi.nlm.nih.gov/pubmed/" + PMID
    content += str(i + 1) + ". " + Title + '\n'
    content += str(Abstract) + '\n'
    content += url + "\n\n"
    

mail_to_list = ["chenwen@biochen.com"]          
subject = "PubMed papers"
if send_mail(mail_to_list, subject, content):  
    print("Automatically send mail successfully")
else:
    print("Automatically send mail failed")  