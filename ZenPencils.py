import requests
import bs4
import urllib
from bs4 import BeautifulSoup
import os.path
import configparser

config = configparser.ConfigParser()
list = []
images = []
keyvalue = {}
listimg = []

r = requests.get(
    'http://www.zenpencils.com', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')

for link in soup.find_all('option'):
    list.append(link.get('value'))

if not os.path.isfile('Details.ini'):
    configfile = open('Details.ini', 'w', 1)
    config['DETAILS'] = {}
    config.write(configfile)
    configfile.close()

config.read('Details.ini')
keyvalue = config._sections['DETAILS']

for element in list:
    if element[7:len(element)] in keyvalue.keys():
        strValue = keyvalue[element[7:len(element)]]
        strValue = strValue[0:-1]
        listimg = strValue.split(',')
        for each in listimg:
            if not os.path.isfile(each):
                print ("%s" % element)
                r = requests.get(
                    element, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(r.text, 'html.parser')
                divtag = soup.find(id="comic")
                value = ''
                for image in divtag.find_all('img'):
                    f = requests.get(
                        str(image.get('src')), headers={'User-Agent': 'Mozilla/5.0'})
                    index = len(str(image.get('src')))
                    filename = str(image.get('src'))[45:index]
                    value = value + filename + ','
                    config['DETAILS'][element[7:len(element)]] = value
                    if not os.path.isfile(filename):
                        local_file = open(filename, "wb", 1)
                        local_file.write(f.content)
                        local_file.close()
    else:
        print ("%s" % element)
        r = requests.get(element, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        divtag = soup.find(id="comic")
        value = ''
        for image in divtag.find_all('img'):
            f = requests.get(
                str(image.get('src')), headers={'User-Agent': 'Mozilla/5.0'})
            index = len(str(image.get('src')))
            filename = str(image.get('src'))[45:index]
            value = value + filename + ','
            config['DETAILS'][element[7:len(element)]] = value
            if not os.path.isfile(filename):
                local_file = open(filename, "wb", 1)
                local_file.write(f.content)
                local_file.close()
            with open('Details.ini', 'w', 1) as configfile:
                config.write(configfile)
            configfile.close()
