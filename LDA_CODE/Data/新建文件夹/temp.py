# -*- coding: utf-8 -*-
import re
import urllib.request as r
import bs4 as b
source = "https://s.taobao.com/search?q=iphone7&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170326&ie=utf8&app=detailproduct&through=1&sort=sale-desc&bcoffset=0&p4ppushleft=6%2C48"
onePageSize = 44
urlPool = []

bsObj = b.BeautifulSoup(r.urlopen(source).read().decode("utf8"))
size = 13
spm1 = "spm=a230r.1.14."
spm2 = ".kdal96"   
ns="ns=1"
abbucket="abbucket=4"
idPattern = re.compile(r'(?<=auctionNids":\[).*?(?=\])')
urlHeadPattern = re.compile('(?<="detail_url":"//).*?(?=id)')
urlHeadPool = urlHeadPattern.findall(bsObj.__str__())
idPool = idPattern.findall(bsObj.__str__())[0].split(",")
for i in range(0,len(idPool)):
    urlPool.append("https://"+urlHeadPool[i]+spm1+str(3+i*8)+spm2+"&id="+idPool[i][1:-1]+"&"+ns+"&"+abbucket)

for i in range(2,size+1):
    bsObj = b.BeautifulSoup(r.urlopen(source+"&s="+str(i*44)).read().decode("utf8"))
    urlHeadPool = urlHeadPattern.findall(bsObj.__str__())
    idPool = idPattern.findall(bsObj.__str__())[0].split(",")
    for i in range(0,len(idPool)):
        urlPool.append("https://"+urlHeadPool[i]+spm1+str(3+i*8)+spm2+"&id="+idPool[i][1:-1]+"&"+ns+"&"+abbucket)
with open("C:\\list","w+") as f:
    for i in urlPool:
        f.write(i)
        f.write("\n")
