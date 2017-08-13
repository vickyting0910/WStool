#from yelpapi import YelpAPI
import pandas as pd
import re
from selenium import webdriver
import pandas as pd
from selenium import webdriver
import pysal as ps

inputshp='D:/crime/environmentdata/dallas/zoning/dallas_zcta.dbf'
db= ps.open(inputshp, 'r')
d = {col: db.by_col(col) for col in db.header}
dbf=pd.DataFrame(d)
zips=sorted(list(dbf['ZCTA5CE10']))
driver = webdriver.Firefox(executable_path=r'C:\DRIVERS\geckodriver.exe')

times1=[]
alcohol1=[]
kids1=[]
group1=[]
ambience1=[]
attire1=[]
parking1=[]
biking1=[]
noise1=[]
price1=[]
add1=[]
lats1=[]
longs1=[]
store1=[]
money1=[]
rating1=[]
#m=4
for m in range(len(zips))[15:22]:
    webpage='https://www.yelp.com/search?find_loc='+str(zips[m])
    

    try:
        driver.get(webpage)
    except:
        driver.get(webpage)
    response=driver.page_source

    regex_pp=' of ([0-9]+)'
    pattern_pp = re.compile(regex_pp)
    yy=re.findall(pattern_pp,response)
    if yy != [] and len(yy) != 1:
        cc = int(yy[0])
        pp = int(yy[1])

    for i in list(range(0,309,30)):
        webpage1='https://www.yelp.com/search?find_loc='+str(zips[m])+'&start='+str(i)
        try:
            driver.get(webpage1)
        except:
            driver.get(webpage1)
        response1=driver.page_source
        
        #regex_add='<address>((?:(?:\n|\r\n?).+)+)</address>'
        regex_add='<div class="secondary-attributes">((?:.|\n)*?)<span class="offscreen">Phone number</span>'
        pattern_add = re.compile(regex_add)
        add=[p.replace('\n', '').replace('  ','').replace('<br>',' ')[p.replace('\n', '').replace('  ','').replace('<br>',' ').rfind('<address>')+9:p.replace('\n', '').replace('  ','').replace('<br>',' ').rfind('</address>')] if '<address>' in p else p.replace('\n', '').replace('  ','').replace('<br>',' ')[p.replace('\n', '').replace('  ','').replace('<br>',' ').rfind('="service-area">')+16:p.replace('\n', '').replace('  ','').replace('<br>',' ').rfind('</div>')] for p in re.findall(pattern_add,response1) ]

        regex_longs=', "location": {"latitude": (.+?)}, "key": '
        pattern_longs = re.compile(regex_longs)
        lats = [float(p.replace(', "longitude":','').split(' ')[0]) for p in re.findall(pattern_longs,response1)]
        longs = [float(p.replace(', "longitude":','').split(' ')[1]) for p in re.findall(pattern_longs,response1)]
        
        regex_store='<span class="indexed-biz-name">(.+?)</span></a>'
        pattern_store = re.compile(regex_store)
        store=[p[p.rfind('>')+1:] for p in re.findall(pattern_store,response1)]
        
        #regex_money='<span class="business-attribute price-range">(.+?)</span>'
        regex_money='<div class="price-category">((?:.|\n)*?)</span>'
        pattern_money = re.compile(regex_money)
        money=re.findall(pattern_money,response1)
        money=[p[p.rfind('">')+2:] if not 'category-str-list' in p else '' for p in money ]

        rr=' rating-large" title="(.+?) star rating">'
        patternrr = re.compile(rr)
        regex_rating='<h3 class="search-result-title">((?:.|\n)*?)</div>'
        pattern_rating = re.compile(regex_rating)
        rating=re.findall(pattern_rating,response1)
        rating=[re.findall(patternrr,p)[0] if 'star rating' in p else '' for p in rating]

        regex_ID='([0-9]+)": {"url": "(.+?)", "location": {"latitude'
        pattern_ID = re.compile(regex_ID)
        ID=['/biz/'+str(''.join(p).split('/')[2]) for p in re.findall(pattern_ID,response1)]
        if len(add) != len(rating) or len(add) != len(money):
            print ('wrong '+str(i))
        if len(add) != len(longs) or len(add) != len(lats):
            print ('wrong '+str(i))
        week=[]
        times=[]
        alcohol=[]
        kids=[]
        group=[]
        ambience=[]
        attire=[]
        parking=[]
        biking=[]
        noise=[]
        price=[]
        for q in ID:
            webpage2='https://www.yelp.com'+str(q)
            try:
                driver.get(webpage2)
            except:
                driver.get(webpage2)
            response2=driver.page_source

            #regex_week='<th scope="row">(.+?)</th>'
            #pattern_week = re.compile(regex_week)
            #week.append(re.findall(pattern_week,response2))

            regex_times='<th scope="row">(.+?)</th>((?:(?:\n|\r\n?).+)+)<td>((?:(?:\n|\r\n?).+)+)</span>'
            pattern_times = re.compile(regex_times)
            tt=[re.split('\n\n|<br>',str(''.join(p)).replace('    ','').replace('<span class="nowrap">','').replace('</span>','').replace('</td>','').replace('<td class="extra">','').replace('<span class="nowrap closed">Closed now','').replace('<span class="nowrap open">Open now','')) for p in re.findall(pattern_times,response2)]
            [p.remove('\n') for p in tt if '\n' in p]
            times.append(tt)
            
            regex_alcohol='<dt class="attribute-key">((?:(?:\n|\r\n?).+)+)Alcohol((?:(?:\n|\r\n?).+)+)</dd>'
            pattern_alcohol = re.compile(regex_alcohol)
            aa=re.findall(pattern_alcohol,response2)
            if aa !=[]:
                aa=''.join(aa[0]).replace('    ','').replace('\n','').replace('<dd>','').replace('</dt>','')
                alcohol.append(aa)
            else:
                alcohol.append('')

            regex_kids='<dt class="attribute-key">((?:(?:\n|\r\n?).+)+)Good for Kids((?:(?:\n|\r\n?).+)+)</dd>'
            pattern_kids = re.compile(regex_kids)
            kk=re.findall(pattern_kids,response2)
            if kk !=[]:
                kk=''.join(kk[0]).replace('    ','').replace('\n','').replace('<dd>','').replace('</dt>','')
                kids.append(kk)
            else:
                kids.append('')
            
            regex_group='<dt class="attribute-key">((?:(?:\n|\r\n?).+)+)Good for Groups((?:(?:\n|\r\n?).+)+)</dd>'
            pattern_group = re.compile(regex_group)
            gg=re.findall(pattern_group,response2)
            if gg != []:
                gg=''.join(gg[0]).replace('    ','').replace('\n','').replace('<dd>','').replace('</dt>','')
                group.append(gg)
            else:
                group.append('')
            
            regex_ambience='<dt class="attribute-key">((?:(?:\n|\r\n?).+)+)Ambience((?:(?:\n|\r\n?).+)+)</dd>'
            pattern_ambience = re.compile(regex_ambience)
            am=re.findall(pattern_ambience,response2)
            if am !=[]:
                am=''.join(am[0]).replace('    ','').replace('\n','').replace('<dd>','').replace('</dt>','')
                ambience.append(am)
            else:
                ambience.append('')

            regex_attire='<dt class="attribute-key">((?:(?:\n|\r\n?).+)+)Attire((?:(?:\n|\r\n?).+)+)</dd>'
            pattern_attire = re.compile(regex_attire)
            at=re.findall(pattern_attire,response2)
            if at != []:
                at=''.join(at[0]).replace('    ','').replace('\n','').replace('<dd>','').replace('</dt>','')
                attire.append(at)
            else:
                attire.append('')

            regex_parking='<dt class="attribute-key">((?:(?:\n|\r\n?).+)+)Parking((?:(?:\n|\r\n?).+)+)</dd>'
            pattern_parking = re.compile(regex_parking)
            ppp=re.findall(pattern_parking,response2)
            if ppp != []:
                ppp=''.join(ppp[0]).replace('    ','').replace('\n','').replace('<dd>','').replace('</dt>','')
                parking.append(ppp)
            else:
                parking.append('')

            regex_biking='<dt class="attribute-key">((?:(?:\n|\r\n?).+)+)Bike Parking((?:(?:\n|\r\n?).+)+)</dd>'
            pattern_biking = re.compile(regex_biking)
            bi=re.findall(pattern_biking,response2)
            if bi !=[]:
                bi=''.join(bi[0]).replace('    ','').replace('\n','').replace('<dd>','').replace('</dt>','')
                biking.append(bi)
            else:
                biking.append('')

            regex_noise='<dt class="attribute-key">((?:(?:\n|\r\n?).+)+)Noise Level((?:(?:\n|\r\n?).+)+)</dd>'
            pattern_noise = re.compile(regex_noise)
            no=re.findall(pattern_noise,response2)
            if no != []:
                no=''.join(no[0]).replace('    ','').replace('\n','').replace('<dd>','').replace('</dt>','')
                noise.append(no)
            else:
                noise.append('')

            regex_price='<dd class="nowrap price-description">((?:(?:\n|\r\n?).+)+)</dd>'
            pattern_price = re.compile(regex_price)
            pr=re.findall(pattern_price,response2)
            if pr != []:
                pr=pr[0].replace('  ','').replace('\n','')
                price.append(pr)
            else:
                price.append('')
        #week1=week1+week
        times1=times1+times
        alcohol1=alcohol1+alcohol
        kids1=kids1+kids
        group1=group1+group
        ambience1=ambience1+ambience
        attire1=attire1+attire
        parking1=parking1+parking
        biking1=biking1+biking
        noise1=noise1+noise
        price1=price1+price
        add1=add1+add
        lats1=lats1+lats
        longs1=longs1+longs
        store1=store1+store
        money1=money1+money
        rating1=rating1+rating

    table1 = pd.DataFrame()
    table1['store']=store1
    table1['addresses']=add1
    table1['longitude']=longs1
    table1['latitude']=lats1
    table1['rating']=rating1
    table1['money']=money1
    table1['price']=price1
    table1['noise']=noise1
    table1['parking']=parking1
    table1['biking']=biking1
    table1['attire']=attire1
    table1['ambience']=ambience1
    table1['group']=group1
    table1['kids']=kids1
    table1['alcohol']=alcohol1
    table1['times']=times1
    table1.to_csv('D:/crime/environmentdata/dallas/places/yelp_'+str(zips[m])+'.csv',index=False)

