#állásajánlat adatai
class Job:
    def __init__(self, title, company, location, seniority, industry, employment_type, job_functions, description):
        self.title=title
        self.company=company
        self.location=location
        self.seniority=seniority
        self.industry=industry
        self.employment_type=employment_type
        self.job_functions=job_functions
        self.description=description
