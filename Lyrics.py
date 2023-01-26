import os
import requests
from bs4 import BeautifulSoup

os.environ['http_proxy'] = 'http://10.0.0.1:3128'
os.environ['https_proxy'] = 'http://10.0.0.1:3128'


def findLyrics(Artist:str, Song:str)->str:
   # Send an HTTP request to the website
   Song2 = Song.replace("  ", "-").replace(" ","-")
   Artist2 = Artist.replace("  ", "-").replace(" ","-")
   url = 'https://genius.com/' + Artist2 +"-"+ Song2 + "-lyrics"
   response = requests.get(url)

   # Parse the HTML of the webpage
   soup = BeautifulSoup(response.text, 'html.parser')

   # Find the element that contains the lyrics
   lyrics_element = soup.find(class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")
   
   # Extract the text of the lyrics
   if lyrics_element is None:
      print("We're unable to find this song, please retry and make sure there's no name mistakes")
   else:
      lyrics = Song + "\n" + lyrics_element.text
      return add_spaces(lyrics)

def add_spaces(string):
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

Artist = input("Artist : ")
Song = input("Song : ")

Lyrics = findLyrics(Artist,Song)

f = open("ExportedLyrics/"+Song+".txt",'w')

f.write(Lyrics)