"""
最肯忘却古人诗，最不屑一顾是相思
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from utils import generate_pic

# 设置一些必要的参数
sheet = '202304'  # 想要统计的表单
cols = ['大国Q修正', '小国Q修正']  # 想要统计的列

# 初始化
df: pd.DataFrame = pd.read_excel('./原始数据.xls', sheet_name=sheet)  # 读取数据
df = df.sort_values('英雄')  # 按英雄名称排序

for col in cols:
    x = df[col].values.reshape(-1, 1)  # 读取数据列
    k_means = KMeans(n_clusters=5, random_state=0).fit(x)  # 对选取的列一维聚类

    centers = k_means.cluster_centers_.reshape(-1)  # 获取每一簇的中心
    labels = k_means.labels_  # 原始分簇结果

    # 获取梯度排行结果（按簇中心从大到小，依次命名为T0~T4）
    d = {value: i for i, value in enumerate(np.argsort(-centers))}
    y = [d[label] for label in labels]
    col_tidu = f'梯度({col})'
    df[col_tidu] = [f'T{i}' for i in y]

    # 打印梯度排行结果
    print(f'梯度排行结果（{col}）')
    for role in ['对抗路', '中路', '发育路', '打野', '游走']:
        data = df[df['分路'].str.contains(role)].sort_values(col, ascending=False)
        print(f'【{role}】')
        lst = []
        for i in range(5):
            part = data[data[col_tidu] == f'T{i}']
            heroes = part['英雄'].values.tolist()
            s = ' '.join(heroes) if heroes else '无'
            print(f'T{i}: {s}')
            lst.append(heroes)

        # 拼接生成该分路的图片（在output文件夹）
        generate_pic(lst, a=50, m=6, margin_h=6, margin_in=4, margin_out=16, pic_name=f'{role}{col}')
        print('')

if __name__ == '__main__':
    pass
