import requests
import json
from scrapy import Selector
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
def start_function():
	url="https://www.globaltrade.net/expert-service-provider.html"
	response = requests.get(url,headers=header)
	sel = Selector(text=response.content)
	country_url = sel.xpath('//ul[@id="mainCountries"]/li/a[@class="sp_country_71"]/@href').extract_first().strip()
	country_url = 'https://www.globaltrade.net' + country_url
	response = requests.get(country_url,headers=header)
	list_page(response)

def list_page(response):
	sel = Selector(text=response.content)
	urls_list = sel.xpath('//div[@class="SPList"]//li/p/a[@class="profileNavigator"]/@href').extract()
	for link in urls_list:
		link = 'https://www.globaltrade.net' + link
		product_response = requests.get(link,headers=header)
		product(product_response)

	next_url = sel.xpath('//a[@class="next-page button btn-small"]/@href').extract_first('').strip()
	next_url  = 'https://www.globaltrade.net' + next_url
	response_2 = requests.get(next_url,headers=header)
	list_page(response_2)

def product(response):

	sel = Selector(text=response.content)
	logo_url = sel.xpath('//img[@class="lazy"]/@data-original').extract_first('').strip()
	title = sel.xpath('//h1[@class="sp-title"]/span/text()').extract_first('').strip()
	sub_title = sel.xpath('//h4/span[@class="sub"]/text()').extract_first('').strip()
	primary_location = sel.xpath('//div[@class="profile-details"]//span[@itemprop="addressLocality"]/text()').extract_first('').strip()
	area_of_expertise = sel.xpath('//a[@class="mainExp"]/text()').extract_first('').strip()
	m = sel.xpath('//div[@class="section details"]/table//tr')
	about_text = ''
	website = ''
	lan = ''
	for i in m:
	    text = i.xpath('td/text()').extract_first('').strip()
	    if text == 'About:':
	        about_text = i.xpath('td/p//text()').extract()
	        about_text = ''.join(about_text).strip()
	    if text == 'Website:':
	        website = i.xpath('td/a/@href').extract_first('').strip()
	    if text == 'Languages spoken:' :
	       lan = i.xpath('td/text()').extract()[1].strip()
	
	if title:
		data = {"Logo Url":logo_url,"Title":title,"Sub-Title":sub_title,"Primary Location":primary_location,"Area Of Expertise":area_of_expertise,"About":about_text,"Website":website,"Language Spoken":lan}
		print(data)
		file = open('globaltrade.json','a')
		file.write(json.dumps(data)+'\n')
		file.close()


start_function()

