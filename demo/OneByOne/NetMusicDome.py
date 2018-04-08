from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
import re
import Net_Compare
from selenium.common.exceptions import NoSuchElementException
import pymysql.cursors
from selenium.webdriver.common.keys import Keys
import string
"""
思路：因为网易云是ajax，所以单纯采用requests和BeautifulSoup是很难实现的，有些网站可以实现，但是网易云的js的请求是post，并且date是动态变化加密的。
所以这里我们引入selenium库来模拟浏览器行为获取网页。
1,先用显式浏览器在测试代码
2,显式完毕之后调用head less来进行测试
3,放置服务器进行设置
"""
def List_Song():#读取歌曲列表文件
    songlist = open('song/songlist.txt', 'r+')
    while 1:
        url = songlist.readline()

        if url == '\n' and url == '':
            break
        List_Song_Work(url.replace('\n', ''))
        if not url:
            break
    songlist.close()

def List_Song_Work(url):#读取歌曲
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.binary_location = "C:\Program Files (x86)\Chrome\Application\chrome.exe"
    # 声明浏览器
    web = webdriver.Chrome(chrome_options=chrome_options)
    # 爬取地址
    print('这是地址:'+url)
    if url=='':
        web.quit()
    else:
        web.get(url)
        web.switch_to.frame('g_iframe')
        web.implicitly_wait(30)
        pattern = re.compile('"txt"><a href="(.*?)"><b title=', re.S)
        gorp = re.findall(pattern, web.page_source)
        file = open('song/songname.txt', 'w+')
        for i in gorp:
            print(i)
            file.write('http://music.163.com/#'+i+'\n')
        file.close()
        web.quit()

def get_user():
    file = open('song/songname.txt', 'r+')
    while 1:
        line = file.readline()
        if not line:
            break
        print(line)
        List_user(line.replace('\n', ''))
    file.close()

def List_user(url):#读取用户
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.binary_location = "H:\Program Files (x86)\Chrome\Application\chrome.exe"
    # 声明浏览器H:\Program Files (x86)\Chrome\Application\chromedriver.exe
    web = webdriver.Chrome(chrome_options=chrome_options)
   # web = webdriver.Chrome('H:\Program Files (x86)\Chrome\Application\chromedriver.exe')
    web.get(url)
    web.switch_to.frame('g_iframe')
    web.implicitly_wait(30)
    pattern = re.compile('class="head"><a href="(.*?)"><img', re.S)
    gorp = re.findall(pattern, web.page_source)
    file = open('song/songuser.txt', 'w+')
    for i in gorp:
        file.write(str(i[14:]) + '\n')
        print(i[14:])
    sun = 1
    while 1:
        claass = web.find_element_by_link_text('下一页').get_attribute('class')
        if 'js-disabled' in claass:
            print('没有下一页了')
            file.close()
            break

        else:
            print('翻页！')
            # 元素被遮挡，用回车键代替单击键
            web.find_element_by_link_text('下一页').send_keys(Keys.ENTER)
            web.implicitly_wait(30)
            time.sleep(0.6)
            gorp = re.findall(pattern, web.page_source)
            for i in gorp:
                file.write(str(i[14:]) + '\n')
                print(i[14:])
    file.close()
    web.quit()


def Work_Mian_for():

    file = open('song/songuser.txt', 'r')
    while 1:
        line = file.readline()
        if not line:
            break
        Work_Mian(line.replace('\n', ''), state=3)
    file.close()





def Work_Mian(id, state=1 , id1=1):
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.binary_location ="H:\Program Files (x86)\Chrome\Application\chrome.exe"
    # 声明浏览器
    a = webdriver.Chrome(chrome_options=chrome_options)
    # 爬取地址
    url = 'http://music.163.com/#/user/songs/rank?id='
    url = url+id
    try:
        a.get(url)
        # 从window转到ifram
        a.switch_to.frame('g_iframe')
        # 显式等待声明
        wait = ui.WebDriverWait(a, 15)
        # 等待 a.find_element_by_class_name('g-bd') 记载
        if wait.until(lambda a: a.find_element_by_class_name('g-bd')):
            # 判断是否有"所有时间"按钮
            if a.find_element_by_xpath('//*[@id="songsall"]'):
                # 点击所有时间按钮，页面的ajax同步所有时间的结果
                a.find_element_by_xpath('//*[@id="songsall"]').click()
                # 强制等待 让界面刷新等待数据出现
                time.sleep(0.2)
                # 同上
                if wait.until(lambda a: a.find_element_by_class_name('g-bd')):
                    time.sleep(0.5)
                    # 声明正则表达式
                    # if a.find_element_by_link_text(' 加载中...'):
                    #     print(str(id) + '该用户数据被设为隐私，不可爬取')
                    # else:
                    pattern = re.compile('<b title=".*?">(.*?)</b>.*?hidefocus="true">(.*?)</a>.*?style="width:(.*?);"', re.S)
                    gorp = re.findall(pattern, a.page_source)
                    print(len(gorp))
                    if len(gorp)==0:
                        print(str(id) + '该用户数据被设为隐私，不可爬取')
                    else :
                        Data_Base(id=id, gorp=gorp, c=1)# 存入数据库
        a.quit()
        if state == 1:
            main()
        if state == 3:
            pass
        else:
            print('正在对比....')
            # Net_Compare.compare(id, id1)

    except NoSuchElementException:
        if state == 1:
            print('ID输入错误，请重新输入！')
            a.close()
            input_id()
        if state == 2:
            print(str(id)+'该用户数据被设为隐私，不可爬取')
            main()
        if state == 3:
            print(str(id) + '该用户数据被设为隐私，不可爬取')
            pass

def Data_Base(id, gorp, c=1):# 调用数据库

    connect = pymysql.Connect(
        host='',
        port=3306,
        user='root',
        passwd='root',
        db='NeteaseMusicResult',
        charset='utf8'
    )
    cursor = connect.cursor()

    if c == 1:#代表全新存入
        try:
            data = "create table a" + str(
                id) + "(id int(5) PRIMARY KEY,songname varchar(50),songer varchar(50),percentage char(5));"
            cursor.execute(data)
        except Exception:
            data_new ="truncate table a"+str(id)
            cursor.execute(data_new)
        d = 0
        for i in gorp:
            sql ="INSERT INTO a"+id+ "(id, songname, songer,percentage) VALUES ( '%d', '%s', '%s','%s')"
            # 防止有些单引号双引号
            c = i[1].replace('\xa0', ' ')
            sql_data = (d, i[0].replace('\'', '\\\''), c.replace('\'', '\\\''), i[2])
            d = d+1
            cursor.execute(sql%sql_data)
        cursor.close()
        connect.close()
        print('爬取成功！')



def input_id():
    print('请输入你要爬取的用户ID:')
    id = input()
    Work_Mian(id)
    main()

def Compare():
    print('请输入你要对比的第一个用户ID:')
    one = input()
    print('请输入你要对比的第二个用户ID:')
    two = input()
    Net_Compare.compare(one, two)
    main()

def main():
    print('请输入数字选择你要的功能:1,存入数据 2,信息匹配 3,退出')
    a = input()
    if a == str(1):
        input_id()
    if a == str(2):
        Compare()
    if a == str(3):
        print('beybey!')
        exit()
    if a != str(2) and a !=str(1) and a!=str(3):
        print('输入错误，请重新输入！')
        main()
if __name__ == '__main__':
    main()