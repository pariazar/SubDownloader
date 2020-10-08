'''Developed by Hamed Pariazar 2020
https://github.com/hamedpa
email : hamedpa21@gmail.com'''

import imdb 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests,re
from difflib import SequenceMatcher
import os
from tqdm import tqdm
from urllib.request import Request, urlopen
import time
import json

#find name of movie from string 
def getNameMovie(name):
    ia = imdb.IMDb() 
    search = ia.search_movie(name)   
    if(not search==[]):
        return(search[0]['title'])
    else:
        return(0)

#add + between words in string
def addPlus(string):
    if(len(string)>1):
        tmp=''
        sx = string.split(" ")
        for x in sx:
            tmp+=x
            tmp+="+"     
        return tmp[0:len(tmp)-1]
    else:
        return string

#add - between words in string
def addDash(string):
    if(len(string)>1):
        tmp=''
        sx = string.split(" ")
        for x in sx:
            tmp+=x
            tmp+="-"     
        return tmp[0:len(tmp)-1]
    else:
        return string

#check name exist in word or not
def checkExistedInString(link,name):
    wordSplit = name.split()
    checksum = len(wordSplit)
    for x in wordSplit:
        if(x in link):
            checksum -= 1
    if(checksum==0):
        return True
    else:
        return False


#this funciton is correcting name of movie if necessary 
def correctInput(nameOfMovie):
    try:
        inp = getNameMovie(nameOfMovie[0:15])
        if(inp==0):
            inp = getNameMovie(nameOfMovie[0:10])
    except:
        print('err')
    #output
    return inp

#get number from this function and make sure that how much two string are similar to each other
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#remove extra words from string
def removeExtraString(mainString,word):
    index = mainString.find ( word )
    return mainString[0:index]

#make directory
def createDirectory(pathVideo,nameDirectory):
    # define the name of the directory to be created
    path = pathVideo+"\\"+nameDirectory

    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)

#download subtitles with this function
def downloadSub(link,nameFile):
    url = link
    response = requests.get(url, stream=True)

    with open(nameFile, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

#extract subtitles links from servers and websites
def getSubLink(nameMovie,searchLink,keyword,afterLink):
    parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
    mkvlist = []
    
    if(not "0" in afterLink):
        site= searchLink+addPlus(nameMovie)+afterLink
    else:
        site= searchLink+addPlus(nameMovie)

    #print(site)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    x = nameMovie
    x = x.split(" ")
    redkeyword1 = x[0].lower()
    if(redkeyword1 in "the"):
        redkeyword1 = x[1].lower()
    
        
    soup = BeautifulSoup(page, parser, from_encoding=page.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        #time.sleep(1)
        
        li = link['href'][(len(link['href'])-len(nameMovie))-10:]
    
        if((similar(nameMovie,li[(len(li)-len(nameMovie))-10:])*100)>40):
            if (keyword in link['href'] ):
                        try:
                            site = link['href']
                            req = Request(site,headers=hdr)
                            page = urlopen(req)
                            soup2 = BeautifulSoup(page, parser, from_encoding=page.info().get_param('charset'))
                            for link2 in soup2.find_all('a', href=True):
                                if("zip" in link2['href'] or "rar" in link2['href']):
                                    mkvlist.append(link2['href'])
                                    #print(link2['href'])
                        except:
                                print('error')
        else:
            if(len(x)>3):
                if(checkExistedInString(link['href'],nameMovie)):
                    if (keyword in link['href']):
                        try:
                            site = link['href']
                            req = Request(site,headers=hdr)
                            page = urlopen(req)
                            soup2 = BeautifulSoup(page, parser, from_encoding=page.info().get_param('charset'))
                            for link2 in soup2.find_all('a', href=True):
                                if("zip" in link2['href'] or "rar" in link2['href'] and redkeyword1 in link['href']):
                                    mkvlist.append(link2['href'])
                                    #print(link2['href'])
                        except:
                            print('error')
            else:
                if(redkeyword1 in link['href']):
                    if (keyword in link['href']):
                        try:
                            site = link['href']
                            req = Request(site,headers=hdr)
                            page = urlopen(req)
                            soup2 = BeautifulSoup(page, parser, from_encoding=page.info().get_param('charset'))
                            for link2 in soup2.find_all('a', href=True):
                                if("zip" in link2['href'] or "rar" in link2['href'] and redkeyword1 in link['href']):
                                    mkvlist.append(link2['href'])
                                    #print(link2['href'])
                        except:
                            print('error')
        
    return mkvlist


def main():
    currentLink = []  
    afterlink = []    
    keyword = []       

    print("Welecome to subDownloader 2020 - Download all subtitles without any trouble ")
    print("Please enter address of movies: ")
    path = input() #"M:\\myfilm"
    newpath = "movie\\"
    with open('websites.json') as json_file:
                data = json.load(json_file)
                for p in data['websites']:
                    currentLink.append(p['link']) 
                    afterlink.append(p['afterlink'])
                    keyword.append(p['keyword'])


    for root, dirs, files in os.walk(path):
        for filename in files:
            #print(os.path.join(root, filename))
            if(".mkv" in filename and (newpath not in (os.path.join(root, filename)))):  
                correctName = correctInput(filename)
                createDirectory(path,newpath+filename)

                # Move a file by renaming it's path
                os.rename(os.path.join(root, filename),path+"\\"+newpath+filename+"\\"+filename)          
                for c in range(len(currentLink)):
                    
                    print("Download subtitle of "+correctName+" from server "+str((c+1))+" ...")
                    if(not getSubLink(correctName,currentLink[c],keyword[c],str(afterlink[c])) ==[]):
                        result1 = getSubLink(correctName,currentLink[c],keyword[c],str(afterlink[c]))[0]
                        if("p" in result1[len(result1):]):
                            downloadSub(result1,path+"\\"+newpath+filename+'\\'+filename+" "+str(c)+".zip")
                        else:
                            downloadSub(result1,path+"\\"+newpath+filename+'\\'+filename+" "+str(c)+".rar")
                        print("Subtitle of "+correctName+" Downloaded successfully")
                
                    print()
                        
                else:
                    print()
        

if __name__ == "__main__":
    main()