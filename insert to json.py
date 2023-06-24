l=[1925,1960,1949,1951,1813,1945,1937,1967,1866,1890]
mf = sum(l)/10
l2=[]
for i in l :
    l2.append(abs(i-mf))

sf = sum(l2)/10

res = []
for i in l:
    res.append((i-mf)/sf)
# print(res)
# ////////////////////
import math


l=[180,80,328,277,279,112,310,417,545,254]
l2=[]
for i in l :
    l2.append((math.log(i)))
maxi = max(l2)
mini = min(l2)

res=[]
for i in l2:
    res.append((i-mini)/(maxi-mini))

# print( res)
# print(l2)
# print(mini)
# print(maxi)
# ////////////////////

l=[5,4,2,3,5,3,5,4,3,1]
l2=[]
for i in l :
    l2.append((i-1)/(max(l)-1))
# print(l2)