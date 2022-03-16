INSERT INTO ArretDeBus (ligne) VALUES (932); -- Faux car PRIMARY KEY contient les deux attributs de ArretDeBus
INSERT INTO SiteTouristique (nom, anciennete) VALUES (200000);
INSERT INTO Hotel (nom, adresse, codePostal, ville, etoiles) VALUES ('3 rue du general de Gaulle', '64291', 'petaouchnok-les-bains', 1);
INSERT INTO Restaurant (sk, telephone, type_cuisine, hotel, site) VALUES (13497, '0123456789','belge', 'Lebrazero', 'monument du requin en eau douce');
INSERT INTO Restaurant (sk, telephone, type_cuisine, hotel, site) VALUES (123, '30303','belge', 'Lebrazero', 'monument du requin en eau douce');
INSERT INTO ActiviteParSite (site, activite) VALUES ('monument du requin en eau douce', 'Parachutisme');
INSERT INTO Restaurant (sk, nom, telephone, type_cuisine, hotel, site) VALUES (13, 'labonnefranquette', '0123456789','belge', 'Lebrazero', 'monument du requin en eau douce');
