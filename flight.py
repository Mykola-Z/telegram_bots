# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:37:17 2020

@author: mzly903
"""

import bs4
from urllib.request import Request
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Gets Flight Number; Gives list [[City of Origin, Airport], [City of Destination, Airport]]

def checkNumber(number):
    my_url = Request('https://flightaware.com/live/flight/'+number)
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_html = str(page_html)
    
    find_from = page_html.find(r'"origin":{"TZ":":')
    origin_city = page_html[find_from:find_from+207]
    find_to = origin_city.find(r'"coord"')
    find_from = origin_city.find(r'friendlyLocation":"')
    
    origin_city = origin_city[find_from+19:find_to-2]

    if origin_city[:4] == 'Kiev':
        origin_city[:4] = 'Kyiv'
    if origin_city == 'Simferopol, Russian Federation':
        origin_city = 'Simferopol, Ukraine'
    if origin_city == 'Chi\xc5\x9fin\xc4\x83u, Moldova (KIV)':
        origin_city = 'Chisinau, Moldova (KIV)'
        
    find_from = page_html.find(r'"destination":{"TZ":":')
    dest_city = page_html[find_from:find_from+207]
    find_to = dest_city.find(r'"coord"')
    find_from = dest_city.find(r'friendlyLocation":"')
    
    dest_city = dest_city[find_from+19:find_to-2]
    if dest_city[:4] == 'Kiev':
        dest_city[:4] = 'Kyiv'
    if dest_city[:10] == 'Simferopol':
        dest_city = 'Simferopol, Ukraine'
    if dest_city == 'Chi\xc5\x9fin\xc4\x83u, Moldova (KIV)':
        dest_city = 'Chisinau, Moldova (KIV)'

    
    find_from = page_html.find(r"\'origin_IATA\', \'") + 19
    orig_air = page_html[find_from:find_from+3]
    
    find_from = page_html.find(r"\'destination_IATA\', \'") + 24
    dest_air = page_html[find_from:find_from+3]

    return [[origin_city, orig_air ], [dest_city, dest_air]]
