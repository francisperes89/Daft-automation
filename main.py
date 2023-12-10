import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import openpyxl
from datetime import datetime
import time
# Tkinter GUI for the data needed to start scraping
# Global variables
location = ""
rent_value = ""
num_rooms = ""
message = ""
email = ""
password = ""
first_name = ""
last_name = ""
current_date = datetime.now()
today = current_date.strftime("%d-%m-%Y")
# Creating the sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
# Adicionar cabeçalhos
sheet['A1'] = 'Date'
sheet['B1'] = 'URL'
sheet['C1'] = 'Address'
sheet['D1'] = 'Rent'


def get_data():
    global location, rent_value, num_rooms, message, email, password, first_name, last_name
    first_name = entry_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    password = entry_password.get()
    location = entry_location.get()
    rent_value = entry_rent_value.get()
    num_rooms = entry_num_rooms.get()
    message = text_message.get("1.0", tk.END)
    scraping_data()

# Starting scraping


def scraping_data():
    global rent_value, num_rooms, message
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.daft.ie/homes-to-rent")
    driver.maximize_window()
    time.sleep(3)
    cookie_accept = driver.find_element(By.XPATH, "//*[@id='didomi-notice-agree-button']")
    cookie_accept.click()
    time.sleep(0.7)
    sign_in = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/header/div/div[2]/div[3]/ul/li/a")
    sign_in.click()
    time.sleep(2)
    email_input = driver.find_element(By.XPATH, "//*[@id='username']")
    email_input.send_keys(email)
    time.sleep(0.7)
    password_input = driver.find_element(By.XPATH, "//*[@id='password']")
    password_input.send_keys(password)
    time.sleep(0.7)
    sign_in_button = driver.find_element(By.XPATH, "//*[@id='login']")
    sign_in_button.click()
    time.sleep(2)
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
    selection_rooms_from = Select(driver.find_element(By.XPATH, "//*[@id='numBedsFrom']"))
    selection_rooms_from.select_by_value(num_rooms)
    still_have_items = True
    while still_have_items:
        list_of_urls = []
        list_of_addresses = []
        list_of_rent_prices = []
        number_of_items = int(driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/h1").text.split()[0])
        total_pages = number_of_items // 20
        if number_of_items % 20 != 0:
            total_pages += 1
        for current_page in range(total_pages):
            list_elements = driver.find_elements(By.CSS_SELECTOR, "ul li a div div .fKxuMi")
            for i in range(len(list_elements)):
                current_element = driver.find_elements(By.CSS_SELECTOR, "ul li a div div .fKxuMi")[i]
                current_element.click()
                time.sleep(2)
                if i == 0:
                    try:
                        address_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/div[1]/h1")
                        rent_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/div[3]/p[2]")
                    except NoSuchElementException:
                        address_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/h1")
                        rent_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/div[1]/h2")
                else:
                    address_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/h1")
                    rent_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[1]/div/div[2]/div[1]/h2")

                url = driver.current_url
                list_of_urls.append(url)
                print(url)
                address = address_element.text
                list_of_addresses.append(address)
                print(address)
                rent = rent_element.text
                list_of_rent_prices.append(rent)
                print(rent)
                new_row = sheet.max_row + 1  # Find the new empty row
                sheet[f'A{new_row}'] = today
                sheet[f'B{new_row}'] = url
                sheet[f'C{new_row}'] = address
                sheet[f'D{new_row}'] = rent
                if message.strip() != "":
                    email_button = driver.find_element(By.XPATH,
                                                       "//*[@id='__next']/main/div[3]/div[2]/div/div[1]/div[2]/div[2]/button/div/span")
                    email_button.click()
                    time.sleep(0.7)
                    name_entry = driver.find_element(By.XPATH, "//*[@id='keyword1']")
                    name_entry.send_keys(first_name)
                    time.sleep(0.7)
                    last_name_entry = driver.find_element(By.XPATH, "//*[@id='keyword2']")
                    last_name_entry.send_keys(last_name)
                    time.sleep(0.7)
                    text_box = driver.find_element(By.XPATH, "//*[@id='message']")
                    current_message = text_box.get_attribute("value")
                    if current_message:
                        time.sleep(0.7)
                        print(current_message)
                        text_box.click()
                        text_box.clear()
                        time.sleep(0.7)
                        text_box.send_keys(message)
                        # send_button = driver.find_element(By.XPATH, "//*[@id='contact-form-modal']/div[2]/form/div/div[9]/div/button")
                        # send_button.click()
                        # time.sleep(0.7)
                    else:
                        print("The box is empty!")
                        text_box.send_keys(message)
                        # send_button = driver.find_element(By.XPATH, "//*[@id='contact-form-modal']/div[2]/form/div/div[9]/div/button")
                        # send_button.click()
                        # time.sleep(0.7)
                    driver.back()
                    time.sleep(2)
                else:
                    driver.back()
                    time.sleep(2)
            if current_page < total_pages - 1:
                next_page = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div[2]/div/div[4]/button")
                next_page.click()
                print("next page")
                time.sleep(2)
            else:
                still_have_items = False
        # Saving the file
        workbook.save("daft-scraping.xlsx")
        print(list_of_addresses)
        print(list_of_rent_prices)
        print(list_of_urls)


        # driver.quit()


# Create the main window
window = tk.Tk()
window.title("Daft Rental Form")
window.geometry("600x800")

# Labels and entries
# Name
label_name = tk.Label(window, text="First Name:")
label_name.pack()
entry_name = tk.Entry(window)
entry_name.pack()
# Last name
label_last_name = tk.Label(window, text="Last Name:")
label_last_name.pack()
entry_last_name = tk.Entry(window)
entry_last_name.pack()
# Email
label_email = tk.Label(window, text="Email:")
label_email.pack()
entry_email = tk.Entry(window)
entry_email.pack()
# Password
label_password = tk.Label(window, text="Password:")
label_password.pack()
entry_password = tk.Entry(window, show="*")
entry_password.pack()
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
label_num_rooms = tk.Label(window, text="Number of Rooms(min):")
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



# se as aplicacoes foram feitas com sucesso salvar em uma planilha