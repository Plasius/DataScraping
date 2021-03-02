import pathlib
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Path=str(pathlib.Path().absolute())+"\chromedriver.exe"
driver=webdriver.Chrome(Path)

driver.get("https://www.linkedin.com/")
driver.maximize_window()

cookies=driver.find_element_by_xpath("//button[@data-control-name='ga-cookie.consent.accept.v3']")
login=WebDriverWait(driver, 5).until(EC.visibility_of(cookies))
cookies.click()

login=driver.find_element_by_partial_link_text("Sign")
login=WebDriverWait(driver, 5).until(EC.visibility_of(login))
login.click()

username=driver.find_element_by_name("session_key")
login=WebDriverWait(driver, 5).until(EC.visibility_of(username))
username.send_keys("bitfakeprofile@gmail.com")

password=driver.find_element_by_name("session_password")
login=WebDriverWait(driver, 5).until(EC.visibility_of(password))
password.send_keys("bitfakeprofile42")
password.send_keys(Keys.RETURN)

