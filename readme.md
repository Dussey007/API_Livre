# API LIVRE Full Stack 

## Démarrage 

### Installation Des Dépendances

#### Python 3.10.2
#### pip 22.0.4 from \Users\AppData\Roaming\Python\Python310\site-packages\pip (python 3.10)

Suivez les instruction pour l'installation de la dernière version de python pour votre système dans le [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Environnement virtuel

Il est recommandé de travailler dans un environnement virtuel quand vous utiliser python dans un projet. cela permettra à ce que vos projets soient bien structurés et organisé. Vous pourriez trouver des instructions pour paraméttrer votre environnement virtuel dans [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Dependance PIP

Maintenant que vous avez configurer et lancer votre environnement virtuel, Installez les dépendances en vous rendant sur le repectoire Livre_api, ensuite exécutez les commandes suivantes :

```bash
pip install -r requirements.txt
or
pip3 install -r requirements.txt
```

Ceci installera toutes les pacquets requis dans le fichier requirements.txt.

##### Dependance Clés

- [Flask](http://flask.pocoo.org/)  est un framework léger de microservices backend. Flask est nécessaire pour gérer les demandes et les réponses.

- [SQLAlchemy](https://www.sqlalchemy.org/) est la boîte à outils Python SQL et l'ORM que nous utiliserons pour gérer la base de données sqlite légère. Vous travaillerez principalement dans app.py et pourrez référencer models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)  est l'extension que nous utiliserons pour gérer les demandes d'origine croisée de notre serveur frontal.

## Configuration de la base de données
Avec Postgres en cours d'exécution, restaurez une base de données à l'aide du fichier plants_database.sql fourni. Depuis le dossier backend dans le terminal
```bash
psql livres_database < livres_database.sql
```

## Lancer le démarrage du serveur

De l'intérieur du `Livre_api` Assurez-vous d'abord que vous travaillez en utilisant votre environnement virtuel créé.

Pour lancer sur Linux ou Mac, exécuter:

```bash
export FLASK_APP=api
export FLASK_ENV=development
flask run
```
Pour lancer le serveur sur Windows, exécuter:

```bash
set FLASK_APP=api
set FLASK_ENV=development
flask run
```

Paraméttrer le `FLASK_ENV` variable en `development` va détecter les fichiers changé puis va recharger le serveur automatiquement.

Paraméttrer le `FLASK_APP` variable en `api` directement flask pour utiliser le dossier `api` et le fichier  `__init__.py` afin de troyuver l'application.

Vous pouvez toute fois carrément directement le lancer avec l'onglet execute dans VsCode, si vous l'utilisez. 

## REFERENCE API 

Démarrage 

Base URL: À l'heure actuelle, cette application ne peut être exécutée que localement et n'est pas hébergée en tant qu'URL de base.Vous pouvez utiliser ce lien dans votre navigateur http://localhost:5000; Elle vous mènera sur la route par défaut.

## Error Handling (La gestion des erreurs)
Les erreurs sont retournés en Json sous le format ci-dessous:
{
    "success":False
    "error": 400
    "message":"Mauvaise requête"
}


L'API renvoie quatre types d'erreurs lorsque les requêtes échouent :
. 400: Bad request
. 500: Internal server error
. 422: Unprocessable
. 404: Not found

## Endpoints (Points de terminaison)
. ## GET/livres

    GENERAL:
        Ce Endpoints renvoie une liste d'objets livres, la valeur que prend le success, le nombre total de livres.
    
        
    exemple: http://localhost:5000/livres (Listes des livres)
```
{
  "Livres": [
        {
            "auteur": "Charles BAUDELAIRE",
            "date publication": "Tue, 21 Jul 1857 00:00:00 GMT",
            "editeur": "Auguste Poulet-Malassis",
            "id": 1,
            "id categorie": 6,
            "isbn": "1956385230546",
            "titre": "fleur du mal"
        },
        {
            "auteur": "lary",
            "date publication": "Tue, 08 May 1990 00:00:00 GMT",
            "editeur": "remo",
            "id": 2,
            "id categorie": 2,
            "isbn": "1228544963615",
            "titre": "rose"
        },
        {
            "auteur": "Laurent Gounelle",
            "date publication": "Tue, 22 Feb 2022 00:00:00 GMT",
            "editeur": "Calmann-Lévy",
            "id": 8,
            "id categorie": 2,
            "isbn": "9216384138566",
            "titre": "le réveil"
        }
    ],
    "nombre de livres": 3,
    "success": true
```
 

. ## POST/enrgCat

    GENERAL: 
Ici il faut copier le format type dont on a parlé un peu plus haut et vous allez renseigner les chants et enfin lancer la route
ensuite l'ont vous retourne la liste présente après votre ajout.
                  

    exemple pour enregistrer:
 ```
              {
             
              "nom":"roulr",
              "libelle_categorie":"mille",
        
              }
       
``` 

	résultats :
``` 
{
    "Liste Categorie": [
        {
            "id": 2,
            "libelle_categorie": "aner",
            "nom": "Canul"
        },
        {
            "id": 4,
            "libelle_categorie": "reme",
            "nom": "Canular"
        },
        {
            "id": 6,
            "libelle_categorie": "poesie",
            "nom": "Poesie-Lyric"
        },
        {
            "id": 7,
            "libelle_categorie": "mille",
            "nom": "roulr"
        }
    ],
    "Nombre de categorie": 4,
    "id categorie": 7,
    "msg": "La categorie est enregistre avec success"
}
``` 

. ##PATCH/upCat/7(id_du _livre_à_madifier)
  GENERAL: 


  Exemple Pour faire le Patch: On va utiliser l'enregistrement qu'ont vient de faire
 ```    
              {
              
              "nom":"melonch",
              "libelle_categorie":"Vychil"
              }
 ```

Voici notre nouvelle liste:
 ```
{
    "Liste categories": [
        {
            "id": 2,
            "libelle_categorie": "aner",
            "nom": "canul"
        },
        {
            "id": 4,
            "libelle_categorie": "reme",
            "nom": "Canular"
        },
        {
            "id": 6,
            "libelle_categorie": "poesie",
            "nom": "Poesie-Lyric"
        },
        {
            "id": 7,
            "libelle_categorie": "Vychil",
            "nom": "melonch"
        }
    ],
    "nombre categories": 4,
    "success": true
}
 ```

. ## DELETE/supCat/(id_categorie_à_supprimer)

    GENERAL:
       Supprimer l'ID donné si elle existe. Renvoie l'identifiant du livre supprimé, la valeur de réussite, le nombre total de livre,

        Les résultats sont paginés par groupes. incluez un chiffre a la fin de la route pour préciser le livre à supprimer au cas contraire cela vous retournera une erreur 404 (Not found).

        exemple:  DELETE http://localhost:5000/supCat/7 (Ici nous allons supprimer celui qu'on vient de modifier)
```
        {
    "Nombre categorie": 3,
    "deleted": 7,
    "success": true
}
           
{
    "Liste categories": [
        {
            "id": 2,
            "libelle_categorie": "aner",
            "nom": "canul"
        },
        {
            "id": 4,
            "libelle_categorie": "reme",
            "nom": "Canular"
        },
        {
            "id": 6,
            "libelle_categorie": "poesie",
            "nom": "Poesie-Lyric"
        }
    ],
    "nombre categories": 3,
    "success": true
}
```



  ``` PATCH http://localhost:5000/upCat/1 -H "Content-Type:application/json" -d " "libelle_categorie": "aner","nom": "Canul"}"
  ```


#Test
Pour tester l'application vous pouvez utiliser le logiciel Postman... toute fois dans notre dossier vous allez trouver un fichier de postMan dans lequel nous avons mis tout
ce qu'il faut pour le test c'est à dire les routes (le fichier a pour extension .postman_collection.     


