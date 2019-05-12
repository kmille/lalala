#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from ipdb import set_trace

session = requests.Session()
cookies = {'ziparchiv': "", 'counter': ""}
session.cookies.update(cookies)
session.headers.update({'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"})

username = "foo@byom.de"
password = "foofoo"
url = "http://usdb.animux.de"


def login():
    print("Trying to login")
    data = {'user': username, 'pass': password, 'login': 'login'}
    params = "/?&link=home"
    resp = session.post("http://usdb.animux.de/?&link=home", params=params, data=data)
    if "Login or Password invalid" in resp.text:
        print("Login failed")
    else:
        print("We are in.")


def get_details(id):
    print(f"Get details for {id}")
    params = "index.php"
    params = f"link=detail&id={id}"
    resp = session.get(url, params=params)
    bs = BeautifulSoup(resp.text, 'html.parser')
    comments = comments = bs.findAll("table")[4]
    for object in comments.findAll("object"):
        youtube_url = object.find("embed").attrs['src']
        print(youtube_url)
    #set_trace()
#    comments = [x.text for x in comments.findAll("td")]
#    for comment in comments:
#        if "youtube" in comment:
#            print(comment)

    header = bs.find("tr", {'class': 'list_head'}).findAll("td")
    interpret = header[0].text
    song_name = header[1].text
    print(interpret)
    print(song_name)

    

def get_source(id):
    print(f"Get source of song {id}")
    params = f"link=gettxt&id={id}"
    data = {'wd': '1'}
    resp = session.post(url, data=data, params=params)
    bs = BeautifulSoup(resp.text, 'html.parser')
    src = bs.find("textarea").text
    print(src[:500])
    return src


if __name__ == '__main__':
    login()
    get_details("5741")
    get_source("5741")


