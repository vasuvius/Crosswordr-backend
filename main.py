from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from unidecode import unidecode
from fake_useragent import UserAgent
import flask;
from flask_cors import CORS, cross_origin

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
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver

def get_answers(driver,allHz, allVert,date):
    #driver = driver object
    #allHz = dictionary
    #allVert = dictionary
    #date = date in MM-DD-YY format
    #9-13 and onword includes numbers in the question
    #driver.get("https://nytcrosswordanswers.org/nyt-crossword-answers-09-04-21/")
    driver.get("https://nytcrosswordanswers.org/nyt-crossword-answers-" + date + "/")
    horizontal = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/article/div/div/div[2]/ul[1]')
    vertical = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/article/div/div/div[2]/ul[2]')
    hz = horizontal.text.split("\n") # split data
    vert = vertical.text.split("\n")
    key = 0
    value = 1
    for i in range(len(hz)//2):
        k = process(hz[key])
        v = process(hz[value])
        allHz[k] = v
        key +=2
        value+=2
    key=0
    value=1
    for i in range(len(vert)//2):
        k = process(vert[key])
        v = process(vert[value])
        allVert[k] = v
        key +=2
        value+=2

def process(toProcess):
    return unidecode(toProcess)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/get-answers/<date>', methods=['GET'])
@cross_origin()
def home(date):
    allHz = {}
    allV = {}
    driver = setup_user(True)
    get_answers(driver,allHz, allV, date)
    return [allHz,allV]

app.run()