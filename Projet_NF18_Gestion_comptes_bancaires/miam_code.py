
"""
- effectuer des requêtes avec un fichier sql
\i documents/school/utc/sem02/nf18/projet_nf18/drop.sql
\i documents/school/utc/sem02/nf18/projet_nf18/create.sql;

- pour importer un fichier csv
\cd documents/school/utc/sem02/nf18/projet_nf18

\copy Client (tel, nom, adresse) FROM 'client.csv' WITH CSV HEADER DELIMITER  ';' QUOTE '"'
"""

########## CONNEXION ##########


# bibliothèque
import psycopg2


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


choice = '1'
while choice!='0':
    connect()
    print("\n ------------ MENU -----------\n")
    print(" 1. Ajouter un client")
    print(" 2. Ajouter un compte")
    print(" 3. Ajouter un propriétaire à un compte")
    print(" 4. Ajouter un type de compte")
    print(" 5. Afficher tous les clients")
    print(" 6. Afficher tous les comptes")
    print(" 7. Afficher tous les propriétaires")
    print("\n -----------------------------\n")

    choice = input(" choix : ")

    if choice=='1':
        add_customer(conn)
    if choice=='2':
        add_account(conn)
    if choice=='3':
        add_owner(conn)
    if choice=='4':
        add_account_type(conn)
    if choice=='5':
        display_all_customer(conn)
    if choice=='6':
        display_all_account(conn)
    if choice=='7':
        display_all_owner(conn)
    print("\n ----------- FIN ----------\n")


########## Contraintes ##########
"""
PROJECTION(Compte, date_crea) = PROJECTION(CompteCourant, date_crea) UNION
    PROJECTION(CompteRevolving, date_crea) UNION PROJECTION(CompteEpargne, date_crea)
----> on verifie à chaque insertion si date_crea de la classe fille n'est pas présente dans les autres filles sinon execption


PROJECTION(Operation, id) = PROJECTION(CarteBleu, id) UNION PROJECTION(EmissionCheque, id)
    UNION PROJECTION(DepotCheque, id) UNION PROJECTION(Virement, id) UNION
    PROJECTION(CreditGuichet, id) UNION PROJECTION(DebitGuichet, id)
----> on verifie que id de la classe fille se trouve dans Compte et n'est pas dans les autres filles sinon execption
"""

# retourne True si la contrainte est respectée, sinon False
def constraint_type_account(date, a_type):
    types = ["CompteCourant", "CompteRevolving", "CompteEpargne"]
    try:
        types.remove(a_type)
        for c in types:
            sql = "SELECT COUNT(*) FROM %s WHERE date_crea=%s" % (c, date)
            cur.execute(sql)
            res = sql.fetchone
            if res[0]!=0 and res!=None:
                return False
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
    return True


# retourne True si la contrainte est respectée, sinon False
def constraint_operation(id, o_type):
    types = ["DebitGuichet", "CreditGuichet", "Virement", "DepotCheque", "EmissionCheque", "CarteBleu"]
    try:
        types.remove(o_type)
        for o in types:
            sql = "SELECT COUNT(*) FROM %s WHERE id=%s" % (o, id)
            cur.execute(sql)
            res = sql.fetchone
            if res[0]!=0 and res!=None:
                return False
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
    return True


# retourne True si la contrainte est respectée, sinon False
def constraint_type_operation(date, a_type):
    return True


########## Ajouter ##########


def quote(s):
    if s:
        return "\'%s\'" % s
    else:
        return 'NULL'


# ajouter un client
def add_customer(conn):
    print("\n ## Ajouter un client \n")
    tel = int(input(" tel : "))
    nom = quote(input(" nom : "))
    adresse = quote(input(" adresse : "))

    try:
        cur = conn.cursor()
        sql = "INSERT INTO Client(tel,nom,adresse) VALUES (%i,%s,%s)" % (tel, nom, adresse)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# ajouter un compte
def add_account(conn):
    print("\n ## Ajouter un compte \n")
    date_crea = quote(input(" date de création aaaa-mm-jj hh:mm = "))
    statut = quote(input(" statut(ouvert,bloqué ou fermé) : "))

    try:
        cur = conn.cursor()
        sql = "INSERT INTO Compte(date_crea,statut) VALUES (%s,%s)" % (date_crea, statut)
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
        sql = "INSERT INTO Asso_Compte_Client(tel,date_crea) VALUES (%s,%s)" % (tel,date_crea)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# ajouter un type de compte
def account_type():
    c = '0'
    while c not in ['1', '2', '3'] :
        print(" 1. Pour un Compte Epargne")
        print(" 2. Pour un Compte Revolving")
        print(" 3. Pour un Compte Courant")
        c = input(" choix : ")
    print("... {} ... ".format(c), end=' ==> ')
    if c=='1':
        return "CompteEpargne"
    if c=='2':
        return "CompteRevolving"
    if c=='3':
        return "CompteCourant"



# Compte Epargne
def Epargne(a_type, date_crea):
    print("\n ## Ajouter un compte Epargne\n")
    solde_min_const = float(input(" solde minimum statuaire (>0) : "))
    balance = float(input(" balance (>solde_min_const): "))
    try:
        cur = conn.cursor()
        sql = "INSERT INTO %s(date_crea, balance, solde_min_const) VALUES (%s, %f, %f)" % (a_type, date_crea, balance, solde_min_const)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# Compte Revolving
def Revolving(a_type, date_crea):
    print("\n ## Ajouter un compte Revolving\n")
    taux_j = float(input(" taux journalier entre ]0;1[ : "))
    solde_min = float(input(" solde minimum (<0) : "))
    balance = float(input(" balance entre [solde min;0] : "))
    try:
        cur = conn.cursor()
        sql = "INSERT INTO %s(date_crea, balance, taux_j, montant_min) VALUES (%s, %f, %f, %f)" % (a_type, date_crea, balance, taux_j, montant_min)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# Compte Courant
def Courant(a_type, date_crea):
    print("\n ## Ajouter un compte Courant\n")
    dec_autorise = quote(input(" montant du découvert autorisé ou sinon Null : "))
    max_solde = float(input(" solde maximum (>0) : "))
    min_solde = float(input(" solde minimum (>0) : "))
    balance = float(input(" balance entre [solde min, solde max] : "))
    debut_decouvert = quote(input(" début du découvert aaaa-mm-jj hh:mm ou sinon Null = "))
    try:
        cur = conn.cursor()
        sql = "INSERT INTO %s(date_crea, balance, montant_decouvert_autorise, max_solde, min_solde, date_debut_decouvert) VALUES (%s, %f, %f, %f, %f, %s)" % (a_type, date_crea, balance, dec_autorise, max_solde, min_solde, debut_decouvert)
        cur.execute(sql)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



def add_account_type(conn):
    print("\n -- Ajouter un type de compte --\n")
    a_type = account_type()
    date_crea = quote(input(" date de création aaaa-mm-jj hh:mm = "))

    if a_type=="CompteEpargne":
        Epargne(a_type, date_crea)
    if a_type=="CompteRevolving":
        Revolving(a_type, date_crea)
    if a_type=="CompteCourant":
        Courant(a_type, date_crea)



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
            print(" - tel : %i | nom : %s | adresse : %s " % (res[0],res[1],res[2]))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# afficher tous les comptes
def display_all_account(conn):
    print("\n ## Afficher tous les comptes \n")
    try:
        cur = conn.cursor()
        sql = "SELECT * FROM Compte"
        cur.execute(sql)
        res = cur.fetchone()
        if res==None:
            print("/!\ AUCUN COMPTE /!\\")
        while res:
            print(" - date création : %s | statut : %s " % (res[0],res[1]))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# afficher tous les propriétaires
def display_all_owner(conn):
    print("\n ## afficher tous les propriétaires  \n")
    try:
        cur = conn.cursor()
        sql = "SELECT * FROM Asso_Compte_Client"
        cur.execute(sql)
        res = cur.fetchone()
        if res==None:
            print("/!\ AUCUN PROPRIÉTAIRE /!\\")
        while res:
            print(" - tel : %s | date création : %s" % (res[0],res[1]))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



# Clôture de la connexion
conn.close()





"""

RESTE A CODER


- Un compte ne peut pas effectuer plusleurs opérations en même temps
- compte fermé n'effectue aucune opération
- compte boque n'effectue que des debits et crédits
- deplacer() permet de retirer et deposer des fonds
- les intérets journaliers sont ajoutés à la balance du compteRevolving
- OperationPossible verifie si le statut et la balance permettent l'opération
- restreindre les opérations pour chaque type de compte
"""