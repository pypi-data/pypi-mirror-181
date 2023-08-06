import os
import time

from selenium.webdriver import Keys

from main import Upload
import win32gui, win32con
from seliky import WebDriver

ups = Upload(win32gui, win32con, browser_type='firefox')
p = WebDriver(executable_path="D:\s\python38\geckodriver.exe")
p.open_browser()
p.get('https://www.baidu.com/')
p.click('//span[@class="soutu-btn"]')
loc = "//span[text()='选择文件']"
loc2 = '//input[@class="upload-pic"]'
go = '//input[@value="百度一下"]'

ups.close_if_opened()
p.click2(loc2) # 运行时可以打开，谷歌浏览器调试时打不开，调试时打开得以下面这种方式，因为windows句柄得被聚焦，这是和系统交互。
# p.click2(loc2).click()  # 调试时打不开
# p.find_element(loc2).send_keys(Keys.CONTROL, 'o')  # 打不开时可以尝试这种方式，一般在有明确表明快捷键的情况下可以。
file_path = os.path.abspath('demo1.png')
ups.upload(file_path)
