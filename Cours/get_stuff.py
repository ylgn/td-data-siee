# -*- coding: UTF-8 -*-
# pip install lxml pandas

import urllib.request
import pandas as pd
import lxml.html

#######################################
# Récupérer une page web et sa dom html
URL = 'https://www.boulanger.com/c/fer-a-repasser?m=g'
headers = {}
uagent = ('Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like '
          'Gecko) Chrome/24.0.1312.27 Safari/537.17')
headers['User-Agent'] = uagent
request = urllib.request.Request(URL, headers=headers)
resp = urllib.request.urlopen(request)
page = resp
html = lxml.html.fromstring(page.read())

def mreplace(sentence):
    options = ['\t', '\n', '\r']
    for opt in options :
         sentence = sentence.replace(opt, '')
    return  sentence.strip()

## Version avec seulement xpath (expert)
titles = html.xpath("//a[@class='grid-product-name']/h2")
prices = html.xpath("//p[@class='fix-price']")
results = {k: {'title': mreplace(titles[k].text_content()),
               'price': mreplace(prices[k].text_content())}
           for k in range(len(titles))}
# Save in xlsx
df = pd.DataFrame.from_dict(results, orient='index')
xlsx_file = "out.xlsx"
df.to_excel(xlsx_file)
print(f'{df.shape} df saved as {xlsx_file}')
