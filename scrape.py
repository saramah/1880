from __future__ import with_statement
"""
KEYS:
    gsfn: firstname
    gsln: lastname
    f5: state
    f4: county
    f7: township
    f42: relationship to head
    f8: marital status
    f15: race
    f27: gender
    f21: birthplace
    rg_81004011__date: estimated birth year
    rs_81004011__date: +/- for birth year
    _8000C002: father's firstname
    f28: father's birthplace
    _80008002: mother's firstname
    f16: mother's birthplace
    _80018002: spouse name
    f6: page number
    f11: microfilm roll
    f10: family history film
    f22: enumeration district
    f43: occupation
    gskw: keywords
"""
import re
import sys
import time
import mechanize
from auth import *

LOGIN_URL = "http://nrs.harvard.edu/urn-3:hul.eresource:ancestry"
DISABLE_NEW_URL = "http://search.ancestry.com/search/default.aspx?new=0"
LOGOUT_URL = "http://www.ancestry.com/security/loginredir.aspx?logout=true&home=true"
SEARCH_URL = "http://search.ancestry.com/cgi-bin/sse.dll?rank=1&gsfn=&gsln=&=&f5=MA&f4=Suffolk&f7=Boston&f42=Self&f8=&f15=&f27=&f21=&rg_81004011__date=&rs_81004011__date=0&_8000C002=&f28=&_80008002=&f16=&_80018002=&f6=&f11=&f10=&f22=%s&f43=%s&gskw=&prox=1&db=1880usfedcen&ti=0&ti.si=0&gl=&gss=IMAGE&gst=&so=3"

def buildlist(path):
    build = []
    with open(path) as infile:
        for line in infile:
            build.append(line.strip())
    return build

enum_districts = range(586, 787)
print "Reading occupations..."
occs = buildlist("occupations.txt")

print "Logging in..."
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(LOGIN_URL)
login_form = br.forms().next()
login_form.set_value(usr, name="__authen_id")
login_form.set_value(pwd, name="__authen_password")
br.select_form("LoginForm")
print "Confirming login..."
response = br.submit()
search_url = response.read().split('\n')[0].split("\"")[1]
br.open(search_url)

# Disable new search mode
print "Disabling new search mode..."
br.open(DISABLE_NEW_URL)

print "Beginning search queries..."
pattern = r'Viewing <b>.+?</b> of <b>((?:\d|,)+)</b>'
outfile = open("output.txt", 'w')
for district in enum_districts:
    for occupation in occs:
        br.open(SEARCH_URL % (district, occupation))
        response = br.response().read()
        num_hits = 0
        if not "Your Search returned no matches" in response:
            find_result = re.findall(pattern, response)
            if find_result:
                num_hits = find_result[0]
        outfile.write("%s,%s,%s\n" % (district, occupation, num_hits))
        print "District [%s]\t\toccupation [%s]\t\thits [%s]" % (district, occupation, num_hits)
        time.sleep(5)

print "Logging out..."
br.open(LOGOUT_URL)
