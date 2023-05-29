import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_csv('D:\\good_yes_order\\9_12\\갑자기 외국인.csv')
df2 = pd.read_csv('D:\\good_yes_order\\9_12\\김남국 넷마블.csv')
df3 = pd.read_csv('D:\\good_yes_order\\9_12\\성폭행 가해자.csv')
df4 = pd.read_csv('D:\\good_yes_order\\9_12\\이 강성팬덤.csv')
df1 = pd.read_csv('D:\\good_yes_order\\12_18\\국회 오염수.csv')
df2 = pd.read_csv('D:\\good_yes_order\\12_18\\말다툼하다.csv')
df3 = pd.read_csv('D:\\good_yes_order\\12_18\\문 임기 중.csv')
df4 = pd.read_csv('D:\\good_yes_order\\12_18\\비명계 욕설.csv')
df5 = pd.read_csv('D:\\good_yes_order\\12_18\\앱으로만난.csv')
df6 = pd.read_csv('D:\\good_yes_order\\12_18\\야 노란봉투법.csv')
df1 = pd.read_csv('D:\\good_yes_order\\18_21\\700피트.csv')
df2 = pd.read_csv('D:\\good_yes_order\\18_21\\숨진 김군.csv')
df3 = pd.read_csv('D:\\good_yes_order\\18_21\\승무원 겁에.csv')
df4 = pd.read_csv('D:\\good_yes_order\\18_21\\여자친구 병원.csv')
df5 = pd.read_csv('D:\\good_yes_order\\18_21\\이선희.csv')
df6 = pd.read_csv('D:\\good_yes_order\\18_21\\조국 달 때문에.csv')
df7 = pd.read_csv('D:\\good_yes_order\\18_21\\중국 한국과 반도체.csv')
df8 = pd.read_csv('D:\\good_yes_order\\18_21\\하태경 김남국 폭로자.csv')
df9 = pd.read_csv('D:\\good_yes_order\\18_21\\학교 주차장.csv')



# =============================================================================
# 좋아요 순으로 확인 불가능한 뉴스
def analysis(df):
    good_list = []
    temp = []
    for i in range(100):
        temp.append(df.loc[i, 'good']) # 수정
        if len(temp) == 10:
            good_list.append(temp)
            temp = []
            
    good_rate_list = []
    temp = []
    for i in range(100):
        temp.append(df.loc[i, 'good_rate']) # 수정
        if len(temp) == 10:
            good_rate_list.append(temp)
            temp = []        
            
    total_list = []
    for i in range(1, 100, 10):
        total_list.append(df.loc[i, 'total']) # 수정  
        
        
    
    timestamp_list = []
    for i in range(0, 100, 10):
        if df.loc[i, 'timestamp'] not in timestamp_list: # 수정
            timestamp_list.append(df.loc[i, 'timestamp'] + '\nTimeDiff: ' + str(df.loc[i, 'diffinminutes'])) # 수정
    
    sex_list = []
    temp = []
    for i in range(0, 100, 10):
        temp.append(df.loc[i, 'male'])
        temp.append(df.loc[i, 'female'])
        if temp[0] == -1:
            temp = [0, 0]
        sex_list.append(temp)
        temp = []
        
    age_list = []
    temp = []
    for i in range(0, 100, 10):
        temp.append(df.loc[i, 'age_10'])
        temp.append(df.loc[i, 'age_20'])
        temp.append(df.loc[i, 'age_30'])
        temp.append(df.loc[i, 'age_40'])
        temp.append(df.loc[i, 'age_50'])
        temp.append(df.loc[i, 'age_60'])
        if temp[0] == -1:
            temp = [0, 0, 0, 0, 0, 0]
        age_list.append(temp)
        temp = []    
        
    comment_top = {}
    comment_top[df.loc[0, 'comment']] = [10]
    for i in range(1, 100):
        temp = comment_top.get(df.loc[i, 'comment'], [])
        if len(temp) == i // 10:
            temp.append(10 - i % 10)
            comment_top[df.loc[i, 'comment']] = temp
        else:
            while (len(temp) < i // 10):
                temp.append(0)
    
            temp.append(10 - i % 10)
            comment_top[df.loc[i, 'comment']] = temp
    total_comments_final = []        
    total_comments = list(comment_top.values())        
    for i in total_comments:
        if len(i) != 10:
            while(len(i) < 10):
                i.append(0)
        total_comments_final.append(i)
        
    return good_list, good_rate_list, total_list, timestamp_list, sex_list, \
        age_list, total_comments_final, df.loc[0, 'written_time']
  
good_list, good_rate_list, total_list, timestamp_list, sex_list, age_list,\
    total_comments_final, written_time = analysis(df)
# =============================================================================
# 좋아요 수
plt.figure(1)
x_axis = [i+0.45 for i in range(10)]
w = 0.05
x_0 = [i*0.1 for i in range(10)]
x_1 = [i*0.1+1 for i in range(10)]
x_2 = [i*0.1+2 for i in range(10)]
x_3 = [i*0.1+3 for i in range(10)]
x_4 = [i*0.1+4 for i in range(10)]
x_5 = [i*0.1+5 for i in range(10)]
x_6 = [i*0.1+6 for i in range(10)]
x_7 = [i*0.1+7 for i in range(10)]
x_8 = [i*0.1+8 for i in range(10)]
x_9 = [i*0.1+9 for i in range(10)]

ax1 = plt.subplot(2, 1, 1)  
plt.xticks(x_axis,timestamp_list,fontsize=7,rotation=0)
plt.bar(x_0, good_list[0], width = w, color='lightcoral')
plt.bar(x_1, good_list[1], width = w, color='red')
plt.bar(x_2, good_list[2], width = w, color='orange')
plt.bar(x_3, good_list[3], width = w, color='yellow')
plt.bar(x_4, good_list[4], width = w, color='lightgreen')
plt.bar(x_5, good_list[5], width = w, color='green')
plt.bar(x_6, good_list[6], width = w, color='skyblue')
plt.bar(x_7, good_list[7], width = w, color='blue')
plt.bar(x_8, good_list[8], width = w, color='midnightblue')
plt.bar(x_9, good_list[9], width = w, color='purple')
plt.ylabel('Numbers of Good')
plt.grid('on')
plt.title('Written time: ' + written_time)
plt.xlim([-0.1, 10.1])

ax2 = plt.subplot(2, 1, 2)
plt.xticks(x_axis,timestamp_list,fontsize=7,rotation=0)
plt.plot(x_axis, total_list, 'k')
plt.grid('on')
plt.xlabel('Data Collected Time')
plt.ylabel('Numbers of Total Comments')
plt.xlim([-0.1, 10.1])
plt.show
# =============================================================================
# 좋아요 비율
plt.figure(2)
x_axis = [i+0.45 for i in range(10)]
w = 0.05
x_0 = [i*0.1 for i in range(10)]
x_1 = [i*0.1+1 for i in range(10)]
x_2 = [i*0.1+2 for i in range(10)]
x_3 = [i*0.1+3 for i in range(10)]
x_4 = [i*0.1+4 for i in range(10)]
x_5 = [i*0.1+5 for i in range(10)]
x_6 = [i*0.1+6 for i in range(10)]
x_7 = [i*0.1+7 for i in range(10)]
x_8 = [i*0.1+8 for i in range(10)]
x_9 = [i*0.1+9 for i in range(10)]

ax1 = plt.subplot(2, 1, 1)  
plt.xticks(x_axis,timestamp_list,fontsize=7,rotation=0)
plt.bar(x_0, good_rate_list[0], width = w, color='lightcoral')
plt.bar(x_1, good_rate_list[1], width = w, color='red')
plt.bar(x_2, good_rate_list[2], width = w, color='orange')
plt.bar(x_3, good_rate_list[3], width = w, color='yellow')
plt.bar(x_4, good_rate_list[4], width = w, color='lightgreen')
plt.bar(x_5, good_rate_list[5], width = w, color='green')
plt.bar(x_6, good_rate_list[6], width = w, color='skyblue')
plt.bar(x_7, good_rate_list[7], width = w, color='blue')
plt.bar(x_8, good_rate_list[8], width = w, color='midnightblue')
plt.bar(x_9, good_rate_list[9], width = w, color='purple')
plt.ylabel('Rate of Good')
plt.grid('on')
plt.title('Written time: ' + written_time)
plt.xlim([-0.1, 10.1])

ax2 = plt.subplot(2, 1, 2)
plt.xticks(x_axis,timestamp_list,fontsize=7,rotation=0)
plt.plot(x_axis, total_list, 'k')
plt.grid('on')
plt.xlabel('Data Collected Time')
plt.ylabel('Numbers of Total Comments')
plt.xlim([-0.1, 10.1])
plt.show
# =============================================================================
# 성별
plt.figure(3)
x_axis = [i for i in range(10)]
w = 0.08
x_0 = [i*0.1 for i in range(2)]
x_1 = [i*0.1+1 for i in range(2)]
x_2 = [i*0.1+2 for i in range(2)]
x_3 = [i*0.1+3 for i in range(2)]
x_4 = [i*0.1+4 for i in range(2)]
x_5 = [i*0.1+5 for i in range(2)]
x_6 = [i*0.1+6 for i in range(2)]
x_7 = [i*0.1+7 for i in range(2)]
x_8 = [i*0.1+8 for i in range(2)]
x_9 = [i*0.1+9 for i in range(2)]

plt.bar(x_0[0], sex_list[0][0], width = w, color='blue')
plt.bar(x_0[1], sex_list[0][1], width = w, color='red')
plt.legend(['male', 'female'], loc='upper right')
plt.bar(x_1[0], sex_list[1][0], width = w, color='blue')
plt.bar(x_1[1], sex_list[1][1], width = w, color='red')
plt.bar(x_2[0], sex_list[2][0], width = w, color='blue')
plt.bar(x_2[1], sex_list[2][1], width = w, color='red')
plt.bar(x_3[0], sex_list[3][0], width = w, color='blue')
plt.bar(x_3[1], sex_list[3][1], width = w, color='red')
plt.bar(x_4[0], sex_list[4][0], width = w, color='blue')
plt.bar(x_4[1], sex_list[4][1], width = w, color='red')
plt.bar(x_5[0], sex_list[5][0], width = w, color='blue')
plt.bar(x_5[1], sex_list[5][1], width = w, color='red')
plt.bar(x_6[0], sex_list[6][0], width = w, color='blue')
plt.bar(x_6[1], sex_list[6][1], width = w, color='red')
plt.bar(x_7[0], sex_list[7][0], width = w, color='blue')
plt.bar(x_7[1], sex_list[7][1], width = w, color='red')
plt.bar(x_8[0], sex_list[8][0], width = w, color='blue')
plt.bar(x_8[1], sex_list[8][1], width = w, color='red')
plt.bar(x_9[0], sex_list[9][0], width = w, color='blue')
plt.bar(x_9[1], sex_list[9][1], width = w, color='red')
plt.grid('on')
plt.xlabel('Data Collected Time')
plt.ylabel('Sex Rate')
plt.title('Written time: ' + written_time)

plt.xticks(x_axis,timestamp_list,fontsize=7,rotation=0)
plt.show
# =============================================================================
# 나이
plt.figure(4)
x_axis = [i + 0.45 for i in range(10)]
age_10 = [i[0] for i in age_list]
age_20 = [i[1] for i in age_list]
age_30 = [i[2] for i in age_list]
age_40 = [i[3] for i in age_list]
age_50 = [i[4] for i in age_list]
age_60 = [i[5] for i in age_list]
w = 0.08
x_0 = [0.1 + i for i in range(10)]
x_1 = [0.2 + i for i in range(10)]
x_2 = [0.3 + i for i in range(10)]
x_3 = [0.4 + i for i in range(10)]
x_4 = [0.5 + i for i in range(10)]
x_5 = [0.6 + i for i in range(10)]
x_6 = [0.7 + i for i in range(10)]
x_7 = [0.8 + i for i in range(10)]
x_8 = [0.9 + i for i in range(10)]
x_9 = [1 + i for i in range(10)]

plt.bar(x_0, age_10, width = w, color='red')
plt.bar(x_1, age_20, width = w, color='orange')
plt.bar(x_2, age_30, width = w, color='yellow')
plt.bar(x_3, age_40, width = w, color='green')
plt.bar(x_4, age_50, width = w, color='blue')
plt.bar(x_5, age_60, width = w, color='purple')
plt.legend(['age_10', 'age_20', 'age_30', 'age_40', 'age_50', 'age_60'], loc='upper right')
plt.grid('on')
plt.xlabel('Data Collected Time')
plt.ylabel('Age Rate')
plt.title('Written time: ' + written_time)

plt.xticks(x_axis,timestamp_list,fontsize=7,rotation=0)
plt.show
# =============================================================================
# 댓글 순서
plt.figure(5)
x_axis = [i + 0.45 for i in range(10)]
y_axis = [i + 1 for i in range(10)]
y_top = [i for i in range(10, 0, -1)]
color_list = ['lightcoral', 'red', 'orange', 'yellow', 'lightgreen', 'green', 'skyblue', 'blue', \
              'midnightblue', 'purple', 'magenta', 'indigo', 'pink', 'cyan', 'slategrey', 'brown',\
              'olive', 'teal']

for idx, value in enumerate(total_comments_final):
    plt.plot(x_axis, value, '-o', color=color_list[idx])

plt.grid('on')
plt.xlabel('Data Collected Time')
plt.ylabel('Top 10 Comments')
plt.title('Written time: ' + written_time)

plt.xticks(x_axis,timestamp_list,fontsize=7,rotation=0)
plt.yticks(y_axis,y_top,fontsize=7,rotation=0)
plt.ylim([0.1, 11])
plt.show