import bs4


with open('example.html') as exampleFile:
    soup = bs4.BeautifulSoup(exampleFile.read(), "html.parser")
    elem = soup.select('span')[0]
    print(str(elem))
    print(elem.get('id'))
    print(elem.get('some_nonexistent_addr') == None )

    print(elem.attrs)

