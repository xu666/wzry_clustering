## 环境准备

Python3.6或以上

第三方包：

- opencv-python
- numpy
- xlrd
- pandas
- pypinyin
- scikit-learn
- sklearn

## 使用方法

1. 在`原始数据.xls`中填写数据
2. 如果有新英雄，则需要在heroes文件夹内补充英雄头像，必须是三通道jpg图片
3. 运行`主程序.py`
4. 在控制台窗口查看输出文字，在`output`文件夹查看梯度图片

## 补充说明

得到的结果不一定相同，因为K-means是随机算法（大部分机器学习算法都有随机性）