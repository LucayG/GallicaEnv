import urllib.request 
from bs4 import BeautifulSoup

#Script pour extraire la page sur gallica, en un corpus


file_input = input("Nom du fichier contenant les arks (avec l'extension .txt) : ")

entete = input("Souhaitez-vous conserver l'entête des documents ? (o/n) ")

limite = "Le taux de reconnaissance estimé pour ce document est de "

nb = 0

with open (file_input, 'r') as file, open("corpus.txt", 'w') as file_output, open("correspondances.txt", "w") as file_match:
	for ark in file:
		nb +=1
		ark = ark.rstrip("\n")
		try :
			html = urllib.request.urlopen(ark)
		except urllib.request.HTTPError :
			print("Une erreur de reseau a été détectée, le résultat peut être incomplet")
			continue
		htmlParse = BeautifulSoup(html, 'html.parser')
		liste=[]
		liste_entete = []
		a = False
		for para in htmlParse.find_all("p"):
			if a:
				liste.append(para.get_text())
			else :
				liste_entete.append(para.get_text())
				if entete=='o':
					liste.append(para.get_text())
			if limite in para.get_text() :
				a = True
		for i in liste:
			file_output.write(i+'\n')
		for i in liste_entete:
			if i.startswith("Titre : "):
				file_match.write("Document "+str(nb)+" : "+ark+'\n')
				file_match.write(i+'\n'+'\n')

            
