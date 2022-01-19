Welcome to repokeeper, use this tool to create and maintain test data as well as manage your .npy object repository.

The repokeeper features visual element highlighting which uses javascript to identify and highlight objects on the page.
This can be used to test your object identifiers. It is also used by the system when you take advantage of its automatic object discovery function.
The program will identify each input, select or checkbox on the page and highlight the one its thinking of. 
Simply enter the name you'd like to give the highlighted web element and repokeeper will add it to your object repo for you. Experts say this extends
the life of your ctr, C and V keys by up to 50%

It even works on dynamically generated salesforce elements. 
If you need to test a web form designed in salesforce that might have 5 inputs for 5 family members in one test scenario but 12 inputs on the same page 
with a different family, repomatic can handle that.

Repomatic is designed to be used in an CLI instance of python or Jupyter notebook on an existing webdriver session. It's an aid for test creation 
and web element identification so there was no need to make it an executable CLI tool, instead it has to be imported into an existing instance of python.

Usage is as follows:

python
>>>from selenium import webdriver
>>>import repokeeper
>>>driver=webdriver.Chrome()
>>>wizard=repokeeper.repo_tools(driver)

###this is a tool to help while you've got a selenium session open. At this point you would run the code or navigate to the page you're
writing the test for

>>>wizard.page_wizard()<br>
>>>----------------------------<br>
>>>Current page= mypage<br>

>>>list found<br>
>>>1.) Add Object<br>
>>>2.) Update Repo<br>
>>>3.) Update Data<br>
>>>4.) Iterate Objects<br>
>>>5.) define subgroup<br>
>>>6.) remove items<br>
>>>7.) List Repo Items<br>
>>>8.) Change Current Page<br>
>>>9.) Add dynamic input set<br>
>>>10.) define datavalues for a dynamic input<br>
>>>Choose:<br>


Select the option 4 here and the tool will ask you if you're trying to identify input elements, select elements or checkboxes.

The tool will then highlight each element it detects in red one at a time and prompt the user to answer if they'd like to update the repo with that element,

If you select Yes, it will first ask you for a subgroup. This allows you to more precisely identify elements from different sections of a page.
