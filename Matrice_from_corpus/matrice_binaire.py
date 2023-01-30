from os import listdir
from os.path import isfile, join
import numpy as np
import csv

monRepertoire = input("Répertoire contenant les documents : ")
fichiers = [f for f in listdir(monRepertoire) if isfile(join(monRepertoire, f))]

print("Liste des documents : ",fichiers)

	
fichier_concat = []
for filename in fichiers:
	with open(monRepertoire + "/" + filename, "r", encoding="utf8") as fic:
		fichier_concat.append(fic.read())

liste_vocab = open(input("Fichier txt contenant la liste de vocabulaire (avec l'extension .txt) : "), 'r').readlines()


for i in range(len(liste_vocab)) :
	liste_vocab[i] = liste_vocab[i].replace("\n","").strip()

print(liste_vocab)

dico_freq = {key : {} for key in liste_vocab}
for fichier, filename in zip(fichier_concat, fichiers):
	fichier = fichier.split()
	for word in liste_vocab :
		dico_freq[word][filename] = 0
		if word in fichier:
			dico_freq[word][filename] = 1

''' Matrice '''

matrice = np.zeros((len(fichiers), len(dico_freq)))

for i in range(len(fichiers)):
	j=0
	for word in dico_freq:
		matrice[i][j] = dico_freq[word][fichiers[i]]
		j+=1

matrice = matrice.astype(int) # float --> int
print("shape : " + str(np.shape(matrice)))


''' Creation du fichier csv'''

with open("Matrice_binaire.csv", 'w', encoding='utf8') as fichiercsv :
    '''for i in range(len(liste_termes)):
        liste_termes[i] = liste_termes[i].encode()
    '''
    writer = csv.writer(fichiercsv)
    writer.writerow([''] + list(dico_freq.keys()))
    for i in range(len(fichiers)):
        liste_temp = [str(fichiers[i])]
        for j in range(len(dico_freq)):
            liste_temp = liste_temp + [matrice[i][j]]
        writer.writerow(liste_temp)
    fichiercsv.close()

	
