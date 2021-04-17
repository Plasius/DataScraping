class Param:
    def __init__(self, keywords, location, date, experience_levels_list, job_types_list, is_remote, is_easy_apply, companies_list):
        self.keywords = keywords
        self.location = location
        self.date = date
        self.experience_levels_list = experience_levels_list
        self.job_types_list = job_types_list
        self.is_remote = is_remote
        self.is_easy_apply = is_easy_apply
        self.companies_list = companies_list

    def __str__(self):
        print(self.keywords)
        print(self.location)
        print(self.date)
        print(self.experience_levels_list)
        print(self.job_types_list)
        print(self.is_remote)
        print(self.is_easy_apply)
        print(self.companies_list)
        return ''