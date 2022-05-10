
\i documents/school/utc/sem02/nf18/nf18/Projet_NF18_Gestion_comptes_bancaires/SQL_et_Data/drop.sql

\i documents/school/utc/sem02/nf18/nf18/Projet_NF18_Gestion_comptes_bancaires/SQL_et_Data/create.sql

\i documents/school/utc/sem02/nf18/nf18/Projet_NF18_Gestion_comptes_bancaires/SQL_et_Data/insert.sql



-- Afficher tous les clients
SELECT c.tel, c.nom, c.adresse, count(c.tel) nbCompte FROM Client c NATURAL JOIN Asso_Compte_Client a group by c.tel;


-- Afficher tous les comptes
SELECT date_crea, statut, 'Epargne' as type FROM Compte NATURAL JOIN CompteEpargne
UNION
SELECT date_crea, statut, 'Revolving' as type FROM Compte NATURAL JOIN CompteRevolving
UNION
SELECT date_crea, statut, 'Courant' as type FROM Compte NATURAL JOIN CompteCourant;


-- Afficher tous les propriétaires
SELECT tel, nom, date_crea FROM Asso_Compte_Client NATURAL JOIN Client;

-- Afficher tous les propriétaires
SELECT id, montant, date, etat, client, date_crea FROM Operation;



