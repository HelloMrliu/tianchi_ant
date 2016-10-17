# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs
import os


train_data_path = '../train_data/pre_train_data.csv'
data = pd.read_csv(train_data_path)

label_list = data['label']
uid_list = data['uid']
mid_list = data['mid']
cid_list = data['cid']

pos_index_list = list()
neg_index_list = list()

pos_rem_set = set()
neg_rem_set = set()

index = 0
for index in range(len(label_list)):
    uid = str(uid_list[index])
    mid = str(mid_list[index])
    cid = str(cid_list[index])

    if str(label_list[index]) == '1':
        if uid + ',' + mid + ',' + 'cid' not in pos_rem_set:
            pos_index_list.append(index)
            pos_rem_set.add(uid + ',' + mid + ',' + 'cid')
    else:
        if index % 2 == 0:
            if uid + ',' + mid + ',' + 'cid' not in pos_rem_set:
                if index != 0:
                    neg_index_list.append(index-2)
                else:
                    neg_index_list.append(index)
                neg_rem_set.add(uid + ',' + mid + ',' + 'cid')

pos_list = list()
neg_list = list()

pos_list = data.ix[pos_index_list]
neg_list = data.ix[neg_index_list]

print len(pos_list)
print len(neg_list)

new_list = pos_list.append(neg_list)
print len(new_list)

new_list.to_csv('../train_data/train_data.csv', index=False)
