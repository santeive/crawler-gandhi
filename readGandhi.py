import csv
import time
import math
import re
import requests
import calendar
from urllib.request import urlopen
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, date

def getFecha():
	#Traemos la fecha
	x = datetime.now()

	dia = str(x.strftime("%d"))
	mes = str(x.strftime("%m"))
	anio = str(x.year)

	return dia + '-' + mes + '-' + anio

def loadSitemap(sitemapList):

	count = 0
	listNames = []
	for s in sitemapList :
		resp = requests.get(s)
		name = getName(count) + ".xml"
		with open(name, 'wb') as f:
			f.write(resp.content)
		listNames.append(name)
		count += 1

	return listNames


def loadRRS():
	#Para sanborns
	#url = 'https://s3.amazonaws.com/medios.plazavip.com/cron-pixeles-sanborns/produccion/catGoogle_Sanborns.xml'
	
	#Para claroshop
	url = 'https://www.gandhi.com.mx/sitemap.xml'
    #Hacemos la peticion a la URL y guardamos el xml
	resp = requests.get(url)
	date = getFecha()

	with open("Gandhii_URL" + date + '.xml', 'wb') as f:
		f.write(resp.content)

	return date

def parseXML(xmlFile):
	#Creamos el arbol
	tree = ET.parse(xmlFile)
	#Obtenemos la raiz
	root = tree.getroot()

	#Lista de almacenamiento
	listaP = []

	#Almacenamos aqui los items
	for movie in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
			link = movie.text
			#print(link)
			listaP.append(link)
	return listaP

def saveCSV(newitems, filename):
	#Especificamos las cabeceras de los campos

	#Lo guardamos en el csv
	with open(filename, 'w', newline='', encoding='UTF-8') as csvfile:
		writer = csv.writer(csvfile)
		#writer.writeheader()
		writer.writerow(newitems)

def main():
	#Cargamos la URL del XML
	date = loadRRS()

	#Regresa lista con todos los links
	newitems = parseXML("Gandhii_URL" + date + '.xml')

	#Cargamos el XML local
	saveCSV(newitems, 'catalogo_gandhi_' + getFecha()+'.csv')

if __name__ == "__main__":
    main()

    #https://stackoverflow.com/questions/10982417/capturing-http-status-codes-with-scrapy-spider