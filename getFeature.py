import random
def get_user_dict(file,user_dict):
    with open(file,encoding = 'gbk',errors='ignore') as fr:
        for line in fr:
            user_profile= line.split('\t')
            if(len(user_profile)==16):
                uid = user_profile[0]
                if(user_dict.get(uid) is None):
                    user_dict[uid] = line
    return  user_dict

def get_video_dict(file,video_dict):
    with open(file,encoding='gbk',errors = 'ignore') as fr:
        for line in fr:
            video_info = line.split('\t')
            if(len(video_info) == 8):
                vid = video_info[0]
                if(video_dict.get(vid) is None):
                    video_dict[vid] = line
    return  video_dict

def read_some_file(file):
    _list = []
    with open(file,encoding='utf-8') as fr:
        for line in fr:
            _list.append(line[0:-1])
    return  _list

def get_user_browser(broswer):
    return  broswer.split('\\')[-1].lower()
def get_user_interest(interest):
    interest_dict=dict()
    interestes = interest.split('#')
    for x in interestes:
        interest_detail = x.split('|')
        if(len(interest_detail) == 2):
            interest_dict[interest_detail[0]] = interest_detail[1]
    return interest_dict
def get_user_district(district):
    district_dict  = dict()
    districts = district.split('#')
    for x in districts:
        district_detail = x.split('%')
        if(len(district_detail) == 2):
            district_dict[district_detail[0]] = district_detail[1]
    return  district_dict
def get_user_videotype(video_type):
    video_type_dict = dict()
    video_sub_type_dict = dict()
    video_types = video_type.split('#')
    for x in video_types:
        video_type_detail = x.split('%')
        type_and_subtype = video_type_detail[0].split('@')
        if len(video_type_detail) ==2:
            if len(type_and_subtype)  == 2:
                try:
                    video_type_dict[int(type_and_subtype[0])] = video_type_detail[1]
                    video_sub_type_dict[type_and_subtype[1]] = video_type_detail[1]
                except:
                    pass
            else:
                video_sub_type_dict[type_and_subtype[0]] = video_type_detail[1]
    return video_type_dict , video_sub_type_dict
def get_user_director(director):
    director_dict = dict()
    directors = director.split('#')
    for x in directors:
        director_detail  = x.split('%')
        if len(director_detail) == 2:
            director_dict[director_detail[0]] = director_detail[1]
    return  director_dict

def get_user_actor(actor):
    actor_dict = dict()
    actors = actor.split('#')
    for x in actors:
        actor_detail  = x.split('%')
        if len(actor_detail) == 2:
            actor_dict[actor_detail[0]] = actor_detail[1]
    return  actor_dict
def get_videotype(video):
    video_list = video.split('|')
    return  video_list
def get_video_director(director):
    return  director.split('|')
def get_video_actor(actor):
    return  actor.split('|')
def readFile(file):
    #key 为 uid ,value 为 对应的用户信息
    user_dict=dict()
    #key 为 vid ,value为对应的视频信息
    video_dict=dict()
    user_dict=get_user_dict(r'F:\video_click_data2\user_profile.txt',user_dict)
    video_dict=get_video_dict(r'F:\video_click_data2\video_info.txt',video_dict)

    #获取挑选出来的兴趣\导演\演员等
    interest_list=read_some_file(r'F:\tencent\user_interest.txt')
    browser_list = read_some_file(r'F:\tencent\browser.txt')
    video_type_list = read_some_file(r'F:\tencent\video_type.txt')
    district_list = read_some_file(r'F:\tencent\districts.txt')
    director_list = read_some_file(r'F:\tencent\director.txt')
    actor_list = read_some_file(r'F:\tencent\actor.txt')

    with open(file , encoding='gbk') as fr:
        with open(r'D:\tencentvideos\xxxx.txt','w',encoding='utf-8') as fw:
            count_line = 0
            for line in fr:
                count_line = count_line + 1
                if count_line%10000 ==0:
                    print(count_line*1.0/19389877)
                user_watch_data = line.split()
                if(len(user_watch_data) == 5):
                    user_profile = user_dict.get(user_watch_data[2])
                    video_info = video_dict.get(user_watch_data[3])
                    if user_profile is not None and video_info is not None:
                        user_profile_detail = user_profile.split('\t')
                        video_info_detail = video_info.split('\t')
                        if(len(user_profile_detail) ==16 and len(video_info_detail) == 8):
                            ############################
                            user_actor = []
                            video_actor = []
                            user_directore = []
                            video_director = []
                            user_district = []
                            video_district = []
                            user_video_type = []
                            video_type = []
                            user_video_sub_type = []
                            video_sub_type = []
                            ############################
                            feature = []
                            #活跃天数
                            if user_profile_detail[1] == 'NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp=int(user_profile_detail[1])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            print(len(feature))
                            #默认浏览器
                            user_broswer = get_user_browser(user_profile_detail[2])
                            for x in browser_list:
                                if user_broswer == x:
                                    feature.append(1)
                                else:
                                    feature.append(0)
                            print(len(feature))
                            #cpu核数
                            if user_profile_detail[3] == 'NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp=int(user_profile_detail[3])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            print(len(feature))
                            #内存
                            if user_profile_detail[4] =='NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp=int(user_profile_detail[4])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            print(len(feature))
                            #共存浏览器
                            if user_profile_detail[5] == 'NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp =int(user_profile_detail[5])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            print(len(feature))
                            #共存安全软件
                            if user_profile_detail[6] == 'NULL':
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(user_profile_detail[6])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            print(len(feature))
                            #大类兴趣标签
                            interest_dict = get_user_interest(user_profile_detail[7])
                            if interest_dict is None:
                                for x in interest_list:
                                    feature.append(0)
                            else:
                                for x in interest_list:
                                    if x in interest_dict.keys():
                                        try:
                                            tmp = int(interest_dict[x])
                                            feature.append(tmp)
                                        except:
                                            feature.append(0)
                                    else:
                                        feature.append(0)
                            print(len(feature))
                            #视频地区标签
                            district_dict = get_user_district(user_profile_detail[8])
                            if district_dict is None:
                                for x in district_list:
                                    feature.append(0)
                            else:
                                for x in district_list:
                                    if x in district_dict.keys():
                                        try:
                                            tmp = int(district_dict[x])
                                            feature.append(tmp)
                                        except:
                                            feature.append(0)
                                    else:
                                        feature.append(0)
                            print(len(feature))
                            #视频类型标签(包括视频大类和子类)
                            video_type_dict ,video_sub_type_dict= get_user_videotype(user_profile_detail[9])
                            for i in range(14):
                                if video_type_dict is None:
                                    feature.append(0)
                                else:
                                    if(video_type_dict.get(i) is None):
                                        feature.append(0)
                                    else:
                                        try:
                                            tmp = int(video_type_dict.get(i))
                                            feature.append(tmp)
                                        except:
                                            feature.append(0)
                            for x in  video_type_list:
                                if video_sub_type_dict is None:
                                    feature.append(0)
                                else:
                                    if video_sub_type_dict.get(x) is None:
                                        feature.append(0)
                                    else:
                                        try:
                                            tmp = int(video_sub_type_dict.get(x))
                                            feature.append(tmp)
                                        except:
                                            feature.append(0)
                            print(len(feature))
                            #导演
                            director_dict = get_user_director(user_profile_detail[10])
                            if director_dict is None:
                                for x in director_list:
                                    feature.append(0)
                            else:
                                for x in director_list:
                                    if x in director_dict.keys():
                                        try:
                                            tmp = int(director_dict[x])
                                            feature.append(tmp)
                                        except:
                                            feature.append(0)
                                    else:
                                        feature.append(0)
                            print(len(feature))
                            #演员
                            actor_dict = get_user_actor(user_profile_detail[11])
                            if actor_dict is None:
                                for x in actor_list:
                                    feature.append(0)
                            else:
                                for x in actor_list:
                                    if x in actor_dict.keys():
                                        try:
                                            tmp = int(actor_dict[x])
                                            feature.append(tmp)
                                        except:
                                            feature.append(0)
                                    else:
                                        feature.append(0)
                            print(len(feature))
                            #性别，年龄，学历
                            if(user_profile_detail[13]=='NULL'):
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(user_profile_detail[13])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)

                            if (user_profile_detail[14] == 'NULL'):
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(user_profile_detail[14])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            if (user_profile_detail[15] == 'NULL'):
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(user_profile_detail[15][0:-1])
                                    #(tmp)
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            print(len(feature))
                            #视频大类类型
                            if(video_info_detail[2] == 'NULL'):
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(video_info_detail[2])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            print(len(feature))
                            #视频子类型
                            v_video_type_list=get_videotype(video_info_detail[3])
                            for x in video_type_list:
                                if x in v_video_type_list:
                                    feature.append(1)
                                else:
                                    feature.append(0)
                            print(len(feature))
                            #导演
                            v_director_list = get_video_director(video_info_detail[4])
                            for x in director_list:
                                if x in v_director_list:
                                    feature.append(1)
                                else:
                                    feature.append(0)
                            print(len(feature))
                            #演员
                            v_actor_list = get_video_actor(video_info_detail[5])
                            for x in actor_list:
                                if x in v_actor_list:
                                    feature.append(1)
                                else:
                                    feature.append(0)
                           # print(len(feature))
                            #上映年份
                            if(video_info_detail[6] == 'NULL'):
                                feature.append(0)
                            else:
                                try:
                                    tmp = int(video_info_detail[6])
                                    feature.append(tmp)
                                except:
                                    feature.append(0)
                            #print(len(feature))
                            #地区
                            for x in district_list:
                                if x == video_info_detail[7][0:-1]:
                                    #print(video_info_detail[7][0:-1])
                                    feature.append(1)
                                else:
                                    feature.append(0)
                            #print(len(feature))
                            #######人工交叉特征
                            #用户年龄和视频上映年份
                            #用户导演标签和视频导演标签
                            #用户演员标签和视频演员标签
                            #用户视频地区标签视频地区标签
                            #用户感兴趣的视频大类标签和视频大类标签
                            #用户感兴趣的视频子类型标签和视频子类型标签



                            feature.append(1)
                            count = 0
                            feature_len = len(feature)
                            random_number = random.uniform(0,10)
                            if random_number<0.08:
                                for x in feature:
                                    count = count+1
                                    fw.write(str(x))
                                    if count!=feature_len:
                                        fw.write(',')
                                fw.write('\n')




if __name__=='__main__':
    readFile(r'F:\tencent\valid_watch_data.txt')