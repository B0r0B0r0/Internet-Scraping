import mysql.connector

import subprocess



mycursor=""

user=""

mydb=""



def selfInit():

    global mydb

    mydb = mysql.connector.connect(

        host="localhost",

        user="root",

        password="123456789",

        database="Priceless"

    )

    global mycursor

    mycursor = mydb.cursor()

    global user

    user = subprocess.check_output(["whoami"]).decode("utf-8").strip()







def init():

    selfInit()

    sql = "CALL adauga_utilizator('"+user+"');"

    mycursor.execute(sql)

    mydb.commit()

    



def adaugaProd(denumire,pseudonim):

    selfInit()

    sql = "CALL add_produs_for_user('"+user+"','"+denumire+"','"+pseudonim+"')"

    mycursor.execute(sql)

    mydb.commit()







def getPseudonime():

    selfInit()

    sql = "CALL get_pseudonime_by_username('"+user+"');"

    mycursor.execute(sql)

    listaProd=[]

    for i in mycursor:

        aux =str(i)

        aux =aux[2:-3]

        listaProd.append(aux)

    return listaProd



def getPreturi(pseudonim,magazin):

    selfInit()

    sql = "CALL afisare_preturi('"+pseudonim+"','"+magazin+"')"

    mycursor.execute(sql)

    listaPret=[]

    for i in mycursor:

        listaPret.append(str(i)[1:-3])

    return listaPret



def adaugaPret(denumire,magazin,pret):

    selfInit()

    ora = subprocess.check_output("date '+%H'", shell=True).decode().strip()

    sql = "CALL adauga_pret('"+denumire+"','"+magazin+"','"+str(pret)+"','"+ora+"')"

    mycursor.execute(sql)

    mydb.commit()



def getOre(pseudonim,magazin):

    selfInit()

    sql = "CALL get_ore_by_pseudonim('"+pseudonim+"','"+magazin+"')"

    mycursor.execute(sql)

    listaOre=[]

    for i in mycursor:

        listaOre.append(str(i)[2:-3]),

    return listaOre



def getDenFromPs(pseudonim):

    selfInit()

    sql = "CALL get_denumire_produs('"+user+"', '"+pseudonim+"', @denumire_produs);"

    mycursor.execute(sql)

    sql = "SELECT @denumire_produs;"

    mycursor.execute(sql)

    for i in mycursor:

        return str(i)[2:-3]

    

def getDens():

    selfInit()

    sql = "select denumire from Produse;"

    mycursor.execute(sql)

    listaDens=[]

    for i in mycursor:

        listaDens.append(str(i)[2:-3])

    return listaDens



