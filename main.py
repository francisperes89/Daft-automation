import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Tkinter GUI for the data needed to start scraping
# Global variables
location = ""
rent_value = ""
num_rooms = ""
message = ""


def get_data():
    global location, rent_value, num_rooms, message
    location = entry_location.get()
    rent_value = entry_rent_value.get()
    num_rooms = entry_num_rooms.get()
    message = text_message.get("1.0", tk.END)
    scraping_data()

# Starting scraping


def scraping_data():
    global rent_value, num_rooms
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.daft.ie/homes-to-rent")
    driver.maximize_window()
    time.sleep(3)
    cookie_accept = driver.find_element(By.XPATH, "//*[@id='didomi-notice-agree-button']")
    cookie_accept.click()
    time.sleep(0.7)
    location_input = driver.find_element(By.XPATH, "//*[@id='search-box-input']")
    location_input.send_keys(location)
    time.sleep(0.7)
    location_input.send_keys(Keys.ENTER)
    time.sleep(2)
    price_button = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[1]/div/div[2]/div[1]/div[1]/button")
    price_button.click()
    time.sleep(2)
    selection_price_up_to = Select(driver.find_element(By.XPATH, "//*[@id='rentalPriceTo']"))
    selection_price_up_to.select_by_value(rent_value)
    time.sleep(1)
    rooms_button = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[1]/div/div[2]/div[2]/div[1]/button")
    rooms_button.click()
    time.sleep(1)
    selection_rooms_up_to = Select(driver.find_element(By.XPATH, "//*[@id='numBedsTo']"))
    selection_rooms_up_to.select_by_value(num_rooms)
    places_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/h1")
    numbers_of_places = int(places_element.text.split()[0])
    total_pages = numbers_of_places/20
    list_elements = driver.find_elements(By.CSS_SELECTOR, "ul li a div div .fKxuMi")
    time.sleep(2)
    list_of_urls = []
  
    for i in range(len(list_elements)):
        current_element = driver.find_elements(By.CSS_SELECTOR, "ul li a div div .fKxuMi")[i]
        current_element.click()
        time.sleep(2)
        if i == 0:
            address_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/div[1]/h1")
            rent_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/div[3]/p[2]")
        else:
            address_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/h1")
            rent_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/div[1]/h2")

        url = driver.current_url
        list_of_urls.append(url)
        print(url)
        address = address_element.text
        print(address)
        rent = rent_element.text
        print(rent)
        driver.back()
        time.sleep(2)
        if i == len(list_elements) - 1:
            try:
                next_page = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[2]/div/div[6]/button/div/span")
                next_page.click()
            except:
                break
    driver.quit()

# Create the main window
window = tk.Tk()
window.title("Daft Rental Form")
window.geometry("500x600")

# Labels and entries
# Location
label_location = tk.Label(window, text="Location:")
label_location.pack()
entry_location = tk.Entry(window)
entry_location.pack()
# Rent value up to
label_rent_value = tk.Label(window, text="Rent Value(up to):")
label_rent_value.pack()
entry_rent_value = tk.Entry(window)
entry_rent_value.pack()
# Number of rooms up to
label_num_rooms = tk.Label(window, text="Number of Rooms:")
label_num_rooms.pack()
entry_num_rooms = tk.Entry(window)
entry_num_rooms.pack()
# Message to the Agency/Landlord
label_message = tk.Label(window, text="Message:")
label_message.pack()
text_message = tk.Text(window, height=10, width=30)
text_message.pack()


# Button to get the data
button_get_data = tk.Button(window, text="Send", command=get_data)
button_get_data.pack()


# Start the main loop of the GUI
window.mainloop()


# fazer scraping do site daft e conforme encontrar imoveis com dados retirados fazer aplicacao


# se as aplicacoes foram feitas com sucesso salvar em uma planilha