import requests
from bs4 import BeautifulSoup as soup
import tkinter as tk
from tkinter import filedialog, Text
import re
import webbrowser

#Recnik gde ime filma je kljuc a vrednosti su nam stranice sa linkovima za skidanje
movies = {}

#funkcija koja pretrazuje filmove prema nazivu
#ako ne unesemo naziv izbacice filmove sa pocetne strane
def Search():
    #zelimo u slucaju da nakon korisnik skine neki film i potom zeli da skine drugi
    #da mu ne ostaju stari rezultati pretrage
    for widget in frame.winfo_children():
        widget.destroy()

    #uzimamo ime iz Entry boxa i saljemo da bismo dobili stranicu kojoj zelimo da imamo pristup
    # u principu kada yts.mx/browse-movies unesemo ime filma dobijamo SVE filmove koji odgovaraju
    #pretrazi
    name = nameEntered.get()
    res = requests.get("https://yts.mx/browse-movies/" + name)
    #print(res.status_code)

    #parsiramo informacije pomocu BeautifulSoupa
    s = soup(res.text, 'lxml')
    titles = s.select('.browse-movie-title')
    links = s.select('.browse-movie-link')

    #ukoliko unesemo pogresno ime filma zelimo da korisnik dobije informaciju da je dobio pogresno ime filma
    if(len(titles) == 0):
        text_box = tk.Text(frame, height = 1.4, width = 300)
        text_box.insert(1.0, "Pogresno uneseno ime ili nema filma sa tim imenom na YTS")
        text_box.pack()
    #u suprotnom dajemo korisniku opcije da izabere koji od filmova zeli
    #posto je moguce da ima vise opcija npr (Godfather -> 1,2,3)
    else:
        for i in range(len(titles)):
            buttonMovie = tk.Button(frame, text= links[i].figure.img["alt"],
                                padx = 10, pady= 5, fg = "black", bg="white")
            buttonMovie.pack()
            buttonMovie.configure(command=lambda btn=buttonMovie: Links(btn))
            movies[links[i].figure.img["alt"]] = titles[i]['href']

#funkcija koja nam na osnovu izabranog filma (filma na koji smo kliknuli)
#izbacuje linkove i opise linkova (rezolucija i tip snimka) za izabrani film
def Links(btn):
    id = movies [btn.cget("text")]

    #sklanjamo prethodno stavljene buttone
    for widget in frame.winfo_children():
        widget.destroy()
    req = requests.get(id)
    s = soup(req.text, 'lxml')
    m = s.find_all("p", {"class":"hidden-md hidden-lg"})
    print(m[0])
    #pomocu regularnih izaraza izvlacimo potrebne informacije
    movie_links = re.compile('(https://yts.mx/torrent/download/[^"]+)')
    title = re.compile('(\"Download [^\"]*\")')
    titles = title.findall(str(m[0]))
    linkovi = movie_links.findall(str(m[0]))
    # brojac nam nije potreban ali cisto radi lepseg ispisa i numeracije
    i = 0
    for link in linkovi:
        text_box1 = tk.Text(frame, height = 1, width = 300)
        text_box1.insert(1.0, str(i+1)+ ". " + str(titles[i]))
        text_box1.pack()
        buttonLink = tk.Button(frame, text= str(link),
                            padx = 10, pady= 5, fg = "black", bg="white")
        buttonLink.pack()
        buttonLink.configure(command=lambda btn=buttonLink: Download(btn))
        i +=1

#funkcija koja nam za kliknuti link otvara taj link
#posto je link download za torrent link kada ga otvorimo mozemo direktno da ga
#dodamo u torrent
def Download(btn):
    webbrowser.open(btn.cget("text"))


#----------------------------------INTERFACE---------------------------------------------
height, width = 600, 700
root = tk.Tk()
root.title("Moives Download")

canvas = tk.Canvas(root, height = height, width = width, bg = "#000000")
canvas.pack()
frame = tk.Frame(root, bg = "white")
frame.place(relwidth = 0.98, relheight = 0.8,relx = 0.01, rely = 0.01)

labelIme = tk.Label(root, text = "Unesi ime filma")
labelIme.pack()
nameEntered = tk.Entry(root, width = 50)
nameEntered.pack()
search = tk.Button(root, text="search", padx = 10,
                        pady= 5, fg = "black", bg="white", command = Search)
search.pack()


root.mainloop()