from urllib.request import urlopen
from lxml import etree
from datetime import datetime, date
from operator import itemgetter
import itertools


# Parameters list
product = [2]
region = [25,26]
links = []
for i in itertools.product(product,region):
    links.append("http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={}&Region={}".format(*i))
    links.append("http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={}&Region={}&Day=tomorrow".format(*i))

list = []

for link in links:
    content = etree.fromstring(urlopen(link).read())
    items = content.findall('.//item')
    
    for item in items:
        list.append(
                    {'brand': item.find('./brand').text,
                    'price': float(item.find('./price').text),
                    'location': item.find('./location').text,
                    'address': item.find('./address').text,
                    'tomorrow': True if datetime.strptime(item.find('./date').text, '%Y-%m-%d').date() != date.today() else False})

new_list = sorted(list, key=itemgetter('price', 'brand', 'address'))

for item in new_list:
    print('{price:.2f} {location:20s}Address: {address:50s}{brand:20s}{tomorrow:5b}'.format(**item))

current_date_time = datetime.strftime(datetime.now(), '%d/%m/%Y %I:%M:%S %p')

table_string = ""
for item in new_list:
    if item['tomorrow'] == False:
        table_string += "<tr><td>{price}</td><td>{location}</td><td>{address}</td><td>{brand}</td></tr>".format(**item)
    else:
        table_string += '<tr class="highlight"><td>{price}</td><td>{location}</td><td>{address}</td><td>{brand}</td></tr>'.format(
                                                                                                                                  **item)

style = '''
    <style style="text/css">
    .highlight{
    background-color:#00FFFF
    }
    </style>
    '''

header = '98 RON for NORTH RIVER and SOUTH RIVER'
template = '<!DOCTYPE html>' + style + '<html><head>{}</head><head style="background-color:#00FFFF">{}</head><body><table>{}</table></body></html>'.format(
                                                                                                                                                           current_date_time, header,
                                                                                                                                                           table_string)

with open("./output.html", "w") as f:
    f.write(template)

# template = "<html>" + "<head>" + "</head" + "body"
