#állásajánlat adatai
class Munka:
    def __init__(self, title, company, location, seniority, industry_list, employment_type, job_functions_list):
        self.title=title
        self.company=company
        self.location=location
        self.seniority=seniority
        self.industry_list=industry_list
        self.employment_type=employment_type
        self.job_functions_list=job_functions_list

    def __str__(self):
        return self.title + self.company + self.location+self.seniority + str(self.industry_list) + self.employment_type+ str(self.job_functions_list)
