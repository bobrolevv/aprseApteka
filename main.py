# This is the way
# Author: pythontoday
# YouTube: https://www.youtube.com/c/PythonToday/videos

import json
import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup


def get_data(url):
    headers = {
        # "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36",

        "user-agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit 537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser / 23.1.5.708 Yowser / 2.5 Safari / 537.36",
        "cooke": "yandexuid=6632749951672330114; yuidss=6632749951672330114; ymex=1987690116.yrts.1672330116; gdpr=0; _ym_uid=1672330116524305286; is_gdpr=0; is_gdpr_b=CJaLGxDrnQEoAg==; yandex_login=bobrolevv; my=YwA=; yabs-frequency=/5/500004twpsC00000/; i=kw+Y1BoszcguK+MPa12QMs/yunKR/uOvSGPqiCa5h5uEIolnns+Mpvv/PyLX28GZ1+WBoXc1inj7JcwW6jFLuUTFps0=; cycada=7eg1yRuwVUXyaiCKHLT0qP2+C8vVCk4l8SgFjqY1uXY=; Session_id=3:1679758971.5.0.1672330537622:39dKgA:3f.1.2:1|54132089.0.2|3:10267449.525493.jHjAUjaLagWDE0J_dA81ZUGMsUM; sessionid2=3:1679758971.5.0.1672330537622:39dKgA:3f.1.2:1|54132089.0.2|3:10267449.525493.fakesign0000000000000000000; _ym_isad=2; sae=0:2BC9B029-7BA2-4532-9DDA-537BD72F9AC7:p:23.1.5.708:w:d:RU:20221229; _ym_d=1679825699; yabs-sid=728254021679825702; ys=svt.1#def_bro.1#ead.2FECB7CF:AB4770B4#wprid.1679826310016175-9234298197725028553-sas2-0343-sas-l7-balancer-8080-BAL-4465#ybzcc.ru#newsca.native_cache; yp=1679912064.uc.ru#1679912064.duc.ru#1703866116.cld.2378379#1995186308.pcs.0#1987690537.udn.cDrQkNGA0YLRkdC8#1679846088.mcv.2#1679846088.mcl.97gyta#1679846088.szm.1:1680x1050:1632x934#1679833464.gpauto.55_355202:86_086845:100000:3:1679826264"

    }

    projects_data_list = []
    iteration_count = 23
    print(f"Всего итераций: #{iteration_count}")

    for item in range(1, 24):
        req = requests.get(url + f"&PAGEN_1={item}&PAGEN_2={item}", headers)

        folder_name = f"data/data_{item}"

        if ospath.exists(folder_name):
            print("Папка уже существует!")
        else:
            os.mkdir(folder_name)

        with open(f"{folder_name}/projects_{item}.html", "w") as file:
            file.write(req.text)

        with open(f"{folder_name}/projects_{item}.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        articles = soup.find_all("article", class_="ib19")

        projects_urls = []
        for article in articles:
            project_url = "http://www.edutainme.ru" + article.find("div", class_="txtBlock").find("a").get("href")
            projects_urls.append(project_url)

        for project_url in projects_urls:
            req = requests.get(project_url, headers)
            project_name = project_url.split("/")[-2]

            with open(f"{folder_name}/{project_name}.html", "w") as file:
                file.write(req.text)

            with open(f"{folder_name}/{project_name}.html") as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            project_data = soup.find("div", class_="inside")

            try:
                project_logo = "http://www.edutainme.ru" + project_data.find("div", class_="Img logo").find("img").get("src")
            except Exception:
                project_logo = "No project logo"

            try:
                project_name = project_data.find("div", class_="txt").find("h1").text
            except Exception:
                project_name = "No project name"

            try:
                project_short_description = project_data.find("div", class_="txt").find("h4", class_="head").text
            except Exception:
                project_short_description = "No project short description"

            try:
                project_website = project_data.find("div", class_="txt").find("p").find("a").text
            except Exception:
                project_website = "No project website"

            try:
                project_full_description = project_data.find("div", class_="textWrap").find("div", class_="rBlock").text
            except Exception:
                project_full_description = "No project full description"

            def replace_string(string):
                return ''.join(re.sub(r'(<p>|</p>)', "", string))
            project_full_description = replace_string(project_full_description)

            # rep = ["<p>", "</p>"]
            # for s in rep:
            #     if s in project_full_description:
            #         project_full_description = project_full_description.replace(s, "")

            projects_data_list.append(
                {
                    "Имя проекта": project_name,
                    "URL логотипа проекта": project_logo,
                    "Короткое описание проекта": project_short_description,
                    "Сайт проекта": project_website,
                    "Полное описание проекта": project_full_description.strip()
                }
            )

        iteration_count -= 1
        print(f"Итерация #{item} завершена, осталось итераций #{iteration_count}")
        if iteration_count == 0:
            print("Сбор данных завершен")
        time.sleep(random.randrange(2, 4))

    with open("data/projects_data.json", "a", encoding="utf-8") as file:
        json.dump(projects_data_list, file, indent=4, ensure_ascii=False)


def get_test(url):
    headers = {
    "user-agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit 537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser / 23.1.5.708 Yowser / 2.5 Safari / 537.36",
    "cooke": "yandexuid=6632749951672330114; yuidss=6632749951672330114; ymex=1987690116.yrts.1672330116; gdpr=0; _ym_uid=1672330116524305286; is_gdpr=0; is_gdpr_b=CJaLGxDrnQEoAg==; yandex_login=bobrolevv; my=YwA=; yabs-frequency=/5/500004twpsC00000/; i=kw+Y1BoszcguK+MPa12QMs/yunKR/uOvSGPqiCa5h5uEIolnns+Mpvv/PyLX28GZ1+WBoXc1inj7JcwW6jFLuUTFps0=; cycada=7eg1yRuwVUXyaiCKHLT0qP2+C8vVCk4l8SgFjqY1uXY=; Session_id=3:1679758971.5.0.1672330537622:39dKgA:3f.1.2:1|54132089.0.2|3:10267449.525493.jHjAUjaLagWDE0J_dA81ZUGMsUM; sessionid2=3:1679758971.5.0.1672330537622:39dKgA:3f.1.2:1|54132089.0.2|3:10267449.525493.fakesign0000000000000000000; _ym_isad=2; sae=0:2BC9B029-7BA2-4532-9DDA-537BD72F9AC7:p:23.1.5.708:w:d:RU:20221229; _ym_d=1679825699; yabs-sid=728254021679825702; ys=svt.1#def_bro.1#ead.2FECB7CF:AB4770B4#wprid.1679826310016175-9234298197725028553-sas2-0343-sas-l7-balancer-8080-BAL-4465#ybzcc.ru#newsca.native_cache; yp=1679912064.uc.ru#1679912064.duc.ru#1703866116.cld.2378379#1995186308.pcs.0#1987690537.udn.cDrQkNGA0YLRkdC8#1679846088.mcv.2#1679846088.mcl.97gyta#1679846088.szm.1:1680x1050:1632x934#1679833464.gpauto.55_355202:86_086845:100000:3:1679826264"
        }

    req = requests.get(url, headers)

    # print(req.text)
    with open('targ.html', "w", encoding="utf-8") as file:
        file.write(req.text)

    # soup = BeautifulSoup(src, "lxml")
    # articles = soup.find_all("article", class_="ib19")


def main():
    # get_data("http://www.edutainme.ru/edindex/ajax.php?params=%7B%22LETTER%22%3Anull%2C%22RESTART%22%3A%22N%22%2C%22CHECK_DATES%22%3Afalse%2C%22arrWHERE%22%3A%5B%22iblock_startaps%22%5D%2C%22arrFILTER%22%3A%5B%22iblock_startaps%22%5D%2C%22startups%22%3A%22Y%22%2C%22SHOW_WHERE%22%3Atrue%2C%22PAGE_RESULT_COUNT%22%3A9%2C%22CACHE_TYPE%22%3A%22A%22%2C%22CACHE_TIME%22%3A0%2C%22TAGS_SORT%22%3A%22NAME%22%2C%22TAGS_PAGE_ELEMENTS%22%3A%22999999999999999999%22%2C%22TAGS_PERIOD%22%3A%22%22%2C%22TAGS_URL_SEARCH%22%3A%22%22%2C%22TAGS_INHERIT%22%3A%22Y%22%2C%22SHOW_RATING%22%3A%22Y%22%2C%22FONT_MAX%22%3A%2214%22%2C%22FONT_MIN%22%3A%2214%22%2C%22COLOR_NEW%22%3A%22000000%22%2C%22COLOR_OLD%22%3A%22C8C8C8%22%2C%22PERIOD_NEW_TAGS%22%3A%22%22%2C%22DISPLAY_TOP_PAGER%22%3A%22N%22%2C%22DISPLAY_BOTTOM_PAGER%22%3A%22N%22%2C%22SHOW_CHAIN%22%3A%22Y%22%2C%22COLOR_TYPE%22%3A%22Y%22%2C%22WIDTH%22%3A%22100%25%22%2C%22USE_LANGUAGE_GUESS%22%3A%22N%22%2C%22PATH_TO_USER_PROFILE%22%3A%22%23SITE_DIR%23people%5C%2Fuser%5C%2F%23USER_ID%23%5C%2F%22%2C%22SHOW_WHEN%22%3Afalse%2C%22PAGER_TITLE%22%3A%22%5Cu0420%5Cu0435%5Cu0437%5Cu0443%5Cu043b%5Cu044c%5Cu0442%5Cu0430%5Cu0442%5Cu044b+%5Cu043f%5Cu043e%5Cu0438%5Cu0441%5Cu043a%5Cu0430%22%2C%22PAGER_SHOW_ALWAYS%22%3Atrue%2C%22USE_TITLE_RANK%22%3Afalse%2C%22PAGER_TEMPLATE%22%3A%22%22%2C%22DEFAULT_SORT%22%3A%22rank%22%2C%22noTitle%22%3A%22Y%22%7D")
    get_test("https://apteka-april.ru/catalog/396070-lekarstvennye_preparaty_i_bady/3872-sredstva_dlya_lecheniya_prostudy_i_grippa")

if __name__ == "__main__":
    main()