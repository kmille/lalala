#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from ipdb import set_trace
import re

from flask import Flask, request, render_template

session = requests.Session()
cookies = {'ziparchiv': "", 'counter': ""}
session.cookies.update(cookies)
session.headers.update({'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"})

#username = "foo2@byom.de"
from credentials import username, password
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
    with open("data/{}.foo".format(id), "w") as f:
        f.write(src)
    print("Write data to data/{}.foo".format(id))
    #print(src[:500])
    return src


def search_songs(artist, title):
    print(f"Searching for {artist} {title}")
    data = {"interpret": artist,
            "title": title,
            "edition": "",
            "language": "",
            "order": "views",
            "ud": "desc",
            "limit": "300"
            }
    resp = session.post(url + "/index.php?link=list", data=data)
    print(resp.url)
    print(resp.request.headers)
    print(resp.request.body)
    assert "You are not logged in. Login to use this funct" not in resp.text, "login failed"
    songs = parse_search_response(resp.text)
    return songs


def parse_search_response(html):
    bs = BeautifulSoup(html, 'html.parser')
    songs_part_one = bs.find_all("tr", {"class": "list_tr1"})
    songs_part_two = bs.find_all("tr", {"class": "list_tr2"})
    songs_part_one.extend(songs_part_two)
    songs = []
    for html_song in songs_part_one:
        columns = html_song.findAll("td")
        for colum in columns:
            song = {}
            song['id'] = re.search('\d+', columns[0].get('onclick')).group()
            song['artist'] = columns[0].text
            song['title'] = columns[1].text
            song['views'] = columns[6].text
        songs.append(song)
    songs = sorted(songs, key=lambda x: int(x['views']), reverse=True)
    return songs


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search", methods=["POST"])
def search():
    artist = request.form.get("artist", "")
    title = request.form.get("title", "")
    songs = search_songs(artist, title)
    return render_template('songs.html', songs=songs)



if __name__ == '__main__':
    login()
    app.run(debug=True)
    search_songs("Coldplay", "")
    #parse_search_response()
    
    
    #get_details("5741")
    #get_source("5741")


