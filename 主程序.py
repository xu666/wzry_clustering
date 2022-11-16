import cv2
import numpy as np
import pandas as pd
import pypinyin
from sklearn.cluster import KMeans

canvas = None  # 当前画布（可容纳一行英雄）
k_current = 0  # 当前画布上已有的英雄头像数目


def generate_pic(data, k=3, margin_h=10, margin_v=20, margin_v_min=10, a=90, pic_name='temp', show_pic=False):
    """
    生成梯度排行图片

    :param data: 排行数据, 二维list
    :param k: 每行最大图片数
    :param margin_h:水平间隙
    :param margin_v:垂直间隙
    :param margin_v_min:软换行垂直间隙
    :param a: 图片边长
    :param pic_name: 图片名称
    :param show_pic: 是否显示
    :return: 生成的图片
    """
    canvas_list = []  # 画布集合

    def get_pic(hero_name, a_=90):
        if '.jpg' in hero_name:
            hero_name = hero_name.replace('.jpg', '')
        im = cv2.imdecode(np.fromfile(f'./heroes/{hero_name}.jpg', dtype=np.uint8), -1)
        im = cv2.resize(im, (a_, a_))
        return im

    def show(img_):
        cv2.imshow('', img_)
        cv2.waitKey()

    def add_canvas(big=False):
        global k_current, canvas
        w = k * a + (k - 1) * margin_h  # 画布宽
        h = a + (margin_v if big else margin_v_min)  # 画布高
        if k_current != 0:
            canvas_list.append(canvas)
        canvas = np.zeros((h, w, 4), dtype='uint8')  # 创建四通道画布
        k_current = 0

    def insert(img_):
        global k_current, canvas
        y1 = k_current * (a + margin_h)
        canvas[-a:, y1:y1 + a, :3] = img_
        canvas[-a:, y1:y1 + a, 3] = 255
        k_current += 1
        if k_current >= k:
            add_canvas()

    for group in data:
        add_canvas(big=True)
        for hero in group:
            insert(get_pic(hero, a))

    add_canvas()

    final_pic = np.vstack(canvas_list)
    if pic_name:
        cv2.imwrite(f"./output/{pic_name}.png", final_pic)
    if show_pic:
        show(final_pic)
    return final_pic


def get_rank(col='分数', header='小国标'):
    """
    根据表格数据计算梯度, 并生成梯度文字/图片

    :param col: 统计数据所在的列名称
    :param header: 标题当中的备注
    :return: 无
    """
    df = pd.read_excel(r'./原始数据.xls')
    x = df[col].values.reshape(-1, 1)
    k_means = KMeans(n_clusters=5, random_state=0).fit(x)

    centers = k_means.cluster_centers_.reshape(-1)
    labels = k_means.labels_

    d = {value: i for i, value in enumerate(np.argsort(-centers))}
    y = [d[label] for label in labels]

    df['梯度'] = [f'T{i}' for i in y]

    def get_data(role_):
        return df[df['分路'].str.contains(role_)].sort_values(col, ascending=False)

    print(f'国服分({header})梯度排行（安卓Q区，基于k-means聚类算法）')
    print('by 果果分水果\n')

    for role in ['对抗路', '中路', '发育路', '打野', '游走']:
        data = get_data(role)
        print(f'【{role}】')
        lst = []
        for i in range(5):
            part = data[data['梯度'] == f'T{i}']
            heroes = part['英雄'].values.tolist()
            s = ' '.join(heroes) if heroes else '无'
            print(f'T{i}: {s}')
            lst.append(heroes)

        generate_pic(lst, k=12, margin_h=15, margin_v=30, margin_v_min=5, pic_name=pypinyin.slug(role))
        print('')


if __name__ == '__main__':
    get_rank('分数', '大国标')
