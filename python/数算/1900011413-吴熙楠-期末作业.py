class Queue:  # 队列
    def __init__(self):
        self.items=[]

    def isEmpty(self):
        return self.items==[]

    def enqueue(self,item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Vertex:  # 顶点
    def __init__(self,key):
        self.name=key  # 演员名字
        self.films=[]  # 出演的电影名字列表
        self.films_id=[]  # 出演的电影id列表
        self.connectedTo={}  # 与该顶点相连的其它顶点为key，权重为value的映射
        self.color='white'
        self.dist=0  # 与起始顶点的距离
        self.pre=None  # 先驱顶点

    def addNeighbor(self,nbr,weight):
        self.connectedTo[nbr]=weight

    def addFilm(self,film,film_id):
        self.films.append(film)
        self.films_id.append(film_id)

    def setColor(self,color):
        self.color=color

    def setDistance(self,d):
        self.dist=d

    def setPre(self,pred):
        self.pre=pred
    
    def getConnections(self):
        return self.connectedTo.keys()

class Graph:  # 图
    def __init__(self):#图初始化，属性为顶点数量和key到顶点的映射表
        self.vertices={}
        self.numVertices=0

    def addVertex(self,key):#添加新顶点:return: 新结点
        
        self.numVertices=self.numVertices+1
        newVertex=Vertex(key)
        self.vertices[key]=newVertex
        return newVertex

    def getVertex(self,key):#通过key查找顶点,return: 若存在key返回key对应的顶点，否则返回None
        
        if key in self.vertices:
            return self.vertices[key]
        else:
            return None

    def __getitem__(self,item):
        return self.getVertex(item)

    def __contains__(self,v):
        return v in self.vertices

    def addEdge(self,f,t,weight=1):
        """
        增加图的边
        f: 起始顶点的key值
        t: 终止顶点的key值
        weight: 权重，默认为1
        return: None
        """
        if f not in self.vertices:
            nv=self.addVertex(f)
        if t not in self.vertices:
            nv=self.addVertex(t)
        self.vertices[f].addNeighbor(self.vertices[t],weight)

    def getVertices(self):#返回顶点的key值列表
        
        return list(self.vertices.keys())

    def __iter__(self):#返回所有顶点的可迭代对象
        
        return iter(self.vertices.values())

class Component:#连通分支类
    def __init__(self):
        #生成一个连通分支的实例，属性包括它的规模、演员、电影id、直径等
        self.scale=0#规模，即演员数量
        self.actors=[]#该连通分支内所有演员的列表
        self.films_id=[]#连通分支内所有电影id列表
        self.most_type=[]#连通分支内电影所属类别的前三名
        self.diameter=-1#直径
        self.aver_star=0#电影的平均星级

    def addActor(self,actor):
        #在联通分支内添加演员
        self.actors.append(actor)
        self.scale+=1

    def addFilm(self,film_id):
        #在连通分支内添加电影
        self.films_id.append(film_id)

    def averageStar(self):
        #计算当前连通分支内所有电影的平均星级
        self.aver_star=sum([film_dict[x]["star"] for x in self.films_id]) / len(self.films_id)

    def maxDiameter(self):
        #用bfs算法计算当前连通分支直径
        graph = bulidGraph([film_dict[x] for x in self.films_id])#生成一个连通图
        for v in graph:#对每一个顶点用bfs计算到它的最大距离
            for t in graph:#重置颜色
                t.setColor('white')
            vertex_queue=Queue()
            vertex_queue.enqueue(v)
            v.setColor('gray')#入队后的顶点将color设为'grey'，避免再次入队
            v.setDistance(0)#将起始顶点的距离设为0
            while not vertex_queue.isEmpty():
                temp=vertex_queue.dequeue()
                for nbr in temp.connectedTo:#将相邻未入过队的顶点入队
                    if nbr.color=='white':
                        vertex_queue.enqueue(nbr)
                        nbr.setColor('gray')#入队后的顶点将color设为'grey'，避免再次入队
                        nbr.setDistance(temp.dist+1)#对应距离加1
            self.diameter=max(self.diameter,temp.dist)#取最大距离
    
import json

f=open('Film.json','rb')
film_data=json.load(f)  # 从json文件中读取电影数据
film_dict={x["_id"]["$oid"]: x for x in film_data}  # 从id到电影列表的映射，便于用id查找电影（电影名存在重复）

def bfs(graph):
    #找到所有的连通分支,返回一个列表，元素为Component类，列表包含所有的连通分支，并按规模排序，其中仅有一人的分支按演员名字排序
    for v in graph:
        v.setColor('white')
    count=-1#计数
    connected_components=[None] * 5000
    for v in graph:
        if v.color=='white':
            vertex_queue=Queue()
            count += 1#一个新连通分支
            vertex_queue.enqueue(v)
            connected_components[count]=Component()#生成一个Component类
            v.setColor('gray')
            while not vertex_queue.isEmpty():#bfs
                temp=vertex_queue.dequeue()
                connected_components[count].addActor(temp.name)#在Component类中加入演员和电影
                for _id in temp.films_id:
                    connected_components[count].addFilm(_id)
                for nbr in temp.connectedTo:
                    if nbr.color=='white':
                        vertex_queue.enqueue(nbr)
                        nbr.setColor('gray')
    connected_components=connected_components[:count + 1]#去除多余的None
    connected_components.sort(key=lambda x: len(x.actors), reverse=True)#按规模排序
    i = 0
    while i < len(connected_components):#查找第一个仅有一个演员的Component的索引
        if len(connected_components[i].actors)==1:
            break
        i += 1
    connected_components=connected_components[:i]+sorted(connected_components[i:],key=lambda x: x.actors[0])#后面的按名字排序
    return connected_components

def bulidGraph(filmdata):
    #通过电影信息列表生成一个图
    graph = Graph()
    for film in filmdata:
        title=film["title"]
        _id=film["_id"]["$oid"]
        coactors=[x for x in film["actor"].split(',') ]#一部电影中所有演员的列表
        for a in coactors:
            for b in coactors:
                if a!=b:
                    graph.addEdge(a, b)#添加边，同时生成顶点
        for actor in coactors:#为演员顶点添加电影
            if actor not in graph:
                graph.addVertex(actor)
            graph[actor].addFilm(title, _id)
    return graph

def topThreeType(films_id_list):
    #查找电影所属类别的前三名,返回前三名的列表
    from collections import Counter
    type_counter=Counter()
    for _id in films_id_list:
        thetype = film_dict[_id]["type"].split(',')
        for t in thetype:
            if t in type_counter:
                type_counter[t]+=1
            else:
                type_counter[t]=1
    typelist=[]
    for x in type_counter.most_common(3):
        typelist.append(x[0])
    return typelist


if __name__ == '__main__':
    actor_graph = bulidGraph(film_data)#生成图

    comp = bfs(actor_graph)
    num = len(comp)#连通分支数

    for c in comp:#计算每个连通分支的类型、直径、平均星级
        c.most_type=topThreeType(c.films_id)
        if c.scale < 100:
            c.maxDiameter()
        c.averageStar()

    """
    第1、2小题
    """
    print(f'联通分支总数：{len(comp)}')
    numlist = list(range(20)) + list(range(-20, 0))  # 需要输出的索引：前20个和后20个
    print(f"{'序号':<5s}{'演员数':<10s}{'类别前三名':<20s}{'直径':<6s}{'平均星级':<10s}")
    def chineseLen(lst):
        return len(''.join(lst))
    for i in numlist:#输出结果对齐
        print(
            f"{i:<6d}{comp[i].scale:<8d}{str(comp[i].most_type) + chr(12288) * (7 - chineseLen(comp[i].most_type)):<24s}{comp[i].diameter:<6d}{comp[i].aver_star:<10.2f}")
    """
    第3小题
    """
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from brokenaxes import brokenaxes
    sps1, sps2, sps3=GridSpec(3,1)
    plt.figure(figsize=(12, 12))
    # 分割
    bax=brokenaxes(ylims=((0,50), (84675, 84700)),subplot_spec=sps1)
    bax.set_title('size')
    bax.bar(range(40),[x.scale for x in comp[:20]] + [x.scale for x in comp[-20:]],tick_label=numlist)
    plt.subplot(312)
    plt.bar(range(40),[17] + [x.diameter for x in comp[1:20]] + [x.diameter for x in comp[-20:]],tick_label=numlist)
    plt.title('diameter')
    plt.subplot(313)
    plt.bar(range(40),[x.aver_star for x in comp[:20]] + [x.aver_star for x in comp[-20:]],tick_label=numlist)
    plt.title('average star')
    
    plt.show()

    """
    第4小题
    """
    zhou = actor_graph['周星驰']
    coactor = ['周星驰'] + [x.name for x in zhou.connectedTo]
    all_films = set()
    for actor in coactor:
        all_films = all_films | set(actor_graph[actor].films_id)

    print(f"周星驰电影平均星级：{sum([film_dict[x]['star'] for x in zhou.films_id]) / len(zhou.films_id):.2f}")
    
    """
    第5小题
    """
    print(f"周星驰和他的共同出演者，有：{len(coactor)}人")
    print(f"他们各自一共出演了电影：{len(all_films)}部")
    print(f"所出演的电影平均星级：{sum([film_dict[x]['star'] for x in all_films]) / len(all_films):.2f}")
    print(f"电影所属类别的前三名：{topThreeType(all_films)}")
    
    """
    第6小题
    """
    a = actor_graph['莉莉·柯林斯']
    coactor1 = ['莉莉·柯林斯'] + [x.name for x in a.connectedTo]
    all_films1 = set()
    for actor in coactor1:
        all_films1 = all_films1 | set(actor_graph[actor].films_id)
    b = actor_graph['日高里菜']
    coactor2 = ['日高里菜'] + [x.name for x in a.connectedTo]
    all_films2 = set()
    for actor in coactor1:
        all_films2 = all_films2 | set(actor_graph[actor].films_id)
    print(f"莉莉·柯林斯电影平均星级：{sum([film_dict[x]['star'] for x in a.films_id]) / len(a.films_id):.2f}")
    print(f"莉莉·柯林斯所出演电影：{a.films}")
    print(f"莉莉·柯林斯电影类别前三:{topThreeType(all_films1)}")
    print(f"日高里菜电影平均星级：{sum([film_dict[x]['star'] for x in b.films_id]) / len(b.films_id):.2f}")
    print(f"日高里菜所出演电影：{b.films}")
    print(f"日高里菜电影类别前三:{topThreeType(all_films2)}")
    
    
    