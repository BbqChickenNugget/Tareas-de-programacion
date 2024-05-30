import random

a=[0]*50
aa=[0]*5
for i in range(0,50):
    a[i]=random.random()
    if a[i]<=0.2:
        aa[0]+=1
    elif a[i]<=0.4:
        aa[1]+=1
    elif a[i]<=0.6:
        aa[2]+=1
    elif a[i]<=0.8:
        aa[3]+=1
    elif a[i]<=1:
        aa[4]+=1
print(a)
print(aa)

b=[0]*1000
bb=[0]*5
for i in range(0,1000):
    b[i]=random.random()
    if b[i]<=0.2:
        bb[0]+=1
    elif b[i]<=0.4:
        bb[1]+=1
    elif b[i]<=0.6:
        bb[2]+=1
    elif b[i]<=0.8:
        bb[3]+=1
    elif b[i]<=1:
        bb[4]+=1
print(bb)
