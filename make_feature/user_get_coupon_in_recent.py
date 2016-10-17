# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


def get_time_diff(less_time, big_time):
    month_diff = int(big_time[-4:-2]) - int(less_time[-4:-2])
    if month_diff == 0 and abs(int(big_time[-2:]) - int(less_time[-2:])) <= 1:
        return 0
    else:
        return 1


def cal_user_get_coupon_in_recent(file_path):
    return_dict = dict()
    result_dict = dict()
    source_data = pd.read_csv(file_path)

    cid_list = source_data['cid']
    uid_list = source_data['uid']
    mid_list = source_data['mid']
    date_received_list = source_data['date_received']

    for index in range(len(uid_list)):
        uid = uid_list[index]
        cid = cid_list[index]
        mid = mid_list[index]
        date_received = date_received_list[index]
        temp_tun = (uid, mid, cid, date_received)
        if uid in result_dict:
            result_dict[uid].append(temp_tun)
        else:
            result_dict[uid] = list()
            result_dict[uid].append(temp_tun)

    for uid in result_dict:
        res_list = result_dict[uid]
        if len(res_list) == 0:
            continue
        else:
            for father_index in range(len(res_list)):
                std_res = res_list[father_index]
                std_uid = str(std_res[0])
                std_mid = str(std_res[1])
                std_cid = str(std_res[2])
                std_time = str(std_res[3])
                if std_cid == 'null':
                    continue
                if father_index == len(res_list):
                    break
                count = 0
                for child_index in range(father_index, len(res_list)):
                    res = res_list[child_index]
                    if str(res[2]) == 'null':
                        continue
                    if str(res[0]) == std_uid and str(res[1]) == std_mid and get_time_diff(str(res[3]), std_time) == 0:
                        count += 1
                if count >= 2:
                    key = str(std_uid) + ';' + str(std_mid)# + ';' + str(std_cid)
                    if key in result_dict:
                        return_dict[key].add(str(std_time))
                    else:
                        return_dict[key] = set()
                        return_dict[key].add(str(std_time))
    return return_dict


def save_result_into_file(feature_save_file_path, save_dict):
    with codecs.open(feature_save_file_path, 'w', 'utf-8') as feature_save_file:
        feature_save_file.write('user_key,x1' + '\n')
        for mid in save_dict:
            result_list = list(save_dict[mid])
            feature_save_file.write(str(mid) + ',' + ';'.join(result_list) + '\n')


online_train_file_path = '../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../tianchi_data/source_data/offline_test.csv'

time_lim = 15

result_dict = cal_user_get_coupon_in_recent(offline_train_file_path)
feature_save_file_path = '../feature_data/user_get_coupon_in_rencent.train_' + str(time_lim) + '.csv'
save_result_into_file(feature_save_file_path, result_dict)


result_dict = cal_user_get_coupon_in_recent(offline_test_file_path)
feature_save_file_path = '../feature_data/user_get_coupon_in_rencent.test_' + str(time_lim) + '.csv'
save_result_into_file(feature_save_file_path, result_dict)