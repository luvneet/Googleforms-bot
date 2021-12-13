import random
import threading
import math
from flask import Flask, request, render_template
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
import json

count = 106
ml = False
tf = False
val = 1
chrome_options = FirefoxOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized")
radio_options = "EcW08c"

app = Flask(__name__, template_folder=r'C:\Users\lovneet\Desktop\gforms')
total = 150
percents = [(34.9, 55.6, 4.5, 5), (22.2, 9.5, 12.7, 6, 7.9, 14.3, 25.4, 2), (73, 11.1, 15.9), (76.2, 15.9, 7.9),
            (11.1, 17.5, 71.4), (12.7, 42.9, 6, 20.6, 5, 9.5, 3.3), (69.8, 23.8, 3, 3.4), (42.9, 46, 11.1),
            (11.1, 14.3, 74.6), (90.5, 9.5), (92.1, 7.9), (4, 41.3, 49.2, 5.5), (71.4, 4.8, 23.8), (45, 35, 20),
            (52.4, 47.6), (76.2, 6.4, 9.5, 7.9), (15.9, 76.2, 7.9), (33.3, 50.8, 15.9), (14.3, 57.1, 17.5, 11.1),
            (74.6, 14.3, 11.1)]  # here goes percentage
persons = {}
response = 100  # Here goes no of respondents.
link = 'https://docs.google.com/forms/....'  # here goes Google form link.


def fillForm(link_):
    global tf
    global count
    global val
    global ml
    try:
        driver = webdriver.Firefox(executable_path="....", options=chrome_options)  # here goes gecko driver ink.
        if not ml:
            val = 1
        for m in range(val):
            temp = count
            count += 1
            driver.get(link_)
            time.sleep(2)
            questions = driver.find_elements_by_css_selector('[class="freebirdFormviewerViewNumberedItemContainer"]')
            for question_ in questions:
                try:
                    que = question_.find_element_by_css_selector('[jscontroller="eFy6Rc"]')
                    choices1 = que.find_elements_by_css_selector('[jscontroller="EcW08c"]')
                    num = persons['{}'.format(temp)][questions.index(question_)]
                    choices1[num].click()

                except:
                    que = question_.find_element_by_css_selector('[jscontroller="tjSPQb"]')
                    try:
                        lines = WebDriverWait(que, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                                 '[class="appsMaterialWizToggleRadiogroupGroupContainer exportGroupContainer freebirdFormviewerComponentsQuestionGridRowGroup"]')))
                        for line in lines:
                            choices3 = line.find_elements_by_css_selector('[jscontroller="EcW08c"]')
                            num = persons['{}'.format(temp)][questions.index(question_)]
                            choices3[num].click()
                    except:
                        pass
            #                choices2 = question.find_elements_by_css_selector('[jscontroller="D8e5bc"]')
            driver.find_element_by_xpath("//*[contains(text(), 'Submit')]").click()

            time.sleep(2)
        tf = True
        ml = False
        val = 1
        driver.quit()
    except:
        pass


def multiRun(key1, key2):
    global tf
    global ml
    global val
    tf = False
    if int(key2) > 4:
        ml = True
        val = math.ceil(int(key2) / 4)
        key2 = 4
    for i in range(int(key2)):
        threading.Thread(target=fillForm, args=(key1,)).start()
        time.sleep(3)
    time.sleep(5)


def formFill(key1, key2):
    try:
        multiRun(key1, key2)
        while True:
            if tf:
                print(f'{key2} times form fill done.')
    except Exception as e:
        print(e)
        print('Error in filling your form,your form might contain questions other than MCQ or have email verification')


for n in range(total):
    a_d = {f"{(n + 1)}": []}
    persons.update(a_d)

mno = 1
for question in percents:
    for option in question:
        rispondant = (math.floor(option * 1.5))
        for ko in range(rispondant):
            persons['{}'.format(mno)].append(question.index(option))
            mno += 1

    mno = 1

formFill(link, response)
