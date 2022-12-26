## **EXTRACTION DES TITRES ET BLOCS DE DEFINITION A PARTIR D'UNE ENCYCLOPEDIE NUMERISEE**

Cet outil permet, à partir d'une encyclopédie numérisée, de générer un fichier contenant tous les termes et leurs blocs de définition, mais également un dossier contenant un fichier par terme. Il s'agit d'un outil interactif, qui demande à l'utilisateur plusieurs paramètres. L'utilisation de l'outil est précisée en détails dans le <u>manuel utilisateur</u> (fichier "MANUEL UTILISATEUR.docx").
Ci-dessous, vous trouverez les instructions liées à l'exécution du programme.

L'utilisation de cet outil se fait en 5 étapes :

1. Récupération de l'encyclopédie numérisée
2. Prétraitement de l'encyclopédie numérisée > *pretraitement.py*
3. Extraction des titres et des blocs (dans un seul fichier) > *script_extraction_encyclopedie.py*
4. Polissage des titres > *polissage.py*
5. Création d'un dossier contenant un fichier par titre > *fichiers_blocs.py*

#### Récupération de l'encyclopédie numérisée :

- Récupérer le fichier correspondant au lien ark de l'encyclopédie (avec "/texteBrut" à la fin de l'URL) sur le site de Gallica
- Copier coller le contenu de ce fichier dans un fichier txt

#### Prétraitement de l'encyclopédie numérisée :

- Exécuter la ligne suivante dans le terminal (dans cet exemple, *encyclopedie.txt* est le nom du fichier de l'encyclopédie)

  ```shell
  python3 pretraitement.py encyclopedie.txt
  ```

- Cette ligne de commande crée un nouveau fichier *Encode_eyclopedie.txt* qui sera utilisé dans l'étape suivante

#### Extraction des titres et des blocs (dans un seul fichier) :

- Exécuter la ligne suivante dans le terminal 

  ```shell
  python3 script_extraction_encyclopedie.py Encode_encyclopedie.txt
  ```

- Suivre les étapes précisées dans le <u>manuel utilisateur</u>

- Cette ligne de commande crée plusieurs fichiers utilisés ou non lors de l'exécution du programme

#### Polissage des titres :

- Exécuter la ligne suivante dans le terminal (dans cet exemple, *liste_des_titres.txt* est le nom du fichier contenant la liste des titres, créé lors de l'étape précédente)

  ```shell
  python3 polissage.py liste_des_titres.txt
  ```

- Cette ligne de commande crée un nouveau fichier *nouveau.txt* contenant une liste des titres plus lisible

#### Création d'un dossier contenant un fichier par titre :

- Exécuter la ligne suivante dans le terminal (dans cet exemple, *titres_et_blocs.txt* est le nom du fichier contenant les titres et leurs blocs de définition, créé lors de l'étape 3)

  ```shell
  python3 fichiers_blocs.py titres_et_blocs.txt
  ```

- Cette ligne de commande crée un dossier contenant un fichier par titre (le nom du fichier est le titre et le contenu du fichier est son bloc correspondant)



## Prérequis : 

python >= 3.6

<u>Modules python</u> :

- unicodedata
- sys
- json
- re
- codecs
- os

Si vous obtenez une erreur "ModuleNotFoundError" liée à l'un des modules ci-dessus, une des lignes de commande suivantes devrait suffire à régler le problème :

```shell
pip install MODULE
```

```shell
pip3 install MODULE
```

