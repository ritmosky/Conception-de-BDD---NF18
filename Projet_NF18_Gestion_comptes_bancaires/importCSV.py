#!/usr/bin/python3

import psycopg2

print("Ici, vous pouvez insérer des données à partir de fichiers CSV. Quelles données souhaitez-vous intégrer à la base ?")
print("1. données client")
choice = input("Que choisissez-vous ? ")

if choice == 1:
    HOST = "localhost"
    USER = "postgres"
    PASSWORD = "fort"
    DATABASE = "postgres"

    # Open connection
    connection = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))

    # Open a cursor to send SQL commands
    cursor = connection.cursor()

    # Execute a SQL SELECT command
    sql = "\copy Client (tel, nom, adresse) FROM './client.csv' WITH CSV DELIMITER ';' QUOTE '\"'"
    cursor.execute(sql)

choice = input("Voulez-vous afficher la table client ? [y/n] ")
if choice == "y":
    HOST = "localhost"
    USER = "postgres"
    PASSWORD = "fort"
    DATABASE = "postgres"

    # Open connection
    connection = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))

    # Open a cursor to send SQL commands
    cursor = connection.cursor()

    # Execute a SQL SELECT command
    sql = "SELECT * FROM Client"
    cursor.execute(sql)

    # Fetch data line by line
    data = cursor.fetchone()
    print("\tTéléphone       Nom     [adresse]")
    while data:
        print("\t%s"%(data[0]), end='')
        print("\t%s" %(data[1]), end='')
        print("\t[%s]" %(data[2]))
        data = cursor.fetchone()
