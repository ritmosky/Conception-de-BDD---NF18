-- Insertion des données
-- Clients
INSERT INTO Client VALUES (0665357620, 'Alexis', '25 rue Robert Latouche');
INSERT INTO Client VALUES (0671307648, 'Camille', '2 av Einstein');
INSERT INTO Client VALUES (0752418768, 'Maxime', '5 rue de Laplace');
INSERT INTO Client VALUES (0663768834, 'Mathieu', '6 av Notre Dame');
INSERT INTO Client VALUES (0764723098, 'Jules', '105 rue Amsterdam');
INSERT INTO Client VALUES (0763357620, 'Julien', '23 rue Pierre');
INSERT INTO Client VALUES (0655298443, 'Alexandre', '77 av Victor Hugo');
INSERT INTO Client VALUES (0736542021, 'Paul', '1 rue des Boulangeries');
INSERT INTO Client VALUES (0776854098, 'Emma', '3 rue Etoile');
INSERT INTO Client VALUES (0642112376, 'Hélène', '65 av de Notre-Dame');

-- Comptes
-- Alexis
INSERT INTO Compte VALUES ('2021-05-03 06:14:00.75', 'ouvert');
INSERT INTO CompteEpargne VALUES ('2021-05-03 06:14:00.75', 600.00, 300.00);
INSERT INTO Compte VALUES ('2021-05-03 07:14:00.75', 'ouvert');
INSERT INTO CompteCourant (date_crea, balance, montant_decouvert_autorise, max_solde, min_solde) 
VALUES ('2021-05-03 07:14:00.75', 1156.00, 300.00, 1200.00, 300.00);
INSERT INTO Asso_Compte_client VALUES (0665357620, '2021-05-03 06:14:00.75');
INSERT INTO Asso_Compte_client VALUES (0665357620, '2021-05-03 07:14:00.75');

-- Camille
INSERT INTO Compte VALUES ('2021-05-03 07:16:00.75', 'ouvert');
INSERT INTO CompteCourant (date_crea, balance, montant_decouvert_autorise, max_solde, min_solde) 
VALUES ('2021-05-03 07:16:00.75', 35650.67, 1000.00, 45607.54, 30432.37);
INSERT INTO Asso_Compte_client VALUES (0671307648, '2021-05-03 07:16:00.75');

-- Maxime
INSERT INTO Compte VALUES ('2022-02-08 06:14:00.75', 'ouvert');
INSERT INTO CompteEpargne VALUES ('2022-02-08 06:14:00.75', 900.00, 100.00);
INSERT INTO Compte VALUES ('2022-05-02 07:14:00.75', 'ouvert');
INSERT INTO CompteCourant (date_crea, balance, montant_decouvert_autorise, max_solde, min_solde) 
VALUES ('2022-05-02 07:14:00.75', 900.00, 300.00, 1200.00, 300.00);
INSERT INTO Asso_Compte_client VALUES (0752418768, '2022-02-08 06:14:00.75');
INSERT INTO Asso_Compte_client VALUES (0752418768, '2022-05-02 07:14:00.75');

-- Mathieu
INSERT INTO Compte VALUES ('2021-09-17 10:15:32.98', 'bloqué');
INSERT INTO CompteCourant VALUES ('2021-09-17 10:15:32.98', 102.34, -300.00, 1300.00, 102.00, '2022-04-30');
INSERT INTO Asso_Compte_client VALUES (0663768834, '2021-09-17 10:15:32.98');

-- Jules
INSERT INTO Compte VALUES ('2021-10-23 11:21:49.32', 'ouvert');
INSERT INTO CompteCourant (date_crea, balance, montant_decouvert_autorise, max_solde, min_solde) 
VALUES ('2021-10-23 11:21:49.32', 4677.68, 500.00, 5898.45, 1337.39);
INSERT INTO Compte VALUES ('2021-11-24 11:21:49.32', 'ouvert');
INSERT INTO CompteRevolving VALUES ('2021-11-24 11:21:49.32', -300.00, 0.001, -1000.00);
INSERT INTO Asso_Compte_client VALUES (0764723098, '2021-10-23 11:21:49.32');
INSERT INTO Asso_Compte_client VALUES (0764723098, '2021-11-24 11:21:49.32');

-- Julien
INSERT INTO Compte VALUES ('2019-09-09 09:09:09.09', 'fermé');
INSERT INTO CompteCourant (date_crea, balance, montant_decouvert_autorise, max_solde, min_solde) 
VALUES ('2019-09-09 09:09:09.09', 0.56, 100.00, 3298.43, 0.55);
INSERT INTO Asso_Compte_client VALUES (0763357620, '2019-09-09 09:09:09.09');

-- Alexandre
INSERT INTO Compte VALUES ('2020-01-27 15:34:32.02', 'ouvert');
INSERT INTO CompteCourant (date_crea, balance, montant_decouvert_autorise, max_solde, min_solde) 
VALUES ('2020-01-27 15:34:32.02', 430.23, 100.00, 1112.38, 130.43);
INSERT INTO Asso_Compte_client VALUES (0655298443, '2020-01-27 15:34:32.02');

-- Paul
INSERT INTO Compte VALUES ('2022-02-16 15:36:32.02', 'ouvert');
INSERT INTO CompteCourant (date_crea, balance, montant_decouvert_autorise, max_solde, min_solde) 
VALUES ('2022-02-16 15:36:32.02', 1230.54, 150.00, 1589.13, 143.56);
INSERT INTO Compte VALUES ('2022-04-23 14:56:12.23', 'ouvert');
INSERT INTO CompteEpargne VALUES ('2022-04-23 14:56:12.23', 650.00, 100.00);
INSERT INTO Asso_Compte_client VALUES (0736542021, '2022-02-16 15:36:32.02');
INSERT INTO Asso_Compte_client VALUES (0736542021, '2022-04-23 14:56:12.23');

-- Emma
INSERT INTO Compte VALUES ('2022-05-03 15:36:32.02', 'ouvert');
INSERT INTO CompteCourant (date_crea, balance, montant_decouvert_autorise, max_solde, min_solde) 
VALUES ('2022-05-03 15:36:32.02', 967.87, 150.00, 967.89, 10.00);
INSERT INTO Asso_Compte_client VALUES (0776854098, '2022-05-03 15:36:32.02');

-- Hélène
INSERT INTO Compte VALUES ('2021-08-13 15:36:32.02', 'ouvert');
INSERT INTO CompteCourant (date_crea, balance, montant_decouvert_autorise, max_solde, min_solde) 
VALUES ('2021-08-13 15:36:32.02', 1267.87, 150.00, 1432.43, 300.43);
INSERT INTO Compte VALUES ('2022-03-04 11:02:30.45', 'ouvert');
INSERT INTO CompteRevolving VALUES ('2022-03-04 11:02:30.45', -210.45, 0.0015, -400.00);
INSERT INTO Asso_Compte_client VALUES (0642112376, '2021-08-13 15:36:32.02');
INSERT INTO Asso_Compte_client VALUES (0642112376, '2022-03-04 11:02:30.45');

-- Opérations 
INSERT INTO Operation VALUES (1, 300, '2022-05-09', 'non traité', 0665357620, '2021-05-03 06:14:00.75');
INSERT INTO DebitGuichet VALUES (1);

INSERT INTO Operation VALUES (2, 2000, '2022-05-09 20:12', 'non traité', 0764723098, '2021-10-23 11:21:49.32');
INSERT INTO EmissionCheque VALUES(2);

INSERT INTO Operation VALUES (3, 200, '2022-05-06', 'non traité', 0671307648, '2021-05-03 07:16:00.75');
INSERT INTO CarteBleu VALUES (3);

INSERT INTO Operation VALUES (4, 500, '2022-05-05', 'non traité', 0752418768, '2022-02-08 06:14:00.75');
INSERT INTO Virement VALUES (4);

INSERT INTO Operation VALUES (5, 230.00, '2022-05-07', 'non traité', 0764723098, '2021-10-23 11:21:49.32');
INSERT INTO EmissionCheque VALUES (5);

INSERT INTO Operation VALUES (6, 230.00, '2019-03-27', 'non traité', 0764723098, '2021-10-23 11:21:49.32');
INSERT INTO EmissionCheque VALUES (6);

INSERT INTO Operation VALUES (7, 100.00, '2022-05-03', 'non traité', 0764723098, '2021-11-24 11:21:49.32');
INSERT INTO EmissionCheque VALUES (7);

INSERT INTO Operation VALUES (8, 50.00, '2022-05-02 10:00:23', 'non traité', 0655298443, '2020-01-27 15:34:32.02');
INSERT INTO DebitGuichet VALUES (8);

INSERT INTO Operation VALUES (9, 150.00, '2022-05-09 17:53:39', 'non traité', 0736542021, '2022-04-23 14:56:12.23');
INSERT INTO Virement VALUES(9);

INSERT INTO Operation VALUES (10, 200.00, '2022-05-08', 'non traité', 0776854098, '2022-05-03 15:36:32.02');
INSERT INTO DepotCheque VALUES (10);

INSERT INTO Operation VALUES (11, 320.00, '2022-05-09 16:45:09', 'non traité', 0642112376, '2022-03-04 11:02:30.45');
INSERT INTO CreditGuichet VALUES (11);




