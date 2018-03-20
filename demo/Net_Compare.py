# 无聊写一个对比歌曲重合度的一个小Dome
import codecs
import NetMusicDome
import pymysql.cursors

def ztt(id , id1):
    connect = pymysql.Connect(
        host='47.100.21.174',
        port=3306,
        user='root',
        passwd='root',
        db='NeteaseMusicResult',
        charset='utf8'
    )
    cursor = connect.cursor()
    sql = "select * from a"+id
    try:
        cursor.execute(sql)
    except Exception:
        print('正在存取'+str(id)+'的数据，请稍后')
        NetMusicDome.Work_Mian(id, 2, id1)
        cursor.execute(sql)

    result = cursor.fetchall()
    return result


def compare(id1, id2):
    print('正在对比，请稍后.....')
    one = ztt(id1, id2)
    two = ztt(id2, id1)
    sum = 0
    print('你们匹配到的歌曲是：')
    try:
        for z in range(len(one)):
            for y in range(len(two)):
                if one[z][1] == two[y][1] and one[z][2] == two[y][2]:
                    print(one[z][1], one[z][2])
                    sum = sum+1
    except TypeError:
        a = 0
    if sum==0:
        print('无')
    print('你们之间的歌曲匹配度是:' + str(sum) + '%')
