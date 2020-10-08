# SubDownloader
Download all subtitles without any trouble ,

input : address of movies directory ,

output : movies with subtitles 

<h3>features</h3>
    Download subtitles without search name of all movies in the internet
    
   it will automatically download subtitle of all movies and easy to use
 
 <h2>Download project</h2>
download program with below commad

    git clone https://github.com/hamedpa/SubDownloader
    
<h2>Requirements</h2>
install requirements with below commad

    pip install -r requirements.txt
    
<h2>Usage</h2>
1 - in the subDownloader directory run program 

    python getSub.py
    
2 - enter address of movies directory
for example if your movies in myfilm (directory/folder)

    M:\myfilm
    
that's it program try to download subtitle of all movies that exist in choosen directory 

<h2>Advance usage</h2>
you can add subtitle website address in json file and the program use data from it for downloading process

if after search word has some parameters then add them into afterlink else add 0

keyword is unique string for every item or movie in subtitle websites

    {"websites": [{"link": "https://subtitlewebsite.com/?s=", "afterlink": "0", "keyword": ".html"}]}

if you have any questions about this program you can contact in telegram : @pariazar21
thanks for using my program


 
