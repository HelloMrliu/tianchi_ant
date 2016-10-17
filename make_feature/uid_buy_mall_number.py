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
    mid_list = source_data['mid']
    date_list = source_data['date']
    if need_action == 0:
        return column_id_list, cid_list, mid_list, date_list
    else:
        action_list = source_data['action']
        return column_id_list, cid_list, mid_list, date_list, action_list


def get_status(column_id_list, cid_list, mid_list, date_list):
    std_id = column_id_list[0]
    std_index = 0
    for index in range(len(column_id_list)):
        if std_id == column_id_list[index]:
            pass
        else:
            column_id = column_id_list[std_index]
            temp_set = set()
            for sub_index in range(std_index, index):
                cid = cid_list[sub_index]
                mid = mid_list[sub_index]
                date = date_list[sub_index]
                if date != 'null':
                    temp_set.add(mid)

            user_status_dict[column_id] = len(temp_set)
            std_id = column_id_list[index]
            std_index = index


def save_result_into_file(feature_save_file_path):
    with codecs.open(feature_save_file_path, 'w', 'utf-8') as feature_save_file:
        feature_save_file.write('uid,x1e' + '\n')
        max_num = 0
        for mid in user_status_dict:
            if max_num < int(user_status_dict[mid]):
                max_num = int(user_status_dict[mid])
        for mid in user_status_dict:
            per = float(user_status_dict[mid]) / max_num
            feature_save_file.write(str(mid) + ',' + str("%.2f" % per) + '\n')

time_lim = 15
column_name = 'uid'

column_id_list, cid_list, mid_list, date_list = get_column_info(offline_train_file_path, column_name, 0)
get_status(column_id_list, cid_list, mid_list, date_list)

feature_save_file_path = '../feature_data/uid_buy_mall_' + str(time_lim) + '.csv'
save_result_into_file(feature_save_file_path)
