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
    result_dict = dict()
    result_date_ditc = dict()
    source_data = pd.read_csv(source_file_path)
    uid_list = source_data['uid']
    cid_list = source_data['cid']
    date_list = source_data['date_received']

    for index in range(len(uid_list)):
        uid = str(uid_list[index])
        cid = str(cid_list[index])
        date = str(date_list[index])
        if cid == 'null':
            continue
        key = uid + ';' + cid + ';' + date
        if key in result_dict:
            result_dict[key] += 1
        else:
            result_dict[key] = 1
        '''
        if key in result_date_ditc:
            result_date_ditc[key].append(date)
        else:
            result_date_ditc[key] = list()
            result_date_ditc[key].append(date)
        '''
    return result_dict, result_date_ditc


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


#online_train_set = set(get_id_list_all(online_train_file_path, '1'))
#offline_train_set = set(get_id_list(offline_train_file_path))
test_dict, test_date_dict = get_test_list(offline_test_file_path)

count = 0
sub_count = 0
for key in test_dict:
    if test_dict[key] >= 2:
        print key
        count += test_dict[key]
print count