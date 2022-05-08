########## COMPTES/CONTRAINTES_COMPTES ##########
"""
----> on verifie à chaque insertion si date_crea de la classe fille n'est pas
présente dans les autres filles sinon execption
PROJECTION(Compte, date_crea) = PROJECTION(CompteCourant, date_crea) UNION
                                PROJECTION(CompteRevolving, date_crea) UNION
                                PROJECTION(CompteEpargne, date_crea)
"""


# retourne True si la contrainte est respectée, sinon False
def constraint_type_account(date_crea, a_type, conn):
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

def constraint_type_operation(date, date_crea, motif, id, conn):
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

def restriction_type_operation(date_crea, motif, conn):
    possible = True
    mssg = ''
    # compte épargne -> opérations au guichet et virements
    if type_compte(date_crea, conn) == 'CompteEpargne' and motif not in ['1','2','3']:
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
def is_owner(tel, date_crea, conn):
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