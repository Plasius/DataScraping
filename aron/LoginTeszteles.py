#A szükséges modulok importálása
import pathlib
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#chromedriver hozzárendelése a programhoz
Path=str(pathlib.Path().absolute())+"\chromedriver.exe"
driver=webdriver.Chrome(Path)

#weboldal megnyitása
driver.get("https://www.linkedin.com/")
driver.maximize_window()

#cookie-k elfogadása
cookies=driver.find_element_by_xpath("//button[@data-control-name='ga-cookie.consent.accept.v3']")
cookies=WebDriverWait(driver, 5).until(EC.visibility_of(cookies))
cookies.click()

#Rákattintás a "sign in" gombra
signin=driver.find_element_by_partial_link_text("Sign")
signin=WebDriverWait(driver, 5).until(EC.visibility_of(signin))
signin.click()

#email cím beírása
username=driver.find_element_by_name("session_key")
username=WebDriverWait(driver, 5).until(EC.visibility_of(username))
username.send_keys("bitfakeprofile@gmail.com")

#jelszó beírása
password=driver.find_element_by_name("session_password")
password=WebDriverWait(driver, 5).until(EC.visibility_of(password))
password.send_keys("bitfakeprofile42")

#ENTER
password.send_keys(Keys.RETURN)

