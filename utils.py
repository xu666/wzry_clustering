import cv2
import numpy as np
import pypinyin


def read_hero_pic(hero_name, size=90):
    """ 读取英雄图片 """
    if '.jpg' in hero_name:
        hero_name = hero_name.replace('.jpg', '')
    im = cv2.imdecode(np.fromfile(f'./heroes/{hero_name}.jpg', dtype=np.uint8), -1)
    im = cv2.resize(im, (size, size))
    return im


def show_pic(img_, title=''):
    """ 显示图片 """
    cv2.imshow(str(title), img_)
    cv2.waitKey()


def generate_pic(data, a=30, m=5, margin_h=5, margin_in=10, margin_out=20, pic_name='temp'):
    """
    生成梯度图片

    :param data: 梯度排行结果，形如[['梦奇','盘古'],['刘邦','苏烈','孙膑']]
    :param a: 英雄头像边长
    :param m: 每行容纳的英雄数量
    :param margin_h: 英雄头像水平间距
    :param margin_in: 英雄头像垂直间距 - 梯度内
    :param margin_out: 英雄头像垂直间距 - 梯度间
    :param pic_name: 保存的图片名称
    :return: 图片
    """
    canvas_list = []  # 画布列表
    k = max(m, (max([len(heroes) for heroes in data]) + 1) // 2)  # 每行容纳的英雄数目

    for group in data:
        # 创建画布
        w = k * a + (k - 1) * margin_h  # 画布宽
        h = 2 * a + margin_in + margin_out  # 画布高
        canvas = np.zeros((h, w, 4), dtype='uint8')  # 创建画布（四通道）

        # 填充英雄头像
        n = len(group)  # 该梯度级别的英雄数量
        for i, hero in enumerate(group):
            if n <= k:  # 共一行
                x1 = (h - a) // 2
                y1 = i * (a + margin_h)
            else:  # 共两行
                if i < k:  # 两行的第一行
                    x1 = margin_out // 2
                    y1 = i * (a + margin_h)
                else:  # 两行的第二行
                    x1 = a + margin_out // 2 + margin_in
                    y1 = (i - k) * (a + margin_h)
            x2, y2 = x1 + a, y1 + a
            img = read_hero_pic(hero, a)
            canvas[x1:x2, y1:y2, :3] = img
            canvas[x1:x2, y1:y2, 3] = 255

        canvas_list.append(canvas)

    final_pic = np.vstack(canvas_list)  # 合并所有画布
    cv2.imwrite(f"./output/{pypinyin.slug(pic_name)}.png", final_pic)
    return final_pic


if __name__ == '__main__':
    generate_pic([[], ['梦奇'] * 2, ['梦奇'] * 10, ['梦奇'] * 12, ['梦奇'] * 6])
