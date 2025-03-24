import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scroll_until_no_new_products(driver):
    product_count = 0
    same_count = 0  # Counter for detecting unchanged product count
    
    while True:
        products = driver.find_elements(By.CLASS_NAME, "findify-components--cards--product__title")
        
        if products:
            driver.execute_script("arguments[0].scrollIntoView();", products[-1])  # Scroll to last product
        time.sleep(3)  # Allow time for new elements to load
        
        new_product_count = len(driver.find_elements(By.CLASS_NAME, "findify-components--cards--product__title"))
        
        if new_product_count == product_count:
            same_count += 1
        else:
            same_count = 0  # Reset counter if new products are found
        
        if same_count >= 2:  # Stop if two consecutive scrolls yield no new products
            break
        
        product_count = new_product_count

def scrape_supertails():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Improve performance
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://supertails.com/search?q=farmina"
    driver.get(url)
    
    print("Page loaded successfully!")
    
    scroll_until_no_new_products(driver)  # Scroll to load all products
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    products = []
    for product in soup.select(".findify-components--cards--product__title"):
        title = product.get_text(strip=True)
        
        original_price_element = product.find_next(class_="findify-components--cards--product--price__compare")
        original_price = original_price_element.find("span", style="text-decoration: line-through;") if original_price_element else None
        original_price = original_price.get_text(strip=True).replace("₹", "") if original_price else "N/A"
        
        discount_element = product.find_next(class_="findify-product-card--sale-percentage")
        discount = discount_element.get_text(strip=True).replace("OFF", "").strip() if discount_element else "N/A"
        
        sale_price = product.find_next(class_="findify-components--cards--product--price__sale-price")
        current_price = product.find_next(class_="findify-components--cards--product--price__price")
        final_price = sale_price.get_text(strip=True) if sale_price else (current_price.get_text(strip=True) if current_price else "N/A")
        
        products.append({
            "Title": title,
            "Original Price (MRP)": original_price,
            "Discount (%)": discount,
            "Current Price": final_price
        })
    
    driver.quit()
    
    df = pd.DataFrame(products)
    excel_filename = "D:\FARMINA\supertail scraper\cleaned_supertails_farmina_products.xlsx"
    df.to_excel(excel_filename, index=False)
    
    print(f"Data saved to {excel_filename}")

if __name__ == "__main__":
    scrape_supertails()
