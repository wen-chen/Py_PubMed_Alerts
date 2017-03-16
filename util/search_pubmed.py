from Bio import Entrez

def search(query, sort='relevance', retmax='20',retmode='xml', db='pubmed'):
    Entrez.email = 'admin@biochen.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='20',
                            retmode='xml', 
                            term=query)
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

if __name__ == '__main__':
    results = search('lncRNA')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):        
        Title = paper['MedlineCitation']['Article']['ArticleTitle']
        print("{}. {}".format(i+1, Title))        