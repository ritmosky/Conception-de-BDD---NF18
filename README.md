# NF18



## Lancer l'applicatif python :

1) cloner le repo ```$ git clone https://gitlab.utc.fr/touedrao/nf18.git```
2) modifier la connexion à la BDD
dans "Projet_NF18_Gestion_comptes_bancaires/python/main_code.py" modifier la partie suivante avec les bonnes valeurs.
```
HOST = "localhost"
USER = "postgres"
PASSWORD = "fort"
DATABASE = "postgres"
```


3) lancer la commande ```$ python3 main_code.py```

/!\ à se rendre dans le dossier contenant miam_code.py avant de le lancer /!\
4) pour le chemin demandé, insérer ```../SQL_et_Data```



## POUR LA PARTIE PROJET

Ce projet a été réalisé dans le cadre de l'UV NF18 -> CONCEPTION DES BASES DE DONNÉES.

Il contient :

- un dossier MCD regroupant l'ensemble de notre travail sur la partie MCD (Modèle Conceptuel de Données).

- un dossier MLD regroupant l'ensemble de notre travail sur la partie MLD (Modèle Logique de Données).

- un dossier PYTHON, contenant le code python, que nous avons modulé en 6 fichiers pour plus de lisibilité.

- un dossier SQL_et_DATA qui contient des fichiers SQL (permettant la création, la suppression, l'insertion de données et quelques requêtes SQL) et aussi des fichiers CSV (à partir desquels on peut charger des données mais également qui s'actualisent à chaque modification de la base de données au travers de l'applicatif Python).

- un fichier txt pour l'étude de normalisation (PS: vraiment désolé de le rendre aussi tardivement, mais sur le site la date de son rendu n'était notifié à aucun endroit).


```
cd existing_repo
git remote add origin https://gitlab.utc.fr/touedrao/nf18.git
git branch -M main
git push -uf origin main
```

