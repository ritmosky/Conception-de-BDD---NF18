########## Afficher ##########

from create_drop_load_save import *
from constraintsEtDivers import *
import psycopg2



# dictionnaire des opérations
ops = {
"1": "DebitGuichet",
"2": "CreditGuichet",
"3": "Virement",
"4": "DepotCheque",
"5": "EmissionCheque",
"6": "CarteBleu"
}


# afficher tous les clients
def display_all_customer(conn):
    print("\n ## Afficher tous les clients \n\n")
    try:
        cur = conn.cursor()
        sql = "SELECT * FROM Client"
        cur.execute(sql)
        res = cur.fetchone()
        if res==None:
            print("/!\ AUCUN CLIENT /!\\")
        while res:
            print(" - tel: {} | nom: {} | adresse: {}".format(res[0],res[1],res[2]))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# afficher tous les comptes
def display_all_account(conn):
    print("\n ## Afficher tous les comptes \n")
    try:
        cur = conn.cursor()
        sql = "SELECT date_crea, statut FROM Compte"
        cur.execute(sql)
        res = cur.fetchone()
        if res==None:
            print("/!\ AUCUN COMPTE /!\\")
        while res:
            type = type_compte(quote(res[0]), conn)
            print(" - date création: {} | statut: {} | type: {} ".format(res[0],res[1],type))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# afficher tous les propriétaires
def display_all_owner(conn):
    print("\n ## Afficher tous les propriétaires  \n")
    try:
        cur = conn.cursor()
        sql = "SELECT tel, nom, date_crea FROM Asso_Compte_Client NATURAL JOIN Client"
        cur.execute(sql)
        res = cur.fetchone()
        if res==None:
            print("/!\ AUCUN PROPRIÉTAIRE /!\\")
        while res:
            type = type_compte(quote(res[2]), conn)
            print(" - tel: {} | nom: {} | date création: {} | type: {}".format(res[0],res[1],res[2],type))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# afficher toutes les opération
def display_all_operation(conn):
    print("\n ## afficher tous les propriétaires  \n")
    try:
        try:
            cur = conn.cursor()
            sql = "SELECT id, montant, date, etat, client, date_crea FROM Operation"
            cur.execute(sql)
            res = cur.fetchone()
        except psycopg2.errors.InFailedSqlTransaction as e:
            print("message système : ", e)
        if res==None:
            print("/!\ AUCUNE OPÉRATION /!\\")
        while res:
            type = type_operation(res[0], conn)
            print(" - id: {} | type: {} | montant: {} | date: {} | etat: {} | client: {} | date_crea: {} ".format(res[0],type,res[1],res[2],res[3],res[4],res[5]))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)