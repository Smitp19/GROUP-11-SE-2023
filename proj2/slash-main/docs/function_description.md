## **slash.py**
### *def main()*: 
Provides help for every argument

## **scaper.py**
### *def httpsGet(URL)*: 
The httpsGet function makes HTTP called to the requested URL with custom headers

### *def searchAmazon(query, df_flag, currency)*:  
The searchAmazon function scrapes amazon.com\
**Parameters**:\
query- search query for the product\
df_flag- flag variable\
currency- currency type entered by the user

Returns a list of items available on Amazon.com that match the product entered by the user.

### *def searchWalmart(query, df_flag, currency)*:
The searchWalmart function scrapes walmart.com\
**Parameters**:\
query- search query for the product\
df_flag- flag variable\
currency- currency type entered by the user

Returns a list of items available on walmart.com that match the product entered by the user.

### *def searchEtsy(query, df_flag, currency)*:
 The searchEtsy function scrapes Etsy.com\
 **Parameters**:\
query- search query for the product\
df_flag- flag variable\
currency- currency type entered by the user

Returns a list of items available on Etsy.com that match the product entered by the user

### *def driver(product, currency, num=None, df_flag=0,csv=False,cd=None)*:
Returns csv if the user enters the --csv arg, else will display the result table in the terminal based on the args entered by the user.

## **formatter.py**
### *def formatResult(website, titles, prices, links,ratings,df_flag, currency)*:
The formatResult function takes the scraped HTML as input, and extracts the necessary values from the HTML code. Ex. extracting a price '$19.99' from a paragraph tag.\
**Parameters**: \
titles- scraped titles of the products\
prices- scraped prices of the products\
links- scraped links of the products on the respective e-commerce sites\
ratings-scraped ratings of the product

Returns a dictionary of all the parameters stated above for the product.

### *def sortList(arr, sortBy, reverse)*:
It sorts the products list based on the flags provided as arguements. Currently, it supports sorting by price.\
**Parameters-**\
SortBy- "pr": sorts by price, SortBy- "ra": sorts by rating

Returns- Sorted list of the products based on the parameter requested by the user

### *def formatSearchQuery(query)*:
It formats the search string into a string that can be sent as a url paramenter.

### *def formatTitle(title)*:
It formats titles extracted from the scraped HTML code.

### *def getNumbers(st)*:
It extracts float values for the price from a string.\
Ex. it extracts 10.99 from '$10.99' or 'starting at $10.99'

### *def getCurrency(currency, price)*:
The getCurrency function converts the prices listed in USD to user specified currency. \
Currently it supports INR, EURO, AUD, YUAN, YEN, POUND.

## full_version.py 

### *def login(self)*:
Used for User Login\
Returns the username and email

### *def scrape(self,prod)*:
calls the scraper function from scraper.py

## csv_writer.py
### *def write_csv(arr,product,file_path)*:
Returns the CSV file with the naming nomenclature as 'ProductDate_Time'\
**Parameters**-\
product: product entered by the user\
file_path: path where the csv needs to be stored\
**Returns**-\
file_name: CSV file













