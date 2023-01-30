import urllib.request 
from bs4 import BeautifulSoup
import os

#Script pour extraire la page sur gallica par titre (plusieurs fichiers generes)


try :
	os.mkdir("Resultat")
except FileExistsError:
	print("Supprimez ou déplacez le répertoire 'Résultats' existant déjà !")
	raise FileExistsError
file_input = input("Nom du fichier contenant les arks (avec l'extension .txt) : ")

limite = "Le taux de reconnaissance estimé pour ce document est de "

entete = input("Souhaitez-vous conserver l'entête des documents ? (o/n) ")

nb = 0


with open (file_input, 'r', encoding='utf8') as fic:
	for ark in fic:
		nb += 1
		ark = ark.rstrip("\n")
		try:
        		html = urllib.request.urlopen(ark)
		except urllib.request.HTTPError:
			print("Une erreur de reseau a été détectée, le résultat peut être incomplet")
			continue
		htmlParse = BeautifulSoup(html, 'html.parser')
        
		liste=[]
		liste_entete=[]
		a=False
		for para in htmlParse.find_all("p"):
			if a:
				liste.append(para.get_text())
			else :
				liste_entete.append(para.get_text())
				if entete=='o':
					liste.append(para.get_text())
			if limite in para.get_text() :
				a = True
		for j in liste_entete :
			if j.startswith("Titre : "):
				titre = j.replace("Titre : ", "")
				with open("Resultat/"+ str(nb)+ "_" + titre[:10] + ".txt", "w", encoding='utf8') as title_file, open("Resultat/correspondances.txt", "a", encoding='utf8') as file_match:
					for i in liste:
						title_file.write(i)
					file_match.write("Document "+str(nb)+" : "+ark+'\n')
					file_match.write("Nom du fichier : " + str(nb)+ "_" + titre[:10] + ".txt\n")
					file_match.write(j+'\n'+'\n')
            
