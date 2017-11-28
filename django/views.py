from django.shortcuts import render
import pymysql
# Create your views here.
def PubMed_Alerts(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword")
        email = request.POST.get("email")
        
        #连接数据库
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='qycw1989', db='pubmed_alerts')
        
        #查询任务是否存在
        cur = conn.cursor()
        keyword_set = set()
        if cur.execute("SELECT keyword FROM task_table WHERE email='{}'".format(email)):
            for each in cur:
                keyword_set.add(each[0])
        cur.close()
        
        if keyword in keyword_set:
            return render(request, 'PubMed_Alerts_result.html')
        else:
            #查询最后一条记录的id
            try:
                cur = conn.cursor()
                cur.execute("select id from task_table order by id DESC limit 1")
                i = cur.fetchone()[0] + 1
                cur.close()
            except:
                i = 1
            #将新任务添加到数据库
            cur = conn.cursor()            
            cur.execute("INSERT INTO task_table values({}, '{}', '{}', '{}')".format(i, "task" + str(i).zfill(3), keyword, email))
            conn.commit()
            cur.close()
            return render(request, 'PubMed_Alerts_result.html')
    else:
        return render(request, 'PubMed_Alerts.html')