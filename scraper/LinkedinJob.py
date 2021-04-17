#állásajánlat adatai
class LinkedinJob:
    def __init__(self, title, company, location, seniority, employment_type, industry_list, job_functions_list):
        self.title=title
        self.company=company
        self.location=location
        self.seniority=seniority
        self.employment_type=employment_type
        self.industry_list=industry_list
        self.job_functions_list=job_functions_list

    def __str__(self):
        return self.title + self.company + self.location+self.seniority + self.employment_type + str(self.industry_list) + str(self.job_functions_list)
