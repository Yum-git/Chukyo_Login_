from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time


# WebDriverの初期設定
def DriverInit():
    # どんな環境でもSeleniumで動かせるよー
    op = Options()
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--start-maximized")
    op.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=op, executable_path='WebDriver/chromedriver.exe')

    return driver


def DriverWait(driver, url):
    start = time.time()
    # ページ情報取得
    selector = 'body'

    # 本番環境
    driver.get(url)

    # テスト環境
    # driver.get('file:///' + url)

    # JavaScript等の動的処理を待つ関数
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )

    # 5秒待機する
    delay = time.time() - start
    if delay < 5:
        time.sleep(5 - delay)

    return driver


def LoginProcess(driver, name, password):
    print(driver.current_url)
    driver.find_element_by_id('username').send_keys(name)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_css_selector('.form-element.form-button').click()

    print(driver.current_url)
    page_base = BeautifulSoup(driver.page_source, features="html.parser")

    return page_base


def PageScraping(page):
    category_list = page.select("[class='tab-newslist']")

    for category in category_list:
        Notion_Title_list = category.select('a')

        for Title in Notion_Title_list:
            Title_base = Title.get_text(strip=True)
            print(Title_base)


def main():
    driver = DriverInit()
    try:

        UserName = input('学籍番号：')
        PassWord = input('パスワード：')

        URL = 'https://cubics-pt-out.mng.chukyo-u.ac.jp/uniprove_pt/UnLoginControl'

        DriverWait(driver, URL)
        page_base = LoginProcess(driver, UserName, PassWord)

        time.sleep(5)

        PageScraping(page_base)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()