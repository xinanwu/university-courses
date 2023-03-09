#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
-----------------------------------------说明---------------------------------------------

一、程序设计思路

    该部分旨在获取推文的地理分布信息并对其进行可视化。
    操作步骤如下：
    1)数据清理与描绘地理坐标;
    2)地理分布可视化。
    
（一）数据清理与描绘地理坐标：

    和推文内容相似，用户的地理信息同样极其庞杂，不仅含有大量的缺失值，地理坐标也五花八门，因
此必须对其进行清理。

    首先，对于地理坐标图，笔者的思路为，采用地理坐标点呈现用户的地理信息，因此必须选取最低能
精确到省、州级别的地理单位。

    首先，只选取能被stanza识别为地理命名实体的用户地理信息；接着，从中去除国家一级的地理单位
和缩写（因为容易被识别错），这样保留的只有省、州及其以下级别的地理单位。虽然这样做造成了巨大
的信息损失（数据集中本来含有1079条推文，经过处理后仅剩614条）,但是这既是原始数据的问题，同时
为了可视化的效果也不得不这么做。（此外，因为上述原因，笔者为保证数据量（如果只保留市级及以下
的地理单位，那么仅剩505条），将省级和市级地理单位混杂，也造成了一定的信息混乱。）

    然后，以已经过处理的地理信息为素材，为每一个地理单位配对经纬度坐标；最后，统计每一个地理
单位出现的次数（实际是统计发自该地的推文的数量），作为坐标点的权重（与颜色对应）。

    而对于旨在展现国家层面的信息的统计图，则只需利用geopy库从地点反查国家名即可

（二）地理分布可视化：

      地理分布可视化分为两个部分：
      1)地理坐标图;
      2)统计图.
      
1.地理坐标图：

    地理坐标图将每个用户的地理信息依据经纬度坐标标注在全球地图上（用户可进行缩放和移动），同
时坐标点的颜色代表同一地点所发的推文数，范围为1-25，数值越大颜色越偏红色，相反越小则越偏蓝色。
点击坐标点，地图会显示该地的发推数，而通过图左下角的滑块，用户可自行选择查看的数值范围。

2.统计图：

    统计图（圆圈图）展示了各个国家发推数量的个数和比例（将鼠标置于圆圈的区段上可显示），用户
可通过左侧的按钮自行选择想要查看的国家。（但通过geopy还原的国家名称为该国语言，需要读者自行查
询中文名）。

二、可视化结果解读

（一）统计图：

     统计图显示，发推数量最多的国家为美国，一共发推397条，占比为64.76%。而发推数量第二（加拿大）、
第三（英国）和第四（法国）的国家发推数量仅为36、32和25，占比分别为5.87%、5.22%和4.08%，可见在这
场讨论中参与的最多的是美国用户，但实际上发出地在美国以外的推文占比也超过了1/3，说明这是一场美国
用户主导，国际用户积极参与的讨论，展现了全球各地对儿童编程教育的关心。

（二）地理坐标图：

    统计图主要展示了国家层面的数量信息，而地理坐标图则可更加直观地反映用户的地理位置信息。从地
理坐标的密度可看出，发推的用户主要集中在北美和西欧；而在各个国家内部，也呈现出地域差异，如美国
用户主要集中在东北部（包括新英格兰、中大西洋和五大湖区）；发推数量多的地点多是大城市等。

（三）总结：

    从上述分析可看出，这是一场美国用户主导，各国用户积极参与的讨论，但来自北美、西欧地区的用户占
绝大多数，同时在每个国家内部，用户的地理位置分布也存在着差异。

-----------------------------------------------------------------------------------------
"""





"""
数据清理与描绘地理坐标
"""
import openpyxl
import pandas as pd
import re



##读取数据集
workbook=openpyxl.load_workbook("新建 Microsoft Excel 工作表.xlsx")
worksheet=workbook.worksheets[0]



##提取用户的地理信息
user__location = [cell.value for cell in list(worksheet.columns)[28]]

##对原始地理信息进行处理,只提取能被识别的地理命名实体
geo_user__location = []

import stanza

nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

for i in range(len(user__location)):
    doc = nlp(str(user__location[i]))
    for ent in doc.ents:
        if ent.type == 'GPE':#如果是地理命名实体
           geo_user__location.append(ent.text)

##删除国家级地理单位
Country = [#加载国家名称列表
    ('US', 'United States'),
    ('AF', 'Afghanistan'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AQ', 'Antarctica'),
    ('AG', 'Antigua And Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia'),
    ('BA', 'Bosnia And Herzegowina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('CV', 'Cape Verde'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Rep'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CX', 'Christmas Island'),
    ('CC', 'Cocos Islands'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('CI', 'Cote D`ivoire'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('TP', 'East Timor'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GF', 'French Guiana'),
    ('PF', 'French Polynesia'),
    ('TF', 'French S. Territories'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GR', 'Greece'),
    ('GL', 'Greenland'),
    ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'),
    ('GU', 'Guam'),
    ('GT', 'Guatemala'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HN', 'Honduras'),
    ('HK', 'Hong Kong'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', 'Korea (North)'),
    ('KR', 'Korea (South)'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', 'Laos'),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MO', 'Macau'),
    ('MK', 'Macedonia'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MQ', 'Martinique'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('YT', 'Mayotte'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia'),
    ('MD', 'Moldova'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('MS', 'Montserrat'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('AN', 'Netherlands Antilles'),
    ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('NU', 'Niue'),
    ('NF', 'Norfolk Island'),
    ('MP', 'Northern Mariana Islands'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PN', 'Pitcairn'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('PR', 'Puerto Rico'),
    ('QA', 'Qatar'),
    ('RE', 'Reunion'),
    ('RO', 'Romania'),
    ('RU', 'Russian Federation'),
    ('RW', 'Rwanda'),
    ('KN', 'Saint Kitts And Nevis'),
    ('LC', 'Saint Lucia'),
    ('VC', 'St Vincent/Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SH', 'St. Helena'),
    ('PM', 'St.Pierre'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SZ', 'Swaziland'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syrian Arab Republic'),
    ('TW', 'Taiwan'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania'),
    ('TH', 'Thailand'),
    ('TG', 'Togo'),
    ('TK', 'Tokelau'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad And Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('UK', 'United Kingdom'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VA', 'Vatican City State'),
    ('VE', 'Venezuela'),
    ('VN', 'Vietnam'),
    ('VG', 'Virgin Islands (British)'),
    ('VI', 'Virgin Islands (U.S.)'),
    ('EH', 'Western Sahara'),
    ('YE', 'Yemen'),
    ('YU', 'Yugoslavia'),
    ('ZR', 'Zaire'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe')
]

list_Country = []
name_Country = []

for item in Country:#将元组转换成列表
    list_Country.append(list(item))

for item in list_Country:#提取每个列表的第二个元素：国家英文全名
    name_Country.append(item[1])
    
processed_geo_user__location = [#删除国家级地理单位和缩写，其中部分为之后手动添加的
    
x for x in geo_user__location if x not in name_Country  if x != 'U.S.A'  if x!= 'Deutschland' if x != 'England' 
if x!= 'South Germany' if x!= 'España' if x != 'México' if x != 'Nederland' if len(x) > 3

]



##统计地理单位出现的次数（实际是统计发自该地的推文的数量），作为坐标点的权重
location_number_dict = {}

for w in processed_geo_user__location:
    if w in location_number_dict.keys():
         location_number_dict[w] = location_number_dict[w] + 1
    else:
         location_number_dict[w] = 1

            
            
##为每一个地理单位配对经纬度坐标，并搜集该地理单位的国别信息
user_location_dict = {}

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='demo_of_gnss_help')

location_list = []
latitude_list = []
longitude_list = []
address_list = []

for i in processed_geo_user__location:
    location = geolocator.geocode(i)
    if location is None:
        continue
    else:
        location_list.append(i)
        latitude_list.append(location.latitude)
        longitude_list.append(location.longitude)
        address_list.append(list(location.address.split())[-1])#在geopy.address里，国别信息排在最后
        
for i in range(0,len(location_list)):
    user_location_dict[location_list[i]]=[latitude_list[i],longitude_list[i]]

    
##统计各个国家的发推数量
address_list = ['United States' if i =='States' else i for i in address_list]#整合部分信息
address_list = ['United Kingdom' if i =='Kingdom' else i for i in address_list]

tweet_location_dict = {}#统计发推数
for w in address_list:
    if w in tweet_location_dict.keys():
         tweet_location_dict[w] = tweet_location_dict[w] + 1
    else:
         tweet_location_dict[w] = 1



"""
地理分布可视化
"""

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType, GeoType
from pyecharts.charts import Pie, Grid, Page

##绘制地理坐标图
geo = Geo()

for i in user_location_dict.keys():
 geo.add_coordinate(#在地图上添加坐标点
        name=i,
        longitude=round(user_location_dict[i][1],2),#坐标取小数点后2位
        latitude=round(user_location_dict[i][0],2)
        )

 geo.add("",
        [(i,location_number_dict[i])]#在坐标点上添加地理单位名称与权重
        )

geo.add_schema(maptype="world")#添加数据项（即设置全图的范围）

geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))#设置相关属性
geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(max_=25),#颜色的最大值为25
                    title_opts=opts.TitleOpts(title="推文空间分布图"))


##绘制饼图
x_data = tweet_location_dict.keys()
y_data = tweet_location_dict.values()
data_pair = [list(z) for z in zip(x_data, y_data)]
data_pair.sort(key=lambda x: x[1])

pie = (
    Pie(init_opts=opts.InitOpts(width="960px", height="600px"))
    .add(
        series_name="国家",
        data_pair=[list(z) for z in zip(x_data, y_data)],
        radius=["50%", "70%"],
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .set_global_opts(legend_opts=opts.LegendOpts(pos_left="legft", orient="vertical"))
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
    )
)

##展示图
page=Page()
page.add(geo)
page.add(pie)
page.render_notebook()


# In[ ]:




