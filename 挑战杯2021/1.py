from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.datasets import register_url
# 如果出现 ssl 异常再加下面这两行
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

register_url("https://echarts-maps.github.io/echarts-countries-js/")
#将数据处理成列表
locate = ['Amazonas','Antioquia','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','重庆','四川','贵州','云南','陕西','甘肃','青海','宁夏','新疆']

GDP_1978 = [108.84,82.65,183.06,87.99,58.04,229.20,81.98,174.80,272.81,249.24,123.72,114.10,66.37,87.00,225.45,162.92,151.00,146.99,185.85,75.85,16.40,67.32,184.61,46.62,69.05,81.07,64.73,15.54,13.00,39.07]

GDP_2017 = [28014.94,18549.19,34016.32,15528.42,16096.21,23409.24,14944.53,15902.68,30632.99,85869.76,51768.26,27018,32182.09,20006.31,72634.15,44552.83,35478.09,33902.96,89705.23,18523.26,4462.54,19424.73,36980.22,13540.83,16376.34,21898.81,7459.9,2624.83,3443.56,10881.96]
list1 = [[locate[i],GDP_1978[i]] for i in range(len(locate))]
list2 = [[locate[i],GDP_2017[i]] for i in range(len(locate))]

map_1 = Map()

map_1.set_global_opts(
    title_opts=opts.TitleOpts(title="Colombian protest statistics"),
    visualmap_opts=opts.VisualMapOpts(max_=100000)  #最大数据范围
    )
map_1.add("Total number of protests", list1, maptype="哥伦比亚")
map_1.add("Number of violent protests", list2, maptype="哥伦比亚")
#map_1.add("Number of peaceful protests", list3, maptype="Colombia")
map_1.render('map1.html')