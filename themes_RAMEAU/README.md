## RELATIONS SEMANTIQUES A PARTIR DE THEMES RAMEAU

Cet outil permet de générer une matrice de relations (1 si relié sémantiquement, 0 sinon) entre des thèmes de la classification RAMEAU de la BNF. A partir d'une requête dans le catalogue général de la BNF, on récupère un fichier au format UNIMARC (voir *notices.txt*) qui, avec cet outil, génère une matrice.

L'utilisation de cet outil se fait en trois étapes :

1. Récupération du fichier UNIMARC sur le catalogue général de la BNF
2. Prétraitement du fichier > _pretraitement.py_
3. Génération de la matrice > _script\_extraction\_relations.py_

#### Récupération du fichier au format UNIMARC :

- Se rendre sur la page de requête dans les notices d'autorité du catalogue général de la BNF : https://catalogue.bnf.fr/recherche-autorite.do?pageRech=rat
- Lancer une requête (par exemple : "environnement")
- Sélectionner (à gauche) "Répertoire RAMEAU" et "Concept, genre ou forme"
- Sélectionner tous les résultats (en cochant la case pour chaque page de résultats)
- Cliquer sur "Télécharger/Imprimer" à droite
- Sélectionner "TXT", "notices complètes" et "Unimarc"
- Enregistrer le fichier généré dans le dossier contenant les scripts

#### Prétraitement du fichier :

- Exécuter la ligne suivante dans le terminal (dans cet exemple, *notices.txt* est le nom du fichier UNIMARC)

  ```shell
  python3 pretraitement.py notices.txt
  ```

- Cette ligne de commande crée un nouveau fichier *Encode_notices.txt* qui sera utilisé dans l'étape suivante

#### Génération de la matrice :

- Exécuter la ligne suivante dans le terminal

  ```shell
  python3 script_extraction_relations.py Encode_notices.txt
  ```

- Cette ligne de commande crée un nouveau fichier *Rameau_Encode_notices.csv* qui contient la matrice de relations



## Prérequis :

python >= 3.6

<u>Modules python</u> :

- unicodedata
- sys
- numpy
- csv
- codecs

Si vous obtenez une erreur "ModuleNotFoundError" liée à l'un des modules ci-dessus, une des lignes de commande suivantes devrait suffire à régler le problème :

```shell
pip install MODULE
```

```shell
pip3 install MODULE
```

