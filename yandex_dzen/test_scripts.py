import time

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
    #open all coments
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
            button = next(button for button in buttons if "Еще" in str(button.text))
            button.click()
        except Exception as e:
            break


def getContent(curDriver):
    allTexts = [extractedText.text for extractedText in
                curDriver.find_elements_by_class_name("article-render__block")]
    errorTexts = [errorText.text for errorText in
                  curDriver.find_elements_by_class_name("article-image__caption")]
    return [text for text in allTexts if text not in errorTexts and len(text) > 0]


with webdriver.Firefox() as driver:
    driver.set_page_load_timeout(10)
    link = "https://zen.yandex.ru/media/kolesa.ru/porsche--znachit-puteshestvie-5fd8d6e9b11a4f02b75e0eec?feed_exp=ordinary_feed&from=channel&rid=1629868127.48.1610296127728.98435&integration=site_desktop&place=more&secdata=CPiZybjmLiABMAJQD1gA"
    linkCrash = "https://www.kolesa.ru/news/yubiley-na-moskovskom-zavode-renault-s-konveyera-soshlo-1-500-000-avtomobiley"
    link2 = "https://zen.yandex.ru/media/chastnye_suzhdenija/strannyi-epizod-sovetskoi-kinoskazki-charodei-606c374a7e1f3129bb2c3c58"
    driver.get(link2)
    scrollToComments(driver)

    texts = getContent(driver)
    openAllComments(driver)
    comments = [extractedComment.text for extractedComment in
                driver.find_elements_by_class_name("comment")]
    tags = [extractedTags.text for extractedTags in
            driver.find_elements_by_class_name('zen-tag-publishers__title')]

    print(texts)
    print(comments)
    print(tags)
