# Extract tags from website
import time

from selenium import webdriver

path = '/home/misha/MasterDegree/Habr-Habr/UpdatedPosts/'
fileWithFilteredLinks = 'HabrLinks_Filtered_Extracted.txt'
with open(path + fileWithFilteredLinks, 'r') as file:
    links = [line.rstrip('\n') for line in file]

linksForPosts = [list(filter(lambda elem: len(elem) > 0, link.split('/')))[-1] for link in links]
print(str(len(linksForPosts)))
print(str(len(set(linksForPosts))))
index = 0
tagsPrefix = path + 'Tags/Habr_Post_Tags_Number_'
with webdriver.Firefox() as driver:
    for link in links:
        try:
            # <div class="post__text post__text_v2" id="post-content-body">
            # postBody = driver.find_element_by_class_name('post__body post__body_full')
            driver.get(link)
            # postBodyElem = driver.find_element_by_id("post-content-body")
            # commentsElem = driver.find_element_by_id("comments")
            tags = driver.find_element_by_class_name("post__tags-list")
            tagsFileName = tagsPrefix + str(index)
            tagsText = str(tags.text).replace("&quot;", "")
            with open(tagsFileName, 'x') as file:
                file.write(tagsText)
            #post__tags-list
#             'МКС
# утечка воздуха
# модуль &quot;Звезда&quot;
# космос
# трещина на МКС'
            index += 1
            print('Content' + tagsFileName + '\n')
        except Exception as e:
            print("Exception " + str(e))
        time.sleep(2)
