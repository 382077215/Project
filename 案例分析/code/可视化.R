multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}
#使用示例multiplot(p1,p2,p3,p4,cols=xxx)
library(ggplot2)
path = 'F:/研习部/第二次案例分析/肠道16S测序数据/'
databg = read.csv(paste0(path,'2054samples backgroud information.csv'))
databg = databg[,-((ncol(databg)-3):ncol(databg))]
databg = databg[databg$Sampled.Loci %in% c('chongqing','quanzhou'),]
databg$Gender<-as.factor(databg$Gender)
databg$Sampled.Loci<-as.factor(databg$Sampled.Loci)
#年龄分布图
p1<-ggplot(data = databg)+geom_histogram(aes(x = Age,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = Age),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#BMI
p2<-ggplot(data = databg)+geom_histogram(aes(x = BMI,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = BMI),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#性别
p3<-ggplot(data = databg)+geom_bar(aes(x = Gender),fill = 'lightblue')
#腰围
p4<-ggplot(data = databg)+geom_histogram(aes(x = Waistline,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = Waistline),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#sp
ggplot(data = databg)+geom_histogram(aes(x = SP,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = SP),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#dp
ggplot(data = databg)+geom_histogram(aes(x = DP,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = DP),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#fbg
ggplot(data = databg)+geom_histogram(aes(x = FBG,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = FBG),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#胆固醇
p5<-ggplot(data = databg)+geom_histogram(aes(x = Cholesterol,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = Cholesterol),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#甘油三酯
p6<-ggplot(data = databg)+geom_histogram(aes(x = Triglyceride,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = Triglyceride),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#ldl
ggplot(data = databg)+geom_histogram(aes(x = LDL,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = LDL),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#hdl
ggplot(data = databg)+geom_histogram(aes(x = HDL,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = HDL),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#ua
ggplot(data = databg)+geom_histogram(aes(x = UA,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = UA),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#肌酐
ggplot(data = databg)+geom_histogram(aes(x = Creatinine,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = Creatinine),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#egfr
ggplot(data = databg)+geom_histogram(aes(x = eGFR,y = ..density..),fill = 'lightblue')+
  stat_density(aes(x = eGFR),geom = 'line',position = 'identity',color = 'red',alpha = 0.8)
#位置
p6<-ggplot(data = databg)+geom_bar(aes(x = Sampled.Loci),fill = 'lightblue')
multiplot(p1,p2,cols = 2)
multiplot(p3,p6,cols = 2)
