import math
import turtle as t

posx= lambda t:8*(t/10)
posy= lambda t:(t/10)**2
x=0
y=0
difteta=0
vecdif=0
for i in range(1,1000):
    if y!=0:
        difteta=(math.atan(posy(i)/posx(i))-math.atan(y/x))*180/math.pi
    else:
        difteta=math.atan(posy(i)/posx(i))*180/math.pi
    vecdif=((posx(i)-x)**2+(posy(i)-y)**2)**(1/2)
    x=posx(i)
    y=posy(i)
    t.right(difteta)
    t.fd(vecdif)