import pandas as pd

# 컬럼명 추가
names = ["순번","월","수출금액","수출증감율","수입금액","수입증감율","수지"]

# 데이터 읽기 ( 3행까지는 header이기 때문에 버린다.)
df_19 = pd.read_excel("./data/ex1.xls", skiprows=3, names = names)
df_20 = pd.read_excel("./data/ex2.xls", skiprows=3, names = names)
df_21 = pd.read_excel("./data/ex3.xls", skiprows=3, names = names)

# 기존에는 월만 나와있기때문에 연도도 추가
df_19["월"] = "19년 " + df_19["월"]
df_20["월"] = "20년 " + df_20["월"]
df_21["월"] = "21년 " + df_21["월"]

# 행 역순으로 저장 (월이 역순으로 들어가있기때문)
df_19 = df_19[::-1]
df_20 = df_20[::-1]
df_21 = df_21[::-1]

total = pd.concat([df_19,df_20,df_21], ignore_index=True)

total = total.drop(['순번'], axis ='columns')
total

idx = ["확진자수평균1","누적확진자수1"]
data = pd.read_excel("./data/data.xlsx")
data
test = total.copy
total

test

test["누적3","누적4"] = data.values

test

data.values

test

total.corr(method='pearson')

total.dtypes