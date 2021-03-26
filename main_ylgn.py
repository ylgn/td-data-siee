import urllib.request
import pandas as pd
import lxml.html

#######################################
# Get all car from berline comptacte on aramisauto.com

def mreplace(sentence):
    options = ['\t', '\n', '\r']
    for opt in options :
         sentence = sentence.replace(opt, '')
    return  sentence.strip()



URL = 'https://www.aramisauto.com/achat/berline-compacte/'
p= 1
headers = {}
current_URL =""
titles = []
prices = []

uagent = ('Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like '
          'Gecko) Chrome/24.0.1312.27 Safari/537.17')
headers['User-Agent'] = uagent

while (p <=25):
	current_URL = URL+"?page="+str(p)
	print(current_URL)
	request = urllib.request.Request(current_URL, headers=headers)
	resp = urllib.request.urlopen(request)
	page = resp
	html = lxml.html.fromstring(page.read())
	## Version avec seulement xpath (expert)
	print(html.xpath('//span[@class="vehicle-model"]'))
	titles.extend((html.xpath('//span[@class="vehicle-model"]')))
	prices.extend((html.xpath('//span[@class="vehicle-loa-offer"]')))
	p = p + 1
	pass



results = {k: {'title': mreplace(titles[k].text_content()),
               'price': mreplace(prices[k].text_content())}
           for k in range(len(titles))}


# Save in xlsx
df = pd.DataFrame.from_dict(results, orient='index')
xlsx_file = "out.xlsx"
df.to_excel(xlsx_file)
print(f'{df.shape} df saved as {xlsx_file}')
