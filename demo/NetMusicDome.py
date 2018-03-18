from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
import re
import Net_Compare
from selenium.common.exceptions import NoSuchElementException
"""
思路：因为网易云是ajax，所以单纯采用requests和BeautifulSoup是很难实现的，有些网站可以实现，但是网易云的js的请求是post，并且date是动态变化加密的。
所以这里我们引入selenium库来模拟浏览器行为获取网页。
1,先用显式浏览器在测试代码
2,显式完毕之后调用head less来进行测试
3,放置服务器进行设置
"""
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
                    # print(type(a.page_source))
                    # print(a.page_source)
                    # 声明正则表达式
                    pattern = re.compile('<b title=".*?">(.*?)</b>.*?hidefocus="true">(.*?)</a>.*?style="width:(.*?);"', re.S)
                    gorp = re.findall(pattern, a.page_source)
                    # 将读取到的数据存入文本文档
                    for i in gorp:
                        f = open("song/"+id+'.txt', 'a+', encoding='utf-8')
                        f.write(i[0]+':'+i[1].replace('\xa0', ' ')+'   '+i[2]+'\n')
                        f.close()
                    print('存取成功！')
        a.quit()
        if state == 1:
            main()
        else:
            Net_Compare.compare(id, id1)

    except NoSuchElementException:
        if state == 1:
            print('ID输入错误，请重新输入！')
            a.close()
            input_id()
        if state == 2:
            print(str(id)+'该用户数据被设为隐私，不可爬取')
            main()

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
