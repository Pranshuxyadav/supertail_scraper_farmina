# supertail_scraper_farmina
web scraper for Farmina products
---------------------------------------------------------------------------------------------------
scraper_supertails.py - Supertails Product Scraper
This Python script scrapes product details from the Supertails website for the search query "farmina." It uses Selenium and BeautifulSoup to extract product names, original prices, discounts, and current prices, saving the results in an Excel file.
------------------------------------------------------------------------------
🚀 Features
Automated Web Scraping using Selenium
Extracts Key Product Details (Name, Price, Discount)
Saves Data in Excel Format

------------------------------------------------------------------------------

🛠️ Requirements
Ensure you have the following installed:
Python 3.x
Selenium
BeautifulSoup4
Pandas
Webdriver Manager

------------------------------------------------------------------------------

Install dependencies using:
pip install selenium beautifulsoup4 pandas webdriver-manager

------------------------------------------------------------------------------

🏃 Usage
Run the script with:
python scraper_supertails.py

------------------------------------------------------------------------------

📁 Output
The script generates an Excel file:
cleaned_supertails_farmina_products.xlsx
containing the scraped product data.

------------------------------------------------------------------------------

📝 Notes
The script runs in headless mode, meaning it does not open a browser window.
It waits 5 seconds to ensure JavaScript content loads.
Ensure Chrome is installed for the WebDriver to function properly.
------------------------------------------------------------------------------
📜 License
This project is open-source under the MIT License.
