from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os, json, time
import pandas as pd

#%%%%%%%%%%%# User Options #%%%%%%%%%%%

# Choose The Save File Format ('CSV' For csv, 'JSON' For JSON)

FileFormat = 'CSV'

#%%%%%%%%%%%# User Options #%%%%%%%%%%%



def counter(list) -> list:

    """Converting String Numeric Values To Int Values ('20K' -> 20000)"""

    # List For Output
    countedList = []

    # Iterating through the input list
    for searchCount in list :

        # An int var for saving value
        count = 0

        # Try statement for handling errors
        try :
            # K for 1 thousand 
            if 'K' in searchCount :
                # Cleaning
                searchCount = searchCount[:searchCount.index('K')]

                count = int(searchCount) * 1000
                countedList.append(count)

            # M for 1 million
            elif 'M' in searchCount :
                searchCount = searchCount[:searchCount.index('M')]
                
                count = int(searchCount) * 1000000

            countedList.append(count)

        except :
            continue

    return countedList



def translator(list) -> list:

    """Translating Non-English Search Keywords To Be Comprehensive"""

    # Opening The Driver In Headless Mode
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service_log_path=os.devnull, options=options)

    # Opening Google Translate
    driver.get("https://translate.google.com.eg/?hl=en")
    time.sleep(2)

    # List for output
    translatedList = []

    # Finding translation input
    textBox = driver.find_element(by=By.CLASS_NAME, value="er8xn")

    # Iterating through The input list
    for word in list :
        textBox.send_keys(word)
        time.sleep(1.5)

        # Try statement for error handling
        try :
            # Copying Translation
            translated = driver.find_element(by=By.CLASS_NAME, value='ryNqvb').text

            # Appending Translation
            translatedList.append(translated)
            textBox.clear()
        except :
            continue
    
    driver.quit()
    return translatedList



def scraper(Bigdata) -> dict:

    """Scraping Data From Google Trends"""

    # Starting the driver in headless mode
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service_log_path=os.devnull, options=options)

    # Iterating through countries
    for country in list(Bigdata.keys()):

        # Input list for translate() function 
        translateThis = []

        # Input list for count() function 
        countThis = []

        # Opening Google Trends
        driver.get(f"https://trends.google.com/trends/trendingsearches/daily?geo={country}&hl=en-US")

        try :
            
            # Waiting for the page to load
            driver.implicitly_wait(5)
            # Main Day List
            TheDailyList = driver.find_element(by=By.CLASS_NAME, value="feed-list-wrapper")
            # Iterating through TheDailyList to find each element
            info = TheDailyList.find_elements(by=By.CLASS_NAME, value='details-wrapper')

        except :
            continue
        
        for data in info :

            # Finding elements
            # The title element
            title = str(data.find_element(by=By.CLASS_NAME, value="title").text)
            # The search count element
            searchCount = str(data.find_element(by=By.CLASS_NAME, value="search-count-title").text)

            translateThis.append(title)
            countThis.append(searchCount)
            
        # Calling counter() func and adding it to Search Count list In Data (17)
        Bigdata[country]['Search Count'] += counter(countThis)

        # Calling Translator() func and adding it to Title list In Data (57)
        Bigdata[country]['Title'] += translator(translateThis)
        
    driver.quit()

    # Big Data is the collected data so far
    return Bigdata


def main():

    """The Main() Function is for All The Previous Functions Into One"""

    # DataTemplate file is for needed inputs and output saving
    Bigdata = json.load(open('DataTemplate.json', encoding='utf8'))

    # for more info for each function please read above (from line number)
    ReturnedData = scraper(Bigdata)

    if FileFormat.upper() == 'CSV' :

        DataFrame = pd.DataFrame.from_dict(ReturnedData)
        DataFrame.T.to_csv('SavedData.csv', encoding='utf8', mode='a')
    
    elif FileFormat.upper() == 'JSON' :

        with open('SavedData.json', 'a', encoding="utf8") as fp:
            json.dump(ReturnedData, fp, ensure_ascii=False)

main()
