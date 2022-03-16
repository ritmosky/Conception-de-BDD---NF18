INSERT INTO Station (num, nom, adresse) VALUES (10, 'Gare SNCF', '1 Avenue de la Gare - Compiègne');
INSERT INTO Conducteur (matricule, nom, prenom) VALUES ('AZDF34GV52', 'Dupond', 'Luc');
INSERT INTO Bus (immat, type, kilometrage, matricule) VALUES ('A-132-GH', 'Soufflets', 130000, 'AZDF34GV52');
INSERT INTO Ligne (num, km) VALUES (444, 2);
INSERT INTO Trajet (immat, ligne, nbtrajets) VALUES ('A-132-GH', 444, 25);


INSERT INTO Conducteur (matricule, nom, prenom) VALUES ('abcd', 'Alain', 'Thobias');
INSERT INTO Conducteur (matricule, nom, prenom) VALUES ('ef', 'John', 'Doe');
INSERT INTO Conducteur (matricule, nom, prenom) VALUES ('gg', 'Robin', 'Batman');

INSERT INTO Bus (immat, type, kilometrage, matricule) VALUES ('5657 MA 49', 'Normaux', 27, 'abcd');
INSERT INTO Bus (immat, type, kilometrage, matricule) VALUES ('666 XX 60', 'Normaux', 12 'ef');
INSERT INTO Bus (immat, type, kilometrage, matricule) VALUES ('232 MR 45', 'Soufflets', 34, 'gg');

INSERT INTO Ligne (num, km) VALUES (1, 6);
INSERT INTO Trajet (immat, ligne, nbtrajets) VALUES ('232 MR 45', 1, 8);

INSERT INTO Ligne (num, km) VALUES (42, 10);
