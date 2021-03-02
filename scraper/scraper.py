import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver=webdriver.Chrome("chromedriver.exe")

def login():
	#chrome megnyitasa
	driver.get("https://www.linkedin.com/login")
	driver.maximize_window()

	#cookies elfogadas
	cookies=driver.find_element_by_xpath("//button[@data-control-name='ga-cookie.consent.accept.v3']")
	login=WebDriverWait(driver, 5).until(EC.visibility_of(cookies))
	cookies.click()

	#felhasznaloi adatok bevitele
	username=driver.find_element_by_name("session_key")
	login=WebDriverWait(driver, 5).until(EC.visibility_of(username))
	username.send_keys("bitfakeprofile@gmail.com")

	password=driver.find_element_by_name("session_password")
	login=WebDriverWait(driver, 5).until(EC.visibility_of(password))
	password.send_keys("bitfakeprofile42")
	password.send_keys(Keys.RETURN)

	
login()
driver.get("https://www.linkedin.com/jobs")
