import urllib.request
import pandas as pd
import lxml.html
from re import sub
from decimal import Decimal

#######################################
# Get all car from berline comptacte on aramisauto.com

def mreplace(sentence):
    options = ['\t', '\n', '\r']
    for opt in options :
         sentence = sentence.replace(opt, '')
    return  sentence.strip()





URL = 'https://www.aramisauto.com/achat/berline-compacte/'
NB_PAGES_MAX = 25
p= 1
print(f'This program scraps every berline cars from page {p} to {NB_PAGES_MAX} on aramisauto website.')
headers = {}
current_URL =""
titles = []
prices = []
motorisation = []
transmission = []




uagent = ('Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like '
          'Gecko) Chrome/24.0.1312.27 Safari/537.17')
headers['User-Agent'] = uagent

print('Processing please wait....')

#GET ALL INFORMATION FROM THE CARS
while (p <= NB_PAGES_MAX):
    print(f'* Scraping page {p} on {NB_PAGES_MAX}')
    current_URL = URL+"?page="+str(p)
    request = urllib.request.Request(current_URL, headers=headers)
    resp = urllib.request.urlopen(request)
    page = resp
    html = lxml.html.fromstring(page.read())
	## Version avec seulement xpath (expert)
    titles.extend((html.xpath('//span[@class="vehicle-model"]')))
    prices.extend((html.xpath('//span[@class="vehicle-loa-offer"]')))
    motorisation.extend((html.xpath('//div[@class="vehicle-motorisation"]')))
    transmission.extend((html.xpath('//div[@class="vehicle-transmission"]')))
    p = p + 1
    pass

results = {k: {'car': mreplace(titles[k].text_content()),
               'price': float(Decimal(sub(r'[^\d.]', '', prices[k].text_content()))),       
               'motorisation': mreplace(motorisation[k].text_content()),
               'transmission': mreplace(transmission[k].text_content())}
               
           for k in range(len(titles))}

# Save in xlsx
df = pd.DataFrame.from_dict(results, orient='index')
df.sort_values(by=['price','car','motorisation'], inplace=True)

nbCars = len(df.index)
cheapestCar = {'car' : df["car"].values[0],'price' : df["price"].values[0],'motorisation' : df["motorisation"].values[0],'transmission' : df["transmission"].values[0]}
expensiveCar = {'car' : df["car"].values[nbCars-1],'price' : df["price"].values[nbCars-1],'motorisation' : df["motorisation"].values[nbCars-1],'transmission' : df["transmission"].values[nbCars-1]}
averagePrice = round(df["price"].mean(),1)

df.loc[len(df)]=['AVERAGE PRICE',averagePrice,'NUMBER OF CARS',nbCars]
df.loc[len(df)]=['CHEAPEST CAR IS :',cheapestCar["car"],'MOST EXPENSIVE CAR CAR IS :',expensiveCar["car"]]  
xlsx_file = "out_cars.xlsx"
df.to_excel(xlsx_file)




print(f'\n{nbCars} cars has been found and sorted by ascending price for UX purposes.\n')
print(f'The cheapest car is the {cheapestCar["car"]}, it costs {cheapestCar["price"]} €. It is equipped by {cheapestCar["motorisation"]} engine and has a {cheapestCar["transmission"]} transmission.\n') 
print(f'The most expensive car is the {expensiveCar["car"]}, it costs {expensiveCar["price"]} €. It is equipped by {expensiveCar["motorisation"]} engine and has a {expensiveCar["transmission"]} transmission.\n')     
     
print(f'On average on this website, a second-hand compact berline car costs {averagePrice}€\n')

print(f'All this information as been fomalised into a matrix {df.shape} and saved as {xlsx_file}')
