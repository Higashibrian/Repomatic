from selenium import webdriver
from selenium.webdriver.support.ui import Select
import bh_global_functions
import os
import command_executor
import numpy
import sys
from IPython.display import clear_output
class object_writer:

	def __init__(self, repo_loc,driver):
		self.driver=driver
		self.current_page=''
		converted_location=''
		split_loc_list=[]
		make_directory_string=''
		if os.path.isfile(repo_loc):
			converted_location=repo_loc.replace('\\','/')
			converted_location=converted_location.replace('//','/')
			#open .npy file, create a self.file variable
		else:
			converted_location=repo_loc.replace('\\','/')
			converted_location=converted_location.replace('//','/')
			split_loc_list=converted_location.split('/')
			make_directory_string=''
			for item in split_loc_list:
				print(make_directory_string)
				if '.' not in item:
					make_directory_string+=item
				try:
					os.mkdir(make_directory_string)
				except:
					pass
				make_directory_string+="/"
			numpy.save(converted_location,{})
		self.repo_loc=converted_location
		self.repo=numpy.load(self.repo_loc, allow_pickle=True).all()

	def save_repo(self):
		numpy.save(self.repo_loc,self.repo)
	def remove_page(self,page_name):
		del self.repo[page_name]
		numpy.save(self.repo_loc,self.repo)
	def load_page(self,page_name):
		try:
			self.repo[page_name]
			self.current_page=page_name
		except Exception as e:
			print ('Could not find page')
			print (e)
	def add_page(self,page_name):
		if page_name in self.repo:
			print ('the page already exists')
			pass
		else:
			self.repo.update({page_name:{}})
		self.save_repo()
		self.load_page(page_name)
	def get_properties(self,webelement,element_list=["id",'class','name','type','size'],additional_properties=[]):
		element_list.extend(additional_properties)
		element_list=list(set(element_list))
		element_list.sort()
		prop_dict={}
		for prop in element_list:
			element_prop=webelement.get_attribute(prop)
			prop_dict.update({prop:element_prop})
		return(prop_dict)
	def write_entry(self,name,elm_dicto):
		#1/31/2018 removed the select and dynamic arguments and declaration
		#no other code should have been affected by this change.
		#this function will still write a single dictionary to the .npy file
		#but when writer functions of the repo_tools class are used they will
		#follow a format like this: "Element"{properties_dict:{properties},dynamic:True,subgroup:'subgroup,etc:etc'}
		repo_entry={name:elm_dicto}
		#if the usage of other keywords becomes necessary then create 
		#additional conditionals here.
		self.repo[self.current_page].update({name:elm_dicto})
		self.save_repo()
	def remove_entry(self,name):
		try:
			del self.repo[self.current_page][name]
		except:
			print ("Error could not find the item "+name+' in '+self.current_page)
		numpy.save(self.repo_loc,self.repo)
	#TODO:
	#create a function for handling the very common 
	#pattern of dynamically created input and select boxes
	#first_string+number+first string
	#rather than concatenating two strings, it could be a better idea 
	#to use the replace function
# class object_reader:
# 	def __init__(self, repo_loc,dataloc,driver):
# 		self.driver=driver
# 		self.repo_loc=repo_loc
# 		self.dataloc=dataloc
# 		self.data=numpy.load(dataloc).all()
# 		self.repo=numpy.load(self.repo_loc+'/repository.npy').all()
# 	def set_page(self,page):
# 		self.current_page=page
# 	def return_dynamic_object(self,object,replacement_string='#replace#'):
# 		pass
# 	def return_select():
# 		pass
# 	def return_element():
# 		pass
# 	def find(self,term):
# 		element_dict=self.repo[self.current_page][term]
# 		identistring=element_dict['properties']
# 		primary_id=element_dict['Primary identifier']
# 		if primary_id=='link_text':
# 			element=self.driver.find_element_by_link_text(identistring['element text'])
# 		elif primary_id=='partial_link_text':
# 			element=self.driver.find_element_by_link_text(identistring['element text'])
# 		elif primary_id=='css_selector':
# 			element=self.driver.find_element_by_css_selector(identistring['element text'])
# 		elif primary_id=='xpath':
# 			element=self.driver.find_element_by_xpath(identistring['element text'])
# 		else:
# 			identifier='['+primary_id+'="'+identistring[primary_id]+'"]'
# 			print 'identifier: '+identifier
# 			element=self.driver.find_element_by_css_selector(identifier)
# 		return element
		#an instance of this class is meant to be 
	#used to compile the entries from an object dictionary.
	#
	#each webelement will be stored with multiple 
	#identifiers in a single dictionary
	#
	#As with the original "repomatic", each .npy file can be used
	#to represent a page.
	#this object reader will attempt to return a web_element object
class repo_tools:
	def __init__(self,driver,file_location="S:\QA\Projects",test_name=''):
		self.selenoid=bh_global_functions.selenium_driver(driver)
		self.current_project=""
		self.primary_identifier={'primary_id':'id'}
		self.subgroup='default'
		self.driver=driver
		self.file_location=file_location
		self.function_runner=bh_global_functions.other_functions()
		self.print_details=self.function_runner.print_details
		self.print_title=self.function_runner.print_title
#		self.reader=object_reader(self.driver)
		self.repo_loc=self.load_repo()
		self.data_location=file_location+'/'+self.current_project
		self.print_title('Load Dataset')
		try:
			os.mkdir(self.data_location+'/testscripts')
		except:
			pass
		try:
			os.mkdir(self.data_location+'/testscripts/data')
		except:
			pass			
		self.data_location=self.data_location+'/testscripts/data'		
		if test_name:
			self.data_location=self.data_location+'/'+test_name
		print ('\ndata location: ')
		print (self.data_location)
		self.load_data_set()
#		self.data_location+'/'+dataset+'.npy'
		self.writer=object_writer(self.repo_loc,self.driver)
		print (str(self.dataset_name))
		datadoink=self.data_location+'/'+self.dataset_name+'.npy'
		self.actor=command_executor.actor(self.repo_loc,datadoink,self.driver)
#		self.page_wizard()

	def code_writer(category_name,page_name):
		self.actor.refresh_library()
		item_list=actor.repo[page_name][category_name]['fields']

		for item in item_list:
		    print (item+'s =[]')
		    
		print ("\nfor item in actor.data['"+page_name+"'].keys():")
		print ("\tif '"+category_name+"' in item:")
		for item in item_list:
		    print ('\t\tif item.endswith("'+item+'"):')
		    print ('\t\t\t'+item+'s.append(item)')
		#    print item+"=actor.dynamic_find('vehicles','"+item+"',x)"
		#    print item+'.clear()'
		#    print item+'.send_keys(actor.data["resources"]['+item+'[x]])'
		for item in item_list:
			print (item+'s.sort()')
		print('x=0')

		print ('for item in '+item_list.keys()[0]+'s:')
		print ('\ttry:')
		print ("\t\tactor.dynamic_find('"+category_name+"','"+item_list.keys()[0]+"',x)")
		print ('\texcept:')
		print ('\t\tactor.find("add_'+category_name+'",offset=-200).click()')
		print ('\t\twait_for_element_to_fade(selector)')
		print ('\t\ttime.sleep(.5)')

		#            wait_for_element_to_fade(selector)
		#            time.sleep(.5)
		for item in item_list:
		    print('\t'+item+'=actor.dynamic_find("'+category_name+'","'+item+'",x)')
		    print ('\t'+item+'.clear()')
		    print ('\t'+item+'.send_keys(actor.data["'+page_name+'"]['+item+'s[x]])')
		print ('\tx+=1')

	def reverse_lookup(self,identifier,identify_by):
		return_list=[]
		page_elements=self.writer.repo[self.writer.current_page]		
		for element in page_elements:
			if 'dynamic' in page_elements[element].keys():
				if page_elements[element]['dynamic']==True:
					pass
			else:
				if 'text' in identify_by:
					identify_by='element text'
				elif 'css' in identify_by:
					identify_by='css_selector'
				returned_value=page_elements[element]['properties'][identify_by]
				if returned_value==identifier:
					title=element
					details=page_elements[element]['properties']
					return_list.append({element:details})
					self.function_runner.print_details(element,details)
		return return_list

	def find(self,term):
		self.actor.find('term')

	def update_dataset(self):
		if self.writer.current_page in self.dataset.keys():
			pass
		else:
			self.dataset.update({self.writer.current_page:{}})

	def add_data(self,element,dv):
		self.update_dataset()
		print ('current project: '+self.current_project)
		print ('current page: '+self.writer.current_page)
		data_key=element
		data_value=dv
		self.dataset[self.writer.current_page].update({data_key:data_value})
		numpy.save(self.dataloc+'/'+self.dataset_name+'.npy',self.dataset)
	def write_multiple_datasets(self):
		title=input('Enter the dataset title')
		sg=subgroup_list()
		element_list=find_elements_by_subgroup()

		self.highlight(current_element)
		self.data_fill(current_element,data_val)

		self.highlight(current_element,color='initial')
	def load_data_set(self):
		dataset_names=[]
		for datafile in os.listdir(self.data_location):
			if '.npy' not in datafile:
				pass
			else:
				dataset_names.append(datafile.split('.')[0])
		dataset_names.append('---new---')
		dataset=self.function_runner.print_menu(dataset_names)
		if dataset=='---new---':
			while True:
				new_ds=input('Name the new dataset:\n')
				if new_ds in dataset_names:
					print ('There is already a dataset called '+new_ds)
				else:
					check_item=input("name dataset '"+new_ds+"'?\ny/n")
					if check_item=='y':
						dataset=new_ds
						numpy.save(self.data_location+'/'+dataset+'.npy',{})
						break
					else:
						pass
		self.dataloc=self.data_location
		self.dataset_name=dataset
		self.dataset=numpy.load(self.data_location+'/'+dataset+'.npy', allow_pickle=True).all()
		return dataset
	# def navigate_data(self):
	# 	print self.dataset
	def remove_data(self):
		datalist=self.dataset[self.writer.current_page].keys()
		datalist.sort()
		print ('-')
		item_for_removal=self.function_runner.print_menu(datalist)
		print ('--')
		self.dataset[self.writer.current_page].pop(item_for_removal,None)
		print ('---')
		numpy.save(self.dataloc+'/'+self.dataset_name+'.npy',self.dataset)
		print ('----')
	def save_data_set(self):
		dataset_names=[]
		for datafile in os.listdir(self.data_location):
			if '.npy' not in datafile:
				pass
			else:
				dataset_names.append(datafile.split('.')[0])
		dataset_names.append('---new---')
		dataset=self.function_runner.print_menu(dataset_names)
		if dataset=='---new---':
			while True:
				new_ds=input('Name the new dataset:\n')
				if new_ds in dataset_names:
					print ('There is already a dataset called '+new_ds)
				else:
					check_item=input("name dataset '"+new_ds+"'?\ny/n")
					if check_item=='y':
						dataset=new_ds
						break						
		numpy.save(self.dataloc+'/'+dataset+'.npy',self.dataset)
		
#	def add_data_value(self,object):

		#current page data.write dataset[current_page]['new term':'value']

	def load_page(self):
		pagelist=[]
		#pagelist(t=[])
		print ('Select the page')
		for item in self.writer.repo:
			pagelist.append(item)
		pagelist.sort()
		pagelist.append('--new--')
		page=self.function_runner.print_menu(pagelist)
		if page == '--new--':
			new_page=input('Name the new page:\n')
			self.writer.add_page(new_page)
			page=new_page
		else:
			pass
		self.writer.load_page(page)

	def subgroup_list(self):
		sglist=[]
		print ('Select the subgroup')
		page_elements=self.writer.repo[self.writer.current_page]
		for item in page_elements.keys():
			element_properties=page_elements[item]
			try:
				subgroup=element_properties['subgroup']
				if subgroup not in sglist:
					sglist.append(subgroup)
			except Exception as e:
				print (e)
		if self.subgroup not in sglist:
			sglist.append(self.subgroup)
		sglist.sort()		
		selected_sg=self.function_runner.print_menu(sglist)
		return selected_sg
	def find_elements_by_subgroup(self,subgroup):
		element_list=[]
		page_elements=self.writer.repo[self.writer.current_page]
		for item in page_elements.keys():
			try:
				element_properties=page_elements[item]
				if subgroup == element_properties['subgroup']:
					element_list.append(item)
			except Exception as e:
				print (e)
		element_list.sort()
		return element_list
#	DELETE 3/6/2018
#	def update_list(self,update_list):#
#		for item in update_list:
#			object=self.writer.repo['self.writer.current_page'][item]
	def fill_data_for_dynamic_fields(self):
		dynamics=[]
		for item in self.writer.repo[self.writer.current_page]:
			if 'dynamic' in self.writer.repo[self.writer.current_page][item]:
#				print 'hawakdafoo '+item
#				print self.writer.repo[self.writer.current_page][item]['dynamic']
				if self.writer.repo[self.writer.current_page][item]['dynamic']==True:
					print (item+' was accepted')
					dynamics.append (item)
		print (dynamics)
		print ('Choose an item')
		item_choice=self.function_runner.print_menu(dynamics)

		box_name=input('Enter a name for this data category')

		funct=self.function_runner.print_menu(['Update single value','Iterate through all items'])
		if funct=='Update single value':
			update_choice=self.function_runner.print_menu(self.writer.repo[self.writer.current_page][item_choice]['fields'].keys())

			prefix=self.writer.repo[self.writer.current_page][item_choice]['prefix']
			suffix=self.writer.repo[self.writer.current_page][item_choice]['fields'][update_choice]
			print ('suffix: '+suffix)
			numbers=self.driver.find_elements_by_css_selector('[id$="'+suffix+'"]')
			no_of_els=len(numbers)
			squash_menu=[]
			for x in range(0,no_of_els):
				print (x)
				squash_menu.append(str(x))
			print (str(no_of_els)+ 'entries found on page')
			squash=self.function_runner.print_menu(squash_menu)
			identifaction=prefix+':'+str(squash)+':'+suffix
			print (identifaction)
			element=self.driver.find_element_by_id(identifaction)
			dv=self.val_prompt(element)
			data_name=box_name+'_'+item_choice+'_'+update_choice+'_'+str(squash)
			print ('data value saved to datafile as '+data_name)
			self.add_data(data_name,dv)
		else:
			for update_choice in self.writer.repo[self.writer.current_page][item_choice]['fields'].keys():
				print (update_choice+':')
				prefix=self.writer.repo[self.writer.current_page][item_choice]['prefix']
				suffix=self.writer.repo[self.writer.current_page][item_choice]['fields'][update_choice]
				print ('suffix: '+suffix)
				numbers=self.driver.find_elements_by_css_selector('[id$="'+suffix+'"]')
				no_of_els=len(numbers)
				squash_menu=[]
				for x in range(0,no_of_els):
					try:
						print (x)
						squash=x
						identifaction=prefix+':'+str(squash)+':'+suffix
						print (identifaction)
						element=self.driver.find_element_by_id(identifaction)
						self.highlight(element)
						dv=self.val_prompt(element)
						data_name=box_name+str(squash)+'_'+item_choice+'_'+update_choice
						print ('data value saved to datafile as '+data_name)
						self.add_data(data_name,dv)
						try:
							self.data_fill(element,dv)
						except Exception as e:
							print ('Could not send data to element ')
							print (e)
						self.highlight(element,color='initial')
					except:
						print ('could not find element '+prefix+'['+str(x)+']')
	def add_dynamic_set(self):
		element_entry={'dynamic':True}
		prefix=input('enter the common string prefix')
		string_search='id^="'+prefix+'"]'
		element_entry.update({'prefix':prefix})
		print (string_search)
		group_items=self.driver.find_elements_by_css_selector('[id^="'+prefix+'"]')
		if len(group_items)<1:
			group_items=self.driver.find_elements_by_css_selector('[name^="'+prefix+'"]')
		a_big_list=[]
		for item in group_items:
			a_big_list.append(item.get_attribute('id'))		    
			self.highlight(item)	
		box_name=input('Name the box:\n')
		if box_name in self.writer.repo[self.writer.current_page]:
			print (box_name+' already in repo')
			already_in=input('Press any key to continue, type "quit" to quit.')
			if already_in.lower()=='quit':
				return False
			else:
				pass
		for item in group_items:
			self.highlight(item,color='Initial')

		item_list=[]
		for element in a_big_list:
		    ending=''
		    item=element
		    item_end=element.split(':')[len(element.split(':'))-1]
		    if item_end in item_list:
		        pass
		    else:
		    	item_list.append(item_end)
		table_array={}
		for field_type in item_list:
		    for element in self.driver.find_elements_by_css_selector('[id$="'+field_type+'"]'):
		        self.highlight(element)
		    name=input('Enter the field name:\ntype "s" to skip')
		    if name=='s':
		    	pass
		    else:
			    for element in self.driver.find_elements_by_css_selector('[id$="'+field_type+'"]'):
			        self.highlight(element,color='Initial')
		    table_array.update({name:field_type})
		element_entry.update({'fields':table_array})
		self.writer.write_entry(box_name,element_entry)
		print (box_name)
		print (element_entry)
	def subgroup_menu(self):
		clear_output()
		sglist=[]
		print ('Select the subgroup')
		page_elements=self.writer.repo[self.writer.current_page]
		for item in page_elements.keys():
			element_properties=page_elements[item]
			try:
				subgroup=element_properties['subgroup']
				if subgroup not in sglist:
					sglist.append(subgroup)
			except Exception as e:
				print (e)
		if self.subgroup not in sglist:
			sglist.append(self.subgroup)
		sglist.sort()
		sglist.append('--new--')
		selected_sg=self.function_runner.print_menu(sglist)
		if selected_sg == '--new--':
			while True:
				new_sg=input('Name the new subgroup:\n')
				if new_sg in sglist:
					print ('There is already a group named '+new_sg)
				else:
					check_item=input("name subgroup '"+new_sg+"'?\ny/n")
					if check_item=='y':
						selected_sg=new_sg
						break
					else:
						pass
		self.subgroup=selected_sg
		print ('The current subgroup is: '+self.subgroup)

	def remove_from_repo(self,edit_object=''):
		if not edit_object:
			items=self.writer.repo[self.writer.current_page].keys()
			items.sort()
			edit_object=self.function_runner.print_menu(items)
		else:
			pass
		try:
			self.writer.remove_entry(edit_object)
		except:
			print ('Unable to remove '+edit_object+' from object repo')
		try:
			del self.dataset[self.writer.current_page][edit_object]
			numpy.save(self.dataloc+'/'+self.dataset_name+'.npy',self.dataset)
		except:
			print ('Unable to find/remove '+edit_object+' from '+self.writer.current_page+' page')
	def repo_items(self):
		objects=self.writer.repo[self.writer.current_page].keys()
		objects.sort()
		edit_object=self.function_runner.print_menu(objects)
		title='Element: '+edit_object
		print (self.print_title(title))
		print ('\n')
		for item in self.writer.repo[self.writer.current_page][edit_object]:
			if len(item)<4:
				menu_key=item+':    '
			else:
				menu_key=item+':'
			if len(menu_key)<9:
				menu_key=menu_key+'   '
			print (menu_key+"\t"+ str(self.writer.repo[self.writer.current_page][edit_object][item]))
		print ('\n')
	def element_update(self):
		edit_object=self.function_runner.print_menu(self.writer.repo[self.writer.current_page].keys())
		title='Element: '+edit_object
		print (self.print_title(title))
		for item in self.writer.repo[self.writer.current_page][edit_object]:
			if len(item)<4:
				menu_key=item+':    '
			else:
				menu_key=item+':'
			if len(menu_key)<9:
				menu_key=menu_key+'   '
			print (menu_key+"\t"+ str(self.writer.repo[self.writer.current_page][edit_object][item]))
		choices=['update_identifier','update data entry']
# 
# 	def print_title(self,title):
# 		if type(title) != str:
# 			pass
# 		else:
# 			total_length=len(title)+4
# 		bread='-'*total_length
# 		butter='--'+title+'--'
# 		sandwich=bread+'\n'+butter+'\n'+bread
# 		return sandwich
# 	def print_details(self,title,details):
# 		print self.print_title(title)
# 		for item in details:			
# 			if len(item)<4:
# 				menu_key=item+':    '
# 			else:
# 				menu_key=item+':'
# 			if len(menu_key)<9:
# 				menu_key=menu_key+'   '
# 			print menu_key+"\t"+ str(details[item])
# 		print '\n'
#
	def edit_dataset(self,item_list=''):
		data_items=[]
		if item_list:
			data_items=item_list
		else:
			for item in self.writer.repo[self.writer.current_page]:
				data_items.append(item)
			print (data_items)
			input('1')
			try:
				dataset_length=len(self.dataset[self.writer.current_page])
			except:
				dataset_length=0
			if dataset_length>0:
				for item in self.dataset[self.writer.current_page]:
					if item not in data_items:
						data_items.append(item)
				print (data_items)
				input('2')
		options_list=[]
		for item in data_items:
			options_list.append(item)
		options_list.sort()
		choice=self.function_runner.print_menu(options_list)
		try:
			print ('Previous data value: '+self.dataset[self.writer.current_page][choice])
		except:
			print ('Previous data not found: ')
		new_dv=input('Enter the new data value')
		self.add_data(choice,new_dv)
	def element_wizard(self):
		title='Page: '+self.writer.current_page
		print (self.print_title(title))
		elm_wizard_options=['Add Object','Update Repo','Update Data','Iterate Objects','define subgroup','remove items','List Repo Items','Change Current Page','Add dynamic input set','define datavalues for a dynamic input']
		selection=self.function_runner.print_menu(elm_wizard_options)
		if selection == 'Update Repo':
			self.update_element()
		if selection == 'Update Data':
			data_choice=self.function_runner.print_menu(['select a subgroup','list the whole page'])
			if data_choice=='select a subgroup':
				while True:
					selected_sg=self.subgroup_list()
					element_list=self.find_elements_by_subgroup(selected_sg)
					self.edit_dataset(item_list=element_list)
					sg_break=input('Type "Q" to quit\n')
					if sg_break.lower()== 'q':
						break
			else:
				self.edit_dataset()
		if selection == "Change Current Page":
			self.load_page()
		if selection == "List Repo Items":
			self.repo_items()
		if selection == "remove items":
			self.remove_from_repo()
		if selection == "Add Object":
			self.add_single_object()
		if selection == "Iterate Objects":
			iter_choice=self.function_runner.print_menu(['Iterate_inputs','Iterate_selects','Iterate_checkboxes','Update the entire page'])
			if iter_choice=='Iterate_inputs':
				self.iterate_inputs()
			elif iter_choice=='Iterate_checkboxes':
				self.iterate_checkboxes()
			elif iter_choice=='Iterate_selects':
				self.iterate_selects()
			elif iter_choice=='Update the entire page':
				self.fill_data_for_entire_page()
		if selection == "define subgroup":
			self.subgroup_menu()
		if selection == 'Add dynamic input set':
			self.add_dynamic_set()
		if selection == 'define datavalues for a dynamic input':
			self.fill_data_for_dynamic_fields()
#	def iterate_unidentified_objects(self):
#		found_list=[]
#		for item in self.repo[self.writer.current_page]:
#			try:
#				self.find(item)
#			except:

	def update_element(self):
		found_repo_choice=0
		repo_items=[]
		for item in self.writer.repo[self.writer.current_page]:
			repo_items.append(item)
		repo_items.sort()
		repo_choice=self.function_runner.print_menu(repo_items)
		self.function_runner.print_title('Element: '+repo_choice)
		self.add_single_object(elmnt_name=repo_choice,from_page=False)

	def iterate_checkboxes(self):
		for item in self.driver.find_elements_by_css_selector('input'):
			if item.get_attribute('type')=='checkbox':
				self.add_object(item)
	def iterate_selects(self):
		for item in self.driver.find_elements_by_css_selector('select'):
			self.add_object(item)
	def iterate_inputs(self):
		for item in self.driver.find_elements_by_css_selector('input'):
			self.add_object(item)
	def add_object(self,current_element):
		props=self.return_properties(current_element)
		print ('\nAdd this element?')
		self.highlight(current_element)
		self.function_runner.print_details('Properties:',props)
		addit=input('y/n: ')

		if addit=='y':
			print ('Subgroup='+self.subgroup)
			change_sg=input('Change subgroup?y/n: ')
			if change_sg=='y':
				self.subgroup_menu()
			else:
				pass
			print ("Select the Primary identifier")
			el_type= current_element.get_attribute('type')
			primary_keys=self.return_primary_keys(props)
			aso_selection=self.function_runner.print_menu(primary_keys)
			element_text=current_element.get_attribute('text')
			props.update({'element text':element_text})

			items=[]
			element_list=current_element.find_elements_by_css_selector('option')
			for item in element_list:
				items.append(item.text)

			self.function_runner.print_details('Props',props)
			print ('subgroup: '+self.subgroup)
			element_entry={'properties':props,'subgroup':self.subgroup,'Primary identifier':aso_selection}
			element_entry.update({'choices':items})
			element_name=input('Name the element: ')
			self.writer.write_entry(element_name,element_entry)

			data_val=self.val_prompt(current_element)
			
			if el_type=='radio' and data_val=='pick':
				current_element.click()
			if el_type=='text' and data_val:
				current_element.clear()
				current_element.send_keys(data_val)
			if 'select' in el_type and data_val:
				secto=Select(current_element)
				secto.select_by_visible_text(data_val)
			if el_type=='checkbox':
				if data_val=='checked':
					try:
						self.selenoid.check(current_element)
					except Exception as e:
						print ('unable to check element')
						print ('-----------------------')
						print (e)
						print ('-----------------------')
				if data_val=='unchecked':
					try:
						self.selenoid.uncheck(current_element)
					except Exception as e:
						print ('unable to check element')
						print ('-----------------------')
						print (e)
						print ('-----------------------')
#			self.data_fill(current_element,data_val)
			self.add_data(element_name,data_val)
		self.highlight(current_element,color='initial')
	def add_single_object(self,elmnt_name='',from_page=True):
		element_text=''
		aso_menu=['id','css_selector','name','xpath','partial_link_text','link_text']
		print ('Identify object by: ')
		aso_selection=self.function_runner.print_menu(aso_menu)
		print ('\n')
		raw_identifier=input('Enter the '+aso_selection+':\n')
		if aso_selection=='id' or aso_selection=='name':
			identifier='['+aso_selection+'="'+raw_identifier+'"]'
			element=self.driver.find_elements_by_css_selector(identifier)
		else:
			identifier=raw_identifier
		if aso_selection =='css_selector':
			element=self.driver.find_elements_by_css_selector(identifier)
		if aso_selection=='xpath':
			element=self.driver.find_elements_by_xpath(identifier)
		if aso_selection=='partial_link_text':
			element_text='identifier'
			element=self.driver.find_elements_by_partial_link_text(identifier)
		if aso_selection=='link_text':
			element_text=identifier
			element=self.driver.find_elements_by_link_text(identifier)	
		if len(element)<1:
			print ('Unable to identify that element')
		if len(element)>1:
			print ('Identified more than one element')
		if len(element)==1:
			print ("Element Identified")
			current_element=element[0]
			if from_page==True:
				print ('heyo')
				print (identifier)
				print (aso_selection)
				try:
					found_elements=[]
					found_elements=self.reverse_lookup(raw_identifier,aso_selection)
				except:
					pass
				if len(found_elements)>0:
					if len(found_elements)<2:
						print ('Found an entry in the or!')
					elif len(found_elements)>1:
						print ('Found multiple entries in the or!'						)
					for entry in found_elements:
						print (entry.keys()[0])
					for term in found_elements:
						choice_cuts=['Remove','Rename','Skip','Quit']	
						item=term.keys()[0]
						title=self.function_runner.print_title(item)
						print (title)
						cut_choice=self.function_runner.print_menu(choice_cuts)
						if cut_choice=='Quit':
							return'Aye aye captain'
						elif cut_choice!='Skip':
							old_info=self.writer.repo[self.writer.current_page][item]
							element_info=old_info
							print (item)
							self.remove_from_repo(edit_object=item)
							if cut_choice=='Rename':
								new_name=input('Enter the new name:\n')
								self.writer.write_entry(new_name,element_info)
					return True
			self.highlight(current_element)
			print ('Subgroup='+self.subgroup)
			change_sg=input('Change subgroup?y/n: ')
			if change_sg=='y':
				self.subgroup_menu()
			else:
				pass
			print ("Select the Primary identifier")
	#		props=self.writer.get_properties(current_element)
			props=self.return_properties(current_element)
			if aso_selection=='xpath' or aso_selection=='css_selector':
				props.update({aso_selection:identifier})
			if not element_text:
				element_text=current_element.get_attribute('text')
			props.update({'element text':element_text})
			self.function_runner.print_details('Props',props)
			print ('subgroup: '+self.subgroup)
			element_entry={'properties':props,'subgroup':self.subgroup,'Primary identifier':aso_selection}
			if elmnt_name:
				element_name=elmnt_name
			else:
				element_name=input('Name the element: ')

				data_val=self.val_prompt(current_element)

				print (current_element.get_attribute('type'))

				self.data_fill(current_element,data_val)
				self.add_data(element_name,data_val)
			#self.data_fill(self,element,dv)
			self.writer.write_entry(element_name,element_entry)
			self.highlight(current_element,color='initial')
	def fill_data_for_entire_page(self):
		self.actor.refresh_library()
		self.actor.set_page(self.writer.current_page)
		could_not_find=[]
		skipped_items=[]
		updated_counter=0
		for item in self.writer.repo[self.writer.current_page]:
			current_value='None'
			found=0
			print (item)
			try:
				update_element=self.actor.find(item,offset=-200,wait=.25)
				found=1
			except Exception as e:
				could_not_find.append(item)
				print ('could not find '+item)
				print (e)
			if found==1:
				try:
					current_value=self.actor.fetch(item)
				except:
					pass
				self.highlight(update_element)
				print (item+' field, current value: '+str(current_value))
				update_prompt=input('Update the '+item+' field? y/n?')
				self.highlight(update_element,'initial')
				if update_prompt.lower()=='n':
					skipped_items.append(item)
				if update_prompt.lower()=='y':
					data_check=''
					updated_counter+=1

					while True:
						self.print_title(item)
						try:
							new_value=self.val_prompt(update_element)
							self.data_fill(update_element,new_value)
							data_check=input('Use the value: '+new_value+' ?(y/n)')
						except Exception as e:
							print ('Sorry, something went wrong')
							print (repr(e))
						if data_check.lower()=='y':
							try:
								self.add_data(item,new_value)
								self.writer.save_repo()
							except Exception as e:
								print ('Could not complete action')
								print ('Object: '+str(item))
								print ('Data: '+str(new_value))
								print (repr(e))
							break
						else:
							redo=input('press any key to enter a new value\nor "s" to(s)kip\n:')
							if redo.lower()=='s':
								break
				try:
					self.highlight(update_element,'initial')
				except:
					pass
	def val_prompt(self,element):
		dv=''
		el_type=str(element.get_attribute('type'))
		print ('Element of type: '+str(el_type)+' found')
		if 'text' in el_type.lower():
			dv=input('Enter the keys: ')
		elif 'select' in el_type.lower():
			print ('selection triggered')
			items=[]
			element_list=element.find_elements_by_css_selector('option')
			for item in element_list:
				items.append(item.text)
			dv=self.function_runner.print_menu(items)
		elif el_type=='checkbox':
			items=['checked','unchecked']
			dv=self.function_runner.print_menu(items)
		elif el_type=='radio':
			items=['pick','pass']
			dv=self.function_runner.print_menu(items)
		else:
			dv=input('Enter the data value: ')
		return dv
	def data_fill(self,element,dv):
		self.selenoid.scroll_to(element,yoffset=-200)
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
				a=''
				b=''
				c=''
				try:
					self.selenoid.check(element)
				except Exception as a:
					try:
						self.selenoid.scroll_to(element,yoffset=0)
						self.selenoid.check(element)
					except Exception as b:
						try:
							self.selenoid.scroll_to(element,yoffset=200)
							self.selenoid.check(element)
						except Exception as c:
							print ('unable to check element')
							print (a)
							print ('-'*15)
							print (b)
							print ('-'*15)
							print (c)

			if dv=='unchecked':
				try:
					self.selenoid.uncheck(element)
				except Exception as e:
					print ('unable to uncheck element')
					print (e)
		else:
			pass

	def element_menu(self,element):
		clear_output()
		props=self.return_properties(element)
		self.highlight(element)
		page='Page:  '+self.writer.current_page
		subgroup='Subgroup:  '+self.subgroup['subgroup']
		title=['NEW ELEMENT','',page,subgroup,'']
		self.function_runner.print_details(title,props,title_lr_border='----------',title_buff='      ')
		menu_functions=['Change Subgroup','Add To Repo','--skip--']
		self.function_runner.print_menu(menu_functions)
		self.highlight(element,'initial')


	def return_properties(self,element):
		property_list=self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
		get_list=self.writer.get_properties(element)
		property_list.update(get_list)
		return property_list
	def return_primary_keys(self,props):
		keys_found=[]
		exceptions=[]
		found_objects=[]
		for item in props:
			value=props[item]
			try:
				found_objects=self.driver.find_elements_by_css_selector('['+item+'="'+value+'"]')
			except Exception as e:
				excptn={item:e}
				exceptions.append(str(excptn))
			if len(found_objects)==1:
				keys_found.append(item)
		if len(exceptions)>0:
			print ('Errors: \n')
			for excp in exceptions:
				print (str(excp))
				for key in excp:
					print (key)
					print ('When trying to locate element by '+key+' the following error occured: \n:::'+str(excp[key])+':::')
		return keys_found
	def highlight(self,element,color="1px solid red"):
		#set color='initial' to reset to its original value.
		#self.driver.execute_script('arguments[0].scrollIntoView();',element)
		self.driver.execute_script('arguments[0].style.outline="'+color+'";',element)
	def page_wizard(self):

		while True:

			page=self.writer.current_page
			self.actor.set_page(page)
			if page:
				self.print_title(page)
			else:
				self.load_page()
			self.element_wizard()
			self.update_dataset()
			dingo=input("it's no 'm' day:")
#			clear_output()
			if dingo =='m':
				return True
	def help(self):
		print ("write_dynamic_entry(self,full_string,identifier='id',replace_with_char='\#replace\#',replace_char=':0:')')")

	# def iterate_objects(self):
	# 	to_do=[]
	# 	tagged=[]
	# 	skipped=[]
	# 	element_list=self.driver.find_elements_by_css_selector('*')
	# 	inputs=self.driver.find_elements_by_css_selector('input')
	# 	selects=self.driver.find_elements_by_css_selector('select')
	# 	for item in element_list:
	# 		element_type=item.get_attribute('type')
	# 		self.writer.get_properties(self,webelement,driver,element_list=["id",'class','name','type','maxlength','size'],additional_properties=[])

	# # def define_subgroup(self,subgroup):
	# # 	self.subgroup=subgroup
	def load_repo(self,repo_name='repository.npy'):
		project_location=self.file_location
		project_names=[]
		for folder in os.listdir(project_location):
			if '.' in folder:
				pass
			else:
				project_names.append(folder)
		project_names.append('---new---')
		print (self.print_title('Select the Project: '))
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
				print ('try again')
				return False
			project=new_project
		self.current_project=project
		try:
			os.mkdir(project_location+'/'+project)
		except:
			pass
		try:
			os.mkdir(project_location+'/'+project+'/or')
		except:
			pass
#		clear_output()
		print (self.print_title('Project: '+project))
		print ('Select environment: ')
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
		env_loc=or_location+'/'+environment
		try:
			os.mkdir(env_loc)
			full_loc=env_loc+'/'+repo_name
			numpy.save(full_loc,{})
			return full_loc
		except:
			pass
		full_loc=env_loc+'/'+repo_name
		return full_loc
