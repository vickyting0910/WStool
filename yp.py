import httplib2
import re
import pandas as pd
import requests
from selenium import webdriver
import numpy as num

#city='richardson-tx'
city='dallas-tx'
#sword='restaurants'
#sword='casinos'
#sword='hotel'
#sword='lodging'
#sword='gas+stations'
#sword='apartment'
#sword='pharmacy'
#sword='bank'
#sword='shop'
#sword='store'
sword='mall'
pages='?page='
http = httplib2.Http()
driver = webdriver.Firefox(executable_path=r'C:\DRIVERS\geckodriver.exe')
webpage='https://www.yellowpages.com/'+str(city)+'/'+str(sword)+str(pages)+'1'
try:
    driver.get(webpage)
except:
    driver.get(webpage)
response=driver.page_source

#status, response = http.request('https://www.yellowpages.com/'+str(city)+'/'+str(sword)+str(pages)+'1')
#response=response.decode('utf-8')

#page
regex_pp='<meta name="description" content="Find (.+?) listings related to '+str(sword).replace('+',' ').title()+' in Dallas on YP.com.'
pattern_pp = re.compile(regex_pp)
pp=re.findall(pattern_pp,response)
if pp != []:
    pp = float(pp[0])
else:
    regex_pp='of (.+?)<span>results'
    pattern_pp = re.compile(regex_pp)
    pp=float(re.findall(pattern_pp,response)[0])    
mypages=(pp/30)+1
if (mypages - int(mypages)) > 0:
    mypages= int(mypages) + 1
else:
    mypages=int(mypages)

store1=[]
add1=[]
city1=[]
trip1=[]
BBB1=[]
YP1=[]
days1=[]
times1=[]
alcohol1=[]
zips1=[]

for p in range(1,mypages):
    if p == 1:
        response1=response
    else:
        webpage1='https://www.yellowpages.com/'+str(city)+'/'+str(sword)+str(pages)+str(p)
        try:
            driver.get(webpage1)
        except:
            driver.get(webpage1)
        response1=driver.page_source
    #status, response = http.request('https://www.yellowpages.com/'+str(city)+'/'+str(sword)+str(pages)+str(p))
    #response=response.decode('utf-8')
    while '<html><head><script src="https://www.google.com/recaptcha/api.js">' in str(response1):
        status1, response1 = http.request('https://www.yellowpages.com/'+str(city)+'/'+str(sword)+str(pages)+str(p))
        response1=response1.decode('utf-8')
        print ('slow')
        while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response1):
            status1, response1 = http.request('https://www.yellowpages.com/'+str(city)+'/'+str(sword)+str(pages)+str(p))
            response1=response1.decode('utf-8')
            print ('slow')
    while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response1):
        status1, response1 = http.request('https://www.yellowpages.com/'+str(city)+'/'+str(sword)+str(pages)+str(p))
        response1=response1.decode('utf-8')
        print ('slow')
    #store
    regex_store='<span itemprop="name">(.+?)</span>'
    pattern_store = re.compile(regex_store)
    store = re.findall(pattern_store,response1)
    dd=[s for s in range(len(store)) if 'Home' == store[s] or city.replace('-',', ').title().replace('Tx','TX') == store[s]]
    store=list(num.delete(store, dd))
    
    #address
    regex_add='<div data-israteable="true" class="info-section info-primary">((?:.|\n)*?)<div itemprop="telephone" class="phones phone primary">'
    pattern_add = re.compile(regex_add)
    addadd = re.findall(pattern_add,response1)
    add=[s[s.rfind('="')+2:s.rfind('">')] if '<p class="adr">' in s else s[s.find('class="street-address">')+23:s.find('</span><span ')] for s in addadd]
 
    #
    if len(store) != len(add):
        regex_add='itemprop="address" class="adr">(.+?)</span>'
        pattern_add = re.compile(regex_add)
        add = [p[p.rfind('>')+1:] if 'streetAddress' in p else '' for p in re.findall(pattern_add,response1) ]
        if len(store) != len(add):
            regex_add='<span itemprop="streetAddress" class="street-address">(.+?)</span>'
            pattern_add = re.compile(regex_add)
            add = re.findall(pattern_add,response1)
            if len(store) != len(add):
                regex_add='</span></a></h2>(.+?)<div itemprop="telephone" class="phones phone primary">'
                pattern_add = re.compile(regex_add)
                adda = re.findall(pattern_add,response1)
                rr=regex_add='<span itemprop="streetAddress" class="street-address">(.+?)</span>'
                pa = re.compile(rr)
                rr1=regex_add='<span itemprop="addressLocality" class="locality">(.+?)</span></p>'
                pa1 = re.compile(rr1)
                #add=[re.findall(pa,p)[0] if 'streetAddress' in p else re.findall(pa1,p)[0].replace('&nbsp;</span><span itemprop="addressRegion">',' ').replace('</span>&nbsp;<span itemprop="postalCode">',' ') for p in add1 ]
                add=[]
                for p in adda:
                    if 'streetAddress' in p:
                        add.append(re.findall(pa,p)[0])
                    elif not 'streetAddress' in p and 'itemprop="addressLocality"' in p:
                        aa=re.findall(pa1,p)[0].replace('&nbsp;</span><span itemprop="addressRegion">',' ').replace('</span>&nbsp;<span itemprop="postalCode">',' ')
                        add.append(aa)
                    elif re.findall(pa1,p) == []:
                        aa=p[p.find('="adr">')+7:p.find('.<meta')]
                        add.append(aa)
                    else:    
                        add.append(re.findall(pa1,p)[0])

                if len(store) != len(add):
                    print ('check '+str(p))
    regex_cc='<span itemprop="addressLocality" class="locality">(.+?),&nbsp;</span><span itemprop="addressRegion">'
    pattern_cc = re.compile(regex_cc)
    #
    cc=[s[s.rfind('="')+2:s.rfind('">')] if '<p class="adr">' in s else re.findall(pattern_cc,s)[0] for s in addadd]
    if len(cc) != len(add):
        cc = re.findall(pattern_cc,response1)

    #rating (1) BBB, (2) YP, (3) TripAdvisor
    #regex_rating='</span></a></h2>(.+?)<p'
    #regex_rating='></a></h2><div data(.+?)<p'
    regex_rating='<span itemprop="name">(.+?)<p'
    pattern_rating = re.compile(regex_rating)
    rating = re.findall(pattern_rating,response1)
    dd=[s for s in range(len(rating)) if 'Home' == rating[s][:4] or city.replace('-',', ').title().replace('Tx','TX') == rating[s][:8]]
    rating=list(num.delete(rating, dd))
    trip=[]
    BBB=[]
    YP=[]
    for i in rating:
        if 'data-tripadvisor' in i:
                regex_tt='<div data-tripadvisor="{&quot;rating&quot;:&quot;(.+?)&'
                pattern_tt = re.compile(regex_tt)
                yy=re.findall(pattern_tt,i)
                if yy != []:
                    trip.append(yy[0])
                else:
                    trip.append('')

        else:
                trip.append('')
        
        if 'bbb-rating' in i:
                regex_B='<span class="bbb-rating extra-rating hasRating">BBB Rating:(.+?)</span>'
                pattern_B = re.compile(regex_B)
                yy=re.findall(pattern_B,i)
                if yy != []:
                    #print (yy[0])
                    BBB.append(yy[0])
                else:
                    BBB.append('')
        else:
                BBB.append('')

        if 'class="count"' in i:
                regex_yy='class="rating hasExtraRating"><div class="result-rating(.+?) "><span class="count">'
                pattern_yy = re.compile(regex_yy)
                yy=re.findall(pattern_yy,i)
                if yy == []:
                    regex_yy='<div class="result-rating(.+?) "><span class="count">'
                    pattern_yy = re.compile(regex_yy)
                    yy=re.findall(pattern_yy,i)
                if yy == []:
                    regex_yy='class="rating"><div class="result-rating(.+?) "><span class="count">'
                    pattern_yy = re.compile(regex_yy)
                    yy=re.findall(pattern_yy,i)
                if yy != []:
                    #print (yy[0])
                    YP.append(yy[0])
                else:
                    YP.append('')
                
        else:
                YP.append('')
          
    #Hour
    regex_web='&nbsp;<a href="(.+?)" data-analytics='
    pattern_web = re.compile(regex_web)
    web = re.findall(pattern_web,response1)

    http = httplib2.Http()
    days=[]
    times=[]
    alcohol=[]
    
    mylist=iter(web)
    for i in mylist:
        if 'http' in i:
            days.append('')
            times.append('')
            alcohol.append('')
            continue
        else:
            webpage2='https://www.yellowpages.com'+str(i)
            try:
                driver.get(webpage2)
            except:
                driver.get(webpage2)
            response2=driver.page_source
            #status2, response2 = http.request('https://www.yellowpages.com'+str(i))
            #response2=response2.decode('utf-8')
            while '<html><head><script src="https://www.google.com/recaptcha/api.js">' in str(response2):
                status2, response2 = http.request('https://www.yellowpages.com'+str(i))
                response2=response2.decode('utf-8')
                print ('slow')
                while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response2):
                    status2, response2 = http.request('https://www.yellowpages.com'+str(i))
                    response2=response2.decode('utf-8')
                    print ('slow')
            while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response2):
                status2, response2 = http.request('https://www.yellowpages.com'+str(i))
                response2=response2.decode('utf-8')
                print ('slow')
        #Hour
        regex_hh='<span class="day-label">(.+?)</span><span'
        pattern_hh = re.compile(regex_hh)
        days.append(re.findall(pattern_hh,response2))

        regex_t1='<span class="day-hours">(.+?)</span>'
        pattern_t1 = re.compile(regex_t1)
        times.append(re.findall(pattern_t1,response2))

        #Alcohol
        if 'Alcohol' in response2:
            regex_aa='Alcohol</strong>:&nbsp;(.+?)</p>'
            pattern_aa = re.compile(regex_aa)
            aa=re.findall(pattern_aa,response2)
            if aa != [] and aa[0] != 'No':
                alcohol.append(aa[0])
            else:
                alcohol.append('')
        else:
            alcohol.append('')
    
    
    add1=add1+add
    city1=city1+cc
    store1=store1+store
    trip1=trip1+trip
    BBB1=BBB1+BBB
    YP1=YP1+YP
    days1=days1+days
    times1=times1+times
    alcohol1=alcohol1+alcohol
    print (len(add1))
    print (len(store1))
    print (len(trip))

    if p in list(range(1,mypages+3,int(mypages/4)))+[mypages-1]:
        print ('save csv')
        table1 = pd.DataFrame()
        table1['stores']=store1
        table1['addresses']=add1
        table1['city']=city1
        table1['trip']=trip1
        table1['BBB rating']=BBB1
        table1['YP rating']=YP1
        table1['days']=days1
        table1['times']=times1
        table1['alcohol']=alcohol1
        table1.to_csv('D:/crime/environmentdata/dallas/places/yp_dallas'+str(p)+'_'+str(sword)+'.csv',index=False)

table1 = pd.DataFrame()
table1['stores']=store1
table1['addresses']=add1
table1['city']=city1
table1['trip']=trip1
table1['BBB rating']=BBB1
table1['YP rating']=YP1
table1['days']=days1
table1['times']=times1
table1['alcohol']=alcohol1
table1.to_csv('D:/crime/environmentdata/dallas/places/yp_dallas'+'_'+str(sword)+'.csv',index=False)
