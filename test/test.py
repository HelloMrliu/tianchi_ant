# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


def get_time_diff(less_time, big_time):
    month_diff = int(big_time[-4:-2]) - int(less_time[-4:-2])

    if month_diff == 0:
        return int(big_time[-2:]) - int(less_time[-2:])
    else:
        return int(big_time[-2:]) - int(less_time[-2:]) + 30 * month_diff


online_train_file_path = '../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../tianchi_data/source_data/offline_test.csv'


def get_test_list(source_file_path):
    source_data = pd.read_csv(source_file_path)
    uid_list = source_data['uid']

    result_list = list()

    for result in uid_list:
        result_list.append(str(result))
    return result_list


def get_id_list(source_file_path):
    source_data = pd.read_csv(source_file_path)
    uid_list = source_data['uid']
    cid_list = source_data['cid']
    date_list = source_data['date']

    result_list = list()

    for index in range(len(uid_list)):
        uid = str(uid_list[index])
        date = str(date_list[index])
        if date != 'null':
            result_list.append(uid)
    return result_list


def get_id_list_all(source_file_path, std_action):
    source_data = pd.read_csv(source_file_path)
    uid_list = source_data['uid']
    action_list = source_data['action']
    result_list = list()

    for index in range(len(uid_list)):
        uid = str(uid_list[index])
        action = str(action_list[index])
        if action == std_action:
            result_list.append(uid)
    return result_list


online_train_set = set(get_id_list_all(online_train_file_path, '1'))
offline_train_set = set(get_id_list(offline_train_file_path))
offline_test_set = set(get_test_list(offline_test_file_path))

print len(offline_test_set)
print len(offline_train_set)
print len(online_train_set)


count = 0
for val in offline_test_set:
    if val in online_train_set and val not in offline_train_set:
        count += 1
print count
'''
76309
207784
412182
10874


print len(offline_train_set)
print len(online_train_set)
print len(offline_train_set & online_train_set)
'''
'''
print len(offline_test_set)
print len(offline_train_set)
print len(offline_test_set & (offline_train_set))
print len(offline_test_set & (offline_train_set | online_train_set))

76309
515379
74417

76309
762858
43155

1559
8376
1556

print len(online_train_set | offline_train_set)
print len(online_train_set & offline_train_set)
print len(offline_test_set & offline_train_set)


all_data = pd.read_csv(offline_train_file_path)
id_list = all_data['cid']

train_index_list = list()
val_index_list = list()

for index in range(len(id_list)):
    if index % 10 == 0:
        val_index_list.append(index)
    else:
        train_index_list.append(index)

train_list = all_data.ix[train_index_list]
val_list = all_data.ix[val_index_list]

print len(train_list)
print len(val_list)


train_list.to_csv('../train_data.csv', index=False)
val_list.to_csv('../val_data.csv', index=False)
'''