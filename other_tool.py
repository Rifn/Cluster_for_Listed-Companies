import pandas as pd
from geopy.distance import geodesic


def calculate_distance(your_df, column4_list):
    """
    根据原表所给经纬度信息，计算出两地球面距离，并返回
    :param your_df: 一个包含了两地经纬度信息的 DataFrame 结构
    :param column4_list: 一个包含四个元素的列表参数，依次为：
                         1> 第一地维度信息所在列名；
                         2> 第一地经度信息所在列名；
                         3> 第二地维度信息所在列名；
                         4> 第二地经度信息所在列明.
    :return: 返回一个 DataFrame，相比原表多了 distance 列
    """
    list_dis = []
    columns_list = list(your_df.columns)
    print(columns_list)
    index_lat1 = columns_list.index(column4_list[0])  # 找出传入列名参数在 df 中的列序号
    index_longit1 = columns_list.index(column4_list[1])
    index_lat2 = columns_list.index(column4_list[2])
    index_longit2 = columns_list.index(column4_list[3])
    for i in range(0, len(your_df)):
        x1 = your_df.iloc[i, index_lat1]
        y1 = your_df.iloc[i, index_longit1]
        x2 = your_df.iloc[i, index_lat2]
        y2 = your_df.iloc[i, index_longit2]
        tuple1 = (x1, y1)
        tuple2 = (x2, y2)
        print(tuple1, tuple2)
        distance = geodesic(tuple1, tuple2).km  # 计算公式代码
        list_dis.append(distance)
        print(distance)
    your_df["distance"] = list_dis
    return your_df
