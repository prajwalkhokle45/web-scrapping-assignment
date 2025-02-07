"""NETCore Scrapper"""

#importing libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in background (no window)
options.add_argument("--disable-gpu")  # Disable GPU for headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the website
driver.get("https://versionsof.net/core/8.0/8.0.0/")
time.sleep(3)  # Wait for the page to load

# Find all tables on the webpage
tables = driver.find_elements(By.XPATH, "//table")

# Extract data from each table
table_data = []
for i, table in enumerate(tables, 1):
    # Extract rows from the table
    rows = table.find_elements(By.XPATH, ".//tr")
    table_rows = []

    for row in rows:
        # Extract data from each cell (td)
        cols = row.find_elements(By.XPATH, ".//td")
        table_rows.append([col.text for col in cols])  # Add cell data to the row

    if table_rows:  # Only add the table if there is data
        table_data.append(table_rows)

# Close the WebDriver
driver.quit()

# Convert the extracted data into a DataFrame (for each table)
for i, data in enumerate(table_data, 1):
    if data:
        header = data[0] if data and len(data[0]) > 0 else []  # First row as columns if valid
        rows = data[1:] if header else data  # Exclude header row if invalid
        # Create a DataFrame with header (columns)
        df = pd.DataFrame(rows, columns=header) if header else pd.DataFrame(rows)
        # Save each table as CSV
        df.to_csv("C:/Users/Prajwal Khokle/Documents/table_1.csv", index=False)
        print(f"Table {i} saved as table_{i}.csv")
