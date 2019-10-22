import csv,pymysql.cursors

conn=pymysql.connect(host='localhost', user='root', password='1234',
                     db='jw', charset='utf8')

f = open('C:/Users/JW/Desktop/차세정자료/sample1000 .txt',
         mode='r',encoding='utf-8')



for line in f.readlines():      #f를 줄단위로 나누어 line에 배정
    if line[0]=='#':            #라인의 제일 첫글자(line[0])이 '#'일 경우에 수행
        a = line.split(" ")     #line을 공백(" ")단위로 끊어 a에 배정
        if a[1]=="sent_id":     #a의 두번째(a[1]) data의 값을 검색
            b=a[3].rstrip()     #a의 네번째(a[3]) data를 b에 저장
            #print(b)
    else :
        if line[0] == '\n' :    #text파일 중간 중간에 "\n"키가 포함되어 있어 불필요한 정보 스킵
            continue
        field = line.strip().split('\t')    #line을 tab('\t')단위로 끊어 field에 배정
        #print(field[9])
        with conn.cursor() as cursor:
            cursor.execute("insert into etri values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (b,field[0],field[1],field[2],field[3],field[4],field[5],field[6],field[7],field[8],field[9]))
            #주의할 점! 마지막 misc에 삽일할 data의 길이가 너무 길어서 misc의 자료형을 변경해주었음. 에러의 요인
        #print("check")
conn.commit()
f.close()
conn.close()







