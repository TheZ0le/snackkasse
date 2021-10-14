# Main Programm for Snackkasse
import random
import time
import mysql.connector
import hashlib
import getpass
global barcode

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

    while True:
        name = input("Wie ist Ihr Benutzername?\n>>")
        barcode = str(random.randint(20000001, 29999999))
        guthaben = "0.00"
        print("Ihre Eingaben sind Folgende:")
        print(name, "Ihr Barcode ist folgender:",barcode)
        time.sleep(5)
        status = input("Wollen sie Ihre Eingaben bestaetigen? Dieser Vorgang kann nicht Rueckgaengig gemacht werden!(j/n)\n>>").lower()
        if status == "j":
            break
        else:
            continue

    sql = "INSERT INTO user (name, barcode, guthaben) VALUES (%s, %s, %s)"
    val = (name, barcode, guthaben)

    usercursor.execute(sql, val)
    userDB.commit()
    print(usercursor.rowcount, "record inserted")


def Addsweets():

    while True:
        name = input("Welchen Snack moechtest du hinzufuegen?\n>>")
        preis = input("Wie teuer soll der Snack sein?\n>>")
        anzahl = input("Wie viele Snacks fuegst du hinzu?\n>>")
        print("Ihre Eingaben sind Folgende:")
        print(name, preis, anzahl)
        time.sleep(5)
        status = input("Wollen sie Ihre Eingaben bestaetigen? Dieser Vorgang kann nicht Rueckgaengig gemacht werden!(j/n)\n>>").lower()
        if status == "j":
            break
        else:
            continue

    sql = "INSERT INTO snack (name, preis, anzahl) VALUES (%s, %s, %s)"
    val = (name, preis, anzahl)

    snackcursor.execute(sql, val)
    snackDB.commit()
    print(snackcursor.rowcount, "record inserted")


def Rmall():
    for r in range(3):
        password = input("Gib bitte das Admin Passwort ein.\n>>").encode()
        password = hashlib.md5(password).hexdigest()

        if password == "d8fa5e3391ec155720e3c9d0c12e6cc8":
            option = input("""Was möchtest du löschen?\n
                           Alle Userdaten (1)\n
                           Alle Snackdaten (2)\n
                           Beide Datensätze (3)\n
                           Vorgang Abrechen (return)\n>>""")
            if option == "1":
                rmu = "DELETE FROM user"
                usercursor.execute(rmu)
                userDB.commit()
                print(usercursor.rowcount, "User record(s) deleted")
                break
            elif option == "2":
                rms = "DELETE FROM snack"
                snackcursor.execute(rms)
                snackDB.commit()
                print(snackcursor.rowcount, "Snack record(s) deleted")
                break
            elif option == "3":
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
                print("Der Vorgang wird Abgebrochen.")
                break
        else:
            print("Access Denied, Check you're Password")
            continue


def show_Tables():
    showtable = input("""Welche Tabelle möchtest du anzeigen?\n
                      Usertabbelle (1)\n
                      Snacktabbelle (2)\n
                      >>""")
    if showtable == "1":
        selecttable = "SELECT * FROM user"
        usercursor.execute(selecttable)
        selecttable = usercursor.fetchall()
        print(selecttable)
    elif showtable == "2":
        selecttable = "SELECT * FROM snack"
        snackcursor.execute(selecttable)
        selecttable = snackcursor.fetchall()
        print(selecttable)
    else:
        print("Das ist kein Gültiger Parameter.")

def cnctDB():
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
    while True:
        wastun = input("""Was möchtest du tuen?\n
                    Das Programm Neu aufsetzen mit zwei leeren Datenbanken (1)\n
                    Einen User hinzufuegen (2)\n
                    Einen Snack hinzufuegen (3)\n
                    Alle Daten loeschen (4)\n
                    Datenbanken anzeigen (5)\n
                    Datenbank einbinden (6)\n>>""")
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
            print("Das ist kein Gültiges Argument")
            continue

    
def Buyskript():


    snackcursor.execute("SELECT name FROM snack")
    allSnacks = snackcursor.fetchall()
    print(allSnacks)
    produkt = input("Was möchtest du kaufen?\n>>").lower()
    snackcursor.execute("SELECT preis FROM snack WHERE name =" + produkt)



while True:
    print("----------------Snackkasse des Rechnerbetriebes Mathe----------------")
    barcode = input("Scanne einen Barcode.\n>>")

    if barcode == "1416":
        Admin()
    elif barcode.startswith("2"):
        Buyskript()
    elif barcode == "420":
        break
    else:
        print("Dein QR code ist ungültig!")