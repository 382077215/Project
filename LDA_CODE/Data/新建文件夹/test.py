from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

page_parameter = {"order":3,"append":0,"content":1,"tarId":"","posi":"","picture":"","ua":"094UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FQntCf0t%2BQHRMcSc%3D%7CU2xMHDJ7G2AHYg8hAS8XIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGhVbFVoXGlXY1tmUWxOdEl3SXBJc0l0SXFPckt2TWM1%7CVWldfS0SMg41CSkSMhwhd0E1WDwSRBI%3D%7CVmhIGCUFOBgkHCkXNw4xBDsbJxwhHDwINQgoFC8SLw86ATxqPA%3D%3D%7CV25OHjAePgU%2BACAcJRsgADUKMQpcCg%3D%3D%7CWGFBET9%2FK2AdYBtFAy0NMQ0zCCgULBkiAj4GOQE%2FaT8%3D%7CWWBAED4QMAsxCioWLxMuDjIKPgs3YTc%3D%7CWmNDEz0TMw8wCzERKhUqCjYMMQQ9az0%3D%7CW2JCEjwSMg4yDzYWLBc3Cz4HMwxaDA%3D%3D%7CXGREFDoUNGRYYVtmRnpBeFh5RX5LaVFxTXFPb1NnWGVFeUV4Lg4xET8RMQ4xDDcKXAo%3D%7CXWVFFTsVNWVZYFpmRnpFeFh5RX5LaVFxTXFPb1NnWGVFeUV4Lg4zEz0TMwwyCT0IXgg%3D%7CXmdHFzkXNwsyCDUVKRYtDTILNwsxZzE%3D%7CX2REFDoUNAg3CSkUNAszCjQBVwE%3D%7CQHlZCScJKR0jGDgNMxMrEikTK30r%7CQXhYCCZmMnkEeQJcGjQUIB4mBjoCOwcnHCEYIxZAFg%3D%3D%7CQntbCyULKxIqHz8DPQgxESoXIxoueC4%3D%7CQ3tbCyULK3tCek9vU21YYTcXKgokCioRLRAlGkwa%7CRH1AfV1gQH9fY1pmRnhAelpjQ39CYlZ2Q2NZeUJiXmdHe0VlW3tEe1tnR3pae0dnXQs%3D","isg":"AuDgX-rNrPVF6BDxW1_NJVmYse7QWMSzleWy9Vrwt_ueVYJ_A_heQjYnm0qv","needFold":0,"_ksTS":"1490441046713_2364","callback":"jsonp2365"}
itemId = re.compile("(?<!\w)itemId=\d*(?=\D)")
spuId = re.compile("((?<!\w)spuId=\d*|shopId=\d*)(?=\D)")
sellerId = re.compile("(?<!\w)sellerId=\d*(?=\D)")
data = pd.DataFrame([],columns=["Text","Date","Type"])
urlTool = {}
lastPage = 1
lastPagePattern = re.compile('(?<=lastPage":)\d*?(?=,"page)')
"""
每次都从\list中读取所有待搜索的页面
每次完成一个搜索就删除一个链接
在一个页面停留过久的话，就跳出。
"""



"""
readHtml——get商品页面，并依次利用temp来生成评论页面，利用find返回评论页面的text，date和type属性，最后通过write写入文件。
url_商品页面
保留问题：
1，若网络中断或者不畅通，如果记录最后一次写入地址
2，若被识别为了爬虫要如何保存最后一次写入
3，如何避免被识别为爬虫
"""        
from time import sleep
def readHtml(url):
    file = open("c:/fail","a+")
    global l
    global lastPage
    tool = []
    try:
        bsObj = BeautifulSoup(urlopen(url).read().decode("GBK"))
    except Exception as e:
        print(e)
        pass
    else:
        i = 1
        try:
            u = temp(bsObj,i)
            lastPage = int(lastPagePattern.findall(urlopen(u).read().decode("GBK"))[0])
        except Exception as ee:
            file.write(url+","+str(i)+"\n")
            print("11")
            print(ee)
            pass
        
        else:
            try:
                while i<=lastPage:
                    u = temp(bsObj,i)
                    tool.append(find(urlopen(u).read().decode("GBK")))
                    i = i+1
            except Exception as ee:
                print(ee)
                pass
            else:
                write(tool)
                l.pop()
    file.close()
        
"""
temp——读取商品页面下的信息，来合成相应的评论页面。
bsObj_商品页面的bsObj
page_评论页面数
"""
def temp(bsObj,page):
    global item
    global spu
    global seller
    
    page_parameter["currentPage"]=page
    item = itemId.findall(bsObj.__str__())[0]
    spu = spuId.findall(bsObj.__str__())[0]
    seller = sellerId.findall(bsObj.__str__())[0]
    s = "https://rate.tmall.com/list_detail_rate.htm?"
    s = s+item+"&"+spu+"&"+seller
    for key,value in page_parameter.items():
        s = s+"&"+key+"="+str(value)
    return s

textPattern = re.compile(r"(?<=rateContent\":\").*?(?=\",\"rateDate)")
datePattern = re.compile(r"(?<=rateDate\":\").*?(?=\",\"reply)")
typePattern = re.compile(r"(?<=auctionSku\":\").*?(?=\",\"auctionTitle)")


def find(s):
    return pd.DataFrame(
            [textPattern.findall(s),datePattern.findall(s),typePattern.findall(s)]
            ).T
    
    
def write(s):
    with open("C:/save.csv","a+") as f:
        for i in s:
            for j in range(0,i.shape[0]):
                f.write(l[-1][:-1]+","+i.iloc[j,0]+","+i.iloc[j,1]+","+i.iloc[j,2]+",\n")


l = []
with open("C:\list","r+") as f:
    l = f.readlines()

while len(l)!=0:
    readHtml(l[-1])
