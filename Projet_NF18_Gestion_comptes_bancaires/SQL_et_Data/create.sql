CREATE TABLE Client (
    tel INTEGER, 
    nom VARCHAR(25) NOT NULL, 
    adresse VARCHAR(150) NOT NULL, 

    PRIMARY KEY (tel)
);   


CREATE TABLE Compte (
    date_crea TIMESTAMP, 
    statut VARCHAR(8) NOT NULL,

    CHECK (statut='ouvert' OR statut='bloqué' OR statut='fermé') ,

    PRIMARY KEY (date_crea)
);


CREATE TABLE Asso_Compte_Client (
    tel INTEGER,
    date_crea TIMESTAMP,

    PRIMARY KEY (tel, date_crea),
    FOREIGN KEY (tel) REFERENCES Client(tel),
    FOREIGN KEY (date_crea) REFERENCES Compte(date_crea)
);


CREATE TABLE CompteEpargne (
    date_crea TIMESTAMP,
    balance FLOAT NOT NULL,
    solde_min_const FLOAT NOT NULL,

    CHECK (balance > solde_min_const),

    PRIMARY KEY(date_crea),
    FOREIGN KEY (date_crea) REFERENCES Compte(date_crea)
);


CREATE TABLE CompteRevolving (
    date_crea TIMESTAMP,
    balance FLOAT NOT NULL,
    taux_j FLOAT NOT NULL,
    montant_min FLOAT NOT NULL,

    CHECK (taux_j > 0 AND taux_j < 1),
    CHECK (montant_min < 0),
    CHECK (montant_min < balance),
    CHECK (balance < 0),
    
    PRIMARY KEY(date_crea),
    FOREIGN KEY (date_crea) REFERENCES Compte(date_crea)
);


CREATE TABLE CompteCourant (
    date_crea TIMESTAMP,
    balance FLOAT NOT NULL,
    montant_decouvert_autorise FLOAT,
    max_solde FLOAT NOT NULL,
    min_solde FLOAT NOT NULL,
    date_debut_decouvert DATE,

    CHECK (balance > min_solde AND balance < max_solde),
    CHECK (max_solde > 0),
    CHECK (min_solde > 0),
    
    PRIMARY KEY(date_crea),
    FOREIGN KEY (date_crea) REFERENCES Compte(date_crea)
);


CREATE TABLE Operation (
    id INT,
    montant FLOAT NOT NULL,
    date DATE NOT NULL,
    etat VARCHAR(11) NOT NULL,
    client INT NOT NULL,
    date_crea TIMESTAMP NOT NULL,

    CHECK (etat='traité' OR etat='non traité'),
    CHECK (montant > 0),

    PRIMARY KEY(id),
    FOREIGN KEY (client) REFERENCES Client(tel),
    FOREIGN KEY (date_crea) REFERENCES Compte(date_crea)
);


CREATE TABLE DebitGuichet (
    id  INT,

    PRIMARY KEY(id),
    FOREIGN KEY (id) REFERENCES Operation(id)
);


CREATE TABLE CreditGuichet (
    id  INT,

    PRIMARY KEY(id),
    FOREIGN KEY (id) REFERENCES Operation(id)
);


CREATE TABLE Virement (
    id  INT,

    PRIMARY KEY(id),
    FOREIGN KEY (id) REFERENCES Operation(id)
);


CREATE TABLE DepotCheque (
    id  INT,

    PRIMARY KEY(id),
    FOREIGN KEY (id) REFERENCES Operation(id)
);


CREATE TABLE EmissionCheque (
    id  INT,

    PRIMARY KEY(id),
    FOREIGN KEY (id) REFERENCES Operation(id)
);


CREATE TABLE CarteBleu (
    id  INT,

    PRIMARY KEY(id),
    FOREIGN KEY (id) REFERENCES Operation(id)
);
