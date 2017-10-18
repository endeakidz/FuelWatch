from urllib.request import urlopen
from lxml import etree
import io
from datetime import datetime, date
from operator import itemgetter, attrgetter
import itertools

links = []
data = {}
list = []

north_98 = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=6&Region=25'
south_98 = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=6&Region=26'
south_98_tomorrow = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=6&Region=26%Day=tomorrow'
north_98_tomorrow = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=6&Region=25&Day=tomorrow'

links.append(north_98)
links.append(south_98)
links.append(north_98_tomorrow)
links.append(south_98_tomorrow)

for link in links:
    response = urlopen(link)
    content = response.read()
    context = etree.iterparse(io.BytesIO(content))
    i = 0
    for action, elem in context:
        if i == 5:
            list.append(data)
            i = 0
            data = {}
        if elem.text != None:
            # print(elem.tag + " => " + elem.text)
            if elem.tag == 'brand':
                data['brand'] = elem.text
                i += 1
            elif elem.tag == 'date':
                temp_date = datetime.strptime(elem.text, '%Y-%m-%d').date()
                data['tomorrow'] = True if temp_date != date.today() else False
                i += 1
            elif elem.tag == 'price':
                data['price'] = float(elem.text)
                i += 1
            elif elem.tag == 'location':
                data['location'] = elem.text
                i += 1
            elif elem.tag == 'address':
                data['address'] = elem.text
                i += 1

# def getKey(dict):
#     return dict['price']
# new_list = sorted(list, key=getKey)

# new_list = sorted(list, key=lambda k: k['price'])

new_list = sorted(list, key=itemgetter('price', 'brand', 'location'))

for item in new_list:
    print('{price:.2f} {location:20s}Address: {address:50s}{brand:20s}{tomorrow:5b}'.format(**item))

current_date_time = datetime.strftime(datetime.now(), '%d/%m/%Y %I:%M:%S %p')
print(current_date_time)

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

print(template)
with open("/Users/Eugene/PycharmProjects/Workshop1/output.html", "w") as f:
    f.write(template)

# template = "<html>" + "<head>" + "</head" + "body"
