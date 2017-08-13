import httplib2
import re
import pysal as ps
import pandas as pd
import requests
from selenium import webdriver

inputshp='D:/crime/environmentdata/dallas/zoning/dallas_zcta.dbf'
db= ps.open(inputshp, 'r')
d = {col: db.by_col(col) for col in db.header}
dbf=pd.DataFrame(d)
zips=sorted(list(dbf['ZCTA5CE10']))

headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","accept-charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3","accept-encoding": "gzip,deflate,sdch","accept-language": "en-US,en;q=0.8",}
driver = webdriver.Firefox(executable_path=r'C:\DRIVERS\geckodriver.exe')
#driver1 = webdriver.Firefox(executable_path=r'C:\DRIVERS\geckodriver.exe')
#driver2 = webdriver.Firefox(executable_path=r'C:\DRIVERS\geckodriver.exe')

#city='richardson-tx'
#city='dallas-tx'
for m in range(len(zips))[31:40]:
    pages='_p'
    http = httplib2.Http()
    #webpage='https://www.zillow.com/'+str(city)+'/1'+str(pages)+'/'
    webpage='https://www.zillow.com/homes/for_sale/'+zips[m]+'_rb/1'+str(pages)+'/'
    try:
        driver.get(webpage)
    except:
        driver.get(webpage)
    response=driver.page_source
    
    #response = requests.get(webpage, headers=headers)
    #response=response.text
    
    #status, response = http.request(webpage)
    #response=response.decode('utf-8')
    
    while '<html><head><script src="https://www.google.com/recaptcha/api.js">' in str(response):
        status, response = http.request(webpage)
        response=response.decode('utf-8')
        print ('slow')
        while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response):
            status, response = http.request(webpage)
            response=response.decode('utf-8')
            print ('slow')
    while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response):
        status, response = http.request(webpage)
        response=response.decode('utf-8')
        print ('slow')
    while '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"' in str(response):
        status, response = http.request(webpage)
        response=response.decode('utf-8')
        print ('slow')

    #page
    #regex_pp='<li class="zsg-pagination_active">(.+?)</a></li><li class="zsg-pagination-next">'
    #pattern_pp = re.compile(regex_pp)
    #pp = int(re.findall(pattern_pp,response)[0][re.findall(pattern_pp,response)[0].rfind('>')+1:])+1

    regex_pp='{"totalResultCount":(.+?),"forSaleCount":'
    pattern_pp = re.compile(regex_pp)
    pp = (float(re.findall(pattern_pp,response)[0]))/25+1
    if (pp-int(pp))>0:
        pp=int(pp)+1
    else:
        pp=int(pp)

    longs1=[]
    lats1=[]
    add1=[]
    price11=[]
    beds1=[]
    baths1=[]
    floorsize1=[]
    builtin1=[]
    lot1=[]
    remodel1=[]
    type11=[]
    family1=[]
    sstyle1=[]
    lastsold11=[]
    fore1=[]
    
    addadd1=[]
    priceprice11=[]
    bedsbeds1=[]
    bathsbaths1=[]
    floorsizefloorsize1=[]
    builtinbuiltin1=[]
    lotlot1=[]
    remodelremodel1=[]
    typetype11=[]
    familyfamily1=[]
    sstylesstyle1=[]
    lastsoldlastsold11=[]
    forefore1=[]

    for p in range(pp)[1:]:
        if p == 1:
            response1=response
        else:
            http = httplib2.Http()
            #webpage1='https://www.zillow.com/'+str(city)+'/'+str(p)+str(pages)+'/'
            webpage1='https://www.zillow.com/homes/for_sale/'+zips[m]+'_rb/'+str(p)+str(pages)+'/'
            try:
                driver.get(webpage1)
            except:
                driver.get(webpage1)
            response1=driver.page_source
        
        #response1 = requests.get(webpage1, headers=headers)
        #response1=response1.text
        
        #status1, response1 = http.request(webpage1)
        #response1=response1.decode('utf-8')
        while '<html><head><script src="https://www.google.com/recaptcha/api.js">' in str(response1):
            #print ('web errors1')
            status1, response1 = http.request(webpage1)
            response1=response1.decode('utf-8')
            print ('slow')
            while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response1):
                status1, response1 = http.request(webpage1)
                response1=response1.decode('utf-8')
                print ('slow')
        while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response1):
            status1, response1 = http.request(webpage1)
            response1=response1.decode('utf-8')
            print ('slow')
        while '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"' in str(response1):
            status1, response1 = http.request(webpage1)
            response1=response1.decode('utf-8')

        #coordinates
        regex_longs='<meta itemprop="longitude" content="(.+?)"></meta></span><div class="zsg-photo-card-caption">'
        pattern_longs = re.compile(regex_longs)
        longs = re.findall(pattern_longs,response1)
        if longs==[]:
            regex_longs='<meta itemprop="longitude" content="(.+?)"></meta></span><div class="zsg-photo-card-caption">'.replace('</meta>','')
            pattern_longs = re.compile(regex_longs)
            longs = re.findall(pattern_longs,response1)

        regex_lats='<meta itemprop="latitude" content="(.+?)"></meta><meta itemprop="longitude"'
        pattern_lats = re.compile(regex_lats)
        lats = re.findall(pattern_lats,response1)
        if lats == []:
            regex_lats='<meta itemprop="latitude" content="(.+?)"></meta><meta itemprop="longitude"'.replace('</meta>','')
            pattern_lats = re.compile(regex_lats)
            lats = re.findall(pattern_lats,response1)

        #id
        regex_id='></div><a href="(.+?)" class="zsg-photo-card-overlay-link routable hdp-link routable mask hdp-link">'
        pattern_id = re.compile(regex_id)
        ID = re.findall(pattern_id,response1)
        
        if len(ID) == len(longs):
            pass
            
        else:
            regex_id='></div><a href="(.+?)"'
            pattern_id = re.compile(regex_id)
            ID = re.findall(pattern_id,response1)
            #driver.get(webpage1)
            #response1=driver.page_source
            if len(ID) != len(longs):
                print (zips[m])
            """
            regex_longs='<meta itemprop="longitude" content="(.+?)"></meta></span><div class="zsg-photo-card-caption">'
            pattern_longs = re.compile(regex_longs)
            longs = re.findall(pattern_longs,response1)
            if longs==[]:
                regex_longs='<meta itemprop="longitude" content="(.+?)"></meta></span><div class="zsg-photo-card-caption">'.replace('</meta>','')
                pattern_longs = re.compile(regex_longs)
                longs = re.findall(pattern_longs,response1)
                
            regex_lats='<meta itemprop="latitude" content="(.+?)"></meta><meta itemprop="longitude"'
            pattern_lats = re.compile(regex_lats)
            lats = re.findall(pattern_lats,response1)
            if lats == []:
                regex_lats='<meta itemprop="latitude" content="(.+?)"></meta><meta itemprop="longitude"'.replace('</meta>','')
                pattern_lats = re.compile(regex_lats)
                lats = re.findall(pattern_lats,response1)
            
            regex_id='></div><a href="(.+?)" class="zsg-photo-card-overlay-link routable hdp-link routable mask hdp-link">'
            pattern_id = re.compile(regex_id)
            ID = re.findall(pattern_id,response1)
            if len(ID) == len(longs):
                print ('Inconsistent '+str(zips[m]))
            """

        add=[]
        price=[]
        beds=[]
        baths=[]
        floorsize=[]
        builtin=[]
        lot=[]
        remodel=[]
        type1=[]
        family=[]
        sstyle=[]
        lastsold=[]
        fore=[]
        mylist=iter(ID)
        for q in mylist:
            if 'AuthRequired' in q:
                response2=''
                add.append('')
                price.append('')
                beds.append('')
                baths.append('')
                floorsize.append('')
                builtin.append('')
                lot.append('')
                remodel.append('')
                type1.append('')
                family.append('')
                sstyle.append('')
                lastsold.append('')
                fore.append('')
                continue
            else:
                http = httplib2.Http()
                webpage2='https://www.zillow.com'+str(q)
                try:
                    driver.get(webpage2)

                except:
                    driver.get(webpage2)
                response2=driver.page_source
            
                #response2 = requests.get(webpage2, headers=headers)
                #response2=response2.text
            
                #status2, response2 = http.request(webpage2)
                #response2=response2.decode('utf-8')
            while '<html><head><script src="https://www.google.com/recaptcha/api.js">' in str(response2):
                #print ('web errors2')
                status2, response2 = http.request(webpage2)
                response2=response2.decode('utf-8')
                print ('slow')
                while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response2):
                    status2, response2 = http.request(webpage2)
                    response2=response2.decode('utf-8')
                    print ('slow')
            while '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>'in str(response2):
                status2, response2 = http.request(webpage2)
                response2=response2.decode('utf-8')
                print ('slow')
            while '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"' in str(response2):
                status2, response2 = http.request(webpage2)
                response2=response2.decode('utf-8')
                print ('slow')
            #address
            regex_add='<title>(.+?)</title>'
            pattern_add = re.compile(regex_add)
            yy=re.findall(pattern_add,response2)
            if yy != []:
                add.append(yy[0][:re.findall(pattern_add,response2)[0].find(' |')])
            else:
                add.append('')
            #print (re.findall(pattern_add,response2)[0][:re.findall(pattern_add,response2)[0].find(' |')])
            
            #beds, baths, floor size, built in and style
            regex_meta='<meta name="description" content="(.+?)."></meta><meta name="author" content="Zillow, Inc."/>'
            pattern_meta = re.compile(regex_meta)
            meta = re.findall(pattern_meta,response2)
            if meta == []:
                regex_meta='<meta name="description" content="(.+?)."></meta><meta name="author" content="Zillow, Inc."/>'.replace('</meta>','').replace('"/','"')
                pattern_meta = re.compile(regex_meta)
                meta = re.findall(pattern_meta,response2)
            
            meta=meta[0]
            if yy != []:
                yy=[g for g in meta.split(' ') if '$' in g]
                if yy != []:
                    price.append(yy[0])
                    price1=[g for g in meta.split(' ') if '$' in g][0]
                else:
                    price.append('')
                    price1=[]
            
                bbed=meta.split(' ')[meta.split(' ').index(price1)+1:][0]
                if 'bed' in bbed:
                    beds.append('')
                else:
                    beds.append(bbed)
                bbath=meta.split(' ')[meta.split(' ').index('bed,')+1:][0]
                if 'bath' in bbath:
                    baths.append('')
                else:
                    baths.append(bbath)
                ffloor=meta.split(' ')[meta.split(' ').index('bath,')+1:][0]
                if 'sqft' in ffloor:
                    floorsize.append('')
                else:
                    floorsize.append(ffloor)
                bbuilt=meta.split(' ')[meta.split(' ').index('built')+2].replace('.','')
                if 'MLS' in bbuilt:
                    builtin.append('')
                else:
                    builtin.append(bbuilt)
                ffamily=' '.join(meta.split(' ')[meta.split(' ').index('sqft')+1:meta.split(' ').index('located')])
                family.append(ffamily)
            else:
                price.append('')
                beds.append('')
                baths.append('')
                floorsize.append('')
                builtin.append('')
                family.append('')
            #Lot size
            #regex_lot='<span class="hdp-fact-name">Lot: </span><span class="hdp-fact-value">(.+?)</span></li></ul></div>'
            regex_lot='<span class="hdp-fact-name">Lot: </span><span class="hdp-fact-value">(.+?)</span></li>'
            pattern_lot = re.compile(regex_lot)
            if re.findall(pattern_lot,response2) !=[]:
                lot.append(re.findall(pattern_lot,response2)[0].replace(' sqft','').replace(' acres','').replace(',',''))
            else:
                lot.append('')

            #foreclosed
            regex_fore='<input type="hidden" id="home-type" value="(.+?)"/><div class="zsg-form-field">'
            pattern_fore = re.compile(regex_fore)
            if re.findall(pattern_fore,response2) !=[]:
                pass
            else:
                regex_fore='<input type="hidden" id="home-type" value="(.+?)"/><div class="zsg-form-field">'.replace('type="hidden" ','').replace('/><div class="zsg-form-field">','')
                pattern_fore = re.compile(regex_fore)
                #re.findall(pattern_fore,response2)
            if re.findall(pattern_fore,response2) !=[]:
                fore.append(re.findall(pattern_fore,response2)[0].replace(' sqft','').replace(' acres','').replace(',',''))
            else:
                fore.append('')

            #Last remodel year
            regex_remodel='<span class="hdp-fact-name">Last remodel year: </span><span class="hdp-fact-value">(.+?)</span></li><li class="">'
            pattern_remodel = re.compile(regex_remodel)
            rr=re.findall(pattern_remodel,response2)
            if rr != []:
                remodel.append(rr[0])
            else:
                remodel.append('')

            #Structure type
            regex_type1='<span class="hdp-fact-name">Structure type: </span><span class="hdp-fact-value">(.+?)</span></li><li class="">'
            pattern_type1 = re.compile(regex_type1)
            rr=re.findall(pattern_type1,response2)
            """
            if rr ==[]:
                regex_type1='<span class="hdp-fact-name">Structure type: </span><span class="hdp-fact-value">(.+?)</span></li><li class="">'.replace('Structure type','Structural Style').replace('<li class="">','')
                pattern_type1 = re.compile(regex_type1)
                rr=re.findall(pattern_type1,response2)
            """
            if rr != []:
                type1.append(rr[0])
            else:
                type1.append('')

            #Structure style
            regex_style='<span class="hdp-fact-name">Structural Style: </span><span class="hdp-fact-value">(.+?)</span></li></ul></div>'
            pattern_style = re.compile(regex_style)
            ss=re.findall(pattern_style,response2)
            if ss != []:
                sstyle.append(ss[0])
            else:
                sstyle.append('')

            #Last sold
            regex_lastsold='<span class="hdp-fact-name">Last sold: </span><span class="hdp-fact-value">(.+?)</span></li><li class="">'
            pattern_lastsold = re.compile(regex_lastsold)
            lastsold1=re.findall(pattern_lastsold,response2)
            if lastsold1 != []:
                lastsold.append(lastsold1[0])
            else:
                lastsold.append('')
        
        longs1=longs1+longs
        lats1=lats1+lats
        add1=add1+add
        price11=price11+price
        beds1=beds1+beds
        baths1=baths1+baths
        floorsize1=floorsize1+floorsize
        builtin1=builtin1+builtin
        lot1=lot1+lot
        fore1=fore1+fore
        remodel1=remodel1+remodel
        type11=type11+type1
        family1=family1+family
        sstyle1=sstyle1+sstyle
        lastsold11=lastsold11+lastsold
    #"""
    if len(longs1) != len(add1):
        print (zips[m])
    else:
        table1 = pd.DataFrame()
        table1['longitude']=longs1
        table1['latitude']=lats1
        table1['addresses']=add1
        table1['price']=price11
        table1['beds']=beds1
        table1['baths']=baths1
        table1['floorsize']=floorsize1
        table1['builtin']=builtin1
        table1['lot']=lot1
        table1['foreclosed']=fore1
        table1['remodel']=remodel1
        table1['type']=type11
        table1['family']=family1
        table1['sstyle']=sstyle1
        table1['lastsold']=lastsold11
        table1.to_csv('D:/crime/environmentdata/dallas/places/zillow_'+str(zips[m])+'.csv',index=False)
    #"""
