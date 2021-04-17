import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import Param
import Munka
import codecs

def export(lista):
	file= codecs.open('exported.csv','w', 'utf-8')

	#fejléc
	for att in lista[0].__dict__.keys():
		if att.split('_')[-1]=='list':
			for repeat in range(1,4): file.write('"'+str(att.upper())+str(repeat)+'",')
		else: file.write('"'+str(att.upper())+'",')
	file.write('\n')

	#ajánlatok
	for ajanlat in lista:
		for att, value in ajanlat.__dict__.items():
			if type(value) is list:
				value += ['']*(3 - len(value))
				for object in value: file.write('"'+str(object)+'",')
			else: file.write('"'+str(value)+'",')
		file.write('\n')

	file.close()

def init_driver() -> webdriver.Chrome:
	options = webdriver.ChromeOptions() 
	options.add_argument("user-data-dir=/scraperdata")
	return webdriver.Chrome(chrome_options=options)

def read_txt() -> Param:
	#INPUT
	#txt sorainak ertelmezese
	keywords_line = 1
	location_line = 2
	date_posted_start,date_posted_end = 5, 9
	experience_level_start, experience_level_end = 11, 17
	job_type_start,job_type_end = 19, 26
	remote_line = 27
	easy_apply_line = 28
	company_line = 30

	#txt beolvasása
	input_file=open('szures.txt', encoding="utf8")
	input = [line.strip().split() for line in input_file]

	#search & location string
	keywords = ' '.join(input[keywords_line][1:])
	location = ' '.join(input[location_line][1:])

	#csak egy érték lehet
	date = [date[0].strip(date[0][-1]).replace('_',' ') for date in input[date_posted_start:date_posted_end] if len(date)>1]

	#több érték is lehet
	experience_levels_list = [level[0].strip(level[0][-1]).replace('_',' ') for level in input[experience_level_start:experience_level_end] if len(level) > 1]
	job_types_list = [type[0].strip(type[0][-1]) for type in input[job_type_start:job_type_end] if len(type)>1]
	print(job_types_list)
	#true or false
	is_remote = True if input[remote_line][-1]=='Y' else False
	is_easy_apply = True if input[easy_apply_line][-1]=='Y' else False   

	#listak
	companies_list = ' '.join(input[company_line][1:]).split(', ')

	#print
	param = Param.Param(keywords, location, date, experience_levels_list, job_types_list, is_remote, is_easy_apply, companies_list)
	print(param)
	return param

def login(driver):
	#LOGIN
	#chrome megnyitasa
	driver.get("https://www.linkedin.com/")
	driver.maximize_window()

	try:
		#cookies elfogadas
		cookies=driver.find_element_by_xpath("//button[@data-control-name='ga-cookie.consent.accept.v3']")
		WebDriverWait(driver, 5).until(EC.visibility_of(cookies))
		cookies.click()
		sleep(3)
	except:
		print('sutik elfogadva')

		
	try:
		#felhasznaloi adatok bevitele
		username=driver.find_element_by_name("session_key")
		WebDriverWait(driver, 5).until(EC.visibility_of(username))
		username.send_keys("fegak36356@zcai55.com")

		password=driver.find_element_by_name("session_password")
		WebDriverWait(driver, 5).until(EC.visibility_of(password))
		password.send_keys("azsxdcfv")
		
		password.send_keys(Keys.RETURN)
		
		sleep(3)
	except:
		print('Login átugrása')

def extract(driver) -> Munka:
	munka = Munka.Munka('','','','','',[],[])

	title = driver.find_elements_by_class_name("jobs-details-top-card__job-title")
	munka.title = title[0].text

	try:
		company = driver.find_elements_by_class_name("jobs-details-top-card__company-url")
		munka.company = company[0].text

		location = driver.find_elements_by_class_name("jobs-details-top-card__bullet")
		munka.location = location[0].text
	except:
		data = driver.find_element_by_class_name('jobs-details-top-card__company-info')
		children = data.find_elements_by_xpath(".//*")

		#get unlinked company name
		if children[0].text == 'Company Name':
			munka.company = data.text.splitlines()[1]
		else:
			munka.company = children[0].text

		munka.location = children[2].text

	group = driver.find_elements_by_class_name('jobs-box__group')
	#tulajdonsag
	for element in group:

		#cim es a konkret
		children = element.find_elements_by_xpath(".//*")

		#konkret
		titlr = children[0].text
		descr = children[1]

		if titlr == 'Seniority Level':
			munka.seniority = descr.text
		elif titlr == 'Employment Type':
			munka.employment_type = descr.text

		elif titlr == 'Industry':
			for item in descr.find_elements_by_xpath(".//*"):
				munka.industry_list.append(item.text)

		elif titlr == 'Job Functions':
			for item in descr.find_elements_by_xpath(".//*"):
				munka.job_functions_list.append(item.text)
			
	return munka

def navigate(driver):
	munkak = []

	i=0
	o=0
	h=1
	kesz=[]
	while o==0:
		try:
			#végigmegy az állásajánlatokon
			h+=1
			while i==0:
				sleep(1)
				jobs = driver.find_elements_by_xpath("//div[@class='mr1 artdeco-entity-lockup__image artdeco-entity-lockup__image--type-square ember-view']")
				jobs = [x for x in jobs if x not in kesz]
				if jobs==[]:
					i=1
				else:
					for job in jobs:
						job.click()
						sleep(2)
						
						#extract
						munkak.append(extract(driver))
						print(munkak[-1])

						kesz.append(job)
			#átlép a következő oldalra
			sleep(1)
			oldalak=driver.find_element_by_xpath("//button[@aria-label='Page {0}']".format(h))
			sleep(2)
			oldalak.click()
			i=0
			kesz=[]
		except:
			o=1

	sleep(2)
	driver.quit()

	return munkak

def filter_results(driver, param):
	#SZŰRÉS
	'''
	Filter options:
	- keywords
	- location
	- Date Posted - single choice
	- Experience Level - multiple choice
	- Job Type - multiple choice
	- Remote - true/false
	- Easy Apply - true/false
	'''
	
	sleep(5)

	#szöveges szűrések
	if param.keywords:
		search_bar = driver.find_elements_by_css_selector("[aria-label='Search by title, skill, or company']")[0].find_elements_by_tag_name("input")[0]
		search_bar.send_keys(str(param.keywords))
		sleep(5)

	if param.location:
		location_bar = driver.find_elements_by_css_selector("[aria-label='City, state, or zip code']")[0].find_elements_by_tag_name("input")[0]
		location_bar.send_keys(Keys.CONTROL, 'a')
		location_bar.send_keys(Keys.BACKSPACE)
		location_bar.send_keys(str(param.location))
		location_bar.send_keys(Keys.RETURN)
		sleep(5)

	#Open the dropdown of the filter, choose filter and hit esc - Date Posted
	if param.date:
		driver.find_element_by_xpath("//button[text()='Date Posted']").click()
		sleep(2)
		
		input_el_date_posted = driver.find_element_by_xpath("//span[text()=\'"+param.date[0]+"\']")
		input_el_date_posted = input_el_date_posted.find_element_by_xpath('..')
		input_el_date_posted = input_el_date_posted.find_element_by_xpath('..')
		input_el_date_posted.click()
		sleep(2)

		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		sleep(2)

	#Open the dropdown of the filter, choose filter and hit esc - Experience Level
	if param.experience_levels_list:
		experience_level = driver.find_element_by_xpath("//button[text()='Experience Level']")
		experience_level.click()
		sleep(2)

		for level in param.experience_levels_list:
			try:
				input_el_experience_level = driver.find_element_by_xpath("//span[text()=\'"+level+"\']")
				input_el_experience_level = input_el_experience_level.find_element_by_xpath('..')
				input_el_experience_level = input_el_experience_level.find_element_by_xpath('..')
				input_el_experience_level.click()
			except:
				print('failed to select experience level: '+ level)
			sleep(1)

		
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		sleep(2)


	#Open the dropdown of the filter, type in companies with downarrow and enter, then hit esc - Company
	if param.companies_list:
		company = driver.find_element_by_xpath("//button[text()='Company']")
		company.click()
		sleep(2)

		for companyname in param.companies_list:
			company_bar = driver.find_element_by_css_selector("[aria-label='Add a company']")
			company_bar.send_keys(companyname)
			sleep(2)

			webdriver.ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
			sleep(1)
			webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
			sleep(2)
		
		webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
		sleep(1)
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		sleep(1)
			
		
	#Open the dropdown of the filter, choose filter and hit esc - Job Type
	if param.job_types_list:
		job_type = driver.find_element_by_xpath("//button[text()='Job Type']")
		job_type.click()
		sleep(2)

		for pos in param.job_types_list:
			try:
				input_el_job_type = driver.find_element_by_xpath("//label[@for=\'"+"jobType-"+pos[0]+"\']")
				input_el_job_type.click()
			except:
				print('failed to select job type: ' + pos)
			sleep(1)
			
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		sleep(2)

	#Push button if filter is true for remote
	if param.is_remote == True:
		remote = driver.find_element_by_xpath("//button[text()='Remote']")
		remote.click()
		sleep(2)
		
	#Push button if filter is true for easy apply
	if param.is_easy_apply == True:
		easy_apply = driver.find_element_by_xpath("//button[text()='Easy Apply']")
		easy_apply.click()
		sleep(2)   


driver = init_driver()

param = read_txt()

login(driver)

driver.get("https://www.linkedin.com/jobs/search/")
sleep(5)

filter_results(driver, param)

munkak = navigate(driver)

export(munkak)

driver.close()