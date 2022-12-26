# -*- coding: utf-8 -*-

import json
import re
import codecs
import os

'''
input : fichier .JSON ou txt d'un dictionnaire ou d'une encyclopedie numerisee
output : 
    un fichier txt contenant la liste des termes
    un fichier txt contenant les titres + blocs
    un fichier txt contenant les termes dans leur contexte (optionnel)
    un fichier txt contenant les regles de selection
    un fichier txt contenant les doublons
    un fichier txt contenant les termes en desordre alphabetique
    un fichier txt contenant les termes a la suite se ressemblant
'''

'''Expressions regulieres : a rentrer entre guillemets sans espaces
    [A-Z][A-Z]+\.  --> sequence de majuscules avec point
    [A-Z][A-Z]+\,  --> sequence de majuscules avec virgule
    (?:[A-Z][A-Z]+ )*[A-Z][A-Z]+\.  --> sequence de plusieurs mots en majuscule, le dernier finissant avec un point
    [A-Z][A-Z](?:[^.,])*[A-Z]\.  --> sequence de 2 maj, n'importe quoi != . ou , puis maj avec point
    \n[A-Z][A-Z](?:[^.,\n])*[A-Z]\.  --> idem mais avec un retour a la ligne avant
    \n[A-Z][A-Z](?:[^.,\n])*\)\.  --> idem mais finissant avec une parenthese fermante et un point
    ([A-Z][A-Z]+ )([A-Z][A-Z]+ )([A-Z][A-Z]+\.)  --> 3 mots en maj, le dernier finit avec un point
    [A-Z](?:[^.,])*[A-Z]  --> premiere lettre majuscule et derniere lettre majuscule
'''

n = int(input("Entrez le numéro d'essai : "))
os.mkdir("Essai_"+str(n))

print("Des que vous donnez une liste d'indices, separez les mots avec le symbole '$' (ex : 1$2$56$90)")

print("Les expressions regulieres, s'il y en a plusieurs, sont a donner entre guillemets et sans espace entre elles.")
print("Si vous utilisez des parentheses dans votre expression reguliere, ecrivez ?: apres la premiere parenthese.")

'''DONNEES JSON

#Recuperation des donnees json dans un dictionnaire

#with open('Nouveau_Dictionnaire_histoire_nat.JSON') as json_data :
#with open('1905_Dictionnaire_populaire_illustre_dhistoire_naturelle.JSON') as json_data :
with open('1857-1859_Nouveau_dictionnaire_dhistoire_naturelle.JSON') as json_data :
#with open('Dictionnaire_raisonne_universel.JSON') as json_data :
    data_dict = json.load(json_data)
    json_data.close()
    
#Creation d'une liste contenant toutes les sequences de mots (listes de mots)

big_content = [] # liste de listes
for k1 in data_dict['Text_Blocks'].keys():
    big_content.append(data_dict['Text_Blocks'][k1]['Content'].split())
    
#Conversion en str

big_content_fusionne = [] # liste simple
for sequence in big_content:
    big_content_fusionne += sequence

big_str = ' '.join(big_content_fusionne) # str
'''

'''DONNEES TXT'''

with open("Encode_Dictionnaire_1857_Tome_1.txt", encoding = 'utf8') as f: # path a changer
    big_str = f.read()
    f.close()
    
#big_str = big_str.replace('É','E') # PROBLEME des caracteres accentues non reconnus comme des majuscules

'''Creation de la liste de termes'''

def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]

def creation_liste_de_termes(content_str):
    liste_patrons = []
    args = input('Entrez les patrons : ').split('"')
    for i in range(len(args)) :
        if args[i]!='' and args[i]!=' ':
            liste_patrons.append(re.compile(args[i]))
    termes = []
    for i in range(len(liste_patrons)):
        termes += re.findall(liste_patrons[i], content_str)
    for i in range(len(termes)):
        if termes[i].startswith('\n'):
            termes[i] = termes[i][1:len(termes[i])]
    termes = manipulations_termes(termes)
    termes.sort(key=len, reverse = True)
    liste_temp = []
    doublons = []
    for i in range(len(termes)):
        if termes[i] not in liste_temp :
            liste_temp.append(termes[i])
        else :
            doublons.append(termes[i])
    termes = unique(termes)
    doublons = unique(doublons)
    dico_termes = {}
    for i in range(len(termes)):
        dico_termes[i] = termes[i].strip()
    return dico_termes, args, doublons

def fichier_liste_termes(dico):
    with codecs.open('Essai_'+str(n)+'/liste_termes_'+str(indice)+'.txt','w', encoding = 'utf8') as fic:
        for (key,value) in dico.items():
            fic.write(str(key)+ " : "+value+"\n")
    fic.close()
    
''' Manipulations sur la liste des termes'''

def manipulations_termes(liste_termes):
    '''desordre'''
    dico_desordre_alphabetique = desordre(liste_termes)
    fichier_desordre_alphabetique(dico_desordre_alphabetique)
    answer_desordre = input('Donnez la liste des termes en desordre que vous souhaitez conserver (INDICES) (T si vous souhaitez tout conserver) : ').split('$')
    if answer_desordre != ['T']:
        liste_termes = selection_termes_desordre(dico_desordre_alphabetique, liste_termes, answer_desordre)
    '''commun'''
    dico_mot_commun = mot_commun(liste_termes)
    fichier_mot_commun(dico_mot_commun)
    print('\nSi les termes ayant des mots communs sont des doublons, il est conseille de les conserver')
    answer_commun = input('Donnez la liste des termes ayant des mots en commun que vous souhaitez conserver (INDICES) (T si vous souhaitez tout conserver) : ').split('$')
    if answer_commun!=['T']:
        liste_termes = selection_termes_commun(dico_mot_commun, liste_termes, answer_commun)
    return liste_termes
    

'''Termes en desordre (alphabetique)'''

def desordre(liste_mots):
    output_dico = {}
    j=0
    for i in range(len(liste_mots)):
        try:
            liste_temp_1 = []
            liste_temp_1.append(liste_mots[i-2])
            liste_temp_1.append(liste_mots[i-1])
            liste_temp_1.append(liste_mots[i])
            liste_temp_1.append(liste_mots[i+1])
            liste_temp_1.append(liste_mots[i+2])
            liste_temp_2 = []
            liste_temp_2.append(liste_mots[i-2])
            liste_temp_2.append(liste_mots[i-1])
            liste_temp_2.append(liste_mots[i+1])
            liste_temp_2.append(liste_mots[i+2])
            if liste_temp_1!=sorted(liste_temp_1) and liste_temp_2==sorted(liste_temp_2):
                output_dico[j] = liste_temp_1
                j+=1
        except IndexError:
            continue
    return output_dico
        
def fichier_desordre_alphabetique(dico_desordre):
    with codecs.open('Essai_'+str(n)+'/termes_en_desordre_'+str(indice)+'.txt','w', encoding = 'utf8') as fic:
        for (key,val) in dico_desordre.items():
            fic.write(str(key)+' : '+dico_desordre[key][2]+'\n')
            fic.write('@' + dico_desordre[key][0] + ' @' + dico_desordre[key][1]+ '    @' + dico_desordre[key][3] + ' @' + dico_desordre[key][4]+'\n')
            fic.write('\n')
    fic.close()
    
def selection_termes_desordre(dico_desordre, liste_mots, liste_indices):
    for key in dico_desordre.keys():
        if str(key) not in liste_indices:
            liste_mots.remove(dico_desordre[key][2])
    return liste_mots

''' Termes a la suite avec mot commun'''

def ont_un_mot_commun(word1,word2):
    word1 = word1.split()
    word2 = word2.split()
    for word in word1 :
        if word in word2 :
            return True
    return False
    
def mot_commun(liste_mots):
    output_dico = {}
    j = 0
    for i in range(len(liste_mots)):
        try :
            if ont_un_mot_commun(liste_mots[i], liste_mots[i-1]) or ont_un_mot_commun(liste_mots[i], liste_mots[i-2]):
                output_dico[j] = [liste_mots[i-2], liste_mots[i-1], liste_mots[i]]
                j+=1
        except IndexError:
            continue
    return output_dico
        
def fichier_mot_commun(dico_commun):
    with codecs.open('Essai_'+str(n)+'/termes_a_la_suite_communs_'+str(indice)+'.txt','w', encoding = 'utf8') as fic:
        for (key,val) in dico_commun.items():
            fic.write(str(key)+' : '+dico_commun[key][2]+'\n')
            fic.write('@' + dico_commun[key][0] + '  @' + dico_commun[key][1] + '  @' + dico_commun[key][2] + '\n')
            fic.write('\n')
    fic.close()
    
def selection_termes_commun(dico_commun, liste_mots, liste_indices):
    for key in dico_commun.keys():
        if str(key) not in liste_indices:
            liste_mots.remove(dico_commun[key][2])
    return liste_mots
            
''' Mise en contexte des doublons pour generer la liste de doublons'''

def doublons_contexte(liste_contexte, nb, doublons):
    dico_doublons_contexte = {}
    i=0
    for elem in liste_contexte:
        liste_temp = []
        a = False
        elem_split = elem.split()
        for word in elem_split:
            if a and word!='@@@':
                liste_temp.append(word)
            if word == '@@@' and not a :
                a = True
            elif word == '@@@':
                a = False
        terme = ' '.join(liste_temp).strip()
        if terme in doublons:
            if terme not in dico_doublons_contexte.keys():
                dico_doublons_contexte[terme] = {i : elem}
            else:
                dico_doublons_contexte[terme][i] = elem
            i+=1
    return dico_doublons_contexte

def fichier_doublons_contexte(dico_doublons_contexte, liste_doublons):
    with codecs.open('Essai_'+str(n)+'/liste_doublons_'+str(indice)+'.txt', 'w', encoding = 'utf8') as fic:
        for terme in liste_doublons :
            try :
                for j in dico_doublons_contexte[terme].keys() : 
                    fic.write(str(j)+' '+terme+' : '+dico_doublons_contexte[terme][j]+'\n')
            except KeyError:
                continue          
    fic.close()
                
    
''' Transformation de big_content en un str avec les termes importants colles les uns aux autres
Et construction du dictionnaire avec les equivalences termes/termes_colles'''


def lier_termes_patrons(data, liste_termes_importants): # retourne str et dictionnaire
    data_str = data
    dico_termes_idx = {}
    dico_positions = {}
    for terme in liste_termes_importants :
        if terme.replace(' ','') in dico_termes_idx.keys() :
            continue
        indice_debut = data_str.find(terme)
        while indice_debut != -1:
            indice_fin = indice_debut+len(terme)-1
            if terme in dico_positions.keys() :
                dico_positions[terme].append((indice_debut, indice_fin))
            else :
                dico_positions[terme] = [(indice_debut, indice_fin)]
            dico_termes_idx[terme.replace(' ','')] = terme
            remplacement=''
            for i in range(len(terme)):
                remplacement += '@'
            data_str = data_str[:indice_debut]+remplacement+data_str[indice_fin+1:]
            indice_debut = data_str.find(terme,indice_fin+1)
    data_str = remplacement_str(data_str, dico_termes_idx, dico_positions)
    return data_str, dico_termes_idx


def remplacement_str(data_str, dico_termes_idx, dico_positions):
    for key in dico_positions.keys() :
        nb_mots = len(key.split())
        remplacement = ''
        for i in range(nb_mots-1):
            remplacement += '@'
        for (indice_debut, indice_fin) in dico_positions[key]:
            data_str = data_str[:indice_debut]+[k for (k,v) in dico_termes_idx.items() if v==key][0]+remplacement + data_str[indice_fin+1:]
    data_str = data_str.replace('@', '')
    return data_str

'''Extraction des termes et de leur bloc de texte dans un dictionnaire '''

def extraction_titres_blocs(data_split, dico_idx, liste_indices):
    dico_extrac = {}
    liste_temp = []
    terme_important = 'debut'
    for i in range(len(data_split)) :
        word = data_split[i]
        boolean = False
        bool2 = True
        if i not in liste_indices :
            for patron in dico_idx.keys():
                if word.__contains__(patron) and bool2:
                    liste_temp.append(word[0:word.find(patron)])
                    dico_extrac[terme_important] = liste_temp
                    terme_important = dico_idx[patron]
                    liste_temp=[word[word.find(patron)+len(patron):]]
                    boolean = True
                    bool2 = False
        if boolean == False:
            if word in dico_idx.keys():
                liste_temp.append(dico_idx[word])
            else :
                liste_temp.append(word)
        if word == data_split[len(content_split)-1]:
            dico_extrac[terme_important] = liste_temp
    del dico_extrac['debut']
    return dico_extrac

def fichier_titre_blocs(dico_extrac, dico_indices, dico_equ):
    with codecs.open('Essai_'+str(n)+'/extraction_titre_bloc_sans_titre'+str(indice)+'.txt','w',encoding = 'utf8') as fic:
        for (key,value) in dico_extrac.items():
            fic.write('@@@'+' '.join([str(k) for (k,v) in dico_indices.items() if v==key])+'@@@'+dico_equ[key]+'\n')
            fic.write('###'+' '.join(value)+"###\n")
            fic.write('\n')
    with codecs.open('Essai_'+str(n)+'/extraction_titre_bloc_avec_titre'+str(indice)+'.txt','w',encoding = 'utf8') as fic:
        for (key, value) in dico_extrac.items():
            fic.write('@@@'+' '.join([str(k) for (k,v) in dico_indices.items() if v==key])+'@@@'+dico_equ[key]+'\n')
            fic.write('###'+key+' '.join(value)+"###\n")
            fic.write('\n')
    fic.close()

'''Extraction des titres dans leur contexte'''

def extraction_titre_contexte(data_split, dico_idx, k):
    liste_titre_contexte = []
    for i in range(len(content_split)) :
        titre_contexte = ''
        for patron in dico_idx.keys():
            if content_split[i].__contains__(patron):
                for ind in range(k,0,-1):
                    try :
                        if content_split[i-ind] in dico_idx.keys():
                            titre_contexte += dico_idx[content_split[i-ind]]+' '
                        else :
                            titre_contexte += content_split[i-ind]+' '
                    except IndexError:
                        titre_contexte+=''
                titre_contexte+=content_split[i][0:content_split[i].find(patron)]+' @@@ '+dico_idx[patron]+' @@@ '+content_split[i][content_split[i].find(patron)+len(patron):]+' '
                for ind in range(1,k+1):
                    try :
                        if content_split[i+ind] in dico_idx.keys():
                            titre_contexte += dico_idx[content_split[i+ind]]+' '
                        else :
                            titre_contexte += content_split[i+ind]+' '
                    except IndexError:
                        titre_contexte+=''
                liste_titre_contexte.append(titre_contexte)
                break
    return liste_titre_contexte

def fichier_titre_contexte(liste_contexte, dico_indices):
    with codecs.open('Essai_'+str(n)+'/mots_en_contexte_'+str(indice)+'.txt','w', encoding = 'utf8') as fic:
        for line in liste_contexte:
            line_split = line.split()
            liste_temp = []
            for i in range(len(line_split)):
                if line_split[i]=='@@@':
                     liste_temp.append(i)
            fic.write('@@@'+' '.join([str(k) for (k,v) in dico_indices.items() if v==' '.join(line_split[liste_temp[0]+1:liste_temp[1]])])+'@@@'+' '.join(line_split[liste_temp[0]+1:liste_temp[1]])+'\n')
            fic.write('###'+line+'###\n')
            fic.write('\n')
        fic.close()
        
'''Fichier regles de selection '''

def fichier_regles_selection(patrons):
    with codecs.open('Essai_'+str(n)+'/regles_de_selection_'+str(indice)+'.txt', 'w', encoding = 'utf8') as fic:
        for patron in patrons:
            fic.write(patron+"\n")
        fic.close()

'''Premiere liste de terme et mots en contexte'''

indice=0
dico_termes, liste_patrons, liste_doublons = creation_liste_de_termes(big_str)
fichier_liste_termes(dico_termes)
big_content_termes_colles, dico_idx_lies = lier_termes_patrons(big_str, list(dico_termes.values()))

content_split = big_content_termes_colles.split() # liste
dico_extraction = extraction_titres_blocs(content_split, dico_idx_lies,[])

k = int(input('Donnez le nombre de mots en contexte (pour les doublons): '))
liste_titre_contexte = extraction_titre_contexte(content_split, dico_idx_lies, k)

dico_doublons_contexte = doublons_contexte(liste_titre_contexte, k, liste_doublons)

fichier_doublons_contexte(dico_doublons_contexte, liste_doublons)
answer_contexte = input("Souhaitez-vous voir tous les mots dans leur contexte ? (y/n) ")
if answer_contexte == 'y':
    fichier_titre_contexte(liste_titre_contexte, dico_termes)
fichier_regles_selection(liste_patrons)


'''Modification des regles de segmentation'''

answer = input("Souhaitez-vous modifier les regles de segmentation du texte ? (y/n) ")

while answer=='y':
    indice +=1
    if input('Souhaitez-vous modifier les patrons ? (y/n) ') == 'y':
        dico_termes, liste_patrons, liste_doublons, data_encode = creation_liste_de_termes(big_str)
    if input("Souhaitez-vous ajouter d'autres mots ? (y/n) ") == 'y':
        print()
        print("Pour donner la liste de mots, ecrire les mots separes par $ (par exemple TOTO$TATA$TUTU).")
        args = input('Donnez la liste des mots a ajouter : ("n" si pas de mots a donner) ').split('$')
        if args==['n']: break
        longueur = len(dico_termes.keys())
        for i in range(longueur, longueur+len(args)):
            dico_termes[i] = args[i-longueur]
    if input("Souhaitez-vous enlever des mots ? (y/n) ") == 'y':
        print()
        print("Pour donner la liste des indices, ecrire les indices separes par $ (par exemple 0$1$2).")
        args = input('Donnez la liste des mots a enlever (INDICES) : ("n" si pas de mots a donner) ').split('$')
        if args==['n']: break
        termes = list(dico_termes.values())
        termes_temp = []
        longueur = len(termes)
        for i in range(longueur):
            if str(i) not in args:
                termes_temp.append(termes[i])
        dico_termes = {}
        for i in range(len(termes_temp)):
            dico_termes[i] = termes_temp[i]
    
    fichier_liste_termes(dico_termes)
    big_content_termes_colles, dico_idx_lies = lier_termes_patrons(big_str, list(dico_termes.values()))
    content_split = big_content_termes_colles.split() # liste
    dico_extraction = extraction_titres_blocs(content_split, dico_idx_lies,[])
    liste_titre_contexte = extraction_titre_contexte(content_split, dico_idx_lies,k)
    dico_doublons_contexte = doublons_contexte(liste_titre_contexte, k, liste_doublons)
    fichier_doublons_contexte(dico_doublons_contexte, liste_doublons)
    if answer_contexte == 'y':
        fichier_titre_contexte(liste_titre_contexte, dico_termes)
    fichier_regles_selection(liste_patrons)
    answer = input("Souhaitez-vous modifier les regles de segmentation du texte ? (y/n) ")

''' Extraction des titres+blocs en supprimant les doublons que l'on ne veut pas '''
    
def position_doublons(dico_doublons_contexte,liste_indices,data_split, dico_idx,k) :
    liste_indices_data = []
    for key in dico_doublons_contexte.keys():
        for i in dico_doublons_contexte[key].keys():
            if str(i) in liste_indices :
                liste_indices_data.append(position_dans_data(key, dico_doublons_contexte[key][i], data_split, dico_idx,k))
    return liste_indices_data
                
def position_dans_data(terme, contexte, data_split, dico_idx,k):
    for i in range(len(data_split)):
        if data_split[i].__contains__([k for k,v in dico_idx.items() if v==terme][0]):     
            try :
                h=0
                for word in contexte.split():
                    if word in data_split[i-7:i+8]:
                        h+=1
            except IndexError:
                return (-1)
            if h>=k+1:
                return i
    return(-1)

'''Polissage des termes'''

def polissage(termes):
    dico_equivalent = {}
    print('\nEcrivez dans un fichier la liste des termes, que vous pouvez modifier ou non\n')
    nouvelle_liste = input('Donnez le chemin du nouveau fichier de termes (ex : Essai_5/nouveau.txt) : ')
    with open(nouvelle_liste,'r', encoding = 'utf8') as fic:
        lines = fic.readlines()
        for i in range(len(termes)):
            ajout = ' '.join(lines[i].split()[2:len(lines[i].split())])
            dico_equivalent[termes[i]] = ajout
    fic.close()
    return dico_equivalent

'''Extraction des titres+blocs'''
                          
answer_doublons = input('Donnez la liste des doublons que vous souhaitez conserver (INDICES) (T si vous souhaitez tout conserver) : ').split('$')
liste_complete = []
for key in dico_doublons_contexte.keys() :
    for i in dico_doublons_contexte[key].keys():
        liste_complete.append(i)
if answer_doublons == ['T']:
    answer_doublons = liste_complete
answer_inverse = set(liste_complete)-set(answer_doublons)
liste_indices_a_supprimer = position_doublons(dico_doublons_contexte, answer_inverse, content_split, dico_idx_lies, k)
dico_extraction = extraction_titres_blocs(content_split, dico_idx_lies, liste_indices_a_supprimer)
dico_equ = polissage(list(dico_termes.values()))
fichier_titre_blocs(dico_extraction, dico_termes, dico_equ)


