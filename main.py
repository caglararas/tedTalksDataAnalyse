from re import X
from pandas.core.computation.common import result_type_many
from pandas.core.groupby.generic import DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ----------------------------------------------------------------------------------------

data = pd.read_csv("ted_talks.csv")

# -----------------------------------------------------------------------------------------
df = pd.DataFrame(data)
# ----------------------------------------------------------------------------------------

# boş veri sorgulama ve kaldırma

null_value = df[df.isna().any(axis=1)]
null_value
df.dropna(inplace=True)

# ----------------------------------------------------------------------------------------

# tip belirlemesi

tip=df.dtypes
data.info()
data.isna().sum()

----------------------------------------------------------------------------------------

# sorgu1
# en çok beğeni alan ilk 20 konuşmacı ve beğeni sayısı

sirala=df[["speaker","likes"]].sort_values(by=['likes'], ascending=False).reset_index().head(20)
print(sirala)

----------------------------------------------------------------------------------------

#sorgu2
#en popüler 20 etkinlik

result=df.groupby("event")["views"]
result=df.groupby('event').views.agg(['count', 'sum']).sort_values(by='sum', ascending=False).head(20)
print(result)

# ----------------------------------------------------------------------------------------

#sorgu3
#en fazla konuşma yapan ilk 10 konuşmacı

konus=df["speaker"].value_counts().sort_values(ascending=False).head(10)
print(konus)

----------------------------------------------------------------------------------------

# sorgu4
# en çok konuşma yapılan ilk 20 etkinlik

result3=df["event"].value_counts().head(20)
print(result3)

----------------------------------------------------------------------------------------

#sorgu5
# konuşmacıların konuşmalarının beğenilme oranı

df['oran']=df['views']/df['likes']
result=df[["speaker","oran"]].sort_values(by=['oran'], ascending=False).head(20)
print(result)

----------------------------------------------------------------------------------------

#sorgu6
# konuşma süresi en fazla olan ilk 20 konuşmacı

df['duration']=df['duration']/60   #sürenin dakikaya çevrilmesi
result=df[["speaker","duration"]].sort_values(by=['duration'],ascending=False).head(20)
print(result)

----------------------------------------------------------------------------------------

# sorgu7
# TED-ed de en uzun konuşmayı yapan ilk 5 konuşmacı

result= df[df["event"]=="TED-Ed"].sort_values(by = ["duration"], ascending = False).head(5)
print(result)

----------------------------------------------------------------------------------------

# sorgu8
# 2010 ve 2015 arası en çok görüntüleme alan ilk 5 konuşmacı

df['published_date'] = pd.to_datetime(df['published_date']) #datetime'a dönüştürme
df['years']=df['published_date'].dt.year
result= df[(df["years"]<=2015) & (df["years"]>=2010)].sort_values(by = ["views"], ascending = False).head(5)
print(result)


----------------------------------------------------------------------------------------

# sorgu9
# en kısa süren 5 etkinlik ve konuşmacısı

result= df[["speaker","event","duration"]].sort_values(by = ["duration"], ascending = True).head(5)
print(result)

----------------------------------------------------------------------------------------

# sorgu10
# 2020 ve 2022 arası en çok konuşma yapan 3 konuşmacı

df['recorded_date'] = pd.to_datetime(df['recorded_date']) #datetime'a dönüştürme
df['years']=df['recorded_date'].dt.year
result= df[(df["years"]<=2022) & (df["years"]>=2020)]["speaker"].value_counts().head(3)
print(result)

----------------------------------------------------------------------------------------

# görselleştirme1
# en çok konuşma yapılan etkinlik ,konuşma sayısı ve grafiği.

events = pd.DataFrame(df['event'].value_counts()).sort_values('event', ascending=False).reset_index().head(20)
fig = px.bar(events,
             x ='index',
             y='event',
             color = 'index',
             color_continuous_scale = px.colors.sequential.Oryel,
             title='En çok konuşma yapılan etkinlik ,konuşma sayısı ve grafiği')

fig.show()

----------------------------------------------------------------------------------------

# görselleştirme2
#En Uzun 10 Konuşma

df['duration']=df['duration']/60
duration = df.sort_values(by = 'duration', ascending = False).head(10)
fig = px.bar(duration,
             x ='speaker',
             y='duration',
             color = 'views',
             color_continuous_scale = px.colors.sequential.Oryel,
             title='Konuşma süresi en fazla olan ilk 10 konuşmacı ve süreleri.')
fig.show()

----------------------------------------------------------------------------------------

# görselleştirme3
# En iyi 20 konuşmacı ve görüntüleme sayıları

talk_views = df[['speaker', 'views']]
konusma_sirali = talk_views.sort_values('views', ascending=False)
top_20 = konusma_sirali.head(20)
ax = plt.subplots(figsize=(15,10))
ax = sns.barplot(x='views', y='speaker', data= top_20, palette='Reds_r')
plt.xlabel('views',fontsize = 15,color='black')
plt.ylabel('speaker',fontsize = 15,color='black')
plt.title("En iyi 20 konuşmacı ve görüntüleme sayıları.")

-----------------------------------------------------------------------------------------

#görselleştirme4
#yıllara göre konuşma sayıları grafiği

df['published_date'] = pd.to_datetime(df['published_date']) #datetime'a dönüştürme
df['years']=df['published_date'].dt.year #years adında yeni sütun oluşturma
df.years.value_counts()
fig, ax = plt.subplots(figsize=(15,5))
sns.countplot(df['years'])

----------------------------------------------------------------------------------------

#görselleştirme5
#en çok konuşma yapan insanın yıllara göre konuşma sayısı

 plt.title("Yıllara göre konuşma sayısı")
 plt.xlabel("Yıllar")
 plt.ylabel("Konuşma sayısı")
 df1=df[df["speaker"]=="Alex Gendler"]["years"].value_counts().plot.bar(color="g")

-----------------------------------------------------------------------------------------

#görselleştirme6
#en iyi 5 konuşma başlığının görüntülenme grafiği

best_talk=df.groupby('title')['views'].sum().reset_index().sort_values(by='views',ascending=False)
plt.figure(figsize=(20,4))
sns.barplot(x='title',y='views',data=best_talk.head(5))

----------------------------------------------------------------------------------------

#görselleştirme7
#en çok görüntülenen ilk 10 konuşmacıya göre başlıkların grafiği

x=pd.DataFrame(df.groupby('speaker')['views'].sum()).reset_index().sort_values(by='views',ascending=False)
fav_speaker=x[x['views']==x['views'].max()]['speaker'].values[0]
fav_speaker_data=df[df['speaker']==fav_speaker]
result=pd.DataFrame(fav_speaker_data[['title','views']].groupby('title').sum()).reset_index().sort_values(by=['views'],ascending=False)
result.head()
plt.figure(figsize=(10,5))
sns.barplot(x='views',y='title',data=result.head(10))

----------------------------------------------------------------------------------------

#görselleştirme8
#en çok beğeni alan ilk 10 konuşmacıya göre başlıkların grafiği

y=pd.DataFrame(df.groupby('speaker')['likes'].sum()).reset_index().sort_values(by='likes',ascending=False)
fav_speaker=y[y['likes']==y['likes'].max()]['speaker'].values[0]
fav_speaker_data=df[df['speaker']==fav_speaker]
result=pd.DataFrame(fav_speaker_data[['title','likes']].groupby('title').sum()).reset_index().sort_values(by=['likes'],ascending=False)
result.head()
plt.figure(figsize=(10,5))
sns.barplot(x='likes',y='title',data=result.head(10))

----------------------------------------------------------------------------------------

#görselleştirme9
#görüntülenme sayılarına göre ilk 20 konuşmacının grafiği

pop_talks = df[['title', 'speaker', 'views', 'published_date']].sort_values('views', ascending=False)[:20]
pop_talks['name'] = pop_talks['speaker'].apply(lambda x: x[:3])
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.barplot(x='name', y='views', data=pop_talks)

----------------------------------------------------------------------------------------

#görselleştirme10
#En iyi 10 konuşmanın izlenme sayısı ve beğeni sayısı

views = df.sort_values(by = 'views', ascending = False).head(10).reset_index()
fig = px.bar_polar(views,
                   r="likes",
                   theta="title",
                   color="views",
                   color_discrete_sequence= px.colors.sequential.Plasma_r,
                   title="En iyi 10 konuşmanın izlenme sayısı ve beğeni sayısı"
                  )
fig.show()

----------------------------------------------------------------------------------------
