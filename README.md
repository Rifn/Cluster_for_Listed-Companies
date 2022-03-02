# Cluster_for_Listed-Companies
上市企业分类任务。使用机器学习的层次聚类方法对上市企业进行分类，得到每个行业的企业分类结果，并按行业输出分类数据结果和树形结构图，以及符合条件的面板数据。
#使用说明
##1.所需库和第三方库
OS,  
Pandas, Scipy, Numpy  
自写脚本：rank_tool, other_tool, Class_Hier_Cluster, Class_IndData  
##2.运行脚本
main_聚类
main_聚类（稳健性检验）  
##3.注意  
1.重新运行需删除已生成的文件夹“制造业聚类结果（分三类）  
2.可于脚本Class_Hier_Cluster中line67修改Cluster类别的初始化参数"num"选择聚类产生结果中类别的个数  
