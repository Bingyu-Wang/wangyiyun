#计算当年歌曲中，歌词词频
#返回结果，词语word，词频count,比例ratio

import jieba
import math
import pandas as pd
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('chinesestopwords.txt',encoding='UTF-8').readlines()]
    return stopwords
stopwords = stopwordslist()

for i in range(1970,1975):
    year = str(i)
    print(year)
    local_main = 'wordcounts' + year +'.csv'
    file = pd.read_csv(year + '.csv',encoding='utf8')

    data = pd.DataFrame(columns = ['words','counts','ratios'])
    data.to_csv(local_main, index = None, encoding = 'utf_8_sig')
    df = pd.DataFrame(file)
    #print(df)
    counts = {}

    print("————————正在计算词频————————")
    n = len(df)
    for i in range(n):
        if i%50 == 0:
            print("\r进度：{:.2f}%".format(100*i/n),end="") 
        document = df[i:i+1]
        #print(document)
        lyric = str(document['lyric'][i]).replace(";"," ").replace("13","")
        #print(lyric)
        words = jieba.lcut(lyric)
        for word in words:
            if word.strip() not in stopwords and word !='\t' and word != '\r\n':
                counts[word] = counts.get(word, 0) + 1
    print("————————词频计算完毕————————")
    #print(counts.keys())


    print("————————正在写入数据到csv文件————————")
    total_word_counts = sum(counts.values())
    items = list(counts.items())
    items.sort(key = lambda x:x[1], reverse = True)
    #print(items)
    for i in range(len(items)):
        word = items[i][0]
        count = items[i][1]
        ratio = math.log(count / total_word_counts)
        data1 = pd.DataFrame({'words':word,
                              'counts':count,
                              'ratios':ratio},
                             columns = ['words','counts','ratios'], index=[0])
        data1.to_csv(local_main, index = None, mode = 'a', header = None, sep = ',', encoding = "utf_8_sig")
    print("————————数据写入完毕————————")   

    #看看分词频率排序情况
    '''
    for i in range(100):
        word, count = items[i]
        print("{0:<10}{1:>5}".format(word,count))
    '''

    #生成词云图
    print("————————正在生成词云图————————")
    mask = np.array(Image.open('0.png'))
    wc = wordcloud.WordCloud(font_path = "msyh.ttc",
                             mask = mask,
                             max_words = 200,
                             background_color = "white")
    wc.generate_from_frequencies(counts)
    wc.to_file("wordcloud"+year+".png")
    print("————————词云图生成完毕————————")
    #plt.imshow(wc)
    #plt.show()
    
