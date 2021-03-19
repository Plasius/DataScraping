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

#példa ajánlatok
pelda1=Job('a1','a2','a3','a4','a5','a6','a7','a8 ő')
pelda2=Job('b1','b2','b3','b4','b5','b6','b7','b8 á')
pelda3=Job('c1','c2','c3','c4','c5','c6','c7','c8 ű')
#példa lista
lista=[pelda1,pelda2,pelda3]

file=open('exported.csv','w')

#fejléc
for att in lista[0].__dict__.keys():
    file.write('"'+str(att)+'",')
file.write('\n')

#ajánlatok
for ajanlat in lista:
    for att, value in ajanlat.__dict__.items():
        file.write('"'+str(value)+'",')
    file.write('\n')

file.close()
