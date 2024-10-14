import os
from os.path import basename
import requests
from bs4 import BeautifulSoup
import re as regex
import fpdf

def reachGeniusPage(Artist:str, Song:str):
   #Make the url
   url = validUrl(Artist,Song)
   #try resquet with or without specific proxy 
   try:
      response = requests.get(url)
   except:
      os.environ['http_proxy'] = 'http://10.0.0.1:3128'
      os.environ['https_proxy'] = 'http://10.0.0.1:3128'
      #add Proxy here
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
      
   else:
      #add title
      lyrics = Song + "\n\n" + lyrics_element.text

      #make layout for the text
      lyrics = layout(lyrics)

      #create the document
      f = open("ExportedLyrics/"+Song.replace(' ','_')+".txt",'w', encoding="utf-8")
      f.write(lyrics)

      print("Lyrics found")


def findImage(Content:str,Song:str)->str:
   #Find the element that contain the album cover
   img = Content.find(class_="SizedImage__NoScript-sc-1hyeaua-2 UJCmI")

   #Download the album cover
   if img is not None:
      link  = img.get("src")
      with open("ExportedLyrics/"+Song.replace(' ','_')+".jpg", "wb") as f:
               f.write(requests.get(link).content)

      print("Album cover found")

def layout(string):
   if (len(string) == 0):
      raise("Error : lyrics are empty")
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
      if string[i] == "]" and i+1 < len(string): 
         if string[i+1] != "[":
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


def makePDF(content):
   pdf = fpdf.FPDF()
   pdf.addPage()

   # set style and size of font 
   # that you want in the pdf
   pdf.set_font("Arial", size = 15)
 
   # create a cell
   pdf.cell(200, 10, txt = content, 
         ln = 1, align = 'C')
   

Artist = ""
Song = ""
retry = True

while(retry):
   Artist = input("Artist : ")
   Song = input("Song : ")
   print("")
   reachGeniusPage(Artist,Song)
   print("Done !\n")
   
   retry = input("search another song ? (y/n)\n") == 'y'



