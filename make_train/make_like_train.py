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


source_file_path = offline_train_file_path
source_data = pd.read_csv(source_file_path)
uid_list = source_data['uid']
mid_list = source_data['mid']
cid_list = source_data['cid']
discount_list = source_data['discount']
distance_list = source_data['distance']
date_received_list = source_data['date_received']
date_list = source_data['date']

sub_count = 0
save_list = list()
for index in range(len(cid_list)):
    uid = uid_list[index]
    mid = mid_list[index]
    cid = cid_list[index]
    discount = discount_list[index]
    distance = distance_list[index]
    date_received = date_received_list[index]
    date = date_list[index]

    if cid != 'null':
        temp_list = list()
        temp_list.append(str(uid))
        temp_list.append(str(mid))
        temp_list.append(str(cid))
        discount_spl = discount.split(':')
        if len(discount_spl) == 2:
            temp_list.append(str("%.2f" % (float(discount_spl[1]) / float(discount_spl[0]))))
            temp_list.append(str("%.2f" % float(discount_spl[0])))
        else:
            temp_list.append(str(discount))
            temp_list.append(str("%.2f" % float('1.00')))
        if distance == 'null':
            temp_list.append('-1')
        else:
            temp_list.append(str(distance))

        if date != 'null':
            if get_time_diff(date_received, date) <= 15:
                temp_list.append('1')
                sub_count += 1
            else:
                temp_list.append('0')
        else:
            temp_list.append('0')

        save_list.append(temp_list)

print sub_count
print len(cid_list)

with codecs.open('../train_data/like_train_data.csv','w','utf-8') as save_file:
    save_file.write('uid,mid,cid,discount,top_discount,distance,label\n')
    for line_list in save_list:
        save_file.write(','.join(line_list))
        save_file.write('\n')


#75382
#1053282
#1754884