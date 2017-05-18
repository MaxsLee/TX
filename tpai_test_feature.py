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


# appID	appCategory
def app_categories_features(app_categories_file):
    app_categories_dict = dict()
    with codecs.open(app_categories_file, mode='r') as read_user:
        for line in islice(read_user, 1, None):
            line_list = line.strip().split(',')
            app_categories_dict[line_list[0]] = line.strip()
    # for key in app_categories_dict.keys():
    #     print(key, user_dict[key])
    return app_categories_dict


# creativeID	adID	camgaignID	advertiserID	appID	appPlatform
def ad_features(ad_file):
    add_dict = dict()
    with codecs.open(ad_file, mode='r') as read_user:
        for line in islice(read_user, 1, None):
            line_list = line.strip().split(',')
            add_dict[line_list[0]] = line.strip()
    # for key in add_dict.keys():
    #     print(key, user_dict[key])
    return add_dict


# positionID	sitesetID	positionType
def position_features(position_file):
    position_dict = dict()
    with codecs.open(position_file, mode='r') as read_user:
        for line in islice(read_user, 1, None):
            line_list = line.strip().split(',')
            position_dict[line_list[0]] = line.strip()
    # for key in position_dict.keys():
    #     print(key, user_dict[key])
    return position_dict


# userID	age	gender	education	marriageStatus	haveBaby	hometown	residence
def user_features(user_file):
    user_dict = dict()
    with codecs.open(user_file, mode='r') as read_user:
        for line in islice(read_user, 1, None):
            line_list = line.strip().split(',')
            user_dict[line_list[0]] = line.strip()
    # for key in user_dict.keys():
    #     print(key, user_dict[key])
    return user_dict


def get_tpai_features():
    sig = os.path.sep                           # separator
    current_path = os.getcwd()                  # current path
    test_features_encode_txt = current_path+sig+'test_features_encode.txt'
    if os.path.exists(test_features_encode_txt):
        os.remove(test_features_encode_txt)

    user_file = current_path + sig + 'pre' + sig + user_file_name  # user.csv
    position_file = current_path + sig + 'pre' + sig + position_file_name
    ad_file = current_path + sig + 'pre' + sig + ad_file_name
    app_categories_file = current_path + sig + 'pre' + sig + app_categories_file_name
    # train_file = current_path + sig + 'pre' + sig + train_file_name
    test_file = current_path + sig + 'pre' + sig + test_file_name

    user_dict = user_features(user_file)
    position_dict = position_features(position_file)
    ad_dict = ad_features(ad_file)
    app_categories_dict = app_categories_features(app_categories_file)

    # write test_features_encode.txt
    with codecs.open(test_features_encode_txt, mode='w') as write_test_features_txt:
        # read train.csv
        with codecs.open(test_file, mode='r') as read_test:
            for line in islice(read_test, 1, None):
                one_hot_encoding_list = list()
                # print(line.strip())
                line_list = line.strip().split(',')
                # print(line_list)
                instance_id = line_list[0]
                creative_id = line_list[-5]
                user_id = line_list[-4]
                position_id = line_list[-3]
                connection_type = line_list[-2]
                telecoms_operator = line_list[-1]
                # print(label, creative_id, user_id, position_id, connection_type, telecoms_operator)
                # time.sleep(2)

                # encoding start
                # train.csv
                # connectionType
                connection_type_list = [0 for i in range(5)]
                connection_type_list[int(connection_type)] = 1
                one_hot_encoding_list.extend(connection_type_list)
                # telecomsOperator
                telecoms_operator_list = [0 for i in range(4)]
                telecoms_operator_list[int(telecoms_operator)] = 1
                one_hot_encoding_list.extend(telecoms_operator_list)

                # user.csv
                user_line = user_dict[user_id].strip()
                user, age, gender, education, marriage_status, have_baby, hometown, residence = user_line.split(',')
                # age
                age_list = [0 for i in range(6)]
                age_index = 0
                if (int(age) > 0) and (int(age) <= 20):
                    age_index = 1
                elif (int(age) > 20) and (int(age) <= 25):
                    age_index = 2
                elif (int(age) > 25) and (int(age) <= 30):
                    age_index = 3
                elif (int(age) > 30) and (int(age) <= 50):
                    age_index = 4
                elif int(age) > 51:
                    age_index = 5
                age_list[age_index] = 1
                one_hot_encoding_list.extend(age_list)
                # gender
                gender_list = [0 for i in range(3)]
                gender_list[int(gender)] = 1
                one_hot_encoding_list.extend(gender_list)
                # education
                education_list = [0 for i in range(8)]
                education_list[int(education)] = 1
                one_hot_encoding_list.extend(education_list)
                # marriage_status
                marriage_list = [0 for i in range(4)]
                marriage_list[int(marriage_status)] = 1
                one_hot_encoding_list.extend(marriage_list)
                # have_baby
                baby_list = [0 for i in range(7)]
                baby_list[int(have_baby)] = 1
                one_hot_encoding_list.extend(baby_list)
                # hometown
                home_province_list = [0 for i in range(35)]
                home_city_list = [0 for i in range(22)]
                home_province = int(hometown) / 100
                home_city = int(hometown) % 100
                home_province_list[int(home_province)] = 1
                home_city_list[int(home_city)] = 1
                one_hot_encoding_list.extend(home_province_list)
                one_hot_encoding_list.extend(home_city_list)
                # residence
                res_province_list = [0 for i in range(35)]
                res_city_list = [0 for i in range(22)]
                res_province = int(residence) / 100
                res_city = int(residence) % 100
                res_province_list[int(res_province)] = 1
                res_city_list[int(res_city)] = 1
                one_hot_encoding_list.extend(res_province_list)
                one_hot_encoding_list.extend(res_city_list)

                # position.csv
                position_line = position_dict[position_id].strip()
                position, siteset_id, position_type = position_line.split(',')
                # position_type
                position_type_list = [0 for i in range(6)]
                position_type_list[int(position_type)] = 1
                one_hot_encoding_list.extend(position_type_list)

                # ad.csv
                ad_line = ad_dict[creative_id].strip()
                creative, ad_id, campaign_id, advertiser_id, app_id, app_platform = ad_line.split(',')
                # app_platform
                app_platform_list = [0 for i in range(3)]
                app_platform_list[int(app_platform)] = 1
                one_hot_encoding_list.extend(app_platform_list)

                # app_categories.csv
                app_categories_line = app_categories_dict[app_id].strip()
                app, app_category = app_categories_line.split(',')
                # app_category
                first_category = int(app_category) / 100
                second_category = int(app_category) % 100
                app_category_first_list = [0 for i in range(6)]
                app_category_second_list = [0 for i in range(12)]
                app_category_first_list[int(first_category)] = 1
                app_category_second_list[int(second_category)] = 1
                one_hot_encoding_list.extend(app_category_first_list)
                one_hot_encoding_list.extend(app_category_second_list)

                # # the last is label
                # one_hot_encoding_list.append(int(label))

                # encoding end
                record = str(one_hot_encoding_list).replace('[', '').replace(']', '').replace(' ', '')
                write_test_features_txt.write(record+'\n')
                # list_a = record.split(',')
                # print(len(list_a))    # 179
                # break


if __name__ == '__main__':
    print('start...')
    get_tpai_features()
    print('end...')
