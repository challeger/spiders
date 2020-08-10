from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.jianshu.com/p/be81b1987af1')

while True:
    try:
        next_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label=展开更多]'))
        )
        driver.execute_script('arguments[0].click();', next_btn)
    except Exception as e:
        print(e)
        break
