import re
import time
import mechanize
from auth import *

def buildlist(path):
    build = []
    with open(path) as infile:
        for line in infile:
            build.append(line.strip())
    return build

login_url = 'http://secure.ancestry.com/security/passwordlogin.aspx?'

state = "Massachusetts"
county = "Suffolk"
town = "Boston"
enum_districts = range(787)[576:]
relhead = "self"
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

census_search_url = 'http://content.ancestry.com/iexec/?htx=List&dbid=6742&enc=1&offerid=0%3a7858%3a0'

br.open(census_search_url)

searchform_id = "s0searchbox"
fname_id = "s0gsfn"
lname_id = "s0gsln"
state_id = "s0f5"
county_id = "s0f4"
town_id = "s0f7"
relhead_id = "s0f42"
enumdist_id = "s0f22"
occ_id = "s0f43"
