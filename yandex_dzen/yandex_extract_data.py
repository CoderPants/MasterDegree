import datetime
import os
import time
from pathlib import Path

from selenium import webdriver


def scrollToComments(curDriver):
    last_height = curDriver.execute_script("return document.body.scrollHeight")
    pagesAmount = 0
    while True and pagesAmount <= 2:
        pagesAmount += 1
        # Scroll down to bottom
        try:
            curDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            print(e)
            continue
        # Wait to load page
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height
        new_height = curDriver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def openAllComments(curDriver):
    # open all coments
    while True:
        try:
            buttons = curDriver.find_elements_by_class_name("comment-more-button")
            button = next(button for button in buttons if "Еще" in str(button.text))
            button.click()
        except Exception as e:
            break
    # show comments, if them are to long
    while True:
        try:
            buttons = curDriver.find_elements_by_class_name("comment__full-comment-button")
            if len(buttons) == 0:
                return

            with open(logFilePath, 'a') as logFile:
                logFile.write("Buttons size " + str(len(buttons)))
                logFile.write('\n')
            for button in buttons:
                button.click()
        except Exception as e:
            with open(logFilePath, 'a') as logFile:
                logFile.write("Can't perform a click")
                logFile.write('\n')
            break


def getContent(curDriver):
    allTexts = [extractedText.text for extractedText in
                curDriver.find_elements_by_class_name("article-render__block")]
    errorTexts = [errorText.text for errorText in
                  curDriver.find_elements_by_class_name("article-image__caption")]
    return [text for text in allTexts if text not in errorTexts and len(text) > 0]


    allTypesPrefix = '/home/misha/MasterDegree/Dzen/Top'
    allExtractedPrefix = '/home/misha/MasterDegree/Dzen/Top_Extracted'
    logFilePath = '/home/misha/MasterDegree/Dzen/log.txt'
    dirs = os.listdir(allTypesPrefix)
    for package in dirs:
        packagePath = allTypesPrefix + "/" + package
        curTypePath = allExtractedPrefix + "/" + package
        path = Path(curTypePath)
        if not path.exists():
            path.mkdir()
        files = os.listdir(packagePath)
        for file in files:
            with open(logFilePath, 'a') as logFile:
                logFile.write(
                    ("Time: " + str(datetime.datetime.now()) + " Opening file " + str(file) + " package " + str(package)))
                logFile.write('\n')
            with webdriver.Firefox() as driver:
                driver.set_page_load_timeout(30)
                extractedGroupPath = packagePath + "/" + file
                curGroupPath = curTypePath + "/" + file.replace('.txt', '').replace('Dzen_Urls_', '')
                path = Path(curGroupPath)
                if not path.exists():
                    path.mkdir()
                with open(extractedGroupPath, 'r') as _file:
                    links = [line.rstrip('\n') for line in _file]
                for link in links:
                    print("Link " + link + " file " + file + " package " + package)
                    if 'zen.yandex.ru' not in link:
                        print('Invalid link')
                        continue

                    curId = round(time.time() * 1000)
                    try:
                        driver.get(link)
                        scrollToComments(driver)

                        texts = getContent(driver)
                        if len(texts) == 0:
                            continue
                        openAllComments(driver)
                        comments = [extractedComment.text for extractedComment in
                                    driver.find_elements_by_class_name("comment")]
                        tags = [extractedTags.text for extractedTags in
                                driver.find_elements_by_class_name('zen-tag-publishers__title')]

                        contentFileName = curGroupPath + '/' + "Content_" + str(curId)
                        commentFileName = curGroupPath + '/' + "Comments_" + str(curId)
                        tagsFileName = curGroupPath + '/' + "Tags_" + str(curId)

                        with open(contentFileName, 'x') as contentFile:
                            for text in texts:
                                contentFile.write(text + "\n")
                        with open(commentFileName, 'x') as commentFile:
                            for comment in comments:
                                commentFile.write(comment + "\n")
                        with open(tagsFileName, 'x') as tagsFile:
                            for tag in tags:
                                tagsFile.write(tag + "\n")

                    except Exception as e:
                        with open(logFilePath, 'a') as logFile:
                            logFile.write("Time: " + str(datetime.datetime.now()) + " Exception " + str(e))
                            logFile.write('\n\n')
                    time.sleep(2)
            with open(logFilePath, 'a') as logFile:
                logFile.write("Time: " + str(datetime.datetime.now()) + " Removing file " + str(file) +
                              " package " + str(package))
                logFile.write('\n')
            print("Time: " + str(datetime.datetime.now()) + " Removing file " + str(file) + " package " + str(package))
            os.remove(extractedGroupPath)
        with open(logFilePath, 'a') as logFile:
            logFile.write("Time: " + str(datetime.datetime.now()) + " Removing package " + str(package))
            logFile.write('\n')
        print("Time: " + str(datetime.datetime.now()) + " Removing package " + str(package))
        os.rmdir(packagePath)
