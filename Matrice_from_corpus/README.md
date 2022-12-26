## GENERATION DE MATRICES A PARTIR D'UN VOCABULAIRE ET DE CORPUS

Cet outil permet de générer une matrice de présence ou d'occurrences de mots dans des documents. Il faut pour cela fournir une liste de vocabulaire, pour lequel chaque mot sera recherché dans les corpus. Les matrices auront ainsi des lignes correspondant aux documents, et des colonnes à chaque terme du vocabulaire. 

La matrice de <u>présence</u> est une matrice binaire (1 si le terme se trouve dans le document, 0 sinon) et la matrice d'<u>occurrences</u> est une matrice contenant le nombre de fois où un terme apparait dans un document.

L'utilisation de cet outil se fait avec deux possibilités :

1. Génération d'une matrice de présence > *matrice_binaire.py*
2. Génération d'une matrice d'occurrences > *matrice_occurrences.py*

#### Génération d'une matrice de présence :

- Exécuter la ligne suivante dans le terminal

  ```shell
  python3 matrice_binaire.py 
  ```

- Il vous sera demandé dans le terminal de donner le nom du dossier contenant les différents corpus stockés dans des fichiers txt

- Il vous sera également demandé de donner le nom du fichier txt contenant la liste de vocabulaire (<u>un terme par ligne</u>)

- Cette ligne de commande crée un nouveau fichier *Matrice_binaire.csv* qui contient la matrice de présence

#### Génération d'une matrice de présence :

- Exécuter la ligne suivante dans le terminal

  ```shell
  python3 matrice_occurrences.py 
  ```

- Il vous sera demandé dans le terminal de donner le nom du dossier contenant les différents corpus stockés dans des fichiers txt

- Il vous sera également demandé de donner le nom du fichier txt contenant la liste de vocabulaire (<u>un terme par ligne</u>)

- Cette ligne de commande crée un nouveau fichier *Matrice_occurrences.csv* qui contient la matrice d'occurrences



## Prérequis :

python >= 3.6

<u>Modules python</u> :

- os
- os.path
- numpy
- csv

Si vous obtenez une erreur "ModuleNotFoundError" liée à l'un des modules ci-dessus, une des lignes de commande suivantes devrait suffire à régler le problème :

```shell
pip install MODULE
```

```shell
pip3 install MODULE
```

