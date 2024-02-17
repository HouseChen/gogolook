#/usr/bin/env python3
# -*-  coding: utf-8 -*-

import logging
import time

from lib.SDET_COMMON import SdetWebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

BASIC_FORMAT = "%(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=BASIC_FORMAT)

base_url = "https://www.twse.com.tw/zh/index.html"

sdet_web_driver = SdetWebDriver()
sdet_web_driver.sdet_open_browser()

logging.info('步驟1. 前往 台灣證券交易所 頁面 https://www.twse.com.tw/zh/index.html')
sdet_web_driver.web_driver.get(base_url)

logging.info('步驟2. 點選 交易資訊-個股日收盤價及月平均價 進入頁面')
sdet_web_driver.sdet_click_element("//*[@id='mega']/ul/li[2]/a")
sdet_web_driver.sdet_click_element("//*[@id='mega']/ul/li[2]/div/div/ul[1]/li[10]")

logging.info('步驟3. 選取年份 民國 112 年 01 月')
yy_xpath = "//*[@id='form']/div/div[1]/div[1]/span/select[1]"
mm_xpath = "//*[@id='form']/div/div[1]/div[1]/span/select[2]"
input_code = "//*[@id='label1']"
btn_submit = "//*[@id='form']/div/div[1]/div[3]/button"

select = Select(sdet_web_driver.web_driver.find_element(By.XPATH, yy_xpath))
select.select_by_value('2023')
select = Select(sdet_web_driver.web_driver.find_element(By.XPATH, mm_xpath))
select.select_by_value('1')

logging.info('步驟4. 輸入股票代碼 2330')
# sdet_web_driver.sdet_fill_text(input_code, '2330') 打太快造成網路連線異常

sdet_web_driver.sdet_fill_text(input_code, '2')
sdet_web_driver.sdet_fill_text(input_code, '3')
sdet_web_driver.sdet_fill_text(input_code, '3')
sdet_web_driver.sdet_fill_text(input_code, '0')

logging.info('步驟5. 點選查詢按鈕')
sdet_web_driver.sdet_click_element(btn_submit)

logging.info('步驟6. 將台積電 112 年 01 月份的每日收盤價 print 出來')
table_xpath = "//*[@id='reports']//table/tbody"
table_ele = sdet_web_driver.web_driver.find_element(By.XPATH, table_xpath)
for item in table_ele.find_elements(By.TAG_NAME, "tr"):
    print(item.text)

logging.info('步驟7. 截圖台積電 112 年 01 月份的每日收盤價資訊')
anchor = "//*[@id='reports']//h2"
sdet_web_driver.sdet_scroll_to(anchor)
sdet_web_driver.sdet_save_screenshot("112_01")

time.sleep(3)
sdet_web_driver.web_driver.quit()
