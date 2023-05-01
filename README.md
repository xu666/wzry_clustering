## 环境准备

Python3.6或以上

第三方包：

- opencv-python==3.4.0.14
- numpy
- openpyxl
- pandas
- scikit-learn
- sklearn

## 使用方法

1. 在`原始数据.xls`中填写数据
2. 如果有新英雄，则需要在heroes文件夹内补充英雄头像，必须是三通道jpg图片
3. 修改`main.py`中的参数，尤其是要统计的表单、要统计的列、梯度数量
4. 运行`main.py`，或者解压`_ENV.7z`到当前文件夹后双击`run.bat`
5. 在控制台窗口查看输出文字，在`output`文件夹查看梯度图片

## 补充说明

得到的结果不一定相同，因为K-means是随机算法（大部分机器学习算法都有随机性）