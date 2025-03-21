import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Setup Chrome options
options = Options()
options.add_argument("--headless")  # Runs Chrome in headless mode (optional)

# Auto-detect and install the correct ChromeDriver version
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL of the Supertails search page
url = "https://supertails.com/search?q=farmina"
driver.get(url)
print("Page loaded successfully!")

# Allow time for JavaScript to load
time.sleep(5)

# Get page source after rendering
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

# Extract product details
products = []
for product in soup.select(".findify-components--cards--product__title"):
    title = product.get_text(strip=True)
    
    # Extract MRP Price
    original_price_element = product.find_next(class_="findify-components--cards--product--price__compare")
    original_price = original_price_element.find("span", style="text-decoration: line-through;") if original_price_element else None
    original_price = original_price.get_text(strip=True).replace("₹", "") if original_price else "N/A"
    
    # Extract Discount Percentage
    discount_element = product.find_next(class_="findify-product-card--sale-percentage")
    discount = discount_element.get_text(strip=True).replace("OFF", "").strip() if discount_element else "N/A"
    
    # Extract Sale or Current Price
    sale_price = product.find_next(class_="findify-components--cards--product--price__sale-price")
    current_price = product.find_next(class_="findify-components--cards--product--price__price")
    final_price = sale_price.get_text(strip=True) if sale_price else (current_price.get_text(strip=True) if current_price else "N/A")
    
    products.append({
        "Title": title,
        "Original Price (MRP)": original_price,
        "Discount (%)": discount,
        "Current Price": final_price
    })

# Close the WebDriver after scraping
driver.quit()

# Convert data to DataFrame
df = pd.DataFrame(products)

# Save to Excel
excel_filename = "cleaned_supertails_farmina_products.xlsx"
df.to_excel(excel_filename, index=False)

print(f"Data saved to {excel_filename}")