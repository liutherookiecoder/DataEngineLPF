"""
汽车消费城市划分：
数据集：car_data.csv
31个省份地区，4个维度的指标（人均GDP，城镇人口比重，交通工具消费价格指数，百户拥有汽车量）
Thinking：将城市划分为几组，哪些城市会是在一组？
"""
# 使用KMeans进行聚类
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np

# 数据加载
#data = pd.read_csv('Mall_Customers.csv', encoding='gbk')
data = pd.read_csv('F:/python/数据分析课程/L3/Data_Engine_with_Python-master/Data_Engine_with_Python-master/L3/car_data.csv',encoding="gbk")
train_x = data[["人均GDP","城镇人口比重","交通工具消费价格指数", "百户拥有汽车量"]]
#print(train_x)
#print(data)

# 规范化到 [0,1] 空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
pd.DataFrame(train_x).to_csv('temp.csv', index=False)
#print(train_x)

# K-Means 手肘法：统计不同K取值的误差平方和
import matplotlib.pyplot as plt
sse = []
for k in range(1, 11):
	# kmeans算法
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(train_x)
	# 计算inertia簇内误差平方和
	sse.append(kmeans.inertia_)
x = range(1, 11)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')
plt.show()

# 使用KMeans聚类，可取最优簇数为4
kmeans = KMeans(n_clusters=4)
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
print(predict_y)


# 合并聚类结果，插入到原数据中
result = pd.concat([data,pd.DataFrame(predict_y)],axis=1)
result.rename({0:u'聚类结果'},axis=1,inplace=True)
print(result)
# 将结果导出到CSV文件中
result.to_csv("customer_cluster_result.csv",index=False)



