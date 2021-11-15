import pandas as pd
import numpy as np

#2019, 2020 전처리 함수
def preprocessing(data, year):
    j = 12
    for i in range(3, 15, 1):
        if j < 10:
            data['Unnamed: 1'][i] = year + '-' + '0' + str(j)
        else:
            data['Unnamed: 1'][i] = year + '-' + str(j)
        j = j - 1
    data = data.drop([0, 1, 2])
    data = data.rename(columns = {'Unnamed: 1': 'y-m', 'Unnamed: 2' : '수출액(천불)', 'Unnamed: 3' : '수출증감률', 'Unnamed: 4' : '수입액(천불)', 'Unnamed: 5' : '수입증감률', 'Unnamed: 6' : '수지'})
    data = data.drop('K-stat 총괄 ', axis = 1)
    data = data[::-1]
    data = data.reset_index(drop=True)
    
    return data

#2002~2020 까지 데이터 전부 합치기
trade_all = pd.DataFrame()
for i in range(2002, 2020, 1):
    data_path = './data/japan_' + str(i) + '.xls'
    temp_df = pd.read_excel(data_path)
    temp_df = preprocessing(temp_df, str(i))

    trade_all= pd.concat([trade_all, temp_df])


#확진자 데이터 전처리
confirmed = pd.read_excel('./data/data.xlsx')

df_confirmed = confirmed.T
df_confirmed = df_confirmed.reset_index()

df_confirmed = df_confirmed.rename(columns = df_confirmed.loc[0])
df_confirmed = df_confirmed.rename(columns = {'Unnamed: 0':'y-m'})
df_confirmed = df_confirmed.drop(0)

df_confirmed['y-m'] = df_confirmed['y-m'].astype(str)
df_confirmed['y-m'] = df_confirmed['y-m'].str[0:7]
df_confirmed.reset_index(drop = True)

df_confirmed
trade_all
#확진자 데이터와 무역 데이터 합치기
#trade_all = pd.concat([df_2019, df_2020, df_2021])
trade_all = trade_all.reset_index(drop=True)
trade_all
trade_confirmed = pd.merge(trade_all, df_confirmed, how='outer', on='y-m')

trade_confirmed.to_excel(excel_writer='./union.xlsx')

trade_confirmed = trade_confirmed.fillna("0")

trade_confirmed
trade_confirmed = trade_confirmed.astype({'수출액(천불)' : 'float','수출증감률' : 'float','수입액(천불)' : 'float','수입증감률' : 'float','수지' : 'float','확진자수평균' : 'float','누적확진자수' : 'float'})


corr = trade_confirmed.corr(method="spearman")
corr


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12,12))
sns.heatmap(corr, linewidths=0.1, vmax = 0.5, cmap=plt.cm.gist_heat, linecolor='white', annot=True)
plt.show()


japan_all = trade_confirmed.copy()

mean_sales = int(np.mean(japan_all['수출액(천불)']))


fig = plt.figure(figsize=(30,20))
ax = fig.add_subplot()


ax.spines['right'].set_visible(False) ## 오른쪽 축 숨김
ax.spines['top'].set_visible(False) ## 위쪽 축 숨김

s1 = [japan_all['y-m'],japan_all['수출액(천불)']] #데이터 인자 

config_plot = dict( ##키워드 인자 
                   color = 'red', # 색
                   linestyle = 'solid', # 스타일
                   linewidth = 2) # 선 두깨

ax.plot(label = '수출액(천불)', *s1,**config_plot)
ax.axhline(mean_sales, label = '수출액 평균 값') # 평균값 y 좌표로 하는 수평선 생성
ylim = ax.get_ylim() ## 기존의 y축 범위 지정
yticks = list(ax.get_yticks())
yticks.append(mean_sales)
yticks = sorted(yticks)

ax.set_yticks(yticks) # 평균이 포함된 y 눈금으로 새롭게 세팅한다.
ax.set_ylim(ylim) ## 기존의 y축 범위를 유지 

#ax.plot(seeq1_s1['y-m'],seeq1_s1['수출액(천불)'],color = '#c02ad1')
#plt.xticks(rotation=45)
ax.legend(loc = 'upper left', fontsize = 15)
plt.xticks(rotation = 45 )# 기울기
plt.title('수출그래프')
plt.show()