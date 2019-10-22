import matplotlib.pyplot as plt
import csv
x=[0]
z=[0]

f = open('C:/Users/JW/Desktop/차세정자료/python/count2000.txt',
         mode='r',encoding='utf-8')

#append values to list

c=0
ss=0

for line in f.readlines():  #f를 줄단위로 나누어 line에 배정
    c=c+1
    ss=ss+1000
    a = line.split("\t")
    #print(a[3])
    x.append(c)
    z.append(a[3])
    '''
    if c == 1000:
        break
'''
plt.axis([0, 22224, 0,1600000 ])
plt.scatter(x, z,s=1)
plt.show()

