CREATE TABLE ArretDeBus (
    ligne INT,
    horaire TIME,
    PRIMARY KEY (ligne,horaire)
);

CREATE TABLE SiteTouristique (
    nom VARCHAR(128),
    anciennete INT,
    PRIMARY KEY (nom)
);

CREATE TABLE Hotel (
    nom VARCHAR(128),
    adresse VARCHAR(128),
    codePostal VARCHAR(10),
    ville VARCHAR(128),
    etoiles INT,
    PRIMARY KEY (nom)
);

CREATE TABLE TypeCuisine (
    label VARCHAR(128),
    PRIMARY KEY (label)
);

CREATE TABLE Restaurant (
    sk INT,
    nom VARCHAR(128),
    telephone VARCHAR(10),
    type_cuisine VARCHAR(128),
    hotel VARCHAR(128),
    site VARCHAR(128),
    
    PRIMARY KEY (sk),
    FOREIGN KEY (type_cuisine) REFERENCES TypeCuisine (label),
    FOREIGN KEY (hotel) REFERENCES Hotel (nom),
    FOREIGN KEY (site) REFERENCES SiteTouristique (nom),
    
    CHECK (nom!=NULL),
    UNIQUE (telephone),
    CHECK (type_cuisine!=NULL)
);

CREATE TABLE Activite (
    nom VARCHAR(128),
    PRIMARY KEY (nom)
);

CREATE TABLE ActiviteParSite (
    site VARCHAR(128),
    activite VARCHAR(128),
    
    PRIMARY KEY (site, activite),
    FOREIGN KEY (site) REFERENCES SiteTouristique (nom),
    FOREIGN KEY (activite) REFERENCES Activite (nom)
);

CREATE TABLE Dessert_hotel (
    bus_ligne INT,
    bus_horaire TIME,
    hotel VARCHAR(128),

    PRIMARY KEY (bus_ligne, bus_horaire, hotel),
    
    FOREIGN KEY (bus_ligne) REFERENCES ArretDeBus (ligne),
    FOREIGN KEY (bus_horaire) REFERENCES ArretDeBus (horaire),
    FOREIGN KEY (hotel) REFERENCES Hotel (nom)
);

CREATE TABLE Dessert_site (
    bus_ligne INT,
    bus_horaire TIME,
    site VARCHAR(128),
    
    PRIMARY KEY (bus_ligne, bus_horaire, site),
    
    FOREIGN KEY (bus_ligne) REFERENCES ArretDeBus (ligne),
    FOREIGN KEY (bus_horaire) REFERENCES ArretDeBus (horaire),
    FOREIGN KEY (site) REFERENCES SiteTouristique (nom)
);

