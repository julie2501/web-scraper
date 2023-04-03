
#To create a web scraper to read articles from theverge.com using Python, we can use the BeautifulSoup library for parsing HTML and requests for fetching the web page. Here's a sample code that extracts the headline, author, date, and URL of each article on theverge.com and stores them in a CSV file and an SQLite database:


import csv
import sqlite3
import datetime
import requests
from bs4 import BeautifulSoup

# specify the URL of the website
url = 'https://www.theverge.com/'

# fetch the content of the website
r = requests.get(url)

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')

# find all articles on the website
articles = soup.find_all('article', class_='c-entry-box--compact')

# create a CSV file with the current date in the filename
csv_filename = datetime.datetime.now().strftime('%d%m%Y') + '_verge.csv'

# create a SQLite database to store the data
db_filename = 'verge.db'
conn = sqlite3.connect(db_filename)
c = conn.cursor()

# create a table for the articles in the database
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id INTEGER PRIMARY KEY, url TEXT, headline TEXT, author TEXT, date TEXT)''')

# loop through each article and extract the headline, author, date, and URL
for i, article in enumerate(articles):
    headline = article.h2.text.strip()
    author = article.find('span', class_='c-byline__item').a.text.strip()
    date = article.find('time', class_='c-byline__item')['datetime'].split('T')[0]
    url = article.a['href']
    
    # insert the article data into the CSV file
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i, url, headline, author, date])
    
    # insert the article data into the SQLite database
    c.execute("INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?)", (i, url, headline, author, date))
    
# commit changes to the database and close the connection
conn.commit()
conn.close()


#To run this script on a cloud service like AWS, we can create an EC2 instance and set up a cron job to run the script daily. We can also configure the instance to automatically save the CSV and SQLite files to an S3 bucket for backup and easy access.
