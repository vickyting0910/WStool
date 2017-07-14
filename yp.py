import httplib2
import re

city='richardson-tx'
sword='restaurants'
pages='?page='
http = httplib2.Http()
status, response = http.request('https://www.yellowpages.com/'+str(city)+'/'+str(sword)+str(pages)+'1')
response=response.decode('utf-8')

#page
regex_pp='<meta name="description" content="Find (.+?) listings related to Restaurants in Richardson on YP.com.'
pattern_pp = re.compile(regex_pp)
pp = float(re.findall(pattern_pp,response)[0])
mypages=(pp/30)+1
if (mypages - int(mypages)) > 0:
    mypages= int(mypages) + 1
else:
    mypages=int(mypages)

for p in range(1,mypages):
    status, response = http.request('https://www.yellowpages.com/'+str(city)+'/'+str(sword)+str(pages)+str(p))
    response=response.decode('utf-8')

    #store
    regex_store='<span itemprop="name">(.+?)</span>'
    pattern_store = re.compile(regex_store)
    store = re.findall(pattern_store,response)[3:]

    #address
    regex_add='<span itemprop="streetAddress" class="street-address">(.+?)</span>'
    pattern_add = re.compile(regex_add)
    add = re.findall(pattern_add,response)

    #rating (1) BBB, (2) YP, (3) TripAdvisor
    regex_rating='</span></a></h2>(.+?)<p itemscope itemtype="http://schema.org/PostalAddress" itemprop="address" class="adr"><span itemprop="streetAddress" class="street-address">'
    pattern_rating = re.compile(regex_rating)
    rating = re.findall(pattern_rating,response)
    trip=[]
    BBB=[]
    YP=[]
    for i in rating:
        if 'data-tripadvisor' in i:
                regex_tt='<div data-tripadvisor=\'{"rating":"(.+?)"'
                pattern_tt = re.compile(regex_tt)
                trip.append(re.findall(pattern_tt,i)[0])

        else:
                trip.append('')
        
        if 'bbb-rating' in i:
                regex_B='<span class="bbb-rating extra-rating hasRating">BBB Rating:(.+?)</span>'
                pattern_B = re.compile(regex_B)
                BBB.append(re.findall(pattern_B,i)[0])
        else:
                BBB.append('')

        if 'class="count"' in i:
                regex_yy='class="rating hasExtraRating"><div class="result-rating(.+?) "><span class="count">'
                pattern_yy = re.compile(regex_yy)
                yy=re.findall(pattern_yy,i)
                if yy != []:
                    print (yy[0])
                    YP.append(yy[0])
                else:
                    YP.append('')
                
        else:
                YP.append('')
                
    #Hour
    regex_web='&nbsp;<a href="(.+?)" data-analytics='
    pattern_web = re.compile(regex_web)
    web = re.findall(pattern_web,response)
    http = httplib2.Http()
    days=[]
    times=[]
    alcohol=[]

    for i in web:
        status1, response1 = http.request('https://www.yellowpages.com'+str(i))
        response1=response1.decode('utf-8')
        #Hour
        regex_hh='<span class="day-label">(.+?)</span><span'
        pattern_hh = re.compile(regex_hh)
        days.append(re.findall(pattern_hh,response1))

        regex_t1='<span class="day-hours">(.+?)</span>'
        pattern_t1 = re.compile(regex_t1)
        times.append(re.findall(pattern_t1,response1))

        #Alcohol
        if 'Alcohol' in response1:
            regex_aa='Alcohol</strong>:&nbsp;(.+?)</p>'
            pattern_aa = re.compile(regex_aa)
            aa=re.findall(pattern_aa,response1)[0]
            if aa != 'No':
                alcohol.append(aa)
            else:
                alcohol.append('')
        else:
            alcohol.append('')
