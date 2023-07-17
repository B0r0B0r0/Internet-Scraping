#!/usr/bin/env python3
from NameScrapingAltex import AltexSc
from NameScrapingEmag import EmagScr
from NameScrapingEvomag import EvomagScr
from NameScrapingMediagalaxy import MediagalaxyScr
from NameScrapingPcgarage import PcgarageScr
from PriceAltex import PrAltex
from PriceEvomag import PrEvomag
from PriceEmag import PrEmag
from PriceMediagalaxy import PrMediaGalaxy
from PricePcgarage import PrPcgarage
from multiprocessing import Process,freeze_support,Queue
from DBManager import init, getDens,adaugaPret
import os
import subprocess



read_pipe_file = "GuiPipeManager.txt"
write_pipe_file = "ManagerPipeGui.txt"

def Altex(link,q):

    for i in range (1,20):
        result = AltexSc(link)
        if result != "Error":            
            break
    print("Altex Succes " + result)
    if result=="Error":
        result =""

    q.put(result)
 
def Evomag(link,q):
   
    for i in range (1,20):
        result = EvomagScr(link)
        if result != "Error":
            break
    print("Evomag Succes " + result)
    if result=="Error":
        result =""
        
    q.put(result)

def Emag(link,q):
    for i in range (1,20):
        result = EmagScr(link)
        if result != "Error":
            break
    print("Emag Succes " + result)
    if result=="Error":
        result =""
        
    q.put(result)

def Pcgarage(link,q):
  
    for i in range (1,20):
        result = PcgarageScr(link)
        if result != "Error":
            break
    print("PcGarage Succes " + result)
    if result=="Error":
        result =""
        
    q.put(result)

def Mediagalaxy(link,q):
    
    for i in range (1,20):
        result = MediagalaxyScr(link)
        if result != "Error":
            break
    print("MediaGalaxy Succes " + result)
    if result =="Error":
        result =""
        
    q.put(result)

def protocol_lista(comm):
    linkAltex = "https://altex.ro/cauta/?q=" + comm
    linkEvomag = "https://www.evomag.ro/?sn.q=" + comm
    linkEmag= "https://www.emag.ro/search/" + comm+"?ref=effective_search"
    linkPcgarage = "https://www.pcgarage.ro/cauta/"+comm
    linkMediagalaxy="https://mediagalaxy.ro/cauta/?q=" +comm

    q = Queue()

    t1 = Process(target=Altex, args=(linkAltex,q,))
    t2 = Process(target=Evomag, args=(linkEvomag,q,))
    t3 = Process(target=Emag, args=(linkEmag,q,))
    t4 = Process(target=Pcgarage, args=(linkPcgarage,q,))
    t5 = Process(target=Mediagalaxy, args=(linkMediagalaxy,q,))

    processes=[t1,t2,t3,t4,t5]

    for t in processes:
       
        t.start()

    t1.join(timeout=20)
    t2.join(timeout=10)
    t3.join(timeout=10)
    t4.join(timeout=10)
    t5.join(timeout=10)

    for t in processes:
        if t.is_alive():
            t.terminate()
            t.join()

    listaProduse=""
    
    for i in range (0,q.qsize()-1):
        listaProduse=listaProduse+q.get()

    listaProduse = listaProduse.split("#")
    with open (write_pipe_file,"w") as f:
         for prod in listaProduse:
            f.write(prod)
            f.write("\n")


def protocol_preturi(comm,automatic=False):
    
    q = Queue()
    p1 = Process(target=PrAltex, args=(comm,q,),name="Altex")
    p2 = Process(target=PrEmag, args=(comm,q,),name="Emag")
    p3 = Process(target=PrEvomag, args=(comm,q,),name="Evomag")
    p4 = Process(target=PrPcgarage, args=(comm,q,),name="PcGarage")
    p5 = Process(target=PrMediaGalaxy, args=(comm,q,),name="MediaGalaxy")

    processes = [p1,p2,p3,p4,p5]
    
    for p in processes:
        p.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()


    if automatic==False:
        with open (write_pipe_file,"w") as f:
            for i in range(0,q.qsize()):
                f.write(q.get())
                f.write("\n")
    
    if automatic == True:
        listaMgPr=[]
        for i in range(0,q.qsize()):
               string = q.get()
               string = string.split(" ")
               listaMgPr.append([string[0][:-1],[string[1][:-4]]])
        for i in listaMgPr:
            adaugaPret(comm,i[0],i[1])
if __name__=='__main__':
    init()
    while True:
        if os.path.getsize(read_pipe_file) > 0:
            with open(read_pipe_file,"r+") as f:
                comanda = f.read()
                if comanda[0] == "1":
                    freeze_support()
                    protocol_lista(comanda[2:])
                    f.truncate(0)
                    comanda = ""
                    listaProduse=""
                elif comanda[0] == "2":
                    freeze_support()
                    protocol_preturi(comanda[2:])
                    f.truncate(0)
                    comanda=""
        if subprocess.check_output("date '+%M'", shell=True).decode().strip() == "00":
            listaProd=getDens()
            processes=[]
            for i in listaProd:
                processes.append(Process(target=protocol_preturi, args=(i,True,),))
            for p in processes:
                p.start()
            for p in processes:
                p.join()
