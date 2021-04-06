import requests, sys
from bs4 import BeautifulSoup
        
def get_contents(target):   # 获取章节内容
    req = requests.get(url = target)
    req.encoding = 'GB2312'
    html = req.text
    bf = BeautifulSoup(html, features = "lxml")
    texts = bf.find_all('div', id = 'content')
    texts = texts[0].text.replace('\n\n', '\n')	#去不掉多余换行？
    return texts

def writer(name, path, text):   # 写入 path
    write_flag = True
    with open(path, 'a', encoding = 'utf-8') as f:
        f.write(name + '\n')
        f.writelines(text)
        f.write('\n\n')
    
if __name__ == "__main__":
    # 获取目录
    names, urls = [], []
    req = requests.get(url = 'http://book.sbkk8.com/xiandai/liucixinzuopinji/qiuzhuangshandian')
    req.encoding = 'GB2312'
    html = req.text
    bf = BeautifulSoup(html, features = "lxml")
    content = bf.find_all('div', class_ = 'mulu')
    atmp = BeautifulSoup(str(content[0]), features = "lxml")
    a = atmp.find_all('a')	# 返回一个list
    num = len(a)

    for u in a:     # 每章名称和链接
        names.append(u.string)
        urls.append('http://book.sbkk8.com/' + u.get('href'))
 
    print("Downloading...")
    for i in range(num):
        writer(names[i], 'Ball-lightning.txt', get_contents(urls[i]))
        print("%.2f%% has been downloaded" % float(100.0*i/num), end = '\r') 
    print("100.00% has been downloaded\nFinish")