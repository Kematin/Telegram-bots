from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException        


from bs4 import BeautifulSoup
import requests
import lxml
from data import data_list

password = data_list['password']
username = data_list['username']



class Parsing():
	def get_weak(self, weak):
		self.weak = weak

	def get_day(self, day):
		self.day = day

	def check_weakness(self):
		if self.weak.lower() == 'текущая неделя': 
			return 'https://cop.admhmao.ru/journal-app/u.268/week.0'
		else: 
			return 'https://cop.admhmao.ru/journal-app/u.268/week.-1'
		
		

	def main_method(self, url):
		day = self.day
		self.driver = webdriver.Firefox(executable_path='firefox/geckodriver.exe')
		self.driver.get(url)
		self.wait = WebDriverWait(self.driver, 500)
		sleep(3)

		self.authorize()
		main_url = self.check_weakness()
		self.driver.get(main_url)
		print('Начинаю брать значения')


		days, hometasks = self.for_all_days()
		self.driver.close()
		return days, hometasks

	


	def authorize(self):
		self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), ' Вход для обучающихся')]")))
		self.driver.find_element_by_xpath("//div[contains(text(), ' Вход для обучающихся')]").click()

		self.wait.until(EC.visibility_of_element_located((By.ID, "loginByPwdButton")))
		self.driver.find_element_by_xpath("//input[@type='text']").send_keys(username)
		self.driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
		self.driver.find_element_by_id('loginByPwdButton').click()
		
		self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='GnVjdQb6FSnU3xt89qS1']//div[@class='h2KKN67m6ryve46AoIFq']")))
		self.driver.find_element_by_xpath("//div[@class='GnVjdQb6FSnU3xt89qS1']//div[@class='h2KKN67m6ryve46AoIFq']").click()
		print('Выполнен вход в аккаунт')



	def for_all_days(self):
		all_homeworks = []
		all_tittles = []
		all_tasks = {}

		tittles = self.driver.find_elements_by_xpath("//div[@class='dnevnik-day__header']//div[@class='dnevnik-day__title']")
		for tittle in tittles:
			all_tittles.append(tittle.text)


		homeworks = self.driver.find_elements_by_xpath("//div[@class='dnevnik-lesson']")
		for homework in homeworks:
			all_elements = homework.text.split('\n')
			all_elements.pop(1)
			all_homeworks.append(all_elements)


		for homework in all_homeworks:
			if len(homework) == 2 or (len(homework) == 3 and len(homework[2]) < 7):
				hometask = ['Без задания']

			elif len(homework) in (3, 4, 5) and len(homework[2]) > 7:
				hometask = homework[2:]

			elif len(homework) in (3, 4, 5) and len(homework[2]) < 7:
				hometask = homework[3:]

			name = homework[1] + ' ' + homework[0]
			if len(name) < 6: name = 'Музыка'
			all_tasks[name] = hometask


		return all_tittles, all_tasks


	def check_element(self, xpath):
	    try:
	        self.driver.find_element_by_xpath(xpath)
	    except NoSuchElementException:
	        return False
	    return True


def run(check_week, day, days, hometasks):
	if check_week:
		flag = 0
		for h in hometasks:
			if h[-2] == '2':
				print(days[flag] + '\n')
				flag += 1

			homework = ' '.join(hometasks[h])
			print(f'{h[:-1]}: {homework}')
	else:
		flag = -1
		w_day = {
			'понедельник': 0,
			'вторник': 1,
			'среда': 2,
			'четверг': 3,
			'пятница': 4
		}
		true_day = w_day[day.lower()]

		print(days[true_day])
		for h in hometasks:
			if h[-2] == '2':
				flag += 1

			if flag == true_day:
				homework = ' '.join(hometasks[h])
				print(f'{h[:-1]}: {homework}')

			else: continue		



if __name__ == '__main__':
	print('начало парсера')
	week, day = 'Следующая неделя', 'вторник'
	pars = Parsing(weak=week, day=day)
	days, hometasks = pars.main_method('https://cop.admhmao.ru/')

	if day.lower() in ('понедельник', 'вторник', 'среда', 'четверг', 'пятница'):
		check = False
	else: check = True
	run(check, day, days, hometasks)

