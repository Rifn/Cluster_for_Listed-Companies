import pandas as pd
import rank_tool as rk


class IndData:
    def __init__(self, df_industry, ind_code):
        self.df = rk.process_code(df_industry, "Stkcd")
        self.ind_code = ind_code
        self.ind_name = rk.ind_name_list[rk.ind_code_list.index(ind_code)]
        self.capital_n = rk.capital_scale_list[rk.ind_code_list.index(ind_code)]
        self.sample_period = rk.sample_period

        self.df_list = self.gen_df_list()
        self.df_list_value = self.add_rank_value_all(['资产总计', '营业收入', "年个股总市值（千元及剔除B股）"])
        self.df_continuity = rk.check_continuity(self.df_list_value, 'merge', True)  # 返回样本期
        # 间内连续样本的股票代码的两种格式
        self.df_list_adjust = rk.adjust_df_year(self.df_list_value, self.df_continuity)
        # 【注意】df_list_adjust中的df与df_continuity中的代码序列一致，calculation_rank_value
        # 的计算结果才有效
        self.df_con = rk.calculation_rank_value(self.df_list_adjust.copy(), self.df_continuity.copy())
        self.capital_code_list = rk.get_capital_code_list(self.df_con, self.capital_n)
        self.capital_df = self.gen_c_df()  # 返回容纳2008-2020期间的capital_code的数据
        self.common_df = self.gen_com_df()
        self.capital_df2 = self.gen_simple_df(self.capital_df,
                                              [1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17,
                                               18, 19, 20, 21, 22])
        self.common_df2 = self.gen_simple_df(self.common_df, [1, 2, 3, 4, 5, 6, 7, 11, 12,
                                                              13, 14, 15, 16, 17,
                                                              18, 19, 20, 21, 22])
        self.panel_data = self.gen_panel()
        self.df_continuity_sample = self.continuity_sample()
        print('行业' + self.ind_code + self.ind_name + '创建成功！')

    def gen_df_list(self):
        li = []
        for year in self.sample_period:
            df_year = self.df[self.df["year"] == year].copy()
            df_year.reset_index(drop=True, inplace=True)
            li.append(df_year)
            del df_year
        return li

    def add_rank_value_all(self, your_anchor_list):
        df_list_value = []
        for df_year in self.df_list:
            copy = df_year.copy()
            df_list_value.append(rk.add_rank_value(copy, your_anchor_list))
            del copy
        return df_list_value

    def gen_c_df(self):
        copy1 = self.df[self.df["Stkcd"].isin(self.capital_code_list)].copy()
        copy1.reset_index(drop=True, inplace=True)
        return copy1

    def gen_com_df(self):
        copy2 = self.df[~self.df["Stkcd"].isin(self.capital_code_list)].copy()
        copy2.reset_index(drop=True, inplace=True)
        return copy2

    def gen_simple_df(self, dfsim, col_list):
        copy = dfsim.copy()
        col_name_li = []
        for i in col_list:
            col_name_li.append(copy.columns[i-1])
        dfs = pd.DataFrame()
        for name in col_name_li:
            dfs[name] = copy[name].copy()
        del copy
        return dfs

    def gen_panel(self):
        df_common = self.common_df2.copy()
        df_capital = self.capital_df2.copy()
        df_sum = pd.DataFrame()
        for year in self.sample_period:
            df_year_capital = df_capital[df_capital["year"] == year].copy()
            df_year_capital.loc["row_sum"] = df_year_capital.apply(rk.row_sum)
            df_sum = df_sum.append(df_year_capital.loc["row_sum"], ignore_index=True)
        df_sum["year"] = df_sum["year"].astype("int")
        df_sum.drop("Stkcd", axis=1, inplace=True)
        df_sum.drop("merge", axis=1, inplace=True)
        df_sum_merge = pd.DataFrame()
        df_sum_merge = pd.merge(df_common, df_sum, on="year", how="left")
        return df_sum_merge

    def continuity_sample(self):
        list1 = []
        list2 = []
        df_cs = pd.DataFrame()
        for i in self.df_continuity["code"]:
            list1.append(i)
        for i in list1:
            for y in range(2008, 2021):
                str1 = str(y)
                str2 = i + '-' + str1
                list2.append(str2)
        df_cs["code"] = list2
        df_cs = pd.merge(df_cs, self.df, how="left", left_on="code", right_on="merge")
        return df_cs
