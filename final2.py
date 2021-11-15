import pandas as pd
import random
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc


font_name = font_manager.FontProperties(fname="C:\Windows\Fonts\gulim.ttc").get_name()
rc('font', family=font_name)


#연도별 데이터 전처리 함수
def preprocessing(data):
    resultData =  data.copy()
    j = 12
    
    for i in range(3, len(resultData['Unnamed: 1']), 1):
        if int(resultData['Unnamed: 1'].values[i][:-1]) < 10 and len(resultData['Unnamed: 1'].values[i][:-1]) < 2 :
            temp = resultData.loc[0][0].find('년도') + 5
            resultData['Unnamed: 1'][i] = resultData.loc[0][0][temp:temp+4] + '-' + '0' + resultData['Unnamed: 1'].values[i][:-1]
        else:
            temp = resultData.loc[0][0].find('년도') + 5
            resultData['Unnamed: 1'][i] = resultData.loc[0][0][temp:temp+4] + '-' + resultData['Unnamed: 1'].values[i][:-1]

    resultData = resultData.drop([0, 1, 2])
    resultData = resultData.rename(columns = {'Unnamed: 1': 'y-m', 'Unnamed: 2' : '수출액(천불)', 'Unnamed: 3' : '수출증감률', 'Unnamed: 4' : '수입액(천불)', 'Unnamed: 5' : '수입증감률', 'Unnamed: 6' : '수지'})
    
    resultData = resultData.drop('K-stat 총괄 ', axis = 1)
    resultData = resultData[::-1]
    resultData = resultData.reset_index(drop=True)
    
    return resultData

#폴더안에 있는 데이터 전부 합치기
def mergeDataInFolder(dataPath):
    import os
    fileList = os.listdir(dataPath)
    
    result = pd.DataFrame()
    for i in fileList:
        tempDf = pd.read_excel(dataPath + i)
        tempDf = preprocessing(tempDf)

        result = pd.concat([result, tempDf])
    
    result = result.sort_values(by=['y-m'])
    return result

#원하는 데이터와 코로나 데이터 합치기
def mergeConfirmed(tradeData):
    result = tradeData.copy()
    result = pd.merge(result, df_confirmed, how='outer', on='y-m')
    result = result.astype({'수출액(천불)':'float', '수출증감률':'float', '수입액(천불)':'float', '수입증감률':'float', '수지':'float', '확진자수평균':'float', '누적확진자수':'float'})
    return result

#확진자 데이터 가져오기 #전역변수로 만들기?
def confirmedData():
    global df_confirmed
    confirmed = pd.read_excel('./data/국가별누적데이터.xlsx')
    df_confirmed = confirmed.copy()
    
    df_confirmed = df_confirmed.T
    df_confirmed = df_confirmed.reset_index()

    df_confirmed = df_confirmed.rename(columns = df_confirmed.loc[0])
    df_confirmed = df_confirmed.rename(columns = {'Unnamed: 0':'y-m'})
    df_confirmed = df_confirmed.drop(0)
    df_confirmed['y-m'] = df_confirmed['y-m'].astype(str)
    df_confirmed['y-m'] = df_confirmed['y-m'].str[0:7]
    df_confirmed.reset_index(drop = True)

#원하는 날짜별로 데이터 짜르기
#data는 confirmedData()의 리턴값
def devideDate(data, *date2):
    year = []
    month = []
    temp = []
    
    for date in date2:
        if len(date) > 4:            
            year.append(date[0:4])
            month.append(date[5:7])
        else:
            year.append(date[0:5])
            month.append('01')

    for i in range(len(date2)):
        temp.append(data[data['y-m'] == year[i] + '-' + month[i]].index[0])
    
    if len(date2) > 1:
        return data.iloc[temp[0]:temp[1] + 1]
    else:
        return data.iloc[temp[0]:]


#데이터 로드 확진자
confirmedData()

#국가별 상관관계 보기
#대한민국
korPath = './data/korea/'
df_korea = mergeDataInFolder(korPath)
trade_confiremd_korea = mergeConfirmed(df_korea)
trade_confiremd_korea.corr()

devideDate(trade_confiremd_korea, '2010', '2019-01')
devideDate(trade_confiremd_korea, '2010')
devideDate(trade_confiremd_korea, '2019-01')
devideDate(trade_confiremd_korea, '2010-05', '2019-07')

korea17 = devideDate(trade_confiremd_korea, '2017', '2017-07')['수출액(천불)'].reset_index(drop=True)
korea18 = devideDate(trade_confiremd_korea, '2018', '2018-07')['수출액(천불)'].reset_index(drop=True)
korea19 = devideDate(trade_confiremd_korea, '2019', '2019-07')['수출액(천불)'].reset_index(drop=True)
korea20 = devideDate(trade_confiremd_korea, '2020', '2020-07')['수출액(천불)'].reset_index(drop=True)
korea21 = devideDate(trade_confiremd_korea, '2021', '2021-07')['수출액(천불)'].reset_index(drop=True)

korea17to21 = pd.concat([korea17, korea18, korea19, korea20, korea21], axis=1)
korea17to21



#중국
chinaPath = './data/china/'
df_china = mergeDataInFolder(chinaPath)
trade_confiremd_china = mergeConfirmed(df_china)
trade_confiremd_china

china17 = devideDate(trade_confiremd_china, '2017', '2017-07')['수출액(천불)'].reset_index(drop=True)
china18 = devideDate(trade_confiremd_china, '2018', '2018-07')['수출액(천불)'].reset_index(drop=True)
china19 = devideDate(trade_confiremd_china, '2019', '2019-07')['수출액(천불)'].reset_index(drop=True)
china20 = devideDate(trade_confiremd_china, '2020', '2020-07')['수출액(천불)'].reset_index(drop=True)
china21 = devideDate(trade_confiremd_china, '2021', '2021-07')['수출액(천불)'].reset_index(drop=True)

china17to21 = pd.concat([china17, china18, china19, china20, china21], axis=1)
china17to21.describe()


#대만
taiwanPath = './data/taiwan/'
df_taiwan = mergeDataInFolder(taiwanPath)
trade_confiremd_taiwan = mergeConfirmed(df_taiwan)
trade_confiremd_taiwan

taiwan17 = devideDate(trade_confiremd_taiwan, '2017', '2017-07')['수출액(천불)'].reset_index(drop=True)
taiwan18 = devideDate(trade_confiremd_taiwan, '2018', '2018-07')['수출액(천불)'].reset_index(drop=True)
taiwan19 = devideDate(trade_confiremd_taiwan, '2019', '2019-07')['수출액(천불)'].reset_index(drop=True)
taiwan20 = devideDate(trade_confiremd_taiwan, '2020', '2020-07')['수출액(천불)'].reset_index(drop=True)
taiwan21 = devideDate(trade_confiremd_taiwan, '2021', '2021-07')['수출액(천불)'].reset_index(drop=True)

taiwan17to21 = pd.concat([taiwan17, taiwan18, taiwan19, taiwan20, taiwan21], axis=1)
taiwan17to21.describe()


#일본
japanPath = './data/japan/'
df_japan = mergeDataInFolder(japanPath)
trade_confiremd_japan = mergeConfirmed(df_japan)
trade_confiremd_japan['수출액(천불)'] = trade_confiremd_japan['수출액(천불)'] * 0.00915
trade_confiremd_japan

japan17 = devideDate(trade_confiremd_japan, '2017', '2017-07')['수출액(천불)'].reset_index(drop=True)
japan18 = devideDate(trade_confiremd_japan, '2018', '2018-07')['수출액(천불)'].reset_index(drop=True)
japan19 = devideDate(trade_confiremd_japan, '2019', '2019-07')['수출액(천불)'].reset_index(drop=True)
japan20 = devideDate(trade_confiremd_japan, '2020', '2020-07')['수출액(천불)'].reset_index(drop=True)
japan21 = devideDate(trade_confiremd_japan, '2021', '2021-07')['수출액(천불)'].reset_index(drop=True)

japan17to21 = pd.concat([japan17, japan18, japan19, japan20, japan21], axis=1)
japan17to21.describe()


#미국
usaPath = './data/usa/'
df_usa = mergeDataInFolder(usaPath)
trade_confiremd_usa = mergeConfirmed(df_usa)
trade_confiremd_usa

usa17 = devideDate(trade_confiremd_usa, '2017', '2017-07')['수출액(천불)'].reset_index(drop=True)
usa18 = devideDate(trade_confiremd_usa, '2018', '2018-07')['수출액(천불)'].reset_index(drop=True)
usa19 = devideDate(trade_confiremd_usa, '2019', '2019-07')['수출액(천불)'].reset_index(drop=True)
usa20 = devideDate(trade_confiremd_usa, '2020', '2020-07')['수출액(천불)'].reset_index(drop=True)
usa21 = devideDate(trade_confiremd_usa, '2021', '2021-07')['수출액(천불)'].reset_index(drop=True)

usa17to21 = pd.concat([usa17, usa18, usa19, usa20, usa21], axis=1)
usa17to21.describe()

#eu
euPath = './data/eu/'
df_eu = mergeDataInFolder(euPath)
trade_confiremd_eu = mergeConfirmed(df_eu)
trade_confiremd_eu['수출액(천불)'] = trade_confiremd_eu['수출액(천불)'] * 1.17166
trade_confiremd_eu

eu17 = devideDate(trade_confiremd_eu, '2017', '2017-07')['수출액(천불)'].reset_index(drop=True)
eu18 = devideDate(trade_confiremd_eu, '2018', '2018-07')['수출액(천불)'].reset_index(drop=True)
eu19 = devideDate(trade_confiremd_eu, '2019', '2019-07')['수출액(천불)'].reset_index(drop=True)
eu20 = devideDate(trade_confiremd_eu, '2020', '2020-07')['수출액(천불)'].reset_index(drop=True)
eu21 = devideDate(trade_confiremd_eu, '2021', '2021-07')['수출액(천불)'].reset_index(drop=True)

eu17to21 = pd.concat([eu17, eu18, eu19, eu20, eu21], axis=1)
eu17to21.describe()


# 각 나라별 상관계수 막대그래프 시각화
# def country(data)
korea = trade_confiremd_korea[['수출액(천불)','누적확진자수']]
china = trade_confiremd_china[['수출액(천불)','누적확진자수']]
taiwan = trade_confiremd_taiwan[['수출액(천불)','누적확진자수']]
japan = trade_confiremd_japan[['수출액(천불)','누적확진자수']]
usa = trade_confiremd_usa[['수출액(천불)','누적확진자수']]
# list 형식으로 값 넣기
correlation_by_country = []
correlation_by_country.append(korea.corr().values[0][1])
correlation_by_country.append(china.corr().values[0][1])
correlation_by_country.append(taiwan.corr().values[0][1])
correlation_by_country.append(japan.corr().values[0][1])
correlation_by_country.append(usa.corr().values[0][1])
#막대로 보여주기 ! 
plt.bar(x=['korea','china','taiwan','japan','usa'],height = correlation_by_country)
plt.title('나라별 코로나와 무역 상관계수')
plt.axhline(0.6,color= 'blue')
plt.show()

#시각화 자료

#코로나
df_confirmed[:18]

plt.plot(df_confirmed[:18]['y-m'], df_confirmed[:18]['누적확진자수'], color='#c02ad1', linestyle='--', label='코로나확진자수')
plt.legend(loc='upper left', fontsize=10)
plt.xticks(rotation=45)
plt.title('전 세계 월별 누적 확진자 수')
plt.show()


#무역 전체 데이터

#선그래프 만들기 
#names title에 들어갈 이름을 리스트로 넣어주기
#data 그래프를 만들 데이터 넣어주기
def makeLineplot(names, *data):
    colors = ['b', 'tomato', 'darkgreen', 'brown']
    random.shuffle(colors)
    data_temp = []
    title = ''
    yvalues = []
    
    plt.figure(figsize=(4.6, 2.5))
    #plt = temp_fig.add_subplot()

    j = 0
    for data in data:
        data_temp.append(devideDate(data, '2011', '2020-01'))
        title = title + ' ' + names[j]
        max = data_temp[j]['수출액(천불)'].max()
        max = format(max, 'e')

        plt.plot(data['y-m'], data['수출액(천불)'], label=names[j], color=colors[j], alpha=0.5)
        plt.axhline(data_temp[j]['수출액(천불)'].mean(), 0, 0.885, linewidth=1, linestyle='--', color='r', alpha=0.6)
        plt.axvspan('2020-01', '2021-07', facecolor='khaki', alpha=0.2)
        plt.axvspan('2011-01', '2020-01', facecolor='gray', alpha=0.1)
        plt.scatter(data_temp[j]['y-m'].loc[data_temp[j]['수출액(천불)'].idxmax()], data_temp[j]['수출액(천불)'].max(), label=max, s=15, color=colors[j], alpha=1)
        xvalues = ['2002-01', '2011-01', '2020-01']
        yvalues.append(data_temp[j]['수출액(천불)'].mean())
        plt.xticks(xvalues, fontsize=8.5)
        plt.yticks(yvalues, fontsize=8.5)
        plt.legend(fontsize=8.5)
        #loc='lower right',
        plt.title(title + ' 무역 데이터')
        
        j += 1


#한국
makeLineplot(['대한민국'], trade_confiremd_korea)

#일본, 대만
makeLineplot(['일본', '대만'], trade_confiremd_japan, trade_confiremd_taiwan)
    
#미국
makeLineplot(['미국'], trade_confiremd_usa)

#eu, 중국
makeLineplot(['중국', 'eu'], trade_confiremd_china, trade_confiremd_eu)

plt.show()

#원유
import re
com = re.compile('\d\d')



wti = pd.read_excel('./data/국제원유2021.xlsx', skiprows=2, header=1)
wti = wti[['월', 'WTI']][:20]
wti['월'][0] = '01월'
wti['월'][12] = '01월'
for i in range(12):
    wti['월'][i] = '20-' + ''.join(com.findall(wti['월'][i]))
for i in range(12, 20):
    wti['월'][i] = '21-' + ''.join(com.findall(wti['월'][i]))

plt.plot(wti['월'], wti['WTI'])
plt.show()
wti.columns

