# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


online_train_file_path = '../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../tianchi_data/source_data/offline_test.csv'


def get_column_info(source_file_path, column_name, need_action):
    source_data = pd.read_csv(source_file_path)
    column_id_list = source_data[column_name]
    cid_list = source_data['cid']
    date_received_list = source_data['date_received']
    date_list = source_data['date']
    if need_action == 0:
        return column_id_list, cid_list, date_received_list, date_list
    else:
        action_list = source_data['action']
        return column_id_list, cid_list, date_received_list, date_list, action_list


def get_time_diff(less_time, big_time):
    month_diff = abs(int(big_time[-4:-2]) - int(less_time[-4:-2]))

    if month_diff == 0:
        return abs(int(big_time[-2:]) - int(less_time[-2:]))
    else:
        return abs(int(big_time[-2:]) - int(less_time[-2:]) + 30 * month_diff)


def count_bc_number_offline(column_id_list, cid_list, date_received_list, date_list, time_limit):
    std_id = column_id_list[0]
    std_index = 0
    count = 0
    sub_count = 0
    for index in range(len(column_id_list)):
        if std_id == column_id_list[index]:
            pass
        else:
            temp_dict = dict()
            buy_number = 0
            for sub_index in range(std_index, index):
                cid = cid_list[sub_index]
                date_received = date_received_list[sub_index]
                date = date_list[sub_index]

                if cid != 'null':
                    if date_received in temp_dict:
                        temp_dict[date_received] += 1
                    else:
                        temp_dict[date_received] = 1
                if date != 'null':
                    buy_number += 1

            for date_rec in temp_dict:
                if temp_dict[date_rec] == index-std_index and index-std_index >= 2:
                    if buy_number > 0:
                        print std_id
                        sub_count += 1
                    count += 1
                    break

            std_id = column_id_list[index]
            std_index = index
    print count
    print sub_count

time_lim = 15
column_name = 'uid'

column_id_list, cid_list, date_received_list, date_list = get_column_info(offline_train_file_path, column_name, 0)
count_bc_number_offline(column_id_list, cid_list, date_received_list, date_list, time_lim)

