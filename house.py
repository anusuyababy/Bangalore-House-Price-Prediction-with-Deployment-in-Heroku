# -*- coding: utf-8 -*-
"""house

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b3ytyew3ja7N_sF5o23Wft2pBxUptYAL
"""

import pandas as pd
import numpy as np

df=pd.read_csv('bhouse.csv')
df.head()

df.shape

df.isnull().sum()

df.info()

df['balcony'] = df['balcony'].fillna(2.0)
df['bath'] = df['bath'].fillna(2.0)
df['bath'] = df['bath'].astype(int)
df['balcony'] = df['balcony'].astype(int)
df.head()

def num(x):
    try:
        float (x)
    except:
        return False
    return True

def convert_to_num(x):
    y=x.split(' - ') 
    if (len(y)>1):
        return (float(y[0])+float(y[1]))/2
    try:
        return float(x)
    except:
        return None

df['total_sqft'] = df.total_sqft.apply(convert_to_num)
df.head()

df = df.dropna(subset=['total_sqft'])
df.head()

df['size'] = df['size'].str.replace('Bedroom', '').str.replace('RK', '').str.replace('BHK', '')
df['size'] = df['size'].fillna(2)
df['size'] = df['size'].astype(int)
df.head()

df.drop([1718,4684], inplace=True)
df.head()

df['location']= df['location'].fillna('Whitefield')
df['society']= df['society'].fillna('Other')
df.head()

df=df.drop(['society', 'availability'], axis = 1)
df.head()

dummy_cols = pd.get_dummies(df.area_type)
df = pd.concat([df,dummy_cols], axis='columns')

df.head()

s=df['location'].value_counts()
s

print(len(s[s>=11]))

r = s[s<11]
df.location = df.location.apply(lambda x: 'other' if x in r else x)
len(df.location.unique())

df.head()

dummy_cols = pd.get_dummies(df.location)
df = pd.concat([df,dummy_cols], axis='columns')

df.drop(['location', 'area_type'], axis='columns', inplace=True)
df.head()

df = df.drop(df[(df['total_sqft']<450)].index)
df.head()

df = df.drop(df[(df['total_sqft']>10000)].index)
df.head()

df = df.drop(df[(df['total_sqft']<1000) & (df['bath']>3) & (df['size']>2)].index)
df.head()

df = df.drop(df[(df['total_sqft']<2000) & (df['bath']>5) & (df['size']>4)].index)
df.head()

df = df.drop(df[(df['total_sqft']<600) & (df['bath']>2) & (df['size']>1)].index)
df.head()

df = df.drop(df[(df['price']>100) & (df['total_sqft']<1000)].index)
df.head()

df = df.drop(df[(df['price']>1000)].index)
df.head()

df = df.drop(df[(df['total_sqft']<1000) & (df['bath']>3)].index)
df.head()

df = df.drop(df[(df['bath']==2) & (df['size']>3)].index)
df.head()

df = df.drop(df[(df['bath']==3) & (df['size']>4)].index)
df.head()

df = df.drop(df[(df['total_sqft']<3000) & (df['bath']>7) & (df['size']>6)].index)
df.head()

df = df.drop(df[(df['total_sqft']<1000) & (df['size']>2)].index)
df.head()

df = df.drop(df[(df['bath'] == 1) & (df['size']>=2)].index)
df.head()

df.drop([1078], inplace=True)
df.head()

df = df.drop(df[(df['bath']==6)&(df['size']<=4)].index)
df.head()

df = df.drop(df[(df['bath']==5)&(df['size']<=3)].index)
df.head()

df = df.drop(df[(df['bath']==7)&(df['size']<=5)].index)
df.head()

df = df.drop(df[(df['price']>500)].index)
df.head()

df = df.drop(df[(df['total_sqft']>4000) & (df['size']>6) & (df['bath']>6)].index)
df.head()

df = df.drop(df[(df['bath']==4)&(df['size']==6)].index)
df.head()

df = df.drop(df[(df['total_sqft']>4000)].index)
df.head()

df = df.drop(df[(df['size']>6) & (df['bath']>6)].index)
df.head()

df = df.drop(df[(df['bath']>=7)].index)
df.head()

df = df.drop(df[(df['size']>6)].index)
df.head()

df = df.drop(df[(df['size']==2) & (df['balcony']==3)].index)
df.head()

df = df.drop(df[(df['size']==1) & (df['balcony']==2)].index)
df.head()

df.shape

x=df.drop(['price'], axis = 1)
y=df['price']
x.shape, y.shape

from sklearn.model_selection import train_test_split
x_train,x_test, y_train, y_test = train_test_split(x,y, test_size =0.20, random_state = 3)

from sklearn.ensemble import GradientBoostingRegressor
clf=GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2, learning_rate = 0.1)
clf.fit(x_train,y_train)

clf.score(x_train,y_train)

clf.score(x_test,y_test)

import json
columns = {
    'data_columns' : [col.lower() for col in x.columns]
}
with open("columns.json","w") as f:
    f.write(json.dumps(columns))

import pickle
pickle.dump(clf, open('model.pkl', 'wb'))