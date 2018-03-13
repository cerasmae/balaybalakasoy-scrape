import sys
import os.path

try:
    from urllib.request import urlopen
    from urllib import parse as urlparse
except ImportError:
    from urllib2 import urlopen, urlparse

from bs4 import BeautifulSoup


'''
Scrapes news links and store it to a file
Stores the news links in news-links.txt
'''
def scrape_blogs():
    f = open('checkpoint.txt', 'r')

    url = f.read().splitlines()[0]
    # url = "http://balaybalakasoy.blogspot.com/2018/03/sphinx-usa-ka-mangtas-nga-tahas-ug-ang.html"
    f.close()

    stop_scraping_process = False
    while not stop_scraping_process:
        page = urlopen(url)
        print(url) 
        soup = BeautifulSoup(page, 'html.parser')
        date = soup.find('h2', {'class': 'date-header'})
        date = date.getText()
        date = date.replace('.', '-')
        
        body = soup.find('div', {'class': 'post hentry uncustomized-post-template'})
        # print(body.getText().strip().splitlines())

        lines = body.getText().strip().splitlines()
        
        content = lines.pop(0).strip() + '\n\n'

        for line in lines:
            curr_line = line.strip()
            if curr_line:
                if curr_line[0] == '-' and curr_line[1] == '-':
                    break
                else:
                    content = content + curr_line + '\n'
                    

        # print lines
        # print content        

        title = soup.find('h3', {'class': 'post-title entry-title'})
        title = title.getText()
        title = title.strip().rstrip('\n')

        # text = ''
        # contents = soup.findAll('span', {'style': 'color: #b6d7a8;', 'style': 'color: #b6d7a8; font-family: "georgia";', 'style': 'color: #b6d7a8; font-family: "georgia"; font-size: 12pt;', 'style': 'color: #b6d7a8; font-family: "georgia"; font-size: 12.0pt;'})
        # # print contents
        # for content in contents:
        #     content = content.getText().strip().rstrip()
        #     if content:
        #         text += content + '\n'

        author = soup.find('span', {'style': 'color: #9fc5e8;', 'style': 'color: #9fc5e8; font-family: "georgia";'})
        
        if not author:
            divs = soup.findAll('div', {'style': 'font-family: Georgia;'})
            child = divs[-1].findChildren()[0]

            if "," in child:
                if "." not in child:
                    child = divs[-2].findChildren()[0]

            author = child

        author = author.getText()
        author = author.replace('--', '')
        author = author.strip().rstrip()
        

        # for title in titles:
        #     child = title.findChildren()[0]
        #     write_file("files/news-links.txt", contents=[main_url + child.get('href')], mode="a")
        #     print(main_url + child.get('href'))
        #     print("\n")
        #     i += 1-
        #     if i == limit:
        #         break

        # # next_page = soup.find('a', {'title': 'Go to next page'})
        # # if next_page:
        # #     url = main_url + next_page.get('href')
        # # else:

        lit = title + '\n'
        lit = lit + date + '\n'
        lit = lit + author + '\n\n'
        lit = lit + content + '\n'

        # print "--------"
        # print lit
        # print "--------"

        if os.path.exists('data/'+ title+'.txt'):
            f = open('data/' + title + '_o.txt', 'w')
        else:
            f = open('data/' + title + '.txt', 'w')

        f.write(lit.encode('utf-8') + '\n')
        f.close()

        older_link = soup.find('a', {'class': 'blog-pager-older-link'})
        if older_link:
            older_link = older_link['href']
            url = older_link
            f = open('checkpoint.txt', 'w')
            f.write(url + '\n')
            f.close()
            stop_scraping_process = False
        else:
            stop_scraping_process = True
        # stop_scraping_process = True

'''
Scrapes news contents from links stored in news-links.txt
Stores the news contents in news-raw.txt
'''
# def scrape_news_contents():
#     checkpoint = read_file("files/news-links-cp.txt")
#     start = int(checkpoint[0])
#     if start == 501:
#         print("Status: Finished!")
#         return

#     urls = read_file("files/news-links.txt", start=start)
#     contents = []
#     for idx, url in enumerate(urls):
#         start += 1
#         print("Link [" + str(start) + "]: "  + url)
#         page = urlopen(url)
#         soup = BeautifulSoup(page, 'html.parser')
#         div = soup.find('div', {'class': 'field-item even', 'property': 'content:encoded'})
#         for child in div.findChildren():
#             contents.append(child.getText())
#         write_file("news-raw.txt", contents=contents, per_line=True, mode="a")
#         contents = []
#         endpoints = [
#             str(start + 1)
#         ]

#         write_file("files/news-links-cp.txt", contents=endpoints, mode="w")


scrape_blogs()
