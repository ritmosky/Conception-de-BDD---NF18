CREATE TABLE Dessert_site (
bus_ligne INT),
bus_horaire TIME,
site VARCHAR(10),

PRIMARY KEY bus_ligne, bus_horaire, site,

FOREIGN KEY bus_ligne REFERENCES ArretDeBus,
FOREIGN KEY bus_horaire REFERENCES ArretDeBus,
FOREIGN KEY site REFERENCES SiteTouristique
);



CREATE TABLE Dessert_hotel (
bus_ligne INT,
bus_horaire TIME,
hotel VARCHAR(10),

PRIMARY KEY bus_ligne, bus_horaire, hotel,

FOREIGN KEY bus_ligne REFERENCES ArretDeBus,
FOREIGN KEY bus_horaire REFERENCES ArretDeBus,
FOREIGN KEY hotel REFERENCES Hotel
);




CREATE TABLE ActivitéParSite (
site VARCHAR(10),
activite VARCHAR(10),

PRIMARY KEY site, activite,

FOREIGN KEY bus_ligne REFERENCES ArretDeBus,
FOREIGN KEY activite REFERENCES Activite
);

