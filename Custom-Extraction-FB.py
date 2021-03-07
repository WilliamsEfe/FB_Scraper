from selenium import webdriver
import requests
import time
import re
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException


class Account_Scraper():
    
    def __init__(self,email,password):
        self.email = email
        self.password = password
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        #chrome_options.add_argument("--headless")  
        self.browser = webdriver.Chrome(executable_path ='chromedriver.exe',chrome_options=options)

    def signIn(self):
        self.driver = self.browser
        
        self.driver.get('https://web.facebook.com/login')
        a = self.driver.find_element_by_id('email')
        #change here
        a.send_keys(self.email)
        print ("Email Id entered...")
        b = self.driver.find_element_by_id('pass')
        #change here
        b.send_keys(self.password)
        print ("Password entered...")
        c = self.driver.find_element_by_id('loginbutton')
        c.click()
        #change here
        d= self.driver.get('https://www.facebook.com/groups/**groupid**/members/?_rdc=1&_rdr')
        self.driver.implicitly_wait(15)
        
        e=self.driver.find_element_by_xpath("//*[@class='inputtext']")
        #change here
        g = e.send_keys('**search term**')
        h = self.driver.find_element_by_css_selector('button[type=submit]')
        e.send_keys(Keys.ENTER)
        time.sleep(10)

        
        i = self.driver.find_elements_by_css_selector('span[class=timestampContent]')
        search_results = []
        for searches in i:
            j=i.index(searches)
            a = i[j].find_element_by_xpath("..").find_element_by_xpath("..")
            search_results.append(a.get_attribute("href"))
       
        people_that_commented = []
        users_commented = []
        users_liked = []
        for searchr in search_results:
            p = search_results.index(searchr)
            self.driver.get(searchr)
            time.sleep(10)
            content_blocks = self.driver.find_elements_by_css_selector('a[class=_6qw4]')
            list_of_hrefs = []
            for block in content_blocks:
                try:

                    list_of_hrefs.append(block.get_attribute("href"))
                    people_that_commented.append(block.text)
                    
                except NoSuchElementException:
                    list_of_hrefs.append("No comments")
                    pass
            
                users_commented += list_of_hrefs
            persons_that_commented = people_that_commented
            

            
            locks = self.driver.find_elements_by_css_selector('span[data-hover=tooltip]')
            c = None
            for a in locks:
                lin = locks.index(a)
                d=a.find_element_by_xpath("..").find_element_by_xpath("..")
                if a.text.isdigit() and d.tag_name == 'a':
                    c = d
                    break
            le = self.driver.get(c.get_attribute("href"))
            
            likes_blocks = self.driver.find_elements_by_xpath("//*[@class='_5j0e fsl fwb fcb']")
            likes = []
            people_that_liked = []
            for like in likes_blocks:
                try:
                    print(like.tag_name)

                    likes.append(like.find_element_by_css_selector('a').get_attribute("href"))#Likes of a post
                    people_that_liked.append(like.find_element_by_css_selector('a').get_attribute("title"))

                except NoSuchElementException:
                    likes.append("No Like for post")
                    pass
                users_liked += likes
                
                
        self.output = list(dict.fromkeys(users_commented + users_liked))
        self.output_names = list(dict.fromkeys(persons_that_commented + people_that_liked))
        print(self.output_names)
        print(self.output)
        
        global phone_number
        self.phone_number = []
        global email
        self.email = []
        global gender
        self.gender = []
        global city
        self.city = []
        self.user_list = []
        
        for list_of_href in self.output:
            #print("list "+list_of_href)
            self.driver.get(list_of_href)

            self.r = self.driver.find_element_by_xpath("//*[@data-tab-key='about']").get_attribute("href")
            self.driver.get(self.r)
            self.s = self.driver.find_element_by_xpath("//*[@class='_5pwr _Interaction__ProfileSectionContactBasic']").get_attribute("href")
            self.forplaces = self.s.replace('contact-info', "living", 1)
            #print(self.forplaces)
            self.driver.get(self.s)
            
            try:
                self.t = self.driver.find_element_by_css_selector('span[dir=ltr]').text
                self.phone_number.append(self.t)
 
                
                #print("phone number is "+t)
            except NoSuchElementException:
                self.t = "No Contact"
                self.phone_number.append(self.t)

            
            try:
                self.u = self.driver.find_element_by_xpath("//*[@class='_50f9 _50f7']")
                self.email.append(self.u.text)
                #print(self.u.tag_name)
            except NoSuchElementException:
                self.u = "No Email"
                self.email.append(self.u) 



            self.pattern = r'Male|Female'
            self.gender_determiner = []   
            self.v = self.driver.find_elements_by_css_selector('span[class=_2iem]')
            for a in self.v:
                self.gender_determiner.append(a.text)

            for text in self.gender_determiner:
                if re.match(self.pattern,text):
                    self.gender.append(text)
                else:
                    continue
            #self.gender_list += self.gender
            try:
                self.driver.get(self.forplaces)
                self.fetch_place = self.driver.find_element_by_xpath("//*[@class='_2iel _50f7']")
                place = self.fetch_place.text
                self.city.append(place)
                print(place)

            except NoSuchElementException:
                self.city.append("No Place added")
            

        time.sleep(2)
        self.driver.close()
        
        
        return self.output,self.phone_number,self.email,self.gender,self.city, self.output_names

     
    def saveAscsv(self,list_of_hrefs,phone_number,email,gender,city,nameofuser):
        self.list_of_hrefs = list_of_hrefs
        self.phone_number = phone_number
        self.email = email
        self.gender = gender
        self.user = nameofuser
        self.city = city
        print(self.list_of_hrefs)
        print(self.phone_number)
        print(self.email)
        print(self.gender)
        print(self.user)
        print(self.city)
        self.df = pd.DataFrame({'Username':self.user,'Facebook Links': self.list_of_hrefs,
                           'Phone Number': self.phone_number,
                            'Email':self.email,
                            'Gender':self.gender,
                            'City':self.city

                                })
        self.df.to_csv('Custom_extraction_FB.csv') 

 
    
    
email = ""
password = ""
facebook = Account_Scraper(email,password)
hrefs,phone_num,email,gender, nameofuser, city = facebook.signIn()
facebook.saveAscsv(hrefs,phone_num,email,gender, nameofuser, city)

