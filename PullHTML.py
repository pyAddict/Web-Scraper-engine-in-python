#Selenium is used to login in a website by a program
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
def write_html(path,url):
	driver=webdriver.Chrome();
	driver.get(url);
	#At the starting of sbi page we have to click Continue Login 
	driver.find_element_by_xpath("html/body/div[1]/div/div[2]/div[2]/div/a").click()
	#To find the user name option in webpage
	username=driver.find_element_by_xpath('html/body/div[1]/div/div[4]/form/div[2]/div[1]/div/input[1]');
	#To fill the user name
	username.send_keys("************")
	#To find the password block
	password=driver.find_element_by_xpath('html/body/div[1]/div/div[4]/form/div[2]/div[1]/div/input[2]');
	time.sleep(3)
	#To fill the password part
	password.send_keys("***********")
	#To click the login button
	driver.find_element_by_xpath("html/body/div[1]/div/div[4]/form/div[2]/div[1]/div/div/input[1]").click()
	time.sleep(3)
	#To enter in the Past 10 transaction link
	#driver.find_element_by_xpath("html/body/form/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td/table[6]/tbody/tr[3]/td[4]/a").click()
	#time.sleep(3)
	#To enter in the account summary
	driver.find_element_by_xpath("html/body/form/table[2]/tbody/tr/td/table[1]/tbody/tr/td[1]/table/tbody/tr[3]/td/ul/li[2]/a").click()
	time.sleep(3)
	#To enter in the last six month data
	driver.find_element_by_xpath("html/body/form/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td/form[2]/table[1]/tbody/tr[5]/td[3]/label").click()
	time.sleep(3)
	#for pressing the go button
	driver.find_element_by_xpath("html/body/form/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td/form[2]/table[1]/tbody/tr[9]/td/div/table/tbody/tr[4]/td/input").click();
	time.sleep(3)
	
	#To save the current page as sbi.html
	elem = driver.find_element_by_xpath("//*")
	source_code = elem.get_attribute("outerHTML")
	f = open(path+"/name.html", 'w')
	f.write(source_code.encode('utf-8'))
	f.close()
	driver.quit()

if __name__ == '__main__':
	path="/home/maulo/2Project/data"
	#SBI web page address
	url="desired url"
	write_html(path,url)

