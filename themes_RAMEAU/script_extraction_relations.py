# -*- coding: utf-8 -*-

'''
input : fichier txt (format unimarc) recensant les resultats d'une requete dans le catalogue general de la bnf
--> idealement faire d'abord tourner le script pretraitement.py sur le fichier pour l'encodage des caracteres
output : fichier csv contenant la matrice (légendée) des relations entre les thèmes RAMEAU
'''

import sys
import numpy as np
import csv
import codecs

#CHEMIN DU FICHIER TXT A PASSER EN ARGUMENT
if __name__ == '__main__':
    if len(sys.argv) > 1: 
        mpath = sys.argv[1]
    else: 
        print("Veuillez entrer le chemin du fichier txt")
f = codecs.open(mpath, encoding = "utf8")


lines = f.readlines()

''' Recuperation des donnees'''

data = {}
terme = ''
equ = [] # termes equivalents
spec = [] # termes specifiques (en-dessous)
gen = [] # termes generiques (au-dessus)

for line in lines : 
    line = line.split()
    for i in range(len(line)):
        line[i].strip()
    if line:
        if line[0] == '250': # recuperation du terme
            liste_terme = [line[i] for i in range(8, len(line))]
            liste_terme = [elem.replace('$x', '--') for elem in liste_terme]
            terme = " ".join(liste_terme)
        if line[0] == '550': 
            if line[3]=='z': # recuperation des termes equivalents
                if line[14] == '2' :
                    liste_equ = [line[i] for i in range(16,len(line))]
                else :
                    liste_equ = [line[i] for i in range(15,len(line))]
                liste_eq = [elem.replace('$x', '--') for elem in liste_equ]
                equ = equ + [" ".join(liste_eq)]
            if line[3] == 'h': # recuperation des termes specifiques
                if line[11] == '2':
                    liste_spec = [line[i] for i in range(13,len(line))]
                else :
                    liste_spec = [line[i] for i in range(12,len(line))]
                liste_spec = [elem.replace('$x', '--') for elem in liste_spec]
                spec = spec + [" ".join(liste_spec)]
            if line[3] == 'g': # recuperation des termes generiques
                if line[11] == '2' :
                    liste_gen = [line[i] for i in range(13,len(line))]
                else :
                    liste_gen = [line[i] for i in range(12,len(line))]  
                liste_gen = [elem.replace('$x', '--') for elem in liste_gen]
                gen = gen + [" ".join(liste_gen)]
        if '----------------------------------' in line :
            data[terme.encode()] = {'equivalent':[equi.encode() for equi in equ], 'specifique':[speci.encode() for speci in spec],'generique':[gene.encode() for gene in gen]}
            terme = ''
            equ = []
            spec = []
            gen = []
        

''' Construction des couples'''

liste_termes_lies = list(data.keys())
liste_couples = []
for k1 in data :
    for k2 in data[k1] :
        for word in data[k1][k2] :
            if word not in liste_termes_lies :
                liste_termes_lies.append(word)
            liste_couples.append((k1,word))
            
            
'''Construction de la matrice'''

matrice = np.zeros((len(liste_termes_lies),len(liste_termes_lies))) # shape (673,157)
for i in range(len(liste_termes_lies)):
    for j in range(len(liste_termes_lies)):
        if (liste_termes_lies[i],liste_termes_lies[j]) in liste_couples or (liste_termes_lies[j],liste_termes_lies[i]) in liste_couples or liste_termes_lies[i] == liste_termes_lies[j]:
            matrice[i][j] = 1

matrice = matrice.astype(int) # float --> int
print("shape : " + str(np.shape(matrice)))


''' Creation du fichier csv'''

with open("Rameau_{}.csv".format(mpath.split(".")[0]), 'w') as fichiercsv :
    '''for i in range(len(liste_termes)):
        liste_termes[i] = liste_termes[i].encode()
    '''
    writer = csv.writer(fichiercsv)
    writer.writerow([''] + liste_termes_lies)
    for i in range(len(liste_termes_lies)):
        liste_temp = [str(liste_termes_lies[i])]
        for j in range(len(liste_termes_lies)):
            liste_temp = liste_temp + [matrice[i][j]]
        writer.writerow(liste_temp)
    fichiercsv.close()

        


            
            
    
    
