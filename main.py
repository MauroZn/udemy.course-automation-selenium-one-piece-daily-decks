from scipy.integrate import fixed_quad
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
import pandas as pd
import pyautogui
import time

decks = []

url = "https://onepiecetopdecks.com/deck-list/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
##Consent button
consent_button = WebDriverWait(driver, 1).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "fc-cta-consent"))
)
consent_button.click()

##Scroll to section
time.sleep(2)
game_formats_section = driver.find_element(By.XPATH, "/html/body/div/div[@class='site-inner']/div[@id='content']/div[2]/section[9]")
driver.execute_script("arguments[0].scrollIntoView();", game_formats_section)
time.sleep(2)

##Find the last "English Cards Expansion" div and click it
current_meta_decks_page = WebDriverWait(driver, 1).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "(/html/body/div/div[@class='site-inner']/div[@id='content']//section)[9]/div[2]/div[1]/div/div/div/a"
    ))
)
current_meta_decks_page.click()

##Move mouse to close Ad
currentMouseX, currentMouseY = pyautogui.position()
time.sleep(1)
pyautogui.moveTo(500, 300)
pyautogui.click()

time.sleep(5)
##Scroll to decks
decks_list_section = driver.find_element(By.XPATH, "/html/body/div[@id='page']/div[1]/div[@id='content']/div[2]/section[7]/div/div/div/div/div/div/div[@id='tablepress-28_wrapper']")
driver.execute_script("arguments[0].scrollIntoView();", decks_list_section)

#Select the last date possible that some decks were uploaded
time.sleep(2)
date_filter_select = decks_list_section.find_element(By.XPATH, ".//div[1]/div/div/div[2]/select")
select = Select(date_filter_select)
all_options = select.options
index = len(all_options) - 1
date_value = all_options[index].text
select.select_by_index(index)

##Get all decks names, placement and tournament
time.sleep(2)
decks_table = decks_list_section.find_element(By.XPATH, ".//table/tbody")
rows = decks_table.find_elements(By.TAG_NAME, "tr")
for row in rows:
    col4 = row.find_element(By.CLASS_NAME, "column-4").text
    col9 = row.find_element(By.CLASS_NAME, "column-9").text
    col10 = row.find_element(By.CLASS_NAME, "column-10").text
    deck_data_list = []
    deck_data_list.append(col4)
    deck_data_list.append(col9)
    deck_data_list.append(col10)
    decks.append(deck_data_list)

columns = ['Leader Name', 'Position In Tournament', 'Tournament Type']
df = pd.DataFrame(decks, columns=columns)

x = list(date_value)
fixed_date = ""
if x[1] == "/":
    fixed_date = x[0] + "-" + x[2] + x[3] + "-" + x[5] + x[6] + x[7] + x[8]
elif x[2] == "/":
    fixed_date = x[0] + x[1] + "-" + x[3] + x[4] + "-" + x[6] + x[7] + x[8] + x[9]

df.to_csv(fixed_date+"_top_decks.csv", index=False)
driver.close()