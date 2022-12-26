# -*- coding: utf-8 -*-

import codecs
import unicodedata
import re
import os

def extract(mpath):   
    # cration du fichier "ramtolist_t.txt" 
    with open('ramtolist_t.txt', 'w', encoding='UTF-8') as fil:
        fil.write("")
        fil.close()
        
    # fichier Unimarc
    f = codecs.open('{}.txt'.format(mpath), encoding = "utf8")

    lines = f.readlines()

    '''Encodage'''
    
    def encodage(data_str):
        output_data = []
        for mot in data_str.split() :
            output_data.append(unicodedata.normalize('NFKD', mot).encode('ascii', 'ignore').decode('ascii'))
        return ' '.join(output_data)    
    
    for i in range(len(lines)) :
        lines[i] = encodage(lines[i])
    
    ''' Recuperation des donnees'''
    
    data = {}
    terme = ''
    equ = [] # termes equivalents
    spec = [] # termes specifiques (en-dessous)
    gen = [] # termes generiques (au-dessus)
    rej = []
    
    for line in lines : 
        line = line.split()
        for i in range(len(line)):
            line[i].strip()
        if line:
            if line[0] == '250': # recuperation du terme
                liste_terme = [line[i] for i in range(8, len(line))]
                liste_terme = [elem.replace('$x', '--') for elem in liste_terme]
                terme = " ".join(liste_terme)
            if line[0] == '450': #recuperation des formes rejetées
                liste_rej = [line[i] for i in range(8, len(line))]
                liste_rej = [elem.replace('$x', '--') for elem in liste_rej]
                rej = rej + [' '.join(liste_rej)]
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
                data[terme.encode()] = {'equivalent':[equi.encode() for equi in equ], 'specifique':[speci.encode() for speci in spec],'generique':[gene.encode() for gene in gen], 'rejetees':[reje.encode() for reje in rej]}
                terme = ''
                equ = []
                spec = []
                gen = []
                rej = []
    
    
    ''' Construction des couples'''
    
    liste_termes_lies = list(data.keys())
    for k1 in data :
        for k2 in data[k1] :
            for word in data[k1][k2] :
                if word not in liste_termes_lies :
                    liste_termes_lies.append(word)
              
    nlis = []
    flis = []
    #nettoyage
    for i in liste_termes_lies:
        liste_termes_lies[liste_termes_lies.index(i)] = liste_termes_lies[liste_termes_lies.index(i)].decode('UTF-8')
    for j in liste_termes_lies:
        if '--' in liste_termes_lies[liste_termes_lies.index(j)] :
            a = liste_termes_lies[liste_termes_lies.index(j)].split(" -- ")
            nlis.append(a[0])
            nlis.append(a[1])
        elif ' (' in liste_termes_lies[liste_termes_lies.index(j)]:
            b = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", liste_termes_lies[liste_termes_lies.index(j)])
            b = re.sub("[\(\[].*?[\)\]]", "", b)
            nlis.append(b)
        elif ', ' in liste_termes_lies[liste_termes_lies.index(j)]:
            z = liste_termes_lies[liste_termes_lies.index(j)].split(', ')
            nlis.append(z[0])
        elif '$a' in liste_termes_lies[liste_termes_lies.index(j)] :
            w = liste_termes_lies[liste_termes_lies.index(j)].split("$a ")
            nlis.append(w[0])
        elif '$y' in liste_termes_lies[liste_termes_lies.index(j)] :
            w = liste_termes_lies[liste_termes_lies.index(j)].split("$y ")
            nlis.append(w[0])
        elif '$z' in liste_termes_lies[liste_termes_lies.index(j)] :
            w = liste_termes_lies[liste_termes_lies.index(j)].split("$z ")
            nlis.append(w[0])
        else:
            nlis.append(liste_termes_lies[liste_termes_lies.index(j)])
    
    for j in nlis:
        if ' (' in nlis[nlis.index(j)]:
            c = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", nlis[nlis.index(j)])
            c = re.sub("[\(\[].*?[\)\]]", "", c)
            flis.append(c)
        elif ', ' in nlis[nlis.index(j)]:
            x = nlis[nlis.index(j)].split(', ')
            nlis.append(x[0])
        elif '$a' in nlis[nlis.index(j)] :
            w = nlis[nlis.index(j)].split("$a ")
            nlis.append(w[0])
        elif '$y' in nlis[nlis.index(j)] :
            w = nlis[nlis.index(j)].split("$y ")
            nlis.append(w[0])
        elif '$z' in nlis[nlis.index(j)] :
            w = nlis[nlis.index(j)].split("$z ")
            nlis.append(w[0])
        else:
            flis.append(nlis[nlis.index(j)])
    
    #inserer dans fichier texte
    with open('ramtolist_t.txt', 'a', encoding='UTF-8') as fil:
        for i in flis:
            fil.write(''.join(str(flis[flis.index(i)])) + '\n')
        
    if os.path.exists('ramtolist1.txt') == False:
        ramnum = str(1)
    else:
        ramnum = str(2)
    
    #enlever lignes vides
    with open('ramtolist_t.txt') as infile, open('ramtolist{}.txt'.format(ramnum), 'w') as outfile :
        for line in infile:
            if not line.strip(): continue
            outfile.write(line)
