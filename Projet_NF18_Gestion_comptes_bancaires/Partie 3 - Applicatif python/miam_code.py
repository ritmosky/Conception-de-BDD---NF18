########## CONNEXION ##########


# bibliothèque
# exécuter => pip install package_name pour installer un package
import psycopg2
import csv
import glob
import os.path

from createDrop import create_table, drop_table
from importCSV import import_data, save_csv
from constraints import constraint_type_account, constraint_type_operation
from update import *
from display import *
from insert import *
from miscellaneous import type_operation, type_compte

HOST = "localhost"
USER = "postgres"
PASSWORD = "fort"
DATABASE = "postgres"


try:
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
except psycopg2.ProgrammingError as e:
    print("message système : ", e)
except psycopg2.OperationalError as e:
    print("message système : ", e)


########## MENU ##########


try:
    create_table(conn)  # pour créer les tables
    import_data(conn)   # pour importer des données csv
except psycopg2.errors.InFailedSqlTransaction as e:
    print("message système : ", e)
except psycopg2.errors.DuplicateTable as e:
    print("message système : ", e)


#drop_table(conn)   # pour supprimer les tables


try:
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
except psycopg2.ProgrammingError as e:
    print("message système : ", e)
except psycopg2.OperationalError as e:
    print("message système : ", e)



choice = '1'

while choice!='0':

    print("\n ------------ MENU -----------")
    print(" 1. Ajouter un client")
    print(" 2. Ajouter un compte et son type")
    print(" 3. Ajouter un propriétaire à un compte")
    print(" 4. Ajouter une opération et son type")
    print(" 6. Afficher tous les clients")
    print(" 7. Afficher tous les comptes")
    print(" 8. Afficher tous les propriétaires")
    print(" 9. Afficher toutes les opérations")

    print(" 10. Afficher balance d'un compte")
    print(" 11. Afficher nombre de chèques émis par un client")
    print(" -----------------------------\n")
    choice = input(" choix : ")
    if choice=='1':
        add_customer(conn)
        conn.commit()
        save_csv(path, conn)
    if choice=='2':
        add_account(conn)
        conn.commit()
        save_csv(path, conn)
    if choice=='3':
        add_owner(conn)
        conn.commit()
        save_csv(path, conn)
    if choice=='4':
        add_operation(conn)
        conn.commit()
        save_csv(path, conn)
    if choice=='6':
        display_all_customer(conn)
    if choice=='7':
        display_all_account(conn)
    if choice=='8':
        display_all_owner(conn)
    if choice=='9':
        display_all_operation(conn)
    if choice=='10':
        try:
            date = quote(input("\n date de création aaaa-mm-jj hh:mm = "))
            cur = conn.cursor()
            sql = "SELECT balance FROM compteepargne WHERE date_crea={} UNION SELECT balance FROM compterevolving WHERE date_crea={} UNION SELECT balance FROM comptecourant WHERE date_crea={}".format(date,date,date)
            # ou simplement avec "SELECT balance FROM {} WHERE date_crea={}".format(type_compte(date))
            cur.execute(sql)
            res = cur.fetchone()
            print("\n## Le compte crée {} a {}€ de balance".format(date, res[0]))
        except psycopg2.errors.InvalidDatetimeFormat as e:
            print("message système : ", e)
        except psycopg2.errors.DatetimeFieldOverflow as e:
            print("message système : ", e)
        except psycopg2.errors.InFailedSqlTransaction as e:
            print("message système : ", e)
    if choice=='11':
        try:
            client = quote(input("\n id(tel) du client : "))
            cur = conn.cursor()
            sql = "SELECT count(id) FROM Operation NATURAL JOIN EmissionCheque WHERE client={}".format(client)
            cur.execute(sql)
            res = cur.fetchone()
            print("\n## Le client {} a émis {} chèques ".format(client, res[0]))
        except psycopg2.errors.InFailedSqlTransaction as e:
            print("message système : ", e)
        except psycopg2.errors.InvalidTextRepresentation as e:
            print("message système : ", e)


# Clôture de la connexion
conn.close()


