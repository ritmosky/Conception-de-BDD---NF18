INSERT INTO ArretDeBus (ligne, horaire) VALUES (932, '14:15');
INSERT INTO SiteTouristique (nom, anciennete) VALUES ('monument du requin en eau douce', 200000);
INSERT INTO Hotel (nom, adresse, codePostal, ville, etoiles) VALUES ('Lebrazero', '3 rue du general de Gaulle', '64291', 'petaouchnok-les-bains', 1);
INSERT INTO TypeCuisine (label) VALUES ('belge');
INSERT INTO Restaurant (sk, nom, telephone, type_cuisine, hotel, site) VALUES (13, 'manger comme quatre', '0123456789','belge', 'Lebrazero', 'monument du requin en eau douce');
INSERT INTO Activite (nom) VALUES ('Parachutisme');
INSERT INTO ActiviteParSite (site, activite) VALUES ('monument du requin en eau douce', 'Parachutisme');
INSERT INTO Dessert_hotel (bus_ligne, bus_horaire, hotel) VALUES (932, '14:15', 'Lebrazero');
INSERT INTO Dessert_site (bus_ligne, bus_horaire, site) VALUES (932, '14:15', 'monument du requin en eau douce');

INSERT INTO ArretDeBus VALUES (16,'8:30');
INSERT INTO ArretDeBus VALUES (16,'8:35');
INSERT INTO SiteTouristique VALUES ('Lac Enghien', 200);
INSERT INTO SiteTouristique VALUES ('Gare Enghien', 100);
INSERT INTO Hotel VALUES ('Barriere','85 Rue du Général de Gaulle', '95880', 'Enghien-les-bains', 4);
INSERT INTO TypeCuisine VALUES ('Vietnamien');
INSERT INTO TypeCuisine VALUES ('Francaise');
INSERT INTO Restaurant VALUES (1,'Hanoi','0139348630','Vietnamien',NULL,'Gare Enghien');
INSERT INTO Restaurant VALUES (2, 'Fouquets', '0134121122','Francaise','Barriere','Lac Enghien');
INSERT INTO Activite VALUES ('Pedalo');
INSERT INTO ActiviteParSite VALUES ('Lac Enghien','Pedalo');
INSERT INTO Dessert_hotel VALUES (16,'8:30','Barriere');
INSERT INTO Dessert_site VALUES (16,'8:35','Gare Enghien');

INSERT INTO typecuisine (label) VALUES('Italien');
INSERT INTO SiteTouristique (nom, anciennete) VALUES ('Plage 08', 9999999);
INSERT INTO restaurant (sk, nom, telephone, type_cuisine, hotel, site) VALUES (4, 'RestoItalie', '0456782312', 'Italien', 'hot1', 'Plage 08');
INSERT INTO activite (nom) VALUES ('Scuba');
INSERT INTO activiteparsite (site, activite) VALUES ('Plage 08', 'Scuba');
INSERT INTO arretdebus (ligne, horaire) VALUES (42, '10:30:00');
INSERT INTO dessert_hotel (bus_ligne, bus_horaire, hotel) VALUES (42, '10:30:00', 'hot1');
INSERT INTO dessert_site (bus_ligne, bus_horaire, site) VALUES (42, '10:30:00', 'hot1');


INSERT INTO TypeCuisine (label)  VALUES ('oriental');

INSERT INTO Restaurant (sk, nom, telephone, type_cuisine, hotel, site) VALUES (99, 'restoDuKeur', 30303, 'oriental', 'ParisHilton', 'Roissy');

INSERT INTO Hotel (nom, adresse, codepostal, ville, etoiles) VALUES ('ParisHilton', 'Rue de Belle', '70100', 'Paris', 9);

INSERT INTO SiteTouristique (nom, anciennete)  VALUES ('Roissy', 994);

INSERT INTO Activite (nom) VALUES ('chasse de dragon');
INSERT INTO Activite (nom) VALUES ('visite de Poudlard'); 

INSERT INTO ActiviteParSite (site, activite) VALUES ('Roissy', 'visite de Poudlard');
INSERT INTO ActiviteParSite (site, activite) VALUES ('Roissy', 'chasse de dragon');

INSERT INTO ArretDeBus (ligne, horaire) VALUES (7, '23:06');
INSERT INTO ArretDeBus (ligne, horaire) VALUES (66, '12:15');
INSERT INTO ArretDeBus (ligne, horaire) VALUES (7, '10:00');


INSERT INTO Dessert_Hotel (bus_ligne, bus_horaire, hotel) VALUES (7, '23:06', 'ParisHilton');
INSERT INTO Dessert_Hotel (bus_ligne, bus_horaire, hotel) VALUES (7, '10:00', 'ParisHilton');

INSERT INTO Dessert_Site (bus_ligne, bus_horaire, site) VALUES (7, '10:00', 'Roissy');
INSERT INTO Dessert_Site (bus_ligne, bus_horaire, site) VALUES (66, '12:15', 'Roissy');
