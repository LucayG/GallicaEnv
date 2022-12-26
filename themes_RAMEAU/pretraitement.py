# -*- coding: utf-8 -*-

import unicodedata
import sys

'''CHEMIN DU FICHIER TXT A PASSER EN ARGUMENT'''
if __name__ == '__main__':
    if len(sys.argv) > 1: 
        path = sys.argv[1]
    else: 
        print("Veuillez entrer le chemin du fichier txt")


with open(path, encoding = 'utf8') as f:
    big_str = f.read()
    f.close()
    
def encodage(data_str):
    return unicodedata.normalize('NFKD', data_str).encode('ascii','ignore').decode('ascii')

with open("Encode_" + path, 'w', encoding = 'utf8') as fic:
    fic.write(encodage(big_str))
fic.close()
