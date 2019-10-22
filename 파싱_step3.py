import os, csv, pymysql.cursors, itertools

conn = pymysql.connect(host='localhost', user='root', password='1234',
                       db='h504', charset='utf8')



path1 = "C:/Users/user/Desktop/차세정/말뭉치/next_gen_KCC150"
path2 = "C:/Users/user/Desktop/차세정/말뭉치/next_gen_output_KCC150"
path3 = "C:/Users/user/Desktop/차세정/말뭉치/next_gen_input_KCC150_ANSI_5"

cp1=1
cp2=1
cp3=1

file_list1 = os.listdir(path1)
file_list2 = os.listdir(path2)
file_list3 = os.listdir(path3)
field1 = ''   
field2 = ''
field3 = ''
sg1=[]    #문장씩 담는 리스트
sg2=[]    #문장씩 담는 리스트
sg3=[]    #문장씩 담는 리스트
c=1
# print(file_list1[0])
for i in range(0, len(file_list1)):
    print('check point')
    fn=file_list1[i]
    full_name1 = os.path.join(path1, file_list1[i])
    full_name2 = os.path.join(path2, file_list2[i])
    full_name3 = os.path.join(path3, file_list3[i])
    print(full_name1)
    if(c==1):
        c=0
        continue
    with open(full_name1, 'r')as f1, open(full_name2, 'r')as f2, open(full_name3, 'r',encoding='utf8')as f3:
        #파일 2 3 도 똑같이 복사 작업 해야함 ---------------------------
        cp1=1# path1파일에 대한 check point
        cp2=1# path1파일에 대한 check point
        cp3=1# path1파일에 대한 check point
        
        lines1=f1.readlines()
        lines2=f2.readlines()
        lines3=f3.readlines()
        while(1):
            for i in range(cp1,len(lines1)):
                if(lines1[i] == '\n'): #다음 문장을 넘어가기위한 수단
                    cp1=i+1
                    break
                sg1.append(lines1[i])
                
            for i in range(cp2,len(lines2)):
                if(lines2[i] == '\n'): #다음 문장을 넘어가기위한 수단
                    cp2=i+1
                    break
                sg2.append(lines2[i])
                
            for i in range(cp3,len(lines3)):
                if(lines3[i] == '\n'): #다음 문장을 넘어가기위한 수단
                    cp3=i+1
                    break
                sg3.append(lines3[i])
            if(len(sg1)==len(sg2) and len(sg2)==len(sg3)):
                for (line1,line2,line3) in zip(sg1,sg2,sg3) :
                    #print(1)
                    if line1[0] == '#':            #라인의 제일 첫글자(line[0])이 '#'일 경우에 수행
                        a = line1.split(" ")     #line을 공백(" ")단위로 끊어 a에 배정
                        if a[1] == "sent_id":     #a의 두번째(a[1]) data의 값을 검색
                            b = a[3].rstrip()     #a의 네번째(a[3]) data를 b에 저장
                            #print(b)
                            conn.commit()
                            #print(b)
                    else:
                        #print(line2)
                        if line1[0] == '\n' :    #text파일 중간 중간에 "\n"키가 포함되어 있어 불필요한 정보 스킵
                            #print("$")
                            continue
                        field1 = line1.strip().split('\t')    #line을 tab('\t')단위로 끊어 field에 배정
                        field2 = line2.strip().split('\t')    #line을 tab('\t')단위로 끊어 field에 배정
                        field3 = line3.strip().split('\t')    #line을 tab('\t')단위로 끊어 field에 배정
                        #print(line2)
                        
                        plusadd= field2[4].strip().split(' ')
                        #print(len(plusadd))
                        field2[4]=''
                        for j in range(0,len(plusadd)):
                            if j != 0:
                                plusadd[j]='+'+plusadd[j]
                            #print(plusadd[j])
                            field2[4]+=plusadd[j]
                        #print(field2[4]+field2[0]+str(len(plusadd)))
                        with conn.cursor() as cursor:
                            try:
                                cursor.execute("insert into v3(file_name, sent_id, id, e_form, e_lemma, e_upos, e_xpos,  e_feats, e_head, e_deprel, e_eps, e_misc, u_form, u_lemma, u_upos, u_xpos,  u_feats, u_head, u_deprel, u_eps, u_misc, k_form, k_lemma, k_upos, k_xpos,  k_feats, k_head, k_deprel, k_eps, k_misc) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (fn,b,field1[0],field1[1],field1[2],field1[3],field1[4],field1[5],field1[6],field1[7],field1[8],field1[9],field2[1],field2[2],field2[3],field2[4],field2[5],field2[6],field2[7],field2[8],field2[9],field3[1],field3[2],field3[3],field3[4],field3[5],field3[6],field3[7],field3[8],field3[9]))
                                #주의할 점! 마지막 misc에 삽일할 data의 길이가 너무 길어서 misc의 자료형을 변경해주었음. 에러의 요인
                            except:
                                print(field1)
                                print(field2)
                                print(field3)
                                print(fn)
                        #print("check")
                        field1.clear()
                        field2.clear()
                        field3.clear()
            else:
                finsert = open("C:/Users/user/Desktop/차세정/말뭉치/insert실패.txt",'r+',encoding='utf8')
                cpfile = finsert.readlines()
                finsert.close()
                finsert = open("C:/Users/user/Desktop/차세정/말뭉치/insert실패.txt",'w',encoding='utf8')
                finsert.writelines(cpfile)
                finsert.writelines('\n' + b + '\t' +  fn )
                print(b + '\t' +  fn )
                finsert.close()
                
            sg1.clear() #리스트 초기화
            sg2.clear() #리스트 초기화
            sg3.clear() #리스트 초기화
            if cp2>=len(lines1)-1:
                break
conn.close()
#무한 루프 안에 함수로 만들어서 돌릴것!!!!



