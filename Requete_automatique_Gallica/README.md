## OUTIL DE RECUPERATION DES RESULTATS D'UNE REQUETE SOUS GALLICA

Cet outil permet de récupérer les résultats d'une requête sous Gallica, en proposant soit de chercher plusieurs termes (indépendamment les uns des autres), soit par couples de termes (à une certaine proximité). Dans ce programme, vous pourrez spécifier certains paramètres de la requête (voir le manuel utilisateur : MANUEL_UTILISATEUR.odx), comme le type de document, le thème, la recherche par expansion, etc.

Dans le cas d'une recherche par mots simples, il est demandé de fournir un fichier (txt ou UNIMARC) contenant les termes à rechercher.

Dans le cas d'une recherche par couples de mots, il est demandé de fournir deux fichiers txt : le croisement de ces deux fichiers permettra la formation des couples. Par exemple si l'on a :

<u>fichier 1</u> : "forêt", "environnement"

<u>fichier 2</u> : "bois", "taillis"

Les couples recherchés seront : ("forêt", "bois"), ("forêt", "taillis"), ("environnement", "bois") et ("environnement", "taillis")



L'utilisation de cet outil se fait en deux étapes : 

1. Récupération des résultats de la requête

   - Avec mots simples > *rich_pages.py*
   - Avec couples de mots > *rich_croise.py*

2. Mise en page plus lisible des résultats > *jolie_sortie.py*

   

#### Récupération des résultats de la requête :

**<u>Avec mots simples</u> :**

- Exécuter la ligne suivante dans le terminal (tous les scripts *.py* doivent être dans le même dossier !)

  ```shell
  python3 rich_pages.py
  ```

- Il vous sera demandé dans le terminal de renseigner le fichier txt (<u>un terme par ligne</u>) ou UNIMARC contenant la liste des termes à rechercher

- Il vous sera également demandé de spécifier les paramètres de la requête (voir <u>manuel utilisateur</u>)

- Cette ligne de commande crée un dossier "Depot_Gallica" contenant cinq fichiers *Extraits.txt*, *Tableau.xml*, *Matrix.xml*, *Liens_ARK.txt* et *Liste_1.txt* (voir <u>manuel utilisateur</u>)

**<u>Avec couples de mots</u> :**

- Exécuter la ligne suivante dans le terminal (tous les scripts *.py* doivent être dans le même dossier !)

  ```shell
  python3 rich_croise.py
  ```

- Il vous sera demandé dans le terminal de renseigner les fichier txt (<u>un terme par ligne</u>) contenant les deux listes de termes à croiser pour former les couples de mots à rechercher

- Il vous sera également demandé de spécifier les paramètres de la requête (voir <u>manuel utilisateur</u>)

- Cette ligne de commande crée un dossier "Depot_Gallica" contenant cinq fichiers *Extraits.txt*, *Tableau.xml*, *Matrix.xml*, *Liens_ARK.txt* et *Liste_1.txt* (voir <u>manuel utilisateur</u>)

#### Mise en page plus lisible des résultats : 

- Exécuter la ligne suivante dans le terminal (dans un dossier contenant le script *jolie_sortie.py* et les fichiers *Extraits.txt* et *Tableau.xml* de l'étape précédente)

  ```shell
  python3 jolie_sortie.py
  ```

- Il vous sera demandé dans le terminal de renseigner le fichier xml contenant le tableau des résultats ainsi que le fichier txt contenant les extraits

- Cette ligne de commande crée un nouveau fichier *Resultats_et_extraits.txt* qui contient moins de renseignements que le fichier *Tableau.xml* mais qui est plus lisible



## Prérequis :

python >= 3.6

<u>Modules python</u> :

- sklearn >= 1.0
- html
- sys
- os
- collections
- pandas
- itertools
- requests
- urllib
- re
- pathlib
- tqdm
- csv
- lxml
- abc
- xmltodict
- bs4
- ast
- docx
- multiprocessing
- codecs
- unicodedata
- tqdm
- csv
- lxml

Si vous obtenez une erreur "ModuleNotFoundError" liée à l'un des modules ci-dessus, une des lignes de commande suivantes devrait suffire à régler le problème :

```shell
pip install MODULE
```

```shell
pip3 install MODULE
```

