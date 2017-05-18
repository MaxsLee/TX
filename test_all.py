#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import codecs
import time
from itertools import islice
user_file_name = 'user.csv'
position_file_name = 'position.csv'
ad_file_name = 'ad.csv'
app_categories_file_name = 'app_categories.csv'
train_file_name = 'train.csv'
test_file_name = 'test.csv'


def test_hometown_number():
    sig = os.path.sep  # 分隔符
    current_path = os.getcwd()  # 获取当前路径
    user_file = current_path + sig + 'pre' + sig + user_file_name  # user.csv
    province_list = list()
    city_list = list()
    with codecs.open(user_file, mode='r') as read_user:
        for line in islice(read_user, 1, None):
            features = line.strip().split(',')
            hometown = int(features[-2])
            residence = int(features[-1])
            province = residence / 100
            city = residence % 100
            province_list.append(province)
            city_list.append(city)
    province_list = list(set(province_list))
    city_list = list(set(city_list))
    province_list.sort()
    city_list.sort()
    print('province:')
    print(province_list)
    print('city:')
    print(city_list)


def test_position():
    sig = os.path.sep  # 分隔符
    current_path = os.getcwd()  # 获取当前路径
    ad_file = current_path + sig + 'pre' + sig + position_file_name  # ad.csv
    position_type_list = list()
    with codecs.open(ad_file, mode='r') as read_user:
        for line in islice(read_user, 1, None):
            features = line.strip().split(',')
            position_type = features[-1]
            position_type_list.append(position_type)
    position_type_list = list(set(position_type_list))
    position_type_list.sort()
    print(position_type_list)


def test_feature():
    file_name = os.getcwd()+os.path.sep+'features_encode.txt'
    with codecs.open(file_name, mode='r') as read_file:
        for line in read_file:
            print(line.strip())
            time.sleep(1)


if __name__ == '__main__':
    # test_feature()
    print(int(int(0)/100))

