import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.daft.ie/homes-to-rent")
    driver.maximize_window()
    time.sleep(4)
    cookie_accept = driver.find_element(By.XPATH, "//*[@id='didomi-notice-agree-button']")
    cookie_accept.click()
    time.sleep(0.7)
    location_input = driver.find_element(By.XPATH, "//*[@id='search-box-input']")
    location_input.send_keys(location)
    time.sleep(0.7)
    location_input.send_keys(Keys.ENTER)
    time.sleep(0.7)
    price_button = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[1]/div/div[2]/div[1]/div[1]/button")
    price_button.click()

    # Here you can do whatever you want with the data, like printing it to the console
    print("Location:", location)
    print("Rent Value:", rent_value)
    print("Number of Rooms:", num_rooms)
    print("message:", message)


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