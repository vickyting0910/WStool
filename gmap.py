import numpy as num
import glob
import pandas as pd
import pysal as ps
import requests
from selenium import webdriver
import httplib2
import re
from datetime import datetime
from dateutil import parser
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup 

def gaddress(dbb,IN_Address,IN_City,IN_State):
    http = httplib2.Http()
    #driver = webdriver.Firefox(executable_path=r'C:\DRIVERS\geckodriver.exe')
    driver = webdriver.Chrome(executable_path=r'C:\DRIVERS\chromedriver.exe')
    timezone=[0]*len(dbb)
    spend=[0]*len(dbb)
    mondaystime=[0]*len(dbb)
    mondayetime=[0]*len(dbb)
    tuesdaystime=[0]*len(dbb)
    tuesdayetime=[0]*len(dbb)
    wednesdaystime=[0]*len(dbb)
    wednesdayetime=[0]*len(dbb)
    thursdaystime=[0]*len(dbb)
    thursdayetime=[0]*len(dbb)
    fridaystime=[0]*len(dbb)
    fridayetime=[0]*len(dbb)
    saturdaystime=[0]*len(dbb)
    saturdayetime=[0]*len(dbb)
    sundaystime=[0]*len(dbb)
    sundayetime=[0]*len(dbb)
    mondaypop=[0]*len(dbb)
    tuesdaypop=[0]*len(dbb)
    wednesdaypop=[0]*len(dbb)
    thursdaypop=[0]*len(dbb)
    fridaypop=[0]*len(dbb)
    saturdaypop=[0]*len(dbb)
    sundaypop=[0]*len(dbb)
    mondaypt=[0]*len(dbb)
    tuesdaypt=[0]*len(dbb)
    wednesdaypt=[0]*len(dbb)
    thursdaypt=[0]*len(dbb)
    fridaypt=[0]*len(dbb)
    saturdaypt=[0]*len(dbb)
    sundaypt=[0]*len(dbb)
    match=[0]*len(dbb)
    place=[0]*len(dbb)
    sttype=[0]*len(dbb)
    for j in range(len(dbb)):
        time1=time.time()
        webpage='https://www.google.com/maps/place/'+str(dbb[IN_Address][j].replace(' ','+'))+',+'+str(dbb[IN_City][j])+',+'+str(dbb[IN_State][j])
        try:
            driver.get(webpage)
        except:
            time.sleep(60)
            driver.get(webpage)
        response=driver.page_source
        regex='spend(.+?)here'   #spending time     
        pattern = re.compile(regex)
        pp=re.findall(pattern,response)
        try:
            a=pp[0].strip(' ')
            spend[j]=a                
        except:
            spend[j]=0
        regex='"America/(.+?)\\",' #time zone       
        pattern = re.compile(regex)
        pp=re.findall(pattern,response)
        try:
            a=pp[0].strip('\\')
            timezone[j]=a
        except:
            timezone[j]=0
        bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
        x=bs_obj.find_all("div", {"class": "section-result-title-container"})        
        if x == []:
            time.sleep(10)
            x=bs_obj.find_all("div", {"class": "section-result-title-container"})
        #x= [p for p in x if 'CVS' not in p and 'ELEVEN' not in p and 'ATM' not in p]
        ltp=len(x)
        aa=[x[p].find("h3", {"class": "section-result-title"}).text.strip(' ') for p in range(len(x))]
        ty=[p.text for p in bs_obj.find_all("span", {"class": "section-result-details"})]
        #ind=[q for q in range(len(x)) if ('bar'.upper() in ty[q].upper() or 'cafe'.upper() in ty[q].upper() or 'liquor'.upper() in ty[q].upper() or 'wine'.upper() in ty[q].upper() or 'night club'.upper() in ty[q].upper() or 'restaurant'.upper() in ty[q].upper() or 'club'.upper() in ty[q].upper() or 'drinking'.upper() in ty[q].upper() or 'hotel'.upper() in ty[q].upper() or 'Cigar'.upper() in ty[q].upper() or 'beer'.upper() in ty[q].upper() or 'alcohol'.upper() in ty[q].upper() or 'lodging'.upper() in ty[q].upper() or 'Mexican'.upper() in ty[q].upper() or 'Chinese'.upper() in ty[q].upper() or 'Grill'.upper() in ty[q].upper() or 'Bakery'.upper() in ty[q].upper() or 'italian'.upper() in ty[q].upper() or 'sandwich'.upper() in ty[q].upper() or 'food'.upper() in ty[q].upper() or 'pub'.upper() in ty[q].upper() or 'Indian'.upper() in ty[q].upper() or 'barbecue'.upper() in ty[q].upper() or 'greek'.upper() in ty[q].upper() or 'hamburger'.upper() in ty[q].upper() or 'mediterranean'.upper() in ty[q].upper() or 'seafood'.upper() in ty[q].upper() or 'sushi'.upper() in ty[q].upper() or 'tex-mex'.upper() in ty[q].upper() or 'japanese'.upper() in ty[q].upper() or 'lebanese'.upper() in ty[q].upper() or 'breakfast'.upper() in ty[q].upper() or 'american'.upper() in ty[q].upper() or 'beef'.upper() in ty[q].upper() or 'chicken'.upper() in ty[q].upper() or 'shabu-shabu'.upper() in ty[q].upper() or 'persian'.upper() in ty[q].upper() or 'vegetarian'.upper() in ty[q].upper() or 'brazilian'.upper() in ty[q].upper() or 'oyster'.upper() in ty[q].upper() or 'thai'.upper() in ty[q].upper() or 'louisiana'.upper() in ty[q].upper() or 'health'.upper() in ty[q].upper() or 'pizza'.upper() in ty[q].upper() or 'cantonese'.upper() in ty[q].upper() or 'ethiopian'.upper() in ty[q].upper() or 'steak'.upper() in ty[q].upper() or 'french'.upper() in ty[q].upper() or 'asian'.upper() in ty[q].upper() or 'hot dog'.upper() in ty[q].upper() or 'african'.upper() in ty[q].upper() or 'jamaican'.upper() in ty[q].upper() or 'cuban'.upper() in ty[q].upper() or 'chophouse'.upper() in ty[q].upper() or 'irish'.upper() in ty[q].upper() or 'gastropub'.upper() in ty[q].upper() or 'brewpub'.upper() in ty[q].upper() or 'cajun'.upper() in ty[q].upper() or 'sport'.upper() in ty[q].upper()) and 'photo'.upper() not in ty[q].upper()] 
        #ind=[q for q in range(len(x)) if 'Apartment'.upper() in ty[q].upper() or 'Housing'.upper() in ty[q].upper() or 'Community'.upper() in ty[q].upper()] 
        #ind=[q for q in range(len(x)) if 'Bank'.upper() in ty[q].upper() or  'ATM'.upper() in ty[q].upper()] 
        #ind=[q for q in range(len(x)) if 'casino'.upper() in ty[q].upper()]
        #ind=[q for q in range(len(x)) if 'gas'.upper() in ty[q].upper() or 'gas station'.upper() in ty[q].upper()]
        #ind=[q for q in range(len(x)) if 'lodging'.upper() in ty[q].upper() or 'hotel'.upper() in ty[q].upper() or 'Motel'.upper() in ty[q].upper() or 'Lodge'.upper() in ty[q].upper()] 
        #ind=[q for q in range(len(x)) if 'mall'.upper() in ty[q].upper() or 'shopping'.upper() in ty[q].upper() or 'outlet'.upper() in ty[q].upper() or 'department'.upper() in ty[q].upper() or 'clothing'.upper() in ty[q].upper() ] 
        #ind=[q for q in range(len(x)) if 'pharmacy'.upper() in ty[q].upper() or 'drug'.upper() in ty[q].upper() or 'medical'.upper() in ty[q].upper()]
        #ind=[q for q in range(len(x)) if 'store'.upper() in ty[q].upper() and not 'drug'.upper() in ty[q].upper() ]
        #ind=[q for q in range(len(x)) if 'store'.upper() in ty[q].upper()] 
        ind=[q for q in range(len(x)) if 'library'.upper() in ty[q].upper()] 
        a=[aa[p] for p in range(len(x)) if p in ind] #store name
        ty=[ty[p] for p in range(len(x)) if p in ind] #store type
        sttype[j]=ty
        tp=[] #At this Location
        matchL=[]
        mondaypop1=[]
        mondaypt1=[]
        tuesdaypop1=[]
        tuesdaypt1=[]
        wednesdaypop1=[]
        wednesdaypt1=[]
        thursdaypop1=[]
        thursdaypt1=[]
        fridaypop1=[]
        fridaypt1=[]
        saturdaypop1=[]
        saturdaypt1=[]
        sundaypop1=[]
        sundaypt1=[]
        mondaystime1=[]
        mondayetime1=[]
        tuesdaystime1=[]
        tuesdayetime1=[]
        wednesdaystime1=[]
        wednesdayetime1=[]
        thursdaystime1=[]
        thursdayetime1=[]
        fridaystime1=[]
        fridayetime1=[]
        saturdaystime1=[]
        saturdayetime1=[]
        sundaystime1=[]
        sundayetime1=[]
        for p, q in zip(ind,a):
            #get store names
            #a=x[p].find("h3", {"class": "section-result-title"}).text.strip(' ')
            tp.append(q)  
            #click button to access stores
            try:
                driver.find_elements_by_css_selector('.section-result-title > span:nth-child(1)')[p].click()
            except:
                time.sleep(20)
                try:
                    driver.find_elements_by_css_selector('.section-result-title > span:nth-child(1)')[p].click()
                except:
                    time.sleep(20)
                    try:
                        driver.find_elements_by_css_selector('.section-result-title > span:nth-child(1)')[p].click()
                    except:
                        time.sleep(20)
                        try:
                            driver.find_elements_by_css_selector('.section-result-title > span:nth-child(1)')[p].click()
                        except:
                            time.sleep(20)
                            try:
                                driver.find_elements_by_css_selector('.section-result-title > span:nth-child(1)')[p].click()
                            except:
                                print ('click')
                                pass
                
            #get the name of the store
            try:
                bb = BeautifulSoup(driver.page_source, 'html.parser')
                tt=bb.find("h1", {"class": "section-hero-header-title"}).text
            except:
                time.sleep(20)
                bb = BeautifulSoup(driver.page_source, 'html.parser')
                tt=bb.find("h1", {"class": "section-hero-header-title"}).text
            if tt == q:
                matchL.append(tt)            
            if tt != q:
                time.sleep(20)
                #get the name of the store
                bb = BeautifulSoup(driver.page_source, 'html.parser')
                tt=bb.find("h1", {"class": "section-hero-header-title"}).text
                matchL.append(tt)
            print ('xt '+str(tt))
            #get popular time            
            try:
                myindex=str(int(bb.find("div", {"class": "section-popular-times"}).find("div", {"class": "section-popular-times-container"}).get('jstcache'))+1)
                ss0_sunday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[0].find_all("div", {"class":"section-popular-times-bar"})]
                ss1_monday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[1].find_all("div", {"class":"section-popular-times-bar"})]
                ss2_tuesday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[2].find_all("div", {"class":"section-popular-times-bar"})]
                ss3_wednesday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[3].find_all("div", {"class":"section-popular-times-bar"})]
                ss4_thursday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[4].find_all("div", {"class":"section-popular-times-bar"})]
                ss5_friday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[5].find_all("div", {"class":"section-popular-times-bar"})]
                ss6_saturday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[6].find_all("div", {"class":"section-popular-times-bar"})]
                s0=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss0_sunday]
                s1=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss1_monday]
                s2=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss2_tuesday]
                s3=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss3_wednesday]
                s4=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss4_thursday]
                s5=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss5_friday]
                s6=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss6_saturday]
                mondaypop1.append(', '.join([p[0] for p in s1]))
                mondaypt1.append(', '.join([p[1] for p in s1]))
                tuesdaypop1.append(', '.join([p[0] for p in s2]))
                tuesdaypt1.append(', '.join([p[1] for p in s2]))
                wednesdaypop1.append(', '.join([p[0] for p in s3]))
                wednesdaypt1.append(', '.join([p[1] for p in s3]))
                thursdaypop1.append(', '.join([p[0] for p in s4]))
                thursdaypt1.append(', '.join([p[1] for p in s4]))
                fridaypop1.append(', '.join([p[0] for p in s5]))
                fridaypt1.append(', '.join([p[1] for p in s5]))
                saturdaypop1.append(', '.join([p[0] for p in s6]))
                saturdaypt1.append(', '.join([p[1] for p in s6]))
                sundaypop1.append(', '.join([p[0] for p in s0]))
                sundaypt1.append(', '.join([p[1] for p in s0]))
            except:
                mondaypop1.append('')
                mondaypt1.append('')
                tuesdaypop1.append('')
                tuesdaypt1.append('')
                wednesdaypop1.append('')
                wednesdaypt1.append('')
                thursdaypop1.append('')
                thursdaypt1.append('')
                fridaypop1.append('')
                fridaypt1.append('')
                saturdaypop1.append('')
                saturdaypt1.append('')
                sundaypop1.append('')
                sundaypt1.append('')        
            
            #get open/ closing time
            try:
                openclose=[p.get('aria-label') for p in bb.find_all("div", {"class": "section-open-hours-container"})][0].replace('. Hide open hours for the week','').split(',')
                if 'Open 24 hours' in openclose[0] or 'Open 24 hours' in openclose[1] or 'Open 24 hours' in openclose[2] or 'Open 24 hours' in openclose[3] or 'Open 24 hours' in openclose[4] or 'Open 24 hours' in openclose[5] or 'Open 24 hours' in openclose[6]:
                    mondaystime1.append(' '.join(openclose[0].split(' ')[1:]))
                    mondayetime1.append(0)
                    tuesdaystime1.append(' '.join(openclose[1].split(' ')[1:]))
                    tuesdayetime1.append(0)
                    wednesdaystime1.append(' '.join(openclose[2].split(' ')[1:]))
                    wednesdayetime1.append(0)
                    thursdaystime1.append(' '.join(openclose[3].split(' ')[1:]))
                    thursdayetime1.append(0)
                    fridaystime1.append(' '.join(openclose[4].split(' ')[1:]))
                    fridayetime1.append(0)
                    saturdaystime1.append(' '.join(openclose[5].split(' ')[1:]))
                    saturdayetime1.append(0)
                    sundaystime1.append(' '.join(openclose[6].split(' ')[1:]))
                    sundayetime1.append(0)
                else:
                    oc=[re.findall(r"[\w:']+|[.,!?;]", p.split(' ')[1]) for p in openclose]
                    if 'Closed' not in oc[0]:
                        mondaystime1.append(oc[0][0])
                        mondayetime1.append(oc[0][1])
                    else:
                        mondaystime1.append(oc[0][0])
                        mondayetime1.append(0)
                    if 'Closed' not in oc[1]:
                        tuesdaystime1.append(oc[1][0])
                        tuesdayetime1.append(oc[1][1])
                    else:
                        tuesdaystime1.append(oc[1][0])
                        tuesdayetime1.append(0)
                    if 'Closed' not in oc[2]:
                        wednesdaystime1.append(oc[2][0])
                        wednesdayetime1.append(oc[2][1])
                    else:
                        wednesdaystime1.append(oc[2][0])
                        wednesdayetime1.append(0)
                    if 'Closed' not in oc[3]:
                        thursdaystime1.append(oc[3][0])
                        thursdayetime1.append(oc[3][1])
                    else:
                        thursdaystime1.append(oc[3][0])
                        thursdayetime1.append(0)
                    if 'Closed' not in oc[4]:
                        fridaystime1.append(oc[4][0])
                        fridayetime1.append(oc[4][1])
                    else:
                        fridaystime1.append(oc[4][0])
                        fridayetime1.append(0)
                    if 'Closed' not in oc[5]:
                        saturdaystime1.append(oc[5][0])
                        saturdayetime1.append(oc[5][1])
                    else:
                        saturdaystime1.append(oc[5][0])
                        saturdayetime1.append(0)
                    if 'Closed' not in oc[6]:
                        sundaystime1.append(oc[6][0])
                        sundayetime1.append(oc[6][1])
                    else:
                        sundaystime1.append(oc[6][0])
                        sundayetime1.append(0)
            except:
                mondaystime1.append('')
                mondayetime1.append('')
                tuesdaystime1.append('')
                tuesdayetime1.append('')
                wednesdaystime1.append('')
                wednesdayetime1.append('')
                thursdaystime1.append('')
                thursdayetime1.append('')
                fridaystime1.append('')
                fridayetime1.append('')
                saturdaystime1.append('')
                saturdayetime1.append('')
                sundaystime1.append('')
                sundayetime1.append('')
            #back to address page
            if p != range(ltp)[-1]:
                driver.get(webpage)

        place[j]=tp #', '.join(tp)
        match[j]=matchL #', '.join(matchL)
        mondaypop[j]=mondaypop1
        mondaypt[j]=mondaypt1
        tuesdaypop[j]=tuesdaypop1
        tuesdaypt[j]=tuesdaypt1
        wednesdaypop[j]=wednesdaypop1
        wednesdaypt[j]=wednesdaypt1
        thursdaypop[j]=thursdaypop1
        thursdaypt[j]=thursdaypt1
        fridaypop[j]=fridaypop1
        fridaypt[j]=fridaypt1
        saturdaypop[j]=saturdaypop1
        saturdaypt[j]=saturdaypt1
        sundaypop[j]=sundaypop1
        sundaypt[j]=sundaypt1
        mondaystime[j]=mondaystime1
        mondayetime[j]=mondayetime1
        tuesdaystime[j]=tuesdaystime1
        tuesdayetime[j]=tuesdayetime1
        wednesdaystime[j]=wednesdaystime1
        wednesdayetime[j]=wednesdayetime1
        thursdaystime[j]=thursdaystime1
        thursdayetime[j]=thursdayetime1
        fridaystime[j]=fridaystime1
        fridayetime[j]=fridayetime1
        saturdaystime[j]=saturdaystime1
        saturdayetime[j]=saturdayetime1
        sundaystime[j]=sundaystime1
        sundayetime[j]=sundayetime1
        print ('Addressed Store '+str(j)+' '+str(place[j]))            
        time2=time.time()
        print ('time '+str(j)+' '+str(time2-time1))
        #save temporary files
        if j in range(0,len(dbb),100):
            dbb['timezone']=timezone
            dbb['spend']=spend
            dbb['mondaystime']=mondaystime
            dbb['mondayetime']=mondayetime
            dbb['tuesdaystime']=tuesdaystime
            dbb['tuesdayetime']=tuesdayetime
            dbb['wednesdaystime']=wednesdaystime
            dbb['wednesdayetime']=wednesdayetime
            dbb['thursdaystime']=thursdaystime
            dbb['thursdayetime']=thursdayetime
            dbb['fridaystime']=fridaystime
            dbb['fridayetime']=fridayetime
            dbb['saturdaystime']=saturdaystime
            dbb['saturdayetime']=saturdayetime
            dbb['sundaystime']=sundaystime
            dbb['sundayetime']=sundayetime
            dbb['mondaypop']=mondaypop
            dbb['tuesdaypop']=tuesdaypop
            dbb['wednesdaypop']=wednesdaypop
            dbb['thursdaypop']=thursdaypop
            dbb['fridaypop']=fridaypop
            dbb['saturdaypop']=saturdaypop
            dbb['sundaypop']=sundaypop
            dbb['mondaypt']=mondaypt
            dbb['tuesdaypt']=tuesdaypt
            dbb['wednesdaypt']=wednesdaypt
            dbb['thursdaypt']=thursdaypt
            dbb['fridaypt']=fridaypt
            dbb['saturdaypt']=saturdaypt
            dbb['sundaypt']=sundaypt
            dbb['match']=match
            dbb['place']=place
            dbb['address']=dbb[IN_Address].map(str)+','+dbb[IN_City].map(str)+','+dbb[IN_State]
            dbb['sttype']=sttype
            dbb.to_csv('rest_temp.csv',index=False)
    dbb['timezone']=timezone
    dbb['spend']=spend
    dbb['mondaystime']=mondaystime
    dbb['mondayetime']=mondayetime
    dbb['tuesdaystime']=tuesdaystime
    dbb['tuesdayetime']=tuesdayetime
    dbb['wednesdaystime']=wednesdaystime
    dbb['wednesdayetime']=wednesdayetime
    dbb['thursdaystime']=thursdaystime
    dbb['thursdayetime']=thursdayetime
    dbb['fridaystime']=fridaystime
    dbb['fridayetime']=fridayetime
    dbb['saturdaystime']=saturdaystime
    dbb['saturdayetime']=saturdayetime
    dbb['sundaystime']=sundaystime
    dbb['sundayetime']=sundayetime
    dbb['mondaypop']=mondaypop
    dbb['tuesdaypop']=tuesdaypop
    dbb['wednesdaypop']=wednesdaypop
    dbb['thursdaypop']=thursdaypop
    dbb['fridaypop']=fridaypop
    dbb['saturdaypop']=saturdaypop
    dbb['sundaypop']=sundaypop
    dbb['mondaypt']=mondaypt
    dbb['tuesdaypt']=tuesdaypt
    dbb['wednesdaypt']=wednesdaypt
    dbb['thursdaypt']=thursdaypt
    dbb['fridaypt']=fridaypt
    dbb['saturdaypt']=saturdaypt
    dbb['sundaypt']=sundaypt
    dbb['match']=match
    dbb['place']=place
    dbb['sttype']=sttype
    dbb['address']=dbb[IN_Address].map(str)+','+dbb[IN_City].map(str)+','+dbb[IN_State]
    dbb.to_csv('rest_temp.csv',index=False)
    return dbb

def gplace(dbb,place,city):
    http = httplib2.Http()
    #driver = webdriver.Firefox(executable_path=r'C:\DRIVERS\geckodriver.exe')
    driver = webdriver.Chrome(executable_path=r'C:\DRIVERS\chromedriver.exe')
    timezone=[0]*len(dbb)
    spend=[0]*len(dbb)
    mondaystime=[0]*len(dbb)
    mondayetime=[0]*len(dbb)
    tuesdaystime=[0]*len(dbb)
    tuesdayetime=[0]*len(dbb)
    wednesdaystime=[0]*len(dbb)
    wednesdayetime=[0]*len(dbb)
    thursdaystime=[0]*len(dbb)
    thursdayetime=[0]*len(dbb)
    fridaystime=[0]*len(dbb)
    fridayetime=[0]*len(dbb)
    saturdaystime=[0]*len(dbb)
    saturdayetime=[0]*len(dbb)
    sundaystime=[0]*len(dbb)
    sundayetime=[0]*len(dbb)
    mondaypop=[0]*len(dbb)
    tuesdaypop=[0]*len(dbb)
    wednesdaypop=[0]*len(dbb)
    thursdaypop=[0]*len(dbb)
    fridaypop=[0]*len(dbb)
    saturdaypop=[0]*len(dbb)
    sundaypop=[0]*len(dbb)
    mondaypt=[0]*len(dbb)
    tuesdaypt=[0]*len(dbb)
    wednesdaypt=[0]*len(dbb)
    thursdaypt=[0]*len(dbb)
    fridaypt=[0]*len(dbb)
    saturdaypt=[0]*len(dbb)
    sundaypt=[0]*len(dbb)
    match=[0]*len(dbb)
    addrs=[0]*len(dbb)
    for j in range(len(dbb)):
        time1=time.time()
        webpage='https://www.google.com/maps/search/'+str(dbb[place][j].replace(' ','+'))+',+'+str(city)
        try:
            driver.get(webpage)
        except:
            time.sleep(60)
            driver.get(webpage)
        response=driver.page_source
        regex='spend(.+?)here'   #spending time     
        pattern = re.compile(regex)
        pp=re.findall(pattern,response)
        try:
            a=pp[0].strip(' ')
            spend[j]=a                
        except:
            spend[j]=0
        regex='"America/(.+?)\\",' #time zone       
        pattern = re.compile(regex)
        pp=re.findall(pattern,response)
        try:
            a=pp[0].strip('\\')
            timezone[j]=a
        except:
            timezone[j]=0
        #get the name of the store
        try:
            bb = BeautifulSoup(driver.page_source, 'html.parser')
            tt=bb.find("h1", {"class": "section-hero-header-title"}).text
        except:
            time.sleep(20)
            try:
                bb = BeautifulSoup(driver.page_source, 'html.parser')
                tt=bb.find("h1", {"class": "section-hero-header-title"}).text
            except:
                time.sleep(20)
                try:
                    bb = BeautifulSoup(driver.page_source, 'html.parser')
                    tt=bb.find("h1", {"class": "section-hero-header-title"}).text
                except:
                    pass
                    tt=0
        print ('xt '+str(tt))
        match[j]=tt
        tt=0
        #address
        try:
            addrs[j]=bb.find("div", {"class": "section-info-line"}).find("span", {"class": "widget-pane-link"}).text
        except:
            pass
        #get popular time            
        try:
            myindex=str(int(bb.find("div", {"class": "section-popular-times"}).find("div", {"class": "section-popular-times-container"}).get('jstcache'))+1)
            ss0_sunday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[0].find_all("div", {"class":"section-popular-times-bar"})]
            ss1_monday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[1].find_all("div", {"class":"section-popular-times-bar"})]
            ss2_tuesday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[2].find_all("div", {"class":"section-popular-times-bar"})]
            ss3_wednesday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[3].find_all("div", {"class":"section-popular-times-bar"})]
            ss4_thursday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[4].find_all("div", {"class":"section-popular-times-bar"})]
            ss5_friday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[5].find_all("div", {"class":"section-popular-times-bar"})]
            ss6_saturday=[p.get('aria-label') for p in bb.find_all("div", {"jstcache": myindex})[6].find_all("div", {"class":"section-popular-times-bar"})]
            s0=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss0_sunday]
            s1=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss1_monday]
            s2=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss2_tuesday]
            s3=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss3_wednesday]
            s4=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss4_thursday]
            s5=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss5_friday]
            s6=[p.strip('.').strip(' ').split('% busy at') if 'Currently' not in p else [p.split('busy, ')[1].replace('usually','').replace('busy','').replace('%','').strip(' ')]+[datetime.now().strftime('%I %p')] for p in ss6_saturday]
            mondaypop[j]=', '.join([p[0] for p in s1])
            mondaypt[j]=', '.join([p[1] for p in s1])
            tuesdaypop[j]=', '.join([p[0] for p in s2])
            tuesdaypt[j]=', '.join([p[1] for p in s2])
            wednesdaypop[j]=', '.join([p[0] for p in s3])
            wednesdaypt[j]=', '.join([p[1] for p in s3])
            thursdaypop[j]=', '.join([p[0] for p in s4])
            thursdaypt[j]=', '.join([p[1] for p in s4])
            fridaypop[j]=', '.join([p[0] for p in s5])
            fridaypt[j]=', '.join([p[1] for p in s5])
            saturdaypop[j]=', '.join([p[0] for p in s6])
            saturdaypt[j]=', '.join([p[1] for p in s6])
            sundaypop[j]=', '.join([p[0] for p in s0])
            sundaypt[j]=', '.join([p[1] for p in s0])
        except:
            pass        
            
        #get open/ closing time
        try:
            openclose=[p.get('aria-label') for p in bb.find_all("div", {"class": "section-open-hours-container"})][0].replace('. Hide open hours for the week','').split(',')
            if 'Open 24 hours' in openclose[0] or 'Open 24 hours' in openclose[1] or 'Open 24 hours' in openclose[2] or 'Open 24 hours' in openclose[3] or 'Open 24 hours' in openclose[4] or 'Open 24 hours' in openclose[5] or 'Open 24 hours' in openclose[6]:
                mondaystime[j]=' '.join(openclose[0].split(' ')[1:])
                mondayetime[j]=0
                tuesdaystime[j]=' '.join(openclose[1].split(' ')[1:])
                tuesdayetime[j]=0
                wednesdaystime[j]=' '.join(openclose[2].split(' ')[1:])
                wednesdayetime[j]=0
                thursdaystime[j]=' '.join(openclose[3].split(' ')[1:])
                thursdayetime[j]=0
                fridaystime[j]=' '.join(openclose[4].split(' ')[1:])
                fridayetime[j]=0
                saturdaystime[j]=' '.join(openclose[5].split(' ')[1:])
                saturdayetime[j]=0
                sundaystime[j]=' '.join(openclose[6].split(' ')[1:])
                sundayetime[j]=0
            else:
                oc=[re.findall(r"[\w:']+|[.,!?;]", p.split(' ')[1]) for p in openclose]
                if 'Closed' not in oc[0]:
                    mondaystime[j]=oc[0][0]
                    mondayetime[j]=oc[0][1]
                else:
                    mondaystime[j]=oc[0][0]
                    mondayetime[j]=0
                if 'Closed' not in oc[1]:
                    tuesdaystime[j]=oc[1][0]
                    tuesdayetime[j]=oc[1][1]
                else:
                    tuesdaystime[j]=oc[1][0]
                    tuesdayetime[j]=0
                if 'Closed' not in oc[2]:
                    wednesdaystime[j]=oc[2][0]
                    wednesdayetime[j]=oc[2][1]
                else:
                    wednesdaystime[j]=oc[2][0]
                    wednesdayetime[j]=0
                if 'Closed' not in oc[3]:
                    thursdaystime[j]=oc[3][0]
                    thursdayetime[j]=oc[3][1]
                else:
                    thursdaystime[j]=oc[3][0]
                    thursdayetime[j]=0
                if 'Closed' not in oc[4]:
                    fridaystime[j]=oc[4][0]
                    fridayetime[j]=oc[4][1]
                else:
                    fridaystime[j]=oc[4][0]
                    fridayetime[j]=0
                if 'Closed' not in oc[5]:
                    saturdaystime[j]=oc[5][0]
                    saturdayetime[j]=oc[5][1]
                else:
                    saturdaystime[j]=oc[5][0]
                    saturdayetime[j]=0
                if 'Closed' not in oc[6]:
                    sundaystime[j]=oc[6][0]
                    sundayetime[j]=oc[6][1]
                else:
                    sundaystime[j]=oc[6][0]
                    sundayetime[j]=0
        except:
            pass
        print ('Place '+str(j)+' '+str(match[j]))            
        time2=time.time()
        print ('time '+str(j)+' '+str(time2-time1))
        #save temporary files
        if j in range(0,len(dbb),100):
            dbb['timezone']=timezone
            dbb['spend']=spend
            dbb['mondaystime']=mondaystime
            dbb['mondayetime']=mondayetime
            dbb['tuesdaystime']=tuesdaystime
            dbb['tuesdayetime']=tuesdayetime
            dbb['wednesdaystime']=wednesdaystime
            dbb['wednesdayetime']=wednesdayetime
            dbb['thursdaystime']=thursdaystime
            dbb['thursdayetime']=thursdayetime
            dbb['fridaystime']=fridaystime
            dbb['fridayetime']=fridayetime
            dbb['saturdaystime']=saturdaystime
            dbb['saturdayetime']=saturdayetime
            dbb['sundaystime']=sundaystime
            dbb['sundayetime']=sundayetime
            dbb['mondaypop']=mondaypop
            dbb['tuesdaypop']=tuesdaypop
            dbb['wednesdaypop']=wednesdaypop
            dbb['thursdaypop']=thursdaypop
            dbb['fridaypop']=fridaypop
            dbb['saturdaypop']=saturdaypop
            dbb['sundaypop']=sundaypop
            dbb['mondaypt']=mondaypt
            dbb['tuesdaypt']=tuesdaypt
            dbb['wednesdaypt']=wednesdaypt
            dbb['thursdaypt']=thursdaypt
            dbb['fridaypt']=fridaypt
            dbb['saturdaypt']=saturdaypt
            dbb['sundaypt']=sundaypt
            dbb['match']=match
            dbb['address']=addrs
            dbb.to_csv('alcohol_temp.csv',index=False)
    dbb['timezone']=timezone
    dbb['spend']=spend
    dbb['mondaystime']=mondaystime
    dbb['mondayetime']=mondayetime
    dbb['tuesdaystime']=tuesdaystime
    dbb['tuesdayetime']=tuesdayetime
    dbb['wednesdaystime']=wednesdaystime
    dbb['wednesdayetime']=wednesdayetime
    dbb['thursdaystime']=thursdaystime
    dbb['thursdayetime']=thursdayetime
    dbb['fridaystime']=fridaystime
    dbb['fridayetime']=fridayetime
    dbb['saturdaystime']=saturdaystime
    dbb['saturdayetime']=saturdayetime
    dbb['sundaystime']=sundaystime
    dbb['sundayetime']=sundayetime
    dbb['mondaypop']=mondaypop
    dbb['tuesdaypop']=tuesdaypop
    dbb['wednesdaypop']=wednesdaypop
    dbb['thursdaypop']=thursdaypop
    dbb['fridaypop']=fridaypop
    dbb['saturdaypop']=saturdaypop
    dbb['sundaypop']=sundaypop
    dbb['mondaypt']=mondaypt
    dbb['tuesdaypt']=tuesdaypt
    dbb['wednesdaypt']=wednesdaypt
    dbb['thursdaypt']=thursdaypt
    dbb['fridaypt']=fridaypt
    dbb['saturdaypt']=saturdaypt
    dbb['sundaypt']=sundaypt
    dbb['match']=match
    dbb['address']=addrs
    return dbb



