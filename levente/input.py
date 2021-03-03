a='szures.txt' #szűrés file neve
b=1 #search bar sor
c=2 #location sor
d,e=5,9 #date posted sorok
f,g=11,17 #experience level sorok
h,k=19,26 #job type sorok
l=27 #remote sor
m=28 #easy apply sor
n=29 #under 10 applicants sor
o=31 #company sor
p=32 #industry sor
q=33 #job function sor


#input fájl összes sorának beolvasása
input_file=open(a, encoding="utf8")
inp=[line.strip().split() for line in input_file]

#search bar értékek, több szó is lehet
fsearch=''
for i in range(1,len(inp[b])):
    fsearch+=inp[b][i]+' '
fsearch=fsearch.strip()

#location értékek, több szó is lehet
flocation=''
for i in range(1,len(inp[c])):
    flocation+=inp[c][i]+' '
flocation=flocation.strip()

#date_posted, csak egy érték lehet
fdate=''
for i in inp[d:e]:
    if len(i)>1:
        fdate=i[0].strip(i[0][-1]).replace('_',' ')

#experience level, több érték is lehet     
fexp=[]
for i in inp[f:g]:
    if len(i)>1:
        fexp.append(i[0].strip(i[0][-1]).replace('_',' '))

#job type, több érték is lehet     
fjob=[]
for i in inp[h:k]:
    if len(i)>1:
        fjob.append(i[0].strip(i[0][-1]))

#eldöntendő szűrők 
fremote=inp[l][-1]
feasy=inp[m][-1]    
funder10=inp[n][-1]

#vállalatok listába
fcompany=''
for i in range(1, len(inp[o])):
    fcompany+=inp[o][i]+' '
fcompany=fcompany.strip().split(', ')

#industryk listába
findustry=''
for i in range(1, len(inp[p])):
    findustry+=inp[p][i]+' '
findustry=findustry.strip().split(', ')

#job function szűrő listázása
fjobfunc=''
for i in range(1, len(inp[q])):
    fjobfunc+=inp[q][i]+' '
fjobfunc=fjobfunc.strip().split(', ')


#teszteléshez outputok
print(fsearch)
print(flocation)
print(fdate)
print(fexp)
print(fjob)
print(fremote)
print(feasy)
print(funder10)
print(fcompany)
print(findustry)
print(fjobfunc)
