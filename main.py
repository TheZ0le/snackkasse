# Main Programm for Snackkasse
import random
import time
import mysql.connector
import hashlib
import os
global barcode

##########################################
#               WICHTIG:                 #
# Der SQL Server brauch den Benutzer:    #
# snackkasse und das PW : snackkasse     #
##########################################


###################################

def NewDB():

    """Erstellt zwei neue Datenbanken für Snacks und User"""

# Defienieren der userDB
    userDB = mysql.connector.connect(
        host="localhost",
        user="snackkasse",
        password="snackkasse"
    )
    usercursor = userDB.cursor()
# Erstellen der Datenbank
    usercursor.execute("CREATE DATABASE userDB")

# Neu Defienieren der userDB
    userDB = mysql.connector.connect(
        host="localhost",
        user="snackkasse",
        password="snackkasse",
        database="userDB"
    )
    usercursor = userDB.cursor()

# Erstellen einer Tabelle
    usercursor.execute("CREATE TABLE user (name VARCHAR(255),barcode VARCHAR(255),guthaben VARCHAR(255))")
# Erstellen eines primären schlüssels
    usercursor.execute("ALTER TABLE user ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

    # Defienieren der snackDB
    snackDB = mysql.connector.connect(
        host="localhost",
        user="snackkasse",
        password="snackkasse"
    )
    snackcursor = snackDB.cursor()
    # Erstellen der Datenbank
    snackcursor.execute("CREATE DATABASE snackDB")

    # Neu Defienieren der snackDB
    snackDB = mysql.connector.connect(
        host="localhost",
        user="snackkasse",
        password="snackkasse",
        database="snackDB"
    )
    snackcursor = snackDB.cursor()

    # Erstellen einer Tabelle
    snackcursor.execute("CREATE TABLE snack (name VARCHAR(255),preis VARCHAR(255),anzahl VARCHAR(255))")
    # Erstellen eines primären schlüssels
    snackcursor.execute("ALTER TABLE snack ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")


def Adduser():

    """Kann User hinzufuegen"""

    #Frage solange nachdem Benutzer bis er seine Eingabe bestaetigt
    while True:

        name = input("Wie ist Ihr Benutzername?\n>>")               # Fragt nach Benutzer namen
        barcode = str(random.randint(20000001, 29999999))           # generiert einen zufälligen Barcode
        guthaben = "0.00"                                           # setzt das guthaben auf 0.00
        print("Ihre Eingaben sind Folgende:")                       # zeigt alle Eingaben an
        print(name, "Ihr Barcode ist folgender:",barcode)           # zeigt alle Eingaben an
        time.sleep(5)                                               # wartet 5 sek.
        status = input("Wollen sie Ihre Eingaben bestaetigen? Dieser Vorgang kann nicht Rueckgaengig gemacht werden!(j/n)\n>>").lower()      #Fragt nach ob man die Eingaben bestaetigen möchte.
        # Abfrage der besteatigung
        if status == "j":
            break
        else:
            continue

    # setzt sql parameter
    sql = "INSERT INTO user (name, barcode, guthaben) VALUES (%s, %s, %s)"
    val = (name, barcode, guthaben)

    # Schreibt dir gesetzten paramerter in die DB
    usercursor.execute(sql, val)
    userDB.commit()
    print(usercursor.rowcount, "record inserted") # Zeigt an ob die Operation erfolgreich war


def Addsweets():

    """Kann Suessigkeiten hinzufuegen"""

    # Wieder holung bis der User Daten besteatigt
    while True:
        name = input("Welchen Snack moechtest du hinzufuegen? (klein geschrieben)\n>>") # Fragt nach snack hinzufuegen
        preis = input("Wie teuer soll der Snack sein?\n>>")                             # fragt den Preis vom Snack
        anzahl = input("Wie viele Snacks fuegst du hinzu?\n>>")                         # Fragt nach der Stueckzahl
        print("Ihre Eingaben sind Folgende:")                                           # zeigt Eingaben an
        print(name, preis, anzahl)                                                      # zeigt Eingaben an
        time.sleep(5)                                                                   # wartet 5 sekunden
        status = input("Wollen sie Ihre Eingaben bestaetigen? Dieser Vorgang kann nicht Rueckgaengig gemacht werden!(j/n)\n>>").lower() # Fragt nach besteatigung
        # ueberprueft besteatigung
        if status == "j":
            break
        else:
            continue

    # setzt sql parameter
    sql = "INSERT INTO snack (name, preis, anzahl) VALUES (%s, %s, %s)"
    val = (name, preis, anzahl)

    # schreibt in die DB
    snackcursor.execute(sql, val)
    snackDB.commit()
    print(snackcursor.rowcount, "record inserted") # Gibt den Erfolg der Operation an


def Rmall():

    """Kann alle Daten in der DB löschen"""

    # Pwd abfrage nach 3 mal dem falschen PWD wird der Vorgang abgebrochen
    for r in range(3):
        password = input("Gib bitte das Admin Passwort ein.\n>>").encode()
        password = hashlib.md5(password).hexdigest() # Erstellt eine md5 summe

        # Vergleicht Checksummen
        if password == "d8fa5e3391ec155720e3c9d0c12e6cc8":

            # Fragt option ab
            option = input("""Was möchtest du löschen?\n
                           Alle Userdaten (1)\n
                           Alle Snackdaten (2)\n
                           Beide Datensätze (3)\n
                           Vorgang Abrechen (return)\n>>""")
            if option == "1":
                # Löscht alle Userdaten und schreibt den Erfolg aus
                rmu = "DELETE FROM user"
                usercursor.execute(rmu)
                userDB.commit()
                print(usercursor.rowcount, "User record(s) deleted")
                break
            elif option == "2":
                # Löscht alle Snackdaten und schreibt den Erfolg aus
                rms = "DELETE FROM snack"
                snackcursor.execute(rms)
                snackDB.commit()
                print(snackcursor.rowcount, "Snack record(s) deleted")
                break
            elif option == "3":
                # Löscht alle Daten und schreibt den Erfolg aus
                rms = "DELETE FROM snack"
                snackcursor.execute(rms)
                snackDB.commit()
                print(snackcursor.rowcount, "Snack record(s) deleted")

                rmu = "DELETE FROM user"
                usercursor.execute(rmu)
                userDB.commit()
                print(usercursor.rowcount, "User record(s) deleted")
                break
            else:
                # Bricht den Vorgang ab
                print("Der Vorgang wird Abgebrochen.")
                break
        else:
            # Wird bei falschen Passwort ausgegeben
            print("Access Denied, Check you're Password")
            continue


def show_Tables():

    """Zeigt Tabbellen an"""

    #Fragt ab welche Datenbank gezeigt werden soll
    showtable = input("""Welche Tabelle möchtest du anzeigen?\n
                      Usertabbelle (1)\n
                      Snacktabbelle (2)\n
                      >>""")
    if showtable == "1":
        # Die User tabbelle wird angezeigt
        selecttable = "SELECT * FROM user"
        usercursor.execute(selecttable)
        selecttable = usercursor.fetchall()
        for x in selecttable:
            print(x)
    elif showtable == "2":
        # Die snacktabbelle wird angezeigt
        selecttable = "SELECT * FROM snack"
        snackcursor.execute(selecttable)
        selecttable = snackcursor.fetchall()
        for x in selecttable:
            print(x)
    else:
        # Wird bei falscher eingabe angezeigt
        print("Das ist kein Gültiger Parameter.")

def cnctDB():

    """Verbindet die Datenbank"""

    userDB = mysql.connector.connect(
        host="localhost",
        user="snackkasse",
        password="snackkasse",
        database="userDB"
    )
    usercursor = userDB.cursor()

    snackDB = mysql.connector.connect(
        host="localhost",
        user="snackkasse",
        password="snackkasse",
        database="snackDB"
    )
    snackcursor = snackDB.cursor()


def Admin():

    """Startet die Auswahl des Agminbereiches"""

    while True:
        wastun = input("""Was möchtest du tuen?\n
                    Das Programm Neu aufsetzen mit zwei leeren Datenbanken (1)\n
                    Einen User hinzufuegen (2)\n
                    Einen Snack hinzufuegen (3)\n
                    Alle Daten loeschen (4)\n
                    Datenbanken anzeigen (5)\n
                    Datenbank einbinden (6)\n
                    Vorgang abbrechen (Enter)\n>>""")
        if wastun == "1":
            NewDB()
            break
        elif wastun == "2":
            Adduser()
            break
        elif wastun == "3":
            Addsweets()
            break
        elif wastun == "4":
            Rmall()
            break
        elif wastun == "5":
            show_Tables()
            break
        elif wastun == "6":
            cnctDB()
            break
        else:
            print("Der Vorgang wird abgebrochen")
            break

    
def Buyskript():

    '''Regelt den Kaufverlauf'''

    snackcursor.execute("SELECT * FROM snack")                                  # Sucht alle Snacks aus der DB
    allSnacks = snackcursor.fetchall()                                          # schreibt Snacks in Var
    for x in allSnacks:                                                         # Zeigt Alle Snacks an
        print(x)
    produkt = input("Was möchtest du kaufen?\n>>").lower()                      # Fragt was du kaufen möchtest
    snackcursor.execute("SELECT preis FROM snack WHERE name =%s", (produkt,))   # Sucht den Preis vom Produkt
    pickedsnack = snackcursor.fetchall()                                        # Schreibt Preis in Var

    # Umwandlungsprozess tuple zu float
    snackpreis = ''.join([str(i) for i in pickedsnack])
    snackpreis = snackpreis.replace("(", "")
    snackpreis = snackpreis.replace(")", "")
    snackpreis = snackpreis.replace(",", "")
    snackpreis = snackpreis.replace("'", "")
    snackpreis = float(snackpreis)

    usercursor.execute("SELECT guthaben FROM user WHERE barcode=%s", (barcode,))# Sucht das User guthaben aus der DB
    pickedguthaben = usercursor.fetchall()                                      # Schreibt das guthaben des Users in VAR

    # Umwandlungsprozess tuble zu float
    guthaben = ''.join([str(i) for i in pickedguthaben])
    guthaben = guthaben.replace("(", "")
    guthaben = guthaben.replace(")", "")
    guthaben = guthaben.replace(",", "")
    guthaben = guthaben.replace("'", "")
    guthaben = float(guthaben)

    # Kauf Prozess
    print("\n Dein Guthaben betraegt " + str(guthaben) + " Euro\n")             # Zeigt guthaben
    kaufen = input("Möchtest du den Kauf abschliessen?(J/n)\n>>").lower()       # Fragt nach dem Kauf

    # Fragt nach ob du den Kauf taetigen willst
    if kaufen == "n":                                                           # Vorgang bricht ab
        print("Vorgang wird abgebrochen")
    else:                                                                       # Kauf wird durchgefuert
        newguthaben = guthaben - snackpreis                                     # Errechnet neues Guthaben
        newguthaben = str(newguthaben)
        sql = "UPDATE user SET guthaben=" + newguthaben + " WHERE barcode=" + barcode
        usercursor.execute(sql)                                                 # Schreibt in die mySQL DB
        userDB.commit()                                                         # Uebertraegt die aenderungen
        print("Dein neues Guthaben beträgt " + str(newguthaben) + " Euro")
    time.sleep(2)                                                               # Wartet 2 sek.

def Aufladen():

    '''Funktion zum Guthaben aufladen'''

    aufladen = float(input("Wie viel Guthaben willlst du aufladen/abbezahlen? (Format:0.00€)\n>>"))

    usercursor.execute("SELECT guthaben FROM user WHERE barcode=%s", (barcode,))  # Sucht das User guthaben aus der DB
    pickedguthaben = usercursor.fetchall()  # Schreibt das guthaben des Users in VAR

    # Umwandlungsprozess tuple zu float
    guthaben = ''.join([str(i) for i in pickedguthaben])
    guthaben = guthaben.replace("(", "")
    guthaben = guthaben.replace(")", "")
    guthaben = guthaben.replace(",", "")
    guthaben = guthaben.replace("'", "")
    guthaben = float(guthaben)

    newguthaben = guthaben + aufladen
    newguthaben = str(newguthaben)
    sql = "UPDATE user SET guthaben=" + newguthaben + " WHERE barcode=" + barcode
    usercursor.execute(sql)                                                   # Schreibt in die mySQL DB
    userDB.commit()                                                           # Uebertraegt die aenderungen
    print("Dein neues Guthaben beträgt " + str(newguthaben) + " Euro")
    time.sleep(2)                                                             # Wartet 2 sek.



######################################################################
#                         Start der Skriptes                         #
######################################################################

print("\nBeim Start des Skriptes werden Datenbanken eingebunden bzw. erstellt. -> QR-Code zum Admin Bereich >> 1416")

# Versucht Datenbanken einzubinden > Nicht Möglich? > erstellt Datenbanken
try:
    userDB = mysql.connector.connect(
        host="localhost",
        user="snackkasse",
        password="snackkasse",
        database="userDB"
    )
    usercursor = userDB.cursor()

    snackDB = mysql.connector.connect(
        host="localhost",
        user="snackkasse",
        password="snackkasse",
        database="snackDB"
    )
    snackcursor = snackDB.cursor()

except:
    NewDB()


while True:
    os.system("cls" if os.name == "nt" else "clear") # leert die Console

    # Hauptbereich fragt den Barcode ab und vergleicht
    print("----------------Snackkasse des Rechnerbetriebes Mathe----------------")
    barcode = input("Scanne einen Barcode.\n>>")

    if barcode == "1416": # Startet den  Admin Bereich
        Admin()
    elif barcode.startswith("2"): # Startet den verkauf
        status = input("Möchtest du Guthaben aufladen (1) oder einen Snack kaufen (2)?\n>>")
        if status == "1":
            Aufladen()
        else:
            Buyskript()
    elif barcode == "420": # Beendet das Programm
        break
    else:
        print("Dein QR code ist ungültig!")