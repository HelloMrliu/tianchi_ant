# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


online_train_file_path = '../../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../../tianchi_data/source_data/offline_test.csv'


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
    date_received = source_data['date_received']

    result_list = list()

    for index in range(len(uid_list)):
        uid = str(uid_list[index])
        date = str(date_received[index])
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

online_train_set = set(get_id_list_all(online_train_file_path, '2'))
offline_train_set = set(get_id_list(offline_train_file_path))
offline_test_set = set(get_test_list(offline_test_file_path))

result_set = set()
count = 0
for val in offline_test_set:
    if val in online_train_set and val not in offline_train_set:
        result_set.add(val)
        count += 1
print count

with codecs.open('../id_not_in_offline/user_cunpon_data', 'w', 'utf-8') as write_file:
    for std_id in result_set:
        write_file.write(std_id + '\n')
