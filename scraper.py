# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def get_houses(url, path, keyword, num_houses, verbose):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    driver.get(url)
    houses = []

    while len(houses) < num_houses:  # If true, should be still looking for new house

        time.sleep(4)
        try:
            driver.find_element_by_class_name("accept-cookies-button").click()  #accept cookies
        except NoSuchElementException:
            pass

        #Going through each house in this page
        house_buttons = driver.find_elements_by_class_name("l-searchResult") 
        
        for house_button in house_buttons:  
            print("Progress: {}".format("" + str(len(houses)) + "/" + str(num_houses)))
            if len(houses) >= num_houses:
                break

            # house_button.click()  #You might 
            time.sleep(1)
            price_collected_successfully = False
            description_collected_successfully = False
            title_collected_successfully = False
            address_collected_successfully = False
            phone_collected_successfully = False
            activity_collected_successfully = False
            collected_successfully = False
            
            ###Come back and clean this up -- Define a new function ###
            # Collect valiable information
            while not collected_successfully:
                # Property Price
                try:
                    property_price = house_button.find_element_by_xpath('.//div[@class="propertyCard-priceValue"]').text
                    price_collected_successfully = True
                except:
                    property_price = -1
                    time.sleep(.5)
                # Property Description
                try:
                    property_description = house_button.find_element_by_xpath('.//span[@itemprop="description"]/child::span').text
                    description_collected_successfully = True
                except:
                    property_description = -1
                    time.sleep(.5)
                # Property Title
                try:
                    property_title = house_button.find_element_by_xpath('.//h2[@class="propertyCard-title"]').text
                    title_collected_successfully = True
                except:
                    property_title = -1
                    time.sleep(.5)
                # Property Address
                try:
                    property_address = house_button.find_element_by_xpath('.//address[@class="propertyCard-address"]').text
                    address_collected_successfully = True
                except:
                    property_address = -1
                    time.sleep(.5)
                # Dealers Phone Number
                try:
                    property_phone = house_button.find_element_by_xpath('.//a[@class="propertyCard-contactsPhoneNumber"]').text
                    phone_collected_successfully = True
                except:
                    property_phone = -1
                    time.sleep(.5)
                # Last Activity
                try:
                    property_activity = house_button.find_element_by_xpath('.//span[@class="propertyCard-branchSummary-addedOrReduced"]').text
                    activity_collected_successfully = True
                except:
                    property_activity = -1
                    time.sleep(.5)
                # All information was collected
                collected_successfully = price_collected_successfully and description_collected_successfully
                """collected_successfully = price_collected_successfully and description_collected_successfully and
                                        title_collected_successfully and address_collected_successfully and 
                                        phone_collected_successfully and email_collected_successfully and 
                                        activity_collected_successfully"""

            # Printing for debugging
            if verbose:
                print("Title: {}".format(property_title))
                print("Price: {}".format(property_price))
                print("Description: {}".format(property_description[:500]))
                print("Address: {}".format(property_address))
                print("Phone: {}".format(property_phone))
                print("Activity: {}".format(property_activity))

            # Add to house data
            houses.append({
                "Title" : property_title,
                "House Price" : property_price,
                "Property Description" : property_description,
                "Address" : property_address,
                "Coontact Phone" : property_phone,
                "Latest Activity" : property_activity
            })

        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//button[@title="Next Page"]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_houses, len(houses)))
            break

    return pd.DataFrame(houses)  #This line converts the dictionary object into a pandas DataFrame.