import os
from os.path import basename
import requests
from bs4 import BeautifulSoup

def findLyrics(Artist:str, Song:str)->str:
   # Send an HTTP request to the website
   Song2 = Song.replace("  ", "-").replace(" ","-")
   Artist2 = Artist.replace("  ", "-").replace(" ","-")
   url = 'https://genius.com/' + Artist2 +'-'+ Song2 + '-lyrics'
   try:
      response = requests.get(url)
   except:
      os.environ['http_proxy'] = 'http://10.0.0.1:3128'
      os.environ['https_proxy'] = 'http://10.0.0.1:3128'
      response = requests.get(url)

   # Parse the HTML of the webpage
   soup = BeautifulSoup(response.content, 'html.parser')

   # Find the element that contains the lyrics and the album cover
   lyrics_element = soup.find(class_="Lyrics__Container-sc-1ynbvzw-5 Dzxov")
   img = soup.find(class_="SizedImage__NoScript-sc-1hyeaua-2 UJCmI")

   #Download the album cover
   link  = img.get("src")
   with open("ExportedLyrics/"+Song+".jpg", "wb") as f:
            f.write(requests.get(link).content)

   # Extract the text of the lyrics if the song is found on Genius
   if lyrics_element is None:
      print("We're unable to find this song, please retry and make sure there's no name mistake")
   else:
      #add title
      lyrics = Song + "\n\n" + lyrics_element.text
      #make layout for the doc
      return layout(lyrics)

def layout(string):
   new_string = ""
   for i in range(len(string)):
         if string[i].isupper() or string[i] == "[" and i > 0 :
            if string[i-1].islower():
               new_string += "\n"
            if string[i] == "[":
               new_string += "\n"
         new_string += string[i]
         if string[i] == "]" and string[i+1] != "[":
            new_string += "\n\n"   
   return new_string

Lyrics = findLyrics("Eminem","rap God")

"""
Artist = ""
Song = ""

while Artist == "":
   Artist = input("Artist : ")
while Song == "":
   Song = input("Song : ")

Lyrics = findLyrics(Artist,Song)
"""

if Lyrics is not None:
   f = open("ExportedLyrics/"+"rapGod"+".txt",'w')
   f.write(Lyrics)
