# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


online_train_file_path = '../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../tianchi_data/source_data/offline_test.csv'

user_status_dict = dict()


def get_column_info(source_file_path, column_name, need_action):
    source_data = pd.read_csv(source_file_path)
    column_id_list = source_data[column_name]
    cid_list = source_data['cid']
    uid_list = source_data['uid']
    mid_list = source_data['mid']
    date_list = source_data['date']
    if need_action == 0:
        return column_id_list, cid_list, uid_list, mid_list, date_list
    else:
        action_list = source_data['action']
        return column_id_list, cid_list, uid_list, mid_list, date_list, action_list


def get_status(column_id_list, cid_list, uid_list, mid_list, date_list):
    for index in range(len(column_id_list)):
        column_id = column_id_list[index]
        uid = uid_list[index]
        mid = mid_list[index]
        date = date_list[index]
        if date != 'null':
            if uid in user_status_dict:
                user_status_dict[uid].add(str(mid))
            else:
                user_status_dict[uid] = set()
                user_status_dict[uid].add(str(mid))


def save_result_into_file(feature_save_file_path):
    with codecs.open(feature_save_file_path, 'w', 'utf-8') as feature_save_file:
        feature_save_file.write('uid,x1' + '\n')
        for mid in user_status_dict:
            result_list = list(user_status_dict[mid])
            feature_save_file.write(str(mid) + ',' + ';'.join(result_list) + '\n')

time_lim = 15
column_name = 'mid'

column_id_list, cid_list, uid_list, mid_list, date_list = get_column_info(offline_train_file_path, column_name, 0)
get_status(column_id_list, cid_list, uid_list, mid_list, date_list)

feature_save_file_path = '../feature_data/user_mall_connection_' + str(time_lim) + '.csv'
save_result_into_file(feature_save_file_path)
