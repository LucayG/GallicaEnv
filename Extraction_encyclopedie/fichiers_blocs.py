# -*- coding: utf-8 -*-

import codecs
import sys
import os

'''
input : fichier txt contenant l'extraction des titres et des blocs (output de script_extraction_encyclopedie.py)
output : dossier Fichiers_blocs contenant un fichier par bloc (le titre du bloc est le titre du fichier)
'''

'''CHEMIN DU FICHIER TXT TITRE_BLOCS A PASSER EN ARGUMENT
if __name__ == '__main__':
    if len(sys.argv) > 1: 
        path = sys.argv[1]
    else: 
        print("Veuillez entrer le chemin du fichier txt contenant l'extraction des titres et des blocs")
with codecs.open(path, encoding = "utf8") as fic :
    data = fic.read().split('\n')
    fic.close()
'''
  
''' QUAND ON N'UTILISE PAS LA LIGNE DE COMMANDE '''      
with codecs.open('extraction_titre_bloc_avec_titre1_Tome_1.txt', encoding = 'utf8') as fic: # path a changer
    data = fic.read().split('\n')
    fic.close()


path = input('Indiquez le nom que vous souhaitez donner au dossier qui va etre cree : ')

os.mkdir(path)
liste_titres = []

for line in data:
    if line.startswith('@@@'):
        line_temp = line.split('@@@')
        line_temp.remove('')
        titre = line_temp[1]
        liste_titres.append(titre)
    if line.startswith('###'):
        line_temp = line.split('###')
        line_temp.remove('')
        bloc = line_temp[0]
        try :
            with codecs.open(path+'/'+titre+'.txt', 'w', encoding = 'utf8') as fic :
                fic.write(bloc)
            fic.close()
        except OSError :
            titre = titre.replace('*','')
            titre = titre.replace('/','')
            titre = titre.replace('\\','')
            titre = titre.replace('>','')
            titre = titre.replace(':','')
            with codecs.open(path+'/'+titre+'.txt', 'w', encoding = 'utf8') as fic :
                fic.write(bloc)
            fic.close()

with codecs.open(path + '/liste_des_titres.txt', 'w', encoding = 'utf8') as fic:
    for line in liste_titres :
        fic.write(line+'\n')
    fic.close()
        
