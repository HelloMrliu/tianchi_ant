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
    date_received_list = source_data['date_received']
    date_list = source_data['date']
    if need_action == 0:
        return column_id_list, cid_list, date_received_list, date_list
    else:
        action_list = source_data['action']
        return column_id_list, cid_list, date_received_list, date_list, action_list


def get_status(column_id_list, cid_list, date_received_list, date_list):
    std_id = column_id_list[0]
    std_index = 0
    for index in range(len(column_id_list)):
        if std_id == column_id_list[index]:
            pass
        else:
            column_id = column_id_list[std_index]
            buy_count = 0
            get_cunpon_count = 0
            get_then_buy_count = 0
            length = index - std_index
            for sub_index in range(std_index, index):
                cid = cid_list[sub_index]
                date = date_list[sub_index]
                if cid != 'null' and date == 'null':
                    buy_count += 1
                elif cid == 'null' and date != 'null':
                    get_cunpon_count += 1
                elif cid != 'null' and date != 'null':
                    get_then_buy_count += 1
                else:
                    pass

            if buy_count == length:
                status = 1
            elif get_cunpon_count == length:
                status = 2
            else:
                status = 4
            '''
            elif get_then_buy_count != 0:
                status = 3
            '''

            user_status_dict[column_id] = status
            std_id = column_id_list[index]
            std_index = index


def save_result_into_file(feature_save_file_path):
    with codecs.open(feature_save_file_path, 'w', 'utf-8') as feature_save_file:
        feature_save_file.write('uid,x1e' + '\n')
        for mid in user_status_dict:
            status = user_status_dict[mid]
            feature_save_file.write(str(mid) + ',' + str("%.1f" % status) + '\n')


time_lim = 15
column_name = 'uid'


column_id_list, cid_list, date_received_list, date_list = get_column_info(offline_train_file_path, column_name, 0)
get_status(column_id_list, cid_list, date_received_list, date_list)

feature_save_file_path = '../feature_data/uid_buy_and_cunpon_status' + str(time_lim) + '.csv'
save_result_into_file(feature_save_file_path)
