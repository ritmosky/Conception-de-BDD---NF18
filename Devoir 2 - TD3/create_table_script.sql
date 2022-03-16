CREATE TABLE Ligne (
    num INTEGER PRIMARY KEY,
    km INTEGER
);

CREATE TABLE Station (
    num INTEGER PRIMARY KEY,
    nom VARCHAR(255),
    adresse VARCHAR(255)
);

CREATE TABLE Arret (
    ligne INTEGER,
    station INTEGER,
    rang INTEGER,
    FOREIGN KEY (ligne) REFERENCES Ligne(num),
    FOREIGN KEY (station) REFERENCES Station(num)
);

CREATE TABLE Conducteur (
    matricule VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50)
);


CREATE TABLE Bus (
    immat VARCHAR(10),
    type VARCHAR(10),
    kilometrage NUMERIC(7),
    matricule VARCHAR(10),

    CHECK (type = 'Soufflets' or type='Normaux' or type='Reduits'),
    PRIMARY KEY (immat),
    FOREIGN KEY (matricule) REFERENCES Conducteur (matricule)
);


CREATE TABLE Trajet (
    immat VARCHAR(10),
    ligne INT,
    nbtrajets NUMERIC(2),

    PRIMARY KEY (ligne, immat),
    FOREIGN KEY (ligne) REFERENCES Ligne (num),
    FOREIGN KEY (immat) REFERENCES Bus (immat)
);
