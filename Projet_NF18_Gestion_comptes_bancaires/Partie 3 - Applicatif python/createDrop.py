########## INITIALIZATION ##########

# 'documents/school/utc/sem02/nf18/projet_nf18'
path = input('chemin du dossier où stocker les données(.../.../dossier) : ')

# create tables ->
def create_table(conn):
    f = open(path+'/create.sql', 'r')
    cur = conn.cursor()
    sql_create = " ".join(f.readlines())
    cur.execute(sql_create)
    conn.commit()
    print(" ==> création des tables effectuée ! <== ")


# /!\/!\/!\ drop tables /!\/!\/!\
def drop_table(conn):
    f = open(path+'/drop.sql', 'r')
    cur = conn.cursor()
    sql_drop = " ".join(f.readlines())
    cur.execute(sql_drop)
    conn.commit()
    print(" ==> suppression des tables effectuée ! <== ")