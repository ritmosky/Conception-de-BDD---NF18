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


def import_data(conn):
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



def save_csv(path, conn):
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
