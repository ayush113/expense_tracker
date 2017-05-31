import sqlite3
import matplotlib.pyplot as plt
import classes
from numpy import arange,linspace
client=classes.User(1,'Joshua1','password1','What is the name of your first pet?','Tuffy',1000.0)
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def get_cats():
    with sqlite3.connect("Accounts.db") as db:
        cur=db.cursor()
        cur.execute("SELECT DISTINCT cat FROM purchases WHERE userID=?",(client.userID,))
        res=cur.fetchone()
        cats=[]
        while res!=None:
            cats.append(res[0])
            res=cur.fetchone()
    return cats

def month_stats(month, year):
    
    with sqlite3.connect("Accounts.db") as db:
        cur=db.cursor()
        
        cats=get_cats()
        
        mDict={}
        for cat in cats:
            mDict[cat]=0.0
            
        cur.execute("SELECT cat, SUM(price) FROM purchases WHERE userID=? and month=? and year=? GROUP BY cat",(client.userID, month, year))
        res=cur.fetchone()

        sum_me=0.0
        
        while res!=None:
            mDict[res[0]]=res[1]
            sum_me+=res[1]
            res=cur.fetchone()
            
    if sum_me!=0.0:
        fig=plt.figure()
        
        ax1=fig.add_subplot(212)
        ax1.pie(mDict.values(), labels=mDict.keys(), shadow=True, startangle=90, labeldistance=-10)
        ax1.axis('equal')
        ax1.legend()
        
        ax2=fig.add_subplot(211)
        x_pos=arange(len(cats))
        ax2.bar(left=x_pos, height=mDict.values(), width=0.6, align='center')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(mDict.keys())
        ax2.set_title("%s-%d" % (months[month-1],year))
        ax2.set_ylabel('Rupees')
        
        plt.savefig("%s_%s-%d.pdf" % (client.userName, months[month-1], year))
        plt.show()

def year_stats_all(year):
    cats=get_cats()
    len_cats=len(cats)
    sum_me=0.0
    yList=[]
    catDict={}
    monthList=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    for cat in cats:
        catDict[cat]=0.0
    for i in range(len_cats):
        yList.append([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
    with sqlite3.connect("Accounts.db") as db:
        cur=db.cursor()
        for i in range(len_cats):
            cur.execute("SELECT month, SUM(price) FROM purchases WHERE userID=? AND year=? AND cat=? GROUP BY month", (client.userID, year, cats[i]))
            res=cur.fetchone()
            while res!=None:
                yList[i][res[0]-1]=res[1]
                sum_me+=res[1]
                res=cur.fetchone()
            
    if sum_me!=0.0:
        
        #plt.style.use('ggplot')
        colors=plt.cm.rainbow(linspace(0,0.4,len_cats))
        fig,ax1=plt.subplots()
        #fig=plt.figure()
        
        #ax1=fig.add_subplot(121)
        x_pos=arange(12)+0.5
        botList=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        for i in range(len_cats):
            ax1.bar(left=x_pos,height=yList[i],width=0.6,align='center',bottom=botList,color=colors[i])
            for y in range(12):
                botList[y]+=yList[i][y]
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels([])
        ax1.set_title(str(year))
        ax1.set_ylabel('Rupees')

        #ax2=fig.add_subplot(312)
        plt.table(cellText=yList,rowLabels=cats, rowColours=colors, colLabels=months, loc='bottom')
        plt.subplots_adjust(left=0.2, bottom=0.2)

        #ax2=fig.add_subplot(122) IN CASE WE WANT TO PUT IT ALL IN ONE FUNCTION!
        #ax2.pie(catDict.values(), labels=catDict.keys(), shadow=True, startangle=90, labeldistance=-10)
        #ax2.axis('equal')
        #ax2.legend()

        #ax3=fig.add_subplot(313)
        #ax3.pie(monthList, labels=months, shadow=True, startangle=90, labeldistance=-10)
        #ax3.axis('equal')
        #ax3.legend()
        
        plt.savefig("%s_%d.pdf" % (client.userName, year))
        plt.show()

def year_stats_pies(year):
    cats=get_cats()
    len_cats=len(cats)
    yList=[]
    catDict={}
    monthList=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    for cat in cats:
        catDict[cat]=0.0

    with sqlite3.connect("Accounts.db") as db:
        cur=db.cursor()
        cur.execute("SELECT cat,SUM(price) FROM purchases WHERE userID=? GROUP BY cat",(client.userID,))
        res=cur.fetchone()
        while res!=None:
            catDict[res[0]]=res[1]
            res=cur.fetchone()
        cur.execute("SELECT month, SUM(price) FROM purchases WHERE userID=? AND year=? GROUP BY month",(client.userID,year))
        res=cur.fetchone()
        while res!=None:
            monthList[res[0]-1]=res[1]
            res=cur.fetchone()
        
        fig=plt.figure()
        ax1=fig.add_subplot(121)
        ax1.pie(catDict.values(), labels=catDict.keys(), shadow=True, startangle=90, labeldistance=-10)
        ax1.axis('equal')
        ax1.legend()

        ax2=fig.add_subplot(122)
        ax2.pie(monthList, labels=months, shadow=True, startangle=90, labeldistance=-10)
        ax2.axis('equal')
        ax2.legend()
        
        plt.savefig("%s_%d_Pies.pdf" % (client.userName, year))
        plt.show()
        
        

    

        
                
    
            
            
            
    
        
        
        
        
