#Selenium import
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#Python import
from time import sleep
from datetime import datetime
import codecs
#Datascraping import
import Parameters
import LinkedinJob

#init and return a webdriver
def init_driver() -> webdriver.Chrome:
	options = webdriver.ChromeOptions() 
	options.add_argument("user-data-dir=/scraperdata8") # cache delete
	return webdriver.Chrome(options=options)

#read filter options from txt and return them through a Param object
def read_txt() -> Parameters:
	#starting line of the filters in the txt
	keywords_line = 1
	location_line = 2
	date_posted_start, date_posted_end = 5, 9
	experience_level_start, experience_level_end = 11, 17
	job_type_start, job_type_end = 21, 28
	remote_line_start, remote_line_end = 30, 33
	easy_apply_line = 34
	company_line = 18
	email_line = 36
	password_line = 37

	#read txt
	input_file = open('filter.txt', encoding="utf8")
	input = [line.strip().split() for line in input_file]

	#strings
	keywords = ' '.join(input[keywords_line][1:])
	location = ' '.join(input[location_line][1:])
	email = ' '.join(input[email_line][1:])
	password = ' '.join(input[password_line][1:])

	#single-choice values
	date = [date[0].strip(date[0][-1]).replace('_',' ') for date in input[date_posted_start:date_posted_end] if len(date)>1]

	#multiple-choice values
	experience_levels_list = [level[0].strip(level[0][-1]).replace('_',' ') for level in input[experience_level_start:experience_level_end] if len(level) > 1]
	job_types_list = [job_type[0].strip(job_type[0][-1]) for job_type in input[job_type_start:job_type_end] if len(job_type)>1]
	remote_type_list = [remote_type[0].strip(remote_type[0][-1]) for remote_type in input[remote_line_start:remote_line_end] if len(remote_type)>1]

	#true or false values
	is_easy_apply = True if input[easy_apply_line][-1]=='Y' else False   

	#lists
	if len(input[company_line]) != 1:
		companies_list = ' '.join((input[company_line][1:])).split(', ')
	else:
		companies_list = []

	#return Parameters object with imported filters
	param = Parameters.Parameters(keywords, location, date, experience_levels_list, job_types_list, remote_type_list, is_easy_apply, companies_list, email, password)
	return param

#login and navigate to /jobs/search
def login(driver, param):
	#chrome megnyitasa
	driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
	driver.maximize_window()

	try:
		#type in credentials
		username=driver.find_element(By.NAME, "session_key")
		WebDriverWait(driver, 5).until(EC.visibility_of(username))
		username.send_keys(param.email)

		password=driver.find_element(By.NAME, "session_password")
		WebDriverWait(driver, 5).until(EC.visibility_of(password))
		password.send_keys(param.password)
		
		password.send_keys(Keys.RETURN)
		
		sleep(3)
	except:
		print('Login átugrása')

	driver.get("https://www.linkedin.com/jobs/search/")
	sleep(3)

#filter job listings based on the Param object
def filter_results(driver, param):
	'''
	Filter options:
	- Keywords - type-in
	- Location - type-in
	- Date Posted - single choice
	- Experience Level - multiple choice
	- Company - multiple choice, type-in
	- Job Type - multiple choice
	- Remote - true/false
	- Easy Apply - true/false
	'''

	#type-in elements
	if param.keywords:
		try:
			search_bar = driver.find_element(By.CSS_SELECTOR, "[aria-label='Search by title, skill, or company']")#[0].find_elements(By.TAG_NAME, "input")[0]
			search_bar.send_keys(str(param.keywords))
			sleep(2)
		except:
			print('Nem sikerült a search bar-ba írni')

	if param.location:
		try:
			location_bar = driver.find_element(By.CSS_SELECTOR, "[aria-label='City, state, or zip code']")#[0].find_elements(By.TAG_NAME, "input")[0]
			location_bar.send_keys(Keys.CONTROL, 'a')
			location_bar.send_keys(Keys.BACKSPACE)
			location_bar.send_keys(str(param.location))
		except:
			print('Nem sikerült a location bar-ba írni')
	
	driver.find_element(By.CLASS_NAME, 'jobs-search-box__submit-button').click()

	sleep(3)

	#Open the dropdown of the filter, choose filter and hit esc - Date Posted
	if param.date:
		try:
			driver.find_element(By.XPATH, "//button[text()='Date Posted']").click()
			sleep(2)

			label_el_date_posted = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[text()=\'"+param.date[0]+"\']/../..")))
			label_el_date_posted.click()
			sleep(2)

			webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
			sleep(2)
		except:
			print('Nem sikerült dátum mezőt kiválasztani')

	#Open the dropdown of the filter, choose filter and hit esc - Experience Level
	if param.experience_levels_list:
		try:
			experience_level = driver.find_element(By.XPATH, "//button[text()='Experience Level']")
			experience_level.click()
			sleep(2)

			for level in param.experience_levels_list:
				try:
					input_el_experience_level = driver.find_element(By.XPATH, "//span[text()=\'"+level+"\']")
					input_el_experience_level = input_el_experience_level.find_element(By.XPATH, '..')
					input_el_experience_level = input_el_experience_level.find_element(By.XPATH, '..')
					input_el_experience_level.click()
				except:
					print('Hiba történt az egyik Experience level kiválasztásakor: '+ level)
				sleep(1)

			
			webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
			sleep(2)
		except:
			print('Nem sikerült a megfelelő Experience Levelt/eket kiválasztani')


	#Open the dropdown of the filter, type in companies with downarrow and enter, then hit esc - Company
	if param.companies_list:
		# try:
			company = driver.find_element(By.XPATH, "//button[text()='Company']")
			company.click()
			sleep(2)

			for company_name in param.companies_list:
				# try:
				company_bar = driver.find_element(By.XPATH, '//div[1]/div/form/fieldset/div[1]/div/div/input')
				company_bar.send_keys(company_name)
				sleep(2)
				webdriver.ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
				sleep(1)
				webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
				sleep(2)
				# except:
				# 	print('Hiba történt egy Company kiválasztásakor: ' + company_name)
			
			webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
			sleep(1)
			webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
			sleep(1)
		# except:
		# 	print('Nem sikerült a megfelelő Companyt/kat kiválasztani')
			
		
	#Open the dropdown of the filter, choose filter and hit esc - Job Type
	if param.job_types_list:
		try:
			job_type = driver.find_element(By.XPATH, "//button[text()='Job Type']")
			job_type.click()
			sleep(2)

			for pos in param.job_types_list:
				try:
					input_el_job_type = driver.find_element(By.XPATH, "//label[@for=\'"+"jobType-"+pos[0]+"\']")
					input_el_job_type.click()
				except:
					print('Hiba történt egy Job Type kiválasztásakor: ' + pos)
				sleep(1)
				
			webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
			sleep(2)
		except:
			print('Nem sikerült a megfelelő Job Typeot/kat kiválasztani')

	#Push button if filter is true for remote
	if param.remote_types_list:
    	
		try:
			remote_type = driver.find_element(By.XPATH, "//button[text()='On-site/Remote']")
			remote_type.click()
			sleep(2)

			for i in range(len(param.remote_types_list)):
				try:
					input_el_remote_type = driver.find_element(By.XPATH, "//label[@for=\'"+"workplaceType-"+str(i+1)+"\']")
					input_el_remote_type.click()
				except:
					print('Hiba történt egy Job Type kiválasztásakor: ' + pos)
				sleep(1)
				
			webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
			sleep(2)
		except:
			print('Nem sikerült a megfelelő Workplace Typeot/kat kiválasztani')

	#Push button if filter is true for easy apply
	if param.is_easy_apply == True:
		try:
			easy_apply = driver.find_element(By.XPATH, "//button[text()='Easy Apply']")
			easy_apply.click()
			sleep(2)  
		except:
			print('Nem sikerült az Easy Applyt kiválasztani')

#get the details from the currently opened job page
def extract(driver) -> LinkedinJob:
	#create a job class
	munka = LinkedinJob.LinkedinJob('','','','','','')

	#extract title
	try:
		title = driver.find_element(By.CLASS_NAME, "t-24")
		munka.title = title.text
	except:
		print('Nem sikerült az állás nevét kimenteni')

	#case 1: company name is a link
	try:
		company = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__subtitle-primary-grouping")
		munka.company = company.find_element(By.TAG_NAME, "a").text
	except:
		#case 2: company name is not a link
		try:
			company = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__subtitle-primary-grouping")
			munka.company = company.find_element(By.TAG_NAME, "span").text
		except:
			print('Nem sikerült az állásadó cég nevét kimenteni: ' + str(munka))


	#extract location
	try:
		location = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__bullet")
		munka.location = location.text
	except:
		print('Nem sikerült a helyszínt kimenteni: ' + str(munka))

	#extract experience_level  ujrairni szepen TODO
	try:
		title = driver.find_element_by_xpath('//div[@class="jobs-unified-top-card__job-insight"]/span')
		title = title.text.split(" ")
		title = " ".join(title[2:])
		munka.experience_level = title
	except:
		print("nem találtam az experience_levelt")

	#extract job_type TODO
	try:
		title = driver.find_element_by_xpath('//div[@class="jobs-unified-top-card__job-insight"]/span')
		title = title.text.split(" ")[0]
		munka.job_type = title
	except:
		print("nem találtam a job type-ot")

	#extract industry TODO
	try:
		title = driver.find_element_by_xpath('//div[@class="jobs-unified-top-card__job-insight"][2]/span')
		title = title.text
		title = title.split(" ")[3:]
		title = " ".join(title)
		if "this job" not in title:
			munka.industry = title
	except:
		print("nem találtam az industryt")



	return munka

#navigate through the filtered jobs and pages, while clicking on every job listing
def navigate(driver, page):
	page = 1
	munkak = []

	#navigate until an error occurs
	while True:
		try:
			try:
				#loop through jobs
				for i in range(0, 25):
					job = driver.find_element(By.CLASS_NAME, 'jobs-search-two-pane__job-card-container--viewport-tracking-'+str(i))
					job.click()
					sleep(2)

					# print(driver.current_url)
					if '/company/' in str(driver.current_url):
						driver.execute_script("window.history.go(-1)")
						sleep(2)
						i=-1
						continue
					#visszalepeskor nem menti le a hibas allasajanlat adatait
					#a kovetkezo oldal lehet pontokkal van feltuntetve
					munkak.append(extract(driver))
					print(munkak[-1])
			except:
				print('Nincs több állás az oldalon')
			

			#attempt clicking on the next page
			page = page + 1
			# btn = driver.find_element(By.CSS_SELECTOR, "li[data-test-pagination-page-btn='{0}']".format(page))
			#btn.click()
			#sleep(5)

			pagebtn = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Page {0}']".format(page))[0]##.find_elements(By.TAG_NAME"button")[0]
			pagebtn.click()
			sleep(5)

		except:
			print('Nincs több oldal')
			break

	return munkak

#export the extracted jobs to a CSV TODO
def export(lista):
	now = datetime.now()
	file_name = now.strftime("%Y-%m-%d-%H-%M")
	file = codecs.open(file_name + '.csv','w', 'utf-8')

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



# read job filters
param = read_txt()

# create driver
driver = init_driver()

# login
login(driver, param)


# filter jobs
filter_results(driver, param)

#get jobs from the page
munkak = navigate(driver, 1)

#export jobs
export(munkak)
