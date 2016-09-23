# coding=utf-8
# filmscreencaps.com page by page from a gallery

import re
import os
from robobrowser import RoboBrowser


def ripPage(browser, starturl):
    links = browser.find_all(href=re.compile('Image.php'))
    for link in links:
        browser.open('http://filmscreencaps.com/' + link['href'])
        imgurl = browser.find('img', id='imageTag')['src']
        request = browser.session.get(
            imgurl.strip(),
        )
        imgfilename = imgurl.split('/')[-1]
        if not os.path.exists(imgfilename):
            with open(imgfilename, 'wb') as imgfile:
                imgfile.write(request.content)
            print "saved {0}".format(repr(imgurl))
        else:
            print "already had {0}".format(repr(imgurl))
    browser.open(starturl)


def getPages(browser, starturl):
    ripPage(browser, starturl)
    page = browser.find('a', string=u'»')
    print page
    if page is not None:
        nexturl = 'http://filmscreencaps.com/' + page['href']
        browser.open(nexturl)
        getPages(browser, nexturl)

fscp = RoboBrowser(
    user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,'
               ' like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    parser='html.parser'
)

# gallery = raw_input('enter album number >> ')
gallery = 'name=The_Matrix&movieid=126'
surl = 'http://filmscreencaps.com/MovieImages.php?{0}'.format(
    gallery)
fscp.open(surl)

title = 'the matrix'

if not os.path.exists(title):
    os.mkdir(title)
os.chdir(title)

getPages(fscp, surl)