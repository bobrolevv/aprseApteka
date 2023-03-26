import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def get_data():
    url = "https://apteka-april.ru/catalog/396070-lekarstvennye_preparaty_i_bady/3872-sredstva_dlya_lecheniya_prostudy_i_grippa"
    # url = "https://apteka-april.ru/catalog/396070-lekarstvennye_preparaty_i_bady/3872-sredstva_dlya_lecheniya_prostudy_i_grippa/492-lechenie_otita"
    driver_path = "C:/Users/user/PycharmProjects/pythonProject/chromedriver_w/chromedriver.exe"
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(
        executable_path=driver_path,
        options=options
    )

    # driver.maximize_window()


    try:
        driver.get(url=url)
        time.sleep(5)
        print('==driver GET==')

        while True:

            find_more_element = driver.find_element_by_class_name("load-more")
            print(find_more_element.text)

            if find_more_element.text:
                driver.execute_script("arguments[0].click();", find_more_element)
                time.sleep(3)

            else:
                print('==else==')
                with open("source-page0.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

def parse_data():
        with open("source-page0.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        items_divs = soup.find_all("div", class_="card-info")

        urls = []
        for item in items_divs:
            item_url = item.find("a", class_="name").get("href")
            urls.append(item_url)

        with open("items_urls2.txt", "w") as file:
            for url in urls:
                file.write(f"https://apteka-april.ru{url}\n")


# get_data()
parse_data()