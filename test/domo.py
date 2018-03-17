from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
import re

"""
思路：因为网易云是ajax，所以单纯采用requests和BeautifulSoup是很难实现的，有些网站可以实现，但是网易云的js的请求是post，并且date是动态变化加密的。
所以这里我们引入selenium库来模拟浏览器行为获取网页。
1,先用显式浏览器在测试代码
2,显式完毕之后调用head less来进行测试
3,放置服务器进行设置
"""

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--window-size=1280,800")
chrome_options.binary_location ="H:\Program Files (x86)\Chrome\Application\chrome.exe"
# 声明浏览器
a = webdriver.Chrome(chrome_options=chrome_options)
# 爬取地址
a.get("http://music.163.com/#/user/songs/rank?id=xxxxxxxx")
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
                f = open('song.txt', 'a+', encoding='utf-8')
                f.write(i[0]+':'+i[1].replace('\xa0', ' ')+'   '+i[2]+'\n')
                f.close()
a.quit()