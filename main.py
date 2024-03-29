from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from unidecode import unidecode
from fake_useragent import UserAgent
import flask;
from flask_cors import CORS, cross_origin
import os
from openai import OpenAI

def setup_user(headless=None, ip=None,port=None ):
    try:
        #headless = boolean, headless or not
        #ip = ip
        #port = port
        #RETURNS a setup driver
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--dsiable-dev-shm-usage")
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
    except Exception as e:
        print("Error in setting up driver object", e)
        return None


def get_answers(driver,allHz, allVert,date):
    try:
        #driver = driver object
        #allHz = dictionary
        #allVert = dictionary
        #date = date in MM-DD-YY format
        #9-13 and onword includes numbers in the question
        #driver.get("https://nytcrosswordanswers.org/nyt-crossword-answers-09-04-21/")
        driver.get("https://nytcrosswordanswers.org/nyt-crossword-answers-" + date + "/")
        horizontal = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/article/div/div/div[2]/ul[1]')
        vertical = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/article/div/div/div[2]/ul[2]')
        #process the number as well! may be null for some use cases
        # number = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/article/div/div/div[2]/ul[2]')
        hz = horizontal.text.split("\n") # split data
        vert = vertical.text.split("\n")
        key = 0
        value = 1
        for i in range(len(hz)//2):
            k = process(hz[key])
            v = process(hz[value])
            allHz.append(["0", k, v])
            key +=2
            value+=2
        key=0
        value=1
        for i in range(len(vert)//2):
            k = process(vert[key])
            v = process(vert[value])
            allVert.append(["0", k, v])
            key +=2
            value+=2
    except Exception as e:
        print("Error in getting Answers: ", e)

def get_completion(prompt):
    try:
        # validation for prompt: 
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        content = os.environ.get("PROMPT")%(prompt)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            model="gpt-4",
        )
        response_message = chat_completion.choices[0].message.content
        return response_message
    except Exception as e:
        print("Error with OpenAI call: ", e)
        return "Error in OpenAI call. Please Try again in a few minutes"


def process(toProcess):
    return unidecode(toProcess)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/get-answers/<date>', methods=['GET'])
@cross_origin()
def home(date):
    allHz = []
    allV = []
    driver = setup_user(True)
    if driver == None:
        return [allHz, allV]
    get_answers(driver,allHz, allV, date)
    return [allHz,allV]

@app.route('/get-openAI/<answer>', methods=['GET'])
@cross_origin()
def openAi(answer):
    return get_completion(answer)

if __name__=="__main__":
    app.run(debug=True, port=5000)

