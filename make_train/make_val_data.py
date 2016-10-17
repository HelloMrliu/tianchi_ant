# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs
import os

online_train_file_path = '../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../tianchi_data/source_data/offline_test.csv'

def make_new_feaature_list(file_path, std_id_list, stname):
    id_value_dict = dict()
    result_list = list()
    with codecs.open(file_path, 'r', 'utf-8') as feature_data_file:
        count = 0
        for feature_data in feature_data_file:
            if count == 0:
                count += 1
                continue
            feature_data_list = feature_data.strip('\n').split(',')
            std_id = str(feature_data_list[0])
            value = str(feature_data_list[1])
            id_value_dict[std_id] = value

    for index in range(len(std_id_list)):
        std_id = str(std_id_list[index])
        if std_id not in id_value_dict:
            value = '0.00'
        else:
            value = id_value_dict[std_id]
        result_list.append(value)
    return result_list
'''

uid_cunpon_liveness_15.csv
0.297067198178
mid_buy_liveness_15.csv
0.0314160971906
uid_coupon_active_15.csv
0.870833333333
mid_coupon_active_15.csv
0.0192482915718
uid_buy_liveness_15.csv
0.543014426727
mid_cunpon_liveness_15.csv
0.000721336370539

def make_new_feaature_list(file_path, std_id_list, stname):
    id_value_dict = dict()
    result_list = list()
    with codecs.open(file_path, 'r', 'utf-8') as feature_data_file:
        count = 0
        for feature_data in feature_data_file:
            if count == 0:
                count += 1
                continue
            feature_data_list = feature_data.strip('\n').split(',')
            std_id = str(feature_data_list[0])
            value = str(feature_data_list[1])
            id_value_dict[std_id] = value

    count = 0

    for index in range(len(std_id_list)):
        std_id = str(std_id_list[index])
        if std_id not in id_value_dict:
            value = '1.00'
            count += 1
        else:
            value = id_value_dict[std_id]
        result_list.append(value)

    print stname
    print float(count) / len(std_id_list)
    return result_list
'''


def make_new_combine_feature(file_path, uid_list, mid_list):
    count = 0
    id_value_dict = dict()
    result_list = list()
    with codecs.open(file_path, 'r', 'utf-8') as feature_data_file:
        for feature_data in feature_data_file:
            feature_data_list = feature_data.strip('\n').split(',')
            std_id = str(feature_data_list[0])
            std_value = feature_data_list[1]
            temp_set = set()
            value_list = std_value.split(';')
            for mid in value_list:
                temp_set.add(str(mid))
            id_value_dict[std_id] = temp_set

    for index in range(len(uid_list)):
        uid = str(uid_list[index])
        if uid in id_value_dict:
            temp_set = id_value_dict[uid]
            mid = str(mid_list[index])
            if mid in temp_set:
                count += 1
                value = '1'
            else:
                value = '0'
        else:
            value = '0'
        result_list.append(value)
    print "connection:"
    print float(count) / len(result_list)
    return result_list


def read_user_get_cunpon_in_recente(file_path, uid_list, mid_list):
    count = 0
    id_value_dict = dict()
    result_list = list()
    with codecs.open(file_path, 'r', 'utf-8') as feature_data_file:
        count = 0
        for feature_data in feature_data_file:
            if count == 0:
                count += 1
                continue
            feature_data_list = feature_data.strip('\n').split(',')
            key = feature_data_list[0]
            value = feature_data_list[1]
            id_value_dict[key] = value

    for index in range(len(uid_list)):
        uid = str(uid_list[index])
        mid = str(mid_list[index])
        key = uid + ';' + mid
        if key in id_value_dict:
            value = '1'
        else:
            value = '0'
        result_list.append(value)
    print 'user_get_coupon_in:'
    print float(count) / len(result_list)
    return result_list


feature_data_dir_path = '../feature_data/'
like_train_file_path = '../train_data/like_val_data.csv'
save_file_path = '../train_data/val_data.csv'

like_train_data = source_data = pd.read_csv(like_train_file_path)

uid_list = like_train_data['uid']
mid_list = like_train_data['mid']
cid_list = like_train_data['cid']
discount_list = like_train_data['discount']
top_discount_list = like_train_data['top_discount']
distance_list = like_train_data['distance']
label_list = like_train_data['label']

result_list = list()
title_list = list()
for file_name in os.listdir(feature_data_dir_path):
    file_path = feature_data_dir_path + file_name

    if 'mid' in file_name:
        temp_result_list = make_new_feaature_list(file_path, mid_list, file_name)
    elif 'uid' in file_name:
        temp_result_list = make_new_feaature_list(file_path, uid_list, file_name)
    elif 'cid' in file_name:
        temp_result_list = make_new_feaature_list(file_path, cid_list, file_name)
    elif 'user_get_coupon' in file_name:
        if 'train' in file_name:
            temp_result_list = read_user_get_cunpon_in_recente(file_path, uid_list, mid_list)
        else:
            continue
    else:
        temp_result_list = make_new_combine_feature(file_path, uid_list, mid_list)

    title_list.append(file_name.split('.')[0])
    result_list.append(temp_result_list)

'''
temp_result_list = be_user_model.get_result_list(like_train_file_path)
title_list.append('user_same_cunpon_time_number')
result_list.append(temp_result_list)
'''

feature_list = list()
for index in range(len(cid_list)):
    uid = uid_list[index]
    mid = mid_list[index]
    cid = cid_list[index]
    discount = discount_list[index]
    top_discount = top_discount_list[index]
    distance = distance_list[index]

    temp_list = list()
    temp_list.append(str(uid))
    temp_list.append(str(mid))
    temp_list.append(str(cid))
    temp_list.append(str(discount))
    temp_list.append(str(top_discount))
    temp_list.append(str(distance))

    feature_list.append(temp_list)

for temp_val_list in result_list:
    for index in range(len(temp_val_list)):
        temp_feature_list = feature_list[index]
        temp_feature_list.append(temp_val_list[index])


for index in range(len(feature_list)):
    temp_list = feature_list[index]
    label = label_list[index]
    temp_list.append(str(label))


with codecs.open(save_file_path, 'w', 'utf-8') as save_file:
    save_file.write('uid,mid,cid,discount,top_discount,distance,' + ','.join(title_list) + ',label' + '\n')
    for val_list in feature_list:
        save_file.write(','.join(val_list) + '\n')

