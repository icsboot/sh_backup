from turtle import back
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# install chromeDriver in not exist in cache
browser = webdriver.Chrome(ChromeDriverManager().install())

# odoo_sh = "https://www.odoo.sh/web/login"
project_name = "ics-globe-odoo15-demo"
odoo_sh_backup_url = f"https://www.odoo.sh/project/{project_name}/branches/production/backups"
# browser.get(odoo_sh)
browser.get(odoo_sh_backup_url)
# login
browser.find_element(by=By.ID,value="login_field").send_keys("")
browser.find_element(by=By.ID,value="password").send_keys("")
browser.find_element(by=By.NAME,value="commit").click()

# browser.find_elements(by=By.CLASS_NAME,value="o_branch_backups_item")

# _________________________ get project build id _________________________
project_build_id = browser.find_element(by=By.XPATH,value="//li[@data-branch-name='production']").get_attribute("data-build-id")
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
# browser.find_element(by=By.ID,value="modal-dialog").find_element(by=By.CLASS_NAME,value="btn-primary").click()
try:
    #  A backup operation is in progress...
    WebDriverWait(driver=browser,timeout=1000).until(
        expected_conditions.invisibility_of_element((By.CLASS_NAME,"fa-cog"))
    )
    backup_link = f"https://eupp51.odoo.com/paas/build/{project_build_id}/download/dump?backup_datetime_utc={last_backup_datetime_utc}&test_dump=1&filestore=0"
    print(backup_link)
except Exception :
    print("failed to construct backup link")