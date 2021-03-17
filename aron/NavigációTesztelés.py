import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome("chromedriver.exe")

def read_input():
	#txt sorainak ertelmezese
	keywords_line = 1
	location_line = 2
	date_posted_start,date_posted_end = 5, 9
	experience_level_start,experience_level_end = 11, 17
	job_type_start,job_type_end = 19, 26
	remote_line = 27
	easy_apply_line = 28
	under_ten_applicants_line = 29
	company_line = 31
	industry_line = 32
	job_function_line = 33

	#txt beolvasása
	input_file=open('szures.txt', encoding="utf8")
	input = [line.strip().split() for line in input_file]

	#search & location string
	keywords = ' '.join(input[keywords_line])
	location = ' '.join(input[location_line])

	#csak egy érték lehet
	date = [date[0].strip(date[0][-1]).replace('_',' ') for date in input[date_posted_start:date_posted_end] if len(date)>1]
	
	#több érték is lehet
	experience_levels_list = [level[0].strip(level[0][-1]).replace('_',' ') for level in input[experience_level_start:experience_level_end] if len(level) > 1]
	job_types_list = [type[0].strip(type[0][-1]) for type in input[job_type_start:job_type_end] if len(type)>1]
 
	#true or false
	is_remote = True if input[remote_line][-1]=='Y' else False
	is_easy_apply = True if input[easy_apply_line][-1]=='Y' else False   
	is_under_ten = True if input[under_ten_applicants_line][-1]=='Y' else False

	#listak
	companies_list = ' '.join(input[company_line][1:]).split(', ')
	industries_list = ' '.join(input[industry_line][1:]).split(', ')
	job_functions_list = ' '.join(input[job_function_line][1:]).split(', ')

	#print
	print(keywords)
	print(location)
	print(date)
	print(experience_levels_list)
	print(job_types_list)
	print(is_remote)
	print(is_easy_apply)
	print(is_under_ten)
	print(companies_list)
	print(industries_list)
	print(job_functions_list)


def login():
	# chrome megnyitasa
	driver.get("https://www.linkedin.com/")
	driver.maximize_window()

	try:
		# cookies elfogadas
		cookies = driver.find_element_by_xpath("//button[@data-control-name='ga-cookie.consent.accept.v3']")
		login = WebDriverWait(driver, 5).until(EC.visibility_of(cookies))
		cookies.click()
		time.sleep(3)
	except:
		print('sutik elfogadva')

	try:
		# felhasznaloi adatok bevitele
		username = driver.find_element_by_name("session_key")
		login = WebDriverWait(driver, 5).until(EC.visibility_of(username))
		username.send_keys("moreda7823@566dh.com")

		password = driver.find_element_by_name("session_password")
		login = WebDriverWait(driver, 5).until(EC.visibility_of(password))
		password.send_keys("azsxdcfv")

		password.send_keys(Keys.RETURN)

		time.sleep(3)
	except:
		print('Login átugrása')
read_input()	
login()

#rákattint a jobs fülre
jobs=driver.find_element_by_xpath("//a[@data-test-global-nav-link='jobs']")
jobs=WebDriverWait(driver, 5).until(EC.visibility_of(jobs))
jobs.click()

time.sleep(2)

#rákattint az első állásajánlatra
job=driver.find_element_by_xpath("//div[@class='job-card-square__main relative display-flex flex-grow-1 flex-column align-items-stretch']")
job=WebDriverWait(driver, 5).until(EC.visibility_of(job))
job.click()
time.sleep(2)

i=0
o=0
h=1
s=0
kesz=[]
while o==0:
	try:
    	#végigmegy az állásajánlatokon
		h+=1
		while i==0:
			time.sleep(1)
			jobs = driver.find_elements_by_xpath("//div[@class='mr1 artdeco-entity-lockup__image artdeco-entity-lockup__image--type-square ember-view']")
			jobs=[x for x in jobs if x not in kesz]
			if jobs==[]:
				i=1
			else:
				for job in jobs:
					job.click()
					time.sleep(0.7)
					kesz.append(job)
		#átlép a következő oldalra
		time.sleep(1)
		oldalak=driver.find_element_by_xpath("//button[@aria-label='Page {0}']".format(h))
		time.sleep(2)
		oldalak.click()
		i=0
		kesz=[]
	except:
		o=1

time.sleep(2)
driver.quit()
