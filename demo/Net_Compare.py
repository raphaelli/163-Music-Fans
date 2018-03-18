# 无聊写一个对比歌曲重合度的一个小Dome
import codecs
import NetMusicDome


def ztt(id , id1):
    try:
        ztt = codecs.open('song/'+id+'.txt', 'r', encoding='UTF-8')

    except IOError:
        print(str(id)+'正在存取该用户数据，请稍后')
        NetMusicDome.Work_Mian(id, 2, id1)
        ztt = codecs.open('song/' + id + '.txt', 'r', encoding='UTF-8')
    else:

        content = ztt.readlines()
        for i in range(len(content)):
            content[i] = content[i][:-8]
        return content



def compare(id1, id2):
    print('正在对比，请稍后.....')
    one = ztt(id1, id2)
    two = ztt(id2, id1)
    sum = 0
    try:
        for z in one:
            for y in two:
                if z == y:
                    sum = sum + 1
                    print(z)
    except TypeError:
        a = 0
    else:
        print('你们之间的歌曲匹配度是:' + str(sum) + '%')


