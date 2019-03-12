#变量顺序  "seq","url,"text"
path = 'F:/星火杯及个人总结及数模资料/国创/Data/data.csv'
rawdata<-read.csv(path,sep = ',',header = FALSE)
colnames(rawdata)=c("seq","url","text")
rawdata$url = as.character(rawdata$url)
spstr<-function(s){
  ans = strsplit(strsplit(s,split="id=")[[1]][2],split = '&ns')[[1]][1]
  return(ans)
}
temp = sapply(rawdata$url,spstr)
names(temp) = NULL
rawdata$id = temp
rawdata$text = as.character(rawdata$text)
rawdata<-rawdata[order(rawdata$id),] #原始数据集，可以用于计算时间，好评率，追加评论的综合得分
data<-rawdata[,c(1,3,4)] #lda训练数据，只包含id页和评论
x=c()  #合并评论，将一个id页看作一个文档
a=data$text[1]
j = 1
shopid = c(1)
for (i in 1:(nrow(data))){
  if (((i!=nrow(data)&data$id[i]==data$id[i+1]))){
    a=paste(a,data$text[i+1])
    shopid = append(shopid,j)
  }
  else if (i==nrow(data)){
    x=c(x,a)
  }
  else{
    x=c(x,a)
    a=data$text[i+1]
    j = j+1
    shopid = append(shopid,j)
  }

}

y=names(table(data$id))   
datanew<-as.data.frame(cbind(x,y))
doc<-as.list(datanew$x)  #转化为list
id<-as.list(datanew$y)
logit=c()   #将doc(list)中每一个元素按空格分隔为字符串向量
for (i in 1:length(doc)){
  doc[i]=strsplit(as.character(doc[[i]]),split = ' ')
}
for (i in 1:length(doc)){  #去掉不符合条件的文档
  if (length(doc[[i]])<=1){
    logit=append(logit,FALSE)
  }
  else{
    logit=append(logit,TRUE)
  }
}

doc=doc[logit]
id=id[logit]

term <- table(unlist(doc))  #统计出现过的每一个词的词频
term<-sort(term,decreasing = TRUE)
condition<- term < 3|(nchar(names(term))<2&term<600)|names(term)==""   #不符合的条件
#dele<-term[condition]
#write.csv(dele,"dele.csv") 
term<-term[!condition]   #词频

vocab<-names(term)  #计算出词库

getterm<-function(x){   #计算没一个文档词出现次数
  index<-match(x,vocab)
  index<-index[!is.na(index)]  #去掉没在词库中出现的词
  rbind(as.integer(index-1),as.integer(rep(1,length(index)))) #从0开始匹配ID
}
documents<-lapply(doc, getterm)  #对list每一个元素用一波getterm，每个元素类似于以一个文档

library(lda)
k<-5          #主题数
iter<-20000      #迭代次数
alpha<-0.1     #主题先验分布参数
beta<-0.02      #词语先验分布参数
fit<-lda.collapsed.gibbs.sampler(
  documents = documents,
  K = k,
  vocab = vocab,
  num.iterations = iter,
  alpha = alpha,
  eta = beta,
  initial = NULL,
  burnin = 0,
  compute.log.likelihood = TRUE
)

doctopmat <- t(apply(fit$document_sums + alpha, 2, function(x) x/sum(x)))  #文档—主题分布矩阵
toptermat <- t(apply(t(fit$topics) + beta, 2, function(x) x/sum(x)))  #主题-词语分布矩阵
freq <- term
for (i in 1:k){
  toptermattop=sort(toptermat[i,],decreasing = TRUE)
  print(toptermattop[1:10])}

#TF-IDF
lambda<-0.65
temp<-as.numeric(term)
pw<-temp/sum(temp)
toptermatnew=matrix(0,ncol = length(term),nrow = k)
for (i in 1:k){
  toptermatnew[i,]<-lambda*(toptermat[i,])+(1-lambda)*((toptermat[i,]/(pw))/sum(toptermat[i,]/(pw)))
}
colnames(toptermatnew)<-colnames(toptermat)
for (i in 1:k){
  x=sort(toptermatnew[i,],decreasing = TRUE)
  print(x[1:10])}