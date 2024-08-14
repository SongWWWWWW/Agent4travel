import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
service = Service(executable_path="C:\\Users\\22476\\Downloads\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(options=chrome_options, service=service)

# 打开网页
driver.get('http://www.baidu.com')

# 找到搜索输入框（通过name属性）
search_box = driver.find_element(By.NAME, 'wd')

# 在搜索框中输入查询内容
search_query = "Python Selenium 教程"
search_box.send_keys(search_query)

# 模拟按下回车键，进行搜索
search_box.send_keys(Keys.RETURN)

# 等待搜索结果加载（可根据需要设置等待时间）
time.sleep(3)

# 抓取搜索结果的标题和链接
results = driver.find_elements(By.CSS_SELECTOR, 'h3.t a')
for result in results:
    title = result.text
    link = result.get_attribute('href')
    print(f"标题: {title}\n链接: {link}\n")

# 关闭浏览器
driver.quit()