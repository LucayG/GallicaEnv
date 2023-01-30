## NETTOYAGE DE CORPUS

Cet outil permet de "nettoyer" un corpus en retirant la ponctuation non nécessaire, les espaces doublons, les chiffres et certains mots spécifiés par l'utilisateur. Il faut fournir un corpus à nettoyer (fichier txt) et une liste de vocabulaire à retirer (fichier txt avec un terme par ligne) éventuellement vide.

L'utilisation de cet outil se fait en 1 étape :

1. Nettoyage du corpus > *nettoyage_avant.py*

#### Nettoyage du corpus :

- Exécuter la ligne suivante dans le terminal

  ```shell
  python3 nettoyage_avant.py
  ```

- Il vous sera demandé dans le terminal de donner le nom du fichier txt contenant le vocabulaire à retirer (<u>un terme par ligne</u>)

- Il vous sera également demandé de donner le nom du fichier txt contenant le corpus à nettoyer

- Cette ligne de commande crée un nouveau fichier *corpus_nettoye.txt* 



## Prérequis :

python >= 3.6

<u>Modules python</u> :

- re
- unicodedata

Si vous obtenez une erreur "ModuleNotFoundError" liée à l'un des modules ci-dessus, une des lignes de commande suivantes devrait suffire à régler le problème :

```shell
pip install MODULE
```

```shell
pip3 install MODULE
```

