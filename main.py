import subprocess
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from time import sleep
import argparse

parser = argparse.ArgumentParser(description="ICS Boot",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-u",'--username', help="github username", required=True)
parser.add_argument("-p",'--password', help="github password", required=True)
parser.add_argument("-pr",'--projectname', help="sh project name", required=True)
parser.add_argument("--filestore", action="store_false", help="download with filestore")
parser.add_argument("--headless", action="store_true", help="run chrome hidden")
args = parser.parse_args()
config = vars(args)
# print(config)
os.environ['WDM_LOG']="0"
os.environ['WDM_LOG_LEVEL']="0"
options= Options()
options.headless=config.get("headless")
# install chromeDriver in not exist in cache
print("open borwser ...",end="\r")
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
# constants
USERNAME= config.get("username") #"icsboot"
PASSWORD= config.get("password") #"ics.globe.boot2022"
PROJECT_NAME = config.get("projectname") #"ics-globe-odoo15-demo"
WITH_FILE_STORE = config.get("filestore")
odoo_sh_backup_url = f"https://www.odoo.sh/project/{PROJECT_NAME}/branches/production/backups"
# browser.get(odoo_sh)
print("\nDone")
print("open project link ... ",end="\r")
browser.get(odoo_sh_backup_url)
print("\nDone")
print("start lgin ... ",end="\r")
browser.find_element(by=By.ID,value="login_field").send_keys(USERNAME)
browser.find_element(by=By.ID,value="password").send_keys(PASSWORD)
browser.find_element(by=By.NAME,value="commit").click()
try:
   WebDriverWait(driver=browser,timeout=5).until(
    expected_conditions.presence_of_element_located((By.ID,"js-oauth-authorize-btn"))
).click()
except Exception:
    pass

print("\nDone")
print("get project build id ... ",end="\r")
# _________________________get project build id_________________________
project_build_id_xpath = "//li[@data-branch-name='production']"
project_build_id =WebDriverWait(driver=browser,timeout=1000).until(
    expected_conditions.presence_of_element_located((By.XPATH,project_build_id_xpath))
).get_attribute("data-build-id") 
print("\nDone")
print("backups container load ... ",end="\r")
# _________________________ wait until backup container load _________________________
backup_container = WebDriverWait(driver=browser,timeout=1000).until(
    expected_conditions.presence_of_element_located((By.CLASS_NAME,"o_branch_backups"))
)
print("\nDone")
print("get all buckups row  ... ",end="\r")
#  _________________________ get all buckups row _________________________
backups_item=backup_container.find_elements(by=By.CLASS_NAME,value="o_branch_backups_item")
# _________________________ get last backup datetime _________________________
print("\nDone")
print("get last backup datetime ... ",end="\r")
last_backup_datetime_utc=backups_item[1].find_element(by=By.CLASS_NAME,value="col-2").text
print("\nDone")
print("choose backup link options ... ",end="\r")
# _________________________create backup link _________________________

backups_item[1].find_element(by=By.CLASS_NAME,value="o_make_backup").click()
print("\nDone")
# browser.find_element(by=By.XPATH,value="//footer[@hasclass='modal-footer']/button[@hasclass='btn-primary']")


if WITH_FILE_STORE :
    WebDriverWait(driver=browser,timeout=1000).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME,"modal-dialog"))
    ).find_element(by=By.ID,value="filestore_2").click()
WebDriverWait(driver=browser,timeout=1000).until(
    expected_conditions.presence_of_element_located((By.CLASS_NAME,"modal-dialog"))
).find_element(by=By.CLASS_NAME,value="btn-primary").click()
# print("waiting to generate backup link ...")
WebDriverWait(driver=browser,timeout=1000).until(
        expected_conditions.visibility_of_element_located((By.CLASS_NAME,"fa-cog"))
    )
try:
    print("A backup operation is in progress... ",end="\r")
    #  A backup operation is in progress...
    WebDriverWait(driver=browser,timeout=10000).until(
        expected_conditions.invisibility_of_element((By.CLASS_NAME,"fa-cog"))
    )
    backup_link = f"https://eupp51.odoo.com/paas/build/{project_build_id}/download/dump?backup_datetime_utc={last_backup_datetime_utc}&test_dump=1&filestore={1 if WITH_FILE_STORE else 0}"
    print("\nDone")
    print("start download... ... ",end="\r")
    browser.get(backup_link)
    
    exist_backup_counter = int(subprocess.run(f'ls | grep "^{PROJECT_NAME}.*.zip$" | wc -l',shell=True,capture_output=True).stdout.strip().decode('utf-8'))
    while exist_backup_counter == int(subprocess.run(f'ls | grep "^{PROJECT_NAME}.*.zip$" | wc -l',shell=True,capture_output=True).stdout.strip().decode('utf-8')):
        sleep(5)
        continue
    browser.quit()
    print("\nDone")
except Exception :
    print("failed to construct backup link")