CREATE TABLE Client (
    tel INTEGER, 
    nom VARCHAR(25), 
    adresse : VARCHAR(150), 
    PRIMARY KEY(tel)
);   

CREATE TABLE Compte (
    date_crea DATETIME, 
    balance FLOAT, 
    statut VARCHAR(6) CHECK (statut='ouvert' OR statut='bloqué' OR statut='fermé'),
    PRIMARY KEY(date_crea)
);
