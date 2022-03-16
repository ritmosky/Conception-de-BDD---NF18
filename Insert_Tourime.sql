INSERT INTO ArretDeBus (ligne, horaire) VALUES (932, '14:15');
INSERT INTO SiteTouristique (nom, anciennete) VALUES ('monument du requin en eau douce', 200000);
INSERT INTO Hotel (nom, adresse, codePostal, ville, etoiles) VALUES ('Lebrazero', '3 rue du general de Gaulle', '64291', 'petaouchnok-les-bains', 1);
INSERT INTO TypeCuisine (label) VALUES ('belge');
INSERT INTO Restaurant (sk, nom, telephone, type_cuisine, hotel, site) VALUES (13, 'manger comme quatre', '0123456789','belge', 'Lebrazero', 'monument du requin en eau douce');
INSERT INTO Activite (nom) VALUES ('Parachutisme');
INSERT INTO ActiviteParSite (site, activite) VALUES ('monument du requin en eau douce', 'Parachutisme');
INSERT INTO Dessert_hotel (bus_ligne, bus_horaire, hotel) VALUES (932, '14:15', 'Lebrazero');
INSERT INTO Dessert_site (bus_ligne, bus_horaire, site) VALUES (932, '14:15', 'monument du requin en eau douce');
