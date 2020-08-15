# Stockage des informations de téléinfo de Enedis à l'aide d'une connexion série

Ce projet contient différents scritps permettant de bien gérer le stockage des informations provenant des compteurs Linky de Enedis. Ainsi, deux services python sont prévus : 

- teleinfo/start_teleinfo.py : lit en continue les informations provenant du port série et stock le tout dans une base de données sqlite locale
- teleinfo/syncdatabases.py : Synchronize la base de données locale avec une base de donnée MySQL distante. Ce script doit être lancé via un crontab et permet de s'affranchir
d'éventuelles pertes de connexions réseau

## Configuration
Toute la configuration des scripts python se fait dans le dossier teleinfo/config

### Base de données MySQL (uniquement pour `syncdatabase`)
Il est nécessaire faire une copie du fichier teleinfo/config/db_prod_mysql.py.sample en teleinfo/config/db_prod_mysql.py et de mettre vos identifiants de base de données MySQL

### Base de données SQLite (Indispensable)
Il faut faire une copie du fichier teleinfo/config/db_prod_sqlite.py.sample en teleinfo/config/db_prod_sqlite.py et de renseigner le chemin de la base sqlite

### Autres configuration
Les autres configurations peuvent être changées dans le fichier `teleinfo/config/config.py`

