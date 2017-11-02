from urllib.request import urlopen
from lxml import etree
from datetime import datetime, date
from operator import itemgetter
import itertools

# Parameters list
product = [6]
region = [25, 26]
tomorrow = ['', '&Day=tomorrow']

links = [
         "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={" \
         "}&Region={}{}".format(*i)
         for i in itertools.product(product, region, tomorrow)
     ]

item_properties = []

for link in links:
    content = etree.fromstring(urlopen(link).read())
    items = content.findall('.//item')
    
    for item in items:
        item_properties.append({
                               'brand': item.find('./brand').text,
                               'price': float(item.find('./price').text),
                               'location': item.find('./location').text,
                               'address': item.find('./address').text,
                               'tomorrow': True if datetime.strptime(item.find('./date').text,
                                                                     '%Y-%m-%d').date() !=
                                                                     date.today() else False
                               })

new_item_properties = sorted(item_properties,
                             key=itemgetter('price', 'brand', 'address'))

current_date_time = datetime.strftime(datetime.now(), '%d/%m/%Y %I:%M:%S %p')

table_string = ""
for item in new_item_properties:
    if item['tomorrow'] == False:
        table_string += "<tr><td>{price}</td><td>{location}</td><td>{" \
            "address}</td><td>{brand}</td></tr>".format(**item)
    else:
        table_string += '<tr class="highlight"><td>{price}</td><td>{' \
            'location}</td><td>{address}</td><td>{' \
                'brand}</td></tr>'.format(**item)

style = '''
    <style style="text/css">
    .highlight{
    background-color:#00FFFF
    }
    </style>
    '''

header = '98 RON for NORTH RIVER and SOUTH RIVER'
template = '<!DOCTYPE html>' + style + '<html><head>{}</head><head '\
    'style="background-color:#00FFFF">{'\
        '}</head><body><table>{}</table></body></html>'.format(current_date_time, header, table_string)

with open("./output.html", "w") as f:
    f.write(template)
