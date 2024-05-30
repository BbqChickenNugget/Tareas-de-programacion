a=[]
b=0
with open("C:\\Users\\Willy\\OneDrive\\Escritorio\\Z°\\Z --- FILES\\z - Python Files\\Class\\numeros.txt") as txt:
    for i in txt:
        a.append(i.split("    "))
        b+=1
c=0
d=0
for i in a:
    for j in i:
        a[c][d]=j.replace(" ","")
        d+=1
    d=0
    c+=1

print(a)
