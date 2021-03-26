import codecs

#állásajánlat adatai
class Munka:
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


#példa ajánlatok
pelda1=Munka('title1','company1','location1','seniority1','employment1',['ind A','ind B'],['job A','job B','job C'])
pelda2=Munka('title2','company2','location2','seniority2','employment2',['ind A','ind B','ind C'],['job A','job B'])
pelda3=Munka('title3','company3','location3','seniority3','employment3',[],['job A'])
#példa lista
lista=[pelda1,pelda2,pelda3]

file= codecs.open('exported.csv','w', 'utf-8')

#fejléc
for att in lista[0].__dict__.keys():
    if att.split('_')[-1]=='list':
        for repeat in range(1,4): file.write('"'+str(att)+str(repeat)+'",')
    else: file.write('"'+str(att)+'",')
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
