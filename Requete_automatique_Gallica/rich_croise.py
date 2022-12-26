# -*- coding: utf-8 -*-
import html
import sys
import pandas as df
import os
from collections import Counter
import itertools
try:
    from search import Search
except ModuleNotFoundError :
    print("Problème de module : préciser path (par exemple < ~\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages >)\n")
    #sys.path.append('C:/Users/Lucie/AppData/Roaming/Python/Python310/site-packages')
    #Decommenter la ligne ci-dessus et mettre le path directement si le probleme apparait a chaque fois
    from search import Search
from script_extraction_short import extract
from refine import refine_it
from findItem import finditem 
import requests
import urllib
import re
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
import csv
try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                import cElementTree as etree
            except ImportError:
                try:
                    import elementtree.ElementTree as etree
                except ImportError:
                    print("okay, something is seriously wrong with the package's installation.")

    ''' Clean Start (just in case) '''

if os.path.exists('GAL.txt'):
    os.remove('GAL.txt')   
if os.path.exists('arkgal.txt'):
    os.remove('arkgal.txt')
if os.path.exists('arkgal2.txt'):
    os.remove('arkgal2.txt')
if os.path.exists('ramtolist1.txt'):
    os.remove('ramtolist1.txt')
if os.path.exists('ramtolist2.txt'):
    os.remove('ramtolist2.txt')
if os.path.exists('ramtolistcouples.txt'):
    os.remove('ramtolistcouples.txt')
if os.path.exists('ramtolist_t.txt'):
    os.remove('ramtolist_t.txt')
if os.path.exists('content.txt'):
    os.remove('content.txt')
if os.path.exists('content2.txt'):
    os.remove('content2.txt')
if os.path.exists('tables.xml'):
    os.remove('tables.xml')
if os.path.exists('pages.txt'):
    os.remove('pages.txt')
if os.path.exists('pages2.txt'):
    os.remove('pages2.txt')


print("Vous allez pouvoir faire une requête sur Gallica avec des couples de mots !\n")

''' Couple combinations '''

lst1 = [] 
lst2 = []

try :
	fil_one = input("Nom du fichier 1 (sans l'extension .txt)\n")
except FileNotFoundError :
	print("Nous n'avons pas trouvé le fichier ! Vérifiez l'orthographe et son emplacement.\n")
	fil_one = input("Nom du fichier 1 (sans l'extension .txt)\n")
try :
	fil_two = input("Nom du fichier 2 (sans l'extension .txt)\n")
except FileNotFoundError :
	print("Nous n'avons pas trouvé le fichier ! Vérifiez l'orthographe et son emplacement.\n")
	fil_two = input("Nom du fichier 2 (sans l'extension .txt)\n")

with open('{}.txt'.format(fil_one), 'r') as firstfile, open('ramtolist1.txt','w') as secondfile:
	for line in firstfile:     
		secondfile.write(line.strip())
		lst1.append(line.strip())
with open('{}.txt'.format(fil_two), 'r') as firstfile, open('ramtolist2.txt','w') as secondfile:
	for line in firstfile:               
             	secondfile.write(line.strip())
             	lst2.append(line.strip())

pairs = itertools.product(lst1, lst2)
lstf = [pair for pair in pairs if pair[0] != pair[1]]
with open('ramtolistcouples.txt','w') as secondfile:
	for line in lstf:
            	secondfile.write(str(line) + "\n")      

try :
    print("> " + str(len(lstf)) + " couples !")
    print("\n Liste des couples: ", lstf, "\n\n")
except MemoryError :
    print("can't print lists because of MemoryError !")


''' Corpus selection '''

#proximity between two words inside the same documents, token-wise
prox_is = input("Traiter par proximité à combien de mots ? (n'importe quel nombre, ne rien mettre pour une recherche de deux mots sans critère de proximité)\n")
try:
    if prox_is == '' or int(prox_is) < 1:
        prox_is = None
except ValueError:
    prox_is = None

# recherche par expansion
souple = ""
while souple!="o" and souple !="n":
	souple = input("Souhaitez-vous effectuer une recherche souple (possibilité d'une lettre différente) ? (o/n)\n")

# taux d'ocr minimal
taux_ocr = float(input("Quel taux d'ocr minimal souhaitez-vous ? (nombre entre 0 et 100, ne rien mettre pour tout conserver)\n"))

#document type
requ_dctype = input("Type de document ? Ecrire sous la forme < document, document, ... > ; par exemple < manuscrit, monographie > ou < manuscrit > .  \nListe des options : monographie, manuscrit. Ne rien mettre pour ne pas l'avoir en critère.\n")
if requ_dctype == '':
    requ_dctype = None
    
#family names of authors
requ_dccreator = '"'+ input("Par auteur(s) ? Ecrire sous la forme < auteur, auteur, ... > ; par exemple < Ilf, Petrov > ou < Hugo > . Ne rien mettre pour ne pas l'avoir en critère.\n")+'"'
if requ_dccreator == "''" or requ_dccreator == '""':
    requ_dccreator = None
    
#titles of documents
requ_dctitle = "'"+input("Par titre ? Ecrire sous la forme < titre, titre > .Ne rien mettre pour ne pas l'avoir en critère.\n")+"'"
if requ_dctitle == "''":
    requ_dctitle = None

#themes or subthemes
whichdewey = input("Par thème, sous-théme ou sans thème ? Se referer à https://www.oclc.org/content/dam/oclc/dewey/resources/summaries/deweysummaries.pdf pour plus d'informations. \nEntrer <dewey> pour un thème général, comme 'Littérature' ou 'Histoire&Géographie' \nEntrer <sdewey> pour une sous-thématique comme Loi, Linguistique ou Agriculture. Ne rien entrer pour ne pas selectionner de théme.\n")
whichdewey = re.sub('<>', '', whichdewey.lower())
#ask for a general theme : from 0 to 9
if whichdewey == 'dewey':
    requ_dewey = input("Thème : Entrer un chiffre entre 0 et 9 ; par exemple < 8 > pour Littérature. Liste des thèmes : 0 = Généralités, 1 = Philosophie et psychologie, 2 = Religion, 3 = Économie et société, 4 = Langues, 5 = Sciences, 6 = Techniques, 7 = Arts et loisirs, 8 = Littérature, 9 = Histoire et géographie.\n")
    dew = True
#ask for a subtheme : from 00 to 99. Note : "sub-subthemes" (000 to 999) can't be found in the xml structure of documents
elif whichdewey == 'sdewey':
    requ_dewey = input("Sous-Thème : Entrer un chiffre entre 00 et 99 ; par exemple < 63 > pour Agriculture. Plus d'informations ici : https://www.oclc.org/content/dam/oclc/dewey/resources/summaries/deweysummaries.pdf \n")
    dew = False
else:
    dew = True
    requ_dewey = None
    
#Librairie 
requ_Lib = "'"+input("Par bibliothèque ? Par exemple < bibliotheque nationale de france >. Ne rien mettre pour ne pas l'avoir en critère.\n")+"'"
if requ_Lib == "''":
    requ_Lib = None

#Ces parametres ne fonctionnent pas (encore !) sur le site de Gallica
requ_format = None
requ_geo = None
requ_langue = None

#date of documents, between "from" and "until" or both at the same time for a given period.
datefrom = input("Date : A partir de quand ? Sous la forme < YYYY(MMJJ) > ; par exemple < 1567 > ou < 17890505 > . Ne rien mettre s'il n'y a pas de date minimale.\n")
dateuntil = input("Jusqu'à quand ? Sous la forme < YYYY(MMJJ) >. Ne rien mettre s'il n'y a pas de date maximale. Si seule l'année est indiquée, mois et jour seront 1er Janvier par défaut. \n")
if datefrom != '' and dateuntil != '':
    requ_dcdate = '< "'+dateuntil+'" and dc.date > "'+datefrom+'"'
elif datefrom != '' and dateuntil == '':
    requ_dcdate = '> "'+datefrom+'"'
elif datefrom == '' and dateuntil != '':
    requ_dcdate = '< "'+dateuntil+'"'
elif datefrom == '' and dateuntil == '':
    requ_dcdate = ''
else:
    print("\n --format incorrect-- \n")
    requ_dcdate = ''

with open('arkgal.txt', 'w') as f:
    f.write('')

anss = 'y'

#how many of the richest pages to keep
nb_pag = input("Combien de pages faut-il garder dans le résultat final ? Les pages les plus riches seront celles préservées. Ne rien écrire pour tout garder.\n")
if nb_pag :
	nb_pag = int(nb_pag)
else :
	nb_pag = -1

''' Searching for Documents '''

#for every search words couples, find the gallica documents and take their url ark links
for i in lstf:
    if prox_is :
        print("Couple testé par proximité de " + str(prox_is) + " : " + str(i), "\n")
    else:
        print("\nMots testés : " + str(i))
    if __name__ == '__main__':
        
        #find the gallica documents        
        if dew:
            #if by theme            
            Searc = Search(prox_is, str(i), requ_dctype, requ_dccreator, requ_dctitle, requ_dcdate, requ_Lib, requ_format, requ_geo, requ_langue, True, dewey = requ_dewey, expansion=souple)
        else:
            #if by subtheme or no (sub)theme
            Searc = Search(prox_is, str(i), requ_dctype, requ_dccreator, requ_dctitle, requ_dcdate, requ_Lib, requ_format, requ_geo, requ_langue, True, sdewey = requ_dewey, expansion=souple)
        
        nbx = Searc.execute(worden = str(i))
        #extract info from the gallica documents
        if nbx != -1:
            for j in range(0, nbx): # for every fifty / every subfile of a given pair of words
                print("Refining #" + str(j))
                l = refine_it('gallica{}.xml'.format(str(i) + '_' + str(j)), str(i), str(j), prox_is, taux_ocr)
                if l == 'stop':
                    print("removing " + 'gallica{}.xml'.format(str(i) + '_' + str(j)))
                    os.remove('gallica{}.xml'.format(str(i) + '_' + str(j)))
                

#clean the duplicate links
with open('arkgal.txt') as result:
    uniqlines = set(result.readlines())
    with open('arkgal2.txt', 'w') as rmdup:
        rmdup.writelines(set(uniqlines))
with open('pages.txt', 'w', encoding=('utf-8')) as pag:
    pag.write('')
with open('content.txt', 'w', encoding=('utf-8')) as pag:
    pag.write('')
    
    ''' Scoring Pages '''
otu = {}
otupage = {}
scorep = {}
scorep2 = {}
condict = {}
listmot=[]
listpage=[]
conttext={}

#get individual pages and (optionnally) excerpts, for each word, for each ark
with open('arkgal2.txt', 'r') as arkg, open('ramtolistcouples.txt', 'r') as ram:
    initial = 'https://gallica.bnf.fr/services/ContentSearch?ark='
    end = '&query='
    lines = arkg.readlines()
    linez = ram.readlines()
    
    #for each ark document
    for arkline in lines:        
        print('\n' + str(lines.index(arkline)) + ' out of ' + str(len(lines)) + ' links\n')
        narkline = arkline.split("/")[5]
        print("Scoring document : " + str(narkline))
        print('Arkline   :  ', arkline)
        #for each single word
        for ramline in linez :
            ramline = ramline.replace("(", "").replace(")","")
            ramline_1 = ramline.split(",")[0].strip().strip("'")
            ramline_2 = ramline.split(",")[1].strip().strip("'")
            print("Scoring words : " + str(ramline))
            link = initial + narkline + end + "%22" + ramline_1 + "%22%20" + "prox/unit=word/distance="+str(prox_is) + "%20%22" + ramline_2 + "%22"
            page = requests.get(link)
            try:
                extr_html = etree.fromstring(page.content)
            except:
                print("FAILED LINK : " + str(link))
            page_id = extr_html.findall('.//p_id')
            if anss == 'y':                
                content_id = extr_html.findall('.//content')
            
            
            tlist = []
            #associate scores to each page
            with open('pages.txt', 'a', encoding=('utf-8')) as pag, open('content.txt', 'a', encoding=('utf-8')) as cont:
                
                #fill informative documents and lists, and extract excerpts
                for i in page_id:
                    tlist.append(i.text + '_' + narkline + arkline[-6:])
                    pag.write(i.text + '_' + narkline + "\n")
                    if anss == 'y':
                        content_clean = html.unescape(content_id[page_id.index(i)].text.replace("<span class='highlight'>", "").replace("</span>", ""))
                        cont.write(i.text + '_' + narkline + '-' +  content_clean + "\n")
                        jump = content_clean
                        page=i.text
                        if narkline not in conttext.keys():
                            conttext[narkline]={}
                        if page in conttext.get(page,{}):
                            temp = conttext.get(narkline, {}).get(page)
                            
                            temp=str(temp) + '   ************************* ' +jump
                         
                            conttext[narkline][page]= temp
                        if page not in conttext[narkline].keys():
                            conttext[narkline][page]= jump
                      
                #Score is UNIQUE OCCURENCES (OU); Also gets ocr rate
                for j in tlist:
                    clef = j[:-6]
                    if clef in scorep.keys():                        
                        scorep[clef][0] += 1
                    else:                               
                        scorep[clef] = [1, str(j[-6:-2])]
                print("SCOREP : ", scorep)
                #Score is TOTAL OCCURENCES (OT)
                for k in tlist :
                    clef = k[:-6]
                    simplepage = re.sub(r'[PAG_bpt]', '' , k[:10])
                    onpage = '&page=' + re.sub(r'[PAG_bpt]', '' , k[:10])
                    rampage = ramline.replace("'", "").replace("\n","")
                    link = initial + narkline + end + "%22" + ramline_1 + "%22%20" + "prox/unit=word/distance="+str(prox_is) + "%20%22" + ramline_2 + "%22" + onpage

                    page = requests.get(link)
                    page.encoding = "UTF-8"
                    try :
                    	root = etree.fromstring(page.content)
                    	try:
                        	q = root[1][0][0].attrib
                        	counting = re.sub(r'[^\d]', '', str(q))
                    	except IndexError:
                        	counting = 0
                    except :
                    	counting = 0
                    
                    if clef in scorep2.keys():
                        scorep2[clef] += int(counting)
                    else:
                        scorep2[clef] = int(counting)


                    if narkline not in otu.keys():
                        otupage[narkline]={}
                        otu[narkline]={}
                    if rampage in otu[narkline].keys():
                        otu[narkline][rampage]=otu[narkline][rampage] + int(counting)
                    else :
                        otu[narkline][rampage]=int(counting)
                    if simplepage not in otupage[narkline].keys():
                        otupage[narkline][simplepage]={}
                    if rampage in otupage[narkline][simplepage].keys():
                        otupage[narkline][simplepage][rampage]=otupage[narkline][simplepage][rampage] + int(counting)
                    else :
                        otupage[narkline][simplepage][rampage]=int(counting)

                tlist = []
    
    ''' Averaging '''
    
    scorep_mix = {}
    #create an average score, between OU and OT
    for key, value in scorep.items():
        try:
            aver = "{:.2f}".format(((scorep[key][0] + scorep2[key]) / 2 ))
        except KeyError:
            print(str(scorep2))
            continue
        scorep_mix[key] = (scorep[key][0], scorep[key][1], scorep2[key], float(aver))
        print("scores : " + str(scorep_mix[key]))
        
        #only keep a certain number of pages, the richest ones based on the average between OU and OT
        if True :
            tempdict = {}
            a = 0
            for key, value in scorep_mix.items():
                tempdict[key] = scorep_mix[key][3]
                a += 1
            if nb_pag != -1:
            	tempdict = dict(Counter(tempdict).most_common(nb_pag))
            else : 
            	tempdict = dict(Counter(tempdict).most_common())
            realdict = {}
            for key, value in tempdict.items():
                if key in scorep_mix.keys():
                    realdict[key] = (scorep_mix[key][0], scorep_mix[key][1], scorep_mix[key][2], tempdict[key])
        else:
            print("Taking all the pages since no request was made")
        
    ''' Charting Results '''
     
    #create csv with all the interesting informations
    
    with open('tables.xml', 'w', encoding = 'utf-8', newline='') as tab:
        nb_rows = 1
        writer = csv.writer(tab)
        header = ['Match', 'Page', 'ARK', 'L1 x OU', 'L1 x OT', 'Occurance Mot', 'Taux OCR', 'Score Moyen' , 'Titre', 'Auteur', "Date d'édition",'Lien Gallica', 'Lien Image', 'Lien Gallica Page', 'Lien OCR', 'Context']
        writer.writerow(header)
        #for every page
        if 'realdict' not in globals():
            print(" Aucun document n'a été trouvé ")
            exit()
           
        for key, value in realdict.items():
            if value[3] <= 0.5 : 
                continue
            else:
                smallark = str(re.sub(r'PAG_\d*_','', key))     #SIMPLE ARK              
                trawpage = str(re.sub(r'PAG_','', key))[:4]     #2360_
                rawpage = str(re.sub(r'[bpt_v]','', trawpage))  #2360_bpt6k98002169
                smallpage = str('PAGE_' + rawpage)              #PAGE_###
                pageconttext = str('PAG_' + rawpage)          
                iniurl = 'https://gallica.bnf.fr/ark:/12148/'   #
                urlpage = '/f' + rawpage + '.item'              #/f310.item
                imgpage = '/f' + rawpage + '.highres'           #/f25.highres
                smallKEY = iniurl + smallark
                bigKEY = iniurl + smallark + urlpage
                imgKEY = iniurl + smallark + imgpage
                ocrlink = bigKEY + '/texteBrut'
                try :
                	OU= str(len(otupage[smallark][rawpage].keys()))
                except KeyError :
                	continue
                OUMot = re.sub(r'(,)','',OU)
                scrmoy = list(otupage[smallark][rawpage].values())
                scr = 1
                for i in range(len(scrmoy)):
                	scr = scr*scrmoy[i]

                #extraire titre date pub et auteur
                allthings = finditem(ocrlink)
                
                data = ['Match-' + str(nb_rows), smallpage, smallark, OUMot, str(value[2]), otupage[smallark][rawpage] ,str(value[1]), scr, str(allthings[0]), str(allthings[2]), str(allthings[1]), smallKEY, imgKEY, bigKEY, ocrlink, conttext[smallark][pageconttext]]            
                writer.writerow(data)
                nb_rows += 1
                listmot.append(otupage[smallark][rawpage])
                listpage.append(ocrlink)

dictvectorizer = DictVectorizer(sparse=False)
features = dictvectorizer.fit_transform(listmot)
feature_name =dictvectorizer.get_feature_names_out()
            

mot_list_final=[]
with open('matrix.xml', 'w', encoding = 'utf-8', newline='') as tabss:
    writer = csv.writer(tabss)
    listpage.insert(0,'Mot')
    j=0
    mot_list_final.append(listpage)

    for i in feature_name:
        tmp = [item[j] for item in features]
        tmp.insert(0,i)
        mot_list_final.append(tmp)
        
        j+=1
    writer.writerows(mot_list_final)
    
    
'''Cleaning and Tidying up '''
with open('finallist.xml', 'w', encoding = 'utf-8', newline='') as tabss:
    writer = csv.writer(tabss)
    writer.writerow(otu)
#final step, put the documents in a folder
print("Scoring done, documents written, beginning cleaning")

folnb = 0
while os.path.exists('Depot_Gallica{}'.format(str(folnb))):
    folnb += 1
os.makedirs('Depot_Gallica{}'.format(folnb))
Path("arkgal2.txt").rename("Depot_Gallica{}/Liens_ARK.txt".format(str(folnb)))
Path("content.txt").rename("Depot_Gallica{}/Extraits.txt".format(str(folnb)))
Path("ramtolistcouples.txt").rename("Depot_Gallica{}/Liste_1.txt".format(str(folnb)))
Path("tables.xml").rename("Depot_Gallica{}/Tableau.xml".format(str(folnb)))
Path("matrix.xml").rename("Depot_Gallica{}/matrix.xml".format(str(folnb)))

#remove residual text and xml files
for file in os.scandir():
    if (file.name.endswith(".txt") and not file.name.startswith(fil_one) and not file.name.startswith(fil_two)) or file.name.endswith(".xml"):
        os.unlink(file)
print("Operation finished")
