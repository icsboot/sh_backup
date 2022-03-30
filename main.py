from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
import os
import requests
import wget
import io
import zipfile
os.environ['WDM_LOG']="0"
os.environ['WDM_LOG_LEVEL']="0"
options= Options()
options.headless=True

# install chromeDriver in not exist in cache
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

# odoo_sh = "https://www.odoo.sh/web/login"
project_name = "ics-globe-odoo15-demo"
odoo_sh_backup_url = f"https://www.odoo.sh/project/{project_name}/branches/production/backups"
# browser.get(odoo_sh)
browser.get(odoo_sh_backup_url)

# login
username= "icsboot"
password= "ics.globe.boot2022"
browser.find_element(by=By.ID,value="login_field").send_keys(username)
browser.find_element(by=By.ID,value="password").send_keys(password)
browser.find_element(by=By.NAME,value="commit").click()

# browser.find_elements(by=By.CLASS_NAME,value="o_branch_backups_item")

# _________________________ get project build id _________________________
project_build_id =WebDriverWait(driver=browser,timeout=1000).until(
    expected_conditions.presence_of_element_located((By.XPATH,"//li[@data-branch-name='production']"))
).get_attribute("data-build-id") 
# _________________________ wait until backup container load _________________________
backup_container = WebDriverWait(driver=browser,timeout=1000).until(
    expected_conditions.presence_of_element_located((By.CLASS_NAME,"o_branch_backups"))
)
#  _________________________ get all buckups row _________________________
backups_item=backup_container.find_elements(by=By.CLASS_NAME,value="o_branch_backups_item")
# _________________________ get last backup datetime _________________________
last_backup_datetime_utc=backups_item[1].find_element(by=By.CLASS_NAME,value="col-2").text
# _________________________create backup link _________________________
backups_item[1].find_element(by=By.CLASS_NAME,value="o_make_backup").click()

# browser.find_element(by=By.XPATH,value="//footer[@hasclass='modal-footer']/button[@hasclass='btn-primary']")
WebDriverWait(driver=browser,timeout=1000).until(
    expected_conditions.presence_of_element_located((By.CLASS_NAME,"modal-dialog"))
).find_element(by=By.CLASS_NAME,value="btn-primary").click()
print("waiting to generate backup link ...")
WebDriverWait(driver=browser,timeout=1000).until(
        expected_conditions.visibility_of_element_located((By.CLASS_NAME,"fa-cog"))
    )

# sleep(5)
# browser.find_element(by=By.ID,value="modal-dialog").find_element(by=By.CLASS_NAME,value="btn-primary").click()
try:
    #  A backup operation is in progress...
    WebDriverWait(driver=browser,timeout=10000).until(
        expected_conditions.invisibility_of_element((By.CLASS_NAME,"fa-cog"))
    )
    backup_link = f"https://eupp51.odoo.com/paas/build/{project_build_id}/download/dump?backup_datetime_utc={last_backup_datetime_utc}&test_dump=1&filestore=0"
    print(backup_link)
    browser.get(backup_link)
    # downloaded_backup=requests.get(url=backup_link,cookies={'domain': 'github.com', 'httpOnly': 'True', 'name': '_gh_sess', 'path': '/', 'sameSite': 'Lax', 'secure': "True", 'value': r'phycNaCGi0F16Nm81dspQxerTHAFjs1MsymiBnah%2FZw4gk%2F%2BWz2eViZ030eyuuWp5tB0fwY5ztnP8femqLmaffEhAWA3nVD%2F4sWpMFg6%2Fj1JTWyKlsKbpR8%2BykVdsi7u1g%2BxCmJPKz3dkFYKNSCtckmJsA4mNs4nz3YrJWQSPTJm2dYv6E4nxcu2ry56xKE9xoWVPc%2Be9CzAROZX8pURvc%2FMEX%2Bkwj%2FyEPMYMo%2BmG%2BqSTHo9riBE%2By1GIaarZ9rvuUwMA%2Fi7HmoITZHGe%2FOSTw%3D%3D--v0f%2FP8T2hotZNEPP--cgooAPD5LBDOG0JqOAFWng%3D%3D'})
    # zbackup = zipfile.ZipInfo(io.BytesIO(downloaded_backup.content))
    # r = requests.get(backup_link, stream=True)
    # with open("data.zip", 'wb') as fd:
    #     for chunk in r.iter_content():
    #         fd.write(chunk)
    # open('data.zip','wb').write(downloaded_backup.content)
except Exception :
    print("failed to construct backup link")