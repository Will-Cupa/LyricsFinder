import os
from os.path import basename
import requests
from bs4 import BeautifulSoup
import re as regex

def reachGeniusPage(Artist:str, Song:str):
   #Make the url
   url = validUrl(Artist,Song)

   #try resquet with or without specific proxy 
   try:
      response = requests.get(url)
   except:
      os.environ['http_proxy'] = 'http://10.0.0.1:3128'
      os.environ['https_proxy'] = 'http://10.0.0.1:3128'
      response = requests.get(url)

   # Parse the HTML of the webpage
   soup = BeautifulSoup(response.content, 'html.parser')

   #find the lyrics in the webpage
   findLyrics(soup,Song)
   findImage(soup,Song)


def findLyrics(Content:str,Song:str)->str:

   # Find the element that contains the lyrics
   # We use regular expression because the class name change over time
   lyrics_element = Content.find(class_= regex.compile("Lyrics__Container*"))

   # Extract the text of the lyrics if the song is found on Genius
   if lyrics_element is None:
      print("\nWe're unable to find this song, please retry and make sure there's no name mistake\n")

      #Restart the function
      Artist = ""
      Song = ""
      while Artist == "":
         Artist = input("Artist : ")
      while Song == "":
         Song = input("Song : ")

      reachGeniusPage(Artist,Song)
   else:
      #add title
      lyrics = Song + "\n\n" + lyrics_element.text

      #make layout for the text
      lyrics = layout(lyrics)

      #create the document
      f = open("ExportedLyrics/"+Song.replace(' ','_')+".txt",'w')
      f.write(lyrics)


def findImage(Content:str,Song:str)->str:
   #Find the element that contain the album cover
   img = Content.find(class_="SizedImage__NoScript-sc-1hyeaua-2 UJCmI")

   #Download the album cover
   if img is not None:
      link  = img.get("src")
      with open("ExportedLyrics/"+Song.replace(' ','_')+".jpg", "wb") as f:
               f.write(requests.get(link).content)

def layout(string):
   #Make a readable layout from the genius content
   new_string = ""
   first_quote = False
   chrIgnore=[" ", "[", "("]
   for i in range(len(string)):
      if string[i] == '"':
         if first_quote:
            first_quote = False
         else:
            first_quote = True
      elif string[i].isupper() or string[i] == "[" and i > 0:
         if not string[i-1].isupper() and not string[i-1] in chrIgnore:
            if string[i] == "[":
               new_string += "\n" 
            if string[i-1] == '"':
               if not first_quote:
                  new_string += "\n"
            else:
               new_string += "\n"
               
      new_string += string[i]
      if string[i] == "]" and string[i+1] != "[":
         new_string += "\n"   
   return new_string

def validUrl(Artist, Song):
   rm = ["  "," "]
   for elem in rm:

      #remove writing mistakes
      if Song[-1:] == elem:
         Song = Song[:-1]
      if Artist[-1:]  == elem:
         Artist = Artist[:-1]

      #replace space by "-" in order to make a valid url
      Song = Song.replace(elem, "-")
      Artist = Artist.replace(elem, "-")

      #return the final url
   return 'https://genius.com/' + Artist +'-'+ Song + '-lyrics'


Artist = ""
Song = ""

while Artist == "":
   Artist = input("Artist : ")
while Song == "":
   Song = input("Song : ")

reachGeniusPage(Artist,Song)

