from mpython import *
# 方位校准
Bxmax = 0
Bxmin = 0
Bymax = 0
Bymin = 0
i = {}
j = 0
oled.fill(0)
# 水平匀速旋转，收集XY轴的数据
oled.DispChar('校准：请水平放置顺时针匀速缓慢两圈', 0, 0)

while True:
    oled.DispChar('已完成：', 0, 32)
    oled.show()
    Bx = magnetic.get_x()
    By = magnetic.get_y()
    A = magnetic.get_heading()
    if Bx > Bxmax:
        Bxmax = Bx
    if Bx < Bxmin:
        Bxmin = Bx
    if By > Bymax:
        Bymax = By
    if By < Bymin:
        Bymin = By
    if A < 10:
        i[1] = 0
        oled.DispChar('北', 0, 48)
        oled.show()
    if 80 < A and A < 100:
        i[2] = 0
        oled.DispChar('东', 15, 48)
        oled.show()
    if 170 < A and A < 190:
        i[3] = 0
        oled.DispChar('南', 30, 48)
        oled.show()
    if 260 < A and A < 280:
        i[4] = 0
        oled.DispChar('西', 45, 48)
        oled.show()
    if len(i) == 4 and j == 0:
        oled.fill(0)
        oled.DispChar('再转一圈', 0, 0)
        oled.show()
        i = {}
        j += 1
    if len(i) == 4 and j == 1:
        oled.fill(0)
        break
gz0 = -9.7
while True:
    X = magnetic.get_x()
    Y = magnetic.get_y()
    Z = magnetic.get_y()
    gx = accelerometer.get_x()
    gy = accelerometer.get_y()
    gz = accelerometer.get_z()
    if gz==0 and gx==gz0:
        return h=-(math.pi)/2
    elif gz==0 and gx==-gz0:
        return h=(math.pi)/2
    else:
        return h = math.atan(-gx/gz)   # 俯仰角
    if gy==0 and gx!=0:
        if gx*math.sin(h)+gz*math.cos(h)==gz0:
            return c=(math.pi)/2
        else:
            return c=-(math.pi)/2
    elif gy==0 and gx==0:
        h=0
        return c=0
    else:
        return c = math.atan(-gx/gy)  # 侧倾角
    Xh = X*math.cos(c) - Y*math.sin(c) 
    Yh = Y*math.cos(c)*math.cos(h) + Z*math.sin(h) - \
         X*math.cos(h)*math.sin(c) 
    A = math.atan(Yh/Xh)*180/math.pi
    if Xh < 0:
        A = 180 - A
    elif Xh > 0 and Yh < 0:
        A = -A
    elif Xh > 0 and Yh > 0:
        A = 360 - A
    elif Xh == 0 and Yh < 0:
        A = 90
    elif Xh == 0 and Yh > 0:
        A = 270
    oled.fill(0)
    oled.DispChar(str(A), 0, 0)
    oled.DispChar(str(h*180/math.pi), 0, 16)
    oled.show()
