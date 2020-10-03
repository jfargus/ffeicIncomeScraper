from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

familyList = pd.read_csv("expdata.csv")
print(familyList)
resultList=[]
resultList2=[]
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx")
rowsTotal = len(familyList)
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
    resultList.append(incomeTract.text)
    resultList2.append(medIncome.text)
    inputElement.clear()
    rowsTotal = rowsTotal - 1
    print("Remaining records to be processed: ", rowsTotal) 
    sleep(2)
familyList['incomeTract'] = resultList
familyList['medIncome'] = resultList2
familyList.to_csv (r'results.csv', index = False, header=True)
