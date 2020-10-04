from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import prettify

#read csv file of addresses and declare empty arrays for address item results
familyList = pd.read_csv("expdata.csv")
resultList=[]
resultList2=[]

#set webdriver for selenium
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx")

#declare rowtotal in CSV for record countdown in console
rowsTotal = len(familyList)
addressesFoundCount = 0
addressErrorsCount = 0

#iterate over CSV and scrape results from geocoder
for index, row in familyList.iterrows():
    FullAddress = str(row['Address']) + ' ' + str(row['City']) + ', ' + str(row['ProvinceCode'])
    inputElement = driver.find_element_by_id("Address")
    inputElement.send_keys(FullAddress,Keys.ENTER)
    sleep(1)
    showTableButton = driver.find_elements_by_xpath("//*[@id='btnCensusData1']")[0]
    showTableButton.click()
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    incomeTract = soup.find(id='cenIncLevel')
    medIncome = soup.find(id='distTract')
    if medIncome.text == '' and incomeTract.text == '':
        inputElement.clear()
        print("Address not found, trying search by ZIP code only...")
        FullAddress = str(row['PostalCode'])
        inputElement = driver.find_element_by_id("Address")
        inputElement.send_keys(FullAddress,Keys.ENTER)
        sleep(1)
        mapItem = driver.find_elements_by_xpath("//*[@id='map_gc']")[0]
        mapItem.click()
        showTableButton2 = driver.find_elements_by_xpath("//*[@id='btnCensusData2']")[0]
        showUserTractButton = driver.find_elements_by_id("chxTractSelect")[0]
        sleep(1)
        try:
            showTableButton2.click()
        except:
            showUserTractButton.click()
            sleep(1)
            showTableButton2.click()
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        incomeTract = soup.find(id='cenIncLevel2')
        medIncome = soup.find(id='distTract2')
        resultList.append(incomeTract.text)
        resultList2.append(medIncome.text)
        inputElement.clear()
        rowsTotal = rowsTotal - 1
        if medIncome.text == '' and incomeTract.text == '':
            print("No address found by zipcode, moving to next record...")
            addressErrorsCount = addressErrorsCount + 1
        else:
            print("Address found by ZIP code...")
            addressesFoundCount = addressesFoundCount +1
        print("Remaining records to be processed: ", rowsTotal)
        inputElement.clear()
        sleep(2)
    else:
        print("Address found...")
        resultList.append(incomeTract.text)
        resultList2.append(medIncome.text)
        inputElement.clear()
        rowsTotal = rowsTotal - 1
        print("Remaining records to be processed: ", rowsTotal) 
        inputElement.clear()
        addressesFoundCount = addressesFoundCount +1
        sleep(2)

#add results to pandas dataframe
familyList['incomeTract'] = resultList
familyList['medIncome'] = resultList2

#write results to csv and close
familyList.to_csv (r'results.csv', index = False, header=True)
print('Geocoding process complete')
print('Total records processed: ', len(familyList))
print('Addresses found: ',addressesFoundCount)
print('Addresses not found: ', addressErrorsCount)
