from Bio import Entrez   

def search(query, retmax='20', retmode='xml', db='pubmed'):
    Entrez.email = 'admin@biochen.com'
    handle = Entrez.esearch(db = db, 
                            retmax = retmax,
                            retmode = retmode, 
                            term = query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'admin@biochen.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

Journal_IF = dict()
ISSN_IF = dict()
with open("IF2016.tsv", "r") as IF2016:
    for line in IF2016:
        line = line.strip()
        item = line.split('\t')
        Journal_IF[item[0]] = item[3] 
        ISSN_IF[item[2]] = item[3]

def get_papers_list(keyword, retmax = "20"):
    papers_list = list()
    results = search(keyword, retmax = retmax)
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):        
        Title = paper['MedlineCitation']['Article']['ArticleTitle']
        try:
            Abstract = ''
            for Text in paper['MedlineCitation']['Article']['Abstract']["AbstractText"]:
                try:
                    Label = Text.attributes['Label']
                    Abstract += Label + ': ' 
                except:
                    pass
                Abstract += Text.title() + '\n'
        except:
            Abstract = "NA"
        PMID = paper['MedlineCitation']["PMID"].split(',')[0]
        try:
            Year = paper['MedlineCitation']['Article']["Journal"]["JournalIssue"]["PubDate"]['Year']
        except:
            Year = "NA"
        try:
            Month = paper['MedlineCitation']['Article']["Journal"]["JournalIssue"]["PubDate"]['Month']
        except:
            Month = "NA"
        Journal = paper['MedlineCitation']['Article']["Journal"]["Title"]
        try:
            ISSN = str(paper['MedlineCitation']['Article']["Journal"]["ISSN"])
        except:
            ISSN = "NA"
        if Journal.upper() in Journal_IF:
            IF = Journal_IF[Journal.upper()]
        else:
            if ISSN in ISSN_IF:
                IF = ISSN_IF[ISSN]
            else:
                IF = "NA"                       
        papers_list.append([PMID, Title, Journal, IF, Month, Year, Abstract])
    return papers_list

if __name__ == '__main__':
    results = search('lncRNA')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']): 
        Title = paper['MedlineCitation']['Article']['ArticleTitle']