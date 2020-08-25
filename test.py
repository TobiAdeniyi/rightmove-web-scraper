#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 16:56:26 2020

@author: tobiadeniyi
"""


import scraper


url = "https://www.rightmove.co.uk/property-for-sale/Dartford.html"
path = "/Users/tobiadeniyi/Documents/Portfolio/Python/ProjectLibrary/RightMove/chromedriver"
keyword = 'Dartford'
num_houses = 10
verbose = True

df = scraper.get_houses(url, path, keyword, num_houses, verbose)