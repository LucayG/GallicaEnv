# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 14:11:25 2022

@author: Lucie
"""

import sys
import codecs

'''CHEMIN DU FICHIER TXT A PASSER EN ARGUMENT'''
if __name__ == '__main__':
    if len(sys.argv) > 1: 
        path = sys.argv[1]
    else: 
        path = input("Veuillez entrer le chemin du fichier txt : ")
        
f = codecs.open(path, encoding = "utf8").readlines()

with open('nouveau.txt', 'w', encoding = 'utf8') as fic :
    for line in f :
        a = True
        if line.endswith('.\n') or line.endswith(',\n'):
            line = line[:len(line)-2]+'\n'
        line_split = line.split()
        for i in range(len(line_split)):
            if line_split[i].startswith('(') and a:
                line_temp = ' '.join(line_split[0:i])
                fic.write(line_temp+'\n')
                a = False
        if a == True:
            fic.write(' '.join(line_split)+'\n')
            
                
    


