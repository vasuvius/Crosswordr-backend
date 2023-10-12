from fastapi import FastAPI
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import json
app = FastAPI()


@app.get("/crossword-answers")
def getAnswers(date):
  driver = setup_user()
  allHz = {}
  allVert={}
  get_answers(driver, allHz, allVert, date)
  return {allHz, allVert} 


def setup_user(headless=None, ip=None,port=None ):
    #headless = boolean, headless or not
    #ip = ip
    #port = port
    #RETURNS a setup driver
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    if (headless != None and headless):
        options.add_argument('--headless')
    if (ip !=None and port!=None):
        PROXY = ip +":" +port
        print(PROXY)
        options.add_argument("--proxy-server=%s" % PROXY) 
    #options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options, )
    return driver

def get_answers(driver,allHz, allVert,date):
    #driver = driver object
    #allHz = dictionary
    #allVert = dictionary
    #date = date in MM-DD-YY format

    #driver.get("https://nytcrosswordanswers.org/nyt-crossword-answers-09-04-21/")
    driver.get("https://nytcrosswordanswers.org/nyt-crossword-answers-" + date + "/")
    horizontal = driver.find_element(By.XPATH, '//*[@id="post-126612"]/div/div/div[2]/ul[1]')
    vertical = driver.find_element(By.XPATH, '//*[@id="post-126612"]/div/div/div[2]/ul[2]')
    hz = horizontal.text.split("\n") # split data
    vert = vertical.text.split("\n")
    key = 0
    value = 1
    for i in range(len(hz)//2):
        allHz[hz[key]] = hz[value]
        key +=2
        value+=2
    key=0
    value=1
    for i in range(len(vert)//2):
        allVert[vert[key]] = vert[value]
        key +=2
        value+=2