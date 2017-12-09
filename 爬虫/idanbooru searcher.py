import requests
import re
from bs4 import BeautifulSoup
import os

    

def makepath():
    mkpath=input('请输入要创建的目录,示例d:\\picture，若回车默认存储在d:\\picture下')  
    if mkpath=='':
        path='d:\\picture'
    else:
        path=mkpath

    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs (path)
        print(path+'创建成功')
    else:
        print(path+'目录已存在')
    os.chdir(path)      #切换默认工作目录为创建的目录
#创建目录，默认为D盘的picture        
def getHtmlText(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return ""
#获取网站代码
def getHtmlBin(url):
    try:
        r=requests.get(url)
        r.raise_for_status()        
        return r.content
    except:
        return []
#获取图片数据
def savePic(img,filename):
    try:
        f=open(filename,'wb')
        f.write(img)
        f.close()        
    except:
        print("error")    
#保存图片

def kind(defaultkind):
    url0='http://www.idanbooru.com/posts?page={}&tags={}'
    if defaultkind=='1':
        kind='scenery'
    elif defaultkind=='2':
        kind='science_fiction'
    elif defaultkind=='3':
        kind='cityscape'
    else:
        kind=defaultkind
    url2=url0.format(page,kind) 
    return url2
#图的种类和页数判断与输入
def getdetailpost(i):
    url2=kind(defaultkind)
    bdText1=getHtmlText(url2)
    bs1=BeautifulSoup(bdText1,'html.parser')
    result1=bs1.find_all(href=re.compile('/posts/\d+'))
    m=result1[i]
    r1=re.findall('posts/2\d+',str(m),re.S)
    print(r1)
    m1=r1[0]
    src1='http://www.idanbooru.com/'+m1
    return src1
#获取关键字分类下网页中各缩略图的实际图片链接


def downpicture():
    for i in range(0,20):
        src1=getdetailpost(i)
        bianhao=re.findall(re.compile('\d+'),src1)
        bh=bianhao[0]
        bdText=getHtmlText(src1)
        bs=BeautifulSoup(bdText,'html.parser')  #找到了图所在网页，开始下载图片
        print('即将开始下载图片,嘀嘀嘀')
        try:
            result=bs.select('#image-resize-link')
            r=result[0]
            src=r.attrs['href']
            print(src)
            ext='http://www.idanbooru.com'+src
            print(ext)
            hz=re.findall(re.compile('.+\.(.+)'),ext)
            img=getHtmlBin(ext)
            file='{}.{}'.format(bh,hz[0])
            print(file)
            print('已找到高清图，正在下载，请稍等')
            savePic(img,file)
            print('下载完毕')
            #先尝试获取大图，若没有转而获取小图
        except:
            print('找不到高清图呢，开始获取原图')
            result=bs.select('#image')
            r=result[0]
            src=r.attrs['src']
            print(src)
            ext='http://www.idanbooru.com'+src
            hz=re.findall(re.compile('.+\.(.+)'),ext)
            img=getHtmlBin(ext)
            file='{}.{}'.format(bh,hz[0])
            print(file)
            print('已获取到源地址，正在下载，请稍候')
            savePic(img,file)
            print('下载完毕')

 
makepath()#创建目录

defaultkind=input('请输入你需要的图片的类别，提供默认实例1，2，3 for 风景，科技幻想，城市风景，输入关键字则可获取其他关键字的图片')
page=input('请选择你要下载的页数，20指下载第20页的')
#由用户输入获取页数和图的类型
downpicture()




