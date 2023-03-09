from mpython import *     
x0=63           
y0=31            
while True: 
    x=accelerometer.get_x()         
    y=accelerometer.get_y()          
    if y<=1 and y>=-1:
        deltaX=int(numberMap(y,1,-1,-64,64))   
    if x<=1 and x>=-1:
        deltaY=int(numberMap(x,1,-1,32,-32))   
    if deltaX==0 and deltaY==0:
        rgb.fill((0,10,0))          
        rgb.write()
    else:
        rgb.fill((10,0,0))           
        rgb.write()
    oled.show()
    oled.fill(0)