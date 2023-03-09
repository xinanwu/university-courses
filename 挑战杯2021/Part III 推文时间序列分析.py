#!/usr/bin/env python
# coding: utf-8

# In[8]:


"""
-----------------------------------------说明--------------------------------------------

一、程序设计思路

    该部分旨在获取推文的时间分布信息并对其进行可视化。
    操作步骤如下：
    1)创建推文数量的时间序列;
    2)时间分布可视化。
    
（一）创建推文数量的时间序列：

    对于提取并加工数据集里的时间数据,笔者的想法是，为减少程序运算，首先分日期统计每日内推文
出现的时间（以小时为单位）与数量，再将所有分日期统计的数据排序并整合，最后生成时间序列数据框。
    
（二）时间分布可视化：

     依据以上生成的时间序列数据框画图，图的横坐标以日期和小时为单位，其中日期被标注在横坐标上，
纵坐标为推文数。

二、可视化结果解读

    对于时间序列图的解读可从两个方面展开。首先，从1月4日到1月9日，每隔一天就会有一次讨论的高峰，
并且推文的数量也越来越多，说明随着时间的推移，参与讨论的人越来越多，参与的热度也逐渐上升；而聚焦
于一日之内，则会发现一般在早晨和傍晚会有两个讨论的小高峰，这可能反映出占发推用户大对数的美国用户
的作息时间（这也符合一般人的作息规律），而其他时段的小高峰则有一部分可能是其他国家/地区的用户造成
的（由于时差）。

    此外，可以发现在非就寝时间内每小时发推数量基本都在5条及以上（大部分在5-10条之间，高峰时可达20
甚至30条以上，并且每小时都有人发推），平均每天的发推数量在200条左右，可见推文的数量很密集，说明这是
一场用户参与激情较高的讨论。

    总而言之，这是一场用户参与激情较高且参与人数和热度随时间推移逐渐上升的讨论。

-----------------------------------------------------------------------------------------
"""




"""
创建推文数量的时间序列
"""

import openpyxl 
import pandas as pd 
import matplotlib #用于绘图
import matplotlib.pyplot as plt  



##读取数据集
workbook=openpyxl.load_workbook("数据集.xlsx")
worksheet=workbook.worksheets[0]



##分日期提取推文的小时信息
def hour(hour_list, day):#定义推文提取函数

    k = -1#防止超出范围
    for c in list(worksheet.columns)[3]:
        k += 1
        if c.value == day:   
           hour_list.append(str((list(worksheet.columns)[5])[k].value))
       
    return hour_list

Mon_Jan_04 = []#创建日期列表
Tue_Jan_05 = []
Wed_Jan_06 = []
Thu_Jan_07 = []
Fri_Jan_08 = []

Mon_Jan_04 = hour(Mon_Jan_04, 'Mon Jan 04')#将提取的内容添加到列表中
Tue_Jan_05 = hour(Tue_Jan_05, 'Tue Jan 05')
Wed_Jan_06 = hour(Wed_Jan_06, 'Wed Jan 06')
Thu_Jan_07 = hour(Thu_Jan_07, 'Thu Jan 07')
Fri_Jan_08 = hour(Fri_Jan_08, 'Fri Jan 08')

##分别统计不同日期列表中每小时的推文数
def cnt(hour_list,hour_dict):
    for t in hour_list:
        if t in hour_dict.keys():
           hour_dict[t] = hour_dict[t] + 1
        else:
           hour_dict[t] = 1

    return hour_dict

cnt_Mon_Jan_04 = {}#分日期创建“小时-数量”字典
cnt_Tue_Jan_05 = {}
cnt_Wed_Jan_06 = {}
cnt_Thu_Jan_07 = {}
cnt_Fri_Jan_08 = {}

cnt_Mon_Jan_04 = cnt(Mon_Jan_04, cnt_Mon_Jan_04)
cnt_Tue_Jan_05 = cnt(Tue_Jan_05, cnt_Tue_Jan_05)
cnt_Wed_Jan_06 = cnt(Wed_Jan_06, cnt_Wed_Jan_06)
cnt_Thu_Jan_07 = cnt(Thu_Jan_07, cnt_Thu_Jan_07)
cnt_Fri_Jan_08 = cnt(Fri_Jan_08, cnt_Fri_Jan_08)

##修改部分错误信息
def delete(hour_dict):
    for k in list(hour_dict.keys()):
        if k == '1899-12-30 00:00:00':
           hour_dict['00:00:00'] = hour_dict.pop(k)
    return hour_dict

cnt_Mon_Jan_04 = delete(cnt_Mon_Jan_04)
cnt_Tue_Jan_05 = delete(cnt_Tue_Jan_05)
cnt_Wed_Jan_06 = delete(cnt_Wed_Jan_06)
cnt_Thu_Jan_07 = delete(cnt_Thu_Jan_07)
cnt_Fri_Jan_08 = delete(cnt_Fri_Jan_08)

#在分小时统计的推文信息前增加日期
def add_date(date,hour_dict):
    for k in list(hour_dict.keys()):
        hour_dict[date + ' ' + k] = hour_dict.pop(k)
    return hour_dict

cnt_Mon_Jan_04 = add_date('2016-01-04', cnt_Mon_Jan_04)
cnt_Tue_Jan_05 = add_date('2016-01-05', cnt_Tue_Jan_05)
cnt_Wed_Jan_06 = add_date('2016-01-06', cnt_Wed_Jan_06)
cnt_Thu_Jan_07 = add_date('2016-01-07', cnt_Thu_Jan_07)
cnt_Fri_Jan_08 = add_date('2016-01-08', cnt_Fri_Jan_08)



##创建时间序列字典，整合分日期的字典
time_series = {}

time_series.update(cnt_Mon_Jan_04)
time_series.update(cnt_Tue_Jan_05)
time_series.update(cnt_Wed_Jan_06)
time_series.update(cnt_Thu_Jan_07)
time_series.update(cnt_Fri_Jan_08)

time_series= dict(sorted(time_series.items(),key=lambda x:x[0]))#按日期与小时排序



##将字典转换为数据框
time_series = pd.DataFrame.from_dict(time_series,orient = 'index', columns= ['count'])
time_series = time_series.reset_index().rename(columns = {'index':'time'})

time_series['datetime'] = pd.to_datetime(time_series['time'])
time_series = time_series.set_index('datetime')
time_series.drop(['time'], axis=1, inplace=True)



"""
可视化
"""

plt.figure(figsize=(15, 7))
plt.plot(time_series)
plt.title('Time Series Plot of Tweets')
plt.grid(True)
plt.show()


# In[ ]:




