#歌词情感分析
#调用百度情感分析API计算

'''
sentiment	int	表示情感极性分类结果，0:负向，1:中性，2:正向
confidence	float	表示分类的置信度，取值范围[0,1]
'''

import urllib3
import json
import time
import pandas as pd
import numpy as np
import os


local_main2 = r'test.csv'
data = pd.DataFrame(columns = ['music_id', 'music_title', 'lyric', 'labels','label_prediction'])
data.to_csv(local_main2, index = None, encoding = 'utf_8_sig')

access_token='改成填自己的access_token'
http=urllib3.PoolManager()
url='https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token='+access_token

file = pd.read_csv('lyr.csv')
df = pd.DataFrame(file)
#print(df)

labels =[]
label_prediction =[]

for i in range(len(df)):
    document = df[i:i+1]
    music_id = document['music_id'][i]
    music_title = document['music_title'][i]
    lyric = document['lyric'][i]
    #print(music_id,'\n',music_title,'\n',lyric)
    if (i+1)%5==0:
        time.sleep(1)
    if lyric =='\n':
        lyric = 'NA'
    params = {'text':lyric}

    encoded_data = json.dumps(params).encode('GBK')
    request=http.request('POST', 
                          url,
                          body=encoded_data,
                          headers={'Content-Type':'application/json'})
    result = str(request.data,'GBK')
    a =json.loads(result)
    a1 =a['items'][0]
    labels.append(a1['sentiment'])#分类结果
    label_prediction.append(a1['positive_prob'])#展示的概率

    data1 = pd.DataFrame({'music_id':music_id,
                          'music_title':music_title,
                          'lyric':lyric, 
                          'labels':labels[i],  
                          'label_prediction':label_prediction[i]}, columns = ['music_id','music_title','lyric', 'labels', 'label_prediction'], index=[0])
    data1.to_csv(local_main2, index = None, mode = 'a', header = None, sep = ',', encoding = "utf_8_sig")

