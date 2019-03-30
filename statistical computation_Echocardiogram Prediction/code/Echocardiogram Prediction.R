##PART ONE:Data Visualization and Data Preprocessing.
library(ggplot2)
library(caret)
library(rpart)
library(rpart.plot)
library(dplyr)
library(tidyr)
library(DataExplorer)
data <- read.csv("echocardiogram.csv", sep =',', na.strings = c('NA','?'))
names(data) <- c('survival','alive','age','pericardialeffusion','fractionalshortening',
                 'epss','lvdd','wallmotionscore','wallmotionindex','mult','name',
                 'group','aliveat1')

###Step One: Visualizing the data structure of the original data.
library(DataExplorer)

#Visualize data structure
str(data)

###Step Two: Visualizing the missing data value.
#Plot missing value profile
plot_missing(data)

###Step Three: Visually analyzing the original data.
data2 <- read.csv("echocardiogram(2).csv")
#Data exploration 
library(ggplot2)
attach(data2)
data2$alive <- as.factor(data2$alive)
ggplot(data2, aes( x = age, y = survival, color = factor(alive), 
                   size = age, shape = factor(alive))) + geom_point(alpha = 0.8) +
  scale_color_manual(values=c('blue','red'))
library(tidyr)
names(data2)<-c('survival','alive','age','pericardialeffusion','fractionalshortening',
                'epss','lvdd','wallmotionindex')
data2 %>% gather(pericardialeffusion:wallmotionindex, key='levels', value='value') %>% 
  ggplot( aes( x = value, fill = factor(alive), color = factor(alive)))+ 
  geom_density(alpha = 0.7) + geom_rug() +  facet_wrap( ~ levels, scales = 'free',ncol = 2)

##Data Preprocessing:Multiple Imputation
library(lattice)
library(mice)
data1<-read.csv('echocardiogram.csv',header=T)
tempData <- mice(data1,m=5,maxit=50,meth='pmm',seed=500)
write.csv(complete(tempData,1),'�岹����(2).csv')

###Step Four: Visually analyzing the interpolation data.
data<-read.csv('�岹����(1).csv',header=T)
names(data)<-c('survival','alive','age','pericardialeffusion','fractionalshortening',
               'epss','lvdd','wallmotionindex')
attach(data)
data$alive <- as.factor(data$alive)
ggplot(data, aes( x = age, y = survival, color = factor(alive), 
                  size = age, shape = factor(alive))) + geom_point(alpha = 0.8) +
  scale_color_manual(values=c('blue','red'))
library(tidyr)
names(data)<-c('survival','alive','age','pericardialeffusion','fractionalshortening',
               'epss','lvdd','wallmotionindex')
data %>% gather(pericardialeffusion:wallmotionindex, key='levels', value='value') %>% 
  ggplot( aes( x = value, fill = factor(alive), color = factor(alive)))+ 
  geom_density(alpha = 0.7) + geom_rug() +  facet_wrap( ~ levels, scales = 'free',ncol = 2)

##########LOGISTIC�ع�
DATA<-read.csv("databalance.csv",header=T)
head(DATA)
set.seed(1234)
index <-sample(1:nrow(DATA), nrow(DATA)*0.75);index
train <-DATA[index,];train
test <-DATA[-index,]
model1<-glm(aliveat1~age+pe+fs+epss+lvdd+wmi,family=binomial,data=DATA)
summary(model1)#age,pe,�ǲ�������
model12<-step(model1)
AIC(model1)-AIC(model12)
summary(model12)##ֻɾ����age,����pe��Ȼ�ǲ�������
anova(model12,model1,test='Chisq')
#p>0.05,����model.step��model1��ģ����ϳ̶�һ���á�
library(car)
influencePlot(model12,id.method="identify",main="Influence Plot",
              sub="Circle size is proportional to Cook's distance")
XX<-cor(train[3:8])
kappa(XX,exact=TRUE)##�����ڶ��ع�����
plot(model12,2)
library(lmtest)
library(zoo)
dwtest(model12)#���������
library(pROC)
p<-length(coefficients(model2));d<-dffits(model2)##DFFITS׼��
n<-length(fitted(model2))
cf<-1:n;cf[d>2*sqrt(p/n)]
library(robust)
modeltt<-glmRob(aliveat1~age+fs+epss+lvdd+wmi,family=binomial(),data=DATA,method = "cubif")
summary(modeltt)
########�������ò��Լ������Ĳ������鲢���Ǻܺã��������ģ�͵�ʱ���õ���ȫ��������
pre <- predict(modeltt,type="response")
modelroc <- roc(DATA$aliveat1,pre)
plot(modelroc, print.auc=TRUE, auc.polygon=TRUE, grid=c(0.1, 0.2),
     grid.col=c("green", "red"), max.auc.polygon=TRUE,
     auc.polygon.col="skyblue", print.thres=TRUE)
#############����������
#���ذ�
library(lattice)
library(rpart)
library(rpart.plot)
library(rattle)
library(ggplot2)
library(caret)
library(foreach)
library(iterators)
library(parallel)
library(doParallel)
library("adabag")
library("pROC")
data<-read.csv('databalance.csv',header=T)
head(data)
names(data) <- c('survival','aliveat1','age','pericardialeffusion','fractionalshortening',
                 'epss','lvdd','wallmotionindex')
data$aliveat1<-as.factor(data$aliveat1)
data$pe<-as.factor(data$pe)
#
set.seed(1234)
index <-sample(1:nrow(data), nrow(data)*0.75)
train <-data[index,];nrow(train)
test <-data[-index,];nrow(test);test
Ctl<-rpart.control(minsplit=4,maxcompete=4,maxdepth=4,cp=0.001,xval=10)
modeldt <-rpart(aliveat1 ~.-survival, data = train, method ='class', control = Ctl)

rpart.plot(modeldt)
modeldt$cptable
0.2500000+0.07128013
plotcp(modeldt)
modeldtt<-prune(modeldt,cp= 0.02272727 )
rpart.plot(modeldtt)
prediction<-predict(modeldtt, newdata =test,type="vector");prediction
modelroc <- roc(test$aliveat1,prediction)
plot(modelroc, print.auc=TRUE, auc.polygon=TRUE, grid=c(0.1, 0.2),
     grid.col=c("green", "red"), max.auc.polygon=TRUE,
     auc.polygon.col="skyblue", print.thres=TRUE)
confusionMatrix(test$aliveat1, prediction)

roc.curve(test$aliveat1, prediction)

###����������ɭ��
#-----------------------����Ԥ����---------------------------------------------------
cost01 = 1
cost10 = 10
dataproc<-read.csv("F:/��ҵ/ͳ�Ƽ������ҵ/dataproc.csv",header = TRUE,sep = ',')
data<-dataproc[(dataproc$survival>=12)|(dataproc$alive==0),]
makelabel<-function(x){
  if(x['survival']>=12){
    return(0)  #0Ϊ���ԣ����һ��
  }
  else{
    return(1) #1Ϊ����,û���һ��
  }
}
label<-apply(data,MARGIN = 1,makelabel)
data$label<-label
data$alive<-as.factor(data$alive)  #����������ӻ���
data$pe<-as.factor(data$pe)
data$label<-as.factor(data$label)
#--------------------------------------------------------------------------------------
#-------------------------��ƽ�⴦��---------------------------------------------------
library(DMwR)
databalance<-SMOTE(label~.,data,perc.over = 1500,k=2,perc.under = 125)
databalance$age<-sapply(databalance$age,function(x){floor(x)})
#--------------------------------------------------------------------------------------
#--------------------------------������֤----------------------------------------------
kcross<-function(data,model,k){
  ksplit<-function(dataset){
    n = nrow(dataset)
    ans = seq(1,n,length.out = k+1)
    ans = sapply(ans, function(x){as.integer(x)})
    return(ans)
  }
  datapos<-data[data$label==1,]
  possplit<-ksplit(datapos)
  dataneg<-data[data$label==0,]
  negsplit<-ksplit(dataneg)
  plotroc<-function(dataplot){
    library(ggplot2)
    fig = ggplot()
    cur = c(1.0,1.0) #һ��ʼ����Ӧ���������
    ysum = 0.0
    ystep<-1/nrow(dataplot[dataplot$y==1,])#y��Ϊ�����������ж�Ϊ���Եı���,1Ϊ����
    xstep<-1/nrow(dataplot[dataplot$y==0,])#x��Ϊ�����������ж�Ϊ���Եı�����0Ϊ����
    for (i in 1:nrow(dataplot)) {
      if(dataplot[i,"y"]==1){  #�Ӹ�����С��������ʼΪ���ԣ�����Ϊ����
        delx = 0
        dely = ystep
      }
      else{
        delx = xstep
        dely = 0
        ysum = ysum+cur[2] #x�ƶ��ˣ�����仯�����ϵ�ǰ����yֵ
      }
      fig = fig+geom_line(data = data.frame(x=c(cur[1],cur[1]-delx),y=c(cur[2],cur[2]-dely)),aes(x=x,y=y))
      cur<-c(cur[1]-delx,cur[2]-dely)
    }
    fig = fig+theme(plot.title = element_text(hjust = 0.5))+labs(title = 'ROC curve',x ='FP',y='TP')
    print(fig)
    print('area:')
    print(ysum*xstep)
  }
  #--------------------------------------------------BPNET-----------------------------------------------------------
  if(model == 'bpnet'){ #������
    sens = c()
    library(nnet)
    transfer<-function(datatransfer){
      #datatransfer$alive<-as.numeric(as.vector(datatransfer$alive))
      datatransfer$pe<-as.numeric(as.vector(datatransfer$pe))
      datatransfer$label<-as.numeric(as.vector(datatransfer$label))
      return(datatransfer)
    }
    classifer<-function(x){
      if(x>0.5){
        return(1)
      }
      else{
        return(0)
      }
    }
    datapos<-transfer(datapos)
    dataneg<-transfer(dataneg)
    for (i in 1:(length(possplit)-1)) {
      indexpos = possplit[i]:(possplit[i+1]-1)
      indexneg = negsplit[i]:(negsplit[i+1]-1)
      datatrain = rbind(datapos[-indexpos,],dataneg[-indexneg,])
      datatest = rbind(datapos[indexpos,],dataneg[indexneg,])
      #testposindex<-sample(1:nrow(datapos),23)  #1/3��Ϊ���Լ�
      #testnegindex<-sample(1:nrow(dataneg),23)
      #traindata<-rbind(datapos[-testposindex,],dataneg[-testnegindex,])
      #testdata<-rbind(datapos[testposindex,],dataneg[testnegindex,])
      xtrain<-datatrain[,1:6] #�������ݺ�����ǰ���У�������1:8��9
      ytrain<-datatrain[,7]
      xtest<-datatest[,1:6]
      ytest<-datatest[,7]
      netmodel<-nnet(xtrain,ytrain,size = 2,decay = 0.1,maxit = 60)
      #���������ز���Ԫ��ѧϰ��Ϊ0.1��100��epoch
      prob<-predict(netmodel,xtest)
      classf<-sapply(prob, classifer)
      dataoutput<-data.frame(p = prob,yhat = classf,y = ytest)
      dataoutput<-dataoutput[order(dataoutput$p),]
      n1 = nrow(dataoutput[(dataoutput$y==0)&(dataoutput$yhat==1),])
      n2 = nrow(dataoutput[(dataoutput$y==1)&(dataoutput$yhat==0),])
      #print(c(n1,n2))
      sens = c(sens,(n1*cost01+n2*cost10)/nrow(dataoutput)) #�������������ʧ
      if(i==(length(possplit)-1)){
        plotroc(dataoutput)
      }
    }
    return(mean(sens))
  }
  #--------------------------------------------------BPNET-----------------------------------------------------------
  error = c() #׼ȷ��
  accu = c() #���� �ж�Ϊ���Ե�����������������
  rec = c() #�ٻ��� �������Ե���������ٱ��ж���ȷ
  sens = c()
  for (i in 1:(length(possplit)-1)) {
    indexpos = possplit[i]:(possplit[i+1]-1)
    indexneg = negsplit[i]:(negsplit[i+1]-1)
    datatrain = rbind(datapos[-indexpos,],dataneg[-indexneg,])
    datatest = rbind(datapos[indexpos,],dataneg[indexneg,])
    if(model == 'rf'){ #���ɭ��
      library(randomForest)
      result = randomForest(x = datatrain[,-ncol(datatrain)],y = datatrain[,ncol(datatrain)],
                            xtest = datatest[,-ncol(datatest)],ytest = datatest[,ncol(datatest)])
      errorrate = (result$test$confusion[1,2]+result$test$confusion[2,1])/
        (result$test$confusion[1,1]+result$test$confusion[2,2]+result$test$confusion[1,2]+result$test$confusion[2,1])
      error = c(error,errorrate)
      accu = c(accu,result$test$confusion[2,2]/(result$test$confusion[1,2]+result$test$confusion[2,2]))
      rec = c(rec,result$test$confusion[2,2]/(result$test$confusion[2,1]+result$test$confusion[2,2]))
      sens = c(sens,(result$test$confusion[1,2]*cost01+result$test$confusion[2,1]*cost10)/nrow(datatest))
      #print(result$test$confusion)
      #�������������ʧ
      if (i==(length(possplit)-1)){
        model = randomForest(x = datatrain[,-ncol(datatrain)],y = datatrain[,ncol(datatrain)])
        pre = predict(model,datatest[,-ncol(datatest)])
        plotroc(data.frame(y = sort(as.numeric(as.vector(unlist(pre)))),none = sort(as.numeric(as.vector(unlist(pre))))))
        print(result$importance)
      }
    }
  }
  return(c(mean(error),mean(accu),mean(rec),mean(sens)))
}
#--------------------------------------------------------------------------------------
databalance = databalance[,-c(1,2)]
answer = kcross(databalance,'bpnet',2)

####�������
#���س����
library('survival')
library(ggplot2)
library(magrittr)
library(ggpubr)
library('survminer')
#���ݶ�ȡ��С����
setwd('E:\\��������\\ѧϰ\\�Ͽ�\\�γ�\\��һ��\\�ִ�ͳ�Ƽ���\\С����ҵ\\����')
lifetime<-read.csv('echocardiogram.csv',header=T)
lifetime<-na.omit(lifetime)
head(lifetime)
attach(lifetime)

#�¼�ʱ��ֲ�����
for(i in 1:length(alive)){
  if (alive[i] == 1){lifetime$status[i]='LIVING'}
  if (alive[i] == 0){lifetime$status[i]='DECEASED'}
}
ggplot(lifetime,       
       aes(x = survival, group = status,colour = status,           
           fill = status
       )) + geom_density(alpha = 0.5)

###�򵥵�KM�������
(fit <- survfit(Surv(survival,alive==0)~1, data = lifetime))
plot(fit)
ggsurvplot(fit,
           conf.int = TRUE,# show confidence intervals for  
           # point estimates of survival 
           risk.table = TRUE, # Add risk table
           table.pval = TRUE, # show p-value of log-rank test
           risk.table.col = "strata", # Change risk table color by groups
           linetype = "strata", # Change line type by groups
           #surv.median.line = "hv", # Specify median survival
           ggtheme = theme_bw(), # Change ggplot2 theme
           palette = c("#2E9FDF")
)
#��ͼչʾ���������ߵĹ���ֵ����������
#Kaplan-Meier����������ʾΪʵ�ߣ�95�������޶���ʾΪ����
#���Ǻ����׿���������ʱ����ӳ������˵Ĵ���ʻ�������0
ggsurvplot(fit,
           conf.int = TRUE,
           risk.table.col = "strata", # Change risk table color by groups
           ggtheme = theme_bw(), # Change ggplot2 theme
           palette = c("#2E9FDF"),
           fun = "event")
detach(lifetime)
#һЩ�о��������ڲ����ۻ����������ߣ��������������ߣ�����ʾ��������Ȥ�¼����ۻ����ʡ������ͼ�����ǿ��Թ��Ʋ�������ĳ��ʱ��������Ŀ����ԡ�

###�з����KM�������
###����������������з������������
p <- ggboxplot(lifetime, x="status", y="age", color = "status",
               palette = "jco", add = "jitter")
p+stat_compare_means(method = "t.test") 
#����pֵС��0.05��˵����ͬ������״̬�µĻ��ߵ������б�����죬���ǲ�һ����������������������ԣ�������������������
#����������飬������ͬ�������Ļ��ߵ���������
sur.cut <- surv_cutpoint(lifetime, time = "survival", event = "alive",
                         variables = c("age"))
summary(sur.cut)
sur.cat <- surv_categorize(sur.cut)
head(sur.cat)
fit1 <- survfit(Surv(survival, alive) ~age, data = sur.cat)       
ggsurvplot(fit1, data = sur.cat,  conf.int = F,pval = T,legend.title="age",
           legend.labs=c(">65","<=65"))
#��ͼ���Կ�����ͬ�������Ļ����������߲���Ǻܴ�ġ�
# ��������ӵĲ�ͬˮƽ�Ƿ����������죬����Ĭ�����ǵ�logrank test ������
survdiff(Surv(survival, alive) ~age, data = sur.cat)

#pֵС��0.05��˵����������Ч���ܺã�����ͬ�����������ʱ�����нϴ��Ӱ���

#���age�Ƿ����������ӵ�Ӱ��,��strata������Э������Ӱ��
sur.cat$epss=lifetime$epss
sur.cat$wmi=lifetime$wmi
survdiff(Surv(survival, alive) ~age+strata(epss),data = sur.cat)
survdiff(Surv(survival, alive) ~age+strata(wmi),data = sur.cat)
#����������ڿ�����������Ӱ�������£������������ʱ���Ӱ�컹�ǽϴ��

lifetime$age_group=ifelse(lifetime$age> median(lifetime$age),'high','low')
attach(lifetime)
table(status,age_group)
my.surv <- Surv(survival,status=='DECEASED')
kmfit1 <- survfit(my.surv~age_group,data = lifetime) 
plot(kmfit1,col = rainbow( 2 ))
ggsurvplot(kmfit1,conf.int =F, pval = T)
detach(lifetime)
#�ɼ���λ������һ���ܺõķ����׼

###cox�������
lifetime<-lifetime[,1:8]
res.cox<-step(coxph(Surv(survival,alive)~.,data=lifetime))
summary(res.cox)
#�ɽ�����Կ���������ÿ����һ����λ��ʹ���ߵ�����������0.085��epssÿ����һ����λ��ʹ���ߵ�����������0.047��wmiÿ����һ����λ���ǻ��ߵ�����������2.263