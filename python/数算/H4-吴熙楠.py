def dpMuseumThief(treasureList, maxWeight):
    maxValue=0;choosenList=[];l=[]
    max_w,max_num=maxWeight,len(treasureList)
    mtv=[[0 for i in range(max_w+1)] for j in range(max_num+1)]
    treasure_used=[[False for p in range(max_w+1)] for q in range(max_num+1)]
    for i in range(1,max_num+1):
        need_w,get_v=treasureList[i-1]['w'],treasureList[i-1]['v'] 
        for j in range(1,max_w+1):
            if i==1:  
                if j<need_w:
                    mtv[1][j]=0
                else:  
                    mtv[1][j]=get_v
                    treasure_used[1][j]=True
            else:
                if j<need_w:  
                    mtv[i][j]=mtv[i-1][j] 
                else:  
                    treasure_used[i][j]=mtv[i-1][j-need_w]+get_v> mtv[i-1][j]
                    mtv[i][j]=max(mtv[i-1][j-need_w]+ get_v,mtv[i-1][j])
    maxValue=mtv[max_num][max_w]
    num=max_num
    w=max_w
    while num > 0:
        if treasure_used[num][w]:
            l.append(treasureList[num-1]) 
            w=w-treasureList[num-1]['w']
            num-=1  
        else:
            num-=1
    while len(l)>0:
        choosenList.append(l.pop())
    return maxValue,choosenList
def dpWordEdit(original, target, oplist):
    score=0;operations=[];s=[]
    m=len(original);n=len(target)
    mylist=[[0 for j in range(n+1)] for i in range(m+1)]
    mywork=[[None for j in range(n+1)] for i in range(m+1)]
    for i in range(1,m+1):
        mywork[i][0]="delete"
        mylist[i][0]=(oplist['delete'])*i
    for j in range(1,n+1):
        mywork[0][j]="insert"
        mylist[0][j]=(oplist['insert'])*j
    for i in range(1,m+1):
        for j in range(1,n+1):
            copy=mylist[i-1][j-1]+oplist['copy']
            insert=mylist[i][j-1]+oplist['insert']
            delete=mylist[i-1][j]+oplist['delete']
            if original[i-1]==target[j-1] and (copy<insert and copy<delete):
                mylist[i][j]=copy
                mywork[i][j]="copy"
            elif insert>delete:
                mylist[i][j]=delete
                mywork[i][j]="delete"
            else:
                mylist[i][j]=insert
                mywork[i][j]="insert"
    score=mylist[m][n]
    while m>0:
        s.append(mywork[m][n])
        if mywork[m][n]=="copy":
            m,n=m-1,n-1
        elif mywork[m][n]=="insert":
            n-=1
        elif mywork[m][n]=="delete":
            m-=1
    while n>0:
        s.append("insert")
        n-=1
    i,j=0,0
    while len(s)>0:
        x=s.pop()
        if x=='delete':
            x+=' '+original[i];i+=1
        elif x=='insert':
            x+=' '+target[j];j+=1
        elif x=='copy':
            x+=' '+original[i];i+=1;j+=1
        operations.append(x)
    return score,operations