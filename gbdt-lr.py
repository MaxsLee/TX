# coding: utf-8
from sklearn import metrics

import numpy as np
import lightgbm as lgb
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import math

print("Load data...")
df_data_train = pd.read_csv(r'F:\WorkSpace\tpai\1\train5.txt',header = None ,sep=',',encoding='gbk')
X_train = df_data_train.drop(len(df_data_train.keys())-1,axis = 1)
print(np.array(X_train).shape)
y_train = df_data_train[len(df_data_train.keys())-1]


# create dataset for light gbm
lgb_train = lgb.Dataset(X_train,y_train)
# lgb_eval = lgb.Dataset(X_test,y_test,reference=lgb_train)

# specify your configuration as a dict
params = {
    'task' : 'train',
    'application' : 'binary',
    'boosting_type' : 'gbdt',
    'learning_rate' : 0.001,
    'num_leaves' : 32,
    'feature_fraction': 0.9 ,
    'bagging_fraction':  0.8 ,
    'bagging_freq' : 5 ,
    'verbose': 0 ,
    'metric' : 'binary_logloss'
}

num_leaf = 32

print('Start training...')
gbm = lgb.train(params,lgb_train,num_boost_round= 100,valid_sets=lgb_train)

print('Start predicting...')
y_pred = gbm.predict(X_train,pred_leaf = True)
print('Writing transformed training data')
transformed_training_matrix  = np.zeros([len(y_pred),len(y_pred[0])*num_leaf ] , dtype = np.int64)
for i in range (0,len(y_pred)):
    temp = np.arange(len(y_pred[0])) * num_leaf -1 + np.array(y_pred[i])
    transformed_training_matrix[i][temp] += 1

# Logistic Regression start
print('Logistic Regression Start')
lm = LogisticRegression(penalty='l2',C=0.05)
lm.fit(transformed_training_matrix,y_train)
df_data_test = []
with open(r'F:\WorkSpace\tpai\1\test_features_encode.txt',encoding='utf-8') as fr:
    for line in fr:
        tmp = []
        data = line.strip().split(',')
        for x in data:
            tmp.append(float(x))
        df_data_test.append(tmp)
cnt = 1
with open(r'F:\WorkSpace\tpai\1\result.csv','w') as fw:
    for line in df_data_test:
        X_test = line
        # print(X_test)
        y_pred = gbm.predict(X_test,pred_leaf=True)
        print(cnt)
        transformed_testing_matrix  = np.zeros([len(y_pred),len(y_pred[0])*num_leaf ] , dtype = np.int64)
        for i in range (0,len(y_pred)):
            temp = np.arange(len(y_pred[0])) * num_leaf -1 + np.array(y_pred[i])
            transformed_testing_matrix[i][temp] += 1
        y_pred_est = lm.predict_proba(transformed_testing_matrix)[:,1]
        for x in y_pred_est:
            fw.write(str(cnt)+','+str(x)+'\n')
            cnt += 1
# fp = 0
# fn = 0
# tp = 0
# tn = 0
# array_len = len(predicted)
# print(array_len)
# for i in range(array_len):
#     if predicted[i] != y_test_list[i]:
#         if predicted[i] == 1 and y_test_list[i] == 0:
#             fp +=1
#         else:
#             fn += 1
#     else:
#         if predicted[i]  == 1:
#             tp += 1
#         else:
#             tn += 1
# print(tp,fp,tn,fn)
# MCC = (tp*tn-fp*fn)/math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
# print(MCC)
# print (metrics.classification_report(y_test_list,predicted))
# print ("log loss %f"%metrics.log_loss(y_test,y_pred_est))
# fpr ,tpr ,thresholds = metrics.roc_curve(y_test,y_pred_est)
# print('AUC %f'%metrics.auc(fpr,tpr))
# #对角线
# plt.plot([0, 1],[0, 1],'--',color=(0.6, 0.6, 0.6),label = 'Luck')
# plt.plot(fpr,tpr)
# plt.xlim([-0.05,1.05])
# plt.ylim=([-0.05,1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver operation characteristic curve')
# plt.legend(loc='lower right')
    #plt.show()
#NE = (-1) / len(y_pred_est) * sum(((1+y_test)/2 * np.log(y_pred_est[:,1]) +  (1-y_test)/2 * np.log(1 - y_pred_est[:,1])))

#print("Normalized Cross Entropy " + str(NE))