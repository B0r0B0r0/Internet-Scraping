import PySimpleGUI as sg
import os
from DBManager import init,adaugaProd,adaugaPret,getPseudonime,getPreturi,getOre
import matplotlib.pyplot as plt
import os


def listaProduse():
    if os.path.getsize(write_pipe_path) == 0:
        with open(write_pipe_path,"w") as f:
            f.write("1 " + values[0])              # scriu numele produsului cautat
                                                        
        while os.path.getsize(read_pipe_path) == 0:
            pass                            # astept listele de produse
        lista =[]
        with open(read_pipe_path,"r+") as f:
            for linie in f.readlines():
                lista.append(linie)
            f.truncate(0)
    else:
         return ""

    collumn = []
    for produs in lista:
        collumn.append([sg.Button(produs)])
    layout= [
        [sg.Column(collumn, scrollable=True, size = (400,800))]
    ]
    window = sg.Window('Lista de produse gasite', layout)

    while True:
        event= window.read()
        if event[0] == sg.WIN_CLOSED:
            return
            
        if event != "":
            window.close()
            event = event[0].strip()
            return event




def PreiaPret(produs):
    produs = produs.split(" ")
    searchProd=""
    for i in range (0,5):
        searchProd = searchProd+produs[i] + " "
    searchProd = searchProd + produs[5]
    with open(write_pipe_path,"w") as f:
                f.write("2 " + searchProd)              # scriu numele produsului cautat
                                          
    while os.path.getsize(read_pipe_path) == 0:
        pass                                            # astept listele de preturi
    pretProd=[]    
    with open(read_pipe_path,"r+") as f:
        for linie in f.readlines():
            pretProd.append(linie)
        f.truncate(0)
    
    layout = [
    [sg.Text('Preturi:')],
    [sg.Text(pretProd[0][:-1])],
    [sg.Text(pretProd[1][:-1])],
    [sg.Text(pretProd[2][:-1])],
    [sg.Text(pretProd[3][:-1])],
    [sg.Text(pretProd[4][:-1])],
    [sg.Button('Close'),sg.Button('Adauga la favorite')]
    ]

    window = sg.Window("Preturi", layout,margins=(300,150))
    event, values = window.read()
    while True:
        if event=="Close" or event ==sg.WIN_CLOSED:
            window.close()
            break

        if event == "Adauga la favorite":
            event = ""
            layout2 = [
                [sg.Text('Introdu numele produsului:', size =(20, 1)), sg.InputText()],
                [sg.Submit(), sg.Cancel()]
            ]
            window2 = sg.Window("Favorites",layout2,margins=(100,50))
            while True:
                event2,values2=window2.read()
                if event2 == "Cancel" or event == sg.WIN_CLOSED:
                    window2.close()
                    break    
                if values2[0]!="":
                    adaugaProd(searchProd,values2[0])
                    for i in pretProd:
                        aux = i[:-5]
                        aux = aux.split(" ")
                        adaugaPret(searchProd,aux[0],aux[1])
                    window2.close()
                    break


def listaFavorite():
    favs=getPseudonime()
    collumn = []
    for i in favs:
        collumn.append([sg.Button(i)])
    layout= [
        [sg.Column(collumn, scrollable=True, size = (400,800))]
    ]
    window = sg.Window('Lista de favorite', layout)

    while True:
        event= window.read()
        if event[0] == sg.WIN_CLOSED:
            break
            
        if event != "":
            window.close()
            event = event[0].strip()
            return event


def favPret(fav):
    listaMagazine= ["Emag","PcGarage","MediaGalaxy","Altex","Evomag"]
    for j in listaMagazine: 
        listaOre= getOre(fav,j)
        listaPreturi=getPreturi(fav,j)
        fig, ax = plt.subplots()
        ax.plot(listaOre, listaPreturi)
        ax.set_xticklabels(listaOre)
        ax.set_title("Preturi " + j)
        ax.set_xlabel("Ora")
        ax.set_ylabel("Suma")
        fig.savefig(j+".png")
        fig.set_size_inches(6, 4)  
        fig.savefig(j + ".png", dpi=100)  

    layout =[  
                [
                    sg.Image(filename="Emag.png"),
                    sg.Image(filename="Altex.png"),
                    sg.Image(filename="PcGarage.png")
                ],
                [
                    sg.Image(filename="Evomag.png"),
                    sg.Image(filename="MediaGalaxy.png")
                ]  
            ]   
    window = sg.Window("Grafice", layout)




    event, values = window.read()

    # Închide fereastra PySimpleGUI și șterge fișierul graficului
    window.close()
    for j in listaMagazine:
        os.remove(j+".png")






write_pipe_path="GuiPipeManager.txt"
read_pipe_path="ManagerPipeGui.txt"

init()

produs = ""
fav = ""
layout = [
    [sg.Text('Introdu numele produsului:', size =(22, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel(), sg.Button('Arata favoritele')]
    ]
window = sg.Window("Priceless", layout,margins=(400,200))
while True:
    event, values = window.read()

    if event == "Cancel" or event == sg.WIN_CLOSED:
        break
    if values[0] != "":
        produs = listaProduse()
        event = ""
        values[0] =""

    if produs != "":
        PreiaPret(produs)
        produs = ""
        event = ""
        values[0] =""
    
    if event == "Arata favoritele":
        fav=listaFavorite()
        event = ""
        values[0] =""
    
    if fav != "":
        favPret(fav)
        fav=""
        event=""
        values[0]=""

                


