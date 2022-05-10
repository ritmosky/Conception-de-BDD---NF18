

from constraintsEtDivers import *

########## OPERATIONS ##########


# on retire de l'argent (DebitGuichet, Virement, EmissionCheque, CarteBleue)
def debiter(date_crea, motif, montant, conn):
    # CompteCourant
    if type_compte(date_crea, conn) == 'CompteCourant':
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
    if type_compte(date_crea, conn) == 'CompteRevolving':
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
    if type_compte(date_crea, conn) == 'CompteEpargne':
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
def crediter(date_crea, motif, montant, conn):
    # CompteCourant
    if type_compte(date_crea, conn) == 'CompteCourant':
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
    if type_compte(date_crea, conn) == 'CompteRevolving' or type_compte(date_crea, conn) == 'CompteEpargne':
        cur = conn.cursor()
        sql = "SELECT balance FROM {} WHERE date_crea={}".format(type_compte(date_crea, conn),date_crea)
        cur.execute(sql)
        balance = cur.fetchone()[0]
        balance = float(balance)
        balance += montant
        sql = "UPDATE CompteCourant SET balance={} WHERE date_crea={}".format(balance, date_crea)
        cur.execute(sql)
        return True
    return False


# hanger la valeur de l'état
def deplacer(date_crea, id, motif, montant, conn):
    etat = quote('traité')
    effectue = False
    type_o = type_operation(id,conn)
    if motif in ['1', '3', '5', '6']:
        debiter(date_crea, motif, montant, conn)
        effectue = True
    elif motif in ['2', '4']:
        crediter(date_crea, motif, montant, conn)
        effectue = True
    if effectue==True:
        cur = conn.cursor()
        sql = "UPDATE Operation SET etat={} WHERE date_crea={} AND id={}".format(etat, date_crea,id)
        cur.execute(sql)


# les intérets sont ajoutés journalièrement à la balance du compteRevolving
def balance_avec_interet_revolving(date_crea, date, conn):
    if type_compte(date_crea, conn)!='CompteRevolving':
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