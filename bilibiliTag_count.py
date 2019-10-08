import requests
from bs4 import BeautifulSoup
#from selenium import webdriver
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib

#写入文件
def write_file(list,fp):
    # 将result这个json格式的对象转化为字符串
    s = json.dumps(list,ensure_ascii=False)
    # 写入文件
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(s)


#读取json文件
def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        s = f.read()
    data = json.loads(s)
    return data


#开始请求
def start_requests(url):
    #显示正在爬取的URL
    print("当前正在爬取"+url)
    data = requests.get(url)
    return data.text
    #selenium操作
    '''
    driver.get(url)
    #设定爬取时间
    #driver.set_page_load_timeout(30)
    #抓取到的信息
    data = driver.page_source
    time.sleep(5)
    driver.quit()
    print(data)
    return data
    '''

def parse_search(text):
    html = text
    # html.parser 用于解析
    soup = BeautifulSoup(html, 'html.parser')
    movie_list = soup.find_all('li', class_='video-item matrix')
    for movie in movie_list:
        mydict = {}
        mydict['aid'] = movie.find('span', class_='type avid').text.replace('av','')
        mydict['title'] = movie.find('a', class_='title').text
        mydict['description'] = movie.find('div', class_='des hide').text.strip('\n').strip(' ').strip('\n')
        #删除前后的换行和空格
        mydict['view'] = movie.find('span', class_='so-icon watch-num').text.strip('\n').strip(' ').strip('\n')
        mydict['danmu'] = movie.find('span', class_='so-icon hide').text.strip('\n').strip(' ').strip('\n')
        mydict['author'] = movie.find('a', class_='up-name').text
        #star = movie.find('div', class_='star')
        #mydict['comment_num'] = star.find_all('span')[-1].text[:-3]
        # 存入result_list中，方便导入文件
        result_list.append(mydict)
        print(mydict)

#解析网页源代码
def parse(text):
    #将获得的文本转化为文本
    temp_data = json.loads(text)
    data = temp_data['data']
    #获取到了data中的内容
    return data
    #使用selenium对Json进行处理
    '''html = text
    # html.parser 用于解析
    soup = BeautifulSoup(html, 'lxml')
    #digital_list = soup.find_all('div', id_='bili_technology')
    #print(digital_list)
    #print("ready?")
    #for digital in digital_list:
    movie_list = soup.find_all('div', class_='con')
    for movie in movie_list:
            mydict = {}
            mydict['title'] = movie.find('p',class_='text').text
            # 存入result_list中，方便导入文件
            result_list.append(mydict)
    print(result_list)'''
#解析单个视频的信息

#数据清洗
def data_wash(result):
    i = 0
    print(result.size)

    for i in range(0,result.size):
        re = {}
        re['tag_name']=result.index[i]
        re['count']=result.values[i]
        re=str(re)
        count_list.append(re)


#TAG数据清洗
def tag_wash(temp_data):
    for data in temp_data:
        datas = {}
        datas['tag_name'] = data['tag_name']
        tag_list.append(datas)
        print(datas)

def tag_anly(data):
    # 使用pandas构造数据
    df = pd.DataFrame(data)
    result=df['tag_name'].value_counts()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel('TAG',fontsize=10)
    plt.ylabel('频数',fontsize=10)
    result.plot.bar()
    plt.show()
    return result



def main():
    #爬取前200名的信息并进行处理（1到5页）
    for i in range(0,page):
        url = 'https://search.bilibili.com/all?keyword=%E9%AC%BC%E7%95%9C&from_source=banner_search&order=click&duration=0&tids_1=0&page={}'.format(i)
        r = start_requests(url)
        data=parse_search(r)
        #data_wash(data)
    #根据排行榜的信息爬取单个视频的TAG
    for result in result_list:
        url = 'https://api.bilibili.com/x/tag/archive/tags?aid={}'.format(result['aid'])
        r = start_requests(url)
        data = parse(r)
        tag_wash(data)
    write_file(result_list,fp)
    read_file(fp)
    write_file(tag_list,tag_fp)
    data = read_file(tag_fp)
    result = tag_anly(data)
    data_wash(result)
    write_file(count_list,count_fp)

if __name__ == "__main__":
    #全局变量
    result_list=[]
    tag_list=[]
    count_list = []
    page = 30
    fp = 'guichu_ranking.json'
    tag_fp = 'tag.json'
    count_fp='tag_count.json'
    #driver = webdriver.Chrome()
    main()
