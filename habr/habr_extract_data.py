# Extract content from website
import re
import time

from selenium import webdriver

test = "BubaVV\n19 марта 2021 в 17:19\n-0\ntext"
regexComments = '\w+\n\d+\s\w+\s\d+\s\w\s\d+:\d+\n?\D*?\d+\n'
regex = re.compile(regexComments)
# test = 'Интересна природа появления этих трещин. Как я понял, их же не было изначально. То есть они появились уже наверху. Если это так, может настать момент когда частота появления трещин возрастёт и модуль перестанет быть пригодным dolbi 17 марта 2021 в 11:03 OvO 17 марта 2021 в 11:50 Wizard_of_light 17 марта 2021 в 12:16 Корпус постоянно подвергается деформациям из-за неравномерного нагрева (тень остывает, солнечная сторона нагрев), смены дня и ночи(днем нагрев, ночью остывание. Деформации микроскопические, но за много лет из-за деформаций накапливается «усталость» металла, что выливается в трещины.     DmitriiR 17 марта 2021 в 10:43 altone 17 марта 2021 в 12:42 Да. В прошлый раз был именно целый пакетик(и за это утверждение мне обильно насыпали минусов), но новость переврали в т.ч. и на Хабре. Сейчас решили рассыпать. Это несёт за собой некоторые риски, но видимо меньшие чем не обнаруженные трещины. unsignedchar 18 марта 2021 в 16:00'
# regexed = regex.sub('', test)
# print(regexed)
# "BubaVV"
# "19 марта 2021 в 17:19"
# "0"
# "text"
path = '/home/misha/MasterDegree/Habr-Habr/UpdatedPosts/'
fileWithFilteredLinks = 'HabrLinks_Filtered_Extracted.txt'
with open(path + fileWithFilteredLinks, 'r') as file:
    links = [line.rstrip('\n') for line in file]

postIds = [list(filter(lambda elem: len(elem) > 0, link.split('/')))[-1] for link in links]

contentPrefix = path + 'Posts/Habr_Post_Content_Number_'
commentsPrefix = path + 'Posts/Habr_Post_Comments_Number_'
tagsPrefix = path + 'Posts/Habr_Post_Tags_Number_'
exceptionFile = path + 'Exceptions.txt'

with webdriver.Firefox() as driver:
    for index, link in enumerate(links):
        try:
            # <div class="post__text post__text_v2" id="post-content-body">
            # postBody = driver.find_element_by_class_name('post__body post__body_full')
            curId = postIds[index]
            driver.get(link)

            postBodyElem = driver.find_element_by_id("post-content-body")
            commentsElem = driver.find_element_by_id("comments")
            tagsElem = driver.find_element_by_class_name("post__tags-list")

            onlyComments = regex.sub('', commentsElem.text)
            onlyTags = str(tagsElem.text).replace("&quot;", "")

            contentFileName = contentPrefix + str(curId)
            commentFileName = commentsPrefix + str(curId)
            tagsFileName = tagsPrefix + str(curId)

            with open(contentFileName, 'x') as file:
                file.write(postBodyElem.text)
            with open(commentFileName, 'x') as file:
                file.write(onlyComments)
            with open(tagsFileName, 'x') as file:
                file.write(onlyTags)

            print('Content' + contentFileName + '\n')
            print('Comments' + commentFileName + '\n')
            print('Content' + tagsFileName + '\n')
        except Exception as e:
            with open(exceptionFile, 'a') as file:
                file.write(str(e))
                file.write('\n\n')
        time.sleep(2)
