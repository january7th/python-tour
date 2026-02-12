import os
import time

from selenium.webdriver.common.by import By

import los_support.constants as const
from selenium import webdriver

class ReportSale(webdriver.Chrome):
    def __init__(self, driver_path=r"D:\Tools\SeleniumDriver", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(ReportSale, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def login(self):
        self.get(const.LOS_SUPPORT_URL)
        self.implicitly_wait(10)
        username_input = self.find_element(By.CSS_SELECTOR, 'input[placeholder="Username"]')
        username_input.send_keys('sale1')
        password_input = self.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]')
        password_input.send_keys('It123456')
        login_button = self.find_element(By.XPATH, "//button[text()='Đăng nhập']")
        login_button.click()

    def go_to_sale_report(self):
        self.implicitly_wait(50)
        sale_department_element = self.find_element(By.CSS_SELECTOR, 'li[title="Kinh doanh"]')
        sale_department_element.click()
        sale_report_element = self.find_element(By.CSS_SELECTOR, 'li[title="Truy vấn hồ sơ"]')
        sale_report_element.click()
        self.implicitly_wait(3)
        try:
            search_button = self.find_element(By.XPATH, "//button[text()=' Tìm kiếm']")
            for i in range(10):
                search_button.click()
                time.sleep(5)
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")






