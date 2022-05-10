########## AJOUTER ##########

import psycopg2
from constraintsEtDivers import *
from operation import *


# ajouter un client
def add_customer(conn):
    print("\n ## Ajouter un client \n")
    try:
        tel = int(input(" tel : "))
    except ValueError as e:
        print("Message système : ",e)
        return
    nom = quote(input(" nom : "))
    adresse = quote(input(" adresse : "))

    try:
        cur = conn.cursor()
        sql = "INSERT INTO Client VALUES ({},{},{})".format(tel, nom, adresse)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
    return tel



# Ajouter un propriétaire à un compte
def add_owner(conn, tel, date_crea):
    print("\n ## Ajouter à un compte existant \n")
    try:
        cur = conn.cursor()
        sql = "INSERT INTO Asso_Compte_Client VALUES ({},{})".format(tel,date_crea)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



def add_account_type(date_crea, type_c, c, conn):
    #Compte Epargne
    if c=='1':
        print("\n ## Ajouter un compte Epargne \n")
        balance = float(input(" balance (>0): "))
        solde_min_const = float(input(" solde minimum statuaire entre [0;balance]) : "))
        try:
            cur = conn.cursor()
            sql = "INSERT INTO {} VALUES ({},{},{})".format(type_c, date_crea, balance, solde_min_const)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)

    #Compte Revolving
    if c=='2':
        print("\n ## Ajouter un compte Revolving \n")
        balance = float(input(" balance (<0) : "))
        taux_j = float(input(" taux journalier entre ]0;1[ : "))
        montant_min = float(input(" prêt minimum (<balance) : "))
        try:
            cur = conn.cursor()
            sql = "INSERT INTO {} VALUES ({},{},{},{})".format(type_c, date_crea, balance, taux_j, montant_min)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)

    #Compte Courant
    if c=='3':
        print("\n ## Ajouter un compte Courant \n")
        balance = float(input(" balance (>0) : "))
        dec_autorise = quote(input(" montant du découvert autorisé (>=0) ou nullable : "))
        max_solde = float(input(" balance maximum (>0) : "))
        min_solde = float(input(" balance minimum (>0) : "))
        debut_decouvert = quote(input(" début du découvert aaaa-mm-jj hh:mm ou nullable = "))
        try:
            cur = conn.cursor()
            sql = "INSERT INTO {} VALUES ({},{},{},{},{},{})".format(type_c, date_crea, balance, dec_autorise, max_solde, min_solde, debut_decouvert)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)



def add_account(conn):
    # ajouter un compte
    print("\n ## Ajouter à un nouveau compte \n")
    date_crea = quote(input(" date de création aaaa-mm-jj hh:mm:ss du compte = "))
    statut = quote(input(" statut(ouvert,bloqué ou fermé) : "))
    try:
        cur = conn.cursor()
        sql = "INSERT INTO Compte VALUES ({},{})".format(date_crea, statut)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
        return
    # ajouter le type du compte
    print("\n ## Ajouter un type de compte \n")
    c = '0'
    while c not in ['1', '2', '3'] :
        print(" 1. Pour un Compte Epargne")
        print(" 2. Pour un Compte Revolving")
        print(" 3. Pour un Compte Courant \n")
        c = input(" choix : ")
    if c=='1':
        type_c = "CompteEpargne"
    if c=='2':
        type_c = "CompteRevolving"
    if c=='3':
        type_c = "CompteCourant"

    if constraint_type_account(date_crea, type_c, conn):
        add_account_type(date_crea, type_c, c, conn)
    else:
        print("\n /!\ Ce compte a déjà un type /!\ ")
    return date_crea



def add_operation_type(date, date_crea, id, montant, conn):
    # Ajouter le type de l'opération
    num = '0'
    while num not in ['1','2','3','4','5','6']:
        print(" ------------------ ")
        print(" 1. Pour faire un retrait au guichet")
        print(" 2. Pour faire un dépôt au guichet")
        print(" 3. Pour faire virement")
        print(" 4. Pour déposer de chèque")
        print(" 5. Pour émettre un chèque")
        print(" 6. Pour faire un retrait avec carte Bleue \n")
        num = input(" choix : ")
    if constraint_type_operation(date,date_crea,num,id,conn) and restriction_type_operation(date_crea,num,conn)[0]: # si opération possible
        print('\n ==> opération possible <== ')
        try:
            cur = conn.cursor()
            sql = "INSERT INTO {} VALUES ({})".format(ops.get(num),id)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)

    else :  # si opération impossible
        print('\n ==> /!\ opération impossible /!\ <==  car :')
        print(restriction_type_operation(date_crea,num,conn)[1])
    return num



def add_operation(conn):
    # Ajouter une opération
    print("\n ## Ajouter une opération \n")
    id = int(input(" id de l'opération' : "))
    montant = float(input(" montant de l'opération (>0) : "))
    date = quote(input(" date d'opération aaaa-mm-jj = "))
    print(" état par défaut = non traité ")
    etat = quote('non traité')
    client = int(input(" tel du client : "))
    date_crea = quote(input(" date de création aaaa-mm-jj hh:mm:ss = "))
    if is_owner(client,date_crea, conn)[0]:  # compte appartient au client
        try:
            cur = conn.cursor()
            sql = "INSERT INTO Operation VALUES ({},{},{},{},{},{})".format(id,montant,date,etat,client,date_crea)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)

        type_account = 'Compte' + type_compte(date_crea, conn).capitalize()
        # Ajouter le type de l'opération
        motif = add_operation_type(date, date_crea, id, montant, conn)
        deplacer(date_crea, id, motif, montant, conn)

    else: # compte n'appartient pas au client
        print(is_owner(client,date_crea,conn)[1])
