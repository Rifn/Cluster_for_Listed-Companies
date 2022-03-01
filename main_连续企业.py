import pandas as pd
import numpy as np
# from Class_Hier_Cluster import Cluster
from Class_IndData import IndData
import rank_tool as rk


file_path = "./原始数据/合并表（是否国企）.csv"
df = pd.read_csv(file_path)

li = []
df_cs = pd.DataFrame()
i = 1
for code in rk.ind_code_list:
    df_ind = df[df["行业代码"] == code].copy()
    car = IndData(df_ind.copy(), code)
    # save_path = "./连续样本处理结果/" + car.ind_code + car.ind_name + ".xlsx"
    # writer = pd.ExcelWriter(save_path)
    # car.df_continuity.to_excel(writer, sheet_name="连续样本", index=False)
    # writer.save()
    # writer.close()
    # del writer
    # li.append(len(car.df_continuity))
    if i == 1:
        df_cs = car.df_continuity_sample
    else:
        df_cs = df_cs.append(car.df_continuity_sample, ignore_index=True)
    print(car.df_continuity_sample)
    i += 1
# df2 = pd.DataFrame()
# # df2["行业代码"] = rk.ind_code_list
# # df2["行业名称"] = rk.ind_name_list
# # df2["连续企业家数"] = li
# # df2.to_excel("./处理结果/连续企业家数.xlsx", index=False)

df_cs.drop("code", axis=1, inplace=True)
df_cs.to_excel('./连续样本2.xlsx', index=False)
