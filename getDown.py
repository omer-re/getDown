# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
import sys, os
from tkinter import ttk
from functools import partial
import fnmatch
import winsound
import unicodedata
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from requests.exceptions import MissingSchema

tqdm_colors= ['RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN']
TQDM_COLORS_OPTIONS=len(tqdm_colors)
progress_indicator=["Working","Working.","Working..","Working...",]

def test_link_content(url):
     r = requests.get(url)
     content_type = r.headers.get('content-type')

     if 'application/pdf' in content_type:
         ext = '.pdf'
         return True
     elif 'text/html' in content_type:
         ext = '.html'
     else:
         ext = ''
         print('Unknown type: {}'.format(content_type))

def get_all_links(soup):
    href_list=[]
    for a in soup.find_all('a', href=True):
        print(a['href'])
        try:
            if len(a['href'])<5: continue
            if test_link_content(a['href']):
                href_list.append(a['href'])
        except MissingSchema:
            continue
    return href_list

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if basename.endswith("html") or basename.endswith("htm"):
                filename = os.path.join(root, basename)
                print(filename)
                yield filename

def find_between( s, first, last ):
    try:
        start = s.index( first ) #+ len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""


def scrape_files(file):
    if (file==None):
        eprint("Invalid input")
    else:
        dirname,src_filename= os.path.split(file)
        # create a folder for each html list of files
        folder_location=os.path.join(dirname, src_filename.rsplit('.', 1)[0])
        #If there is no such folder, the script will create one automatically
        if not os.path.exists(folder_location.rsplit('.', 1)[0]):os.mkdir(folder_location.rsplit('.', 1)[0])
        print("DEST DIRECTORY: ", folder_location.rsplit('.', 1)[0], " PATH EXISTS: ",os.path.exists(folder_location.rsplit('.', 1)[0]))

        with open(file, 'r', encoding='utf-8', errors='ignore') as page:
            soup = BeautifulSoup(page.read(), 'html.parser')

        soup_list = get_all_links(soup)

        # for links manually scraped
        for link in soup_list:
            Label(root, textvariable=foldername,width=20).grid(row=4, column=1, sticky=(N,S,E,W))
            try:
                # print(link['href'])
                new_link=(find_between(str(link),'http','" '))
                filename = os.path.join(folder_location,new_link.split("/")[-1])
                print("path ", filename)
            except:
                print("problematic name:", link, "   ", link['href'])
                filename = os.path.join(folder_location,link['href'][-1])

            print("pdf filename   ", link.split("/")[-1])
            filename2= os.path.join((folder_location.rsplit('.', 1)[0]), link.split("/")[-1])

            with open(filename2, 'wb') as f:
                f.write(requests.get(urljoin(str(file),str(link))).content)



def get_html_files():
    for htmlfile in find_files(filename1.get(), '*.html'):
        tree_walk_list.append(htmlfile)

    print("HTML FILES TO SCAN: ",tree_walk_list)

    # get filename of each
    for htmlfile in tree_walk_list:
        print("Working on: ", htmlfile)
        try:
            scrape_files(htmlfile)
        except:
            print("Error: ", htmlfile)
            continue
        foldername.set("working")

    winsound.Beep(800,400)
    winsound.Beep(500,600)
    winsound.Beep(700,800)
    foldername.set("DONE")
    print("DONE")

def load1():
    f = askdirectory()
    filename1.set(f)
    print(f)
    display_text=filename1.get().rsplit("/")[-2:]
    foldername.set(str("..."+display_text[0]+"/"+display_text[1]+"/"))

root=Tk()
root.title('Course files downloader')
filename1=StringVar()
foldername=StringVar()
stamp_text=StringVar()

if __name__ == "__main__":
    # get all files list
    tree_walk_list = []

    button1=Button(root, text="Choose folder", command=load1, font='Helvetica 14 bold',height = 4).grid(row=1, column=0)

    Label(root, textvariable=foldername,width=20).grid(row=3, column=1, sticky=(N,S,E,W))


    button2=Button(root, text="Get files", command=get_html_files,font='Helvetica 14 bold', fg="red", height =4).grid(row=1, column=2,sticky=E)


    Label(root, text="\n\n\nOmer Reuveni\nOmer@Solution-oriented.com", font='Helvetica 10',fg="blue", justify=LEFT).grid(row=6, column=0, sticky="w")

    root.mainloop()







