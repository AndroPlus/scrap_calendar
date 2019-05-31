from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tamil.txt2unicode import *
import re
import json
from datetime import datetime
from datetime import timedelta
import calendar
# create a new Firefox session
#cap = DesiredCapabilities().FIREFOX
#cap["marionette"] = False
class MyTest(object):
	
	def __init__(self):
		self.storeUrl = []
		self.storeName = []
		self.newDate = datetime(2019, 1, 1, 0, 0)

		self.currentMonth = 1		
		self.currentMonthText = "Jan"
		self.currentDay = 1
		self.currentYear = 2019
		self.calendarData = {}
		self.monthJsonArray = []

		options = Options()
		options.add_argument("--headless")
		self.driver = webdriver.Firefox(firefox_options=options, executable_path='D:\Ram\geckodriver.exe')

	def	getYearDetails(self):

		if(self.currentYear == 2020 and self.currentMonth == 1 and self.currentDay == 1):
			exit	
		else:
			last_day_of_month = calendar.monthrange(self.currentYear, self.currentMonth)
			last_day = last_day_of_month[1]
			#print(str(last_day) +" "+str(self.currentDay))
			if(self.currentDay == last_day and len(self.monthJsonArray)>0):
				with open(str(self.currentMonth - 1)+'.json', 'w') as outfile:
					json.dump(self.monthJsonArray, outfile)
					self.monthJsonArray = []

			self.newDate = self.newDate + timedelta(days=1)		
			self.currentMonth = self.newDate.month
			self.currentDay = self.newDate.day
			self.currentYear = self.newDate.year
			self.currentMonthText = self.newDate.strftime("%b")
			self.getParentUrls()
			

		#while (self.currentMonth <= 12 and self.currentDay <=31):						
		#	print(str(self.newDate.month) +" "+str(self.newDate.day) + " "+ str(self.newDate.year))
		#	self.newDate = self.newDate + timedelta(days=1)			
		#	self.currentMonthText = self.newDate.strftime("%b")
		#	self.currentMonth = self.newDate.month
		#	self.currentDay = self.newDate.day
		#	if(self.currentMonth == 12 and self.currentDay ==31):
		#		break

	def getParentUrls(self):	
		url = "https://www.dinamalar.com/dailysheetcalendar.asp?year="+str(self.currentYear)+"&month="+str(self.currentMonthText)+"&date="+str(self.currentDay)
		print("Url -->"+url)
		self.driver.get(url)
		self.driver.implicitly_wait(5)
		#self.driver.maximize_window()
		calendarAreaHtml = self.driver.find_element_by_class_name("calmiddle")
		# get the number of elements found
		#print ("Found " + calendarAreaHtml.get_attribute('innerHTML'))
		
		self.calendarData = {}		

		self.calendarData['ghi'] = ""
		self.calendarData['gh'] = ""
		self.calendarData['ti'] = ""
		self.calendarData['d'] = self.currentDay
		self.calendarData['ts'] = ""
		self.calendarData['mdy'] = ""
		self.calendarData['mdt'] = ""
		self.calendarData['gh'] = ""

		#print(calendarAreaHtml.find_element_by_class_name("eng").find_element_by_class_name("month").get_attribute('innerHTML'))
		#spl day
		
		splObj  = re.search(r'<div class=\"splday\">([^>]+)<\/div>', calendarAreaHtml.get_attribute('innerHTML'),re.M|re.I)
		if splObj:
			self.calendarData['spl'] = unicode2bamini(splObj.group(1))
		else:
			self.calendarData['spl'] = ""
			print ("not found")					
		
		#eng month 
		self.calendarData['m'] = unicode2bamini(calendarAreaHtml.find_element_by_class_name("eng").find_element_by_class_name("month").get_attribute('innerHTML'))

		#tamil month - year
		#print(calendarAreaHtml.find_element_by_class_name("tamil").find_element_by_class_name("month").get_attribute('innerHTML'))
		tamil_month_year = calendarAreaHtml.find_element_by_class_name("tamil").find_element_by_class_name("month").get_attribute('innerHTML')
		tamArray = tamil_month_year.split("-")
		self.calendarData['ty'] = unicode2bamini(tamArray[0])
		self.calendarData['tm'] = unicode2bamini(tamArray[1])
		
		#tamil date
		#print(calendarAreaHtml.find_element_by_class_name("tamil").find_element_by_class_name("tamildate").get_attribute('innerHTML'))
		self.calendarData['td'] = unicode2bamini(calendarAreaHtml.find_element_by_class_name("tamil").find_element_by_class_name("tamildate").get_attribute('innerHTML'))
		#print(calendarAreaHtml.find_elements_by_class_name("runningrasi")[0].get_attribute('innerHTML'))
		

		
		nallaNerum = calendarAreaHtml.find_elements_by_class_name("runningrasi")[0]
		#print(nallaNerum.get_attribute('innerHTML'))

		searchObj  = re.search(r'<tr>\s*<td[^>]+>([^>]+)<\/td>\s*<td[^>]+>:<\/td>\s*<td[^>]+>([^>]+)<\/td>\s*<td[^>]+>([^>]+)<\/td>\s*<td[^>]+>:<\/td>\s*<td[^>]+>([^>]+)<\/td>\s*<td[^>]+>([^>]+)<\/td>\s*<td[^>]+>:<\/td>\s*<td[^>]+>([^>]+)<\/td>\s*<\/tr>\s*<tr>\s*<td>([^>]+)<\/td>\s*<td[^>]*>:<\/td>\s*<td[^>]+>([^>]+)<\/td>', nallaNerum.get_attribute('innerHTML'),re.M|re.I)
		#
		if searchObj:
			print ("NNText", searchObj.group(1))			
			print ("NNTime", searchObj.group(2))
			self.calendarData['NN'] = searchObj.group(2)

			print ("RagText", searchObj.group(3))
			print ("RagTime", searchObj.group(4))
			self.calendarData['rg'] = searchObj.group(4)

			print ("KuliText", searchObj.group(5))
			print ("KuliTime", searchObj.group(6))
			self.calendarData['kl'] = searchObj.group(6)

			print ("YemaText", searchObj.group(7))
			print ("YemaTime", searchObj.group(8))
			self.calendarData['em'] = searchObj.group(8)
		else:
			print ("not found")

		Rasi2 = calendarAreaHtml.find_elements_by_class_name("runningrasi")[1].get_attribute('innerHTML')

		searchRasi2Obj  = re.search(r'<tr>\s*<td[^>]+>([^>]+)<\/td>\s*<td[^>]+>:<\/td>\s*<td[^>]+>([^>]+)<\/td>\s*<td[^>]+>[^>]+<\/td>\s*<td[^>]+>[^>]+<\/td>\s*<\/tr>\s*<tr>\s*<td>([^>]+)<\/td>\s*<td[^>]*>:<\/td>\s*<td>([^>]+)<\/td>\s*<td>([^>]+)<\/td>\s*<td>([^>]+)<\/td>\s*<\/tr>\s*<tr>\s*<td>([^>]+)<\/td>\s*<td[^>]*>:<\/td>\s*<td>([^>]+)<\/td>\s*<td>([^>]+)<\/td>\s*<td>([^>]+)<\/td>\s*<\/tr>', Rasi2 ,re.M|re.I)

		if searchRasi2Obj:
			print ("Titi", searchRasi2Obj.group(1))
			print ("titiText", searchRasi2Obj.group(2))

			print ("titi time", searchRasi2Obj.group(3))
			print ("titi 4", searchRasi2Obj.group(4))
			print ("titi 4", searchRasi2Obj.group(5))
			print ("titi 4", searchRasi2Obj.group(6))
			self.calendarData['tt'] = unicode2bamini(searchRasi2Obj.group(2))
			self.calendarData['ttn'] = unicode2bamini(searchRasi2Obj.group(3) +" "+searchRasi2Obj.group(4)+" "+searchRasi2Obj.group(5)+" "+searchRasi2Obj.group(6))


			print ("natcha", searchRasi2Obj.group(7))
			print ("natcha", searchRasi2Obj.group(8))
			print ("natcha", searchRasi2Obj.group(9))
			print ("natcha", searchRasi2Obj.group(10))
			self.calendarData['nat'] = unicode2bamini(searchRasi2Obj.group(7) +" "+searchRasi2Obj.group(8)+" "+searchRasi2Obj.group(9)+" "+searchRasi2Obj.group(10))

		Rasi3 = calendarAreaHtml.find_elements_by_class_name("runningrasi")[2].get_attribute('innerHTML')

		searchRasi3Obj  = re.search(r'<tr>\s*<td[^>]*>([^>]+)<\/td>\s*<td[^>]*>:<\/td>\s*<td[^>]*>([^>]+)<\/td>\s*<\/tr>\s*<tr>\s*<td[^>]*>([^>]+)<\/td>\s*<td[^>]*>:<\/td>\s*<td[^>]*>([^>]+)<\/td>\s*<\/tr>\s*<tr>\s*<td[^>]*>([^>]+)<\/td>\s*<td[^>]*>:<\/td>\s*<td[^>]*>([^>]+)<\/td>\s*<\/tr>\s*<tr>\s*<td[^>]*>([^>]+)<\/td>\s*<td[^>]*>:<\/td>\s*<td[^>]*>([^>]+)<\/td>\s*<\/tr>', Rasi3 ,re.M|re.I)

		if searchRasi3Obj:
			print ("Yogam", searchRasi3Obj.group(1))
			print ("YogamText", searchRasi3Obj.group(2))
			self.calendarData['yg'] = unicode2bamini(searchRasi3Obj.group(2))

			print ("chandirastam", searchRasi3Obj.group(3))
			print ("chandirastamText", searchRasi3Obj.group(4))
			self.calendarData['cnd'] = unicode2bamini(searchRasi3Obj.group(4))

			print ("soolam", searchRasi3Obj.group(5))
			print ("SoolamText", searchRasi3Obj.group(6))
			self.calendarData['slm'] = unicode2bamini(searchRasi3Obj.group(6))

			print ("Parigaram", searchRasi3Obj.group(7))
			print ("ParigaramText", searchRasi3Obj.group(8))
			self.calendarData['phm'] = unicode2bamini(searchRasi3Obj.group(8))	

		self.monthJsonArray.append(self.calendarData)		
		self.getYearDetails()

		
	def getImageUrls(self):		
		for storeurl in self.storeUrl:
			self.driver.get(storeurl+"/menu")
			self.driver.implicitly_wait(10)
			menuHTMLBody = self.driver.find_element_by_tag_name("body")	
			menuImageUrls  = re.findall(r'\"url\":\"([^\"]+)\"', menuHTMLBody.get_attribute('innerHTML'),re.M|re.I)
			print (menuImageUrls)
			for menuImageUrl in menuImageUrls:
				print ("menuImageUrl--"+menuImageUrl)

	
	def browserQuit(self):		
		# close the browser window
		self.driver.quit()
	


test =  MyTest()
test.getParentUrls()
#test.getImageUrls()
#test.getYearDetails()
test.browserQuit()		

