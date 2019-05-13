class Solution:
    def classification(self, text):
        import re
        from math import log
        from math import exp
        from functools import reduce
        def pre_proc(txt):
            txt = txt.split('\n')
            txt = [i for i in txt if len(i)>1]
            txt = list(map(lambda x:re.sub('[,.]','',x),txt))
            txt = list(map(lambda x:re.findall('[a-zA-Z0-9]+',x),txt))
            return txt
        stop = ['the','and','with','both','back','such','known','knew','knows','konw','would','for','that','this','from',
       'are','their','via','These','these','was','not','were','including','does','what','What','With','have','had',
       'has','them','which','its','who','whose','However','about','due','been','out','within','itself','while']
        #停用词表
        def create_word(txt):
            word_item = set(reduce(lambda x,y:x+y,txt))
            def choose(x):
                #return (x.isupper() or len(x)>3)
                return (len(x)>2) and (x not in stop) #词库选词准则
            word_item = list(filter(choose,word_item))
            return word_item
        def tf_idf(doc,word):
            ans_vector = []
            total_len = len(doc)
            for i in range(total_len):
                docu = doc[i]
                others = doc[:i]+doc[(i+1):]
                length = len(docu)
                tf = map(lambda x:docu.count(x)/length,word)
                def counting(x):
                    def temp(i):
                        if x in i:
                            return 1
                        else:
                            return 0
                    return sum(map(temp,others))
                count_times = map(counting,word)
                idf = map(lambda x:log(total_len/(x+1)),count_times)
                ans_vector.append(list(map(lambda x,y:x*y,tf,idf)))
            return ans_vector
        def d_cos(x,y):
            m1 = sum(map(lambda x:x**2,x))
            m2 = sum(map(lambda x:x**2,y))
            mit = sum(map(lambda x,y:x*y,x,y))
            return 0.5-0.5*mit/(m1*m2)**0.5
        def randomcenter(data,k):  #初始时随机生成类别中心
            from random import random
            n = len(data[0])
            cen = [[] for i in range(k)]
            for j in range(n):
                tempj = [item[j] for item in data]  #计算变量的取值范围
                maxj,minj = max(tempj),min(tempj)
                rangej = maxj - minj
                cen = list(map(lambda x:x + [minj+rangej*random()],cen))
            return cen
        def user_sum(x,y):
            return list(map(lambda a,b:a+b,x,y))
        def kmeans(data,k,distance = d_cos,createcenter = randomcenter,iteration = 50):   #k为类别个数
            num_iter = 0
            m = len(data) #样本个数
            clusterdata = [[0,0] for i in range(m)]  #记录数据样本所属于中心点的情况,第一列是所属中心点位置索引，第二个位置记录离中心点的距离
            cent = createcenter(data,k)   #初始化聚类中心
            clusterchange = True  #用于记录聚类情况是否改变
            while clusterchange and num_iter<=iteration: #停机条件为每个样本点的所属类别都不再改变
                clusterchange = False
                for i in range(m):
                    mindist = 99999999
                    minindex = -1
                    for j in range(k):
                        tempdist = distance(data[i],cent[j])
                        if tempdist<mindist:
                            mindist = tempdist
                            minindex = j
                    if clusterdata[i][0] != minindex:   #如果发现样本的所属类别改变了，则下一次还需要再运行算法
                        clusterchange = True
                    clusterdata[i] = [minindex,mindist**2]  #更新记录
                for j in range(k):  #更新聚类中心
                    temp = [data[i] for i in range(m) if clusterdata[i][0] == j] #选出属于这一类的样本
                    temp_len = len(temp)
                    if temp_len == 0:
                        continue
                    temp = reduce(user_sum,temp)
                    cent[j] = list(map(lambda x:x/temp_len,temp))
                num_iter += 1
            return cent,clusterdata
        def np_mean(data):
            temp_mean = reduce(user_sum,data)
            return list(map(lambda x:x/len(data),temp_mean))
        def seckmeans(data,k,distance = d_cos):
            m = len(data)
            clusterdata = [[0,0] for i in range(m)]  #记录数据样本所属于中心点的情况,第一列是所属中心点位置索引，第二个位置记录离中心点的距离,初始都属于第0类
            cent0 = np_mean(data)  #初始时假设所有样本都是一个类，计算类的中心点
            centlist = [cent0]
            for j in range(m):
                clusterdata[j][1] = distance(cent0,data[j])**2
            while len(centlist)<k:   #当不足k类时就继续
                minloss = 99999999
                for i in range(len(centlist)):
                    temp = [data[h] for h in range(m) if clusterdata[h][0] == i]
                    if len(temp) <= 1:
                        continue
                    centmat,splitclust = kmeans(temp,2)   #对于每一个类的数据进行2均值聚类
                    temploss = sum([h[1] for h in splitclust])
                    #tempotherloss = np.sum(clusterdata[np.nonzero(clusterdata[:,0] != i)[0],1])
                    tempotherloss = sum([clusterdata[h][1] for h in range(m) if clusterdata[h][0] != i])
                    if (temploss + tempotherloss)<minloss: #计算这样划分后结果的聚类误差之和
                        bestsplit = i
                        bestcents = centmat
                        minloss = temploss+tempotherloss
                        bestclusterdata = splitclust.copy()
                #bestclusterdata[np.nonzero(bestclusterdata[:,0]==0)[0],0] = bestsplit  #更新新划分出的两个类的类别，一个为原来划分类的类索引
                for i in range(len(bestclusterdata)):
                    if bestclusterdata[i][0]==0:
                        bestclusterdata[i][0] = bestsplit
                    else:
                        bestclusterdata[i][0] = len(centlist)
                #bestclusterdata[np.nonzero(bestclusterdata[:,0]==1)[0],0] = len(centlist)  #一个为原来类别数新增加出来的一个类索引
                centlist[bestsplit] = bestcents[0]   #更新类别的中心点
                centlist.append(bestcents[1])
                for i in range(m-1,-1,-1):
                    if clusterdata[i][0] == bestsplit:
                        clusterdata[i] = bestclusterdata.pop()
               # clusterdata[np.nonzero(clusterdata[:,0]==bestsplit)[0],:] = bestclusterdata
            return centlist,clusterdata
        def sse(data,cent,cluster,k,distance):
            score_l = [i[1] for i in cluster]
            ans = []
            for i in range(len(cent)-1):
                for j in range(i+1,len(cent)):
                    ans.append(distance(cent[i],cent[j]))
            #print(sum(score_l),min(ans),sum(score_l)/(min(ans)+0.1)+log(k,2.5))
            return sum(score_l)/(min(ans)+0.1)+log(k,2.5)
        def sco(data,cent,cluster,k,distance):
            ans = []
            for i in range(len(data)):
                dis = [[] for i in range(k)]
                clf_label = cluster[i][0]
                for j in range(len(data)):
                    if j == i:
                        continue
                    else:
                        dis[cluster[j][0]].append(data[j])
                dis = [sum(list(map(lambda x:distance(x,data[i]),h)))/len(h) if len(h)>0 else 999999 for h in dis]
                num_a = dis[cluster[i][0]]
                del dis[cluster[i][0]]
                num_b = min(dis)
                ans.append((num_b-num_a)/max(num_b,num_a))
            #print(-sum(ans)/len(ans)+3/exp(k))
            return -sum(ans)/len(ans)+3/exp(k)
        def choose_k(data,nowtime,model = sse,distance = d_cos,createcenter = randomcenter,iteration = 50):
            best_score = 99999999
            best_clust = None
            best_k = 0
            for k in range(2,min(13,len(data)+1)):
                cent,clusterdata = kmeans(data,k,distance,createcenter,iteration)
                #cent,clusterdata = seckmeans(data,k,distance)
                score = model(data,cent,clusterdata,k,distance)
                if score<best_score:
                    best_clust = clusterdata
                    best_score = score
                    best_k = k
                if (time.time()-nowtime)>1.95: #防止超时
                    break
            return best_clust,best_k
        import time
        starttime = time.time()
        doc = pre_proc(text)
        #doc = doc[:4]+[doc[4]+doc[5]]+doc[6:] #解决训练数据异常
        word = create_word(doc)
        imp_doc = tf_idf(doc,word)
        ans1,ans2 = choose_k(imp_doc,starttime,model = sco,distance = d_cos,createcenter = randomcenter,iteration = 50)
        res = [i[0] for i in ans1]
        #endtime = time.time()
        #print ('time:%fs'%(endtime - starttime))
        return res
