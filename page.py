import csv
from collections import namedtuple
from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def openJIRA(jSessionId):
    driver.get("https://support.flatironssolutions.com")
    cookie = {'name':'JSESSIONID', 'value':jSessionId}
    driver.add_cookie(cookie)
    driver.get_cookies()
    driver.get("https://support.flatironssolutions.com/browse/RDSANDBOX-723")
    try:
        driver.find_element_by_id("login-form")
        raise Exception("Failed to login JIRA")
    except NoSuchElementException:
        pass;


def openCreateDialog():
    elem = driver.find_element_by_id("create_link")
    elem.click()
    wait.until(EC.presence_of_element_located((By.ID, "customfield_11591-field")))

def inputEpic():
    elem = driver.find_element_by_id("customfield_11591-field")
    elem.send_keys("DSANDBOX-665")
    wait.until(EC.visibility_of_element_located((By.ID, "showing-1-of-1-matching-epics")))
    elem.send_keys("\t")

def inputSummary(content):
    elem = driver.find_element_by_id("summary")
    elem.send_keys(content)
    elem.send_keys("\t")

def inputSecurity():
    elem = driver.find_element_by_xpath("//select[@id='security']/option[@value='10401']")
    elem.click()

def inputDesc(content):
    elem = driver.find_element_by_id("description")
    elem.send_keys(content)
    elem.send_keys("\t")

def makeDesc(item):
    newline = Keys.SHIFT + Keys.ENTER + Keys.SHIFT
    return 'As a {item.role}, I can {item.summary}{newline}{newline}*References:*{newline}* {item.reference}{newline}{newline}*Acceptance Criteria:*{newline}* '.format(item=item, newline=newline).replace("|","\n")


def inputLabels(labels):
    elem = driver.find_element_by_id("labels-textarea")
    elem.send_keys(labels)
    elem.send_keys("\t")

def makeLabels(item):
    return '{item.product} Level_{item.level} Development_ramup'.format(item=item)

def submit():
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "issue-created-key")))
    driver.find_element_by_id("create-issue-submit").click()


def findNewTicketURL():
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "issue-created-key")))
    elem = driver.find_element_by_class_name("issue-created-key")
    return elem.get_attribute("data-issue-key")

def createTicket(item):
    openCreateDialog()
    inputEpic()
    inputSummary(item.summary)
    inputSecurity()
    inputDesc(makeDesc(item))
    inputLabels(makeLabels(item))
    submit()
    return findNewTicketURL()


def defineArgs():
    parser = ArgumentParser()
    parser.add_argument('-j', dest='jSessionId', help='Requestion cookie', type=str, default='0D66B71F5785CA9ABCB6CB25E116377E')
    parser.add_argument('-i', dest='input', help='input csv file', type=str, default='ppt-dev.csv')
    parser.add_argument('-o', dest='output', help='output md file', type=str, default='ppt-dev.md')
    return parser.parse_args()

Item = namedtuple('Item', 'product level role role_short summary reference') 

if __name__ == '__main__':
    args = defineArgs()
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    openJIRA(args.jSessionId)
    with open(args.output, "wt") as out:
        print('|| Level || As a || Description ||', file=out)
        for item in map(Item._make, csv.reader(open(args.input, "rt"))):
            id = createTicket(item)
            url = "https://support.flatironssolutions.com/browse/"+id
            print('| {item.level} | {item.role_short} | [I can {item.summary}|{url}]'.format(item=item, url=url), file=out)

'''
    driver.close()
'''
