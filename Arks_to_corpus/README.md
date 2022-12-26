## GENERATION D'UN CORPUS A PARTIR D'ARKS DE DOCUMENTS GALLICA

Cet outil permet de générer un corpus à partir d'une liste d'arks de documents sous Gallica. Il est possible de créer ce corpus sous forme d'un seul fichier (avec les documents concaténés) ou dans plusieurs fichiers (un par document) stockés dans un dossier. Un fichier txt indiquant les liens de correspondance entre un ark, le titre d'un document et le fichier créé correspondant (dans le deuxième cas) sera également généré.

L'utilisation de cet outil nécessite un fichier txt contenant une liste de liens ark (<u>exemple</u> : *idark.txt*) et s'utilise avec deux possibilités :

1. Création d'un corpus stocké dans un seul fichier > *extraire_doc.py*
2. Création d'un corpus stocké dans plusieurs fichiers > *extraire_doc_plusieurs_pages.py*

#### Création d'un corpus stocké dans un seul fichier :

- Exécuter la ligne suivante dans le terminal

  ```shell
  python3 extraire_doc.py
  ```

- Il vous sera demandé dans le terminal de donner le nom du fichier contenant la liste des arks (<u>un par ligne</u>)

- Il vous sera également demandé si vous souhaitez conserver les entêtes des documents (métadonnées du document numérisé)

- Cette ligne de commande crée un nouveau fichier *corpus.txt* qui contient tous les documents (avec ou sans leur entête) concaténés, ainsi que le fichier *correpondances.txt*

- #### Création d'un corpus stocké dans plusieurs fichiers :

  - Exécuter la ligne suivante dans le terminal

    ```shell
    python3 extraire_doc_plusieurs_pages.py
    ```

  - Il vous sera demandé dans le terminal de donner le nom du fichier contenant la liste des arks

  - Il vous sera également demandé si vous souhaitez conserver les entêtes des documents (métadonnées du document numérisé)

  - Cette ligne de commande crée un nouveau dossier "Résultat" qui contient tous les fichiers (un par document, avec ou sans entête), ainsi que le fichier *correpondances.txt*



## Prérequis :

python >= 3.6

<u>Modules python</u> :

- urllib.request
- bs4
- os

Si vous obtenez une erreur "ModuleNotFoundError" liée à l'un des modules ci-dessus, une des lignes de commande suivantes devrait suffire à régler le problème :

```shell
pip install MODULE
```

```shell
pip3 install MODULE
```

