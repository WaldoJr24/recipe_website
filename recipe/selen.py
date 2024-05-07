from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

print("inside selenium script") 

s = Service(executable_path='E:\chromedriver.exe')

driver = webdriver.Chrome(service=s)

website = '127.0.0.1:5000/login'

driver.get(website)

title="titleEgal"

passwords = ["passwordEgal", "gal", "teeeest", "1234"]

i=0


for passw in passwords:
    print("test with password", passw)
    res = driver.find_element(By.CLASS_NAME, "form-control")

    res[0].clear()
    res[0].send_keys("Dennis")
    res[1].clear()
    res[1].send_keys(passw)

    but = driver.find_element(By.CLASS_NAME, "btn")
    assert(len(but) == 1)   
    but[0].click()

    print(driver.title)

    if driver.title == "Login":
        print(f"PASSW 0", passw)
