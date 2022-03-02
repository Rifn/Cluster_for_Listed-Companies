import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import linkage, ward, fcluster, leaders, dendrogram
from scipy.spatial.distance import pdist
import matplotlib.pylab as plt
import pandas as pd
import numpy as np


class Classifier:  # 对输入的数据表按照其某列分类标记赋予其经济含义，判断出哪个标记类别位于行业头部
    def __init__(self, your_df, anchor, columns):
        self.df = your_df
        self.anchor = anchor
        self.cal_columns = columns  # 用于计算距离用到的列名列表
        self.num = self.count()  # 找出数据表中 anchor 列（分类标记）中的类别数目
        self.gen_list_dis()
        self.df_list = self.gen_list()  # 生成不同类别的数据表的列表

        self.df_class = self.rank()

    def count(self):
        list1 = []
        for i in self.df[self.anchor]:
            list1.append(i)
        lenth = len(set(list1))
        return lenth

    def gen_list(self):
        df_list = []
        for i in range(1, self.num + 1):
            df_sub = self.df[self.df[self.anchor] == i].copy()
            df_list.append(df_sub)
        return df_list

    def gen_list_dis(self):
        self.df['distance'] = [0] * len(self.df)
        for name in self.cal_columns:
            self.df['distance'] = self.df['distance'] + self.df[name] ** 2
        self.df['distance'] = np.sqrt(self.df['distance'])

    def rank(self):
        list1 = list(range(1, self.num + 1))
        list2 = []
        df_little = pd.DataFrame()
        for i in range(1, self.num + 1):
            df_sub = self.df_list[i-1].copy()
            dis = 0
            for m in df_sub['distance']:
                dis = dis + m
            if len(df_sub) != 0:
                dis = dis / len(df_sub)
            list2.append(dis)
            del df_sub

        df_little['table'] = list1
        df_little['dis'] = list2
        df_little.sort_values(by='dis', axis=0, ascending=False, inplace=True)
        df_little['分类结果'] = list(range(1, self.num + 1))

        dfcs = pd.merge(self.df, df_little, how='left', left_on=self.anchor, right_on='table')

        dfcs.drop(['distance', 'table', 'dis'], axis=1, inplace=True)
        print(dfcs)
        return dfcs


class Cluster:
    def __init__(self, ndarray, num):
        self.X = ndarray
        self.Z = self.gen_Z('average', 'euclidean')

        # fig = plt.figure(figsize=(25, 10))
        self.P = dendrogram(self.Z)
        # plt.savefig('./picture.png')

        self.cluster_num = num
        self.real_num = 0
        self.T = self.try_fcluster()

    def gen_Z(self, method, metric):
        Z = linkage(pdist(self.X), method, metric)
        return Z

    def try_fcluster(self):
        t1 = 0
        p1 = 1000000000
        x = 1
        while True:
            T_list = fcluster(self.Z, t1, 'distance')
            self.real_num = len(set(T_list))
            print('第%d次聚类，当前分了%d类,t1=%f,p1=%f' % (x, self.real_num, t1, p1))

            if self.real_num > self.cluster_num:
                t1 += p1
                x += 1
            elif self.real_num < self.cluster_num:
                p1 *= 0.5
                t1 -= p1
                x += 1
            elif self.real_num == self.cluster_num:
                break
        return fcluster(self.Z, t1, 'distance')

    def gen_dendrogram_fig(self, save_path):
        fig = plt.figure(figsize=(25, 10))
        P = dendrogram(self.Z)
        plt.savefig(save_path)


# X = [[0, 0], [0, 1], [1, 0],
#      [0, 4], [0, 3], [1, 4],
#      [4, 0], [3, 0], [4, 1],
#      [4, 4], [3, 4], [4, 3]]
# this = Cluster(X)
# print(this.X)
# print(this.Z)
# print(this.T)

# df = pd.read_csv('testfile.csv')
# print(df)
# nd = df.to_numpy()
# print(nd)
#
# this = Cluster(nd, 3)
# print(this.T)
# file_path = "./聚类结果/fig.png"
# this.gen_dendrogram_fig(file_path)


df = pd.DataFrame([[0, 1], [0, 1], [1, 2],
                   [0, 4], [0, 3], [1, 4],
                   [4, 1], [3, 3], [4, 1],
                   [4, 4], [3, 4], [4, 3]], columns=['a', 'b'])
print(df)
hand = Classifier(df, 'b', ['a'])
print(hand.df_class)
