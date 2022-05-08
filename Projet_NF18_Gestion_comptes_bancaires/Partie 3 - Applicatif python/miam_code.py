########## CONNEXION ##########


# bibliothèque
# exécuter => pip install package_name pour installer un package
import psycopg2
import csv
import glob
import os.path


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


########## INITIALIZATION ##########


# '/Users/taoufiq/Documents/school/Utc/sem02/NF18/nf18/Projet_NF18_Gestion_comptes_bancaires/SQL_et_Data'
path = input('chemin du dossier où stocker les données(.../.../dossier) : ')


# create tables ->
def create_table():
    f = open(path+'/create.sql', 'r')
    cur = conn.cursor()
    sql_create = " ".join(f.readlines())
    cur.execute(sql_create)
    conn.commit()
    print(" ==> création des tables effectuée ! <== ")


# /!\/!\/!\ drop tables /!\/!\/!\
def drop_table():
    f = open(path+'/drop.sql', 'r')
    cur = conn.cursor()
    sql_drop = " ".join(f.readlines())
    cur.execute(sql_drop)
    conn.commit()
    print(" ==> suppression des tables effectuée ! <== ")


# pour charger tous les fichiers csv dans le dossier
# /!\ il faut renommer les fichiers csv selon le nom des tables en minuscule /!\
classes = {
1: 'client',
2: 'compte',
3: 'asso_compte_client',
4: 'compteepargne',
5: 'compterevolving',
6: 'comptecourant',
7: 'operation',
8: 'debitguichet',
9: 'creditguichet',
10: 'depotcheque',
11: 'emissioncheque',
12: 'cartebleu',
13: 'virement'
}


def import_data():
    files = []
    for file in glob.glob(path + "/*.csv"):
        #print(file)
        files.append(file)

    for c in list(classes.values()):
        file = path + '/' + c + ".csv"  # remplacer '/' par '\\' sur windows
        if file in files:
            with open(file, 'r') as f:
                cur = conn.cursor()
                next(f)     # sauter l'en-tête
                table_name = file[len(path)+1:file.find('.csv')]
                cur.copy_from(f, table_name, sep=';', null='')
                conn.commit()
    print(" ==> importation des données effectuée ! <== ")


########## Enregistrer les tables dans un fichier CSV  ##########


# dico des opérations
ops = {
"1": "DebitGuichet",
"2": "CreditGuichet",
"3": "Virement",
"4": "DepotCheque",
"5": "EmissionCheque",
"6": "CarteBleu"
}


# dictionnaire des attributs des différentes tables
dico = {
'Client_col' : ["tel", "nom", "adresse"],
'Compte_col' : ['date_crea', 'statut'],
'Asso_Compte_Client_col' : ['tel', 'date_crea'],
'CompteEpargne_col' : ['date_crea', 'balance', 'solde_min_const'],
'CompteRevolving_col' : ['date_crea', 'balance', 'taux_j', 'montant_min'],
'CompteCourant_col' : ['date_crea', 'balance', 'montant_decouvert_autorise','max_solde' ,'min_solde', 'date_debut_decouvert'],
'Operation_col' : ['id', 'montant', 'date', 'etat', 'client', 'date_crea'],
'DebitGuichet_col' : ['id'],
'CreditGuichet_col' : ['id'],
'Virement_col' : ['id'],
'DepotCheque_col' : ['id'],
'EmissionCheque_col' : ['id'],
'CarteBleu_col' : ['id']
}



def save_csv(path):
    #cols, table = recognize_table()
    for key,cols in dico.items():
        table = key[:key.find('_col')]
        cur = conn.cursor()
        sql = "SELECT * FROM {}".format(table)
        cur.execute(sql)
        line = cur.fetchone()
    #Ouverture du fichier CSV en écriture
        with open('{}/{}.csv'.format(path, table.lower()),'w',newline='') as f:
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
                return type
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



# les intérets sont ajoutés journalièrement à la balance du compteRevolving
def balance_avec_interet_revolving(date_crea, date):
    if type_compte(date_crea)!='CompteRevolving':
        return '\n /!\ {} n\'est pas une compte de Revolving /!\ '.format(date_crea)
    if date < date_crea:
        return False
    cur = conn.cursor()
    sql = "SELECT EXTRACT(DAY FROM TO_TIMESTAMP({}, 'YYYY-MM-DD') - TO_TIMESTAMP({}, 'YYYY-MM-DD'))".format(date,date_crea)
    cur.execute(sql)
    nb_jr = int(cur.fetchone()[0])        # le nombre de jours écoulés
    sql = "SELECT balance, taux_j FROM CompteRevolving WHERE date_crea={}".format(date_crea)
    cur.execute(sql)
    balance, taux = cur.fetchone()
    new_balance = pow(taux+1, nb_jr) * balance
    return new_balance




def add_account_type(date_crea, type_c, c):
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
    print("\n ## Ajouter un compte \n")
    date_crea = quote(input(" date de création aaaa-mm-jj hh:mm:ss = "))
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

    if constraint_type_account(date_crea, type_c):
        add_account_type(date_crea, type_c, c)
    else:
        print("\n /!\ Ce compte a déjà un type /!\ ")



########## OPERATIONS/CONTRAINTES_OPERATIONS ##########


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

def constraint_type_operation(date, date_crea, motif, id):
    types = list(ops.values())
    try:
        # un compte ne peut effectuer plusieurs opérations en même temps
        cur = conn.cursor()
        sql = "SELECT COUNT(*) FROM Operation WHERE date={} AND date_crea={}".format(date,date_crea)
        cur.execute(sql)
        res = cur.fetchone()
        if res[0]>1:
            return False

        types.remove(ops.get(motif))
        for o in types:   # exclusivités des opérations
            sql = "SELECT COUNT(*) FROM {} WHERE id={}".format(o, id)
            cur.execute(sql)
            res = cur.fetchone()
            if res[0]!=0 and res!=None:
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
    possible = True
    mssg = ''
    # compte épargne -> opérations au guichet et virements
    if type_compte(date_crea) == 'CompteEpargne' and motif not in ['1','2','3']:
        possible = False
        mssg += '- /!\ compte epargne ne permet pas cette opération /!\ \n'.format(ops.get(motif))
    try:
        # compte fermé -> aucune opération
        cur = conn.cursor()
        sql = "SELECT statut FROM Compte WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        statut = cur.fetchone()
        if statut=='fermé':
            possible = False
            mssg += '- /!\ compte fermé ne permet aucune opération /!\ '
        # compte bloqué -> debits et crédits
        if statut=='bloqué' and motif not in ['1','2']:
            possible = False
            mssg += '- /!\ compte bloqué ne permet pas de {} /!\\n'.format(ops.get(motif))
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
    return possible, mssg



# vérifie si le compte appartient au client
def is_owner(tel, date_crea):
    mssg = ''
    possible = True
    try:
        cur = conn.cursor()
        sql = "SELECT count(*) FROM Asso_Compte_Client WHERE date_crea={} AND tel={}".format(date_crea, tel)
        cur.execute(sql)
        res = cur.fetchone()[0]
        if res == 0 :
            possible = False
            mssg += ' ==> /!\ le compte {} n\'appartient pas au client {} /!\ <=='.format(date_crea,tel)
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)
    return possible, mssg


########## OPERATIONS ##########



# on retire de l'argent (DebitGuichet, Virement, EmissionCheque, CarteBleue)
def debiter(date_crea, motif, montant):
    # CompteCourant
    if type_compte(date_crea) == 'CompteCourant':
        cur = conn.cursor()
        sql = "SELECT balance,min_solde,montant_decouvert_autorise FROM CompteCourant WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance, min, decouvert = cur.fetchone()
        balance = float(balance)
        min = float(min)
        decouvert = float(decouvert)
        dif = balance-montant
        if dif>min:     # si il y'a assez de fonds
            sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}".format(dif, date_crea)
            cur.execute(sql)
            return True
        # pour utiliser le découvert, nous baissons la valeur min_solde
        if dif<=min and (decouvert!=None and decouvert>min-dif):
            sql = "UPDATE CompteCourant SET min_solde={} WHERE date_crea={}".format(min-dif-1, date_crea)
            cur.execute(sql)
            conn.commit()
            sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}".format(min+1, date_crea)
            cur.execute(sql)
            return True
    # CompteRevolving
    if type_compte(date_crea) == 'CompteRevolving':
        cur = conn.cursor()
        sql = "SELECT balance, montant_min FROM CompteRevolving WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance, min = cur.fetchone()
        balance = float(balance)
        min = float(min)
        dif = balance-montant
        if dif>min:     # si il y'a assez de fonds
            sql = "UPDATE CompteRevolving SET balance={} WHERE date_crea={}".format(dif, date_crea)
            cur.execute(sql)
            return True
    # CompteEpargne
    if type_compte(date_crea) == 'CompteEpargne':
        cur = conn.cursor()
        sql = "SELECT balance,solde_min_const FROM CompteEpargne WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance, min = cur.fetchone()
        balance = float(balance)
        min = float(min)
        dif = balance-montant
        if dif>min:     # si il y'a assez de fonds
            sql = "UPDATE CompteEpargne SET balance={} WHERE date_crea={}".format(dif, date_crea)
            cur.execute(sql)
            return True
    return False



# on dépose de l'argent (CreditGuichet, DepotCheque)
def crediter(date_crea, motif, montant):
    # CompteCourant
    if type_compte(date_crea) == 'CompteCourant':
        cur = conn.cursor()
        sql = "SELECT balance,max_solde FROM CompteCourant WHERE date_crea={}".format(date_crea)
        cur.execute(sql)
        balance,  = cur.fetchone()
        balance = float(balance)
        max = float(max)
        balance += montant
        if balance+montant>max:     # si il y'a assez de fonds
            sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}".format(balance,date_crea)
            cur.execute(sql)
            return True
    # CompteRevolving et CompteEpargne
    if type_compte(date_crea) == 'CompteRevolving' or type_compte(date_crea) == 'CompteEpargne':
        cur = conn.cursor()
        sql = "SELECT balance FROM {} WHERE date_crea={}".format(type_compte(date_crea),date_crea)
        cur.execute(sql)
        balance = cur.fetchone()[0]
        balance = float(balance)
        balance += montant
        sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}".format(balance, date_crea)
        cur.execute(sql)
        return True
    return False



def deplacer(date_crea, id, motif, montant):
    etat = quote('traité')
    effectue = False
    type_o = type_operation(id)
    if motif in ['1', '3', '5', '6']:
        debiter(date_crea, motif, montant)
        effectue = True
    if motif in ['2', '4']:
        crediter(date_crea, motif, montant)
        effectue = True
    if effectue==True:
        cur = conn.cursor()
        sql = "UPDATE Operation SET etat={} WHERE date_crea={} AND id={}".format(etat, date_crea,id)
        cur.execute(sql)



def add_operation_type(date, date_crea, id, montant):
    # Ajouter le type de l'opération
    print(" ------------------ ")
    print(" 1. Pour faire un retrait au guichet")
    print(" 2. Pour faire un dépôt au guichet")
    print(" 3. Pour faire virement")
    print(" 4. Pour déposer de chèque")
    print(" 5. Pour émettre un chèque")
    print(" 6. Pour faire un retrait avec carte Bleue \n")
    num = input(" choix : ")
    if constraint_type_operation(date,date_crea,num,id) and restriction_type_operation(date_crea,num)[0]: # si opération possible
        print('opération possible')
        try:
            cur = conn.cursor()
            sql = "INSERT INTO {} VALUES ({})".format(ops.get(num),id)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)

    else :  # si opération impossible
        print('\n ==> /!\ opération impossible /!\ <==  car :')
        print(restriction_type_operation(date_crea,num)[1])




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
    if is_owner(client,date_crea)[0]:  # compte appartient au client
        try:
            cur = conn.cursor()
            sql = "INSERT INTO Operation VALUES ({},{},{},{},{},{})".format(id,montant,date,etat,client,date_crea)
            cur.execute(sql)
        except psycopg2.IntegrityError as e:
            print("Message système : ",e)

        type_account = 'Compte' + type_compte(date_crea).capitalize()
        # Ajouter le type de l'opération
        add_operation_type(date, date_crea, id, montant)
        deplacer(date_crea, id, motif, montant)

    else: # compte n'appartient pas au client
        print(is_owner(client,date_crea)[1])



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
            type = type_operation(res[0])
            print(" - id: {} | type: {} | montant: {} | date: {} | etat: {} | client: {} | date_crea: {} ".format(res[0],type,res[1],res[2],res[3],res[4],res[5]))
            res = cur.fetchone()
    except psycopg2.IntegrityError as e:
        print("Message système : ",e)



########## MENU ##########


try:
    create_table()  # pour créer les tables
    import_data()   # pour importer des données csv
except psycopg2.errors.InFailedSqlTransaction as e:
    print("message système : ", e)
except psycopg2.errors.DuplicateTable as e:
    print("message système : ", e)


#drop_table()   # pour supprimer les tables



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
        save_csv(path)
    if choice=='2':
        add_account(conn)
        conn.commit()
        save_csv(path)
    if choice=='3':
        add_owner(conn)
        conn.commit()
        save_csv(path)
    if choice=='4':
        add_operation(conn)
        conn.commit()
        save_csv(path)
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


