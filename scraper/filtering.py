#!/usr/bin/env python
# coding: utf-8

# In[74]:


import selenium
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome("chromedriver.exe")
#mac driver
#driver = webdriver.Chrome("./chromedriver")

#def read_input():
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
	username.send_keys("bitfakeprofile3@gmail.com")

	password=driver.find_element_by_name("session_password")
	login=WebDriverWait(driver, 5).until(EC.visibility_of(password))
	password.send_keys("bitfakeprofile42")
	password.send_keys(Keys.RETURN)


login()
driver.get("https://www.linkedin.com/jobs")


#Ez nem működik
#search_bar=driver.FindElement(By.CssSelector("#jobs-search-box__text-input jobs-search-box__keyboard-text-input"))
#search_bar=driver.find_element(By.cssSelector("input[class='jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-box__ghost-text-input']"))
#search_bar=driver.find_elements_by_class_name('jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-box__ghost-text-input')
#search_bar=formfield.findElement(By.CssSelector("Input[class*='jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-box__ghost-text-input'"))
#print(search_bar)
#len(search_bar)
#search_bar=driver.find_element_by_class_name('jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-box__keyboard-text-input--reflowed jobs-search-box__ghost-text-input')
#search_bar[0].send_keys(str(keywords))
#location =driver.find_element_by_class_name('jobs-search-box-location-id-ember277')
#location.send_keys(str(location))



sleep(5)
search = driver.find_element_by_xpath("//button[text()='Search']")
sleep(5)
search.click()
sleep(5)


#Open the dropdown of the filter, choose filter and hit esc - Date Posted
date_posted = driver.find_element_by_xpath("//button[text()='Date Posted']")
date_posted.click()

sleep(9)
input_el_date_posted = driver.find_element_by_xpath("//span[text()=\'"+date[0]+"\']")
sleep(5)
input_el_date_posted = input_el_date_posted.find_element_by_xpath('..')
input_el_date_posted = input_el_date_posted.find_element_by_xpath('..')
sleep(5)
input_el_date_posted.click()
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

#Open the dropdown of the filter, choose filter and hit esc - Date Posted
sleep(2)
experience_level = driver.find_element_by_xpath("//button[text()='Experience Level']")
sleep(2)
experience_level.click()
sleep(2)

for level in experience_levels_list:
    input_el_experience_level=driver.find_element_by_xpath("//span[text()=\'"+level+"\']")
    input_el_experience_level = input_el_experience_level.find_element_by_xpath('..')
    input_el_experience_level = input_el_experience_level.find_element_by_xpath('..')
    input_el_experience_level.click()
    
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    
#Open the dropdown of the filter, choose filter and hit esc - Date Posted
sleep(2)
job_type = driver.find_element_by_xpath("//button[text()='Job Type']")
sleep(2)
job_type.click()
sleep(2)

#Push button if filter is true for remote
if is_remote is True:
    remote = driver.find_element_by_xpath("//button[text()='Remote']")
    remote.click()
    
#Push button if filter is true for easy apply
if is_easy_apply is True:
    easy_apply = driver.find_element_by_xpath("//button[text()='Easy Apply']")
    easy_apply.click()    
    
all_filters = driver.find_element_by_xpath("//button[text()='All filters']")
sleep(2)
all_filters.click()    
sleep(4)

#Click under 10 filter
under_10=driver.find_elements_by_class_name('jobs-search-advanced-filters__binary-toggle')
sleep(4)
under_10[2].click()


for job in job_types_list:
    input_el_job_type=driver.find_element_by_xpath("//span[text()=\'"+job+"\']")
    input_el_job_type = input_el_job_type.find_element_by_xpath('..')
    input_el_job_type = input_el_job_type.find_element_by_xpath('..')
    input_el_job_type.click()


#Type company name - nem működik
#add_new_company=driver.find_element_by_xpath("//span[text()='Add a company']")
#add_new_company = add_new_company.find_element_by_xpath('..')
#add_new_company.click()
#sleep(2)


#text_box=driver.driver.find_element_by_id('search-reusables__filter-value-item mt4 pl0')
#text_box.send_keys('Google')
#sleep(4)
#text_box.send_keys(Keys.ARROW-DOWN)
#sleep(2)
#text_box.send_keys(Keys.RETURN)


# In[73]:


import selenium
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#driver = webdriver.Chrome("chromedriver.exe")
driver = webdriver.Chrome("./chromedriver")

#def read_input():
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
	username.send_keys("bitfakeprofile3@gmail.com")

	password=driver.find_element_by_name("session_password")
	login=WebDriverWait(driver, 5).until(EC.visibility_of(password))
	password.send_keys("bitfakeprofile42")
	password.send_keys(Keys.RETURN)


login()
driver.get("https://www.linkedin.com/jobs")


sleep(2)
#Ez nem működik
#search_bar=driver.FindElement(By.CssSelector("#jobs-search-box__text-input jobs-search-box__keyboard-text-input"))
#search_bar=driver.find_element(By.cssSelector("input[class='jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-box__ghost-text-input']"))
#search_bar=driver.find_elements_by_class_name('jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-box__ghost-text-input')
#search_bar=formfield.findElement(By.CssSelector("Input[class*='jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-box__ghost-text-input'"))
#print(search_bar)
#len(search_bar)
#search_bar=driver.find_element_by_class_name('jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-box__keyboard-text-input--reflowed jobs-search-box__ghost-text-input')
#search_bar[0].send_keys(str(keywords))
#location =driver.find_element_by_class_name('jobs-search-box-location-id-ember277')
#location.send_keys(str(location))

sleep(5)
search = driver.find_element_by_xpath("//button[text()='Search']")
sleep(5)
search.click()
sleep(5)



# In[ ]:




