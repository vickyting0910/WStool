import httplib2
import re

city='richardson-tx'
pages='_p'
http = httplib2.Http()
webpage='https://www.zillow.com/'+str(city)+'/1'+str(pages)+'/'
status, response = http.request(webpage)
response=response.decode('utf-8')

#page
regex_pp='<li class="zsg-pagination_active">(.+?)</a></li><li class="zsg-pagination-next">'
pattern_pp = re.compile(regex_pp)
pp = int(re.findall(pattern_pp,response)[0][re.findall(pattern_pp,response)[0].rfind('>')+1:])+1

for p in [range(pp)[1:][0]]:
    http = httplib2.Http()
    webpage1='https://www.zillow.com/'+str(city)+'/'+str(p)+str(pages)+'/'
    status1, response1 = http.request(webpage1)
    response1=response1.decode('utf-8')
    
    #coordinates
    regex_longs='<meta itemprop="longitude" content="(.+?)"></meta></span><div class="zsg-photo-card-caption">'
    pattern_longs = re.compile(regex_longs)
    longs = re.findall(pattern_longs,response1)
    
    regex_lats='<meta itemprop="latitude" content="(.+?)"></meta><meta itemprop="longitude"'
    pattern_lats = re.compile(regex_lats)
    lats = re.findall(pattern_lats,response1)

    #id
    regex_id='></div><a href="(.+?)" class="zsg-photo-card-overlay-link routable hdp-link routable mask hdp-link">'
    pattern_id = re.compile(regex_id)
    ID = re.findall(pattern_id,response1)
    
    add=[]
    price=[]
    beds=[]
    baths=[]
    floorsize=[]
    builtin=[]
    lot=[]
    remodel=[]
    type1=[]
    style=[]
    lastsold=[]
    for q in ID[1:5]:
        http = httplib2.Http()
        webpage2='https://www.zillow.com'+str(q)
        status2, response2 = http.request(webpage2)
        response2=response2.decode('utf-8')
        
        #address
        regex_add='<title>(.+?)</title>'
        pattern_add = re.compile(regex_add)
        add.append(re.findall(pattern_add,response2)[0][:re.findall(pattern_add,response2)[0].find(' |')])
        
        #beds, baths, floor size, built in and style
        regex_meta='<meta name="description" content="(.+?)."></meta><meta name="author" content="Zillow, Inc."/>'
        pattern_meta = re.compile(regex_meta)
        meta = re.findall(pattern_meta,response2)[0]
        
        price.append([g for g in meta.split(' ') if '$' in g][0])
        price1=[g for g in meta.split(' ') if '$' in g][0]
        beds.append(meta.split(' ')[meta.split(' ').index(price1)+1:][0])
        baths.append(meta.split(' ')[meta.split(' ').index('bed,')+1:][0])
        floorsize.append(meta.split(' ')[meta.split(' ').index('bath,')+1:][0])
        builtin.append(meta.split(' ')[meta.split(' ').index('built')+2].replace('.',''))
        style.append(' '.join(meta.split(' ')[meta.split(' ').index('sqft')+1:meta.split(' ').index('located')]))
        
        #Lot size
        regex_lot='<span class="hdp-fact-name">Lot: </span><span class="hdp-fact-value">(.+?)</span></li></ul></div>'
        pattern_lot = re.compile(regex_lot)
        lot.append(int(re.findall(pattern_lot,response2)[0].replace(' sqft','').replace(',','')))

        #Last remodel year
        regex_remodel='<span class="hdp-fact-name">Last remodel year: </span><span class="hdp-fact-value">(.+?)</span></li><li class="">'
        pattern_remodel = re.compile(regex_remodel)
        remodel.append(int(re.findall(pattern_remodel,response2)[0]))

        #Structure type
        regex_type1='<span class="hdp-fact-name">Structure type: </span><span class="hdp-fact-value">(.+?)</span></li><li class="">'
        pattern_type1 = re.compile(regex_type1)
        type1.append(re.findall(pattern_type1,response2)[0])

        #Structure style
        regex_style='<span class="hdp-fact-name">Structural Style: </span><span class="hdp-fact-value">(.+?)</span></li></ul></div>'
        pattern_style = re.compile(regex_style)
        style.append(re.findall(pattern_style,response2)[0])

        #Last sold
        regex_lastsold='<span class="hdp-fact-name">Last sold: </span><span class="hdp-fact-value">(.+?)</span></li><li class="">'
        pattern_lastsold = re.compile(regex_lastsold)
        lastsold.append(re.findall(pattern_lastsold,response2))
        if lastsold != []:
            lastsold.append(lastsold[0])
        else:
            lastsold.append('')

