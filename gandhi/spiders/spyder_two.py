import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http.request import Request
import csv
from datetime import datetime, date
import time, re
import math

class GandhiSpider(scrapy.Spider):
	name = 'Gandhi_crawl'
	allowed_domains = ["www.gandhi.com.mx"]

	#custom_settings = {
	#'FEED_EXPORT_FIELDS': ["nombre", "original", "descuento", "porcentaje", "marca", "vendedor", "categoria", "envio", "meses", "desc", "url"]
	#}

	#https://www.gandhi.com.mx/sitemap.xml
	
	#scrapy crawl mercadoUno -o MercadoLibreParteDos.csv
	def start_requests(self):
		urls = ["https://www.gandhi.com.mx/ninos/categorias/poesia",
				"https://www.gandhi.com.mx/libros/licenciaturas-y-profesionistas/matematicas/geometria-y-trigonometria",
				"https://www.gandhi.com.mx/libros/licenciaturas-y-profesionistas/matematicas/algebra",
				"https://www.gandhi.com.mx/libros/licenciaturas-y-profesionistas/matematicas/calculo",
				"https://www.gandhi.com.mx/ninos/animales",
				"https://www.gandhi.com.mx/libros/negocios-y-finanzas/admnistracion/mercadotecnia",
				"https://www.gandhi.com.mx/libros/arte/decoracion",
				"https://www.gandhi.com.mx/libros/negocios-y-finanzas/admnistracion/finanzas",
				"https://www.gandhi.com.mx/libros/arte/fotografia",
				"https://www.gandhi.com.mx/libros/licenciaturas-y-profesionistas/quimica",
				"https://www.gandhi.com.mx/libros/licenciaturas-y-profesionistas/ciencias-de-la-salud",
				"https://www.gandhi.com.mx/libros/licenciaturas-y-profesionistas/economia",
				"https://www.gandhi.com.mx/libros/licenciaturas-y-profesionistas/filosofia",
				"https://www.gandhi.com.mx/libros/licenciaturas-y-profesionistas/matematicas",
				"https://www.gandhi.com.mx/libros/historia/historia-universal",
				"https://www.gandhi.com.mx/libros/historia/historia-de-mexico"]

		for i in urls:
			yield scrapy.Request(url=i, callback=self.parse_dir_contents, dont_filter=True, meta={'url':i})


	def parse_dir_contents(self, response):
		count = 0

		pages = response.xpath('(//input[@id="totalPages"]/@value)[last()]').extract() #(80)
		pages = int(pages[0])

		number = math.ceil(pages/20) #(4)
		#print(type(number))
		#print(response.url)

		for i in range(1, number + 1):
			url = response.url
			next_url = url + str(i)
			#print(next_url) 

			yield Request(
				url=next_url, 
				callback=self.parse, dont_filter=True)


	def parse(self, response):
		for href in response.xpath('//h2[@class="product-name"]/a/@href'):
			url = response.urljoin(href.extract())

			yield {
				'link':url	
			}