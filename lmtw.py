import re
import os
from robobrowser import RoboBrowser

lmtw = RoboBrowser(
    user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,'
               ' like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    parser='html.parser'
)

# gallery = raw_input('enter album number >> ')
gallery = '62'
surl = 'http://www.leavemethewhite.com/caps/thumbnails.php?album={0}'.format(
    gallery)
lmtw.open(surl)

title = lmtw.select('td.statlink > h2')[0].string

if not os.path.exists(title):
    os.mkdir(title)
os.chdir(title)

links = lmtw.find_all(href=re.compile('displayimage.php'))
for link in links:
    lmtw.open('http://www.leavemethewhite.com/caps/' + link['href'])
    imgurl = lmtw.find('td', style='{SLIDESHOW_STYLE}').img['src']
    request = lmtw.session.get(
        'http://www.leavemethewhite.com/caps/' + imgurl,
        stream=True
    )
    with open(imgurl.split('/')[-1], 'wb') as imgfile:
        imgfile.write(request.content)
    print "saved {0}".format(imgurl)
