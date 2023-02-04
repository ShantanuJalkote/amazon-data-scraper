import csv
from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString


URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

driver = webdriver.Chrome()
answer = []
pages = []
scraped_data = []

pages.append(URL)

def get_urls(url_list):
    """"Gets all the Pages URL and saves them in a List"""
    for page in range(2,21):
        next_url = URL + f"&page={page}"
        url_list.append(next_url)

    return url_list

def get_data(item):
    """Extract Data("Product URL", "Product Name", "Product Price", "Rating", "Number of reviews")
       and Returns it as a Dictionary"""
    atag = item.h2.a    #Defing the tag that contains Product Name and URL
    req_name = item.h2.text #Extracting URL from tag
    req_url = "https://www.amazon.in/" + atag.get("href")   #Extracting Link from tag
    #Exception handling for Price if Price does not exists
    try:
        req_price = item.find('span', 'a-offscreen').text   #Extracting Price from tag
    except AttributeError:
        return
    #Exception handling for Ratings if Ratings does not exists
    try:
        #Extracting Ratings from tag
        req_rating = item.i.text
        #Extracting Number of Reviews from tag
        req_no_of_ratings = item.find('span', {'class' : 'a-size-base s-underline-text'}).text
    except AttributeError:
        req_rating = ' '
        req_no_of_ratings = ' '
    #Returning the Required result as a Dictionary
    return ({"Product Name" : req_name, "Product URL" : req_url, "Product Price" : req_price,
             "Rating" : req_rating, "Number of reviews" : req_no_of_ratings})

def main():
    """Main Function"""
    #Calling get_url function and saving the results in pages
    get_urls(pages)

    #Iterating through pages to extract all the required data and saving it in answer
    for i in pages:
        driver.get(i)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type':"s-search-result"}) #Tag specified for the required result
        for j in range(len(results)-1):
            item = results[j]
            answer.append(get_data(item))

    #Iterating through answer list to find URL of Each Product and extract more information by visiting those URl
    for row in answer:
        check = ""  #Initialising check as None
        url = row['Product URL']    #TO Extract URL of Each Product
        driver.get(url) #To open Each URL
        #Extracting data From Each Product Page
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        info = soup2.find_all('div', {'id' : "detailBullets_feature_div"})  #Tag specified for the required result
        #If the Product Details are present in list form
        if info != []:
            item2 = info[0]
            req_list = item2.find_all('span', 'a-list-item')
            check="prodDes"
        #If the Product Details are present in Table Form
        else:
            #Checking data in First Table
            info = soup2.find_all('table', {'id' : "productDetails_techSpec_section_1"})
            item3 = info[0]
            req_list_1 = item3.find_all('tr')

            #Checking data in Second Table
            info2 = soup2.find_all('table', {'id' : "productDetails_detailBullets_sections1"})
            item4 = info2[0]
            req_list_2 = item4.find_all('tr')

            #Combining Both result to get all the required information
            req_list = req_list_1 + req_list_2
            check = "prodTable"
        #Defining the list of data to extract
        product_desc_list = ['Manufacturer', 'ASIN']
        req_dict = {}   #Initialising empty dictionary
        #Adding the data extracted previously
        req_dict["Product Name"] = row["Product Name"]
        req_dict["Product URL"] = row["Product URL"]
        req_dict["Product Price"] = row["Product Price"]
        req_dict["Rating"] = row["Rating"]
        req_dict["Number of reviews"] = row["Number of reviews"]
        #To Extract Data from Product Page if it is present in a list
        if check == "prodDes":
            for req in req_list:
                x = req.contents
                key_new, value_new  = '', ''
                for _ in x:
                    if isinstance(_, NavigableString): #TO solve BeutifulSoup Error
                        continue
                    if _ != ' ':
                        prod = (_.contents[0].split('\n'))[0] #To get data in required format
                        #To store data in required format
                        if str(prod) in product_desc_list:
                            key_new = prod
                        else:
                            value_new = _.contents

                #To remove unneccessary data
                if key_new != '':
                    req_dict[key_new] = value_new[0]
        #To Extract Data from Product Page if it is present in a table
        elif check == "prodTable":
            for req in req_list:
                key, val = '', ''
                x = req.contents
                for _ in x:
                    if _ != ' ':
                        prod = _.contents[0].strip(' \n\u200e') #To get data in required format
                        #To store data in required format
                        if str(prod) in product_desc_list:
                            key = prod
                        else:
                            val = prod

                #To remove unneccessary data
                if key != '':
                    req_dict[key] = val

        #Adding Required Data
        scraped_data.append(req_dict) 

        #Defining Reuired Field in the csv file
        field_name = ["Product URL", "Product Name", "Product Price", "Rating", "Number of reviews",
                    "Manufacturer", "ASIN"]
        #To Write Data in a csv File
        with open('Scraped_Data.csv', 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_name)
            writer.writeheader()
            writer.writerows(scraped_data)       
#Calling Main Function
main()
