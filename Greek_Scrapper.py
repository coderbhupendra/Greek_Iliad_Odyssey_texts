import urllib
import re
import os 
import string
from nltk import tokenize
#from cltk.stem.lemma import LemmaReplacer

try:
	from bs4 import BeautifulSoup
except ImportError:
	from BeautifulSoup import BeautifulSoup
	#http://sacred-texts.com/cla/homer/ili/ili01.htm
	#http://sacred-texts.com/cla/homer/greek/ili01.htm

	#http://sacred-texts.com/cla/homer/ody/ody01.htm
	#http://sacred-texts.com/cla/homer/greek/ody01.htm

def scrap_doc(file_no,type_book):	
	url_g="http://sacred-texts.com/cla/homer/greek/"+file_no
	url_e="http://sacred-texts.com/cla/homer/"+type_book+"/"+file_no
	
	
	directory="dataset/"+str(file_no)
	if not os.path.exists(directory):
		os.makedirs(directory)

	#scraping english literature
	html = urllib.urlopen(url_e)
	soup = BeautifulSoup(html)
	#to remove <a></a>
	for a in soup.findAll('a'):
		del a['href']
	
	text=soup.find_all('p')

	regex = re.compile('[%s]' % re.escape(string.punctuation))
	target_e = open("dataset/"+str(file_no)+"/"+str(file_no)+"_eng.txt", 'w')

	no_sentences_eng=0
	for i in range(1,len(text)-1) :
		page = text[i].getText()
		#print page,"\n"
		
		sentences=tokenize.sent_tokenize(page)
		#(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s

		for i in range(len(sentences)):
			line=sentences[i]
			line=regex.sub('', line).strip()
			
			
			if line!="":
				line+='.'
				target_e.write((line.lower()).encode('utf-8'))
				target_e.write("\n")
				no_sentences_eng+=1
	print (no_sentences_eng)	


	#scraping Greek literature
	html = urllib.urlopen(url_g)
	soup = BeautifulSoup(html)
	#to remove <a></a>
	for a in soup.findAll('a'):
		del a['href']
	for font in soup.findAll('font'):
		del font['color']
	
	text=soup.find_all('p')
	
	#lemmatizer = LemmaReplacer('greek')

	#text= text.encode('utf-8')

	regex = re.compile('[%s]' % re.escape(string.punctuation))
	target_g = open("dataset/"+str(file_no)+"/"+str(file_no)+"_greek.txt", 'w')

	no_sentences_greek=0
	for i in range(0,len(text)-1) :
		page = text[i].getText()
		#print (page.encode('utf-8') )#,lemmatizer.lemmatize(page),"\n"
		
		sentences=tokenize.sent_tokenize(page)
		#(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s

		#print ("len ",len(sentences))
		for i in range(len(sentences)):
			line=sentences[i]
			line=re.sub("[\s]?\d+[\s]?", " ", line)
			line=regex.sub('', line).strip()
						
			
			if line!="":
				line+='.'
				target_g.write((line.lower()).encode('utf-8'))
				target_g.write("\n")
				no_sentences_greek+=1
	
	
	print (no_sentences_greek)


def get_links():
	#scrapping all book links one by one
	url="http://sacred-texts.com/cla/homer/greek/index.htm"
	html = urllib.urlopen(url)
	soup = BeautifulSoup(html)
	h_tag=soup.find('h3')
	for br in h_tag.find_next_siblings():
		link=br.get('href')
		if link!=None:
			#print link
			if link[0:3]=="ili":
				scrap_doc(link,"ili")
			else:
				scrap_doc(link,"ody")	
			



if __name__ == "__main__":
	get_links()