#!/usr/bin/python
import time
import urllib
import urllib
import urllib2
import cookielib
from html5lib import HTMLParser, treebuilders

import getpass
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
 
gmail_user = "you@should.login"
gmail_pwd = "wrong password"
 
def login(user):
   global gmail_user, gmail_pwd
   gmail_user = user
   gmail_pwd = getpass.getpass('Password for %s: ' % gmail_user)
 
def mail(to, subject, text, attach=None):
   msg = MIMEMultipart()
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
   msg.attach(MIMEText(text))
   if attach:
      part = MIMEBase('application', 'octet-stream')
      part.set_payload(open(attach, 'rb').read())
      Encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
      msg.attach(part)
   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   mailServer.close()
 
# Example!
def example(available):
   email = raw_input("Your Gmail address: ")
   login(email)
   mail(email, "Course opening Available", str(available)+" spots available")


def get_spaces_available(dept_abbr, course_num):
    # define
    post_data = {
            'classyear' : '2008', # why??
            'subj': dept_abbr,
            'crsenum': course_num,
            }
    url = 'http://oracle-www.dartmouth.edu/dart/groucho/timetable.course_quicksearch'

    # scrape the html
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    headers =  {'User-agent' : 'Mozilla/c.0 (compatible; MSIE 5.5; Windows NT)'}
    request = urllib2.Request(url, urllib.urlencode(post_data), headers)
    handle = urllib2.urlopen(request)
    html = handle.read()

    # parse for the dept and course number
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    soup = parser.parse(html)
    tbody = soup.find('th', text='Term').parent.parent.parent
    cells = tbody.findAll('tr')[2]('td')
    enrolled = int(cells[-2].contents[0])
    capacity = int(cells[-3].contents[0])
    available = capacity - enrolled
    print "%i spaces left (capacity of %i with %i enrolled)" % (available, capacity, enrolled)

    return available


# test with elementary oceanography
available = get_spaces_available('EARS', 003)

# test with email
#example(available)  

while available == 0:
    # check again for space
    time.sleep(30)
    available = get_spaces_available('EARS', 003)
else:
    # respond and email me if course update
    example(available)

 
