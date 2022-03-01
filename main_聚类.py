import pandas as pd
import numpy as np
from Class_Hier_Cluster import Cluster, Classifier
from Class_IndData import IndData
import rank_tool as rk
import os
from other_tool import calculate_distance


text1 = '制造业聚类结果(分三类+股权性质)/'
df_capital_table = pd.DataFrame()
ind_code = []
ind_name = []
list1_code = []
list2_name = []
df_panel = pd.DataFrame()
df = pd.read_csv('./原始数据/连续样本2.csv')  # 这里用筛选出来的连续样本表
for code in rk.ind_code_list:
    if code not in ['C21', 'C24', 'C19', 'C20', 'C40', 'C41']:
        ind = IndData(df[df['行业代码'] == code].copy(), code)  # 创建行业数据容器对象，第一个参数为df， 第二个参数为行业代码
        input_df = ind.df_list[-1].copy()  # 读取行业数据容器中 df_list 的最后一个 df，也即2020年的数据，用于聚类
        input_df["年个股总市值（千元及剔除B股）"] = input_df["年个股总市值（千元及剔除B股）"] * 1000  # 换算单位
        input_df2 = input_df[["年个股总市值（千元及剔除B股）", "资产总计", "归属于母公司所有者权益合计",
                              "营业总收入", "利润总额"]].copy()  # 索引处用于聚类的五个维度指标
        nd = input_df2.to_numpy()  # 转化为 numpy 中的数组
        cluster = Cluster(nd, 3)  # 传入数组和需要分类的簇数
        print(ind.ind_code + ind.ind_name + '聚类完成！')
        T = cluster.T
        print(T)

        df_mergef = ind.df_list[-1]
        df_mergeb = df_mergef[['merge']].copy()
        df_mergeb = df_mergeb.rename(columns={'merge': 'merge2'})
        df_mergeb['分类标记'] = T  # 为最后一年数据贴上聚类标签

        ind.df = pd.merge(ind.df, df_mergeb, how='left', left_on='merge', right_on='merge2')
        ind.df.drop('merge2', axis=1, inplace=True)

        hand = Classifier(ind.df.copy(), '分类标记', ["年个股总市值（千元及剔除B股）", "资产总计", "归属于母公司所有者权益合计",
                                                  "营业总收入", "利润总额"])
        ind.df = hand.df_class

        cluster_list = []
        for i in range(1, 4):  # 根据分类个数确定 cluster_list 中元素的个数
            df_sub = ind.df[ind.df['分类结果'] == i].copy()
            cluster_list.append(df_sub)

        text2 = ind.ind_code + ind.ind_name  # 创捷保存聚类结果的相关文件夹
        os.makedirs(text1 + text2)

        path = text1 + text2 + '/' + text2 + '.xlsx'
        path_fig = text1 + text2 + '/树形结构图.png'
        print('正在保存：' + path)
        writer = pd.ExcelWriter(path)
        ind.df.to_excel(writer, sheet_name="总表")
        cluster_list[0].to_excel(writer, sheet_name="第一类")
        ind_code.append(ind.ind_code)  # 索引出头部企业的证券代码和证券简称
        ind_name.append(ind.ind_name)
        list1_code.append(cluster_list[0].iloc[0, 0])
        list2_name.append(cluster_list[0].iloc[0, 3])  # 索引出头部企业的证券代码和证券简称
        cluster_list[1].to_excel(writer, sheet_name="第二类")
        cluster_list[2].to_excel(writer, sheet_name="第三类")
        # cluster_list[3].to_excel(writer, sheet_name="第四类")
        # cluster_list[4].to_excel(writer, sheet_name="第五类")  # 分五类时，要考虑一些行业连续样本不足问题
        writer.save()
        writer.close()
        cluster.gen_dendrogram_fig(path_fig)

        t1 = str(len(cluster_list[0]))  # 输出分类结果的文本信息，并保存
        t2 = str(len(cluster_list[1]))
        t3 = str(len(cluster_list[2]))
        text = '在' + ind.ind_code + ind.ind_name + '中:\n' + \
               '第一类%s家；\n第二类%s家；\n第三类%s家\n' % (t1, t2, t3)
        path_txt = r'C:\Users\11596\Desktop\PycharmProjects\对上市企业的聚类任务/' + text1 + text2 + '.txt'
        file = open(path_txt, 'w')
        file.write(text)
        file.close()
        print('保存成功')

        # 将聚类完成的数据构造成面板数据
        df_first = cluster_list[0].copy()  # 聚类结果 DataFrame 列表中的第一个列表
        capital_code_list = []
        for i in df_first["Stkcd"]:
            capital_code_list.append(i)
        capital_df = ind.df[ind.df["Stkcd"].isin(capital_code_list)].copy()
        common_df = ind.df[~ind.df["Stkcd"].isin(capital_code_list)].copy()
        capital_df["year"] = capital_df["year"].astype("str")
        common_df["year"] = common_df["year"].astype("str")
        panel_sub = pd.merge(common_df, capital_df, how="left", on="year")
        print(panel_sub)
        df_panel = df_panel.append(panel_sub, ignore_index=True)

df_panel = calculate_distance(df_panel, ["latitude_x", "longitude_x", "latitude_y", "longitude_y"])
df_panel.to_excel(text1 + "panel.xlsx", sheet_name="panel", index=False)

df_capital_table["行业代码"] = ind_code
df_capital_table["行业名称"] = ind_name
df_capital_table["证券代码"] = list1_code
df_capital_table["证券简称"] = list2_name
df_capital_table.to_excel(text1 + "头部企业名单.xlsx", sheet_name="名单", index=False)
