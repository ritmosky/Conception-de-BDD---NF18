CREATE TABLE Client (
    tel INTEGER, 
    nom VARCHAR(25) NOT NULL, 
    adresse : VARCHAR(150) NOT NULL, 
    PRIMARY KEY (tel)
);   

CREATE TABLE Compte (
    date_crea DATETIME, 
    balance FLOAT NOT NULL, 
    statut VARCHAR(6) CHECK (statut='ouvert' OR statut='bloqué' OR statut='fermé') NOT NULL,
    PRIMARY KEY (date_crea)
);

CREATE TABLE Asso_Compte_Client (
    tel INTEGER,
    date_crea DATETIME,
    FOREIGN KEY (tel, date_crea) REFERENCES Client(tel), Compte(date_crea)
);
