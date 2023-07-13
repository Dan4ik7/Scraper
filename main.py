from DBconnect import commit, close
from ninesraper import scrape_pages, scrape_page

scrape_pages()
scrape_page()
commit()
close()