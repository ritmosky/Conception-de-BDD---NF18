########## FONCTIONS INTERMEDIAIRES ##########

def quote(s):
    if s:
        return "\'%s\'" % s
    else:
        return 'NULL'


def type_compte(date_crea, conn):
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



def type_operation(id, conn):
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