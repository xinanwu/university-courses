
from mpython import *
import ntptime

def openning():
    image_picture = Image()
    for j in range(0,18):
        oled.fill(0)
        oled.blit(image_picture.load(str((str(j))) + str('.pbm'), 1), 0, 0)
        oled.show()
        sleep_ms(100)
    oled.DispChar('星图', 50, 16)
    oled.show()
    time.sleep(2)

def timeUpdate():
    oled.fill(0)
    oled.DispChar('正在同步时间...(需要wifi)', 0, 0)
    oled.show()
    mywifi=wifi()
    mywifi.connectWiFi('nova 4e','fuhaozhu')

    print("同步前本地时间：%s" %str(time.localtime()))
    ntptime.settime()
    print("同步后本地时间：%s" %str(time.localtime()))

# 为了方便，我定义这些函数来直接计算角度制的反三角函数。

def sin(x):
    return float("%.8f"%math.sin(x*math.pi/180))

def cos(x):
    return float("%.8f"%math.cos(x*math.pi/180))

def arcsin(x):
    if x > 1:
        x -= 0.01
    if x < -1:
        x += 0.01
    return float("%.8f"%(math.asin(x)/math.pi*180))

def arccos(x):
    return float("%.8f"%(math.acos(x)/math.pi*180))

Lat = 30.67 # 当地纬度

# 函数一：地平坐标转化为时角坐标

def c_Dec(x,y):    # 赤纬declination，x为方位角，y为地平高度
    return float("%.8f"%(90 - arccos(cos(90 - Lat)*cos(90 - y) + sin(90 - Lat)*sin(90 - y)*cos(360 - x))))

def c_HA(x,y,z):    # 时角hour angle，x为方位角，y为地平高度，z为赤纬
    Dec2 = c_Dec(x,y + 0.1)
    s = sin(360-x)*sin(90 - y)/sin(90 - z)
    s1 = sin(360-x)*sin(90 - y - 0.1)/sin(90 - Dec2)
    HA = float("%.8f"%(arcsin(s)))*24/360
    if y == 90:
        HA = 0
    elif y == -90:
        HA = 12   # 在h为正负90时，HA与A无关，直接输出好了
    else:
        if 0 <= x < 180 and s >= s1:
            HA = 12 - HA
        elif 0 <= x < 180 and s < s1:
            HA = 24 + HA
        elif 180 <= x < 360 and s < s1:
            HA = 12 - HA
        elif 180 <= x < 360 and s >= s1:
            HA = HA
    return HA

# 函数三：计算两天间的天数

def count_days(x,y):    # 样例：x = ‘2000 1 3’, y = ‘2019 11 10’
                        # 年份范围在1~3000。保证日期正确且结束日期不早于起始日期。
    sList = x.split()
    eList = y.split()
    sYear = int(sList[0])
    sMonth = int(sList[1])
    sDay = int(sList[2])
    eYear = int(eList[0])
    eMonth = int(eList[1])
    eDay = int(eList[2])
    dict1 = {'1':31,'2':28,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31}
    dict2 = {'1':31,'2':29,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31}
    d = 0
    if sYear == eYear:
        if sMonth == eMonth:
            d = eDay - sDay
        else:
            a = sYear
            if a % 4 != 0 or a % 100 == 0 and a % 400 != 0:
                d = d + dict1[str(sMonth)] - sDay + 1 + eDay - 1    # dict['1']=...
                for i in range(sMonth+1,eMonth):
                    d = d + dict1[str(i)]
            else:
                d = d + dict2[str(sMonth)] - sDay + 1 + eDay - 1
                for i in range(sMonth+1,eMonth):
                    d = d + dict2[str(i)]
    else:
        a = sYear
        k = 0
        b = eYear
        if a % 4 != 0 or a % 100 == 0 and a % 400 != 0:
            d = d + dict1[str(sMonth)] - sDay + 1
            for i in range(sMonth+1,13):
                d = d + dict1[str(i)]
            for i in range(sYear+1,eYear):
                if i % 4 != 0 or i % 100 == 0 and i % 400 != 0:
                    k = k + 1
            d = d + k * 365 + (eYear - sYear - 1 - k) * 366
            d = d + eDay - 1
            if b % 4 != 0 or b % 100 == 0 and b % 400 != 0:
                for i in range(1,eMonth):
                    d = d + dict1[str(i)]
            else:
                for i in range(1,eMonth):
                    d = d + dict2[str(i)]
        else:
            d = d + dict2[str(sMonth)] - sDay + 1
            for i in range(sMonth+1,13):
                d = d + dict2[str(i)]
            for i in range(sYear+1,eYear):
                if i % 4 != 0 or i % 100 == 0 and i % 400 != 0:
                    k = k + 1
            d = d + k * 365 + (eYear - sYear - 1 - k) * 366
            d = d + eDay - 1
            if b % 4 != 0 or b % 100 == 0 and b % 400 != 0:
                for i in range(1,eMonth):
                    d = d + dict1[str(i)]
            else:
                for i in range(1,eMonth):
                    d = d + dict2[str(i)]
    return d

# 函数四：时角坐标转化为地平坐标

def c_h(x,y):   # x为赤纬，y为时角
    a = y * 15
    return float("%.8f"%(90 - arccos(cos(90 - Lat)*cos(90 - x) + sin(90 - Lat)*sin(90 - x)*cos(a))))

def c_A(x,y,z):   # x为赤纬，y为时角，z为地平高度
    a = y * 15
    h1 = c_h(x + 0.1,y)
    s = sin(a)*sin(90 - x)/sin(90 - z)
    s1 = sin(a)*sin(90 - x - 0.1)/sin(90 - h1)
    A = float("%.8f"%(arcsin(s)))
    if 0 <= y < 12 and s <= s1:
        return 180 + A
    elif 0 <= y < 12 and s > s1:
        return 360 - A
    elif 12 <= y < 24 and s <= s1:
        if A < 0:
            A = -A
        return A
    elif 12 <= y < 24 and s > s1:
        return 180 + A

# 函数五：计算球面上两点的角距

def distance(A1,h1,A2,h2):
    b = 90 - h1
    c = 90 - h2
    A = A1 - A2
    cosa = cos(b)*cos(c)+sin(b)*sin(c)*cos(A)
    if cosa > 1:
        cosa -= 0.001
    a = arccos(cosa)
    return a

# 这个字典包含视亮度数据 
dict_magnitude = {'天狼星': -1.44, '老人星': -0.62, '大角': -0.05, '南门二': -0.01, '织女星': 0.03, \
'五车二': 0.08, '参宿七': 0.18, '南河三': 0.4, '参宿四': 0.45, '水委一': 0.45, '牛郎星': 0.76, \
'毕宿五': 0.87, '角宿一': 0.98, '心宿二': 1.06, '北河三': 1.16, '北落师门': 1.17, '天津四': 1.25, \
'轩辕十四': 1.36, '弧矢七': 1.5, '北河二': 1.58, '十字架一': 1.59, '尾宿八': 1.62, '参宿五': 1.64, \
'五车五': 1.65, '参宿二': 1.69, '鹤一': 1.73, '参宿一': 1.74, '天社一': 1.75, '北斗五': 1.76, \
'天船三': 1.79, '箕宿三': 1.79, '北斗一': 1.81, '弧矢一': 1.83, '北斗七': 1.85, '尾宿五': 1.86, \
'五车三': 1.9, '井宿三': 1.93, '北极星': 1.97, '军市一': 1.98, '星宿一': 1.99, '娄宿三': 2.01, \
'轩辕十二': 2.01, '土司空': 2.04, '斗宿四': 2.05, '库楼三': 2.06, '参宿六': 2.07, '壁宿二': 2.07, \
'奎宿九': 2.07, '北极二': 2.07, '�天鹅座': 2.07, '候': 2.08, '大陵五': 2.09, '天大将军一': 2.1, \
'五帝座一': 2.14, '�半人马座': 2.2, '弧矢增二十二': 2.21, '贯索四': 2.22, '天津一': 2.23, \
'天记': 2.23, '开阳': 2.23, '天棓四': 2.24, '王良四': 2.24, '参宿三': 2.25, '王良一': 2.28, \
'房宿三': 2.29, '北斗二': 2.34, '北斗三': 2.41, '北斗四': 3.32}


# 这个列表包含5月1日的时角坐标 [名称, 时角, 赤纬]
list_HA = [['天狼星', '6.734711', '-16.716111'], ['老人星', '7.137965', '-52.695658'], \
['大角', '23.263931', '19.182408'], ['南门二', '22.858247', '-60.833978'], \
['织女星', '17.081736', '38.783692'], ['五车二', '8.240245', '45.997989'], \
['参宿七', '8.282366', '-8.201642'], ['南河三', '5.876943', '5.224994'], \
['参宿四', '7.603440', '7.407064'], ['水委一', '11.899920', '-57.236756'], \
['牛郎星', '17.672097', '8.868322'], ['毕宿五', '8.923970', '16.509300'], \
['角宿一', '0.103442', '-11.161322'], ['心宿二', '21.031726', '-26.432000'], \
['北河三', '5.796177', '28.026194'], ['北落师门', '14.565200', '-29.622236'], \
['天津四', '16.823515', '45.280339'], ['轩辕十四', '3.385363', '11.967222'], \
['弧矢七', '6.558106', '-28.972222'], ['北河二', '5.948561', '31.888275'], \
['十字架一', '0.999753', '-57.113214'], ['尾宿八', '19.959226', '-37.103819'], \
['参宿五', '8.104431', '6.349722'], ['五车五', '8.082613', '28.607450'], \
['参宿二', '7.920478', '-1.201944'], ['鹤一', '15.391686', '-46.960975'], \
['参宿一', '7.844811', '-1.942572'], ['天社一', '6.653992', '-47.336589'], \
['北斗五', '0.627843', '55.959819'], ['天船三', '10.114559', '49.861181'], \
['箕宿三', '19.114051', '-34.384617'], ['北斗一', '2.468643', '61.751033'], \
['弧矢一', '6.398373', '-26.393200'], ['北斗七', '23.735008', '49.313267'], \
['尾宿五', '19.896166', '-42.997825'], ['五车三', '4.475790', '44.947433'], \
['井宿三', '6.891642', '16.399253'], ['北极星', '10.753753', '89.264106'], \
['军市一', '7.148816', '-17.955917'], ['星宿一', '4.063192', '-8.658361'], \
['娄宿三', '11.403061', '23.462422'], ['轩辕十二', '3.192622', '19.841489'], \
['土司空', '12.798400', '-17.986606'], ['斗宿四', '12.217696', '-26.296722'], \
['库楼三', '23.410342', '-36.369953'], ['参宿六', '7.729123', '-9.669611'], \
['壁宿二', '13.382366', '29.090431'], ['奎宿九', '12.359591', '35.620558'], \
['北极二', '22.689856', '74.155500'], ['�天鹅座', '14.817039', '-46.884578'], \
['候', '19.943023', '12.560036'], ['大陵五', '10.384962', '40.955647'], \
['天大将军一', '11.456215', '42.329722'], ['五帝座一', '1.707103', '14.572058'], \
['�半人马座', '0.828490', '-48.959889'], ['弧矢增二十二', '6.553239', '-40.003147'], \
['贯索四', '21.947511', '26.714694'], ['天津一', '17.142153', '40.256667'], \
['天记', '4.383835', '-43.432592'], ['开阳', '0.129352', '54.925361'], \
['天棓四', '19.589665', '51.488894'], ['王良四', '12.844220', '56.537333'], \
['参宿三', '7.990501', '-0.299092'], ['王良一', '13.365676', '59.149781'], \
['房宿三', '21.516814', '-22.621711'], ['北斗二', '2.498808', '56.382428'], \
['北斗三', '1.631139', '53.694758'], ['北斗四', '1.271620', '57.032617']]



def starMapping(): # 将所有星星转换为目前时间的位置
    oled.fill(0)
    oled.DispChar('正在计算...', 0, 0)
    oled.show()

    date_now = str(time.localtime()[0])+' '+str(time.localtime()[1])+' '+str(time.localtime()[2])
    time_now = [time.localtime()[3],time.localtime()[4]]

    d = count_days('2020 5 1',date_now)

    # 计算与2020.5.1的时间差，以分钟为单位。
    mins = d*24*60 + time_now[0]*60 + time_now[1]

    # 23时56分4.09秒是恒星时中的一天，经过恒星时的一天，恒星在天球上的位置不会改变。
    dt = (mins%(23*60 + 56 + 4.09/60))/60

    # 将5.1的时角坐标转化为现在的地平坐标
    global list_now
    list_now = []
    for i in list_HA:
        HA = float(i[1]) + dt      # 现在的时角
        if HA > 24:
            HA = HA - 24
        h = c_h(float(i[2]),HA)    # 高度
        A = c_A(float(i[2]),HA,h)  # 方位角
        list_now += [[i[0],A,h]]


def starShowing(target_h,target_A): # 显示星星
    global target_list
    target_list = []
    for i in list_now:
        A = i[1]
        h = i[2]
        # 搜索范围：距离单片机背面指向坐标的角距小于60度
        if distance(A,h,target_A,target_h) <= 60:
            # 求以指向坐标为原点的直角坐标系的x、y
            x = distance(A,target_h,target_A,target_h)
            y = distance(target_A,h,target_A,target_h)
            # 显示范围：-24<x<24,-12<y<12
            if x<24 and y<12:
                if (A < target_A and target_A - A < 24) or (A - target_A > 24):
                    x = - x
                d1 = distance(target_A,h,target_A,0)
                d2 = distance(target_A,target_h,target_A,0)
                if (d1 < d2 and h > 0 and target_h > 0) or (d1 > d2 and h < 0 and target_h < 0) \
                   or (h < 0 and target_h >= 0):
                    y = - y
                # 再变换到以左上角为坐标原点，便于显示.比例：24（角距）：64（像素）
                x = (x + 24)/24*64
                y = - (y - 12)/24*64
                target_list += [[i[0],x,y,dict_magnitude[i[0]]]]  # [[name, x, y, 视亮度]]
    oled.fill(0)
    for i in target_list:
        x = i[1]
        y = i[2]
        m = i[3] # 视亮度
        if m > 0.5:
            oled.pixel(round(x),round(y),1)
        else:
            oled.fill_circle(round(x),round(y),1,1)
    oled.show()


openning()
timeUpdate()
starMapping()
oled.fill(0)

def ledon2(_):  # 中断函数：显示星星名称
    global hp
    hp -= 2
    string = '按亮度排序：'
    if len(target_list) != 0:
        oled.fill(0)
        for i in range(len(target_list)):
            name = target_list[i][0]
            x = target_list[i][1]
            y = target_list[i][2]
            oled.DispChar(str(i+1), round(x)+1, round(y)-1)
            string += str(i+1)+'.'+name+' '
        oled.show()
        sleep(1)
        oled.fill(0)
        oled.DispChar(string, 0, 0)
        oled.show()
        sleep(1)
        oled.fill(0)
    
def ledon(_):             # 中断处理函数：控制指向
    global hm,Am
    if touchPad_P.read() < 100 and hm <= 85:
        hm += 5
    elif touchPad_Y.read() < 100 and hm >= -85:
        hm -= 5
    elif touchPad_T.read() < 100 and Am < 350:
        Am += 10
    elif touchPad_T.read() < 100 and Am <= 360:
        Am = 0
    elif touchPad_H.read() < 100 and Am >= 10:
        Am -= 10
    elif touchPad_H.read() < 100 and Am >= 0:
        Am = 350
    elif touchPad_O.read() < 100:
        A1 = magnetic.get_heading()
        A2 = magnetic.get_heading()
        A3 = magnetic.get_heading()
        Am = (A1 + A2 + A3)/3      # 取平均值减小误差
    elif touchPad_N.read() < 100:
        gx = accelerometer.get_x()
        gz = accelerometer.get_z()
        if gz == 0 and gx < 0:
            hm = -90
        elif gz == 0 and gx > 0:
            hm = 90
        else:
            hm = math.atan(-gx/gz)
        
def main1():
    global Am, hm, Ap, hp
    while True:
        if round(Ap) != round(Am) or round(hp) != round(hm):
            starShowing(hm,Am)
            oled.DispChar(str(round(Am))+','+str(round(hm)), 0, 0)
            oled.show()
            Ap, hp = Am, hm


button_a.irq(trigger=Pin.IRQ_FALLING, handler=ledon2)     # 设置按键 A 中断
button_b.irq(trigger=Pin.IRQ_FALLING, handler=ledon)     # 设置按键 B 中断
hp, Ap = 1, 0
hm, Am = 0, 0
main1()     
