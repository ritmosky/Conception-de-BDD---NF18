INSERT INTO Station (num, nom, adresse) VALUES (10, 'Gare SNCF', '1 Avenue de la Gare - Compiègne');
INSERT INTO Conducteur (matricule, nom, prenom) VALUES ('AZDF34GV52', 'Dupond', 'Luc');
INSERT INTO Bus (immat, type, kilometrage, matricule) VALUES ('A-132-GH', 'Soufflets', 130000, 'AZDF34GV52');
INSERT INTO Ligne (num, km) VALUES (444, 2);
INSERT INTO Trajet (immat, ligne, nbtrajets) VALUES ('A-132-GH', 444, 25);
