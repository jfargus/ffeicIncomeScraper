# ffeicIncomeScraper
A small python program to enter addresses into the FFIEC geocoder website and return census income tract and underserved status from a csv of addresses. 

Make sure you have the dependencies installed: BeautifulSoup4, Selenium and Pandas.

Also for Selenium to work, you need to download the appropriate Chrome webdriver for your version of Chrome from Chromium's website.

Place your source CSV file of addresses into the same folder as the script, name it expdata.csv and make sure your header names match the ones in the script: Address, City, and ProvinceCode (for US State).

I wrote this to analyze the population served by my organization for grant reporting, but you can change the data fields it pulls as you see fit by finding the HTML ID of the field using Chrome's developer tools Inspect function.

Yeah I know this script is janky, but it works and will save you a ton of time inputting addresses into the FFIEC geocoder. Feel free to adjust the second Sleep time if you don't want to wait as long, I left it at 2 seconds because I didn't want to overwhelm the geocoder website with requests. 
