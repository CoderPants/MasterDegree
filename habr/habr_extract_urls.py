# # fetch HTML
# image_url = 'https://habr.com/ru/post/513402/'
# r = requests.get(image_url)
#
# # get main article without comments
# content = extract_content(r.content)
#
# print(content)
#
# # get article and comments
# content_comments = extract_content_and_comments(r.content)

# -----------------------------------------------------------------------------------------------------------------------
# Extract urls from website
import time

from selenium import webdriver

start_time = time.clock()
print("Current time " + str(time.time()))
start = time.time()
amount = 0
max_amount = 10000
with open('/home/misha/MasterDegree/HabrLinksUpdated.txt', 'a') as file:
    with webdriver.Firefox() as driver:
        startingLinks = ["https://habr.com/ru/top/yearly/",
                         "https://habr.com/ru/all/top10/",
                         "https://habr.com/ru/news/"]
        for start in startingLinks:
            nextPage = start
            while nextPage is not None and amount <= max_amount:
                driver.get(nextPage)
                posts = driver.find_elements_by_class_name("post__title_link")
                for post in posts:
                    file.write(post.get_attribute('href') + "\n")
                    amount += 1
                try:
                    nextPage = driver\
                        .find_element_by_id("next_page")\
                        .get_attribute('href')
                except Exception as e:
                    break
                print(nextPage + "\n")
                time.sleep(2)

print("Execution time " + str(time.time() - start))
print("Amount of pages " + str(amount))
