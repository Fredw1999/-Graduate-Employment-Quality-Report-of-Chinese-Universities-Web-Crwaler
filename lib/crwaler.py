import urllib.request
from lxml import etree
import pandas as pd
import requests
from urllib import parse
import chardet
import urllib
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl

s = requests.session()
s.keep_alive = False

ssl._create_default_https_context = ssl._create_unverified_context

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)
 
 
if __name__ == '__main__':
    s = requests.Session()
    s.mount('https://', MyAdapter())
    
header={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
ssl._create_default_https_context = ssl._create_unverified_context

site='https://www.ncss.cn/tbch/2020jyzlbg/'
content = urllib.request.urlopen(site).read().decode('utf-8')
data = etree.HTML(content)
allurl= data.xpath('//div[@class="box"]//div[@class="right-r clearfix"]/ul/li/a/@href')
name=data.xpath('//div[@class="right-r clearfix"]/ul/li/a/text()')
kxx=[]
xz=[]
urlslist=[]
fwwt=[]
n=0


sccs=5
sfkx=0
wt=0

def isfile(url):
    if url.endswith('.pdf'):
        return True
    else:
        
        return False

def downloadfile(url):
    global sccs
    dldurl=url
    filename = name[n]+'2020年就业质量报告'
    try:
        urllib.request.urlretrieve(dldurl,filename)
        print(dldurl+"成功下载")
        sccs=1
    except Exception as e:   
        print('未下载原因')
        print(e)
        sccs=0
    return sccs
    
def geturl(url):
    global wt
    newsite=url
    '''data1 = urllib.request.urlopen(newsite).read()
    chardit1 = chardet.detect(data1)'''
    try:
        result = etree.HTML(requests.get(newsite).content)
        newdata=result
        newurlhref=newdata.xpath('//*[contains(@href,".pdf")]/@href')
        newurlsrc=newdata.xpath('//*[contains(@src,".pdf")]/@src')
        newurldoc=newdata.xpath('//*[contains(@href,".doc")]/@href')
        newurldldhref=newdata.xpath('//*[contains(@href,"download")]/@href')
        newurldldsrc=newdata.xpath('//*[contains(@src,"download")]/@src')
        newurl=newurlhref+newurlsrc+newurldoc+newurldldhref+newurldldsrc
        wt=0
    except Exception as e:
        newurl=[]
        print("访问问题")
        print(e)
        wt=1

    return newurl

for i in allurl:
    print(n)
    sccs=5
    try:
        b=urllib.request.urlopen(i)
    except Exception as e:
        print(i+"       no")
        print('原因')
        print(e)
        sccs=0
        sfkx=0

    else:
        sfkx=1
        print(i+"      yes")
        if isfile(i):
            downloadfile(i)
        else:
            newurl=geturl(i)
            if newurl==[]:

                    sccs=0
                    print('未找到文件')
            else:
                path=newurl[0]
                newurls=parse.urljoin(i,path,allow_fragments=True)
                downloadfile(newurls)
                
    

    xz.append(sccs)
    kxx.append(sfkx)
    fwwt.append(wt)
    print(fwwt)
    print(xz)
    print(kxx)
    n=n+1
    
        
df=pd.DataFrame({"name":name,"link":allurl,"是否失效":kxx,"是否下载":xz})
df.to_excel('1st_try.xlsx')

