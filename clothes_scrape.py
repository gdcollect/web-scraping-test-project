#!/usr/bin/python3
"""
Web Scraping Junior Python Developer homework task
Scrape information about clothing items
from an online store website
and export it into a JSON file
"""
from bs4 import BeautifulSoup
import requests
import json


# Scrape the BOTTOMS section
# --------------------------

# Parse page and get list of items
source = requests.get('https://suzyshier.com/collections/sz_bottoms_shop-all-bottoms?view_all=true').text
soup = BeautifulSoup(source, 'lxml')
items = soup.find_all('div', class_="featured-collection__info js-product-tile")

# Make dictionary to store data for export
bottoms = {}

# Get data for every single item
links = [item.find('a', alt=True) for item in items]
for a in links:

    title = a['alt']
    url = a['href'].split('/')[4]
    url = 'https://suzyshier.com/products/{}'.format(url)

    detail = requests.get(url).text
    soup2 = BeautifulSoup(detail, 'lxml')

    price = soup2.find('div', class_="product__price-wrapper").span.text.strip()
    if "$" not in price:
        price = soup2.find('div', class_="product__price-wrapper")
        price = price.find(class_="product__price product__discount js-product-price").text.strip()

    color = soup2.find('div', class_="product__option-label").span.text.strip()

    sizes_raw = soup2.find_all('div', class_="selector-wrapper js product__option-selector")[1]
    sizes_raw = sizes_raw.find_all('label')
    sizes = ""
    for label in sizes_raw:
        sizes += label.input['value'] + ', '
    sizes = sizes.rstrip(', ')

    specs_raw = soup2.find('div', id="toggle-product__specs").ul
    specs = ""
    for spec in specs_raw.find_all('li'):
        specs += spec.text.rstrip() + ', '
    specs = specs.rstrip(', ')

    description = soup2.find('div', id="toggle-product__description").text.strip()

    # Write information about the item to dictionary
    bottoms[title] = {"Price" : price, "Color" : color, "Sizes" : sizes,
                            "Specs" : specs, "Description" : description}

# Export scraped data into a JSON file
with open('bottoms.json', 'w') as fp:
    json.dump(bottoms, fp)


# Scrape the WEB EXCLUSIVES section
# ---------------------------------


# Parse page and get list of items
source = requests.get('https://suzyshier.com/collections/sz_trend_online-exclusives').text
soup = BeautifulSoup(source, 'lxml')
items = soup.find_all('div', class_="featured-collection__info js-product-tile")

# Make dictionary to store data for export
exclusives = {}

# Get data for every single item
for item in items:
    title = item.find('h2').text
    price = item.find('div', class_="featured-collection__product-price")

    # Check if there is a discounted price
    try:
        price = price.find('span', class_="grid-item-price").text.strip()
        discounted_price = None
    except:
        discounted_price = price.find('p', class_="grid-item-sale").text.strip()
        price = price.find('p', class_="grid-item-compare").text.strip()

    # Write information about the item to dictionary
    exclusives[title] = {"Price": price, "Discounted price": discounted_price}


# Export scraped data into a JSON file
with open('exclusives.json', 'w') as fp:
    json.dump(exclusives, fp)
