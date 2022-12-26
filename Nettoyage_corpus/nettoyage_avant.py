import re

#Script nettoyage pour enlever tous les stopwords, il faut fournir la liste de stopwords et le corpus de travail a nettoyer

file_stopwords = input("Fichier txt contenant la liste des mots à retirer (avec l'extension .txt) : ")

with open(file_stopwords, "r") as f: #fichier qui contient liste de stopwords
    my_stopwords = f.read()
    my_stopwords = my_stopwords.split()

def remove_mystopwords(text):
    token = text.lower()
    token = re.sub("\d+", "", token) #delete digit and all string containing digit
    token = re.sub('([.;:,\[\]!?^*\(«)])', r' \1 ', token) #decoller ponctuation
    token = re.sub('([-]) ([a-zA-Z])', '\\1\\2', token) 
    token = re.sub('([a-zA-Z]) ([-])', '\\1\\2', token) 
    token = re.sub('\s{2,}', ' ', token) #remove if double whitespace
    token = token.strip()
    token = token.split()
    tokens_filtered= [word for word in token if not word in my_stopwords]
    return (" ").join(tokens_filtered)

file_input = input("Fichier txt contenant le corpus à nettoyer (avec l'extension .txt) : ")
text = open(file_input, "r")

with open("corpus_nettoye.txt", "w") as file_output :
	for token in text:
		filtered_text = remove_mystopwords(token)
		file_output.write(filtered_text+"\n")
    
