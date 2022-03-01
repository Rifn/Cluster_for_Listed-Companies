import pandas as pd
import numpy as np


ind_code_list = ['C13', 'C14', 'C15', 'C17', 'C18', 'C19', 'C20', 'C21',
                 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29',
                 'C30', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37',
                 'C38', 'C39', 'C40', 'C41']
capital_scale_list = [4, 3, 4, 7, 4, 2, 1, 3, 4, 2, 2, 2, 25, 22, 3, 9, 8, 5, 5, 4, 12,
                      15, 5, 3, 14, 21, 5, 2]
ind_name_list = ['农副食品加工业', '食品制造业', '酒、饮料和精制茶制造业',
                 '纺织业', '纺织服装、服饰业', '皮革、毛皮、羽毛及其制品和制鞋业',
                 '木材加工及木、竹、藤、棕、草制品业', '家具制造业', '造纸及纸制品业',
                 '印刷和记录媒介复制业', '文教、工美、体育和娱乐用品制造业',
                 '石油加工、炼焦及核燃料加工业', '化学原料及化学制品制造业',
                 '医药制造业', '化学纤维制造业', '橡胶和塑料制品业', '非金属矿物制品业',
                 '黑色金属冶炼及压延加工业', '有色金属冶炼及压延加工业', '金属制品业',
                 '通用设备制造业', '专用设备制造业', '汽车制造业',
                 '铁路、船舶、航空航天和其它运输设备制造业', '电气机械及器材制造业',
                 '计算机、通信和其他电子设备制造业', '仪器仪表制造业', '其他制造业']
sample_period = list(range(2008, 2021))


def process_code(df, process_column):
    df[process_column] = df[process_column].astype("str")
    code_list = []
    for i in df[process_column]:
        code_list.append(("0" * (6 - len(i))) + i)
    df[process_column] = code_list
    return df


def add_rank_value(df, your_anchor_list):
    df["rank_value"] = [0] * len(df)
    rank_name_list = []
    for anchor in your_anchor_list:
        rank_name_list.append("rank_" + anchor[0:2])
    for anchor in your_anchor_list:
        df.sort_values(by=anchor, axis=0, ascending=False, inplace=True)
        list_rank_value = list(range(0, len(df)))
        rank_name = rank_name_list[your_anchor_list.index(anchor)]
        df[rank_name] = list_rank_value
        df["rank_value"] = df["rank_value"] + df[rank_name]
    df["rank_value"] = df["rank_value"] / len(your_anchor_list)
    df.sort_values(by="rank_value", axis=0, ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def check_continuity(df_list, check_columns, returnwhat):  # 返回封装样本期间连续代码的DataFrame
    list_list = []
    for df in df_list:  # 给df列表中的每一个df创建剔除年份的代码序列
        merge_code_list = []  # 创建一个剔除年份的代码列
        for i in df[check_columns]:
            merge_code_list.append(i[0:6])  # 创建一个剔除年份的代码列
        list_list.append(merge_code_list)
    union_list = []
    for i in range(13):
        union_list = list(set(list_list[i]).union(set(union_list)))
    continuity_list = union_list.copy()
    del union_list
    for i in range(13):
        continuity_list = list(set(list_list[i]) & set(continuity_list))
    continuity_df = pd.DataFrame()
    continuity_df["code"] = continuity_list
    if returnwhat is True:
        return continuity_df
    else:
        return continuity_list


def adjust_df_year(df_list, df_continuity):
    df_list_adjust = []
    for df_year in df_list:
        df_year_adjust = pd.merge(df_continuity, df_year, left_on="code",
                                  right_on="Stkcd", how="left")
        df_year_adjust.reset_index(drop=True, inplace=True)
        df_list_adjust.append(df_year_adjust)
        del df_year_adjust
    return df_list_adjust


def calculation_rank_value(df_list_adjust, df_continuity):
    df_continuity["rank_value"] = [0] * len(df_continuity)
    year = int(2008)
    for df_year_adjust in df_list_adjust:
        df_continuity["rank_value"] = df_continuity["rank_value"] + df_year_adjust["rank_value"]
        df_continuity["rank_value_" + str(year)] = df_year_adjust["rank_value"]
        year += 1
    df_continuity["rank_value"] = df_continuity["rank_value"] / 13
    df_continuity.sort_values(by="rank_value", axis=0, ascending=True, inplace=True)
    df_continuity.reset_index(drop=True, inplace=True)
    return df_continuity


def get_capital_code_list(df, capital_n):
    df_capital = df.head(capital_n).copy()
    capital_code_list = []
    for i in df_capital["code"]:
        capital_code_list.append(i)
    del df_capital
    return capital_code_list


def row_sum(x):
    if x.name == "Stkcd":
        return np.nan
    elif x.name in ["year", "行业名称", "行业代码", "报表类型"]:
        li = []
        for i in x:
            li.append(i)
        return li[0]
    elif x.name == "merge":
        return np.nan
    elif x.name == "证券简称":
        return "capital"
    else:
        return x.sum()











