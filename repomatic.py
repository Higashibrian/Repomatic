import numpy
import bh_global_functions
from selenium.webdriver.support.ui import Select
import os, sys, time



from selenium import webdriver
# class repomatic:
# 	def __init__(self,driver,project=None,environment=None):
# 		if a is None and b is None:
# 			#start menu
# 		else if 

# 	def find_by_id(id):

class page:
	def __init__(self,environment,project,projects_directory="S:/QA/Projects"):
		self.project_list=[]
		self.projects_directory=projects_directory
		self.environment=environment
		self.project=project
#		self.page
		self.page_directory=projects_directory+'/'+project+'/or/'+environment

	def load_page(self,page_name,extension='.npy'):
		self.page_location=self.page_directory+'/'+page_name+extension
		try:
			self.object_dictionary=numpy.load(self.page_location).all()
			return self.object_dictionary
		except:
			print("error loading dictionary from: \n"+self.page_location)
			print('\n Does the file exist?')
	def list_variable_names(self):
		for item in self.object_dictionary:
			print(item)
	def check_object_dictionary(self):
		for item in self.object_dictionary:
			try:
				exec(self.object_dictionary[item])
			except:
				print("-----Error with "+item+"-----\n: "+self.object_dictionary[item])
	def save_page(self):
		numpy.save(self.page_location,self.object_dictionary)

	def update(self,update_dict):
		self.object_dictionary.update(update_dict)
	def load_object(self,object):
		exec(object+" = "+self.object_dictionary[object])
	def list_all_objects(self):
		for item in self.object_dictionary:
			print(item+"\t:\t"+self.object_dictionary[item])
		def set_set(self):
			exec('hello="goodbye"')
class repomatic:
	def __init__(self):
		pass
		self.page=None                                                                                     
		self.function_runner=bh_global_functions.other_functions()

#	def delete_object(self):

	def load_repo(self,project_location='S:/QA/Projects'):
		project_names=[]
		for folder in os.listdir(project_location):
			if '.' in folder:
				pass
			else:
				project_names.append(folder)
		project_names.append('---new---')
		print('Select project: ')
		project=self.function_runner.print_menu(project_names)
		if project=='---new---':
			new_project=input('Name the new project:\n')
			try:
				os.mkdir(project_location+'/'+new_project)
			except:
				pass
			try:
				os.mkdir(project_location+'/'+new_project+'/or')
			except:
				print('try again')
				return False
			project=new_project
		try:
			os.mkdir(project_location+'/'+project)
		except:
			pass
		try:
			os.mkdir(project_location+'/'+project+'/or')
		except:
			pass
		print('Select environment: ')
		or_location=project_location+'/'+project+'/or'
		env=[]
		for envio in os.listdir(or_location):
			if '.' in envio:
				pass
			else:
				env.append(envio)
		env.append('---new---')
		environment=self.function_runner.print_menu(env)
		if environment == '---new---':
			environment=input('Name the new environment:\n')
			try:
				os.mkdir(or_location+'/'+environment)
			except:
				print('try again!')
				return False
		self.env_location=or_location+'/'+environment
		print('Select page')
		pagelist=[]
		for item in os.listdir(self.env_location):
			if '.npy' in item:
				pagelist.append(item.split('.npy')[0])
			else:
				pass
		pagelist.append('---new---')
		thepage=self.function_runner.print_menu(pagelist)
		if thepage=='---new---':
			thepage=input('Name the new page:\n')
			print(self.env_location+'/'+thepage)
			object_dictionary={}
#			thepage=thepage+'.npy'
			numpy.save(self.env_location+'/'+thepage,{})
#			try:
#				os.mkdir(self.env_location+'/'+thepage)
#			except:
#				print('try again!')
#				return False
#		thepage=thepage+'.npy'
		print(thepage)
		self.project_location=self.env_location+'/'+thepage
		self.page=page(environment,project)
		self.page.load_page(thepage)
		print(self.project_location)
		print(thepage)
	#def print_repo(self):

	def iterate_objects(self,driver):
		for item in self.page.object_dictionary:
			time.sleep(1)
			print(self.page.object_dictionary[item])
			try:
				exec(self.page.object_dictionary[item])
			except Exception as e:
				print(e)
				print(e.message, e.args)
				print('\n'*3)
				print(item+' not found!\nupdate the dictionary?')
				print(self.page.object_dictionary[item])
				response = input('y/n')
				if response.lower() == 'y':
					print(item)
					select_select=input('select?')
					if select_select.lower()=='n':
						self.add_element(item)
					else:
						self.add_select(item)
				else:
					pass
	def iterate_inputs(self,driver):
			self.driver = driver
			input_list=[]
			element_list=[]
			x=0
			for item in driver.find_elements_by_css_selector('input'):
	#			input_list.append(item)
				x+=1
				input_string=str(x)+'.)-------------------------------\n'
				input_string+="type: "+item.get_attribute('type')
				input_string+="id: "+item.get_attribute('id')
				input_string+= "\nname: "+item.get_attribute('name')
				input_string+="\nlist_number: "+str(x)+"\n"
				input_list.append(input_string)
				element_list.append(item)
			
			for x in range(0,len(element_list)):
				def iteration(x):
					index=x
					element=element_list[int(index)]
					element_id=element.get_attribute('id')
					element_name=element.get_attribute('name')
					if element_id!='':
						print(element.get_attribute('id'))
						driver.execute_script('document.getElementById("'+element_id+'").style.backgroundColor = "#FDFF47";')
						print(element.get_attribute('type'))
						update=""
						update=input('Update the repo? Y/N:')
						if update.lower() =='y':
							update_name=input("Enter the object name")
							if update_name !="":
								name_pair="global "+update_name+"; "+update_name+" =driver.find_element_by_id('"+element_id+"')"
								verify=""
								verify=input('verify:\n'+name_pair+'\nIs this correct?(y/n)')
								if verify.lower()=='y':
									self.page.update({update_name:name_pair})
									self.page.save_page()
								else:
									iteration(x)
						else:
							pass
						driver.execute_script('document.getElementById("'+element_id+'").style.backgroundColor = "";')
					elif element_name!='':
						print(element.get_attribute('name'))
						print(element.get_attribute('type'))
						print("Name: "+element_name)
						driver.execute_script('document.getElementsByName("'+element_name+'")[0].style.backgroundColor = "#FDFF47";')
						update=""
						update=input('Update the repo? Y/N:')
						print("update lower = "+update.lower())
						if update.lower()=='y':
							update_name=input("Enter the object name")
							if update_name !="":
								name_pair=update_name+" =driver.find_element_by_name('"+element_name+"')"
								verify=""
								verify=input('verify:\n'+name_pair+'\nIs this correct?(y/n)')
								if verify.lower()=='y':
									self.page.update({update_name:name_pair})
									self.page.save_page()
								else:
									iteration(x)
									pass
						driver.execute_script('document.getElementsByName("'+element_name+'")[0].style.backgroundColor = "";')
				iteration(x)
	def list_inputs(self,driver):
		self.driver = driver
		input_list=[]
		element_list=[]
		x=0
		for item in driver.find_elements_by_css_selector('input'):
#			input_list.append(item)
			x+=1
			input_string=str(x)+'.)-------------------------------\n'
			input_string+="type: "+item.get_attribute('type')
			input_string+="id: "+item.get_attribute('id')
			input_string+= "\nname: "+item.get_attribute('name')
			input_string+="\nlist_number: "+str(x)+"\n"
			input_list.append(input_string)
			element_list.append(item)
		print(element_list)
		print(('Select an element to highlight'))
		index=self.function_runner.print_menu(input_list,return_type="index")
		print(index)
		element=element_list[int(index)]
		element_id=element.get_attribute('id')
		print(type(element_id))
		element_name=element.get_attribute('name')
		if element_id!='':
			driver.execute_script('document.getElementById("'+element_id+'").style.backgroundColor = "#FDFF47";')
			update=""
			print('id: '+element_id)
			update=input('Update the repo? Y/N:')
			if update.lower() =='y':
				print("ID: "+element_id)
				update_name=input("Enter the object name")
				if update_name !="":
					name_pair="global "+update_name+"; "+update_name+" =driver.find_element_by_id('"+element_id+"')"
					verify=""
					verify=input('verify:\n'+name_pair+'\nIs this correct?(y/n)')
					if verify.lower()=='y':
						self.page.update({update_name:name_pair})
						self.page.save_page()
					else:
						pass
			else:
				pass
			driver.execute_script('document.getElementById("'+element_id+'").style.backgroundColor = "";')
		elif element_name!='':
			driver.execute_script('document.getElementsByName("'+element_name+'")[0].style.backgroundColor = "#FDFF47";')
			print("Name: "+element_name)
			update=""
			update=input('Update the repo? Y/N:')
			print("update lower = "+update.lower())
			if update.lower()=='y':
				update_name=input("Enter the object name")
				if update_name !="":
					name_pair=update_name+" =driver.find_element_by_name('"+element_name+"')"
					verify=""
					verify=input('verify:\n'+name_pair+'\nIs this correct?(y/n)')
					if verify.lower()=='y':
						self.page.update({update_name:name_pair})
						self.page.save_page()
					else:
						pass
			response=input("Press Enter when loaded")
			driver.execute_script('document.getElementsByName("'+element_name+'")[0].style.backgroundColor = "";')

	def list_selects(self,driver):
		self.driver = driver
		input_list=[]
		element_list=[]
		x=0
		for item in driver.find_elements_by_css_selector('select'):
#			input_list.append(item)
			x+=1
			input_string=str(x)+'.)-------------------------------\n'
			input_string+="type: "+item.get_attribute('type')
			input_string+="\nid: "+item.get_attribute('id')
			input_string+= "\nname: "+item.get_attribute('name')
			input_string+="\nlist_number: "+str(x)+"\n"
			input_list.append(input_string)
			element_list.append(item)
		print('Select an element to highlight')
		index=self.function_runner.print_menu(input_list,return_type="index")
		element=element_list[index]
		element_id=element.get_attribute('id')		
		element_name=element.get_attribute('name')
		if element_id!=None:
			driver.execute_script('document.getElementById("'+element_id+'").style.backgroundColor = "#FDFF47";')
			update=""
			update=input('Update the repo? Y/N:')
			if update.lower()=='y':
				update_name=input("Enter the object name")
				if update_name !="":
					name_pair="global "+update_name+"; "+update_name+" =Select(driver.find_element_by_id('"+element_id+"'))"
					verify=""
					verify=input('verify:\n'+name_pair+'\nIs this correct?(y/n)')
					if verify.lower()=='y':
						self.page.update({update_name:name_pair})
						self.page.save_page()
				else:
					pass
			else:
				pass
			driver.execute_script('document.getElementById("'+element_id+'").style.backgroundColor = "";')
		elif element_name!=None:
			driver.execute_script('document.getElementsByName("'+element_name+'")[0].style.backgroundColor = "#FDFF47";')
			update=""
			update=input('Update the repo? Y/N:')
			if update.lower()=='y':
				update_name=input("Enter the object name")
				if update_name !="":
					name_pair=update_name+" =Select(driver.find_element_by_name('"+element_name+"'))"
					verify=""
					verify=input('verify:\n'+name_pair+'\nIs this correct?(y/n)')
					if verify.lower()=='y':
						self.page.update({update_name:name_pair})
						self.page.save_page()

			response=input("Press Enter when loaded")
			driver.execute_script('document.getElementsByName("'+element_id+'")[0].style.backgroundColor = "";')
	def remove_item(self):
		item_list=[]
		for item in self.page.object_dictionary.keys():
			item_list.append(item)
			item_list.sort()
		item_for_removal=self.function_runner.print_menu(item_list)
		check=input('delete: '+item_for_removal+'?\ny/n\n')
		if check.lower()=='y':
			del(self.page.object_dictionary[item_for_removal])
			self.page.save_page()
		else:
			pass




	def add_element(self,element_name):
		identifier_list=['id','name','css_selector','link_text','partial_link_text','declared_string','---other---']
		chosen_identifier=self.function_runner.print_menu(identifier_list)
		user_input_element_attribute=input("Enter the object's "+chosen_identifier)
		if chosen_identifier !=('---other---') and chosen_identifier !=('declared_string'):
			executable_string="global "+element_name+"; "+element_name+'=driver.find_element_by_'+chosen_identifier+'("'+user_input_element_attribute+'")'
		elif chosen_identifier == ('declared_string'):
			executable_string="global "+element_name+"; "+element_name+'= "'+user_input_element_attribute+'"'
		else:
			executable_string=input('Enter the code:\n')
		verification_step=input(executable_string+'\n correct? y/n\n')
		if verification_step.lower()=='y':
			pass
		else:
			return False
		self.page.update({element_name:executable_string})
		self.page.save_page()
	def add_select(self,element_name):
		identifier_list=['id','name','css_selector','link_text','partial_link_text','---other---']
		chosen_identifier=self.function_runner.print_menu(identifier_list)
		user_input_element_attribute=input("Enter the object's "+chosen_identifier)
		if chosen_identifier !=('---other---'):
			executable_string="global "+element_name+"; "+element_name+'=Select(driver.find_element_by_'+chosen_identifier+'("'+user_input_element_attribute+'"))'
		else:
			executable_string=input('Enter the code:\n')
		verification_step=input(executable_string+'\n correct? y/n\n')
		if verification_step.lower()=='y':
			pass
		else:
			return False
		self.page.update({element_name:executable_string})
		self.page.save_page()
	def highlight_elements(driver):
		driver.execute_script('document.getElementById("lst-ib").style.backgroundColor = "#FDFF47";')
	def print_something(self):
		print('something')
"""
class library_builder:
	def __init__(self,environment,project,projects_directory="S:\QA\Projects"):
	self.project_list=[]
	self.projects_directory=projects_directory
	self.environment=environment
	self.project=project
#		self.page
	self.page_directory=projects_directory+'/'+project+'/or/'+environment
"""