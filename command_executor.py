from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import bh_global_functions
import os
import numpy
import sys
from IPython.display import clear_output


class actor:
	def __init__(self, repo_loc,dataloc,driver):
		self.function_runner=bh_global_functions.other_functions()
		self.driver=driver
		self.selenoid=bh_global_functions.selenium_driver(self.driver)
		if repo_loc.endswith('repository.npy'):
			repo_loc=repo_loc.split('/repository.npy')[0]
		self.repo_loc=repo_loc
		self.dataloc=dataloc
		self.data=numpy.load(dataloc, allow_pickle=True).all()	
		self.repo=numpy.load(self.repo_loc+'/repository.npy',allow_pickle=True).all()
	def elements(self):
		elements_list=self.repo[self.current_page].keys()
		elements_list.sort()
		return_list=elements_list
		return_list.sort()
		return return_list
	def accept_alert(self):
		try:
			WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
			'Timed out waiting for PA creation ' +
			'confirmation popup to appear.')
			self.alert = self.driver.switch_to_alert()
			self.alert.accept()
			print ("alert accepted")
		except TimeoutException:
			print ("no alert")
	def conditional_fill(self,element,data_val):
		try:
			el_type=element.get_attribute('type')
			if 'text' in el_type:
				element.clear()
				element.send_keys(data_val)
			elif 'select' in el_type:
				Select(element).select_by_visible_text(data_val)
			elif el_type == 'checkbox':
				if data_val=='checked':
					self.selenoid.check(element)
				elif data_val=='unchecked':
					self.selenoid.uncheck(element)
			return True
		except:
			print ('could not do')
			return False
	def dynamic_find(self,box_name,field_name,row_number):
		prefix=self.repo[self.current_page][box_name]['prefix']
		ending=self.repo[self.current_page][box_name]['fields'][field_name]
		id_string=prefix+':'+str(row_number)+':'+ending
		element=self.driver.find_element_by_id(id_string)
		return element
	def list_dynamic_elements(self):
		dynamic_items=[]
		repo_items=self.repo[self.current_page]
		for item in repo_items:
			if 'dynamic' in self.repo[self.current_page][item]:
				dynamic_items.append(item)
		chosen_set=self.function_runner.print_menu(dynamic_items)
		termo=self.function_runner.print_menu(repo_items[chosen_set]['fields'].keys())
		print ("To reference this value in a script use the dynamic_find function:\nactor.dynamic_find('"+chosen_set+"','"+termo+"',0)")

	def data_fill(self,element,dv):
		self.selenoid.scroll_to(element)
		el_type=str(element.get_attribute('type'))
		if not el_type:
			pass
			#start data_fill prompt
		elif 'text' in el_type.lower():
			element.clear()
			element.send_keys(dv)
		elif 'select' in el_type.lower():
			select=Select(element)
			select.select_by_visible_text(dv)
		elif el_type=='checkbox':
			if dv=='checked':
				self.selenoid.check(element)
			if dv=='unchecked':
				self.selenoid.uncheck(element)
		else:
			pass
	def click_and_load_next_page(self,term,wait_time=10,alert=False):
		button=self.find(term)
		wait = WebDriverWait(self.driver,wait_time)
		button.click()
		if alert==True:
			self.accept_alert()
		try:
			wait.until(EC.staleness_of(button))
		except Exception as e:
			print (e)
	def find(self,term,offset=250,wait=10):
		element_dict=self.repo[self.current_page][term]
		identistring=element_dict['properties']
		primary_id=element_dict['Primary identifier']
		if primary_id=='link_text':
			element = WebDriverWait(self.driver, wait).until(
		        EC.presence_of_element_located((By.LINK_TEXT, identistring['element text']))
    			)		
		elif primary_id=='partial_link_text':
			element = WebDriverWait(self.driver, wait).until(
		        EC.presence_of_element_located((By.CSS_SELECTOR, identistring['element text']))
    			)		
		elif primary_id=='css_selector':
			element = WebDriverWait(self.driver, wait).until(
		        EC.presence_of_element_located((By.CSS_SELECTOR, identistring['css_selector']))
    			)
		elif primary_id=='xpath':
			element = WebDriverWait(self.driver, wait).until(
		        EC.presence_of_element_located((By.XPATH, identistring['xpath']))
    			)
		else:
			print ('primary_id: '+primary_id)
			identifier='['+primary_id+'="'+identistring[primary_id]+'"]'
			print ('identifier: '+identifier)
			element = WebDriverWait(self.driver, wait).until(
		        EC.presence_of_element_located((By.CSS_SELECTOR, identifier))
    			)

		self.selenoid.scroll_to(element, offset)
		return element
		# except NoSuchElementException:
		# 	print 'Could not find the element '+term+' in the current browser'
		# 	return False
		# except Exception as e:
		# 	print 'Something went wrong\n'
		# 	print repr(e)
		# 	return e
	def fetch(self,term):
		try:
			page_data=self.data[self.current_page]
			return page_data[term]
		except:
			return ''
	def list_subgroups(self):
		sglist=[]
		page=self.repo[self.current_page]
		for item in page:
		    if page[item]['subgroup'] not in sglist:
		        sglist.append(page[item]['subgroup'])
		        print (page[item]['subgroup'])
	def pages(self):
		page_list=self.repo.keys()
		page_list.sort()
		return page_list
	def refresh_library(self):
		self.data=numpy.load(self.dataloc).all()
		self.repo=numpy.load(self.repo_loc+'/repository.npy').all()
	def set_page(self,page):
		self.current_page=page
		try:
			for item in self.data[page]:
				print (item)
		except:
			print ('Repo loaded...no entry found in datafile for: '+page)
		print ('Current page= '+page)
	def subgroup_query(self,subgroup):
		sglist=[]
		page=self.repo[self.current_page]
		for item in page:
		    if page[item]['subgroup']==subgroup:
		    	dataval=self.data[self.current_page][item]
		    	print (item+': '+dataval)

#	def multipage_member_datafill(self,member)
