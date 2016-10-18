# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs

small_count_dict = dict()


def get_id_list_all(source_file_path):
    source_data = pd.read_csv(source_file_path)
    uid_list = source_data['uid']
    mid_list = source_data['mid']
    cid_list = source_data['cid']
    date_received_list = source_data['date_received']
    date_list = source_data['date']
    action_list = source_data['action']
    return uid_list, mid_list, cid_list, date_received_list, date_list, action_list


def count_bc_number_offline(uid_list, mid_list, cid_list, date_received_list, date_list, action_list, std_action, online_id_set):
    for index in range(len(uid_list)):
        uid = str(uid_list[index])
        cid = str(cid_list[index])
        mid = str(mid_list[index])
        date_received = str(date_received_list[index])
        date = str(date_list[index])
        action = str(action_list[index])
        if uid not in online_id_set:
            continue
        if action == std_action:
            if date != 'null':
                if uid in small_count_dict:
                    small_count_dict[uid] += 1
                else:
                    small_count_dict[uid] = 1


def save_result_into_file(feature_save_file_path):
    with codecs.open(feature_save_file_path, 'a+', 'utf-8') as feature_save_file:
        max_num = 0
        for mid in small_count_dict:
            if max_num < int(small_count_dict[mid]):
                max_num = int(small_count_dict[mid])
        for mid in small_count_dict:
            per = float(small_count_dict[mid]) / max_num
            feature_save_file.write(str(mid) + ',' + str("%.3f" % per) + '\n')


offline_data_file = '../feature_data/uid_buy_liveness_15.csv'
online_data_file = '../../../tianchi_data/source_data/online_train.csv'
online_id_data_file = '../id_not_in_offline/user_buy_data'
online_id_set = set()

with codecs.open(online_id_data_file, 'r', 'utf-8') as online_id_data:
    for data in online_id_data:
        online_id_set.add(data.strip('\n'))

uid_list, mid_list, cid_list, date_received_list, date_list, action_list = get_id_list_all(online_data_file)
count_bc_number_offline(uid_list, mid_list, cid_list, date_received_list, date_list, action_list, '1', online_id_set)

save_result_into_file(offline_data_file)
