# -*- coding: utf-8 -*-
import urllib.request 
from bs4 import BeautifulSoup
import re

# url = 'https://gallica.bnf.fr/ark:/12148/bpt6k5625980p/texteBrut'
def finditem(ark):
	try :
		html = urllib.request.urlopen(ark)
	except urllib.error.HTTPError :
		return["Nan","Nan","Nan"]
	htmlParse = BeautifulSoup(html, 'html.parser')
	title=''
	pubdate=''
	autor=''
	for para in htmlParse.find_all("p"):
		if 'Auteur :' in para.get_text():
			j = re.sub(r"Auteur : ", "", para.get_text())
			j = re.sub(r"Auteur du texte", "", j)
			autor = autor+j
		if "Date d'édition :" in para.get_text():
			j = re.sub(r"Date d'édition : ", "", para.get_text())
			pubdate = pubdate+j
		if "Titre :" in para.get_text():
			j = re.sub(r"Titre : ", "", para.get_text())
			title=title+j
	allthings= [title,pubdate,autor]  
	return allthings
        
    
