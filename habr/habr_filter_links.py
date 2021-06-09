# Filter and save to the new file
path = '/home/misha/MasterDegree/Habr-Habr/UpdatedPosts/'
fileWithLinks = 'HabrLinksUpdated.txt'
fileWithFilteredLinks = 'HabrLinks_Filtered.txt'
with open(path + fileWithLinks, 'r') as file:
    links = [line.rstrip('\n') for line in file]
    distinctLinks = list(set(links))
    filteredLinks = list(filter(lambda link: len(link) > 0 and str(link).startswith("http"), distinctLinks))

with open(path + fileWithFilteredLinks, 'w') as file:
    for link in filteredLinks:
        file.write(link + "\n")
