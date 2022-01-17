print('bh_global_functions')
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from IPython.display import clear_output
import sys
class other_functions():
	def __init__(self):
		pass
	def print_menu(self,selection_list,return_type="text",sort=False):
		print('-entered print menu-')
		if sort==True:
			selection_list.sort(key=lambda y: y.lower())
		x=0
		print('---')
		print('type: '+str(type(selection_list)))
		print('---')

		if type(selection_list)==list:
			print('list found')
			timeout=0
			while True:
				x=0
				try:
					for item in selection_list:
						item=str(item)
						x+=1
						print (str(x)+".) "+str(selection_list[x-1]))
					choice=input('Choose: ')
					print(choice)
					choice=int(choice)-1
					break
				except Exception as e:
					timeout+=1
					print('Try again!')
					if timeout>19:
						print(e)
						return False
			if return_type=="text" or return_type==None:
				return selection_list[choice]
			elif return_type=="index":
				return choice
		elif type(selection_list)==dict:
			print('dict found')
			while True:
				x=0
				temp_list=[]
				for item in selection_list:
					temp_list.append(item)
				for item in temp_list:
					x+=1
					print(str(x)+".) "+temp_list[x-1])
				choice = input('Choose: ')
				choice=int(choice)-1
				break
			print('choice: '+str(choice))
			print('temp_list: '+str(temp_list))
			print('temp_list_indexed: '+str([temp_list[choice]]))
			print(selection_list[temp_list[choice]])

			key=temp_list[choice]
			print('key: '+str(key))
			pair=selection_list[key]
			print('pair: '+pair)
			print('return '+str(key))
			return(key)

	def dict_menu(self,selection_dict):
		dictionary_keys=selection_dict
		find_item=self.print_menu(dictionary_keys)
		print('selection dict: '+str(selection_dict))
		print('find item: '+str(find_item))
		return(find_item,selection_dict[find_item])
	def print_title(self,title,indent='',side_wall='----',buff='   '):
		butter=""
		total_length=10
		wall_width=len(side_wall)*2
		buff_width=len(buff)*2
		if type(title) == str:
			total_length=len(title)+wall_width+buff_width
			butter='\n'+indent+side_wall+buff+title+buff+side_wall+'\n'

		elif type(title==list):
			butter='\n'
			longest_string=max(title,key=len)
			max_length=len(longest_string)
			total_length=max_length+wall_width+buff_width
			top_entry=title[0]
			centralize=max_length-len(top_entry)
			centralize_buffer=centralize/2
			top_entry=' '*centralize_buffer+top_entry
			title[0]=top_entry 
			for item in title:
				butter+=indent+side_wall+buff
				trailing_spaces=max_length-len(item)
				butter+=str(item)+' '*trailing_spaces+buff+side_wall+'\n'
		else:
			try:
				total_length=len(str(title))
				butter=str(title)
			except:
				total_length=10
				butter='\nNULL\n'
		bread=indent+'-'*total_length
		sandwich=bread+butter+bread
		return sandwich
	def print_details(self,title,details,title_indent='',title_lr_border='-----',title_buff='   ',clear=True):
		#print self.#print_title(title,indent=title_indent,side_wall=title_lr_border,buff=title_buff)
		#print details.keys()
		for item in details.keys():
			if details[item]==None:
				details[item]=''
			if len(item)<4:
				menu_key=item+':	'
			else:
				menu_key=item+':'
			if len(menu_key)<9:
				menu_key=menu_key+'   '

			#print menu_key+"\t"+ details[item]
		
		#print '\n'
class selenium_driver:
	def __init__(self,driver):
		self.driver = driver
		self.counter=0
	def scroll_to(self,element,yoffset=0,xoffset=0):
		loco=element.location
		#print '---1---'
		#print loco
		x=str(int(element.location['x'])+xoffset)
		#print '---2---'
		#print x
		y=str(int(element.location['y'])+yoffset)
		#print 'window.scroll('+x+','+y+');'
		self.driver.execute_script('window.scroll('+x+','+y+');')
	def highlight(self,element,color="1px solid red"):
		self.driver.execute_script('arguments[0].style.outline="'+color+'";',element)
	def check(self,element):
		err_count=0
		while err_count<6:
			if element.is_selected():
				pass
			else:
				try:
					element.click()
				except:
					err_count+=1
					time.sleep(.5)
			try:
				if element.is_selected():
					return True
			except:
				return False
			else:
				print('element came up unselected despite all our best efforts...')		
				err_count+=1
				time.sleep(.5)
		return False					
	def check_if_yes(self,element,response):
		if response.lower()=='yes':
			self.check(element)
		else:
			self.uncheck(element)
	def uncheck(self,element):
		if element.is_selected():
			element.click()
		else:
			pass
	def accept_alert(self):
		try:
			WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
			'Timed out waiting for PA creation ' +
			'confirmation popup to appear.')
			self.alert = self.driver.switch_to_alert()
			self.alert.accept()
			#print "alert accepted"
		except TimeoutException:
			print("no alert")
	# def accept_alert(self):
	# 	print '1-accept_alert'
	# 	self.counter=0
	# 	print 'counter initialized'
	# 	while self.counter <5:
	# 		print 'inside while loop: '+str(self.counter)
	# 		try:
	# 			print "\tTry"
	# 			self.alert()
	# 			return True
	# 		except Exception as e:
	# 			print e
	# 			print '\texcept'
	# 			time.sleep(.4)
	# 			self.counter+=1
	# 		break
	def nav_navigator(self,item,search_term):
		span = self.driver.find_element_by_id(item)
		elements = span.find_elements_by_css_selector('li')
		nav_items=[]
		for x in range(0,len(elements)):
			#print str(x)+elements[x].text
			nav_items.append(elements[x].text.rstrip())
		if search_term in nav_items:
			return self.driver.find_element_by_link_text(search_term+" ")
		else:
			return False


