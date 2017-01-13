#import urllib2 
import re
#from urllib import FancyURLopener
import httplib2
import calendar
import pandas as pd
import time

time1=time.time()
alltable_comet=pd.DataFrame({})
alltable_ongoing=pd.DataFrame({})
alltable_academic=pd.DataFrame({})

#outer pages
years=range(2011,2018)
months=range(1,13)
days=[]
table1_comet1=pd.DataFrame({})
table1_ongoing1=pd.DataFrame({})
table1_academic1=pd.DataFrame({})
for i in years:
	for j in months:
		d1=calendar.monthrange(i,j)
		for k in range(1,d1[1]+1):
			table1_comet=pd.DataFrame({})
			table1_ongoing=pd.DataFrame({})
			table1_academic=pd.DataFrame({})
			#print i, j, k
			#print '                    '
			#print '###### Comet Calandar ######'
			http = httplib2.Http()
			status, response = http.request('http://www.utdallas.edu/calendar/getEvents.php?month='+str(j)+'&year=+'+str(i)+'+&type=day'+str(k))
			#print response
			
			##########comet calandar: events and time##########
			regex_e1="<div class='events-name'>(.+?)</a>"
			pattern_e1 = re.compile(regex_e1)
			event1 = re.findall(pattern_e1,response)
			events1=[]
			for m in range(len(event1)):
				events1.append(event1[m][event1[m].rfind('>')+1:])
			#events1=''.join(events1)
			#print events1
			table1_comet['events']=events1
			table1_comet['year']=i
			table1_comet['month']=j
			table1_comet['date']=k
			
			regex_t1="<span class='events-time'>(.+?)</span>"
			pattern_t1 = re.compile(regex_t1)
			eventtime1 = re.findall(pattern_t1,response)
			regex_t2="<div class='events-time'>(.+?)</div>"
			pattern_t2 = re.compile(regex_t2)
			time2 = re.findall(pattern_t2,response)
			eventtime1.extend(time2)
			#eventtime1=''.join(eventtime1)
			#print eventtime1
			starttime=[]
			endtime=[]
			for m in eventtime1:
				if len(m.split(' - ')) == 0:
					starttime.append(0)
					endtime.append(0)
				if len(m.split(' - ')) == 1:
					starttime.append(m.split(' - ')[0])
					endtime.append(0)
				else:
					starttime.append(m.split(' - ')[0])
					endtime.append(m.split(' - ')[1])
			
			table1_comet['starttime']=starttime
			table1_comet['endtime']=endtime
			
			#comet calandar: locations
			regex_p="<a class='eventTitle' href='(.+?)' id='"
			pattern_p = re.compile(regex_p)
			phpsite = re.findall(pattern_p,response)
			locations=[]
			for m in phpsite:
				status, response_loc = http.request('http://www.utdallas.edu/calendar/'+str(m))
			
				regex_loc="<span class='fn org'>(.+?)</span>"
				pattern_loc = re.compile(regex_loc)
				locations.append(''.join(re.findall(pattern_loc,response_loc)))
				#locations = ''.join(locations)
			#print locations
			table1_comet['location']=locations

			##########ongoing events##########
			#print '                    '
			#print '###### Ongoing Events ######'
			regex_goingevent='<div class="events-name">(.+?)</a>'
			pattern_goingevent = re.compile(regex_goingevent)
			goingevent = re.findall(pattern_goingevent,response)
			goingevent1=[]
			for m in range(len(goingevent)):
				goingevent1.append(goingevent[m][goingevent[m].rfind('>')+1:])
			#events1=''.join(events1)
			#print goingevent1
			table1_ongoing['event']=goingevent1
			table1_ongoing['year']=i

			regex_goingtime='<div class="events-time">(.+?)</div>'
			pattern_goingtime = re.compile(regex_goingtime)
			goingtime = re.findall(pattern_goingtime,response)
			#print goingtime
			startdate_o=[]
			enddate_o=[]
			for m in goingtime:
				if len(m.split(' - ')) == 0:
					startdate_o.append(0)
					enddate_o.append(0)
				elif len(m.split(' - ')) == 1:
					startdate_o.append(m.split(' - ')[0])
					enddate_o.append(0)
				else:
					startdate_o.append(m.split(' - ')[0])
					enddate_o.append(m.split(' - ')[1])
			
			table1_ongoing['startdate']=startdate_o
			table1_ongoing['enddate']=enddate_o

			##########academic calandar##########
			#print '                    '
			#print '###### Academic Calandar ######'
			regex_acadevent='<li id="details-copy">(.+?) \n                \t\n                                    </li>'
			pattern_acadevent = re.compile(regex_acadevent)
			acadevent = re.findall(pattern_acadevent,response)
			#print acadevent
			table1_academic['event']=acadevent
			table1_academic['year']=i

			regex_acadtime1="<span class='startMonth'>(.+?)</span></span></li>"
			pattern_acadtime1 = re.compile(regex_acadtime1)
			acadtime1 = re.findall(pattern_acadtime1,response)
			acadtime=[]
			for m in acadtime1:
				acadtime1=m.replace("</span><span class='startMonth'>","").replace("</span><span class='startDay'>","").replace("</span></span>","").replace("<span class='ccDash'>","").replace("</span> <span class='stopDate'><span class='day-of-week'>"," ").replace("</span><span class='stopMonth'>","").replace("</span><span class='stopDay'>","").replace(",","").replace("Monday ","").replace("Tuesday ","").replace("Wednesday ","").replace("Thursday ","").replace("Friday ","").replace("Saturday ","").replace("Sunday ","").replace("</span><span class='startYear'>","").replace("</span><span class='stopYear'>","").replace(" 2012","").replace(" 2013","").replace(" 2014","").replace(" 2015","").replace(" 2016","").replace(" 2017","").replace(" 2018","").replace("</span> <span class='stopDate'><span class='stopMonth'>","")
				acadtime.append(acadtime1)
			#print acadtime
			startdate_a=[]
			enddate_a=[]
			for m in acadtime:
				if len(m.split(' - ')) == 0:
					startdate_a.append(0)
					enddate_a.append(0)
				elif len(m.split(' - ')) == 1:
					startdate_a.append(m.split(' - ')[0])
					enddate_a.append(0)
				else:
					startdate_a.append(m.split(' - ')[0])
					enddate_a.append(m.split(' - ')[1])
			
			if startdate_a != []:
				table1_academic['startdate']=startdate_a
				table1_academic['enddate']=enddate_a

			#print '                    '
			#print '                    '
			#print '                    '
			#print '                    '
			#print '                    '
			if len(table1_comet)!=0:
				table1_comet1=table1_comet1.append(table1_comet)
			#print table1_comet1
			if len(table1_ongoing)!=0:
				table1_ongoing1=table1_ongoing1.append(table1_ongoing)
			if len(table1_academic)!=0:
				table1_academic1=table1_academic1.append(table1_academic)

	time2=time.time()
	print time2-time1   

table1_comet1.to_csv('cometcalandar.csv', index=False)
table1_ongoing1=table1_ongoing1.drop_duplicates()
table1_ongoing1.to_csv('ongoingevents.csv', index=False)
table1_academic1=table1_academic1.drop_duplicates()
table1_academic1.to_csv('academiccalandar.csv', index=False)



