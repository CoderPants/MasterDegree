import os
import re
import time

# import requests
# from dragnet import extract_content_and_comments

# request = requests.get("https://lifehacker.ru/tonkoe-iskusstvo-pofigizma/?utm_referrer=https%3A%2F%2Fzen.yandex.com")
# content_comments = extract_content_and_comments(request.content)
# print(content_comments)
from os import listdir
from os.path import isfile, join
from pathlib import Path

from selenium import webdriver


def isIncorrectUrl(_url):
    return _url == "None" or \
           ("other_page" in _url) \
           or ("about" in _url) \
           or ("support" in _url) \
           or ("adv" in _url) \
           or (_url == "https://zen.yandex.ru/") \
           or (_url == "https://yandex.ru/") \
           or ("channels" in _url) \
           or ("legal" in _url) \
           or ("partner" in _url) \
           or ("twitter" in _url) \
           or ("instagram" in _url) \
           or ("youtube" in _url) \
           or ("facebook" in _url) \
           or ("vk" in _url) \
           or ("test" in _url)


SCROLL_PAUSE_TIME = 2
# with webdriver.Firefox() as driver:
#     driver.get("https://zen.yandex.ru/top")
#     time.sleep(2)
#     elements = driver.find_elements_by_css_selector("a")
#     categoryLinks = list()
#     for element in elements:
#         try:
#             url = str(element.get_attribute("href"))
#             if "https://zen.yandex.ru/top/" not in url:
#                 continue
#             categoryLinks.append(url)
#         except Exception as e:
#             print(e)
#             continue
#     # startingLinks = list()
#     # names = list()
#     directory = "/home/misha/MasterDegree/Dzen/Top_Groups/"
#     for categoryLink in categoryLinks:
#         #print(categoryLink)
#         driver.get(categoryLink)
#         time.sleep(2)
#         groups = driver.find_elements_by_class_name("channel-row__wrap")
#         groupNames = driver.find_elements_by_class_name("channel-row__title")
#         index = 0
#         filePath = directory + categoryLink.replace("https://zen.yandex.ru/top/", "").capitalize() + ".txt"
#         print(filePath)
#         for group in groups:
#             try:
#                 url = str(group.get_attribute("href"))
#                 #startingLinks.append(url)
#                 # print("Group url: " + url)
#                 name = str(groupNames[index].text)
#                 index += 1
#                 #names.append(name)
#                 with open(filePath, 'a') as file:
#                     file.write(name + ": " + url + "\n")
#                 # print("Group name: " + name)
#             except Exception as e:
#                 print(e)
#                 index += 1
#                 continue
directoryPath = "/home/misha/MasterDegree/Dzen/Top_Groups/"
files = [f for f in listdir(directoryPath) if isfile(join(directoryPath, f))]
for categoryFile in files:
    newDirectory = os.path.splitext(categoryFile)[0]
    with open(directoryPath + categoryFile, 'r') as file:
        groups = [line.rstrip('\n') for line in file]
    for group in groups:
        nameAndUrl = group.split(": ")
        groupName = nameAndUrl[0].replace(" ", "_")
        groupName = re.sub(r'[^\w\s]', '', groupName)
        groupUrl = nameAndUrl[1]
        if not groupUrl.startswith("https"):
            continue
        time.sleep(10)
        with webdriver.Firefox() as driver:
            try:
                driver.get(groupUrl)
            except Exception as e:
                continue
            time.sleep(SCROLL_PAUSE_TIME)
            last_height = driver.execute_script("return document.body.scrollHeight")
            pagesAmount = 0
            while True and pagesAmount <= 200:
                pagesAmount += 1
                print("Page: " + str(pagesAmount))
                # Scroll down to bottom
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except Exception as e:
                    print(e)
                    continue
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            elements = driver.find_elements_by_css_selector("a")
            print("Links size: " + str(len(elements)))
            if len(elements) > 0:
                filePath = "/home/misha/MasterDegree/Dzen/Top/" + newDirectory + "/"
                fileName = filePath + "Dzen_Urls_" + groupName + ".txt"
                if not Path(fileName).exists():
                    print("Filename: " + fileName)
                    Path(filePath).mkdir(parents=True, exist_ok=True)
                    links = list()
                    for element in elements:
                        try:
                            url = str(element.get_attribute("href"))
                            if isIncorrectUrl(url):
                                continue
                            links.append(url)
                        except Exception as e:
                            print(e)
                            continue
                    print("Opening file " + fileName)
                    try:
                        with open(fileName, 'a') as file:
                            for distinctLink in links:
                                file.write(distinctLink + "\n")
                    except Exception as e:
                        print(e)
    # index = 0
    # for startingLink in startingLinks:
    #     print("Starting Link: " + startingLink)
    #     driver.get(startingLink)
    #     last_height = driver.execute_script("return document.body.scrollHeight")
    #     pagesAmount = 0
    #     while True:
    #         pagesAmount += 1
    #         print("Page: " + str(pagesAmount))
    #         # Scroll down to bottom
    #         try:
    #             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         except Exception as e:
    #             print(e)
    #             continue
    #         # Wait to load page
    #         time.sleep(SCROLL_PAUSE_TIME)
    #         # Calculate new scroll height and compare with last scroll height
    #         new_height = driver.execute_script("return document.body.scrollHeight")
    #         if new_height == last_height:
    #             break
    #         last_height = new_height
    #     elements = driver.find_elements_by_css_selector("a")
    #     print("Links size: " + str(len(elements)))
    #     if len(elements) > 0:
    #         filePath = "/home/misha/MasterDegree/Dzen/Top/"
    #         fileName = filePath + "Dzen_Urls_" + names[index] + ".txt"
    #         print("Filename: " + fileName)
    #         index += 1
    #         links = list()
    #         for element in elements:
    #             try:
    #                 url = str(element.get_attribute("href"))
    #                 if isIncorrectUrl(url):
    #                     continue
    #                 links.append(url)
    #             except Exception as e:
    #                 print(e)
    #                 continue
    #         distinctLinks = list(set(links))
    #         print("Links size: " + str(len(links)) + " Distinct links size: " + str(len(distinctLinks)))
    #         with open(fileName, 'w') as file:
    #             for distinctLink in distinctLinks:
    #                 file.write(url + "\n")
