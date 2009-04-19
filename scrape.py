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

def buildlist(path):
    build = []
    with open(path) as infile:
        for line in infile:
            build.append(line.strip())
    return build

login_url = "http://secure.ancestry.com/security/passwordlogin.aspx?"

#enum_districts = range(787)[576:]
enum_districts = range(787)[784:]
occs = buildlist("occupations.txt")

br = mechanize.Browser()
br.open(login_url)
login_form = br.forms().next()

login_form.set_value(usr, name="userNameTB")
login_form.set_value(pwd, name="passwordTB")

br.select_form("LoginForm")
response = br.submit()
search_url = response.read().split('\n')[0].split("\"")[1]
br.open(search_url)

census_search_url = "http://search.ancestry.com/cgi-bin/sse.dll?rank=1&gsfn=&gsln=&=&f5=MA&f4=Suffolk&f7=Boston&f42=Self&f8=&f15=&f27=&f21=&rg_81004011__date=&rs_81004011__date=0&_8000C002=&f28=&_80008002=&f16=&_80018002=&f6=&f11=&f10=&f22=%s&f43=%s&gskw=&prox=1&db=1880usfedcen&ti=0&ti.si=0&gl=&gss=IMAGE&gst=&so=3"

occupation = "carpenter"
#outfile = open("output", 'w')
pattern = r'Matches <strong>.*<\/strong> of <strong>(\d|,)+<\/strong>'
district = 777

#for district in enum_districts:
to_open = census_search_url % (district, occupation)
br.open(to_open)
#    response = br.response().read()
#    num_hits = 0
#    if not re.search("Your Search returned no matches", response):
#        num_hits = re.findall(pattern, response)[0].replace(",","")
#    outfile.write("%s,%s,%s" % (district, occupation, num_hits))
#    print response
#    sys.exit()
#    time.sleep(5)

#outfile.close()
