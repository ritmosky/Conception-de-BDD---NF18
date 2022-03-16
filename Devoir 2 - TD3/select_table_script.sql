--Nom et prénom du conducteur du bus immatriculé "5657 MA 49".
SELECT nom, prenom FROM Conducteur, Bus WHERE  Conducteur.matricule = Bus.matricule AND Bus.immat = '5657 MA 49';

--Immatriculation et type des bus qui partent de la station "Gare SNCF".

--Numéros des lignes qui ne sont pas desservies par des bus à soufflets.

