"""
- effectuer des requêtes avec un fichier sql
\i documents/school/utc/sem02/nf18/projet_nf18/nom_fichier.sql

- pour importer un fichier csv(d'abord se placer dans le dossier)
\cd doss/.../dossier_fichier
\copy Client FROM 'client.csv' WITH CSV HEADER DELIMITER  ';' QUOTE '"'
"""


########## CONNEXION ##########


# bibliothèque
# exécuter => pip install package_name pour installer un package
import psycopg2
import csv
import glob
import os.path

 
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


########## INITIALIZATION ##########


# 'documents/school/utc/sem02/nf18/projet_nf18'
path = input('chemin du dossier où stocker les données(.../.../dossier) : ')


# create tables ->
f = open(path+'/create.sql', 'r')
cur = conn.cursor()
sql_create = " ".join(f.readlines())
cur.execute(sql_create)
conn.commit()


# /!\/!\/!\ drop tables /!\/!\/!\
f = open(path+'/drop.sql', 'r')
cur = conn.cursor()
sql_drop = " ".join(f.readlines())
cur.execute(sql_drop)
conn.commit()


# pour charger tous les fichiers csv dans le dossier
# /!\ il faut renommer les fichiers csv selon le nom des tables en minuscule /!\
for file in glob.glob(path + "/*.csv"):
    print(file)
    with open(file, 'r') as f:
        cur = conn.cursor()
        next(f)     # sauter l'en-tête
        table_name = file[len(path)+1:file.find('.csv')]
        cur.copy_from(f, table_name, sep=';')
        conn.commit()


########## Enregistrer les tables dans un fichier CSV  ##########



# dictionnaire des attributs des différentes tables
dico = {
'Client_col' : ["tel", "nom", "adresse"],
'Compte_col' : ['date_crea', 'statut'],
'Asso_Compte_Client_col' : ['tel', 'date_crea'],
'CompteEpargne_col' : ['date_crea', 'balance', 'solde_min_const'],
'CompteRevolving_col' : ['date_crea', 'balance', 'taux_j', 'montant_min'],
'CompteCourant_col' : ['date_crea', 'balance', 'montant_decouvert_autorise','max_solde' ,'min_solde', 'date_debut_decouvert'],
'Operation_col' : ['id', 'montant', 'date', 'etat', 'client', 'date_crea'],
'DebitGuichet_col' : ['id', 'compteCourant', 'compteRevolving', 'compteEpargne'],
'CreditGuichet_col' : ['id', 'compteCourant', 'compteRevolving', 'compteEpargne'],
'Virement_col' : ['id', 'compteCourant', 'compteRevolving', 'compteEpargne'],
'DepotCheque_col' : ['id', 'compteCourant', 'compteRevolving'],
'EmissionCheque_col' : ['id', 'compteCourant', 'compteRevolving'],
'CarteBleu_col' : ['id', 'compteCourant', 'compteRevolving']
}



def save_csv(chemin):
    #cols, table = recognize_table()
    for key,cols in dico.items():
        table = key[:key.find('_col')]
        cur = conn.cursor()
        sql = "SELECT * FROM {}".format(table)
        cur.execute(sql)
        line = cur.fetchone()
    #Ouverture du fichier CSV en écriture
        with open('{}/{}.csv'.format(chemin, table.lower()),'w',newline='') as f:
            ecrire = csv.writer(f, delimiter=";")
            ecrire.writerow(cols) # écrire une ligne dans le fichier
            while line:
                    ecrire.writerow(line)
                    line = cur.fetchone()  # passage à la ligne suivante



########## FONCTIONS INTERMEDIAIRES ##########


def quote(s):
    if s:
        return "\'%s\'" % s
    else:
        return 'NULL'


def type_compte(date_crea):
    types = ["CompteCourant", "CompteRevolving", "CompteEpargne"]
    try:
        for type in types:
            cur = conn.cursor()
            sql = "SELECT COUNT(date_crea) FROM {} WHERE date_crea={}".format(type, date_crea)
            cur.execute(sql)
            res = cur.fetchone()
            if res[0] != 0:
                return type.lower()[6:]
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
        

        
def type_operation(id):
    try:
        for type in list(ops.values()):
            cur = conn.cursor()
            sql = "SELECT COUNT(id) FROM {} WHERE id={}".format(type, id)
            cur.execute(sql)
            res = cur.fetchone()
            if res[0] != 0:
                return type
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)


########## AJOUTER ##########


        
# ajouter un client
def add_customer(conn):
    print("\n ## Ajouter un client \n")
    tel = int(input(" tel : "))
    nom = quote(input(" nom : "))
    adresse = quote(input(" adresse : "))

    try:
        cur = conn.cursor()
        sql = "INSERT INTO Client VALUES ({},{},{})".format(tel, nom, adresse)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# Ajouter un propriétaire à un compte
def add_owner(conn):
    print("\n ## Ajouter un propriétaire à un compte \n")
    tel = int(input(" tel : "))
    date_crea = quote(input(" date de création aaaa-mm-jj hh:mm:ss = "))

    try:
        cur = conn.cursor()
        sql = "INSERT INTO Asso_Compte_Client VALUES ({},{})".format(tel,date_crea)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



########## COMPTES/CONTRAINTES_COMPTES ##########
"""
----> on verifie à chaque insertion si date_crea de la classe fille n'est pas 
présente dans les autres filles sinon execption
PROJECTION(Compte, date_crea) = PROJECTION(CompteCourant, date_crea) UNION
                                PROJECTION(CompteRevolving, date_crea) UNION
                                PROJECTION(CompteEpargne, date_crea)
"""


# retourne True si la contrainte est respectée, sinon False
def constraint_type_account(date_crea, a_type):
    types = ["CompteCourant", "CompteRevolving", "CompteEpargne"]
    try:
        types.remove(a_type)
        for c in types:
            cur = conn.cursor()
            sql = "SELECT COUNT(*) FROM %s WHERE date_crea=%s" % (c, date_crea)
            cur.execute(sql)
            res = cur.fetchone()
            if res[0]!=0 and res!=None:
                return False
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
    return True



# les intérets journaliers sont ajoutés à la balance du compteRevolving
def calcul_interet_j():
    cur = conn.cursor()
    sql = "SELECT balance,taux FROM CompteRevolving WHERE date_crea={}".format(date_crea)
    cur.execute(sql)
    balance, taux = cur.fetchone()
    balance += taux*balance
    return balance



def account_type(date_crea, a_type, num):
    #Compte Epargne
    if num=='1': 
        print("\n ## Ajouter un compte Epargne \n")
        balance = float(input(" balance (>0): "))
        solde_min_const = float(input(" solde minimum statuaire entre [0;balance]) : "))
        try:
            cur = conn.cursor()
            sql = "INSERT INTO {} VALUES ({},{},{})".format(a_type, date_crea, balance, solde_min_const)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)
            
    #Compte Revolving
    if num=='2':
        print("\n ## Ajouter un compte Revolving \n")
        balance = float(input(" balance (<0) : "))
        taux_j = float(input(" taux journalier entre ]0;1[ : "))
        montant_min = float(input(" prêt minimum (<balance) : "))
        try:
            cur = conn.cursor()
            sql = "INSERT INTO {} VALUES ({},{},{},{})".format(a_type, date_crea, balance, taux_j, montant_min)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)
            
    #Compte Courant
    if num=='3':
        print("\n ## Ajouter un compte Courant \n")
        balance = float(input(" balance (>0) : "))
        dec_autorise = quote(input(" montant du découvert autorisé (>=0) ou nullable : "))
        max_solde = float(input(" balance maximum (>0) : "))
        min_solde = float(input(" balance minimum (>0) : "))
        debut_decouvert = quote(input(" début du découvert aaaa-mm-jj hh:mm ou nullable = "))
        try:
            cur = conn.cursor()
            sql = "INSERT INTO {} VALUES ({},{},{},{},{},{})".format(a_type, date_crea, balance, dec_autorise, max_solde, min_solde, debut_decouvert)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)

    
        
def add_account(conn):
    # ajouter un compte
    print("\n ## Ajouter un compte \n")
    date_crea = quote(input(" date de création aaaa-mm-jj hh:mm:ss = "))
    statut = quote(input(" statut(ouvert,bloqué ou fermé) : "))
    try:
        cur = conn.cursor()
        sql = "INSERT INTO Compte VALUES ({},{})".format(date_crea, statut)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
    # ajouter le type du compte
    print("\n ## Ajouter un type de compte \n")
    c = '0'
    while c not in ['1', '2', '3'] :
        print(" 1. Pour un Compte Epargne")
        print(" 2. Pour un Compte Revolving")
        print(" 3. Pour un Compte Courant \n")
        c = input(" choix : ")
    if c=='1':
        a_type = "CompteEpargne"
    if c=='2':
        a_type = "CompteRevolving"
    if c=='3':
        a_type = "CompteCourant"
        
    if constraint_type_account(date_crea, a_type):
        account_type(date_crea, a_type, c)
    else:
        print("\n /!\ Ce compte a déjà un type /!\ ")



########## OPERATIONS/CONTRAINTES_OPERATIONS ##########


ops = {
"1": "DebitGuichet",
"2": "CreditGuichet",
"3": "Virement",
"4": "DepotCheque",
"5": "EmissionCheque",
"6": "CarteBleue"
}


"""
----> compte ne peut pas effectuer plusieurs opérations en même temps
----> on verifie que id de la classe fille se trouve dans Compte et n'est pas dans les autres filles sinon execption
PROJECTION(Operation, id) = PROJECTION(CarteBleu, id) UNION
                            PROJECTION(EmissionCheque, id) UNION
                            PROJECTION(DepotCheque, id) UNION
                            PROJECTION(Virement, id) UNION
                            PROJECTION(CreditGuichet, id) UNION
                            PROJECTION(DebitGuichet, id)
"""

def constraint_type_account(date, date_crea, motif, id):
    types = list(ops.values())
    try:
        types.remove(ops.get(motif))
        for o in types:   # exclusivités des opérations
            cur = conn.cursor()
            sql1 = "SELECT COUNT(*) FROM {} WHERE id={}".format(o, id)
            cur.execute(sql1)
            res1 = cur.fetchone()
            if res1[0]!=0 and res1!=None:
                return False

            # un compte ne peut effectuer plusieurs opérations en même temps
            sql2 = "SELECT COUNT(*) FROM {} WHERE date={} AND date_crea={}".format(o,date,date_crea)
            cur.execute(sql2)
            res2 = cur.fetchone()
            if res2[0]!=0 and res2!=None:
                return False

        # un compte ne peut effectuer plusieurs opérations de même type en même temps
        o = ops.get(motif)
        cur = conn.cursor()
        sql3 = "SELECT COUNT(*) FROM {} WHERE date={} AND date_crea={}".format(o,date,date_crea)
        cur.execute(sql3)
        res3 = cur.fetchone()
        if res3[0]>1 and res3!=None:
            return False

    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
    return True



"""
----> restreindre les opérations pour chaque type de compte
- compte épargne n'effectue que les opérations au guichet et virements
- compte fermé n'effectue aucune opération
- compte bloqué n'effectue que des debits et crédits
"""

def restriction_type_operation(date_crea, motif):
    try:
        # compte épargne -> opérations au guichet et virements
        cur = conn.cursor()
        sql = "SELECT balance FROM CompteEpargne WHERE date_crea=%s" % (date_crea)
        cur.execute(sql)
        res = cur.fetchone()
        if res!=None and motif not in ['1','2','3']:
            return False 
            
        # compte fermé -> aucune opération
        cur = conn.cursor()
        sql = "SELECT statut FROM Compte WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        statut = cur.fetchone()[0]
        if statut=='fermé':
            return False  
            
        # compte bloqué -> debits et crédits
        if statut=='bloqué' and motif not in ['1','2']:
            return False 
             
        return True
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



########## OPERATIONS ##########



# on retire de l'argent (DebitGuichet, Virement, EmissionCheque, CarteBleue)
def debiter(date_crea, motif, type, montant):
    # CompteCourant
    if type == 'CompteCourant':
        compteCourant = date_crea
        cur = conn.cursor()
        sql = "SELECT balance,min_solde,montant_decouvert_autorise FROM CompteCourant WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance, min, decouvert = cur.fetchone()
        dif = balance-montant
        if dif>min:     # si il y'a assez de fonds
            cur = conn.cursor()
            sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}" % (dif, date_crea)
            cur.execute(sql)
            return True
        # pour utiliser le découvert, nous baissons la valeur min_solde
        if dif<=min and (decouvert!=None and decouvert>min-dif):
            cur = conn.cursor()
            sql = "UPDATE CompteCourant SET min_solde={} WHERE date_crea={}" % (min-dif-1, date_crea)
            cur.execute(sql)
            conn.commit()
            cur = conn.cursor()
            sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}" % (min+1, date_crea)
            cur.execute(sql)
            return True
    # CompteRevolving
    if type == 'CompteRevolving':
        compteRevolving = date_crea
        cur = conn.cursor()
        sql = "SELECT balance,montant_min FROM CompteRevolving WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance, min = cur.fetchone()
        dif = balance-montant
        if dif>min:     # si il y'a assez de fonds
            cur = conn.cursor()
            sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}" % (dif, date_crea)
            cur.execute(sql)
            return True
    # CompteEpargne
    if type == 'CompteEpargne':
        compteEpargne = date_crea
        cur = conn.cursor()
        sql = "SELECT balance,solde_min_const FROM CompteEpargne WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance, min = cur.fetchone()
        dif = balance-montant
        if dif>min:     # si il y'a assez de fonds
            cur = conn.cursor()
            sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}" % (dif, date_crea)
            cur.execute(sql)
            return True
    return False



# on dépose de l'argent (CreditGuichet, DepotCheque)
def crediter(date_crea, motif, type, montant):
    # CompteCourant
    if type == 'CompteCourant':
        cur = conn.cursor()
        sql = "SELECT balance,max_solde FROM CompteCourant WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance, max = cur.fetchone()
        new_solde = balance + montant
        if balance+montant>max:     # si il y'a assez de fonds
            cur = conn.cursor()
            sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}" % (new_solde,date_crea)
            cur.execute(sql)
            return True
    # CompteRevolving
    if type == 'CompteRevolving':
        cur = conn.cursor()
        sql = "SELECT balance FROM CompteRevolving WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance = cur.fetchone()[0]
        new_solde = balance + montant
        cur = conn.cursor()
        sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}" % (new_solde, date_crea)
        cur.execute(sql)
        return True
    # CompteEpargne
    if type == 'CompteEpargne':
        compteEpargne = date_crea
        cur = conn.cursor()
        sql = "SELECT balance FROM CompteEpargne WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance = cur.fetchone()[0]
        new_solde = balance + montant
        cur = conn.cursor()
        sql = "UPDATE CompteEpargne SET balance={} WHERE date_crea={}" % (new_solde, date_crea)
        cur.execute(sql)
        return True
    return False
    
    

def deplacer(date_crea, motif, type, montant):
    if motif in ['1', '3', '5', '6']:
        debiter(date_crea, motif, type, -montant)
    if motif in ['2', '4']:
        crediter(date_crea, motif, type, montant)
        
        
ops = {
"1": "DebitGuichet",
"2": "CreditGuichet",
"3": "Virement",
"4": "DepotCheque",
"5": "EmissionCheque",
"6": "CarteBleue"
}



def add_operation(conn):
    # Ajouter une opération
    print("\n ## Ajouter une opération \n")
    id = int(input(" id : "))
    montant = float(input(" montant de l'opération (>0) : "))
    date = quote(input(" date d'opération aaaa-mm-jj = "))
    print(" état par défaut = non traité ")
    etat = "non traité"
    client = int(input(" tel du client : "))
    date_crea = quote(input(" date de création aaaa-mm-jj hh:mm:ss = "))
    try:
        cur = conn.cursor()
        sql = "INSERT INTO operation VALUES ({},{},{},{},{},{})".format(id,montant,date,etat,client,date_crea)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
        
    # Ajouter le type de l'opération
    print(" 1. Pour faire un retrait au guichet")
    print(" 2. Pour faire un dépôt au guichet")
    print(" 3. Pour faire virement")
    print(" 4. Pour déposer de chèque")
    print(" 5. Pour émettre un chèque")
    print(" 6. Pour faire un retrait avec carte Bleue \n")
    
    num = input(" choix : ")
    if constraint_type_account(date,date_crea,num,id) and restriction_type_operation(date_crea,num):
        try:
            cur = conn.cursor()
            sql = "INSERT INTO {} VALUES ({})".format(ops.get(num),id)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)
        


########## Afficher ##########


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
            type = type_compte(quote(res[0]))
            print(" - date création: {} | statut: {} | type: {} ".format(res[0],res[1],type))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# afficher tous les propriétaires
def display_all_owner(conn):
    print("\n ## afficher tous les propriétaires  \n")
    try:
        cur = conn.cursor()
        sql = "SELECT tel, nom, date_crea FROM Asso_Compte_Client NATURAL JOIN Client"
        cur.execute(sql)
        res = cur.fetchone()
        if res==None:
            print("/!\ AUCUN PROPRIÉTAIRE /!\\")
        while res:
            type = type_compte(quote(res[2]))
            print(" - tel: {} | nom: {} | date création: {} | type: {}".format(res[0],res[1],res[2],type))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)


try:
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
except psycopg2.ProgrammingError as e:
    print("message système : ", e)
except psycopg2.OperationalError as e:
    print("message système : ", e)



# afficher toutes les opération
def display_all_operation(conn):
    print("\n ## afficher tous les propriétaires  \n")
    try:
        cur = conn.cursor()
        sql = "SELECT id, montant, date, etat, client, date_crea FROM Operation"
        cur.execute(sql)
        res = cur.fetchone()
        if res==None:
            print("/!\ AUCUNE OPÉRATION /!\\")
        while res:
            type = type_operation(res[0])
            print(" - id: {} | type: {} | montant: {} | date: {} | etat: {} | client: {} | date_crea: {} ".format(res[0],type,res[1],res[2],res[3],res[4],res[5]))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



########## MENU ##########

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
        save_csv(chemin)
    if choice=='2':
        add_account(conn)
        conn.commit()
        save_csv(chemin)
    if choice=='3':
        add_owner(conn)
        conn.commit()
        save_csv(chemin)
    if choice=='4':
        add_operation(conn)
        conn.commit()
        save_csv(chemin)
    if choice=='6':
        display_all_customer(conn)
    if choice=='7':
        display_all_account(conn)
    if choice=='8':
        display_all_owner(conn)
    if choice=='9':
        display_all_operation(conn)
    if choice=='10':
        date = quote(input("\n date de création aaaa-mm-jj hh:mm = "))
        cur = conn.cursor()
        sql = "SELECT balance FROM compteepargne WHERE date_crea={} UNION SELECT balance FROM compterevolving WHERE date_crea={} UNION SELECT balance FROM comptecourant WHERE date_crea={}".format(date,date,date)
        cur.execute(sql)
        res = cur.fetchone()
        print("\n## Le compte crée {} a {}€ de balance".format(date, res[0]))
    if choice=='11':
        client = quote(input("\n id(tel) du client : "))
        cur = conn.cursor()
        sql = "SELECT count(id) FROM Operation NATURAL JOIN EmissionCheque WHERE client={}".format(client)
        cur.execute(sql)
        res = cur.fetchone()
        print("\n## Le client {} a émis {} chèques ".format(client, res[0]))

# Clôture de la connexion
conn.close()


