#állásajánlat adatai
class LinkedinJob:
    def __init__(self, title, company, location, experience_level, job_type, industry):
        self.title=title
        self.company=company
        self.location=location
        self.experience_level=experience_level
        self.job_type=job_type
        self.industry=industry

    def __str__(self):
        return self.title + self.company + self.location+self.experience_level + self.job_type + str(self.industry)
