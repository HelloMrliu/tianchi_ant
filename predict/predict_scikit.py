# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import codecs
import time


train_data_path = '../train_data/train_data.csv'
val_data_path = '../train_data/val_data.csv'
test_data_path = '../train_data/test_data.csv'
save_file_path = '../result_data/result_'

data = pd.read_csv(train_data_path)
val_data = pd.read_csv(val_data_path)
test_data = pd.read_csv(test_data_path)

train_data, temp_data = train_test_split(data, test_size=0.1)

train_uid = train_data['uid']
train_mid = train_data['mid']
train_cid = train_data['cid']

val_uid = val_data['uid']
val_mid = val_data['mid']
val_cid = val_data['cid']

test_uid = test_data['uid']
test_mid = test_data['mid']
test_cid = test_data['cid']
test_date_received = test_data['date_received']

train_x = train_data.drop(['uid', 'mid', 'cid', 'label'], axis=1)
train_y = train_data['label']

val_x = val_data.drop(['uid', 'mid', 'cid', 'label'], axis=1)
val_y = val_data['label']

test_x = test_data.drop(['uid', 'mid', 'cid', 'date_received'], axis=1)

weight_dict = {
    0: 0.3,
    1: 0.7
}

print 'start'
model = GradientBoostingRegressor(n_estimators=300, learning_rate=0.1, max_depth=4, random_state=0, loss='ls')
#model = linear_model.LinearRegression()
model.fit (train_x, train_y)
predict_y = model.predict(test_x)

#print model.score(val_x, val_y, weight_dict)

max_val = -10.0
min_val = 10.0
for val in predict_y:
    val = float(val)
    if val > max_val:
        max_val = val
    if val < min_val:
        min_val = val

    test_y = list()
for val in predict_y:
    test_y.append((float(val) - min_val) / (max_val - min_val))

uid_list = list(test_uid)
mid_list = list(test_mid)
cid_list = list(test_cid)
date_received_list = list(test_date_received)
y_list = list(test_y)

current_time = time.strftime('%Y%m%d%H%M%S')
with codecs.open(save_file_path + str(current_time) + '.csv', 'w', 'utf-8') as save_file:
    for index in range(len(y_list)):
        save_file.write(str(uid_list[index]) + ',' + str(cid_list[index]) + ',' + str(date_received_list[index]) + ',' + str("%.6f" % float(y_list[index])) + '\n')
