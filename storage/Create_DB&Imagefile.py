import json
import pymysql
import pandas as pd
from PIL import Image
import urllib.request
from io import BytesIO
from pathlib import Path
from urllib import request
from moviepy.editor import *
from sqlalchemy import text, create_engine


df = pd.read_csv('DB.csv')
engine = create_engine('mysql+pymysql://bigdata:123@localhost:3306/chat')

# Create object table
ob = {}
for i in df.index:
    if pd.isna(df.iloc[i,0]):
        pass
    else:
        l = df.iloc[i,0].split(',')
        for j in l:
            j = j.replace(' ','')
            if 'jpeg' in df.iloc[i,3] or 'png' in df.iloc[i,3] or 'PNG' in df.iloc[i,3] or 'JPEG' in df.iloc[i,3]:
                if j in ob:
                    ob[j] += ',' + str(i+1) + '.jpeg'
                    
                else:
                    ob[j] = str(i+1) + '.jpeg'
                    
            elif 'jpg' in df.iloc[i,3] or 'JPG' in df.iloc[i,3]:
                if j in ob:
                    ob[j] += ',' + str(i+1) + '.jpg'

                else:
                    ob[j] = str(i+1) + '.jpg'
            elif 'gif' in df.iloc[i,3] or 'GIF' in df.iloc[i,3]:
                if j in ob:
                    ob[j] += ',' + str(i+1) + '.gif'

                else:
                    ob[j] = str(i+1) + '.gif'                
            elif 'mp4' in df.iloc[i,3] or 'MP4' in df.iloc[i,3]:
                if j in ob:
                    ob[j] += ',' + str(i+1) + '.mp4'
                else:
                    ob[j] = str(i+1) + '.mp4'
sql = """
insert into object(단어, idx)
values(
:객체명,
:jarray)
"""
for i,k in ob.items():
    객체명 = i
    jarray = k
    dt = {"객체명":객체명,"jarray":str(jarray)}
    engine.execute(text(sql),**dt)

# Create action table
ac = {}
for i in df.index:
    if pd.isna(df.iloc[i,1]):
        pass
    else:
        l = df.iloc[i,1].split(',')
        for j in l:
            j = j.replace(' ','')
            if 'jpeg' in df.iloc[i,3] or 'png' in df.iloc[i,3] or 'PNG' in df.iloc[i,3] or 'JPEG' in df.iloc[i,3]:
                if j in ac:
                    ac[j] += ',' + str(i+1) + '.jpeg'
                    
                else:
                    ac[j] = str(i+1) + '.jpeg'
                    
            elif 'jpg' in df.iloc[i,3] or 'JPG' in df.iloc[i,3]:
                if j in ac:
                    ac[j] += ',' + str(i+1) + '.jpg'

                else:
                    ac[j] = str(i+1) + '.jpg'
            elif 'gif' in df.iloc[i,3] or 'GIF' in df.iloc[i,3]:
                if j in ob:
                    ob[j] += ',' + str(i+1) + '.gif'

                else:
                    ob[j] = str(i+1) + '.gif'                
            elif 'mp4' in df.iloc[i,3] or 'MP4' in df.iloc[i,3]:
                if j in ob:
                    ob[j] += ',' + str(i+1) + '.mp4'
                else:
                    ob[j] = str(i+1) + '.mp4'
sql = """
insert into action(단어, idx)
values(
:객체명,
:jarray)
"""
for i,k in ac.items():
    객체명 = i
    jarray = k
    dt = {"객체명":객체명,"jarray":str(jarray)}
    engine.execute(text(sql),**dt)

# Create emotion table
em = {}
for i in df.index:
    if pd.isna(df.iloc[i,2]):
        pass
    else:
        l = df.iloc[i,2].split(',')
        for j in l:
            j = j.replace(' ','')
            if 'jpeg' in df.iloc[i,3] or 'png' in df.iloc[i,3] or 'PNG' in df.iloc[i,3] or 'JPEG' in df.iloc[i,3]:
                if j in em:
                    em[j] += ',' + str(i+1) + '.jpeg'
                    
                else:
                    em[j] = str(i+1) + '.jpeg'
                    
            elif 'jpg' in df.iloc[i,3] or 'JPG' in df.iloc[i,3]:
                if j in em:
                    em[j] += ',' + str(i+1) + '.jpg'

                else:
                    em[j] = str(i+1) + '.jpg'
            elif 'gif' in df.iloc[i,3] or 'GIF' in df.iloc[i,3]:
                if j in ob:
                    ob[j] += ',' + str(i+1) + '.gif'

                else:
                    ob[j] = str(i+1) + '.gif'                
            elif 'mp4' in df.iloc[i,3] or 'MP4' in df.iloc[i,3]:
                if j in ob:
                    ob[j] += ',' + str(i+1) + '.mp4'
                else:
                    ob[j] = str(i+1) + '.mp4'
sql = """
insert into emotion(단어, idx)
values(
:객체명,
:jarray)
"""
for i,k in em.items():
    객체명 = i
    jarray = k
    dt = {"객체명":객체명,"jarray":str(jarray)}
    engine.execute(text(sql),**dt)

# Create mal_main table
df = pd.read_csv('./db_mal.csv')
sql = """
insert into mal_main(URL)
values(
:URL)
"""
for i in df.index:
    URL = df.iloc[i,2]
    if 'jpeg' in df.iloc[i,2] or 'png' in df.iloc[i,2] or 'PNG' in df.iloc[i,2] or 'JPEG' in df.iloc[i,2]:
        dt = {"URL":df.iloc[i,2] +','+df.iloc[i,1]}
    elif 'jpg' in df.iloc[i,2] or 'JPG' in df.iloc[i,2]:
        dt = {"URL":df.iloc[i,2] +','+df.iloc[i,1]}
    elif 'gif' in df.iloc[i,2] or 'GIF' in df.iloc[i,2] or 'mp4' in df.iloc[i,2] or 'MP4' in df.iloc[i,2]:
        dt = {"URL":df.iloc[i,2] +','+df.iloc[i,1]}
    engine.execute(text(sql),**dt)

# Create mal table
mal = {}
for i in df.index:

    if 'jpeg' in df.iloc[i,2] or 'png' in df.iloc[i,2] or 'PNG' in df.iloc[i,2] or 'JPEG' in df.iloc[i,2]:
        if df.iloc[i,0] in mal:
            mal[df.iloc[i,0]] += ','+df.iloc[i,2]
        else:
            mal[df.iloc[i,0]] = df.iloc[i,2] + '.jpeg'
            
    elif 'jpg' in df.iloc[i,2] or 'JPG' in df.iloc[i,2]:
        if df.iloc[i,0] in mal:
            mal[df.iloc[i,0]] += ','+df.iloc[i,2]
        else:
            mal[df.iloc[i,0]] = df.iloc[i,2]
            
    elif 'gif' in df.iloc[i,2] or 'GIF' in df.iloc[i,2]:
        if df.iloc[i,0] in mal:
            mal[df.iloc[i,0]] += ','+df.iloc[i,2]
        else:
            mal[df.iloc[i,0]] = df.iloc[i,2]
    
sql = """
insert into mal(단어, idx)
values(
:객체명,
:jarray)
"""
for i,k in mal.items():
    객체명 = i
    jarray = k
    dt = {"객체명":객체명,"jarray":str(jarray)}
    engine.execute(text(sql),**dt)


# Download Image from Web

df = pd.read_csv('db3.csv')
for idx, url in enumerate(df.iloc[:,3]):
    if 'gif' in url or 'GIF'in url:
        urllib.request.urlretrieve(url, 'Img/' + str(idx+1)+'.gif')

    elif 'png' in url or 'PNG' in url:
        res = request.urlopen(url).read()
        tmp = Image.open(BytesIO(res)).convert('RGB')
        tmp.save(f'Img/{idx+1}.jpeg','jpeg')

    elif 'jpeg' in url or 'JPEG' in url:
        urllib.request.urlretrieve(url, 'Img/' + str(idx+1)+'.jpeg')

    elif 'jpg' in url or 'JPG' in url:
        urllib.request.urlretrieve(url, 'Img/' + str(idx+1)+'.jpg')
    
    elif 'mp4' in url or 'MP4' in url:
        file_name = f'Img/{idx+1}.mp4' 
        urllib.request.urlretrieve(url, file_name)


# 1Mb 초과시, resize 시킨 후 저장(텔레그램 API의 Limit_size)
k = []
for i in df.index:
    URL = df.iloc[i,3]
    if 'jpeg' in df.iloc[i,3] or 'png' in df.iloc[i,3] or 'JPEG' in df.iloc[i,3] or 'PNG' in df.iloc[i,3]:
        file_size = Path(f'Img/{i+1}.jpeg').stat().st_size
        if file_size >= 1048576:
            k.append(str(i+1)+'.jpeg')
    elif 'jpg' in df.iloc[i,3] or 'JPG' in df.iloc[i,3]:
        file_size = Path(f'Img/{i+1}.jpg').stat().st_size
        if file_size >= 1048576:
            k.append(str(i+1)+'.jpg')
    elif 'gif' in df.iloc[i,3] or 'GIF' in df.iloc[i,3]:
        file_size = Path(f'Img/{i+1}.gif').stat().st_size
        if file_size >= 1048576:
            k.append(str(i+1)+'.gif')
path = 'Img/'
for i in k:
    image = Image.open(f'Img/{i}')
    resize = image.resize((328,256))
    resize.save(f'Img/{i}','gif',quality=95)