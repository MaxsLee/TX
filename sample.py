import random


def loadDataSet(fileName):
    dataMat = []
    with open(fileName, encoding='utf-8') as fr:
        for line in fr:
            dataMat.append(line)
    print(len(dataMat[0]))
    return dataMat


def RandomSampling(dataMat,number):
    try:
        slice = random.sample(dataMat,number)
        return slice
    except:
        print('Sample larger than population')


if __name__ == '__main__':
    # train
    dataMat = loadDataSet(r'F:\WorkSpace\tpai\1\features_encode_1.txt')
    ss = RandomSampling(dataMat, 20000)
    with open(r'F:\WorkSpace\tpai\1\train5_1.txt', 'w', encoding='utf-8') as fw:
        for s in ss:
            fw.write(s)

    # test
    # dataMat = loadDataSet(r'F:\WorkSpace\tpai\1\features_encode_1.txt')
    # ss = RandomSampling(dataMat, 300)
    # with open(r'F:\WorkSpace\tpai\1\test4_1.txt', 'w', encoding='utf-8') as fw:
    #     for s in ss:
    #         fw.write(s)
