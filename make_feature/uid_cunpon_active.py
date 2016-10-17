# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


online_train_file_path = '../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../tianchi_data/source_data/offline_test.csv'

small_count_dict = dict()
all_count_dict = dict()
test_set = set()

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
    month_diff = int(big_time[-4:-2]) - int(less_time[-4:-2])

    if month_diff == 0:
        return int(big_time[-2:]) - int(less_time[-2:])
    else:
        return int(big_time[-2:]) - int(less_time[-2:]) + 30 * month_diff


def count_bc_number_offline(column_id_list, cid_list, date_received_list, date_list, time_limit):
    for index in range(len(column_id_list)):
        column_id = column_id_list[index]
        cid = cid_list[index]
        date_received = date_received_list[index]
        date = date_list[index]
        if cid != 'null' and date != 'null':
            time_diff = get_time_diff(date_received, date)
            if time_diff <= time_limit:
                if column_id in small_count_dict:
                    small_count_dict[column_id] += 1
                else:
                    small_count_dict[column_id] = 1
            else:
                pass


def count_bc_number_online(column_id_list, cid_list, date_received_list, date_list, action_list, time_limit, action_number):
    for index in range(len(column_id_list)):
        column_id = column_id_list[index]
        cid = cid_list[index]
        date_received = date_received_list[index]
        date = date_list[index]
        action = action_list[index]
        if action == action_number:
            if cid != 'null' and date != 'null':
                if column_id in all_count_dict:
                    all_count_dict[column_id] += 1
                else:
                    all_count_dict[column_id] = 1
        else:
            pass

'''
def save_result_into_file(feature_save_file_path):
    with codecs.open(feature_save_file_path, 'w', 'utf-8') as feature_save_file:
        feature_save_file.write('mid,x1e' + '\n')
        max_num = 0
        for mid in small_count_dict:
            if max_num < int(small_count_dict[mid]):
                max_num = int(small_count_dict[mid])
        for mid in small_count_dict:
            per = float(small_count_dict[mid]) / max_num
            feature_save_file.write(str(mid) + ',' + str("%.4f" % per) + '\n')
'''
def save_result_into_file(feature_save_file_path):
    with codecs.open(feature_save_file_path, 'w', 'utf-8') as feature_save_file:
        feature_save_file.write('uid,x1' + '\n')
        max_num = 0
        for mid in small_count_dict:
            if max_num < int(small_count_dict[mid]):
                max_num = int(small_count_dict[mid])

        for mid in all_count_dict:
            if mid in small_count_dict:
                per = float(all_count_dict[mid]) / max_num
                feature_save_file.write(str(mid) + ',' + str("%.5f" % per) + '\n')
                small_count_dict.pop(mid)
            elif mid in test_set:
                per = float(all_count_dict[mid]) / max_num
                feature_save_file.write(str(mid) + ',' + str("%.5f" % per) + '\n')
            else:
                pass

        for mid in small_count_dict:
            per = float(small_count_dict[mid]) / max_num
            feature_save_file.write(str(mid) + ',' + str("%.5f" % per) + '\n')


time_lim = 15
column_name = 'uid'


test_data = pd.read_csv(offline_test_file_path)
test_uid_list = test_data['uid']
for data in test_uid_list:
    test_set.add(data)

column_id_list, cid_list, date_received_list, date_list = get_column_info(offline_train_file_path, column_name, 0)
count_bc_number_offline(column_id_list, cid_list, date_received_list, date_list, time_lim)


column_id_list, cid_list, date_received_list, date_list, action_list = get_column_info(online_train_file_path, column_name, 1)
count_bc_number_online(column_id_list, cid_list, date_received_list, date_list, action_list, time_lim, 1)

feature_save_file_path = '../feature_data/uid_coupon_active_' + str(time_lim) + '.csv'
save_result_into_file(feature_save_file_path)
