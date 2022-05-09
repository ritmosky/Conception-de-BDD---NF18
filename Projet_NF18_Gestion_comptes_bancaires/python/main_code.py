########## CONNEXION ##########



# bibliothèque
# exécuter => pip install package_name pour installer un package
import psycopg2
import os.path


# se placer dans '/Users/taoufiq/Documents/school/Utc/sem02/NF18/nf18/Projet_NF18_Gestion_comptes_bancaires/python'
os.chdir('/Users/taoufiq/Documents/school/Utc/sem02/NF18/nf18/Projet_NF18_Gestion_comptes_bancaires/python')


from add_element import *
from operation import *
from display import *
from create_drop_load_save import *
from constraintsEtDivers import *


# '/Users/taoufiq/Documents/school/Utc/sem02/NF18/nf18/Projet_NF18_Gestion_comptes_bancaires/SQL_et_Data'

########## CONNEXION ##########



HOST = "localhost"
USER = "me"
PASSWORD = "secret"
DATABASE = "projetdb"


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


# drop_table(conn)   # pour supprimer les tables


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
    print(" 2. Ajouter une opération et son type")
    print(" 3. Afficher tous les clients")
    print(" 4. Afficher tous les comptes")
    print(" 5. Afficher tous les propriétaires")
    print(" 6. Afficher toutes les opérations")
    print(" 7. Afficher balance d'un compte")
    print(" 8. Afficher nombre de chèques émis par un client")
    print(" -----------------------------\n")
    choice = input(" choix : ")

    if choice=='1':  # Ajouter un client
        tel = add_customer(conn)
        conn.commit()
        print(" 1. Ajouter à un nouveau compte et son type")
        print(" 2. Ajouter à un compte existant")
        choice1 = input(" choix : ")

        while choice1!='ok':
            if choice1=='1': # Ajouter à un nouveau compte et son type
                date_crea = add_account(conn, tel)
                add_owner(conn, tel, date_crea)
                choice1 = 'ok'
            if choice=='2':   # Ajouter à un compte existant
                quote(input(" date de création aaaa-mm-jj hh:mm:ss du compte = "))
                add_owner(conn, tel, date_crea)
                choice1 = 'ok'
        conn.commit()
        save_csv(path, conn)


    if choice=='2': # Ajouter une opération et son type
        add_operation(conn)
        conn.commit()
        save_csv(path, conn)

    if choice=='3': # Afficher tous les clients
        display_all_customer(conn)

    if choice=='4': # Afficher tous les comptes
        display_all_account(conn)

    if choice=='5': # Afficher tous les propriétaires
        display_all_owner(conn)

    if choice=='6': # Afficher toutes les opérations
        display_all_operation(conn)

    if choice=='7': # Afficher balance d'un compte
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

    if choice=='8': # Afficher nombre de chèques émis par un client
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


