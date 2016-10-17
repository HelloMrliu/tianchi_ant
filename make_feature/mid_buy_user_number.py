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
    date_list = source_data['date']
    if need_action == 0:
        return column_id_list, cid_list, uid_list, date_list
    else:
        action_list = source_data['action']
        return column_id_list, cid_list, uid_list, date_list, action_list


def get_status(column_id_list, cid_list, uid_list, date_list):
    for index in range(len(column_id_list)):
        column_id = column_id_list[index]
        uid = uid_list[index]
        date = date_list[index]
        if date != 'null':
            if column_id in user_status_dict:
                user_status_dict[column_id].add(uid)
            else:
                user_status_dict[column_id] = set()
                user_status_dict[column_id].add(uid)


def save_result_into_file(feature_save_file_path):
    with codecs.open(feature_save_file_path, 'w', 'utf-8') as feature_save_file:
        feature_save_file.write('mid,x1e' + '\n')
        max_num = 0
        for mid in user_status_dict:
            if max_num < int(len(user_status_dict[mid])):
                max_num = int(len(user_status_dict[mid]))
        for mid in user_status_dict:
            print len(user_status_dict[mid])
            per = float(len(user_status_dict[mid])) / max_num
            feature_save_file.write(str(mid) + ',' + str("%.4f" % per) + '\n')

time_lim = 15
column_name = 'mid'

column_id_list, cid_list, uid_list, date_list = get_column_info(offline_train_file_path, column_name, 0)
get_status(column_id_list, cid_list, uid_list, date_list)

feature_save_file_path = '../feature_data/mid_buy_user_' + str(time_lim) + '.csv'
save_result_into_file(feature_save_file_path)
