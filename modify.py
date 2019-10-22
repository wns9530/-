import csv,pymysql.cursors


def ec_update():
    conn=pymysql.connect(host='localhost', user='root', password='1234',
                         db='jw', charset='utf8')

    f = open('C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/file_id.csv',
             mode='r',encoding='utf-8')

    c=0
    for line in f.readlines():      #f를 줄단위로 나누어 line에 배정

        #c=c+1
        #if c < 730000:
            #continue

        a = line.split("\t")     #line을 공백(" ")단위로 끊어 a에 배정
        #print(a[0]+" "+a[1])
        with conn.cursor() as cursor:
            sql="select xpos, u_xpos, form, file_name, sent_id, id from jw.etri_v2 where file_name = %s and sent_id = %s"
            cursor.execute(sql,(a[0].strip(),a[1].strip()) ) 
            result= cursor.fetchall()
            #끝에서 2번째 어절의 형태소 분석 결과가 e_pos가 '+EC' u_pos가 '+EF'인 경우 '+EF'로 통일
            try:        
                if(str(result[len(result)-2][0]).endswith('+EC') and str(result[len(result)-2][1]).endswith('+EF')):
                    cursor.execute('update jw.etri_v2 set m_xpos = %s where file_name = %s and sent_id = %s and id =%s',(str(result[len(result)-2][0])[:-3]+'+EF',a[0].strip(),a[1].strip(),(len(result)-1)))
            except:
                print(a[0],a[1],len(result))
            if len(a)==5:
                if a[4]==1:
                    try:        
                        cursor.execute('update jw.etri_v2 set m_u_xpos = %s where file_name = %s and sent_id = %s and id =%s',(str(result[len(result)-2][0])[:-3]+'+EF',a[0].strip(),a[1].strip(),(len(result)-1)))
                    except:
                        print(a[0],a[1],len(result))
            
                    
            del result
        conn.commit()
        del a
        if(c%1000==0):
                   print(c)
    f.close()
    conn.close()
#---------------------------------------------------------------------------------------------------------------------------
def tag_update():
    conn=pymysql.connect(host='localhost', user='root', password='1234',
                         db='jw', charset='utf8')

    f = open('C:/Users/JW/Desktop/차세정자료/python/count2000.txt',
             mode='r',encoding='utf-8')

    c=0
    for line in f.readlines():      #f를 줄단위로 나누어 line에 배정
        c=c+1        
        a = line.split("\t")
        print(len(a),a[0],a[1],a[2],a[3],a[4])
        print("a[4]= ","[",a[4],"]")
        if len(a)==5 and str(a[4].strip())=="1":
            print(a[0],a[1])
            with conn.cursor() as cursor:
                try:        
                    cursor.execute('update jw.etri_v2 set m_u_xpos = %s where xpos = %s and u_xpos = %s',(a[0].strip(),a[0].strip(),a[1].strip()) )
                except:
                    print(a[0],a[1],len(result))
        elif len(a)==5 and str(a[4].strip())=="2":
            print(a[0],a[1])
            with conn.cursor() as cursor:
                try:        
                    cursor.execute('update jw.etri_v2 set m_xpos = %s where xpos = %s and u_xpos = %s',(a[1].strip(),a[0].strip(),a[1].strip()) )
                except:
                    print(a[0],a[1],len(result))

            

        #if c == 5 :
            #break
        conn.commit()
        del a
        if(c%1000==0):
                   print(c)
    f.close()
    conn.close()




tag_update()



