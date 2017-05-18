# coding: utf-8
from sklearn import metrics

import numpy as np
import lightgbm as lgb
import  pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import math

print("Load data...")
# df_data = pd.read_csv(r'D:\tencentvideos\10-1-600-test.txt',header=None, sep=',',encoding='gbk')
# X = df_data.drop(len(df_data.keys())-1,axis=1)
# y = df_data[len(df_data.keys())-1]
# # X = df_data.drop(0,axis=1)
# # y = df_data[0]
# X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.6,random_state=31,stratify=y)
#
#
# print(X_train.__class__)
# with open('train.txt','w',encoding='utf-8') as fw:
#     cnt = 0
#     yy_train = list(y_train)
#     yy_test = list(y_test)
#     for index,row in X_train.iterrows():
#         for x in row:
#             fw.write(str(x)+',')
#         fw.write(str(yy_train[cnt]) + '\n')
#         cnt += 1
# with open('test.txt','w',encoding='utf-8') as fw:
#     cnt = 0
#     for index, row in X_test.iterrows():
#         for x in row:
#             fw.write(str(x) + ',')
#         fw.write(str(yy_test[cnt]) + '\n')
#         cnt += 1

#
df_data_train = pd.read_csv(r'F:\WorkSpace\tpai\1\train4.txt', header=None, sep=',', encoding='gbk')
X_train = df_data_train.drop(len(df_data_train.keys())-1, axis=1)
print(np.array(X_train).shape)
y_train = df_data_train[len(df_data_train.keys())-1]
df_data_test = pd.read_csv(r'F:\WorkSpace\tpai\1\test4.txt', header=None, sep=',', encoding='gbk')
X_test = df_data_test.drop(len(df_data_test.keys())-1, axis=1)
print(np.array(X_test).shape)
y_test = df_data_test[len(df_data_test.keys())-1]
# min_max_scaler = preprocessing.MinMaxScaler()
# X_train_normalized = min_max_scaler.fit_transform(np.mat(X_train))
# X_test_normalized = min_max_scaler.transform(np.mat(X_test))
y_test_list = list(y_test)
# create dataset for light gbm
lgb_train = lgb.Dataset(X_train,y_train)
lgb_eval = lgb.Dataset(X_test,y_test,reference=lgb_train)

# specify your configuration as a dict
params = {
    'task': 'train',
    'application': 'binary',
    'boosting_type': 'gbdt',
    'learning_rate': 0.001,
    'num_leaves': 64,
    'feature_fraction': 0.9,
    'bagging_fraction':  0.8,
    'bagging_freq': 5,
    'verbose': 0,
    'metric': 'binary_logloss'
}

num_leaf = 64

print('Start training...')
gbm = lgb.train(params, lgb_train, num_boost_round=100, valid_sets=lgb_eval)

print('Start predicting...')
y_pred = gbm.predict(X_train, pred_leaf=True)
# with open('y_pred.txt','w',encoding='utf-8') as fw:
#     for line in y_pred:
#         for x in line:
#             fw.write(str(x)+',')
#         fw.write('\n')
print('Writing transformed training data')
transformed_training_matrix = np.zeros([len(y_pred), len(y_pred[0])*num_leaf], dtype=np.int64)
yy_train = list(y_train)
yy_test = list(y_test)
# with open('tree_feature_train.txt','w',encoding='utf-8') as fw:
# print(y_pred[0],y_pred[1],len(y_pred))
for i in range(0, len(y_pred)):
    temp = np.arange(len(y_pred[0])) * num_leaf - 1 + np.array(y_pred[i])
    transformed_training_matrix[i][temp] += 1
    # cnt = 0
    # for line in transformed_training_matrix:
    #     for x in line:
    #         fw.write(str(x)+',')
    #     fw.write(str(yy_train[cnt])+'\n')
    #     cnt += 1
y_pred = gbm.predict(X_test, pred_leaf=True)
print('Writing transformed testing data')
transformed_testing_matrix = np.zeros([len(y_pred), len(y_pred[0])*num_leaf], dtype=np.int64)
# with open('tree_feature_test.txt','w',encoding='utf-8') as fw:
for i in range(0, len(y_pred)):
    temp = np.arange(len(y_pred[0])) * num_leaf -1 + np.array(y_pred[i])
    transformed_testing_matrix[i][temp] += 1
    # for i in range(len(transformed_testing_matrix[0])):
    #     fw.write(str(i))
    #     if(i!=len(transformed_testing_matrix[0])):
    #         fw.write(',')
    # fw.write('\n')
    # cnt = 0
    # for line in transformed_testing_matrix:
    #     for x in line:
    #         fw.write(str(x)+',')
    #     fw.write(str(yy_test[cnt])+'\n')
    #     cnt += 1

# Logistic Regression start
print('Logistic Regression Start')

c = np.array([1, 0.1, 0.05, 0.02, 0.01, 0.005])
for t in range(0, len(c)):
    lm = LogisticRegression(penalty='l2', C=c[t])
    lm.fit(transformed_training_matrix, y_train)
    predicted = lm.predict(transformed_testing_matrix)
    # scores = lm.decision_function(transformed_testing_matrix)
    y_pred_est = lm.predict_proba(transformed_testing_matrix)[:, 1]
    fp = 0
    fn = 0
    tp = 0
    tn = 0
    array_len = len(predicted)
    print(array_len)
    for i in range(array_len):
        if predicted[i] != y_test_list[i]:
            if predicted[i] == 1 and y_test_list[i] == 0:
                fp += 1
            else:
                fn += 1
        else:
            if predicted[i] == 1:
                tp += 1
            else:
                tn += 1
    print(tp, fp, tn, fn)
    MCC = (tp*tn-fp*fn)/math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    print(MCC)
    print(metrics.classification_report(y_test_list, predicted))
    print("log loss %f" % metrics.log_loss(y_test, y_pred_est))
    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred_est)
    print('AUC %f' % metrics.auc(fpr, tpr))
    # #对角线
    # plt.plot([0, 1],[0, 1],'--',color=(0.6, 0.6, 0.6),label = 'Luck')
    # plt.plot(fpr,tpr)
    # plt.xlim([-0.05,1.05])
    # plt.ylim=([-0.05,1.05])
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('Receiver operation characteristic curve')
    # plt.legend(loc='lower right')
    # plt.show()
# NE = (-1) / len(y_pred_est) * sum(((1+y_test)/2 * np.log(y_pred_est[:,1]) +  (1-y_test)/2 * np.log(1 - y_pred_est[:,1])))

# print("Normalized Cross Entropy " + str(NE))
