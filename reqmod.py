import requests
import bs4
'''
res = requests.get('http://inventwithpython.com/page_that_does_not_exist')


try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
'''
'''
res = requests.get('http://www.gutenberg.org/cache/epub/1112/pg1112.txt')
res.raise_for_status()'''

'''
with open('RomeoAndJuliet.txt','wb') as playFile:
    for chunk in res.iter_content(100000):
        playFile.write(chunk)'''

with open('example.html') as exampleFile:
    exampleSoup = bs4.BeautifulSoup(exampleFile.read())
    elems = exampleSoup.select('#author')
    type(elems)
