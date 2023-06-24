from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium webdriver
driver = webdriver.Chrome()

# Navigate to the dashboard
driver.get("file:///C:/path/to/your/dashboard.html")  # Replace with the path to your HTML file

# Define the buttons to choose the table
trees_button = driver.find_element(By.ID, "trees_button")  # Replace with the actual ID of your trees button
tls_logs_button = driver.find_element(By.ID, "tls_logs_button")  # Replace with the actual ID of your tls logs button

import pandas as pd

# Function to switch to the "trees" table
def show_trees_table():
    # Assuming the table is stored in a file named "trees.csv"
    file_path = "C:/Users/159om/OneDrive/Desktop/xl/trees.csv"
    # Code to load the table from the CSV file and display it on the dashboard goes here
    df = pd.read_csv(file_path)
    # Display the table on the dashboard using your preferred method (e.g., printing or rendering in HTML)

# Function to switch to the "tls logs" table
def show_tls_logs_table():
    # Assuming the table is stored in a file named "tls_logs.csv"
    file_path = "C:/Users/159om/OneDrive/Desktop/xl/tls_logs.csv"
    # Code to load the table from the CSV file and display it on the dashboard goes here
    df = pd.read_csv(file_path)
    # Display the table on the dashbo

# Define the button click event handlers
trees_button.click = show_trees_table
tls_logs_button.click = show_tls_logs_table

# Wait for user interaction (e.g., closing the browser)
WebDriverWait(driver, 0).until(EC.alert_is_present())

# Clean up resources
driver.quit()
